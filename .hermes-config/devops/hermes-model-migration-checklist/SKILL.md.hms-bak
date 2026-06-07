---
name: hermes-model-migration-checklist
description: "Fix config drift after model/provider switches in Hermes Agent. Use whenever model has changed mid-session and delegation/auxiliary calls start failing or charging unexpectedly."
version: 1.0.0
author: agent-self
license: MIT
tags: [hermes, config, delegation, billing, free-tier, troubleshooting]
---

# Hermes Model Migration Checklist

Model switches (via `hermes model` or manual edits) frequently leave stale config behind. This skill documents the complete drift pattern and the precise fixes.

## Symptoms

- `delegate_task` returns HTTP 404 / Not Found
- Subagent falls back to old provider/model
- "Auxiliary: marking nous unhealthy for 60s (payment / credit error)"
- Context compression burns grant credits unexpectedly
- Main session works on new model, but subagents/background jobs do not

## Root Cause

Hermes has **three independent routing layers** that are NOT synchronized by `hermes model`:

| Layer | Config key | Drift risk |
|---|---|---|
| Main session | `model.provider`, `model.chat_model`, `model.default` | High |
| Subagents | `delegation.provider`, `delegation.model` | **Critical** — empty values inherit stale top-level defaults |
| Auxiliary system | `auxiliary.compression.*`, `auxiliary.vision.*`, `auxiliary.web_extract.*` | High |

When these drift, the system silently routes different traffic to different providers (some possibly dead, some paid, some over quota).

## Full Repair Sequence

Run every step. Do not skip.

```bash
# 1. Inspect current config
grep -E '^(model|delegation|auxiliary):' ~/.hermes/config.yaml
grep -A 15 '^delegation:' ~/.hermes/config.yaml
grep -A 15 '^auxiliary:' ~/.hermes/config.yaml

# 2. Set main session routing
hermes config set model.provider <WORKING_PROVIDER>
hermes config set model.chat_model <WORKING_MODEL>
hermes config set model.default <WORKING_MODEL>

# 3. Fix delegation — THIS IS THE COMMON FAILURE POINT
hermes config set delegation.provider <WORKING_PROVIDER>
hermes config set delegation.model <WORKING_MODEL>

# 4. Fix auxiliary (compression, vision, web_extract)
hermes config set auxiliary.compression.provider <AUX_PROVIDER>
hermes config set auxiliary.compression.model <AUX_MODEL>
hermes config set auxiliary.vision.provider <AUX_PROVIDER>
hermes config set auxiliary.vision.model <AUX_MODEL>
hermes config set auxiliary.web_extract.provider <AUX_PROVIDER>
hermes config set auxiliary.web_extract.model <AUX_MODEL>
```

## Example: Free-Tier Only Setup

```bash
# Main + delegation → Nous free tier
hermes config set model.provider nous
hermes config set model.chat_model stepfun/step-3.7-flash:free
hermes config set model.default stepfun/step-3.7-flash:free
hermes config set delegation.provider nous
hermes config set delegation.model stepfun/step-3.7-flash:free

# Auxiliary → OpenRouter free tier (avoids burning Nous grant credits)
hermes config set auxiliary.compression.provider openrouter
hermes config set auxiliary.compression.model nvidia/nemotron-3-super-120b-a12b:free
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model nvidia/nemotron-3-super-120b-a12b:free
hermes config set auxiliary.web_extract.provider openrouter
hermes config set auxiliary.web_extract.model nvidia/nemotron-3-super-120b-a12b:free
```

## Verification

```bash
# Confirm resolved config
grep -A 5 '^model:' ~/.hermes/config.yaml
grep -A 12 '^delegation:' ~/.hermes/config.yaml
grep -A 20 '^auxiliary:' ~/.hermes/config.yaml

# Test main chat
timeout 60 hermes chat -q 'reply OK' -m <WORKING_MODEL> --provider <WORKING_PROVIDER>

# Test delegation
delegate_task with goal="Reply OK"
```

## Named Profiles

Each named profile under `~/.hermes/profiles/<name>/config.yaml` has its own `model:` and `delegation:` blocks. They are NOT modified by editing the default profile config.

If you use cron jobs, kanban workers, or multi-agent flows under named profiles, repeat the repair sequence for each profile whose config references a dead or paid provider.

Common stale values to hunt for: `opencode-go`, `opencode-zen`, `minimax-m3`, `deepseek-v4-flash` (when not explicitly free-tier).

## Browser Automation Note

Browser costs are controlled by `browser.engine` and `browser.cloud_provider`, NOT by the model routing:
- `engine: lightpanda` → free, self-hosted
- `engine: camofox` → free, self-hosted Firefox
- `cloud_provider: browser-use` → local lightweight (free)
- `cloud_provider: browserbase` → paid cloud (avoid unless explicitly needed)

Check with:
```bash
grep -A 10 '^browser:' ~/.hermes/config.yaml
```

## Pitfalls

- **Do not edit `~/.hermes/config.yaml` directly** when secrets are managed by Bitwarden — use `hermes config set` so secrets stay managed.
- `hermes config set` triggers Bitwarden sync on every call. This is normal.
- After any `hermes config set`, restart the session (`/reset` or new `hermes` invocation) for changes to take effect.
- Delegation changes do NOT apply to the current running session — they take effect on the next session.
- The `opencode-go` endpoint `https://opencode.ai/zen/go/v1` does not support all models (e.g. `minimax-m3` returns HTML 404). Avoid mixing models across providers without explicit provider binding.
- The `auxiliary.client` retry loop can silently burn grant credits even when the main model is free. Always verify assistant log: `grep auxiliary ~/.hermes/logs/agent.log | tail -20`.
