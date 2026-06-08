---
name: disk-full-mnemosyne-recovery
description: Recover from a full disk that corrupted Mnemosyne SQLite database — triage, reclaim space, repair DB, restart gateways.
category: devops
trigger: Mnemosyne returns "database or disk is full" OR any Hermes tool fails with disk-full/db-locked errors.
---

# Disk Full + Mnemosyne Corruption Recovery

## Detection

When Mnemosyne returns `OperationalError: database or disk is full`, FIRST determine whether disk is actually full or it's a stale cached error.

## Mnemosyne backup selection

When multiple Mnemosyne snapshots exist (`mnemosyne.db`, `mnemosyne.db.backup-YYYYMMDD-HHMMSS`, imported WSL backups), **choose the newest file whose schema/layout matches the running Hermes version**, not the largest file. If schemas match but row counts differ, prefer the higher count.

**Decision rule:**
1. Run `sqlite3 <db> "PRAGMA user_version;"` and compare column lists with `PRAGMA table_info(...)` on candidate DBs.
2. Prefer the DB with more rows when schemas match.
3. Only refuse to replace the live DB if the candidate is smaller OR schema-mismatched.

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

- **DB integrity check failed?** Then the DB is genuinely corrupt despite having disk space — fall through to "Step 4: Recover Corrupted Mnemosyne DB" below. The `rm` of `.corrupt` files in step 1 is still safe to run.

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

## Mnemosyne backup selection

When multiple Mnemosyne snapshots exist (`mnemosyne.db`, `mnemosyne.db.backup-YYYYMMDD-HHMMSS`, imported WSL backups), **choose the newest file whose schema/layout matches the running Hermes version**, not the largest file. If schemas match but row counts differ, prefer the higher count.

**Decision rule:**
1. Run `sqlite3 <db> "PRAGMA user_version;"` and compare column lists with `PRAGMA table_info(...)` on candidate DBs.
2. Prefer the DB with more rows when schemas match.
3. Only refuse to replace the live DB if the candidate is smaller OR schema-mismatched.

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

## Step 7: Cross-Schema Recovery via Python Merge (2026-06-08)

When the corrupt DB has a different schema version than the live DB (e.g., missing `profile_id` column), the `sqlite3 .dump → INSERT OR IGNORE` approach may fail because column counts don't match. The Python merge approach works:

```python
import sqlite3, json

live_conn = sqlite3.connect("/root/.hermes/mnemosyne/data/mnemosyne.db")
rec_conn = sqlite3.connect("/root/.hermes/mnemosyne/data/mnemosyne-clean.db")

live_cur = live_conn.cursor()
rec_cur = rec_conn.cursor()

# Get common columns across schemas
live_cur.execute("PRAGMA table_info(working_memory)")
live_cols = {row[1] for row in live_cur.fetchall()}
rec_cur.execute("PRAGMA table_info(working_memory)")
rec_cols = {row[1] for row in rec_cur.fetchall()}
common = live_cols & rec_cols

# Fetch recovered rows, insert with common columns only
rec_cur.execute(f"SELECT {','.join(common)} FROM working_memory WHERE timestamp < '2026-06-07'")
rows = rec_cur.fetchall()

ph = ','.join(['?' for _ in common])
ins = f"INSERT OR IGNORE INTO working_memory ({','.join(common)}) VALUES ({ph})"
live_cur.executemany(ins, rows)
live_conn.commit()
print(f"Merged {live_cur.rowcount} rows")
```

**Key insight:** `sqlite3 ATTACH` with different schema versions fails silently. Python with explicit column lists is the reliable cross-schema merge strategy.

### Recovery from .corrupt files (2026-06-08)

When Hermes detects DB corruption during schema migration, it creates `.corrupt` or `.corrupt2` files. These files often contain intact data even when the live DB is unreachable. Common scenarios include:
- Live DB has new schema (e.g., with `profile_id` column in `working_memory`)
- Corrupt DB has old schema (missing `profile_id`) PLUS a separate `memories` table (old format)
- Need to merge data from both tables into the current `working_memory` table

**Recovery path:**
```bash
# 1. Check corrupt files exist
ls -la ~/.hermes/mnemosyne/data/*.corrupt*

# 2. Dump the corrupt DB (integrity_check may pass even on "corrupt" files)
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db.corrupt ".dump" > /tmp/mnemosyne_corrupt_dump.sql
sqlite3 /tmp/mnemosyne_clean.db < /tmp/mnemosyne_corrupt_dump.sql

# 3. Merge into live DB using Python merge (handles schema differences and multiple tables)
# See "Cross-Table Merge for Schema Migration" below for detailed Python script
```

Also check for `.backup-*` files — they hold pre-migration state that may have additional rows.

### Cross-Table Merge for Schema Migration (2026-06-08)

When recovering from a schema migration where the corrupt DB contains both:
- A `working_memory` table with the new schema structure but missing recent columns (e.g., `profile_id`)
- A separate `memories` table with the old format (to be merged into `working_memory`)

Use this Python script to perform the merge:

```python
import sqlite3
import os

def merge_corrupted_mnemosyne(live_db_path, corrupt_db_path):
    """Merge data from corrupt Mnemosyne DB into live DB handling schema differences."""
    live_conn = sqlite3.connect(live_db_path)
    corrupt_conn = sqlite3.connect(corrupt_db_path)
    
    live_cur = live_conn.cursor()
    corrupt_cur = corrupt_conn.cursor()
    
    print("=== Starting Mnemosyne Merge ===")
    
    # 1. Merge working_memory table (handle missing columns)
    live_cur.execute("PRAGMA table_info(working_memory)")
    live_wm_cols = [row[1] for row in live_cur.fetchall()]
    
    corrupt_cur.execute("PRAGMA table_info(working_memory)")
    corrupt_wm_cols = [row[1] for row in corrupt_cur.fetchall()]
    
    # Find common columns
    common_wm_cols = [col for col in corrupt_wm_cols if col in live_wm_cols]
    print(f"Working memory - Common columns: {len(common_wm_cols)}")
    
    # Fetch working_memory data from corrupt DB (pre-June-7 to avoid duplicates)
    corrupt_cur.execute(f"""
        SELECT {','.join(common_wm_cols)} 
        FROM working_memory 
        WHERE timestamp < '2026-06-07'
    """)
    wm_rows = corrupt_cur.fetchall()
    print(f"Working memory rows to merge: {len(wm_rows)}")
    
    if wm_rows:
        # Build INSERT statement with placeholders for common columns
        # Add default values for missing columns (e.g., profile_id)
        placeholders = ','.join(['?' for _ in common_wm_cols])
        # Check if profile_id needs to be added
        if 'profile_id' in live_wm_cols and 'profile_id' not in common_wm_cols:
            placeholders += ",'default'"
            insert_cols = common_wm_cols + ['profile_id']
        else:
            insert_cols = common_wm_cols
            
        insert_sql = f"""
            INSERT OR IGNORE INTO working_memory 
            ({','.join(insert_cols)}) 
            VALUES ({placeholders})
        """
        live_cur.executemany(insert_sql, wm_rows)
        live_conn.commit()
        print(f"Working memory merged: {live_cur.rowcount} rows")
    
    # 2. Merge memories table (old format) into working_memory
    corrupt_cur.execute("PRAGMA table_info(memories)")
    mem_cols = [row[1] for row in corrupt_cur.fetchall()]
    print(f"Memories table columns: {mem_cols}")
    
    # Map memories table columns to working_memory columns
    mem_to_wm_map = {
        'id': 'id',
        'content': 'content', 
        'source': 'source',
        'timestamp': 'timestamp',
        'session_id': 'session_id',
        'importance': 'importance',
        'metadata_json': 'metadata_json',
        'created_at': 'created_at'
    }
    
    # Verify all required columns exist
    required_mem_cols = list(mem_to_wm_map.keys())
    missing_mem_cols = [col for col in required_mem_cols if col not in mem_cols]
    if missing_mem_cols:
        print(f"WARNING: Missing columns in memories table: {missing_mem_cols}")
    
    # Fetch memories data (pre-June-7)
    select_cols = [mem_to_wm_map[col] for col in required_mem_cols if col in mem_cols]
    corrupt_cur.execute(f"""
        SELECT {','.join(select_cols)}
        FROM memories
        WHERE timestamp < '2026-06-07'
    """)
    mem_rows = corrupt_cur.fetchall()
    print(f"Memories rows to merge: {len(mem_rows)}")
    
    if mem_rows:
        # Build INSERT statement for working_memory
        # Map memories columns to working_memory columns
        wm_target_cols = []
        wm_placeholders = []
        wm_values = []
        
        for mem_col, wm_col in mem_to_wm_map.items():
            if mem_col in select_cols:
                wm_target_cols.append(wm_col)
                wm_placeholders.append('?')
        
        # Add default for profile_id if needed
        if 'profile_id' in live_wm_cols and 'profile_id' not in wm_target_cols:
            wm_target_cols.append('profile_id')
            wm_placeholders.append("'default'")
        
        if wm_target_cols:
            placeholders = ','.join(['?' for _ in range(len(select_cols))])
            if 'profile_id' in live_wm_cols and 'profile_id' not in [mem_to_wm_map.get(c, c) for c in select_cols]:
                # Need to handle profile_id separately
                insert_sql = f"""
                    INSERT OR IGNORE INTO working_memory 
                    ({','.join(wm_target_cols)}) 
                    VALUES ({','.join(['?' for _ in range(len(select_cols))])},'default')
                """
                # Extract just the values we have from mem_rows
                mem_values_only = [row[:len(select_cols)] for row in mem_rows]
                live_cur.executemany(insert_sql, mem_values_only)
            else:
                insert_sql = f"""
                    INSERT OR IGNORE INTO working_memory 
                    ({','.join(wm_target_cols)}) 
                    VALUES ({','.join(['?' for _ in range(len(select_cols))])})
                """
                live_cur.executemany(insert_sql, mem_rows)
            live_conn.commit()
            print(f"Memories merged: {live_cur.rowcount} rows")
    
    # 3. Merge facts tables (simple INSERT OR IGNORE)
    fact_tables = ['facts', 'memoria_facts', 'memoria_instructions', 'memoria_preferences', 'episodic_memory']
    for table in fact_tables:
        try:
            corrupt_cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = corrupt_cur.fetchone()[0]
            if count > 0:
                corrupt_cur.execute(f"SELECT * FROM {table}")
                rows = corrupt_cur.fetchall()
                if rows:
                    corrupt_cur.execute(f"PRAGMA table_info({table})")
                    cols = [row[1] for row in corrupt_cur.fetchall()]
                    placeholders = ','.join(['?' for _ in cols])
                    insert_sql = f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
                    live_cur.executemany(insert_sql, rows)
                    live_conn.commit()
                    print(f"{table} merged: {live_cur.rowcount} rows")
        except sqlite3.OperationalError as e:
            print(f"Skipping {table}: {e}")
    
    live_conn.close()
    corrupt_conn.close()
    print("=== Merge Complete ===")

# Usage:
# merge_corrupted_mnemosyne(
#     "/root/.hermes/mnemosyne/data/mnemosyne.db",
#     "/root/.hermes/mnemosyne/data/mnemosyne-corrupt.db"
# )
```

**Key insights from 2026-06-08 recovery:**
1. `sqlite3 ATTACH` fails silently when schema versions differ - always use Python with explicit column lists for cross-schema merges
2. When schema migration adds columns (e.g., `profile_id`), provide default values during merge
3. Handle both `working_memory` (schema variant) and `memories` (format variant) tables from pre-migration DBs
4. Always verify merge success with daily distribution checks to ensure no gaps in temporal coverage

**Verification after merge:**
```bash
# Check working memory count and date range
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM working_memory;"

# Verify daily continuity (should see no major gaps)
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "SELECT DATE(timestamp), COUNT(*) FROM working_memory GROUP BY DATE(timestamp) ORDER BY DATE(timestamp);"

# Cross-verify with LCM (should have overlapping date ranges)
sqlite3 ~/.hermes/lcm.db "SELECT MIN(timestamp), MAX(timestamp) FROM messages;"
```

## Cross-Store Verification (2026-06-08)

After any recovery, verify all three stores are consistent:

```bash
# 1. LCM: session_search works
session_search(query="<known topic from recovered period>", limit=5)

# 2. Mnemosyne: recall works
mnemosyne_recall(query="<known fact from recovered period>", limit=5)

# 3. Backup chain ran
ls -lh ~/.hermes/backups/mnemosyne/ ~/.hermes/backups/lcm/ ~/.hermes/backups/dbs/
cd /root/work && git log --oneline -3

# 4. Cross-reference daily counts
sqlite3 ~/.hermes/lcm.db "SELECT SUBSTR(session_id,1,8), COUNT(DISTINCT session_id) FROM messages GROUP BY SUBSTR(session_id,1,8) ORDER BY 1 LIMIT 30;"
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "SELECT DATE(timestamp), COUNT(*) FROM working_memory GROUP BY DATE(timestamp) ORDER BY 1 LIMIT 30;"
```

**Coverage expectation:** LCM sessions and Mnemosyne memories should overlap for post-install dates. Pre-Mnemosyne sessions (before May 18) will have LCM data but no Mnemosyne memories — this is expected.

## Backup Architecture (2026-06-08)

The combined backup chain runs Sundays at 06:00 UTC via `combined-backup.sh`:

1. `work-backup.sh` — git commit/push config/skills to GitHub
2. `backup-archive-sessions.sh` — compress sessions older than 7 days to `.gz`
3. `backup-mnemosyne.sh` — daily Mnemosyne snapshot (keep 7, promote to git on Sundays)
4. `backup-lcm.sh` — weekly LCM snapshot (keep 4, promote to git on Sundays)
5. `backup-other-dbs.sh` — weekly kanban/response_store/state snapshots (keep 2)

**Off-site gap:** GitHub covers config/skills/sessions. SQLite DBs (Mnemosyne, LCM, kanban, state) are local-only. Cloud backup (B2) is planned but not yet configured.

## Pitfalls

- **Cached error state (Python process in-memory)**: The Mnemosyne module stores `OperationalError` once and never retries — it is not a connection that reconnects. Each Python process (gateway, `hermes chat` session, kanban worker) has its own independent connection and its own cached error. Fixing the DB and restarting the gateway only clears the gateway's copy. All other processes that connected before the fix still hold the stale error. They must be restarted.
- **Check disk before assuming corruption**: `df -h /` is the first triage step. If disk < 85% used, the error is almost certainly a stale cache, not actual corruption. Run the "Cached Error State Recovery" path, not the full dump/restore.
- **`.corrupt` files are recovery debris, not the problem**: When Hermes detects corrupted Mnemosyne files, it renames them to `*.corrupt` and creates a fresh DB. Finding `.corrupt` files means recovery already happened — the fix is cleanup + restart, not another recovery cycle.
- **cp preserves inodes on same filesystem**: When you `cp` over an existing file on the same filesystem, the inode stays the same. This means old file descriptors in other processes still point to the correct file — but with stale locks. You MUST kill those processes.
- **state.db WAL can grow large**: The state.db has FTS indexes that create large WAL files. Checkpoint periodically.
- **OCR temp files**: Book/document OCR pipelines can leave GBs in `/tmp` — check after heavy OCR sessions.
