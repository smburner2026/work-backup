# SQLite Schema Drift in Persistent Services

## The Pattern

A long-running service uses `CREATE TABLE IF NOT EXISTS` for initial schema
setup, then `ALTER TABLE ... ADD COLUMN` (via a migration function) for
additive schema changes. A code update adds new columns to the `CREATE TABLE`
statement. On restart, the service:

1. Runs `CREATE TABLE IF NOT EXISTS` — SQLite sees the table exists, skips it;
   new columns from the `CREATE TABLE` statement are **never created**.
2. Runs the migration function — which checks `PRAGMA table_info()` against a
   hardcoded column list and adds any missing ones with `ALTER TABLE`.
3. **But** if the connection is cached (e.g. `_INITIALIZED_PATHS` set in the
   process), step 2 is skipped on subsequent calls. The migration only runs
   on the *first* connection. Threads or dispatcher ticks that open
   connections later inherit the stale schema.

## Symptom

```
sqlite3.OperationalError: no such column: <column_name>
```

Appears **minutes into runtime**, not at startup — because the error only
fires when the code path that *queries* or *indexes* the column actually
executes (e.g. a dispatcher tick, a scheduled job, an API handler).

The service itself doesn't crash immediately. It logs the error and keeps
running, but the error recurs every time that code path triggers.

## Root Cause

The `CREATE TABLE IF NOT EXISTS` statement in the migration worked fine for a
clean DB, but became a no-op on upgrade. The migration function should have
added the column — but was in a code path gated by a process-wide cache
(`_INITIALIZED_PATHS`) so it only fires on the *very first* `connect()` call.
If the migration code was added in a deploy that started *before* the schema
update, the cached init path skips re-migration.

Specifically, this ordering is fragile:

```python
def connect():
    if path not in _INITIALIZED_PATHS:
        conn.executescript(SCHEMA_SQL)            # CREATE TABLE IF NOT EXISTS — no-op on existing table
        _migrate_add_optional_columns(conn)       # ALTER TABLE — adds missing columns
        _INITIALIZED_PATHS.add(path)              # cached!
    return conn
```

The first process to start with the new code runs the migration correctly
and caches the path. If the gateway restarts (exit code 75 → systemd relaunch),
the new process's `_INITIALIZED_PATHS` is empty, so it should re-run the
migration. But if a third party (another process, a concurrent thread) opens
a connection without going through `connect()`, or if the `_INITIALIZED_PATHS`
persists across restarts via a global (e.g. module-level cache in a
long-running daemon), the schema drift becomes permanent until a full process
kill + fresh start.

## Detection

```bash
# 1. Check the actual schema
python3 -c "
import sqlite3
conn = sqlite3.connect('/path/to/db.sqlite')
cols = [r[1] for r in conn.execute('PRAGMA table_info(tasks)')]
print('columns:', cols)
print('session_id in cols:', 'session_id' in cols)
"

# 2. Grep the code for migration logic
grep -n 'ADD COLUMN\|_migrate_add_optional\|PRAGMA table_info' kanban_db.py

# 3. Check gateway logs for the repeated error pattern
grep 'no such column' ~/.hermes/logs/gateway.log
```

## Fix

```python
python3 -c "
import sqlite3
conn = sqlite3.connect('/path/to/db.sqlite')
cols = [r[1] for r in conn.execute('PRAGMA table_info(tasks)')]
for col_name in ['session_id', 'branch_name']:
    if col_name not in cols:
        conn.execute(f'ALTER TABLE tasks ADD COLUMN {col_name} TEXT')
        print(f'Added {col_name} column')
conn.commit()
# Create indexes after columns exist
conn.execute('CREATE INDEX IF NOT EXISTS idx_tasks_session_id ON tasks(session_id)')
conn.commit()
print('Done')
"
```

After fixing the DB, reset the failed systemd state:

```bash
systemctl --user reset-failed hermes-gateway
```

Then restart the service.

## Prevention

- Do not put additive columns only in `CREATE TABLE IF NOT EXISTS`. The
  migration function (`_migrate_add_optional_columns`) should be the single
  source of truth for schema additions, and it must run on **every**
  connection open, not just the first one.
- Or: remove the caching (`_INITIALIZED_PATHS`) and make schema init
  idempotent for every connection (cheap: `CREATE TABLE IF NOT EXISTS` +
  `ALTER TABLE ADD COLUMN IF NOT EXISTS` — though SQLite doesn't have
  `IF NOT EXISTS` for `ALTER TABLE`, so you need the `PRAGMA table_info`
  check every time).
- When deploying a schema change, stop the service entirely first, then
  start fresh — don't rely on graceful restarts (exit 75) that may race
  with connection caching.

## Related: Gateway Exit Code 75 + Systemd RestartSteps

The Hermes gateway uses exit code 75 (TEMPFAIL) as a self-restart signal.
Systemd's `RestartForceExitStatus=75` triggers a restart, but when
`RestartSteps=N` and `RestartSec=S` are set, the delay increases
exponentially (step × base_sec). A manual `systemctl start` during this
backoff can block longer than expected.

`systemctl --user reset-failed hermes-gateway` clears the restart counter
and lets a manual start proceed immediately.
