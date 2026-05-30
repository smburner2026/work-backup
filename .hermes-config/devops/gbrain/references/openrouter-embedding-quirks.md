# OpenRouter Embedding Models — Complete Reference

## Dimension Passthrough Bug (GBrain v0.41.10.1)

In `src/core/ai/dims.ts`, the `dimsProviderOptions()` function falls through to `return undefined` for unrecognized `openai-compatible` models, so the `dimensions` parameter is never sent in the request body.

**Fix:** In `src/core/ai/dims.ts`, replace `return undefined;` with:
```typescript
return { openaiCompatible: { dimensions: dims } };
```

Safe because OpenAI-compatible endpoints silently ignore unsupported fields per spec.

## Verified Models & Availability

| Model ID | Cost | Dims | Status |
|----------|------|------|--------|
| `nvidia/llama-nemotron-embed-vl-1b-v2` | **FREE** | 512/768/1024/1536 | ✅ Always works |
| `openai/text-embedding-3-small` | $0.02/M | 1536 | ❌ "Insufficient credits" on some OR accounts |
| `baai/bge-m3` | $0.01/M | 1024 | ❌ Same routing issue |
| `qwen/qwen3-embedding-8b` | $0.01/M | variable | ❌ Same routing issue |

The "Insufficient credits" error is an **OpenRouter routing issue**, not actual balance exhaustion. The key is valid; the model endpoint just can't serve this key/tier.

## NVIDIA Dimension Constraints

The test probe returns 2048d native, but the model only accepts 512/768/1024/1536. Init with:
```bash
gbrain init --pglite \
  --embedding-model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 \
  --embedding-dimensions 1024
```

## Chat Model Defaults

When `OPENROUTER_API_KEY` is detected: `gbrain init` auto-selects `openrouter:openai/gpt-5.2`. Override:
```bash
gbrain config set chat_model openrouter:<model-id>
```

## BWS Token Issue

`bws secret list` may fail with:
```
Error:
   0: Doesn't contain a decryption key
```
**Workaround:** Source keys directly from `.env` instead of using BWS for gbrain:
```bash
set -a; source ~/.hermes/.env 2>/dev/null; set +a; gbrain init --pglite ...
```

## Final Working Configuration (May 2026)

```
Embedding: openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 (1024d, FREE)
Chat:      openrouter:openai/gpt-5.2 (or user-preferred)
Search:    conservative (default, no OpenAI key)
Engine:    PGLite (local Postgres, no server)
```
