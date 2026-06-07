---
name: gbrain
description: "Install, configure, and operate G-Brain (garrytan/gbrain) — a production-grade brain layer for Hermes with synthesis, graph traversal, gap analysis, and self-wiring knowledge graph."
version: 1.8.0
author: Hermes Agent
tags: [gbrain, brain-layer, knowledge-management, rag, synthesis, knowledge-graph]
related_skills: [hermes-maintenance, remote-agent-infrastructure]
---

# G-Brain

G-Brain is a brain layer for AI agents (OpenClaw/Hermes/Claude Code) that goes beyond simple RAG to provide synthesis, graph traversal, and gap analysis in a single system. Powers Garry Tan's personal autonomous agents.

**Key differentiator:** `gbrain search` returns ranked pages; `gbrain think` returns a synthesized answer with explicit citations AND a gap analysis (stale data, missing context, contradictions).

## When to Use

- User asks to install or set up G-Brain
- User needs to configure a knowledge brain for Hermes
- User mentions "brain layer", "gbrain", or Garry Tan's knowledge system
- User wants persistent, searchable knowledge across sessions beyond simple RAG
- User has large reference material collections (textbooks, regulations, research papers) that need cross-source synthesis

## Independent from Hermes Provider Setup (Critical)

**gbrain is a standalone Bun/TypeScript CLI with its own model gateway.** It does NOT inherit, share, or use Hermes's provider/transport infrastructure. This is a frequent source of confusion.

### What this means

| Hermes concept | Does gbrain use it? | 
|---|---|
| Your current Hermes provider (`opencode-go`, `pi`, `claude-code`, `codex`) | **No** — these are ACP subprocess transports, not API providers. gbrain can't connect to them. |
| Hermes `config.yaml` providers | **No** — gbrain reads `~/.gbrain/config.json` and env vars, not Hermes config |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `OPENROUTER_API_KEY` | **Yes** — but only if you export them for gbrain's own use. They must be in gbrain's environment, not just Hermes's. |

### The key implication

If Hermes is running through `opencode-go → deepseek-v4-flash`, that doesn't give gbrain any model access. gbrain needs its **own** API key to one of its supported providers:

- Set `OPENROUTER_API_KEY` → gbrain can use any OpenRouter model
- Set `OPENAI_API_KEY` → gbrain can use OpenAI models
- Set `GOOGLE_GENERATIVE_AI_API_KEY` → gbrain can use Google models  
- Run a local Ollama server → zero API cost, gbrain uses it directly

You cannot "reuse" a Hermes ACP transport like opencode-go (the CLI subprocess) as gbrain's API provider — they are different architectural layers.

### Exception: OpenAI-compatible API services

Some services provide BOTH a standalone OpenAI-compatible API AND a Hermes ACP connector. **OpenCode Go** is an example — its subscription at `https://opencode.ai/zen/go/v1` speaks the standard OpenAI chat completions protocol with a Bearer token key. gbrain CAN use this as a chat model provider via the `provider_base_urls` config key (see [Custom OpenAI-Compatible Endpoints](#custom-openai-compatible-endpoints) below).

**Rule of thumb:** If the service gives you a `POST /v1/chat/completions` endpoint + an API key → gbrain can use it. If it's only an ACP subprocess CLI you run locally → gbrain cannot.

See the [API Key Setup](#api-key-setup) section below for the full built-in provider table.

### MCP wiring caveat

When running gbrain as an MCP server for Hermes, the Hermes MCP client **filters environment variables** — only safe baseline vars (`PATH`, `HOME`, `USER`) plus whatever you add to `mcp_servers.gbrain.env` get passed. So gbrain's API keys must be either:
1. Listed explicitly in `mcp_servers.gbrain.env` → `env:` block in config.yaml
2. OR loaded via a wrapper script that sources them before starting `gbrain serve`

See the [MCP Server Wiring section](#mcp-server-wiring-hermes-agent) for the wrapper script pattern.

## Caveat: Anthropic Key Dependency (Partial — Think Works with OpenRouter via --model)

**gbrain's model support is split between two code paths with different capabilities:**

### gbrain think (synthesis + gap analysis)

**`gbrain think` CAN work with non-Anthropic providers via the `--model` flag.** Confirmed on gbrain v0.41.10.1 with OpenRouter:

```bash
# WORKS — no ANTHROPIC_API_KEY needed:
OPENROUTER_API_KEY=*** gbrain think "question" \
  --model openrouter:inclusionai/ling-2.6-flash
```

**Why the confusion:** The `think` command's model resolution uses a 6-tier chain (CLI flag → config → env → tier default). Without `--model`, it resolves to `anthropic:claude-opus-4-7` (tier default for 'deep') and fails without Anthropic key. The error "no LLM available — set anthropic_api_key" is a **generic AIConfigError fallback** that fires for ANY missing API key regardless of provider. The gateway (`tryBuildGatewayClient`) only checks Anthropic key when provider is 'anthropic'.

**To make think work without Anthropic:**
1. Set `models.default` and `models.think` config keys to your non-Anthropic model
2. OR pass `--model openrouter:provider/model` on every call  
3. Ensure the API key for your provider (e.g., `OPENROUTER_API_KEY`) is in the environment

### Dream cycle LLM phases (propose_takes, grade_takes, consolidate)

**These phases need TWO things to work without Anthropic — source patches AND config keys in the DB.** The dream cycle runner doesn't pass model hints to individual phase implementations, so each phase resolves its model independently.

The source code contained hardcoded `'claude-sonnet-4-6'` defaults in `propose-takes.ts`, `grade-takes.ts`, and `calibration-profile.ts`. On this install these have been patched to `deepseek:deepseek-v4-flash` (the patches survive git pull if they match upstream defaults, but verify after major version jumps).

**Even with source patches, the extractor (called by `propose_takes`) calls `gatewayChat()` WITHOUT a model hint** — it falls through to `getChatModel()` → `reconfigureGatewayWithEngine()` → `resolveModel()`. If `models.default`, `models.chat`, and `models.tier.*` are NOT set in the PGLite DB, `resolveModel` falls to tier defaults (all Anthropic). The `~/.gbrain/config.json` file is NOT read by `resolveModel` — it reads from the DB.

**Complete fix requires BOTH:**
1. Source code patches (hardcoded defaults → your model) — see [`references/dream-cycle-model-patching.md`](./references/dream-cycle-model-patching.md)
2. Config keys set in the PGLite DB (not just `~/.gbrain/config.json`):
   ```bash
   gbrain config set chat_model "deepseek:deepseek-v4-flash"
   gbrain config set models.default "deepseek:deepseek-v4-flash"
   gbrain config set models.chat "deepseek:deepseek-v4-flash"
   gbrain config set models.think "deepseek:deepseek-v4-flash"
   gbrain config set models.tier.utility "deepseek:deepseek-v4-flash"
   gbrain config set models.tier.reasoning "deepseek:deepseek-v4-flash"
   gbrain config set models.tier.deep "deepseek:deepseek-v4-flash"
   gbrain config set models.tier.subagent "deepseek:deepseek-v4-flash"
   # CRITICAL: provider_base_urls MUST be set in the DB when using
   # a custom OpenAI-compatible endpoint like OpenCode Go.
   # Without this, the deepseek recipe routes to DeepSeek's API, not yours.
   # JSON notation required — dot-notation silently fails (v0.41.10.1 confirmed):
   gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}'
   ```
   Then sync the JSON: manually edit `~/.gbrain/config.json` to match.

**Verification that the fix took:** Run `gbrain dream --dry-run --phase propose_takes` and check that `BUDGET_METER_NO_PRICING` shows the correct model (not `ANTHROPIC_PRICING`). If you see "Anthropic chat requires ANTHROPIC_API_KEY" in the extractor warnings, the config keys are missing from the DB.

### What works without Anthropic key

| Feature | Works? | Details |
|---------|--------|---------|
| `gbrain search` / `query` | ✅ | Uses configured embedding model |
| `gbrain doctor` / `stats` / `config` | ✅ | Database operations only |
| `gbrain import` / `embed` | ✅ | Chunking + embedding, no chat model |
| `gbrain think --model openrouter:...` | ✅ | Routes through gateway → needs provider API key |
| `gbrain think` via custom OpenAI-compatible endpoint (`provider_base_urls`) | ✅ | Set `models.think` + `chat_model` to your `recipe:model`, ensure API key env var is set |
| `gbrain think` (no --model, no config in DB) | ❌ | Resolves to Anthropic tier default — even with correct `~/.gbrain/config.json` |
| `gbrain dream` (mechanical phases) | ✅ | lint, backlinks, embed work fine |
| `gbrain dream` (LLM phases — propose_takes, grade_takes) | ✅ (with source patches + config keys set in DB) | Needs BOTH: hardcoded defaults patched AND `models.default` etc. set in PGLite DB (see dream-cycle-model-patching.md) |
| Subagent features (dream phase propose_takes, gbrain agent run, gbrain autopilot) | ✅ When `agent.use_gateway_loop` is enabled | Set via `gbrain config set agent.use_gateway_loop true --force`. See `references/dream-cycle-model-patching.md` for full setup. |

**When to recommend install vs hold off:**
- **Has Anthropic key** → Full value. Install, set up dream cycles, the brain compounds overnight.
- **No Anthropic key, has large reference collection** → Still worth it for search + `gbrain think --model openrouter:...`. LLM synthesis works with OpenRouter via `--model` flag. Brain stays flat (dream cycle enrichment won't work without patching), but semantic search + ad-hoc synthesis is better than grep.
- **No Anthropic key, small reference collection** → Probably not worth the setup overhead. grep + search_files covers you.

## Prerequisites

- **Bun** (v1.0+) — installed at `~/.bun/bin/bun` or system-wide
- **One API key for embeddings** — see provider table below
- PGLite (zero-config, default) — no server needed; Postgres/Supabase optional for scale

## Installation

### DO NOT use `bun install -g`

**The Bun global install is broken.** Bun blocks the top-level postinstall hook on global installs, so schema migrations never run and the CLI aborts with `Aborted()` when it opens PGLite. Tracking issue: [#218](https://github.com/garrytan/gbrain/issues/218).

### Correct install path (git clone + bun link)

```bash
git clone https://github.com/garrytan/gbrain.git ~/gbrain && cd ~/gbrain

# Ensure bun is in PATH
export PATH="$HOME/.bun/bin:$PATH"

bun install && bun link

# Verify — if gbrain: command not found, fix the symlink
export PATH="$HOME/.bun/bin:$PATH"
gbrain --version || ln -sf "$PWD/src/cli.ts" "$HOME/.bun/bin/gbrain"
gbrain --version   # Should print e.g. 0.41.10.1
```

**⚠️ bun link does not always create the CLI symlink.** Unlike `bun install -g`, `bun link` only registers the package name for `bun link gbrain` in other projects. It does NOT reliably create `~/.bun/bin/gbrain`. The `ln -sf` fallback covers the case where the global install directory was cleaned or the symlink was broken. Always verify with `gbrain --version` after install.

### Alternative: if bun install -g was used

Run recovery:
```bash
gbrain apply-migrations --yes
```

If that fails, fall back to the git clone path.

## API Key Setup

G-Brain auto-detects embedding providers from environment variables on `gbrain init`. Source the key into the environment before running `gbrain init` — the CLI reads from env vars, not from `~/.gbrain/config.json`.

### Embedding Provider Options (sorted by cost)

| Provider | Env Var | Default Dims | Cost/1M tokens | Notes |
|----------|---------|-------------|----------------|-------|
| **NVIDIA Nemotron (via OpenRouter)** | `OPENROUTER_API_KEY` | 1024 (supports 512/768/1024/1536) | **$0 (FREE)** | Best for OpenRouter users with credit issues; 131K context, multimodal |
| `openrouter` (OpenAI/text-embedding-3-small) | `OPENROUTER_API_KEY` | 1536 | $0.02 | Default OR embedding; may hit "Insufficient credits" on some OR accounts |
| `google` | `GOOGLE_GENERATIVE_AI_API_KEY` | 768 | $0.025 | Gemini embeddings; also works via OpenRouter as `openrouter:google/gemini-embedding-2-preview` |
| `zeroentropyai` | `ZEROENTROPY_API_KEY` | 2560 (Matryoshka to 1280/640/320/...) | $0.05 | Fast + cheap; also serves as reranker |
| `openai` | `OPENAI_API_KEY` | 1536 | $0.13 | Most battle-tested for vector search |
| `voyage` | `VOYAGE_API_KEY` | 1024 | $0.18 | Best quality per dollar; code-tuned variant available |
| `ollama` | (none — local) | 768 | $0 | Local only, requires Ollama daemon running |
| `llama-server` | (none — local) | user-set | $0 | Local only, requires llama-server daemon |

**Important:** OpenRouter may return "Insufficient credits" for many embedding models (`openai/text-embedding-3-small`, `bge-m3`, `qwen/qwen3-embedding-8b`) even when the account has credit balance. This is an OpenRouter routing/provider-availability issue, not an actual balance problem. The **NVIDIA Nemotron** model (`nvidia/llama-nemotron-embed-vl-1b-v2`) consistently works on OR and is **free**.

### Using OpenRouter (recommended with Hermes if OpenRouter key exists)

```bash
export OPENROUTER_API_KEY=*** Verify the key works
gbrain providers test --model openrouter:openai/text-embedding-3-small
```

### Using BWS (Bitwarden Secrets Manager)

If keys are managed via BWS and the Hermes `.env` is populated at startup, source it:
```bash
set -a; source /root/.hermes/.env 2>/dev/null; set +a
```

## Search Mode Decision (CRITICAL — Ask the User)

**Before running `gbrain init`, you MUST present the cost matrix and confirm the user's choice.** The cost spread between corners is 25×. Silent acceptance is the wrong default.

Per-query cost at 10K queries/month (typical single-user volume):

| Mode | Budget | Haiku-tier | Sonnet-tier | Opus-tier | Characteristics |
|------|--------|-----------|-------------|-----------|-----------------|
| conservative | 4K, 10 chunks | ~$40/mo | ~$120/mo | ~$200/mo | No LLM expansion. Best for cost-sensitive, high-volume loops |
| balanced | 12K, 25 chunks | ~$100/mo | ~$300/mo | ~$500/mo | No expansion. Sonnet-tier sweet spot |
| tokenmax | No budget, 50 chunks | ~$200/mo | ~$600/mo | ~$1,000/mo | LLM expansion ON. Best for frontier models |

Scales linearly: ×10 for 100K/mo, ÷10 for 1K/mo.

Set after user picks:
```bash
gbrain config set search.mode <mode>
```

For a 20-chunk limit matching pre-v0.32.x shape:
```bash
gbrain config set search.searchLimit 20
```

Verify: `gbrain search modes`

## Provider Health Testing

Before initializing, test that your chosen **embedding** model works:

```bash
# Test a specific model (before init — doesn't need a brain)
gbrain providers test --model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2

# Test with chat completion model
gbrain providers test --model openrouter:meta-llama/llama-3.1-8b-instruct

# List all available providers
gbrain providers list
```

**Note:** `gbrain providers test` validates the FULL pipeline including the configured embedding provider. Before `gbrain init` (no brain exists), it can test embedding models but chat model tests may fail because no embedding provider is configured yet. To verify a custom chat endpoint before init, use direct curl instead:

```bash
curl -s https://your-endpoint/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"your-model","messages":[{"role":"user","content":"ping"}],"max_tokens":10}'
```

## Brain Initialization

After search mode is confirmed:

```bash
# For a brain with API key set — auto-detects provider
gbrain init --pglite          # Default PGLite, zero-config, no server needed

# Use a specific embedding model with explicit dimensions
OPENROUTER_API_KEY=*** gbrain init --pglite \
  --embedding-model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 \
  --embedding-dimensions 1024

# To skip embedding (keyword-only search)
gbrain init --pglite --no-embedding
```

To use a non-default provider, pass `--model`:
```bash
gbrain init --pglite --model openrouter
```

To use a non-default chat model after init:
```bash
# Reasonable cheap model for synthesis
gbrain config set chat_model openrouter:meta-llama/llama-3.1-8b-instruct

# Absolute cheapest ($0.01/M input)
gbrain config set chat_model openrouter:inclusionai/ling-2.6-flash
```

Verify:
```bash
gbrain doctor --json    # Full health check
```

`gbrain init` creates `~/.gbrain/config.json` with the resolved provider + dimensions.

## Custom OpenAI-Compatible Endpoints

gbrain supports arbitrary OpenAI-compatible chat endpoints beyond its built-in provider recipes. This lets you use services like **OpenCode Go**, **Together AI**, **DeepSeek API**, or any local/commercial endpoint that speaks the OpenAI chat completions protocol.

### How it works

The `provider_base_urls` config key (`Record<string, string>` keyed by recipe id) overrides the base URL for any registered recipe. The **`deepseek`** recipe is the best base for custom endpoints — it's already `openai-compatible` tier with `implementation: 'openai-compatible'` and requires only `DEEPSEEK_API_KEY` as auth:

```bash
# Override the deepseek recipe's base URL to your custom endpoint
# IMPORTANT: use JSON notation — dot notation (provider_base_urls.deepseek)
# is silently accepted but does NOT persist (v0.41.10.1 confirmed).
gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}'

# Set API key (sent as Authorization: Bearer to the custom endpoint)
export DEEPSEEK_API_KEY=your-opencode-go-key

# Configure the chat model using deepseek recipe + your provider's model ID
gbrain config set chat_model deepseek:deepseek-v4-flash
```

The model ID (`deepseek-v4-flash` above) is passed verbatim in the chat completions request body — use whatever model name your provider expects on the wire.

### Split-provider configuration (most useful pattern)

Use different providers for embeddings vs chat — this is the common setup when you want free/stick embeddings with a specific chat provider:

| Layer | Provider | Why |
|-------|----------|-----|
| **Embeddings** | OpenRouter → NVIDIA Nemotron | **Free** ($0), reliable, 1024-dim |
| **Chat/think** | Custom endpoint (OpenCode Go, Together, DeepSeek API) | Your subscription, specific model |

```bash
# Step 1: Init with free NVIDIA Nemotron for embeddings
export OPENROUTER_API_KEY=sk-or-...
gbrain init --pglite \
  --embedding-model openrouter:nvidia/llama-nemotron-embed-vl-1b-v2 \
  --embedding-dimensions 1024

# Step 2: Configure your custom chat endpoint (JSON notation only — see How it works above)
export DEEPSEEK_API_KEY=your-custom-endpoint-key
gbrain config set provider_base_urls '{"deepseek":"https://opencode.ai/zen/go/v1"}'
gbrain config set chat_model deepseek:deepseek-v4-flash

# Step 3: Set config keys so think routes through the custom endpoint
gbrain config set models.default deepseek:deepseek-v4-flash
gbrain config set models.think deepseek:deepseek-v4-flash
```

### Available recipes suitable for base URL override

| Recipe | `tier` | `implementation` | Best for |
|--------|--------|-----------------|----------|
| `deepseek` | `openai-compat` | `openai-compatible` | Chat completions only (no embeddings). Model: `deepseek-v4-flash`, `deepseek-chat`, etc. |
| `openai` | `native` | `native-openai` | Chat + embeddings. Model: any OpenAI-compatible ID. |
| `groq` | `openai-compat` | `openai-compatible` | Fast inference endpoints. No embedding. |
| `together` | `openai-compat` | `openai-compatible` | Open-model aggregators. Chat only. |

Key distinction: `openai-compatible` recipes use the AI SDK's `createOpenAICompatible()` adapter — more forgiving with non-OpenAPI endpoints. `native-openai` uses `createOpenAI()` which may have stricter request/response expectations.

### Verification

```bash
# Test the chat model through the custom endpoint
gbrain providers test --model deepseek:deepseek-v4-flash

# Verify split config is healthy
gbrain doctor --json | grep -E '(embedding|chat)_model'
```

## Brain Repo Setup

The brain's markdown files live in a SEPARATE git repo, NOT inside `~/gbrain/`:

```bash
mkdir -p ~/brain && cd ~/brain && git init
```

Set up a MECE directory structure inside the brain repo. Read the recommended schema for guidance:
```bash
# Read the schema guide (in the gbrain repo)
cat ~/gbrain/docs/GBRAIN_RECOMMENDED_SCHEMA.md
```

Typical structure:
```
~/brain/
├── people/
├── companies/
├── concepts/
├── projects/
├── notes/
└── daily/
```

## Importing Knowledge

### Standard Import

```bash
# Import markdown files from the brain repo
gbrain import ~/brain/

# Generate vector embeddings (if --no-embed was used)
gbrain embed --stale

# Test a query
gbrain query "key themes across these documents?"
```

### Importing Extracted Reference Materials (.txt → .md)

When working with extracted textbook chapters, regulations, or other reference content that exists as `.txt` files:

1. **Create a clean copy as `.md` files** — skip `.hms-bak` backups:
   ```bash
   DEST=~/brain/extracted
   mkdir -p $DEST/<category>
   for src in /path/to/*.txt; do
     [[ "$src" == *.hms-bak ]] && continue
     base=$(basename "$src" .txt)
     cp "$src" "$DEST/<category>/$base.md"
   done
   ```

2. **Import with sufficient timeout** — large collections (100+ files, 50MB+) may exceed the default 180s. Use `gbrain import` with a longer timeout or run in multiple passes. GBrain skips already-imported files on re-run.

3. **Large file warnings are informational** — files >50KB trigger content-sanity warnings but still import. Very large files (>1MB) may be soft-blocked from embedding (page lands, embedding skipped) — the full text is searchable via FTS5 but won't appear in vector search results. Split oversized files if vector search coverage is needed. For a complete guide to interpreting content-sanity audit logs (warn vs soft_block vs hard, deduping duplicate events), see [`references/content-sanity-audit.md`](./references/content-sanity-audit.md).

4. **Verify import counts:**
   ```bash
   gbrain stats
   # Pages: N  Chunks: N  Embedded: N
   ```

### Knowledge Graph Setup

Backfill typed-link graph and timeline for existing brains:

```bash
gbrain extract links --source db --dry-run | head -20   # preview
gbrain extract links --source db                          # commit
gbrain extract timeline --source db                       # dated events
gbrain stats                                              # verify links > 0
```

For large brains (>10K pages), use `--since YYYY-MM-DD` for incremental extraction. The process is idempotent.

## Verification

```bash
gbrain doctor --json    # Full health check
gbrain models           # Which AI models are configured for what
gbrain models doctor    # 1-token probe per configured model
gbrain search "test query"  # Quick smoke test
```

## Recommended Skills / Skillpacks

After install, GBrain offers bundled skillpacks for MCP conversation workflows. Always show the list to the user and ask before installing:

```bash
gbrain skillpack list                # see all options
gbrain skillpack install --all       # install all (after user confirms)
gbrain skillpack install <name>      # install one
```

## Dream Cycle (`gbrain dream`)

**What it is:** gbrain's autonomous overnight maintenance — entity sweep, page enrichment, citation fixing, and stale embedding. Runs while you sleep; you wake up to a smarter brain.

### What Each Phase Does

| Phase | What happens | LLM call? |
|-------|-------------|-----------|
| **Entity sweep** | Scans recent conversations/interactions, detects entities (people, companies, concepts), creates or enriches brain pages for each | Yes — configured chat model |
| **Citation fix** | Pages with missing source attributions or broken URLs get repaired | No — filesystem check |
| **Consolidate** | Identifies patterns across conversations, promotes ephemeral signals to durable knowledge | Yes — configured chat model |
| **Embed stale** | Re-embeds pages whose content changed since last embed | No — embedding model only |

### Model Requirements — Split Between Think and Dream Cycle

**The `gbrain think` command and the dream cycle's LLM phases use different model resolution paths:**

- **`gbrain think`** resolves through `resolveModel` (6-tier chain, CLI flag supported) and routes through the gateway — works with any provider that has a recipe and API key. Set `models.think` config or pass `--model` to use non-Anthropic providers.
- **Dream cycle LLM phases** (`propose_takes`, `grade_takes`) have hardcoded Anthropic defaults in their source code. See `references/dream-cycle-model-patching.md` for the fix.

| Phase | LLM call? | Works without Anthropic? | How |
|-------|--------|-------------------------|-----|
| lint, backlinks, embed | No | ✅ Yes | Filesystem + embedding operations |
| extract (FS links/timelines) | No | ✅ Yes | Regex-based, no LLM |
| extract_facts | Yes | ✅ Yes (with config keys in DB, not JSON) | Uses `getChatModel()` → requires `models.default` in PGLite DB |
| propose_takes | Yes — LLM proposes claims | ✅ Yes (with source patches + config keys in DB) | Budget meter patched to non-Anthropic model; extractor needs `models.default` in DB to avoid Anthropic tier defaults |
| grade_takes | Yes — LLM grades takes | ✅ Yes (with source patches + config keys) | Hardcoded default patched to non-Anthropic model |
| consolidate | Yes — LLM promotes facts | ✅ Yes (via config keys) | Uses `resolveModel` → respects `models.default` in DB |
| patterns | Yes — cross-session pattern detection | ⚠️ Configurable | Uses `models.dream.patterns` key — set it in config |
| synthesize_concepts | Yes — cross-doc concept synthesis | ❌ No | Hardcoded Anthropic subagent dispatch |

### Setting Up

**For Hermes, as a no_agent bash script cron (graceful degradation pattern):**

Create the script at `~/.hermes/scripts/gbrain-dream-cycle.sh`:

> **Key insight:** The gateway auto-restarts `gbrain serve` within seconds of being killed. Don't fight this — let the dream degrade gracefully. Filesystem-only phases (lint, backlinks, extract) run even when PGLite is locked. DB phases (sync, embed, propose_takes) are handled by the MCP server during normal operation.

```bash
#!/bin/bash
# gbrain-dream-cycle.sh — Nightly G-Brain maintenance (graceful degradation)
set -uo pipefail

export HOME="/root"
source /root/.hermes/.env 2>/dev/null
export PATH="/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"

MARKER_FILE="/root/.gbrain/.dream-last-run"
cd /root/gbrain

# Attempt to kill MCP — gateway may respawn it before dream starts
pkill -9 -f "gbrain serve" 2>/dev/null || true
rm -f /root/.gbrain/brain.pglite/postmaster.pid 2>/dev/null

# Run dream — degrades gracefully if PGLite is locked
# Filesystem phases (lint, backlinks, extract) always run
# DB phases (sync, embed, propose_takes) skip when locked
DREAM_OK=0
timeout 180 gbrain dream --dir /root/brain 2>&1 || DREAM_OK=$?

date -u +%s > "$MARKER_FILE"
if [ "$DREAM_OK" -eq 0 ]; then
    echo "DREAM CYCLE: completed successfully"
else
    echo "DREAM CYCLE: completed with code $DREAM_OK"
fi
echo "=== DREAM CYCLE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
```

Then create the cron:
```bash
# name: "gbrain-dream-cycle"
# schedule: "0 2 * * *"
# no_agent: true
# script: gbrain-dream-cycle.sh
# deliver: local
```

**Critical:**
- **Graceful degradation is the correct pattern for cron.** The gateway auto-restarts `gbrain serve` within seconds — don't fight it. `gbrain dream` runs filesystem-only phases (lint, backlinks, extract) when PGLite is locked. DB phases (sync, embed, propose_takes) are handled by the MCP server during normal operation. See `references/pglite-lock-contention-gateway.md`.
- `set -a; source .env; set +a` is REQUIRED in cron scripts. Without it, env vars are set in the script shell but NOT exported to gbrain child processes.
- If gbrain dream is OOM-killed, it leaves a stale row in gbrain_cycle_locks. Fix: DELETE FROM gbrain_cycle_locks WHERE id='gbrain-cycle' via direct PGLite query (included in the script).
- The dream cycle's --json output includes all 20+ phases in one efficient process. Do NOT run separate gbrain sync, gbrain embed --stale, or gbrain extract before gbrain dream -- the dream cycle handles all of them internally.
- On low-RAM machines (<=2GB): increase cron.script_timeout_seconds to at least 600s (set in config.yaml), kill all MCP servers before running, and maintain at least 4GB swap.

**Or as a Hermes-agent prompt-based cron (more flexible — lets the agent reason about what to enrich):**
```bash
# Using Hermes cronjob tool:
# prompt: "Run gbrain dream cycle: search today's sessions for entities mentioned. For each person, company, or concept: check if a brain page exists (gbrain search), create or update it if thin. Fix any broken citations. Then gbrain embed --stale."
# schedule: "0 2 * * *"
# skills: [gbrain]
# name: "nightly-dream-cycle"
```

**Or using raw cron:**
```bash
# crontab entry
0 2 * * * cd ~/gbrain && source ~/.hermes/.env && gbrain dream --dir ~/brain/ --json >> /var/log/gbrain-dream.log 2>&1
```

### Memory Optimization for Low-RAM Machines

The dream cycle uses PGLite WASM inside a Bun process, which can consume **1.2GB+ RSS** on a full brain. On machines with ≤2GB RAM, this frequently causes OOM kills during `backlinks.scan` or `embed` phases.

**Techniques ranked by impact:**

| Technique | Memory saved | Effort | Notes |
|-----------|-------------|--------|-------|
| Kill ALL MCP servers before dream | ~120MB | Low | Kill tradingview-mcp, wundertrading, etc. alongside gbrain serve. Hermes auto-restarts them. |
| Run phases individually | Reduces peak per phase | Low | Replace `gbrain dream --json` with sequential `--phase` calls (bun exits between phases) |
| Increase swap to 4GB | OOM buffer | Low | `fallocate -l 3G /swapfile && mkswap /swapfile && swapon /swapfile` |
| Eliminate redundant steps | Fewer bun invocations | Low | Drop pre-dream sync/embed/extract — `gbrain dream` does them internally |
| Add `sleep 3` after killing MCP server | Ensures memory reclaimed | Trivial | Lets the kernel fully reclaim PGLite pages before starting CLI |
| Skip backlinks phase | Avoids peak phase | Medium | OOM hit here most often; skip via selective `--phase` calls |
| Use remote Postgres backend | ~800MB freed | High | Postgres (Neon/Supabase/local) eliminates WASM memory entirely |

**Recommended pattern for ≤2GB RAM:**

```bash
# Step 1: Kill ALL MCP servers to free maximum memory
pkill -f "gbrain serve" 2>/dev/null; pkill -f "tradingview-mcp" 2>/dev/null; pkill -f "wundertrading" 2>/dev/null
sleep 3
rm -f /root/.gbrain/brain.pglite/postmaster.pid

# Step 2: Run phases individually (each exits before next starts)
gbrain dream --phase lint 2>&1
gbrain dream --phase backlinks 2>&1
gbrain sync --repo ~/brain/ 2>&1          # sync has no --phase flag
gbrain dream --phase embed --stale 2>&1
gbrain dream --phase orphans 2>&1

# Step 3: Restart MCP servers (Hermes handles this automatically)
```

See `references/dream-cycle-memory-optimization.md` for the full analysis including OOM dmesg patterns, swap sizing, and phase-level memory profiling.

### Cost Considerations

At `$0.01/M` input (Ling 2.6 Flash), a dream cycle processing ~50 entities costs ~$0.05-0.15/night depending on page size. At `$0.15/M` (Claude Sonnet 4), the same cycle costs ~$0.75-2.25/night. Pick the chat model based on your tolerance for overnight spend vs. enrichment quality.

### Verification

```bash
# Run dry-run first to see what would happen
gbrain dream --dry-run

# Full cycle, JSON report
gbrain dream --json

# Single phase (for testing)
gbrain dream --phase lint

# Check brain health after
gbrain doctor --json
```

### Pitfalls

- **Dream cycle LLM phases can work without Anthropic, but need TWO things.** The old claim "LLM phases ARE Anthropic-gated despite docs claims" is outdated — with source patches AND config keys in the DB, `propose_takes`, `grade_takes`, `calibration_profile`, and `extract_facts` all route through non-Anthropic providers. The one truly Anthropic-gated path is `subagent dispatch` (used by `synthesize` and `autopilot`) which hard-enforces via `isAnthropicProvider()`. See [`references/dream-cycle-model-patching.md`](./references/dream-cycle-model-patching.md) for the complete fix.
- **Cost depends on chat model, not dream itself.** A user who turns on dream cycles with GPT-5.2 via OpenRouter will pay ~5-10× more per cycle than with Ling 2.6 Flash. Always surface the cost implication.
- **Dream is NOT optional for knowledge compounding.** Without it, imported documents sit as flat chunks — the graph never builds itself, entities never get enriched, and gaps never get flagged. The brain stays at "dump of files" level.
- **MCP server holds exclusive PGLite lock — gateway auto-restart creates race condition.** The gbrain MCP server (`gbrain serve`) keeps a persistent PGLite connection. The Hermes gateway auto-restarts it within ~2-5s of being killed. This means the "kill MCP → run CLI" pattern is unreliable — by the time the CLI starts, the gateway has already respawned serve. **Dream cycle gracefully degrades:** `gbrain dream` runs filesystem-only phases (lint, backlinks, extract) when PGLite is locked, skipping DB-dependent phases (sync, embed, propose_takes). It exits 0 in degraded mode. For cron jobs, accept degraded mode — the filesystem phases still provide value. For full dream, stop the gateway first (`pkill -f "hermes.*gateway"`) or run from an interactive session. See [`references/pglite-lock-contention-gateway.md`](./references/pglite-lock-contention-gateway.md) for the full analysis.
- **OOM-killed dream processes leave stale cycle lock.** If `gbrain dream` is killed by OOM or timeout, it leaves a row in `gbrain_cycle_locks` with `id='gbrain-cycle'`. Subsequent dream runs fail with "cycle_already_running" even after a fresh start. **Quick fix:** `rm -f /root/.gbrain/cycle.lock` (removes the filesystem-level marker). **Full fix:** `DELETE FROM gbrain_cycle_locks WHERE id='gbrain-cycle'` via direct PGLite query (use `bun -e` with `PGlite.create({dataDir})`). The dream cycle script should include this cleanup step.
- **120s default timeout for no_agent cron scripts (configurable).** Hermes no_agent cron jobs default to 120s. The dream cycle's mechanical phases (lint, backlinks, sync, embed, extract, consolidate) complete in ~62s, but LLM-based phases (propose_takes, grade_takes) take longer and get SIGTERM'd. Increase via `cron.script_timeout_seconds` in `~/.hermes/config.yaml` or the `HERMES_CRON_SCRIPT_TIMEOUT` env var (see [cron internals docs](https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals#skill--script-backing)). This install uses **900s** for the dream cycle. Acceptable for nightly maintenance — the critical mechanical phases run. Use a completion marker file (~/.gbrain/.dream-last-run) and have the nightly audit check its freshness.
- **Measured dream cycle runtime on constrained VPS:** On a 2GB VPS with ~327 pages, the full dream cycle (all phases including embed) takes **~7-9 minutes** (~420-540s). The embed phase alone takes ~17s for 1407 chunks (May 29 data: 32s total for 155 pages). Page count growth scales the embed phase roughly linearly. The 900s cron timeout provides ~1.7× headroom over worst-case measured time. If the cycle exceeds 900s, the likely culprit is the embed phase on a large page set — consider `--phase embed` separately or switching to a remote Postgres backend.
- **`set -a` is required before source .env in cron scripts.** Cron jobs run in a sanitized environment. `source /root/.hermes/.env` sets variables in the script's shell but does NOT export them to child processes unless `set -a` is active first. Without it, `gbrain` subprocesses can't find OPENROUTER_API_KEY or other env vars. Always use: `set -a; source .env; set +a`.

## MCP Server Wiring (Hermes Agent)

GBrain ships with a built-in MCP server (`gbrain serve`) that exposes ~30 tools (search, think, embed, import, doctor, etc.) via stdio transport. Wiring it into Hermes makes these tools available alongside built-in tools like `web_search` and `session_search`.

### Configuration

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  gbrain:
    command: "/root/.bun/bin/gbrain"
    args: ["serve"]
    env:
      PATH: "/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
      HOME: "/root"
    timeout: 180
```

### CLI Env Wrapper Pattern (Interactive Sessions)

When running `gbrain think`, `gbrain dream`, or any command that needs API keys from a Hermes interactive session, the keys must be in the shell environment. The Hermes `.env` file isn't auto-sourced for subprocesses.

Create a wrapper that sources Hermes env before every gbrain invocation:

**`/usr/local/bin/gbrain-env`:**
```bash
#!/bin/bash
# Source Hermes env vars (API keys) then run gbrain
while IFS='=' read -r key val; do
  [[ "$key" =~ ^[A-Z_] ]] && export "$key=$val"
done < <(grep -v '^#' /root/.hermes/.env | grep -v '^$')
exec /usr/local/bin/gbrain "$@"
```

```bash
chmod +x /usr/local/bin/gbrain-env
alias gbrain="gbrain-env"  # add to ~/.bashrc for persistence
```

**Why this matters:** `gbrain think --model deepseek:deepseek-v4-flash` still needs `DEEPSEEK_API_KEY` (or whichever key the recipe's `auth_env` declares) in the environment. Without it, the gateway catches `AIConfigError` and degrades to `"(no LLM available — set anthropic_api_key via gbrain config or ANTHROPIC_API_KEY env)"`. This message is misleading — it's a generic fallback, not actually about Anthropic. 100% of the time, the real cause is the provider's API key missing from env, regardless of what model you pass with `--model`.

**Verification:** `gbrain-env think "test" --model deepseek:deepseek-v4-flash` returns a real answer, not the degraded stub.

### MCP Server Wrapper Pattern

The **Hermes native MCP client filters environment variables** — it only passes safe baseline vars (`PATH`, `HOME`, `USER`, etc.) plus anything you explicitly add in the `env:` block. If gbrain needs API keys at runtime (e.g., `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`), they must be explicitly listed there.

Since API keys are sensitive and shouldn't be hardcoded in config.yaml, use the same source-pattern as a **wrapper script**:

**`~/.hermes/scripts/gbrain-mcp-wrapper.sh`:**
```bash
#!/bin/bash
# Wrapper for gbrain MCP server — sources environment before starting
set -a
source /root/.hermes/.env 2>/dev/null
set +a
exec /root/.bun/bin/gbrain serve
```

Then point the config at the wrapper:

```yaml
mcp_servers:
  gbrain:
    command: "/root/.hermes/scripts/gbrain-mcp-wrapper.sh"
    args: []
    env:
      PATH: "/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
      HOME: "/root"
    timeout: 180
```

### Tools Exposed

| Hermes tool name | What it does | Requires API key? |
|-----------------|-------------|-------------------|
| `mcp_gbrain_search` | Semantic vector search across brain pages | No (uses configured embedding model) |
| `mcp_gbrain_think` | Multi-hop synthesis + gap analysis | Yes — the provider's API key for whichever model the server's config resolves to. With a proper env wrapper, OpenRouter/DeepSeek keys work (not just Anthropic). |
| `mcp_gbrain_doctor` | Health check | No |
| `mcp_gbrain_import` | Import markdown files | No |
| `mcp_gbrain_embed` | Embed stale content | No |
| `mcp_gbrain_stats` | Brain statistics | No |

### Verification

After restarting Hermes, test the connection:
```bash
# Check gbrain serve starts
echo "test" | timeout 5 /root/.bun/bin/gbrain serve 2>&1
# Should show: "Starting GBrain MCP server (stdio)..." + "graceful exit"

# From inside a Hermes session, search should work:
# User: "query gbrain for Ames test"
# Agent: calls mcp_gbrain_search internally
```

### Pitfalls

- **gbrain think MCP tool model resolution:** The `mcp_gbrain_think` tool exposed via MCP calls `gbrain think` which resolves through the 6-tier model chain. Without explicit `--model` (which MCP can't pass dynamically), it lands on the tier default (`anthropic:claude-opus-4-7`) and needs `ANTHROPIC_API_KEY`. Set `models.think` and `models.default` config keys to a non-Anthropic model to make it work without an Anthropic key.
- **Per-turn MCP context bloat:** When gbrain MCP tools are always-loaded, their tool definitions consume ~25K tokens in the system prompt every turn. Teknium (@Teknium) flagged this as the #1 gbrain performance issue. See [`references/teknium-mcp-performance-tweet.md`](./references/teknium-mcp-performance-tweet.md) for details and the Tier A/B/C routing fix.
- **Wrapper script must be executable** (`chmod +x`). If it isn't, the MCP server won't start.
- **Restart required:** Adding/removing MCP servers in config.yaml requires restarting the Hermes gateway. No hot-reload.
- **Timeout:** Complex think/synthesis queries may exceed the default 180s timeout. Increase `timeout` in the config if needed.

When installed, add to `~/.hermes/community-manifest.json`:

```json
{
  "name": "gbrain",
  "type": "external_tool",
  "source": "https://github.com/garrytan/gbrain",
  "install_date": "<YYYY-MM-DD>",
  "version": "<from 'gbrain --version'>",
  "install_method": "git clone → bun install → bun link",
  "update_command": "cd ~/gbrain && git pull && bun install && bun link",
  "post_update": "gbrain apply-migrations --yes --non-interactive (if needed)",
  "status": "active"
}
```

## Related

| `devops/gbrain/references/gbrain-config-regression-detection.md` — detection & recovery protocol for the config-split regression: how to spot when DB and JSON diverge, the exact set of keys that must be in the DB, and verification steps after fixing
| `devops/gbrain/references/embedding-dimension-mismatch-recovery.md` — step-by-step recovery sequence when embedding model returns different dimensions than the DB schema expects: config change → kill MCP → remove stale PGLite locks → restart → re-embed
| `devops/gbrain/references/source-isolation-pattern.md` — using isolated sources (federated: false) to keep multiple projects in the same G-Brain without cross-contamination
- `devops/gbrain/references/teknium-mcp-performance-tweet.md` — Teknium's real-world analysis of gbrain MCP context bloat and Tier A/B/C skill routing fix
- `devops/hermes-maintenance` — community manifest governance, long-term Hermes care
- `devops/gbrain/references/session-install-transcript.md` — detailed session-specific install transcript with error resolution
- `devops/gbrain/references/openrouter-embedding-models.md` — OpenRouter embedding model quirks, dimension passthrough bug fix, and working model list
- `devops/gbrain/references/openrouter-embedding-quirks.md` — combined reference including the BWS token issue, final config, and chat model defaults (merged from archived gbrain-install skill)
- `devops/gbrain/references/config-mcp-cron-setup.md` — session transcript: config split fix, MCP wiring, dream cycle cron setup
- `devops/remote-agent-infrastructure` — Tailscale mesh, git as memory layer, scripting discipline (complementary infra)
- `devops/gbrain/references/opencode-go-config.md` — using OpenCode Go as a custom OpenAI-compatible chat provider for gbrain, with split-provider config pattern
- `devops/gbrain/references/dream-cycle-model-patching.md` — code-level patch analysis: which lines to change in propose-takes.ts and grade-takes.ts to make dream cycle LLM phases work with OpenRouter/OpenAI
- `devops/gbrain/references/pglite-database-recovery.md` — data directory corruption diagnostic flow: how to distinguish lock/stale-PID from corruption, test fresh vs existing, and recovery options
- `devops/gbrain/references/pglite-backup-restoration.md` — step-by-step backup restoration sequence after PGLite WASM corruption: swap to backup, re-import DABT references, re-run dream cycle, restart MCP server
| `devops/gbrain/references/pglite-lock-contention-gateway.md` — PGLite lock contention with gateway auto-restart: why "kill MCP → run CLI" is unreliable, graceful degradation pattern, cron script design
| `devops/gbrain/references/dream-cycle-memory-optimization.md` — OOM analysis, phase-by-phase execution, swap sizing, and low-RAM operation recipes for ≤2GB machines

## Pitfalls

- **Bun global install bug (#218):** Do NOT use `bun install -g github:garrytan/gbrain`. Always clone + bun link.
- **CLI binary symlink breakage:** `~/.bun/bin/gbrain` is a symlink to `../install/global/node_modules/gbrain/src/cli.ts`. If the bun global install directory is cleaned or corrupted, the symlink becomes a dead link and `gbrain: command not found` results despite the package being installed. Fix: `rm ~/.bun/bin/gbrain && ln -sf ~/gbrain/src/cli.ts ~/.bun/bin/gbrain` (point to the cloned repo's entry point, not the global install path). Verify with `gbrain --version`.
- **`#!/usr/bin/env bun` shebang fails in non-interactive shells (cron, scripts, tool output):** The gbrain CLI entry point uses `#!/usr/bin/env bun`. The `env` lookup requires `bun` to be in the system PATH. `.bashrc` adds `~/.bun/bin` to PATH, but cron jobs, non-interactive shells, and tool subprocesses don't source `.bashrc`. Symptoms: `gbrain: command not found` (exit 127) in cron output, or `/usr/bin/env: 'bun': No such file or directory` when running gbrain from a script. **Fix:** Create a system-level symlink so `env bun` works from any context: `ln -sf ~/.bun/bin/bun /usr/local/bin/bun`. Verify: `gbrain --version` from a bare shell (no `.bashrc` sourcing). This is the durable fix — it survives `.bashrc` changes, profile resets, and non-login shell invocations.
- **Search mode default:** `gbrain init` auto-applies `tokenmax` unless a Haiku-tier agent or no OpenAI key is detected. Always confirm with the user.
- **Non-TTY init without API key:** Falls immediately. Must set at least one embedding provider env var, pass `--no-embedding`, or run interactively.
- **PGLite cannot ALTER COLUMN vector(N):** Switching embedding models requires `gbrain reinit-pglite` (wipes embeddings, re-indexes). No in-place column type change.
- **Memory-constrained environments:** PGLite runs as WASM inside the Bun process. On <1GB RAM VPS, consider Supabase + pgvector instead. On 1-2GB machines, the dream cycle's bun+PGLite process can use 1.2GB+ RSS and OOM. Mitigations (see `references/dream-cycle-memory-optimization.md`):
  - Kill ALL MCP servers (not just gbrain) before the dream cycle to free ~120MB
  - Run dream phases individually (`--phase lint`, `--phase backlinks`, etc.) so bun exits between phases
  - Increase swap to 4GB+ for OOM headroom
  - Eliminate redundant pre-dream steps (sync/embed/extract are inside `gbrain dream` already)
  - Or switch to a remote Postgres backend (eliminates WASM memory entirely)
- **API key in env vs config:** `gbrain init` reads from env vars but writes the resolved provider/dims to `~/.gbrain/config.json`. Keys themselves are NOT stored in config — they're read from env at runtime.
- **Brain repo ≠ tool repo:** The user's markdown knowledge (`~/brain/`) is a separate git repo from the gbrain tool install (`~/gbrain/`). Do not conflate them.
- **Known bug: dimension passthrough for unknown openai-compatible models (v0.41.10.1):** `dimsProviderOptions()` in `src/core/ai/dims.ts` returns `undefined` for any embedding model in the `openai-compatible` tier that isn't in its switch cases (ZeroEntropy, Voyage, text-embedding-3, DashScope, Zhipu, MiniMax). Models like `nvidia/llama-nemotron-embed-vl-1b-v2` on OpenRouter never receive the `dimensions` parameter, returning native 2048-dim instead of configured dims. **Fix:** Replace `return undefined;` at the end of the `openai-compatible` case with `return { openaiCompatible: { dimensions: dims } };`. Safe because endpoints that don't support `dimensions` silently ignore the field per OpenAI-compat spec.
- **OpenRouter embedding model routing:** Models like `openai/text-embedding-3-small`, `bge-m3`, `qwen/qwen3-embedding-8b` may return "Insufficient credits" on OpenRouter even with valid balance. This is a routing issue, not a key problem. Use `nvidia/llama-nemotron-embed-vl-1b-v2` (free, confirmed working) instead. Embedding health monitoring — see [`references/embedding-health-monitoring.md`](./references/embedding-health-monitoring.md) for the nightly audit watchdog that detects API failures before they silently break search.
- **Chat model selection:** GBrain defaults chat to `openrouter:openai/gpt-5.2`. For a cheap alternative that still handles synthesis well, use `openrouter:meta-llama/llama-3.1-8b-instruct` ($0.02/M input). Cheapest option overall: `inclusionai/ling-2.6-flash` ($0.01/M input). For users with an OpenCode Go subscription, consider `deepseek:deepseek-v4-flash` with `provider_base_urls.deepseek` set to `https://opencode.ai/zen/go/v1`.
- **Large imports may timeout:** Importing 100+ files (50MB+) can exceed the default 180s terminal timeout. Run with `timeout=300` or in multiple passes — GBrain skips already-imported files on re-run.
- **HMS sync after GBrain operations:** If files were created/deleted on the VPS during GBrain setup (like `.hms-bak` debris or extracted reference copies), ensure the same changes are reflected locally before the next `hms push`. HMS uses `--update` (no `--delete`), so files that exist locally but were deleted on VPS get re-uploaded. Run `hms push --dry-run` first to check, then clean up local copies.
- **Config split — gbrain config CLI vs ~/.gbrain/config.json:** There are two config sources that can diverge. `gbrain config set chat_model` writes to the PGLite DB (canonical, read by CLI). `~/.gbrain/config.json` is a fallback file only written during `gbrain init` — it does NOT auto-sync when config changes via CLI. **Critical consequence: `resolveModel()` (the 8-tier model resolution chain) reads from DB config keys only** — it checks `models.default`, `models.chat`, `models.think`, `models.tier.<tier>` in the PGLite DB. Setting these in `~/.gbrain/config.json` alone does NOTHING at runtime. The `subagent_capability` doctor check reads from JSON and will flag the old model. **Fix:** after setting config via CLI, always verify with `gbrain config get <key>` (reads DB, the actual runtime value). To be safe, sync the JSON manually:
  ```bash
  # After any gbrain config set, verify DB has the right value:
  gbrain config get models.default models.chat models.think models.tier.reasoning
  
  # Then sync JSON to match:
  python3 -c "
  import json
  with open('/root/.gbrain/config.json') as f:
      c = json.load(f)
  c['models.default'] = 'deepseek:deepseek-v4-flash'
  with open('/root/.gbrain/config.json', 'w') as f:
      json.dump(c, f, indent=4)
  "
  ```
  **Post-git-pull verification:** After any `git pull` that updates gbrain, check that the model config keys are still in the DB — `git pull` only touches source files, not the DB or JSON, but the config split means the JSON can get out of sync with what the runtime actually uses. Run `gbrain config get models.default` and confirm it returns your non-Anthropic model.
- **Files >500KB are soft-blocked from embedding:** gbrain's content-sanity check has a 500KB hard block threshold. Files exceeding this size (e.g., 1.27MB Casarett ch6 biotransformation, 1.4MB FDA Silverbook) have `event_type: soft_block` — the page lands in the database as metadata but gets ZERO embedding chunks, making it invisible to vector search. Only FTS5 keyword search can find these pages. Fix: split oversized files by `##` heading into individual section files before import, or accept they'll be keyword-searchable only.
- **Content-sanity audit classification:** The doctor check `content_sanity_audit_recent` reports: `warn` = file >50KB (embedded but flagged oversized), `soft_block` = file >500KB (not embedded, metadata only), `hard` = corrupt or unreadable (rare). All 132 events in a fresh DABT brain import were oversized files, not corruption. Always check the raw events in `~/.gbrain/audit/content-sanity-*.jsonl` to understand what's actually happening.
- **Dream cycle model routing requires TWO things — source patches AND config keys in DB.** The source patches (hardcoded `'claude-sonnet-4-6'` → your model in `propose-takes.ts`, `grade-takes.ts`, `calibration-profile.ts`) fix the budget meter and DB insert model IDs. But the **extractor** inside `propose_takes` calls `gatewayChat()` without a model hint, which falls to `getChatModel()` → calls `reconfigureGatewayWithEngine()` → `resolveModel()`. If `models.default` (or `models.chat` / `models.tier.*`) is not set in the PGLite DB, `resolveModel` falls to tier step 7 — all `TIER_DEFAULTS` are Anthropic, hence "Anthropic chat requires ANTHROPIC_API_KEY". The `~/.gbrain/config.json` file is NOT read by `resolveModel`. **Fix:** after setting source patches, also run `gbrain config set models.default <your-model>` and `gbrain config set models.tier.reasoning <your-model>` in the DB (the CLI writes to the DB, not the JSON). Verify with `gbrain config get models.default`. See [`references/dream-cycle-model-patching.md`](./references/dream-cycle-model-patching.md) for the full patch + config guide.
- **`provider_base_urls` requires JSON notation, not dot-notation (v0.41.10.1):** `gbrain config set provider_base_urls.deepseek '...'` returns success but the value never persists — `config get provider_base_urls` returns "Config key not found". Always use JSON: `gbrain config set provider_base_urls '{"deepseek":"..."}'`. Tested and confirmed on v0.41.10.1. This affects all nested object config keys, not just provider_base_urls.
- **`config show` vs `config get` read different sources:** `gbrain config show` reads from `~/.gbrain/config.json` (the init-time file snapshot, may be stale). `gbrain config get <key>` reads from the PGLite DB (the current runtime value). After changing config via `gbrain config set`, use `config get` to verify — `config show` will show the old value until the JSON file is manually updated.
- **`gbrain providers test --model` fails pre-init for chat models:** The `providers test` command validates the FULL provider pipeline including embedding configuration. Before `gbrain init`, it cannot test chat models because no embedding provider is configured. To verify a custom chat endpoint before init, use direct curl against the endpoint instead.
- **`DEEPSEEK_API_KEY` env var naming:** When using the `deepseek` recipe with a custom endpoint (e.g., OpenCode Go), the env var name is `DEEPSEEK_API_KEY` because that's what the deepseek recipe's `auth_env` declares. The actual key is your custom endpoint's key, not DeepSeek's. gbrain just reads the env var and sends `Authorization: Bearer*** This is confusing but harmless.

- **Split-path auth: `deepseek:` recipe + OpenCode base URL breaks `gbrain think` but dream cycle phases still work.** The dream cycle's LLM phases (`propose_takes`, `grade_takes`, `extract_facts`) call `gatewayChat()` directly — when `modelHint` is omitted, the gateway resolves auth using the endpoint's metadata and succeeds against the OpenCode URL with `DEEPSEEK_API_KEY`. But `gbrain think` routes through `tryBuildGatewayClient()` which **always passes an explicit model** to `gatewayChat()`. With the model resolved to `deepseek:` provider, the gateway tries to auth as the DeepSeek recipe against the OpenCode base URL — the auth mechanisms differ (OpenCode expects a different Bearer token format than the deepseek recipe's standard `DEEPSEEK_API_KEY`), and `gatewayChat` throws `AIConfigError`, caught and degraded to `"(no LLM available — set anthropic_api_key...)"`. **Fix: route think through OpenRouter** — `gbrain config set models.think openrouter:deepseek/deepseek-chat` (uses `OPENROUTER_API_KEY`, proper auth). The dream cycle phases continue using the `deepseek:` recipe + OpenCode URL just fine since they don't always pass a model hint. See also `references/pglite-backup-restoration.md` for the full recovery sequence if the DB gets corrupted during this split-config operation.

- **Broken CLI symlink after bun global install cleanup:** `bun link` creates a symlink at `~/.bun/bin/gbrain` → `../install/global/node_modules/gbrain/src/cli.ts`. If the global install directory gets deleted or the Bun global registry is corrupted (missing package.json), the symlink goes dead — `gbrain` returns "No such file or directory" but the binary symlink still shows. The brain data at `~/.gbrain/` (PGLite, config, markdown) is unaffected.

  **Recovery:**
  ```bash
  cd /root && git clone https://github.com/garrytan/gbrain.git
  cd /root/gbrain && bun install
  ln -sf /root/gbrain/src/cli.ts /root/.bun/bin/gbrain
  gbrain --version
  ```

  **Detection:** `file /root/.bun/bin/gbrain` returns "broken symbolic link" — fix with `ln -sf` above. No data loss, the brain at `~/.gbrain/` is separate from the CLI binary.
- **MCP server inherits filtered environment:** The Hermes native MCP client strips most env vars from subprocesses. Only safe baseline vars (`PATH`, `HOME`, `USER`, etc.) plus explicitly configured `env` entries are passed. If gbrain needs API keys (`OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`), they must be explicitly added to the `mcp_servers.gbrain.env` block OR a wrapper script that sources them before spawning the server must be used.
- **PGLite WASM CLI bug (gh#223):** Fresh `gbrain` CLI invocations may fail with "PGLite failed to initialize its WASM runtime" — three possible causes:
  - **MCP server holds exclusive PGLite lock:** Separate CLI commands (sync, embed, extract) hang with "Timed out waiting for PGLite lock" if the gbrain MCP server is running. The dream cycle script must stop the MCP server (`pkill -f "gbrain serve"`) before running CLI commands, then let Hermes auto-restart it.
  - **Dirty data directory:** A stale `postmaster.pid` from a prior crash prevents PGLite from starting. Fix: test fresh dir vs existing dir to isolate the cause, then either remove the stale pid or swap to the clean `brain.pglite.bak` backup.
  - **Data directory corruption** (distinct from lock/stale-pid): Fresh PGLite instances work fine but opening the existing `brain.pglite` data directory crashes with a WASM abort. Indicates corrupted internal Postgres state — not recoverable by removing pid files. See `references/pglite-database-recovery.md` for full diagnostic flow.
  See `references/pglite-wasm-cli-workaround.md` for the standard lock/pid workaround, and `references/pglite-database-recovery.md` for the corruption recovery flow.

- **`gbrain dream` needs `--dir` or `sync.repo_path` config — `database_path` is not enough.** The dream command's `resolveBrainDir()` only checks two sources: (1) an explicit `--dir <path>` argument, or (2) the `sync.repo_path` config key in the PGLite DB. The `database_path` config key is NOT checked. If you restored from a backup or the brain repo path was never configured, `sync.repo_path` may be unset and `gbrain dream` fails with "No brain directory found" even though the DB exists. The `--dir` flag is the quick workaround: `gbrain dream --dir <brain-repo-path>`. To make it permanent: `gbrain config set sync.repo_path /path/to/brain/repo`.
