---
name: hermes-provider-config
description: "Configure Hermes Agent inference providers and models — active config model, provider selection, environment variables, restart requirements, OpenCode Go/DeepSeek routing, and provider-specific quirks."
version: 0.1
author: Hermes Agent
---

# Hermes Provider Configuration

How Hermes selects models and providers, what paths control runtime behavior, and record of verified configurations.

## Active Config Model

Hermes reads the **active inference target** from the top-level `model:` section in `~/.hermes/config.yaml`:
- `model.provider`
- `model.chat_model`
- `model.default`
- `model.base_url`

Subsections like `providers.<id>` describe configured provider families and hold wizard defaults such as `providers.<id>.default_model`. They do **not** switch the active runtime provider on their own.

Common failure mode: editing a `providers.*` subsection and assuming it changes the active session model. It does not. Use `model.*` keys.

## Switching Providers

```bash
# Wrong: only updates a subsection hint
hermes config set providers.nous.default_model X

# Right: set active provider/model
hermes config set model.provider opencode-go
hermes config set model.chat_model deepseek/deepseek-v4-flash
hermes config set model.default ''
hermes config set model.base_url ''
```

## Environment Variables and Keys

Provider credentials are loaded from `~/.hermes/.env` or via Bitwarden Secrets Manager. After changing provider/changes, restart the session and gateway if needed:
```bash
hermes gateway restart
```

## xAI OAuth (Remote/VPS Setup)

xAI Grok OAuth requires a browser callback to `127.0.0.1:56121`. On a headless VPS, this needs an SSH tunnel.

### SSH Tunnel Approach
```bash
# From WSL/local machine — forward port 56121 to VPS:
ssh -L 56121:127.0.0.1:56121 root@<vps-ip>

# On VPS (after tunnel is ready):
hermes auth add xai-oauth --no-browser
# → prints auth URL, starts listener on port 56121
# → user opens URL in WSL browser, authorizes, callback routes through tunnel
```

### Port Issues
- **Default port:** 56121 (defined in `auth.py` as `XAI_OAUTH_REDIRECT_PORT`)
- **Fallback:** If port 56121 is occupied, listener falls back to random port (e.g. 40399)
- **Check before starting:** `ss -tlnp | grep 56121` — if occupied, kill the process first
- **Stuck processes:** Previous failed auth attempts may leave ports bound. Kill with `kill <pid>` before retrying.

### Manual-Paste Mode
For environments where port forwarding is impractical:
```bash
hermes auth add xai-oauth --manual-paste
# → prints auth URL, waits for user to paste callback URL/code
# → user opens URL, authorizes, copies failed redirect URL or bare code
```
Note: Each `--manual-paste` invocation generates a NEW PKCE challenge. The authorization code from a previous URL won't work — user must re-authorize with the new URL.

### Common Failures
1. **PKCE verification failed** — Authorization code from a different URL/challenge. Must re-authorize with the current URL.
2. **Port already in use** — Kill stuck process, verify port is free, retry.
3. **Callback never arrives** — SSH tunnel not established or port mismatch. Verify `ssh -L` uses same port as listener.
4. **Telegram URL corruption (CRITICAL)** — Long OAuth URLs get line-break-wrapped when displayed in Telegram, corrupting query parameters. The `code_challenge` and `state` values become invalid. **Never paste long OAuth URLs directly into Telegram chat.** Fix: write the auth URL to a file (`/tmp/xai-auth-url.txt`) and have the user read it via SSH: `ssh root@<vps-ip> cat /tmp/xai-auth-url.txt` from their WSL terminal. This preserves the URL intact.

## Delegation Config Drift (CRITICAL PITFALL)

When the active model is switched mid-session (e.g. via `/model` or `hermes config set model.default X`), **`delegation.provider` and `delegation.model` do NOT auto-update.** If they remain empty strings, subagents silently fall back to the stale top-level provider.

**Fix — two commands (run for the active profile):**
```bash
hermes --profile <profile-name> config set delegation.provider xai
hermes --profile <profile-name> config set delegation.model x-ai/grok-4.3
# Use the actual working provider + model from your session
```

**Verification:**
```bash
grep -A 10 '^delegation:' ~/.hermes/config.yaml
# Should show non-empty provider and model values
```

**Prevention:** After any model/provider switch, always verify `delegation.provider` and `delegation.model` are set. Empty strings cause silent fallback.

**Never reference deleted infrastructure** (GBrain, PGLite, old deepseek mandates). The user has explicitly removed the entire system. Any lingering references in responses, skills, or memory must be retired immediately. This is a hard user preference.

## OpenCode Go Topology

See `references/opencode-go-setup.md` for the verified DeepSeek V4 setup, model-name caveats, and known provider quirks including Why dots must be preserved.

## Profile-Specific Grok Model Assignment (User Preference — June 2026)

See `references/grok-profile-mapping.md` for the canonical, user-approved mapping after full conversation review.

**Key preferences to always follow:**
- Assign models per profile based on persona and workload (class-level pattern).
- Use lighter/non-reasoning variants for soft or mechanical profiles (**Euphy** especially — user explicitly stated it does not need high-spec).
- Use high-reasoning or flagship (Grok 4.3) for intellectual depth (mike, research).
- **Never reference deleted systems** (GBrain, PGLite, old deepseek mandates, or related memory). The user has completely removed this infrastructure. Any mention is a hard style violation. This skill must actively prevent it.

**Approved mapping (user confirmed):**
- default: `x-ai/grok-4.3`
- euphy: `x-ai/grok-4.2-non-reasoning`
- mike: `x-ai/grok-4.2-reasoning`
- research: `x-ai/grok-4.3`
- scraper: `x-ai/grok-4.2-non-reasoning`
- worker: `x-ai/grok-4.2-multi-agent`

**Update method (preferred):**
```bash
hermes --profile <name> config set model.provider xai
hermes --profile <name> config set model.default x-ai/grok-4.3
```

Always verify with `hermes --profile <name> config show model` after changes. This pattern emerged from multiple iterations where the user corrected model choices and outdated references.
