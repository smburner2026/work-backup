# HMS Config Corruption — Reproduction & Recovery

## Session: 2026-05-25

### Symptoms

User ran `hms push` (local → VPS direction). After the sync, the local config.yaml had its provider overwritten from `opencode-go` to `custom` with `base_url: https://inference-api.nousresearch.com/v1` (the "nous research" URL the user saw). API calls to opencode.ai started failing because the wrong API key was being sent.

### Root Cause

The VPS machine was configured with a `nous` custom provider (pointing to `inference-api.nousresearch.com`) while the local machine used `opencode-go` (pointing to `opencode.ai/zen/go/v1`). Since HMS syncs config.yaml bidirectionally (per the Sync Strategy table), the VPS config overwrote the local config during a push.

### What Got Overwritten

```
BEFORE (local, correct):                      AFTER (post-HMS-push, wrong):
model:                                         model:
  default: deepseek-v4-flash                     default: deepseek/deepseek-v4-flash:free
  provider: opencode-go                          provider: custom
  base_url: https://opencode.ai/zen/go/v1        base_url: https://inference-api.nousresearch.com/v1
  api_key: ${OPENCODE_GO_API_KEY}                (no api_key line — custom provider uses key_env)
```

### The Partial Fix Trap

User (or auto-recovery) noticed the provider and base_url were wrong and fixed them back to `opencode-go` / `opencode.ai/zen/go/v1`. But the `api_key` line was left pointing at `${NOUS_API_KEY}` — because the original local config already had `api_key: ${NOUS_API_KEY}` from a previous misconfiguration.

**Result:** The model block looked correct at a glance (right provider, right URL) but was sending the Nous Research API key to the OpenCode Go endpoint. Auth failures persisted silently.

### Detection

```bash
grep -A5 '^model:' config.yaml
# model:
#   default: deepseek-v4-flash
#   provider: opencode-go
#   base_url: https://opencode.ai/zen/go/v1
#   api_mode: chat_completions
#   api_key: ${NOUS_API_KEY}          ← WRONG! Should be ${OPENCODE_GO_API_KEY}
```

### Fix Applied

```bash
sed -i '6s/api_key: ${NOUS_API_KEY}/api_key: ${OPENCODE_GO_API_KEY}/' config.yaml
```

### .env Cosmetic Corruption

HMS sync also merged adjacent comment lines in .env:

```
# BEFORE:                              # AFTER (post-HMS, wrong):
# OPENCODE_GO_API_KEY=***               # OPENCODE_GO_API_KEY=*** # HF_TOKEN=*** OPENCODE_GO_BASE_URL=https://opencode.ai/zen/go/v1
# =============================================================================
# LLM PROVIDER (Hugging Face...)
# HF_TOKEN=***
# OPENCODE_GO_BASE_URL=...
```

Fixed by splitting at the natural boundary. Cosmetic only — commented lines have no runtime effect.

### Bitwarden BWS Verification

The BWS project `c3d06b5a-b678-4a8e-958e-b45400206274` has 10 secrets, all importing correctly:
- OPENROUTER_API_KEY, OPENCODE_GO_API_KEY, TAVILY_API_KEY
- TELEGRAM_BOT_TOKEN, DISCORD_BOT_TOKEN
- API_SERVER_KEY, GITHUB_TOKEN, HETZNER_API_TOKEN, NOUS_API_KEY
- oauth.xai-oauth (skipped by auto-detect — dots in key name)

Verified via: `bws secret list c3d06b5a-b678-4a8e-958e-b45400206274`

### Prevention

After fixing the local config, update the VPS config too so the next HMS push doesn't re-corrupt:

```bash
scp ~/.hermes/config.yaml root@<vps-host>:.hermes/config.yaml
```

### Key Lesson

The **triad** (provider, base_url, api_key) must all be verified after any config-corruption recovery. Fixing 2 of 3 leaves a subtle bug where the right endpoint receives the wrong credentials.
