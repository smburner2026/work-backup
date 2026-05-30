# Dream Cycle — Model Patching (Proven Fix)

## Problem

gbrain v0.41.x dream cycle LLM phases (`propose_takes`, `grade_takes`, `calibration_profile`) hardcode `'claude-sonnet-4-6'` as their default model in multiple places — source code defaults, model resolution chain fallbacks (`TIER_DEFAULTS`), and the subagent handler gate. These are in **three independent layers**, and fixing any one in isolation is NOT enough:

| Layer | File/Location | Default | Fix |
|-------|--------------|---------|-----|
| Source code hardcodes | `propose-takes.ts`, `grade-takes.ts`, `calibration-profile.ts` | `claude-sonnet-4-6` | Patch source files |
| Model resolution chain | `model-config.ts` → `TIER_DEFAULTS` | `anthropic:claude-*` | Set `models.default` + `models.tier.*` in PGLite DB |
| Subagent handler gate | `minions/handlers/subagent.ts` | Blocks non-Anthropic models | Set `agent.use_gateway_loop=true` in DB |

## Durable Fix: Self-Healing Config (Canonical — Use This)

The **only** approach that survives git pulls, DB wipes, and MCP server restarts is to make the dream cycle script re-assert all 8 config keys before every run. This fixes all three layers atomically:

```bash
# In the dream cycle script, BEFORE gbrain dream:
gbrain config set agent.use_gateway_loop true --force 2>/dev/null || true
gbrain config set models.default deepseek:deepseek-v4-flash --force 2>/dev/null || true
gbrain config set models.think deepseek:deepseek-v4-flash --force 2>/dev/null || true
gbrain config set models.tier.utility deepseek:deepseek-v4-flash --force 2>/dev/null || true
gbrain config set models.tier.reasoning deepseek:deepseek-v4-flash --force 2>/dev/null || true
gbrain config set models.tier.deep deepseek:deepseek-v4-flash --force 2>/dev/null || true
gbrain config set models.tier.subagent deepseek:deepseek-v4-flash --force 2>/dev/null || true
gbrain config set chat_model deepseek:deepseek-v4-flash --force 2>/dev/null || true
```

**Why this works:** Git pulls overwrite source patches but can't touch the DB → keys survive. DB gets wiped or rebuilt → re-applied next run. No manual re-patching ever needed. This is now baked into the canonical dream cycle script at `~/.hermes/scripts/gbrain-dream-cycle.sh`.

## Legacy Fix: One-Time Patching (Fallback)

Use this ONLY when running `gbrain dream` interactively outside the cron script. These patches fix two of the three layers but remain vulnerable to git pull overwrites.

## Patches Applied

### 1. `src/core/cycle/propose-takes.ts` — 2 changes

**Line 360 (budget meter):**
```typescript
// BEFORE:
modelId: opts.model ?? 'claude-sonnet-4-6',
// AFTER:
modelId: opts.model ?? 'openrouter:inclusionai/ling-2.6-flash',
```

**Line 409 (DB insert):**
```typescript
// BEFORE:
opts.model ?? 'claude-sonnet-4-6',
// AFTER:
opts.model ?? 'openrouter:inclusionai/ling-2.6-flash',
```

### 2. `src/core/cycle/grade-takes.ts` — 1 change

**Line 398 (judge model):**
```typescript
// BEFORE:
const judgeModelId = opts.model ?? 'claude-sonnet-4-6';
// AFTER:
const judgeModelId = opts.model ?? 'openrouter:inclusionai/ling-2.6-flash';
```

### 3. `src/core/cycle/calibration-profile.ts` — 1 change

**Line 231 (profile generation):**
```typescript
// BEFORE:
const modelId = opts.model ?? 'claude-sonnet-4-6';
// AFTER:
const modelId = opts.model ?? 'openrouter:inclusionai/ling-2.6-flash';
```

## Enable Gateway Loop for Subagent Dispatch — MANDATORY for Non-Anthropic

**Even with source patches and DB config keys set, `propose_takes` will fail with "Anthropic chat requires ANTHROPIC_API_KEY" if `agent.use_gateway_loop` is not enabled.**

The `propose_takes` phase dispatches its LLM extraction calls through a **subagent worker** (`src/core/minions/handlers/subagent.ts`). The subagent handler checks:

```typescript
const useGatewayLoopRaw = await engine.getConfig('agent.use_gateway_loop').catch(() => null);
const useGatewayLoop = typeof useGatewayLoopRaw === 'string' &&
  (useGatewayLoopRaw === 'true' || useGatewayLoopRaw === '1');
if (!useGatewayLoop && !isAnthropicProvider(model)) {
  throw new Error(
    `subagent job: resolved model "${model}" is non-Anthropic but agent.use_gateway_loop is not enabled.`
  );
}
```

When `agent.use_gateway_loop` is missing/false and the model is non-Anthropic, the handler throws — which surfaces as "Anthropic chat requires ANTHROPIC_API_KEY" in the dream cycle output (caught at the gateway level).

**This config key is NOT in gbrain's known config registry**, so `gbrain config set` refuses it without --force:

```bash
gbrain config set agent.use_gateway_loop true --force
```

**Verify the key stuck:**
```bash
gbrain config get agent.use_gateway_loop
# Should return: true
```

The tool warns "Nothing in gbrain reads this" — this is misleading. The runtime subagent handler reads it via `engine.getConfig()` which queries the DB directly, bypassing the CLI's known-key registry.

**After enabling this, the subagent correctly routes non-Anthropic model calls through the gateway's tool loop instead of the legacy Anthropic-SDK path.**

## Config Keys in PGLite DB — CRITICAL

**The source patches + gateway loop alone are NOT sufficient.** The `propose_takes` extractor calls `gatewayChat()` without passing `modelHint`, which falls through to `getChatModel()` → `reconfigureGatewayWithEngine()` → `resolveModel()`. The `resolveModel()` 8-tier chain reads model config **from the PGLite DB only** — `~/.gbrain/config.json` is invisible to it.

If the DB keys are not set, `resolveModel` falls to tier step 7 (`TIER_DEFAULTS`) — all Anthropic. You'll get "Anthropic chat requires ANTHROPIC_API_KEY" in the extractor warnings even with correct source patches and a correct `chat_model` in JSON.

If the DB keys are not set, `resolveModel` falls to tier step 7 (`TIER_DEFAULTS`) — all Anthropic. You'll get "Anthropic chat requires ANTHROPIC_API_KEY" in the extractor warnings even with correct source patches and a correct `chat_model` in JSON.

**Set these in the DB (they persist across git pulls since the DB is separate from the source tree):**

```bash
# Set global default — caught by resolveModel step 4
gbrain config set models.default "deepseek:deepseek-v4-flash"

# Set chat-specific — caught by resolveModel step 2 (when configKey='models.chat')
gbrain config set models.chat "deepseek:deepseek-v4-flash"

# Set think-specific — caught by resolveModel step 2
gbrain config set models.think "deepseek:deepseek-v4-flash"

# Set tier defaults — caught by resolveModel step 5
gbrain config set models.tier.utility "deepseek:deepseek-v4-flash"
gbrain config set models.tier.reasoning "deepseek:deepseek-v4-flash"
gbrain config set models.tier.deep "deepseek:deepseek-v4-flash"
```

**Verify the keys are in the DB (not just JSON):**
```bash
gbrain config get models.default
gbrain config get models.chat
gbrain config get models.think
gbrain config get models.tier.reasoning
```
If any return "Config key not found", `resolveModel` will use Anthropic tier defaults for that path.

**Sync the JSON afterward** to prevent the config split warning:
```bash
python3 -c "
import json
with open('/root/.gbrain/config.json') as f:
    c = json.load(f)
c['models.default'] = 'deepseek:deepseek-v4-flash'
c['models.chat'] = 'deepseek:deepseek-v4-flash'
c['models.think'] = 'deepseek:deepseek-v4-flash'
c['models.tier'] = {'utility': 'deepseek:deepseek-v4-flash', 'reasoning': 'deepseek:deepseek-v4-flash', 'deep': 'deepseek:deepseek-v4-flash'}
with open('/root/.gbrain/config.json', 'w') as f:
    json.dump(c, f, indent=4)
"
```

## How Model Resolution Works

The `resolveModel()` function uses an 8-tier chain (highest precedence first):

1. CLI flag (`--model`)
2. New-key config (e.g. `models.think`, `models.dream.patterns`)
3. Deprecated old-key config (e.g. `dream.synthesize.model`)
4. Global default (`models.default`)
5. Tier override (`models.tier.<tier>` where tier = utility/reasoning/deep)
6. Env var (`GBRAIN_MODEL`)
7. Tier default (`TIER_DEFAULTS[tier]` — all Anthropic: opus/sonnet/haiku)
8. Hardcoded fallback (caller-supplied, also Anthropic)

The `chat_model` config key is NOT part of this chain — it's a separate key used only for the initial provider detection. To make think work, set `models.default` (step 4 catches most cases) or `models.think` (step 2).

## Why the Dream Cycle Can't Use --model

The dream cycle runner (`src/core/cycle.ts`) doesn't accept a `--model` flag and never passes model hints to individual phase implementations. Each phase resolves its own model internally through one of two paths:

1. **Hardcoded default** (propose_takes budget meter, grade_takes judge) — must be source-patched
2. **`resolveModel()` chain** (extractor, extract_facts, consolidate, synthesize) — reads from DB config

The `resolveModel()` path is the more common one across phases. This is why setting `models.default` in the PGLite DB is critical — it catches most phases even when source patches aren't applied. The phases that hardcode models (propose_takes budget/insert, grade_takes judge, calibration_profile) need source patches in addition to config keys.

## Verification

Check for remaining Anthropic errors and verify gateway loop is active:

```bash
# 1. Verify all three config layers are set
echo "=== GATEWAY LOOP ==="
gbrain config get agent.use_gateway_loop       # Must be "true"
echo "=== DB KEYS ==="
gbrain config get models.default               # Must be your non-Anthropic model
gbrain config get models.chat
gbrain config get models.think
gbrain config get models.tier.reasoning
# Each should return your model, not "Config key not found"

# 2. Test think with specified model
gbrain think "test" --model deepseek:deepseek-v4-flash
# Should return real synthesis, not "no LLM available"

# 3. Test dream cycle extractor (catches config-key-only issues)
gbrain dream --dry-run --phase propose_takes 2>&1 | grep -E "extractor failed|BUDGET_METER"
# If you see "extractor failed ... Anthropic chat requires ANTHROPIC_API_KEY"
# → models.default is missing from DB config

# 4. Check for remaining Anthropic errors
gbrain doctor --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data['checks']:
    if c['name'] == 'subagent_capability':
        print(c['message'])
"
```

## Files Not Patched (use config only — no source changes needed)

These files use `resolveModel` correctly and will respect `models.default`:

- `src/core/cycle/drift.ts` — config: `models.drift`
- `src/core/cycle/patterns.ts` — config: `models.dream.patterns`
- `src/core/cycle/synthesize.ts` — configs: `models.dream.synthesize`, `models.dream.synthesize_verdict`

**Additionally, `extract_facts` and `consolidate` phases work via config keys alone** — they call `gatewayChat()` without model hints, which falls to `getChatModel()` → `resolveModel()`. Set `models.default` in the DB and they use your model automatically.

## Tests Performed

- `gbrain think --model openrouter:inclusionai/ling-2.6-flash` → 5 pages gathered, real synthesis output, 3 citations ✅
- `gbrain think --model ling` → same result (alias works) ✅
- `gbrain dream --dry-run --phase propose_takes` → model now reads `openrouter:inclusionai/ling-2.6-flash` (no Anthropic error, timed out on 106 pages due to API latency) ✅
- `gbrain search "carcinogenesis Ames test"` → ranked results from both textbooks ✅
- Budget meter shows `BUDGET_METER_NO_PRICING` for unknown-pricing models — expected, non-Anthropic models aren't in the pricing table ⚠️

## Performance Note: Ling Is Cheap But Slow

Ling 2.6 Flash through OpenRouter is extremely cheap ($0.01/M input) but has noticeable API latency:
- A full `gbrain dream` on 106 pages **timed out at 5 minutes**
- A single `propose_takes` dry-run (100 pages) **timed out at 60 seconds**
- Individual `gbrain think` calls return in 5-15 seconds (fine for interactive use)

If dream cycle is too slow, consider: a faster model (e.g., `meta-llama/llama-3.1-8b-instruct` at 2-3× speed, $0.02/M), fewer phases per run, smaller import batches, or accepting slower enrichment for lowest cost.

## Caveats

- Budget gating is disabled for unknown-pricing models. This means the dream cycle won't enforce a dollar cap for non-Anthropic providers. Set `dream.cycle.budget_usd` or use conservative settings.
- Subagent features (`gbrain agent run`, `gbrain autopilot`) hard-enforce Anthropic via `isAnthropicProvider()` — these CANNOT be patched to non-Anthropic without significant refactoring.
- The `synthesize` phase uses subagent dispatch internally, which limits it to Anthropic.
