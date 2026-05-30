# OpenRouter Embedding Models — Provider Quirks & Dimension Passthrough

## The Problem

GBrain (v0.41.10.1) fails to import pages when using certain embedding models via OpenRouter. The error:

```
Embedding dim mismatch: model nvidia/llama-nemotron-embed-vl-1b-v2 returned 2048 but schema expects 1024.
```

## Root Cause

In `src/core/ai/dims.ts`, the `dimsProviderOptions()` function has a switch on `implementation` that only passes `dimensions` in the request body for explicitly known models:

- `native-openai` → passes `{ openai: { dimensions: dims } }` for text-embedding-3 models
- `native-google` → passes for gemini-embedding models
- `openai-compatible`:
  - ZeroEntropy zembed-1 → passes with `input_type`
  - Voyage models → passes with `input_type`  
  - OpenAI text-embedding-3 → passes
  - DashScope / Zhipu → passes for specific model IDs
  - MiniMax embo-01 → passes `type: 'db'`
  - **Everything else → `return undefined`** ← THE BUG

The `openrouter` recipe uses `implementation: 'openai-compatible'`. When `dimsProviderOptions` returns `undefined`, the Vercel AI SDK doesn't include `dimensions` in the request body, so OpenRouter returns the model's native dimension (2048 for NVIDIA Nemotron Embed VL).

## The Fix

In `src/core/ai/dims.ts`, replace `return undefined;` at line 231 with:

```typescript
return { openaiCompatible: { dimensions: dims } };
```

This is safe because any OpenAI-compatible endpoint that doesn't support `dimensions` silently ignores the field per spec.

**After fix**, `gbrain providers test --model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2` shows:
```
Probing embedding provider...
  ✓ 722ms, 1536 dims
All probes green.
```

## Verified Working OpenRouter Embedding Models

| Model ID | Cost | Dims | Status |
|----------|------|------|--------|
| `nvidia/llama-nemotron-embed-vl-1b-v2` | FREE | 512/768/1024/1536 | ✅ Always works |
| `openai/text-embedding-3-small` | $0.02/M | 1536 | ❌ "Insufficient credits" on some OR accounts |
| `bge-m3` | $0.01/M | 1024 | ❌ Same routing issue |
| `qwen/qwen3-embedding-8b` | $0.01/M | variable | ❌ Same routing issue |

The "Insufficient credits" error for OpenAI/BGE/Qwen models is an OpenRouter routing issue, not a balance problem. Direct API calls with the same key succeed.

## Direct API Test (works correctly)

```bash
curl -s https://openrouter.ai/api/v1/embeddings \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/llama-nemotron-embed-vl-1b-v2","input":"hello test","dimensions":1024}'
```

This returns a 1024-dim embedding with `cost: 0`.

## Version

GBrain v0.41.10.1. The fix applies to `src/core/ai/dims.ts` in the `openai-compatible` implementation case. Since GBrain runs via `bun link` (source → `src/cli.ts`), the patch takes effect immediately without rebuilding.
