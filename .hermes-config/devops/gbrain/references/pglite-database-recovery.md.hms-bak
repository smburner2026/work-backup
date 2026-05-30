# PGLite Database Recovery

## Scenario

PGLite itself works fine — `PGlite.create()` with no dataDir or a new path succeeds. But opening an **existing** database (`dataDir: /root/.gbrain/brain.pglite`) triggers an unrecoverable WASM abort:

```
PGLite failed to initialize its WASM runtime.
  Most common cause: the macOS 26.3 WASM bug
  Original error: Aborted(). Build with -sASSERTIONS for more info.
```

This is NOT a WASM incompatibility issue (despite the misleading error message that blames "macOS 26.3 WASM bug"). It means the specific database data directory has corrupted internal Postgres state — PGLite's WASM Postgres engine cannot mount it.

## Diagnostic Flow

### Step 1: Confirm fresh DB works vs existing DB crashes

```js
// Fresh instance — WORKS
const db = await PGlite.create({});
// succeeds

// Existing corrupted DB — CRASHES
const db = await PGlite.create({
  dataDir: '/root/.gbrain/brain.pglite',
  extensions: {}
});
// RuntimeError: Aborted(). Build with -sASSERTIONS for more info.
```

### Step 2: Check migration history

```bash
cat /root/.gbrain/migrations/completed.jsonl
```

Look for:
- Failed migration records (status: "partial", phase "schema" failed)
- The last successful migration version
- Retry records that eventually succeeded

If the logs show a version where migration failed repeatedly then eventually succeeded, the database state may be inconsistent (schema applied partially, data in wrong format).

### Step 3: Check postmaster.pid

```bash
cat /root/.gbrain/brain.pglite/postmaster.pid
```

The first line is a signal number (-42 = PostgreSQL SIGUSR2 used for recovery). If the PID (last two values) refers to a dead process, the database may have had an unclean shutdown. Try removing this file and retry — this resolves some cases but NOT full corruption.

### Step 4: Test the backup

```bash
# Check if brain.pglite.bak exists (May 27 snapshot in this install)
ls -la /root/.gbrain/brain.pglite.bak/

# Try opening it — if it's empty/pre-migration it won't have gbrain schema
const db = await PGlite.create({
  dataDir: '/root/.gbrain/brain.pglite.bak',
  extensions: {}
});
const result = await db.query('SELECT count(*) as n FROM gbrain_pages');
// If "relation gbrain_pages does not exist" → backup is empty/uninitialized
```

### Step 5: Check PG internal files

```bash
cat /root/.gbrain/brain.pglite/PG_VERSION  # Should be "17"
ls /root/.gbrain/brain.pglite/pg_wal/       # Check for WAL segments
ls /root/.gbrain/brain.pglite/base/          # Database OID directories
```

Unapplied WAL segments suggest an unclean shutdown where Postgres was recovering and never completed.

## Common Patterns Seen

| Pattern | What it means | Likelihood |
|---------|--------------|------------|
| Fresh DB works, existing crashes | Data directory corruption, not WASM incompatibility | High |
| postmaster.pid exists, PID is dead | Unclean shutdown, stale lock | Try removing pid first |
| Migration log shows partial+retry+complete | Schema was applied after retries but internal state may be inconsistent | Medium |
| brain.pglite.bak exists but empty | Backup was taken pre-migration, no useful data | Confirmed |
| WAL segments present | Unapplied WAL logs — recovery never completed | Likely cause |

## Recovery Options

### Option A: Re-init + Re-import (Recommended)

```
1. Backup the corrupted database (already done: brain.pglite.bak):
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   mv /root/.gbrain/brain.pglite /root/.gbrain/brain.pglite.corrupt_$TIMESTAMP

2. Re-init from scratch (same embedding provider as original):
   OPENROUTER_API_KEY=*** gbrain init --pglite \
     --embedding-model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 \
     --embedding-dimensions 1024

3. Re-import source documents:
   gbrain import ~/brain/extracted/
   # Large collections may timeout — re-run; gbrain skips already-imported files:
   gbrain import ~/brain/extracted/ 2>&1 | tail -5

4. Verify import:
   gbrain stats
   # Expected: Pages: N  Chunks: N  Embedded: N

5. Rebuild custom pages from session_search + filesystem backups:
   - Check ~/.hermes/cron/output/ for saved miss journal entries
   - Check project reference/data/ directories for assessment files
   - Recreate dabt/flashcards/*, dabt/learner-profile, miss journal entries
   - Use: echo '...' | gbrain put 'dabt/<slug>'
   - Reference prior session_search output to reconstruct page content
```

**Worked example (DABT tutor, May 28, 2026):**
- Source docs at `/root/brain/extracted/` (105 .md files, Casarett & Doull 9e, Hayes 7e, regulations, ABT handbook)
- Ran `gbrain import` twice (first pass hit 300s timeout at 86/105; second pass completed all 105 via skip logic)
- Rebuilt 9 custom pages via `gbrain put` from session history: master-index, risk-assessment deck, as-cd-cr-deepdive deck, metals-hg-pb deck, learner profile, 4 miss journal entries
- Full recovery in ~12 minutes

**Data lost:** All gbrain pages (flashcard collection docs, miss journal entries, learner profile) not backed up to filesystem. Source documents (C&D, Hayes, regs) are safe on disk and will re-import.

**Critical:** `gbrain export` also fails on a corrupted DB (calls `gbrain get` which needs PGLite mount). You cannot export pages once corruption is detected — they survive only in session transcripts and filesystem backups. Periodically snapshot key pages via `gbrain export --dir ~/brain-backup/` while the DB is healthy.

### Option B: DB Repair (Unlikely to work)

PGLite has no built-in repair tool. WAL replay is automatic on mount — if that's the issue, the DB would self-recover. Since it doesn't:
- The corruption is structural (not a WAL issue)
- `pg_resetwal` equivalent doesn't exist for PGLite
- Removing individual files (pg_xact, pg_wal) makes it worse

### Option C: Migrate Engine

Switch from PGLite to a real Postgres instance or Supabase:
```bash
gbrain migrate --to supabase --connection-url postgres://...
```
Only possible if you have a running Postgres instance. Still requires the source DB to be readable.

## Prevention

1. **Set up proper backup schedule:** Copy the brain.pglite directory to a timestamped backup after each significant import or review session
2. **Develop without breaking brain:** Test PGLite version upgrades on a copy first
3. **Export key pages to markdown periodically:** `gbrain export --dir ~/brain-backup/` snapshots all pages as markdown files
4. **After failed migration, don't retry blindly:** If PGLite WASM crashes during migration, the database may be left in an inconsistent state — re-init instead
