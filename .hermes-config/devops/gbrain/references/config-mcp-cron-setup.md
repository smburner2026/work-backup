# gbrain Configuration: MCP Wiring + Dream Cycle Cron

Date: 2026-05-26
Version: gbrain v0.41.10.1
Setup context: VPS at 2GB RAM, PGLite backend, OpenRouter via `.env`

## Config Split Issue

**Problem:** `gbrain config get chat_model` showed `openrouter:inclusionai/ling-2.6-flash` (correct) but `~/.gbrain/config.json` still showed `openrouter:openai/gpt-5.2` (stale). The doctor check `subagent_capability` reads from the JSON file and flagged GPT-5.2 even though the CLI used Ling.

**Root cause:** `gbrain config set` writes to the PGLite DB. `~/.gbrain/config.json` is only written during `gbrain init` and never auto-synced when config changes via CLI.

**Fix:** Manually edit `~/.gbrain/config.json` to match:
```json
{
  "engine": "pglite",
  "database_path": "/root/.gbrain/brain.pglite",
  "embedding_model": "openrouter:nvidia/llama-nemotron-embed-vl-1b-v2",
  "embedding_dimensions": 1024,
  "chat_model": "openrouter:inclusionai/ling-2.6-flash"
}
```

## gbrain think Works with OpenRouter via --model (CORRECTION to previous assumption)

**Previous assumption (WRONG):** `gbrain think` requires `ANTHROPIC_API_KEY` regardless of config.  
**Actual behavior (discovered 2026-05-26):** `gbrain think` works with non-Anthropic providers when `--model` is explicitly passed.

**Confirmed working command:**
```bash
set -a; source /root/.hermes/.env; set +a
gbrain think "What toxicology topics are covered?" \
  --dir ~/brain/ \
  --model openrouter:inclusionai/ling-2.6-flash
```
Result: 5 pages gathered, 3 citations, real synthesis output. Model: `openrouter:inclusionai/ling-2.6-flash`.

**Why it works:** The `tryBuildGatewayClient` function in `src/core/think/index.ts` only checks `ANTHROPIC_API_KEY` when `providerId === 'anthropic'` (line 602). For `openrouter:` provider, the gateway routes through the OpenRouter recipe and uses `OPENROUTER_API_KEY` instead. The error "set anthropic_api_key" is a generic `buildGracefulMessage()` fallback that fires for ANY `AIConfigError` — it doesn't mean Anthropic is required, it means the AIConfigError is caught and surfaced with a misleading message.

**Why it appeared broken before:** The model resolution chain (6 tiers) falls through to tier default (`anthropic:claude-opus-4-7`) when no `--model` flag or `models.think` config is set. Earlier testing either omitted `--model` or ran without `OPENROUTER_API_KEY` in env.

**To make `gbrain think` work without Anthropic key long-term:**
```bash
gbrain config set models.default "openrouter:inclusionai/ling-2.6-flash"
gbrain config set models.think "openrouter:inclusionai/ling-2.6-flash"
```
(Note: `models.default` and `models.think` are distinct from `chat_model` in gbrain config.)

## MCP Server Wiring

### Problem: Filtered Environment

The Hermes native MCP client strips most env vars from subprocesses. Only safe baseline vars plus explicitly configured `env` entries pass through. Since gbrain needs `OPENROUTER_API_KEY` at runtime, a wrapper script is required.

### Solution: Wrapper Script

Created `~/.hermes/scripts/gbrain-mcp-wrapper.sh`:
```bash
#!/bin/bash
set -a
source /root/.hermes/.env 2>/dev/null
set +a
exec /root/.bun/bin/gbrain serve
```

Config added to `~/.hermes/config.yaml`:
```yaml
mcp_servers:
  gbrain:
    command: "/root/.hermes/scripts/gbrain-mcp-wrapper.sh"
    args: []
    env:
      PATH: "/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
      HOME: "/root"
    timeout: 180
```

### Verification
```bash
echo "test" | timeout 5 /root/.bun/bin/gbrain serve 2>&1
# Expected: "Starting GBrain MCP server (stdio)..." + "graceful exit (stdin-end)"
```

## Dream Cycle Cron

### no_agent Script Pattern

Created `~/.hermes/scripts/gbrain-dream-cycle.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.bun/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="$HOME"
cd /root/gbrain
echo "=== DREAM CYCLE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
gbrain dream --dir ~/brain/ --json 2>&1
echo "=== DREAM CYCLE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
```

Cron job created via Hermes cronjob tool:
- name: gbrain-dream-cycle
- schedule: 0 2 * * * (nightly at 2AM)
- no_agent: true (runs script directly, no LLM overhead)
- script: gbrain-dream-cycle.sh
- deliver: local

### Dry-run Verification
```bash
gbrain dream --dry-run --dir ~/brain/
# All 6 phases ran: lint, backlinks, sync, synthesize, extract, extract_facts,
# resolve_symbol_edges, patterns, recompute_emotional_weight, consolidate,
# propose_takes, grade_takes, calibration_profile, embed, orphans, schema-suggest, purge
# Expected: 106 orphan pages, 0 facts extracted (dry-run)
```

## DABT Brain Health Check (Baseline)

Initial `gbrain doctor --brain dabt` results:
- Health score: 55/100
- Brain score: 45/100 (embed 35/35 ✓, links 0/25, timeline 0/15, orphans 0/15 ✓, dead-links 10/10 ✓)
- 106 pages, 100% embedding coverage
- Schema v95 (latest)
- Content sanity: 132 events (0 hard, 8 soft, 124 warn) — expected for fresh import of large files
- No entity pages (brain is markdown-only — dream cycles will build the graph)
