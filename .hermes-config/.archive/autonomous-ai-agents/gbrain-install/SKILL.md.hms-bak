---
name: gbrain-install
description: "Install, configure, and verify garrytan/gbrain — a production-grade brain layer (PGLite vector DB + knowledge graph + synthesis) for Hermes/OpenClaw agents. Covers clone-vs-global-install decision, OpenRouter embedding model selection, the free NVIDIA Llama Nemotron path, search mode configuration (mandatory stop), and brain init."
version: 1.0
author: Randoooos + Hermes
---

# GBrain Install & Configuration

[garrytan/gbrain](https://github.com/garrytan/gbrain) is a brain layer for AI agents — hybrid search (vector + BM25 + reranker), self-wiring knowledge graph, gap analysis via `gbrain think`, and a durable job queue. Runs on PGLite (zero-config, default) or Supabase/Postgres for scale.

## When to load

- User asks to install gbrain or a "brain layer" for the agent
- User needs persistent knowledge base with semantic search + synthesis
- Setting up a new Hermes/OpenClaw instance that needs knowledge management

## Prerequisites

- **Bun** — installed at `/root/.bun/bin/bun` or via `curl -fsSL https://bun.sh/install | bash`
- **API key** — at minimum an OpenRouter or OpenAI key for embeddings. GBrain auto-detects from env vars.
- **Git** — for cloning the repo

## Installation

### ⚠️ Critical: Bun Global Install Bug (#218)

**Do NOT use `bun install -g github:garrytan/gbrain`.** Bun blocks the top-level postinstall hook on global installs, so schema migrations never run and the CLI aborts. Use the deterministic path:

```bash
git clone https://github.com/garrytan/gbrain.git ~/gbrain
cd ~/gbrain
bun install
bun link
```

Verify: `gbrain --version`

Bun must be in PATH. If `which bun` fails, use the full path:
```bash
export PATH="$HOME/.bun/bin:$PATH"
```

## API Key Configuration

GBrain needs an API key for embeddings. Auto-detects from env vars at init time.

### Preferred: OpenRouter

Set `OPENROUTER_API_KEY` in the environment. Source from the Hermes `.env` file:

```bash
set -a; source ~/.hermes/.env 2>/dev/null; set +a
```

GBrain auto-detects `OPENROUTER_API_KEY` and selects `openrouter` as the provider.

### Available embedding models via OpenRouter

| Model | Dims | Price/M tokens | Notes |
|-------|------|---------------|-------|
| `nvidia/llama-nemotron-embed-vl-1b-v2` | 1024 | **FREE** | 131K context, multimodal. Dims: 512/768/1024/1536 only |
| `openai/text-embedding-3-small` | 1536 | $0.02 | Most popular, 8K context |
| `qwen/qwen3-embedding-8b` | — | $0.01 | 32K context, multilingual |
| `baai/bge-m3` | 1024 | $0.01 | Multilingual retrieval |

### Known OpenRouter gotcha

Some embedding models return **"Insufficient credits"** even when the account has $8+ balance and the key is active. This is a routing/provider issue on OpenRouter's side, not an actual credit shortage. If a model fails, try a different one.

The **NVIDIA Llama Nemotron** model is **free** on OpenRouter and routes reliably — use it as the fallback when paid models fail.

### Alternative: Direct OpenAI

If `OPENAI_API_KEY` is set, GBrain defaults to `openai:text-embedding-3-large` (1536d). This is the simplest path but requires an OpenAI key.

## Brain Initialization

### 1. Init with PGLite (no server needed)

```bash
cd ~/gbrain
gbrain init --pglite —-embedding-model openrouter:<model-id> —-embedding-dimensions <N>
```

If omitting the embedding model flags, GBrain auto-detects from env vars. Explicit flags are recommended to avoid surprises.

**Example with free NVIDIA model:**
```bash
gbrain init --pglite \
  --embedding-model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 \
  --embedding-dimensions 1024
```

### 2. ⛔ STOP — Search Mode Configuration

`gbrain init` auto-applies a search mode (conservative by default when no OpenAI key). **You must NOT silently accept the default.** Present this cost matrix to the user and ask which mode they want:

| Mode | Budget | Best for | Est. cost @ 10K queries/mo |
|------|--------|----------|---------------------------|
| **conservative** | 4K tokens, 10 chunks, no LLM expansion | Cost-sensitive, high-volume loops | $40–$200 |
| **balanced** | 12K tokens, 25 chunks | Middle ground | $100–$500 |
| **tokenmax** | No budget, LLM expansion ON, 50 chunks | Maximum quality | $200–$1,000 |

Cost spread between corners is **25x**. Natural diagonal pairings span ~4x.

To change later:
```bash
gbrain config set search.mode <conservative|balanced|tokenmax>
```

### 3. Configure chat model (optional)

GBrain auto-picks a chat model (defaults to `openrouter:openai/gpt-5.2` when using OpenRouter). The chat model is used by `gbrain think` (synthesis + gap analysis), query expansion, and the dream cycle.

Switch to the user's preferred model:
```bash
gbrain config set chat_model openrouter:deepseek/deepseek-v4-flash
```

**Subagent features** (`gbrain dream`, `gbrain agent run`, `gbrain autopilot`) require `ANTHROPIC_API_KEY` regardless of chat model. Chat alone (`gbrain think`) works without it.

### 4. Verify

```bash
gbrain doctor
```

All checks should return `[OK]` or acceptable warnings. Key indicators:
- `embedding_provider` — green means the embedding model is accessible
- `search_mode` — confirms the active mode
- `schema_version` — should match the binary version

### 5. Set up brain repo

The brain repo (markdown files) is **separate** from the tool repo (`~/gbrain`).

```bash
mkdir -p ~/brain && cd ~/brain && git init
```

Then read `~/gbrain/docs/GBRAIN_RECOMMENDED_SCHEMA.md` for the MECE directory structure.

### 6. Import and index

```bash
gbrain import ~/brain/ --no-embed    # import markdown files
gbrain embed --stale                  # generate vector embeddings
gbrain query "test query"             # verify search works
```

### 7. Knowledge graph (optional)

```bash
gbrain extract links --source db --dry-run | head -20   # preview
gbrain extract links --source db                          # commit
gbrain stats                                              # verify links > 0
```

## Recommended Skills

After install, GBrain suggests installing bundled skills. Show the list to the user and ask before installing:

```bash
gbrain skillpack list                # see all options
gbrain skillpack install --all       # install all (after user confirms)
gbrain skillpack install <name>      # install one
```

## Pitfalls

- **Bun global install bug** (#218) — always use git clone + bun link, not `bun install -g`
- **OpenRouter "Insufficient credits"** — can be a routing issue, not actual credit exhaustion. Try a different model or the free NVIDIA one.
- **NVIDIA embedding model dims** — only accepts 512/768/1024/1536. Default provider test returns 2048 which causes dim mismatch; use `--embedding-dimensions 1024` at init time.
- **BWS access token** — `bws secret list` may fail with "Doesn't contain a decryption key" if the token format is incompatible. Source `.env` directly instead.
- **Anthropic key for subagents** — dream cycle, autopilot, and agent commands need `ANTHROPIC_API_KEY` even if the chat model is non-Anthropic. Warn the user if they try these without it.
- **No OpenAI key** — without it, search mode defaults to conservative and LLM expansion is unavailable. Semantic cache still works.
- **Dimension migration** — switching embedding models later requires `gbrain reinit-pglite` or a full reindex. Choose carefully at init time.
