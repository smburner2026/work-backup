# G-Brain Embedding Health Monitoring

## Why

G-Brain's configured embedding model (typically `openrouter:nvidia/llama-nemotron-embed-vl-1b-v2`) is an **external API dependency**. OpenRouter can have routing issues, model deprecation, auth failures, or rate-limiting that silently break embedding — causing searches to return empty results while gbrain itself reports healthy.

Additionally, the **dream cycle** and **PGLite CLI** can silently fail, leaving the brain unmaintained. The audit should cover all three layers.

## Nightly Audit Integration

The recommended approach is a silent-on-ok watchdog in the nightly self-audit cron (`~/.hermes/scripts/self-audit.sh`, runs at `0 8 * * *`):

### 1. Embedding API Health (curl — preferred over gbrain CLI)

Tests the actual OpenRouter endpoint without needing gbrain's PGLite:

```bash
source /root/.hermes/.env 2>/dev/null || true
OR_KEY="${OPENROUTER_API_KEY:-}"
if [ -n "$OR_KEY" ]; then
    EMBED_RESP=$(curl -sf -w "\\n%{http_code}" \
        https://openrouter.ai/api/v1/embeddings \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OR_KEY" \
        -d '{"model":"nvidia/llama-nemotron-embed-vl-1b-v2","input":"gbrain nightly embedding health check"}' \
        2>&1 || true)
    HTTP_CODE=$(echo "$EMBED_RESP" | tail -1)
    if [ "$HTTP_CODE" != "200" ]; then
        # Fire alert: embed model HTTP $HTTP_CODE
    elif ! echo "$EMBED_RESP" | head -n -1 | \
        python3 -c "import sys,json; d=json.load(sys.stdin); assert 'data' in d and len(d['data'])>0" 2>/dev/null; then
        # Fire alert: malformed response
    fi
fi
unset OR_KEY
```

### 2. Dream Cycle Completion Check

Verifies the dream cycle ran recently via its marker file:

```bash
MARKER_FILE="$HOME/.gbrain/.dream-last-run"
if [ -f "$MARKER_FILE" ]; then
    read -r LAST_DREAM < "$MARKER_FILE" 2>/dev/null || true
    NOW=$(date -u +%s)
    HOURS_SINCE=$(( (NOW - LAST_DREAM) / 3600 ))
    if [ "$HOURS_SINCE" -gt 36 ]; then
        # Fire alert: dream cycle stale ($HOURS_SINCE hours)
    fi
else
    # Fire alert: dream cycle never completed
fi
```

### 3. PGLite CLI Health

Quick probe to detect a hung gbrain CLI (PGLite WASM lock contention):

```bash
if command -v gbrain &>/dev/null; then
    CLI_OK=$(timeout 10 gbrain providers list 2>/dev/null | head -3 || true)
    if [ -z "$CLI_OK" ]; then
        # Fire alert: gbrain CLI unresponsive (PGLite WASM / hung process)
    fi
fi
```

## Design decisions

| Decision | Rationale |
|----------|-----------|
| **Direct curl, not `gbrain providers test`** | Avoids gbrain's PGLite WASM CLI bug (gh#223) — curl tests the real dependency without needing a healthy gbrain process. Also works if gbrain binary isn't in PATH. |
| **Dream cycle marker file, not cron status** | The cron may report "success" even if the dream was skipped (cycle lock). The marker file is written only after the dream command actually runs. |
| **PGLite CLI probe is separate** | A short `timeout 10 gbrain providers list` catches a hung PGLite (WASM lock contention) without the expense of a full `gbrain doctor`. |
| **Sources `.env` directly** | Cron jobs run in sanitized environment; API keys live in `.env` not in cron's env. |
| **Guarded with `[ -n "${OPENROUTER_API_KEY:-}" ]`** | No false-positive alerts on machines without the key configured. |
| **Two failure modes** | HTTP status (downtime/auth/routing) vs JSON body (API change/malformed response) — each tells a different story. |
| **No output on success** | Watchdog pattern — the user only hears about the check when it fails. |

## Failure Modes

| Symptom | Probable cause | User action |
|---------|---------------|-------------|
| HTTP 401/403 | Key expired, revoked, or not sourced in `.env` | `source ~/.hermes/.env` and verify `echo $OPENR...EY` |
| HTTP 429 | Rate limited | Wait, check OpenRouter dashboard |
| HTTP 5xx | OpenRouter outage or model routing failure | Check https://status.openrouter.ai |
| HTTP 200 but no `data[0].embedding` | OpenRouter API response format changed | Update the JSON validation path |
| HTTP 200, valid JSON, but gbrain embedding still fails | Dimension passthrough bug (see `references/openrouter-embedding-quirks.md`) | Apply the `dimsProviderOptions()` patch |
| Dream cycle marker >36h stale | Dream cycle script failed or timed out | Check cron output: `cat ~/.hermes/cron/output/<gbrain-dream-id>/*`; manually run `gbrain dream --dir ~/brain/` |
| Dream cycle marker missing | Dream never ran (new install or script broken) | Same as above; verify script at `~/.hermes/scripts/gbrain-dream-cycle.sh` |
| gbrain CLI timeout/unresponsive | PGLite lock contention with MCP server or stale postmaster.pid | Kill gbrain MCP server: `pkill -f "gbrain serve"`; remove stale pid: `rm -f /root/.gbrain/brain.pglite/postmaster.pid` |

## Testing

```bash
# Quick manual check
source ~/.hermes/.env && \
curl -sf -w "\n%{http_code}" \
  https://openrouter.ai/api/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENR...EY" \
  -d '{"model":"nvidia/llama-nemotron-embed-vl-1b-v2","input":"ping"}' | tail -1
# Expected: 200

# Full simulation — inject a failure to verify the alert path
curl -sf -w "\n%{http_code}" \
  https://openrouter.ai/api/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer bad-key" \
  -d '{"model":"nvidia/llama-nemotron-embed-vl-1b-v2","input":"ping"}' | tail -1
# Expected: 401
```
