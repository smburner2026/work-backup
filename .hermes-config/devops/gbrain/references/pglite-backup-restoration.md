# PGLite Backup Restoration After Corruption

Recovery sequence after ungraceful kill corrupted the PGLite WASM database.
Sourced from a real recovery on 2026-05-31.

## Symptoms

- `gbrain serve` fails: "PGLite failed to initialize its WASM runtime"
- `gbrain dream` fails: same WASM init error
- `gbrain doctor` succeeds but shows 0 pages / 0% embed coverage (it use a different path)
- Fresh PGLite init works, but opening the existing `brain.pglite/` directory crashes

## Distinguishing Corruption from Lock

| Symptom | Likely cause |
|---------|-------------|
| "Timed out waiting for PGLite lock" | MCP server running; kill it first |
| "PGLite failed to initialize its WASM runtime" after kill | Stale `postmaster.pid` — remove it |
| WASM abort on existing dir, works on fresh dir | **Data corruption** — need backup restoration |
| `gbrain init --pglite` succeeds, but opening old DB fails | Corrupted internal Postgres state |

## Recovery Sequence

```bash
# 1. Kill ALL gbrain processes
pkill -f "gbrain" 2>/dev/null
sleep 2

# 2. Try the easy fix first — stale pid
rm -f /root/.gbrain/brain.pglite/postmaster.pid

# 3. Test if the DB is still good
bun /root/.bun/bin/gbrain serve
# If it starts → done. If WASM abort → corrupted.

# 4. Preserve the corrupted DB for analysis
cp -a /root/.gbrain/brain.pglite /root/.gbrain/brain.pglite.corrupted-$(date +%Y%m%d_%H%M%S)

# 5. Restore from backup
# The backup is typically smaller (~42MB vs 425MB working DB)
cp -a /root/.gbrain/brain.pglite.bak /root/.gbrain/brain.pglite
rm -f /root/.gbrain/brain.pglite/postmaster.pid

# 6. Apply schema migrations (backup may be from older version)
gbrain init --pglite --dir /root/.gbrain/brain.pglite --yes
# This applies pending migrations + sets up skillpacks

# 7. Import reference content back into the restored brain
# (backup has no pages — they were in the corrupted DB)
mkdir -p /root/.gbrain/dabt-ref/{casarett-doull,hayes,regulations,abt-handbook}
cp /root/work/dabt/dabt-tutor/reference/extracted/casarett-doull-9e/*.txt /root/.gbrain/dabt-ref/casarett-doull/
cp /root/work/dabt/dabt-tutor/reference/extracted/hayes-7e/*.txt /root/.gbrain/dabt-ref/hayes/
cp /root/work/dabt/dabt-tutor/reference/extracted/regulations/*.txt /root/.gbrain/dabt-ref/regulations/
cp /root/work/dabt/dabt-tutor/reference/extracted/abt-handbook/*.txt /root/.gbrain/dabt-ref/abt-handbook/

# Rename .txt to .md (gbrain only imports .md)
cd /root/.gbrain/dabt-ref
for f in $(find . -name '*.txt'); do mv "$f" "${f%.txt}.md"; done

# 8. Import (with --no-embed for speed, then dream cycle handles embed)
gbrain import /root/.gbrain/dabt-ref --no-embed
# Expect: 150 pages, 8000+ chunks

# 9. Run dream cycle to embed and link
gbrain dream --dir /root/.gbrain/brain.pglite
# Embed phase will process the 8000+ chunks (0 if they were pre-embedded)

# 10. Restart MCP server
nohup bash /root/.hermes/scripts/gbrain-mcp-wrapper.sh >/dev/null 2>&1 &
```

## Result

After this sequence:
- **150 pages** imported (Casarett & Doull + Hayes + regulations + ABT handbook)
- **8,013 chunks** created
- Dream cycle runs clean (all phases pass)
- `gbrain think` works with OpenRouter model
- MCP server serves tools

## Preventing Recurrence

- Always `rm -f /root/.gbrain/brain.pglite/postmaster.pid` after killing the MCP server
- Keep `brain.pglite.bak` up to date: `cp -a /root/.gbrain/brain.pglite /root/.gbrain/brain.pglite.bak` after major imports
- The dream cycle script should use `--dir` flag: `gbrain dream --dir /root/.gbrain/brain.pglite` (without it, it checks `sync.repo_path` which may be unset on restored backups)
