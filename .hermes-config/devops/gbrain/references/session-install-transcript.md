# G-Brain Install Transcript (2026-05-25)

## Environment

- Host: Linux 6.8.0-117-generic
- Bun: 1.3.14 at `/root/.bun/bin/bun`
- Hermes profile: default (opencode-go provider)
- API keys in BWS: OPENROUTER_API_KEY, OPENCODE_GO_API_KEY, TAVILY_API_KEY

## Install Steps (verified working)

```bash
# 1. Clone
git clone https://github.com/garrytan/gbrain.git ~/gbrain

# 2. Install deps
export PATH="/root/.bun/bin:$PATH"
cd ~/gbrain && bun install

# 3. Register CLI
bun link

# 4. Verify
gbrain --version   # → 0.41.10.1
```

## Key Discovery: OpenRouter as Embedding Provider

The user has an OpenRouter key in BWS but NO OpenAI key. GBrain v0.41.x supports OpenRouter as an embedding provider out of the box.

**Resolution from BWS:**
```bash
set -a; source /root/.hermes/.env 2>/dev/null; set +a
```

### OpenRouter Embedding Model Issues

Multiple models return "Insufficient credits" on OR despite valid balance:
- `openai/text-embedding-3-small`
- `bge-m3`  
- `qwen/qwen3-embedding-8b`

**Working model:** `nvidia/llama-nemotron-embed-vl-1b-v2` — **FREE** on OpenRouter, 131K context, consistently works.

### Dimension Passthrough Bug

NVIDIA model kept returning 2048-dim vectors regardless of configured dims (1024). Root cause: `dimsProviderOptions()` in `src/core/ai/dims.ts` returns `undefined` for unknown models in the `openai-compatible` case — no `dimensions` parameter sent to API. Patched by changing the fallthrough from `return undefined` to `return { openaiCompatible: { dimensions: dims } }`.

## Final Configuration

| Setting | Value | Cost |
|---------|-------|------|
| Embedding model | `openrouter:nvidia/llama-nemotron-embed-vl-1b-v2` (1024d) | **Free** |
| Chat model | `openrouter:inclusionai/ling-2.6-flash` | $0.01/M in |
| Search mode | conservative | Minimal |
| Storage | PGLite (local, no server) | Free |
| Brain repo | `~/brain/` | Git-backed |

## DABT Reference Import

**Source:** `/root/work/dabt/dabt-tutor/reference/extracted/` (Casarett 9e 72 ch, Hayes 7e 80 ch, 60 regulations, ABT handbook)

**Import process:**
1. Copied `.txt` files to `~/brain/extracted/` as `.md` (excluding `.hms-bak` backups)
2. Ran `gbrain import ~/brain/extracted/` — 105 files, 26MB total
3. First pass timed out at 180s (54% complete) — large Haye's chapters slow to embed
4. Second pass completed remaining files (GBrain skips unchanged)
5. Total: **106 pages imported, 6,597 chunks, all embedded**

**Search verification:**
```
gbrain search "carcinogenesis mechanism"
  → 0.7977 casarett-doull-9e/3-mechanisms-of-toxicity
  → 0.7391 hayes-7e/19-metals
  → 0.7063 hayes-7e/2-use-of-toxicology-in-the-regulatory-process
  → 0.6328 regulations/epa_cancer_guidelines_2005
```

## Key Commands After Setup

```bash
# Query/search
gbrain search "query text"
gbrain think "synthesis question"  # uses chat model ($0.01/M)

# Add new knowledge
echo "# My Note" > ~/brain/new-topic.md
gbrain import ~/brain/

# Check health
gbrain doctor
gbrain stats

# Switch chat model
gbrain config set chat_model openrouter:inclusionai/ling-2.6-flash
```
