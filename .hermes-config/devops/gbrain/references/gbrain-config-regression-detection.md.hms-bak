# GBrain Config Regression — Detection & Recovery

A recurring class of regression where `gbrain think` or `gbrain models` shows wrong model routes despite `~/.gbrain/config.json` appearing correct.

## Root Cause

gbrain has **two config stores** that diverge:

| Store | Path | Written by | Read by |
|-------|------|-----------|---------|
| PGLite DB | `~/.gbrain/brain.pglite` | `gbrain config set <key>` | `gbrain config get <key>`, `resolveModel()`, `getChatModel()`, `gatewayChat()` |
| JSON file | `~/.gbrain/config.json` | `gbrain init` | `gbrain config show` |

`resolveModel()` — the 8-tier model resolution chain that all LLM paths use — reads **only from the PGLite DB**. The JSON file is a fallback snapshot written at init time; setting keys there does nothing at runtime.

## Detection

If a user reports "gbrain keeps falling back to Anthropic" or "I see the right model in config but think doesn't use it":

```bash
# Compare the two sources:
gbrain config get models.default      # Reads DB (runtime truth)
gbrain config get models.think        # Reads DB
gbrain config get models.chat         # Reads DB
gbrain config get models.tier.utility # Reads DB
gbrain config get provider_base_urls  # Reads DB
gbrain config show                    # Reads JSON (may differ)
```

If `config get` returns "Config key not found" for any of these, gbrain's model resolver falls through to the Anthropic tier default for that path — regardless of what the JSON file says.

## Complete Fix

Set ALL model keys in the PGLite DB. Each missing key silently regresses one path:

```bash
gbrain config set chat_model deepseek:deepseek-v4-flash --force
gbrain config set models.default deepseek:deepseek-v4-flash --force
gbrain config set models.think deepseek:deepseek-v4-flash --force
gbrain config set models.chat deepseek:deepseek-v4-flash --force
gbrain config set models.tier.utility deepseek:deepseek-v4-flash --force
gbrain config set models.tier.reasoning deepseek:deepseek-v4-flash --force
gbrain config set models.tier.deep deepseek:deepseek-v4-flash --force
gbrain config set models.tier.subagent deepseek:deepseek-v4-flash --force

# CRITICAL: provider_base_urls must use JSON notation (dot-notation silently fails):
gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}' --force
```

Then sync the JSON file to keep them aligned:

```bash
python3 -c "
import json
c = json.load(open('/root/.gbrain/config.json'))
c['chat_model'] = 'deepseek:deepseek-v4-flash'
c['models.default'] = 'deepseek:deepseek-v4-flash'
c['models.think'] = 'deepseek:deepseek-v4-flash'
c['models.chat'] = 'deepseek:deepseek-v4-flash'
c['models.tier'] = {k: 'deepseek:deepseek-v4-flash' for k in ['utility','reasoning','deep','subagent']}
c['provider_base_urls'] = {'deepseek': 'https://opencode.ai/zen/go/v1'}
json.dump(c, open('/root/.gbrain/config.json', 'w'), indent=2)
"
```

## Verification

```bash
# 1. Check model routing (all tiers must show correct model + source "config:" not "tier default:"):
gbrain models

# 2. Probe chat endpoint directly:
curl -s https://opencode.ai/zen/go/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'

# 3. Full synthesis test:
gbrain think "Ames test" --limit 3
# Confirm "Model: deepseek:deepseek-v4-flash" in the footer

# 4. MCP integration:
# From inside a Hermes session, call mcp_gbrain_query and mcp_gbrain_think
```

## Prevention

The dream cycle script (`~/.hermes/scripts/gbrain-dream-cycle.sh`) self-heals all 9 keys before every run. If you change `chat_model` or any model config directly, the next dream cycle overwrites it back. To make a permanent change, update the script first, then the DB.

Common regression triggers:
- `gbrain init --pglite` (recreates DB, writing only `engine` and `database_path` to config)
- Manual `gbrain config set chat_model ...` (only writes to DB, not to JSON, and only sets one key)
- `git pull` + `bun install` in gbrain repo (doesn't touch DB or JSON, but may add config keys that need setting)
