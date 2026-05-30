# OpenRouter Embedding Provider: Known Quirks & Workarounds

Captured during GBrain install via Hermes (May 2026).

## OpenRouter Key Validation

Confirmed active key: returned `"is_free_tier": false`, `"usage": 8.08` (no hard limit), key label `sk-or-v1-ce5...`.

```
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

## "Insufficient Credits" Error

Some OpenRouter embedding models return this even with $8+ on the account:

```
[embed(openrouter:openai/text-embedding-3-small)] Insufficient credits.
[embed(openrouter:qwen/qwen3-embedding-8b)] Insufficient credits.
```

This is **not actual credit exhaustion**. It's a routing/provider issue on OpenRouter's side — the model can't be served to this key/tier. The key and account are both healthy.

### Models that worked

- `openrouter:nvidia/llama-nemotron-embed-vl-1b-v2` — **FREE**, routed successfully, returned 2048d embedding on first probe

### Models that failed (despite valid key)

- `openrouter:openai/text-embedding-3-small` — "Insufficient credits"
- `openrouter:qwen/qwen3-embedding-8b` — "Insufficient credits"

## NVIDIA Model Dimension Constraints

The test probe returned 2048d but init rejected custom dimensions:

```
Refusing to init: Provider "openrouter" model "nvidia/llama-nemotron-embed-vl-1b-v2"
rejects custom dimensions 2048 (allowed: 512, 768, 1024, 1536).
```

Successful init used `--embedding-dimensions 1024`.

## Chat Model Auto-Default

When `OPENROUTER_API_KEY` is detected: `gbrain init` auto-selects `openrouter:openai/gpt-5.2` as the chat model. This is used by `gbrain think`, query expansion, and the dream cycle. Override with `gbrain config set chat_model openrouter:<model-id>`.

## BWS Token Issue

```
Error:
   0: Doesn't contain a decryption key

Location:
   crates/bws/src/main.rs:67
```

The environment had `BWS_ACCESS_TOKEN` set but `bws secret list` failed with this error. Cause: token format mismatch (possible 2.1.0 client issue with token format). Workaround: source `OPENROUTER_API_KEY` directly from `~/.hermes/.env`:

```bash
set -a; source ~/.hermes/.env 2>/dev/null; set +a
```

## Final Working Configuration

```
Embedding: openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 (1024d, FREE)
Chat:      openrouter:openai/gpt-5.2 (or user-preferred)
Search:    conservative (default, no OpenAI key)
Engine:    PGLite (local Postgres, no server)
Health:    70/100 — OK
```
