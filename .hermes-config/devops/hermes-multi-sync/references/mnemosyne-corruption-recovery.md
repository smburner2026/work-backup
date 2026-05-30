# Mnemosyne DB Corruption Recovery

When a HMS sync (or any raw rsync) hits a live Mnemosyne DB while the gateway has it open, the SQLite WAL file can desync from the main database file. This produces B-tree corruption that manifests as "database disk image is malformed" errors on `mnemosyne_remember` / `mnemosyne_recall` / `mnemosyne_stats` tools, even though the file may appear valid by size.

## Root Cause

- Mnemosyne runs in **WAL mode** — writes go to a `.db-wal` file first, periodically checkpointed to the main `.db` file
- The gateway holds **multiple open connections** (4+ FDs) to the DB
- When rsync (via HMS) reads the `.db` file while the WAL holds uncheckpointed writes, the synced copy may be in an inconsistent state
- Additionally, the sync can create a **split-brain** where a 0-byte `mnemosyne/mnemosyne.db` file appears at the root level, shadowing the real DB at `mnemosyne/data/mnemosyne.db`

## Symptoms

| Symptom | Likely cause |
|---------|-------------|
| `mnemosyne_remember` fails with "database disk image is malformed" | B-tree corruption OR 0-byte split-brain file |
| `PRAGMA integrity_check` returns "ok" but tool still fails | Provider initialized with corrupted file at session start; stale in-memory state persists until restart |
| `SELECT COUNT(*) FROM working_memory` returns 0 but file is large | Split file — querying wrong DB path |
| Integrity check reports "rowid out of order", "missing from index", "malformed inverted index" | B-tree corruption from desynced WAL |

## Recovery Procedure

### 1. Detect the split-brain

```bash
# Check both paths
ls -la ~/.hermes/mnemosyne/mnemosyne.db
ls -la ~/.hermes/mnemosyne/data/mnemosyne.db
```

If `mnemosyne/mnemosyne.db` is 0 bytes but `data/mnemosyne.db` is 10MB+ with data, you have a split-brain. The tool looks at the root path; the real data is in `data/`.

### 2. Rebuild from dump

```bash
# Identify the real (non-empty) DB
REAL_DB=~/.hermes/mnemosyne/data/mnemosyne.db

# Back up
cp "$REAL_DB" /tmp/mnemosyne-corrupted-backup.db

# Check WAL files
ls -la "$(dirname "$REAL_DB")"/*.db-wal "$(dirname "$REAL_DB")"/*.db-shm 2>/dev/null

# Try WAL checkpoint first
cp "$REAL_DB" /tmp/mnemosyne-checkpoint.db
sqlite3 /tmp/mnemosyne-checkpoint.db "PRAGMA wal_checkpoint(FULL);"

# Check integrity
sqlite3 /tmp/mnemosyne-checkpoint.db "PRAGMA integrity_check;"

# If corrupt, dump and rebuild
sqlite3 /tmp/mnemosyne-checkpoint.db ".output /tmp/mnemosyne-dump.sql" ".dump" 2>/dev/null
wc -l /tmp/mnemosyne-dump.sql  # Should be 20K+ lines if data exists
```

### 3. Fix the dump for import

The `.dump` wraps everything in `BEGIN TRANSACTION` / `COMMIT`. If ANY row fails (e.g., NOT NULL constraint on a corrupted `graph_edges` row), the entire transaction rolls back and zero data is imported.

Fix:

```bash
cd /tmp
# Remove BEGIN TRANSACTION (so each statement auto-commits)
sed -i 's/^BEGIN TRANSACTION;$/-- BEGIN TRANSACTION;/' mnemosyne-dump.sql
# Replace ROLLBACK with COMMIT (in case of prior failed attempts)
sed -i 's/^ROLLBACK; -- due to errors$/COMMIT;/' mnemosyne-dump.sql
# Add ignore_check_constraints for corrupted NOT NULL rows
sed -i '1i PRAGMA ignore_check_constraints=ON;' mnemosyne-dump.sql

# Rebuild into a clean database
rm -f mnemosyne-rebuilt.db
sqlite3 mnemosyne-rebuilt.db ".read mnemosyne-dump.sql" 2>&1 | tail -5
```

If you get "table sqlite_master may not be modified" errors, those are harmless — they come from `PRAGMA writable_schema=ON` blocks in the dump.

### 4. Verify the rebuilt DB

```bash
sqlite3 mnemosyne-rebuilt.db "PRAGMA integrity_check;"
# Must return "ok"

# Check record counts
for table in working_memory episodic_memory facts consolidated_facts triples scratchpad graph_edges; do
  count=$(sqlite3 mnemosyne-rebuilt.db "SELECT COUNT(*) FROM \"$table\";" 2>/dev/null)
  echo "$table: $count"
done

# Typical healthy counts: working_memory 2000+, episodic_memory 100+, facts 500+
```

### 5. Deploy

```bash
cd ~/.hermes/mnemosyne/
cp data/mnemosyne.db data/mnemosyne.db.corrupted-backup

# Copy the rebuilt DB
cp /tmp/mnemosyne-rebuilt.db data/mnemosyne.db

# Fix root-level split-brain if it's a 0-byte file
rm -f mnemosyne.db
ln -sf data/mnemosyne.db mnemosyne.db

# Clear stale WAL/SHM files
rm -f data/mnemosyne.db-wal data/mnemosyne.db-shm
```

### 6. Restart the gateway

The gateway has stale FDs pointing to the old inode. Even though the file on disk is replaced, the gateway continues reading the old (corrupted) data through its cached file handles.

```bash
# Kill the gateway to release old FDs
kill -TERM "$(cat ~/.hermes/gateway.pid)"
sleep 2

# Start fresh
hermes gateway run --replace --daemon 2>&1 &

# Verify
sleep 3
cat ~/.hermes/gateway.pid
```

### 7. Session restart requirement

The current Hermes session has a cached "database disk image is malformed" error from when the provider initialized with the corrupted DB. Even after the DB is fixed, the in-memory error persists until the session ends.

**The Mnemosyne tools will not work in the current session.** They will work in the next session when the provider initializes with the clean DB.

## Prevention

- **Stop the gateway before any manual sync** — `kill -TERM $(cat ~/.hermes/gateway.pid)` on the destination machine before syncing Mnemosyne data
- **HMS auto (cron) does NOT sync Mnemosyne** — only `hms push`/`hms pull` do. The cron-based auto-sync is safe.
- **After any raw rsync or non-HMS sync**, always verify Mnemosyne integrity before restarting the gateway
- **The `--update` flag in rsync only checks timestamps, not WAL state** — even a timestamp-safe sync can corrupt if the DB was being written during the rsync
