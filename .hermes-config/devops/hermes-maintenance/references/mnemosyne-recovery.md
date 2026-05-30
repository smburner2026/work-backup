# Mnemosyne DB Recovery

Recovery procedures for the Mnemosyne memory provider (v3.0.0+) database corruption — orphaned FTS5/vec0 shadow tables, WAL journal corruption, and the "database disk image is malformed" error.

## Symptom Detection

### FTS5 shadow table conflict

On `import mnemosyne` or Hermes startup with `memory.provider: mnemosyne`:

```
sqlite3.OperationalError: fts5: error creating shadow table fts_episodes_data:
  table 'fts_episodes_data' already exists
```

### Vec0/vec extension not loaded

```
sqlite3.OperationalError: no such module: vec0
```

### Database disk image is malformed

On `Mnemosyne.recall()` or any write operation:

```
sqlite3.DatabaseError: database disk image is malformed
```

## Diagnosis

### 1. Check virtual tables

```bash
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db \
  "SELECT name, type FROM sqlite_master WHERE type='virtual'"
```

Expected: at least 5 virtual tables (`fts_episodes`, `fts_working`, `fts_facts`, `vec_episodes`, `vec_facts`). If this query returns **zero rows**, the virtual table entries are missing.

### 2. Check for orphaned shadow tables

Orphaned FTS5 shadow tables exist when:
- A regular table named `fts_episodes_data`, `fts_episodes_idx`, `fts_episodes_docsize`, `fts_episodes_config` exists
- But the virtual table `fts_episodes` does NOT exist in `sqlite_master`
- Same pattern for `fts_working_*`, `fts_facts_*`, `vec_episodes_*`, `vec_facts_*`

### 3. Check vec0 module loadability

```bash
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db \
  "SELECT COUNT(*) FROM vec_episodes;"
```

If this returns "Error: no such module: vec0", the vec0 extension is not loaded in the CLI context. This is normal for plain `sqlite3` — the critical test is inside the Mnemosyne process context which loads the extension via `sqlite_vec.load(conn)`.

### 4. Check DB integrity

```python
import sqlite3
conn = sqlite3.connect('~/.hermes/mnemosyne/data/mnemosyne.db')
conn.execute('PRAGMA integrity_check')
# Returns [('ok',)] if clean
```

Note: `integrity_check` may return `ok` even when recall operations fail with "malformed database" — the WAL journal can be the corrupt component while the main DB file is intact.

## Repair Procedures

### Procedure A: Orphaned shadow tables (the most common failure)

SQLite FTS5's `CREATE VIRTUAL TABLE IF NOT EXISTS` checks whether the virtual table itself exists in `sqlite_master`, but does NOT check whether its internal shadow tables (`fts_*_data`, `fts_*_idx`, etc.) already exist as regular tables. When a crash, schema migration failure, or manual cleanup leaves orphaned shadow tables behind, FTS5 raises an error on init.

**Fix: drop all orphaned FTS5 and vec0 shadow tables, then let init recreate them.**

```python
import sqlite3

db_path = os.path.expanduser('~/.hermes/mnemosyne/data/mnemosyne.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Identify existing virtual tables
cur.execute("SELECT name FROM sqlite_master WHERE type='virtual'")
virtuals = set(row[0] for row in cur.fetchall())
print(f'Virtual tables present: {virtuals}')

# Drop orphaned FTS5 shadow tables
fts_suffixes = ['_data', '_idx', '_docsize', '_config', '_content']
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name GLOB 'fts_*'")
dropped = []
for (tbl,) in cur.fetchall():
    base = tbl
    for suffix in fts_suffixes:
        if tbl.endswith(suffix):
            base = tbl[:-len(suffix)]
            break
    if base not in virtuals:
        cur.execute(f'DROP TABLE IF EXISTS "{tbl}"')
        dropped.append(tbl)

# Drop orphaned vec0 shadow tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name GLOB 'vec_*'")
for (tbl,) in cur.fetchall():
    if tbl.startswith('vec_episodes'):
        base = 'vec_episodes'
    elif tbl.startswith('vec_facts'):
        base = 'vec_facts'
    else:
        base = tbl.rsplit('_', 1)[0]
    if base not in virtuals:
        cur.execute(f'DROP TABLE IF EXISTS "{tbl}"')
        dropped.append(tbl)

conn.commit()
print(f'Dropped {len(dropped)} orphaned shadow tables')
conn.close()
```

After running this, test that mnemosyne imports cleanly:

```bash
/usr/local/lib/hermes-agent/venv/bin/python -c "
from mnemosyne import Mnemosyne
m = Mnemosyne()
m.remember('smoke test', scope='global')
print('mnemosyne init OK')
"
```

### Procedure B: "Database disk image is malformed" on write

After fixing shadow tables, recall may still fail with "database disk image is malformed" due to WAL journal corruption or internal page-level issues.

**Fix: checkpoint WAL + VACUUM**

```python
import sqlite3, os

db_path = os.path.expanduser('~/.hermes/mnemosyne/data/mnemosyne.db')

# Step 1: Force WAL checkpoint to flush WAL into main DB
conn = sqlite3.connect(db_path)
conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
conn.close()

# Step 2: VACUUM rebuilds the entire DB file, discarding any corruption
conn = sqlite3.connect(db_path)
conn.execute('VACUUM')
conn.close()

print(f'DB size after VACUUM: {os.path.getsize(db_path)} bytes')
```

After VACUUM, the WAL and SHM files are recreated clean.

**Important:** VACUUM requires free disk space approximately equal to the DB file size. If the DB is large (>1GB), ensure enough disk space.

### Procedure C: Full reset (nuclear option)

If procedures A and B don't resolve the issue, or the vector embeddings are empty (vec tables dropped and vectors lost), the cleanest recovery is to rebuild the DB from scratch:

```bash
# Back up the old DB
cp ~/.hermes/mnemosyne/data/mnemosyne.db{,.bak-$(date +%Y%m%d)}

# Remove DB files (mnemosyne recreates on next init)
rm -f ~/.hermes/mnemosyne/data/mnemosyne.db*
```

Note: This loses ALL stored memories. Use only as last resort — the content tables (episodic_memory, working_memory, facts) are recreated empty. After this, Hermes will re-accumulate memories from scratch.

## Verification

After any repair, verify end-to-end:

```python
from mnemosyne import Mnemosyne
m = Mnemosyne()

# Write
m.remember('Verification: mnemosyne is healthy', scope='global')

# Read
results = m.recall('verification mnemosyne healthy', top_k=5)
print(f'Recall returned {len(results)} results')

# Check storage
import sqlite3
conn = sqlite3.connect('~/.hermes/mnemosyne/data/mnemosyne.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM episodic_memory')
print(f'Episodic memory count: {cur.fetchone()[0]}')
cur.execute('SELECT COUNT(*) FROM working_memory')
print(f'Working memory count: {cur.fetchone()[0]}')
```

## Root Cause

The most common trigger for orphaned shadow tables is an incomplete schema migration in mnemosyne v3.0.0. The `init_beam()` function creates virtual tables with `IF NOT EXISTS`, but if a crash or interrupted migration leaves shadow tables without their parent virtual table entry, every subsequent startup fails. The virtual table entries in `sqlite_master` are recoverable — they just need the shadow tables cleared first.

## References

- Mnemosyne installation and setup: `hermes-agent` skill → `references/mnemosyne-memory-provider.md`
- mnemosyne-memory pip package: https://github.com/AxDSan/mnemosyne
