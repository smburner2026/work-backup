# OpenCode Go — Verified Setup Notes

## Provider constants

- Provider ID: `opencode-go`
- Env vars: `OPENCODE_GO_API_KEY`, `OPENCODE_GO_BASE_URL`
- Default base URL: `https://opencode.ai/zen/go/v1`
- Hermes profile plugin path: `/usr/local/lib/hermes-agent/plugins/model-providers/opencode-zen/__init__.py`

## Model-name normalization

OpenCode Go preserves dots in model IDs. Older Hermes bug: `.` in model IDs could be replaced with `-` (see NousResearch/hermes-agent PR #17011).
Set `model.chat_model` using the dot-preserved form: `deepseek/deepseek-v4-flash`, not `deepseek/deepseek-v4-flash-free` variants unless recursion intended.

Recurring anthology-of-errors note in session history links `Confirming opencode-go provider usage` to the `deepseek-v4-pro` model. Likely cause: `model.chat_model` was set to the slash-less short form instead of `provider/model` form, or `model.default` still overrode it.

## Verified DeepSeek V4 endpoint flow

1. Ensure `OPENCODE_GO_API_KEY` is set in `.env` or via Bitwarden Secrets Manager.
2. Ensure `OPENCODE_GO_BASE_URL` is `https://opencode.ai/zen/go/v1`.
3. Set active config:
   - `model.provider` = `opencode-go`
   - `model.chat_model` = `deepseek/deepseek-v4-flash`
   - `model.default` = `''`
   - `model.base_url` = `''` so provider's default URL is used.
4. Restart session (`/reset`) and gateway (`hermes gateway restart`).
5. Confirm with `hermes dump` and `hermes config`.

## Pitfalls

- `model.base_url` set to the Nous inference endpoint while provider is `opencode-go` causes cross-provider wire mismatch.
- Provider subsections (`providers.nous`) do not switch runtime providers on their own.
- `model.default` holding a non-empty value can mask `model.chat_model`.
- Some `deepseek-v4-*` short aliases exist in registry but OpenCode Go routing expects `deepseek/deepseek-v4-flash`.
