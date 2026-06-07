# Embedding Dimension Mismatch — Recovery Sequence

## Symptoms

`mcp_gbrain_put_page` or `gbrain put` fails with:

```
Embedding dim mismatch: model <model-name> returned <N> but schema expects <M>.
```

Example: `nvidia/llama-nemotron-embed-vl-1b-v2 returned 2048 but schema expects 1024.`

## Root Cause

The PGLite vector column was created with `<M>` dimensions (from config at init time). The currently configured model outputs `<N>` dimensions instead. Common causes:

- **Switched embedding models** (e.g. `nvidia/llama-nemotron-embed-vl-1b-v2` outputs 2048, `text-embedding-3-small` outputs 1536 natively)
- **Model changed behavior** (dimension passthrough bug — some OpenRouter models ignore `dimensions` parameter and return native dims)
- **Config.json was edited without reinitializing** (the file says one dimension, the DB schema says another)

## Step-by-Step Recovery

### 1. Diagnose the mismatch

```bash
# Check what the config says vs what the DB schema has
cat ~/.gbrain/config.json | python3 -c "
import sys, json
c = json.load(sys.stdin)
print(f'Config: model={c[\"embedding_model\"]}, dims={c[\"embedding_dimensions\"]}')
"

# Check actual DB stats
gbrain stats 2>&1 | grep -E "Pages|Chunks|Embedded"
```

The error message tells you what the model actually returned vs what the schema expects.

### 2. Choose a fix path

| Scenario | Fix | DB impact |
|----------|-----|-----------|
| **Switching embedding models** (most common) | **`gbrain reinit-pglite`** (recommended) | Wipes + recreates DB with correct dims |
| Model supports dimension parameter, same dims | Edit config.json only | Requires re-embed |
| Model DOESN'T support dimension parameter | Must change dims + re-embed | Requires reinit |

### 3. RECOMMENDED: `gbrain reinit-pglite` (one-command fix)

**PGLite cannot ALTER vector column types** (pgvector ships as embedded WASM). Editing config.json alone leaves the DB schema at the old dimension — `gbrain embed` will fail with the same mismatch. `reinit-pglite` recreates the schema correctly.

```bash
# Back up first
mv /root/.gbrain/brain.pglite /root/.gbrain/brain.pglite.bak.$(date +%Y%m%d%H%M)

# Reinit with new model + dimensions
export PATH="/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
source /root/.hermes/.env
export OPENROUTER_API_KEY  # or whichever key your model needs
cd ~/gbrain
gbrain reinit-pglite \
  --embedding-model openrouter:openai/text-embedding-3-small \
  --embedding-dimensions 1536 \
  --yes

# Re-import content
gbrain import /root/brain/

# Verify
gbrain stats  # Should show correct page/chunk/embedded counts
gbrain search "test query"  # Verify search works
```

**Gotcha:** `reinit-pglite` requires `--yes` in non-TTY environments (cron, scripts). Without it, the confirmation prompt hangs.

**Gotcha:** If a backup already exists at `.bak`, move it first: `mv /root/.gbrain/brain.pglite.bak /root/.gbrain/brain.pglite.bak.$(date +%Y%m%d%H%M)`

### 3b. Alternative: config-only fix (only if dimensions match)

If the model supports the `dimensions` parameter AND you're keeping the same dimension count:

```bash
python3 -c "
import json
with open('/root/.gbrain/config.json') as f:
    c = json.load(f)
c['embedding_dimensions'] = <ACTUAL_DIMENSIONS>
with open('/root/.gbrain/config.json', 'w') as f:
    json.dump(c, f, indent=4)
print(f'Set dimensions to {c[\"embedding_dimensions\"]}')
"
```

### 4. Kill all gbrain MCP servers

```bash
for pid in $(ps aux | grep "gbrain serve" | grep -v grep | awk '{print $2}'); do
  kill $pid 2>/dev/null
done
sleep 2
```

### 5. Clean stale PGLite locks

The MCP server holds an exclusive PGLite lock. If killed uncleanly, stale lock files prevent reconnection:

```bash
# Stale postmaster.pid (from orphaned PostgreSQL backend)
rm -f /root/.gbrain/brain.pglite/postmaster.pid

# Stale .gbrain-lock directory (container has a 'lock' file inside)
rm -rf /root/.gbrain/brain.pglite/.gbrain-lock

# Verify no stale PIDs are holding the DB open
# (if found, kill them too)
fuser /root/.gbrain/brain.pglite/ 2>/dev/null
```

### 6. Restart gbrain MCP server

```bash
source /root/.hermes/.env 2>/dev/null
export PATH="/root/.bun/bin:$PATH"
nohup /root/.bun/bin/gbrain serve > /dev/null 2>&1 &
sleep 3
```

Or let the Hermes gateway handle it (if configured via `mcp_servers.gbrain` in config.yaml):
```bash
# Restart the Hermes gateway to force MCP server restart
hermes gateway restart 2>/dev/null || true
# Or kill the gateway process; Hermes auto-restarts it
```

### 7. Test

```bash
# Via CLI (more reliable for diagnostics):
gbrain put test/embedding-fix < /tmp/test-page.md 2>&1
gbrain get test/embedding-fix 2>&1 | head -5
gbrain delete test/embedding-fix 2>&1

# Via MCP tools (after gateway reconnects):
mcp_gbrain_get_brain_identity  # Should succeed, not error
```

### 8. Re-embed existing content (if dimension changed)

If you changed dimensions, existing embeddings at the old dimension are orphaned. Re-embed:

```bash
# Re-embed all stale content
gbrain embed --all 2>&1

# Or submit via MCP job
mcp_gbrain_submit_job(name='embed', data='{"source": "default"}')
```

## Prevention

- **When changing embedding models**, always update BOTH `embedding_model` AND `embedding_dimensions` in config.json.
- **After config change**, kill the MCP server before the new config is read (gbrain serve caches config at startup).
- **Test with a single page** before bulk operations.
- **Preferred model set:** `openrouter:openai/text-embedding-3-small` with 1536 dimensions (reliable, widely supported, works through OpenRouter without dimension passthrough bugs).

## Related

- gbrain reference: `openrouter-embedding-models.md` — working model list for OpenRouter
- gbrain reference: `pglite-wasm-cli-workaround.md` — lock/stale-pid diagnostics
- gbrain pitfall: "PGLite cannot ALTER COLUMN vector(N)" — you can't in-place change dimension
