# Delegation & Auxiliary Billing Drift

## Problem: Subagent 404s after model switch

When changing models/providers mid-session, only `model.provider` updates.  
`delegation.provider` and `delegation.model` remain empty.

Subagents inherit the *top-level* provider from config.yaml at startup.  
If that top-level value is stale (e.g. `opencode-go`, an old free quota that reset, a defunct model id), subagents route to a dead or exhausted backend and fail before any tool runs.

Symptom in logs:
```
provider=opencode-go base_url=... error=NotFoundError
HTTP 404 — Not Found | opencode
Error code: 429 - Monthly usage limit reached
```

**Fix:** Explicitly pin both fields:
```bash
hermes config set delegation.provider <provider>
hermes config set delegation.model <model>
```

## Problem: "Free" main model still burning credits

Nous Portal `step-*:free` (or similar grant models) are inference-only.  
Hermes makes background calls through the **auxiliary client** for:
- context compression between large turns
- vision fallback descriptions
- web_extract preprocessing
- session_search / skills_hub lookups
- title generation, triage, approval prompts, MCP tool generation

With `provider: auto`, auxiliary auto-resolves to the main provider and hits the same grant/credit pool.

Symptom in logs:
```
Auxiliary: marking nous unhealthy for 60s (payment / credit error)
Inference call #N: ... auxiliary model=...
```

**Fix:** Point auxiliary explicitly to a free provider:
```bash
hermes config set auxiliary.compression.provider openrouter
hermes config set auxiliary.compression.model nvidia/nemotron-3-super-120b-a12b:free
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model nvidia/nemotron-3-super-120b-a12b:free
hermes config set auxiliary.web_extract.provider openrouter
hermes config set auxiliary.web_extract.model nvidia/nemotron-3-super-120b-a12b:free
# mirror for session_search, skills_hub, approval, mcp, title_generation, triage_specifier, curator
```

## Problem: Config is per-profile, not global

`~/.hermes/config.yaml` controls only the `default` profile.  
Named profiles under `~/.hermes/profiles/<name>/config.yaml` maintain independent `model:`, `delegation:`, and `auxiliary:` blocks.

Fixing default alone leaves other profiles on dead providers.

**Fix pattern:** Write normalized config to each profile explicitly, or `hermes config set` with `--profile <name>` if supported.

## Normalized free-tier template (copy/paste)

```yaml
model:
  default: stepfun/step-3.7-flash:free
  provider: nous
  base_url: ''
auxiliary:
  vision:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  web_extract:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  compression:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  session_search:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  skills_hub:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  approval:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  mcp:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  title_generation:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  triage_specifier:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
  curator:
    provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free
delegation:
  model: deepseek/deepseek-v4-flash:free
  provider: nous
  base_url: ''
  api_key: ''
  api_mode: ''
  inherit_mcp_toolsets: true
  max_iterations: 50
  child_timeout_seconds: 600
  reasoning_effort: ''
  max_concurrent_children: 3
  max_spawn_depth: 1
  orchestrator_enabled: true
```

After updating config, restart gateway / start a new session to activate.
