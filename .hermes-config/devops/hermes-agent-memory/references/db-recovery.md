# DB Recovery: Corrupt SQLite Hermes Databases

## When to Use
- `PRAGMA integrity_check` returns errors
- `sqlite3 ATTACH` fails silently or with WAL errors
- DB file exists but queries return unexpected empty results
- Hermes session data or Mnemosyne memories appear "lost" after migration

## Recovery Procedure

### Step 1: Dump the corrupt DB
```bash
sqlite3 corrupt.db ".dump" > /tmp/recovery.sql
```
This often succeeds even when integrity_check fails, because `.dump` reads row-by-row.

### Step 2: Rebuild clean DB
```bash
sqlite3 clean.db < /tmp/recovery.sql
```
Verify: `sqlite3 clean.db "PRAGMA integrity_check;"` → should return `ok`

### Step 3: Merge into live DB using Python
sqlite3 ATTACH often fails on WAL-corrupt DBs. Use Python instead:

```python
import sqlite3

live = sqlite3.connect("live.db")
rec = sqlite3.connect("clean.db")
live_cur = live.cursor()
rec_cur = rec.cursor()

# Get common columns
live_cur.execute("PRAGMA table_info(target_table)")
live_cols = [r[1] for r in live_cur.fetchall()]
rec_cur.execute("PRAGMA table_info(target_table)")
rec_cols = [r[1] for r in rec_cur.fetchall()]
common = [c for c in rec_cols if c in live_cols]

# Fetch and insert
rec_cur.execute(f"SELECT {','.join(common)} FROM target_table WHERE timestamp < 'cutoff'")
rows = rec_cur.fetchall()
ph = ','.join(['?' for _ in common])
ins = f"INSERT OR IGNORE INTO target_table ({','.join(common)}) VALUES ({ph})"
live_cur.executemany(ins, rows)
live.commit()
```

### Step 4: Verify
```bash
sqlite3 live.db "SELECT COUNT(*) FROM target_table;"
sqlite3 live.db "SELECT MIN(timestamp), MAX(timestamp) FROM target_table;"
```

## Known Recoverable DBs (as of 2026-06-08)
- `~/.hermes/mnemosyne/data/mnemosyne.db.corrupt` — pre-June-7 Mnemosyne data
- `~/.hermes/mnemosyne/data/mnemosyne.db.corrupt2` — duplicate
- Both successfully recovered and merged into live Mnemosyne DB

## Prevention
- Always create a `.backup-YYYYMMDD-HHMMSS` before schema migrations
- Run `PRAGMA integrity_check` after any DB modification
- The `combined-backup.sh` cron handles this for all SQLite DBs on Sundays
