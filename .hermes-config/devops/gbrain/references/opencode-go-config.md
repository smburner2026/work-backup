# OpenCode Go as a gbrain Chat Model Provider

## Background

OpenCode Go (https://opencode.ai/go) is a subscription API service ($5 first month, $10/month) providing access to curated open-source coding models. Despite its name, it is NOT just a Hermes ACP transport — it provides a standalone OpenAI-compatible chat completions API.

## API Details

- **Endpoint:** `https://opencode.ai/zen/go/v1/chat/completions`
- **Auth:** Bearer token (API key from subscription)
- **Format:** OpenAI-compatible (`@ai-sdk/openai-compatible`)
- **Available models:** deepseek-v4-flash, deepseek-v4-pro, glm-5, glm-5.1, kimi-k2.5, kimi-k2.6, mimo-v2.5, mimo-v2.5-pro, minimax-m2.5, minimax-m2.7, qwen3.5-plus, qwen3.6-plus
- **Model ID format on wire:** `deepseek-v4-flash` (not `opencode-go/deepseek-v4-flash` — that's the OpenCode CLI config convention)
- **Limits:** Dollar-based windows ($12/5h, $30/week, $60/month)
- **Privacy:** Zero-retention policy, data not used for training
- **No embedding support:** Chat completions only

## gbrain Configuration

gbrain's `provider_base_urls` config key overrides the base URL for any registered recipe. The `deepseek` recipe is the best fit since it's already `openai-compatible` tier:

```bash
# Set API key (gbrain sends it as Authorization: Bearer)
export DEEPSEEK_API_KEY='your-opencode-go-api-key'

# Override the deepseek recipe base URL to OpenCode Go
# IMPORTANT: use JSON notation — dot notation silently fails
gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}'

# Set chat model to use OpenCode Go's model ID
gbrain config set chat_model deepseek:deepseek-v4-flash

# Also set config keys so think command routes correctly
gbrain config set models.default deepseek:deepseek-v4-flash
gbrain config set models.think deepseek:deepseek-v4-flash
```

## Split-Provider Pattern (Recommended)

Use OpenRouter + free NVIDIA Nemotron for embeddings, OpenCode Go for chat:

```bash
# Embeddings via OpenRouter (free)
export OPENROUTER_API_KEY='your-openrouter-key'
gbrain init --pglite \
  --embedding-model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 \
  --embedding-dimensions 1024

# Chat via OpenCode Go (JSON notation required, dot notation silently fails)
export DEEPSEEK_API_KEY='your-opencode-go-key'
gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}'
gbrain config set chat_model deepseek:deepseek-v4-flash
gbrain config set models.default deepseek:deepseek-v4-flash
gbrain config set models.think deepseek:deepseek-v4-flash
```

## gbrain Recipe Details

The `deepseek` recipe in `src/core/ai/recipes/deepseek.ts`:
- `id: 'deepseek'`
- `tier: 'openai-compat'`
- `implementation: 'openai-compatible'`
- `base_url_default: 'https://api.deepseek.com/v1'` (overridden via `provider_base_urls`)
- `auth_env: { required: ['DEEPSEEK_API_KEY'] }`
- Chat touchpoint: supports_tools=true, supports_subagent_loop=true, max_context=128K

## Limitations

- OpenCode Go provides **no embedding endpoint** — gbrain still needs a separate embedding provider (OpenRouter/Nemotron, Google, local Ollama, or skip embeddings)
- The `DEEPSEEK_API_KEY` env var name is misleading when pointing at OpenCode Go — it's just the auth header mechanism. The key itself is the OpenCode Go API key.
- Model IDs must match what OpenCode Go expects on the wire (e.g., `deepseek-v4-flash`), not the `opencode-go/` prefix convention from their OpenCode CLI config format.

## Known Pitfalls

### `gbrain config set` dot notation silently fails

`gbrain config set provider_base_urls.deepseek '...'` (dot notation) is **silently accepted but does not persist** on v0.41.10.1. Always use JSON notation:

```bash
# ✓ Works
gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}'

# ✗ Silently fails
gbrain config set provider_base_urls.deepseek 'https://opencode.ai/zen/go/v1'
```

### `config show` vs `config get` read different sources

After running `gbrain config set`, always verify with `config get`:

```bash
# Shows what gbrain actually uses at runtime (DB source)
gbrain config get chat_model

# Shows ~/.gbrain/config.json (may be stale — not synced from DB)
gbrain config show
```

The JSON file (`~/.gbrain/config.json`) must be manually updated after `config set` changes to keep it in sync. The DB config is authoritative at runtime.

### `gbrain providers test` fails before init

The `providers test` command validates the full provider pipeline including embedding configuration. Before `gbrain init`, chat model tests fail even if the endpoint is valid because no embedding provider exists yet. To verify a custom chat endpoint before init, use direct curl against the endpoint.
