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
cat ~/.gbrain/config.json | python3 -c "
import sys, json
c = json.load(sys.stdin)
print(f'Config: model={c[\"embedding_model\"]}, dims={c[\"embedding_dimensions\"]}')
"
```

The error message tells you what the model actually returned vs what the schema expects.

### 2. Choose a fix path

| Scenario | Fix | DB impact |
|----------|-----|-----------|
| Model supports dimension parameter (text-embedding-3-small, text-embedding-ada-002, voyage-*) | Set config to model's native dims. Example: text-embedding-3-small → 1536. | Requires re-embed of all existing content |
| Model DOESN'T support dimension parameter (Nemotron on OpenRouter, many openai-compatible models) | Can't passthrough dims. Must either: (a) use native dims, or (b) patch source code (see gbrain pitfalls). | Requires dimension change + re-embed |
| Want to switch models entirely | Set both model name and dims to the new model's supported/output dimensions. | Requires dimension change + re-embed |

### 3. Update config.json dimension

```bash
python3 -c "
import json
with open('/root/.gbrain/config.json') as f:
    c = json.load(f)
# Set to what the model actually outputs
c['embedding_dimensions'] = <ACTUAL_DIMENSIONS>
with open('/root/.gbrain/config.json', 'w') as f:
    json.dump(c, f, indent=4)
print(f'Set dimensions to {c[\"embedding_dimensions\"]}')
"
```

If also switching models:
```bash
c['embedding_model'] = 'openrouter:openai/text-embedding-3-small'
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
