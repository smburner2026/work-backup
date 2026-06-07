---
name: disk-full-mnemosyne-recovery
description: Recover from a full disk that corrupted Mnemosyne SQLite database — triage, reclaim space, repair DB, restart gateways.
category: devops
trigger: Mnemosyne returns "database or disk is full" OR any Hermes tool fails with disk-full/db-locked errors.
---

# Disk Full + Mnemosyne Corruption Recovery

## Detection

When Mnemosyne returns `OperationalError: database or disk is full`, FIRST determine whether disk is actually full or it's a stale cached error.

## Triage: Is disk actually full?

```bash
df -h /
```

- **Disk ≥ 85% used** → Likely a genuine full-disk incident. Proceed to "Full Disk Recovery" below.
- **Disk < 85% used** → This is a **false alarm** — a cached in-memory error state from a past corruption. Skip to "Cached Error State Recovery".

## Cached Error State Recovery (Disk NOT Full)

When disk has space but the error persists, the Mnemosyne Python module has cached the `SQLITE_FULL` error once and never retries — even after the underlying cause (WAL corruption, disk filling up temporarily) is resolved. The DB itself is likely healthy.

```bash
# 0. Quick sanity: check if DB is actually healthy
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "PRAGMA integrity_check;"

# 1. Clean up leftover corruption artifacts
ls -la ~/.hermes/mnemosyne/data/*.corrupt 2>/dev/null
rm -v ~/.hermes/mnemosyne/data/*.corrupt 2>/dev/null

# 2. Restart the gateway (clears cached error from gateway Python process)
hermes gateway restart
```

After gateway restart, the error clears for:
- Gateway-mediated sessions (Discord, Telegram, API server)
- New CLI sessions started after the restart (`hermes chat`)

**Still seeing the error in your current CLI session?** That's expected — each `hermes chat` process has its own Python process with its own Mnemosyne connection and its own cached error. Issue `/reset` or start a fresh `hermes` invocation to get a clean memory connection.

**DB integrity check failed?** Then the DB is genuinely corrupt despite having disk space — fall through to "Step 4: Recover Corrupted Mnemosyne DB" below. The `rm` of `.corrupt` files in step 1 is still safe to run.

## Full Disk Recovery (Disk WAS Full)

When disk actually filled up, you'll see:
- Mnemosyne tools return `OperationalError: database or disk is full`
- Terminal tools may fail silently or time out
- `df -h /` shows 100% Use%
- Agent log (`~/.hermes/logs/agent.log`) shows WARNINGs with "database or disk is full"

## Step 1: Diagnose Space Usage

```bash
# Overall disk
df -h /

# Top-level space hogs
du -sh /* 2>/dev/null | sort -rh | head -15

# User-space hogs
du -sh ~/.* 2>/dev/null | sort -rh | head -15

# Hermes DB sizes
du -sh ~/.hermes/*.db ~/.hermes/mnemosyne/data/
```

**Common space hogs:**
- `/tmp` — OCR temp files, build artifacts (safest to clear)
- `/var/log/journal` — old systemd journals
- `~/.cache` — pip/npm package caches
- `~/.hermes/state.db-wal` — uncheckpointed WAL file

## Step 2: Reclaim Space

```bash
# 1. Clear /tmp (safe — reboot clears it anyway)
rm -rf /tmp/*

# 2. Trim systemd journals (keep last 100M)
journalctl --vacuum-size=100M

# 3. Clear caches (rebuildable)
pip3 cache purge 2>/dev/null || true
npm cache clean --force 2>/dev/null || true

# 4. Checkpoint SQLite WAL files (reclaims wasted space)
sqlite3 ~/.hermes/state.db "PRAGMA wal_checkpoint(TRUNCATE);"
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "PRAGMA wal_checkpoint(TRUNCATE);"
```

## Step 3: Diagnose Mnemosyne Corruption

```bash
# Check if Mnemosyne DB is corrupted
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "PRAGMA integrity_check;"

# If it returns anything other than "ok", it's corrupted
```

## Step 4: Recover Corrupted Mnemosyne DB

The `.dump` + `INSERT OR IGNORE` approach recovers data even with duplicate rows:

```bash
# 1. Backup the corrupt DB
cp ~/.hermes/mnemosyne/data/mnemosyne.db \
   ~/.hermes/mnemosyne/data/mnemosyne.db.corrupt

# 2. Dump to SQL, replacing INSERT with INSERT OR IGNORE to skip duplicates
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db .dump > /tmp/mnemo_dump.sql
sed -i 's/^INSERT INTO annotations VALUES/INSERT OR IGNORE INTO annotations VALUES/' /tmp/mnemo_dump.sql
sed -i 's/^INSERT INTO memories VALUES/INSERT OR IGNORE INTO memories VALUES/' /tmp/mnemo_dump.sql
# Remove transaction wrapper so failures don't roll back everything
sed -i '/^BEGIN TRANSACTION;/d; /^COMMIT;/d; /^ROLLBACK;.*/d' /tmp/mnemo_dump.sql
# Remove trigger manipulation at end
sed -i '/^\/\* WARNING/d; /PRAGMA writable_schema=OFF/d' /tmp/mnemo_dump.sql

# Note: If the import still fails on FTS tables or sqlite_master, fall back to
# deleting the DB so Hermes recreates a fresh one on next gateway start.

# 3. Restore to fresh DB
sqlite3 /tmp/mnemosyne_clean.db < /tmp/mnemo_dump.sql

# 4. Verify
sqlite3 /tmp/mnemosyne_clean.db "PRAGMA integrity_check;"
sqlite3 /tmp/mnemosyne_clean.db "SELECT COUNT(*) FROM memories;"
sqlite3 /tmp/mnemosyne_clean.db "SELECT COUNT(*) FROM annotations;"

# 5. Swap in place
rm -f ~/.hermes/mnemosyne/data/mnemosyne.db-wal ~/.hermes/mnemosyne/data/mnemosyne.db-shm
cp /tmp/mnemosyne_clean.db ~/.hermes/mnemosyne/data/mnemosyne.db

# 6. Cleanup temp files
rm -f /tmp/mnemo_dump.sql /tmp/mnemosyne_clean.db
```

## Step 5: Release Database Locks

Old gateway processes may hold stale SQLite locks:

```bash
# Find processes holding the DB
fuser ~/.hermes/mnemosyne/data/mnemosyne.db

# Identify them
ps -p <PID> -o pid,cmd --no-headers

# Check if they have deleted WAL/SHM file descriptors (stale locks)
ls -la /proc/<PID>/fd/ 2>/dev/null | grep mnemosyne

# Kill stale gateway processes (they auto-restart)
kill <PID>   # SIGTERM first
kill -9 <PID>  # SIGKILL if needed
```

Then restart the gateway:
```bash
hermes gateway run --replace &
```

## Step 6: Verify Recovery

```bash
# Test direct DB access
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "SELECT 'OK', COUNT(*) FROM memories;"

# Mnemosyne should work on next session start (this session may need restart)
```

## Pitfalls

- **Cached error state (Python process in-memory)**: The Mnemosyne module stores `OperationalError` once and never retries — it is not a connection that reconnects. Each Python process (gateway, `hermes chat` session, kanban worker) has its own independent connection and its own cached error. Fixing the DB and restarting the gateway only clears the gateway's copy. All other processes that connected before the fix still hold the stale error. They must be restarted.
- **Check disk before assuming corruption**: `df -h /` is the first triage step. If disk < 85% used, the error is almost certainly a stale cache, not actual corruption. Run the "Cached Error State Recovery" path, not the full dump/restore.
- **`.corrupt` files are recovery debris, not the problem**: When Hermes detects corrupted Mnemosyne files, it renames them to `*.corrupt` and creates a fresh DB. Finding `.corrupt` files means recovery already happened — the fix is cleanup + restart, not another recovery cycle.
- **cp preserves inodes on same filesystem**: When you `cp` over an existing file on the same filesystem, the inode stays the same. This means old file descriptors in other processes still point to the correct file — but with stale locks. You MUST kill those processes.
- **state.db WAL can grow large**: The state.db has FTS indexes that create large WAL files. Checkpoint periodically.
- **OCR temp files**: Book/document OCR pipelines can leave GBs in `/tmp` — check after heavy OCR sessions.
