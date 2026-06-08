# Nous Portal Billing Diagnosis (Session 2026-06-07)

## User's Core Question
"Why am I still seeing non-inference charges on Nous Portal even when main model is Grok?"

## Root Cause (from full config audit)
Even when:
- Main model = `grok-4.3` / `xai-oauth`
- Delegation = `grok-4.3` / `xai-oauth`
- Most `auxiliary:` services = `grok-4.3` / `xai-oauth`

The following still routed through Nous infrastructure:

- `browser`: `cloud_provider: browser-use` + `use_gateway: true`
- `image_gen`: `use_gateway: true` (FAL)
- `video_gen`: `use_gateway: true` (FAL)
- Persistent `nous` provider block with `default_model: openrouter/qwen3-coder:free`

"Non-inference" line items are typically from these **gateway-managed tool backends**, not LLM tokens.

## User's Explicit Preferences (embed in all future responses)
- "no lock grok in as the aux" — do not force Grok for auxiliary models unless explicitly requested.
- When user says "just run them", "dispatch all of them", or similar — switch to immediate execution. Do not produce additional analysis or kanban cards.
- `mike` profile = **all DABT work only**. Do not mix DABT context into `default`.

## Resolution Steps Taken
1. Disabled gateway entirely (`use_gateway: false` across config).
2. Removed `cloud_provider: browser-use`.
3. Restarted gateway.
4. Updated `hermes-agent` skill with this diagnostic and user preferences.

## Verification Commands
```bash
hermes config get browser.use_gateway
hermes config get image_gen.use_gateway
hermes config get video_gen.use_gateway
hermes gateway status
```

Expected: all should show `false`.

## Future Prevention
- Always audit the full `auxiliary:`, `gateway:`, `image_gen:`, `video_gen:`, and `browser:` sections after any model change.
- When user expresses frustration with over-analysis ("why aren't you doing them"), immediately update the governing skill (`hermes-agent` or `orchestration-workflow`) with the preference.

This reference file should be consulted whenever billing or gateway issues appear.