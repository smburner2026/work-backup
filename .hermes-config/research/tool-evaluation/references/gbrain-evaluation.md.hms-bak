# gbrain Evaluation — Garry Tan's Open-Source Hermes/OpenClaw Fork

**Evaluated:** 2026-05-25
**Source:** https://github.com/garrytan/gbrain
**Hosted:** https://gbrain.io
**Verdict:** CONDITIONAL GO — complementary brain layer under existing Hermes stack

## What It Is

gbrain is an open-source "brain layer" for AI agents — Garry Tan's opinionated fork of the OpenClaw/Hermes architecture. It ships three capabilities in one box:

1. **`gbrain think`** — Synthesis retrieval that returns an *answer* (not a list of pages) with explicit citations and **gap analysis** ("Heads up: nothing's been added about Alice since April 22"). The gap detection is the moat.
2. **`gbrain search`** — Hybrid retrieval (Vector + BM25 + RRF + Reranker). 3 modes: `conservative`/`balanced`/`tokenmax` with explicit per-query cost estimates.
3. **Self-wiring knowledge graph** — Automated entity extraction + typed relationship edges (`works_at`, `founded`, `invested_in`, `attended`) from markdown/wikilinks. **Zero LLM calls.** +31.4% P@5 lift over vector-only RAG.

## Architecture

### Engines (Two, One Contract)

| Engine | Use Case | Scale |
|--------|----------|-------|
| **PGLite** (Postgres 17 WASM) | Personal brains, zero config | ~50K pages max |
| **Postgres + pgvector** (Supabase/self-hosted) | Shared, multi-machine | Unlimited |

### Brain × Source Model

- **Brain** = Database (personal or team)
- **Source** = Git repo inside that brain
- Routing via `.gbrain-source` dotfiles, 6-tier precedence chain
- Source of record is the git repo; syncs to Postgres; deletes in git = soft deletes in DB

### Data Ingestion

Multiple paths: `gbrain capture <url|file|text>`, webhooks (Zapier, IFTTT, Apple Shortcuts), inbox folder (`~/.gbrain/inbox/`), MCP protocol from remote agents, third-party skillpacks.

### Production Scale (Garry's instance)

- 146,646 pages indexed
- 24,585 people entities
- 5,339 company entities
- 66 autonomous cron jobs

## Key Differentiators vs. Existing Stack

| Feature | Hermes + Mnemosyne | gbrain |
|---------|-------------------|--------|
| Knowledge retrieval | Mnemosyne recall (key-value) | Hybrid vector + BM25 + RRF + graph reranker |
| Synthesis | Agent writes from context | `gbrain think` — dedicated synthesis with citations |
| Gap analysis | None | Built-in — flags stale/missing knowledge |
| Knowledge graph | Mnemosyne graph (manual edges) | Auto-extracts entities + typed edges from content |
| Schema flexibility | Flat key-value | Schema packs (custom via `gbrain schema` CLI) |
| Search cost awareness | None | Explicit cost matrix (3 modes × 4 model tiers) |
| Protocol | Mnemosyne API | MCP server (30+ tools), CLI, HTTP |
| Multiuser | Single-user | Brain mounts for team shared context |

## Where gbrain Excels

### Knowledge-Intensive Research (History Research)
- Feed historical sources → auto-extracts people, events, dates, places
- Typed relationships (`governed`, `declared_war_on`, `signed_treaty`, `wrote_to`) build graph automatically
- Multi-hop graph queries: "Show all connections between X and Y"
- Gap analysis for coverage: "You haven't indexed anything on Period Z yet"
- Knowledge compounds project-to-project

### Cross-Source Synthesis (DABT Study)
- Ingest textbooks (Casarett & Doull, Hayes) + regulations (OECD, ICH, FDA) + past exams
- One query synthesizes across all: "What are carcinogenicity testing requirements?"
- Returns citations spanning textbook chapter + regulatory guideline + past exam question
- Gap analysis flags exam prep blind spots

## Where gbrain Falls Short

| Territory | Why gbrain doesn't help | Who handles it |
|-----------|------------------------|----------------|
| Coding agents | No Pi/Codex/Claude Code equivalent | Hermes → Pi |
| Trading pipeline | No BAMBAM/swingcatcher/Binance capability | Hermes → custom scripts |
| Agent orchestration | No orchestrator — brain to *query*, not agent manager | Hermes (delegate_task, cron, kanban) |
| Arbitrary tool integration | Can't run Lightpanda, call Binance API, execute terminal | Hermes tool ecosystem |

## The Layered Architecture (Recommended Integration)

```
User request
       |
  ┌────┴────┐
  │ Hermes  │  ← Orchestrator: decompose, delegate, synthesize, verify
  └────┬────┘
       |
  ┌────┴────┐    ┌────────┐    ┌──────────┐
  │ gbrain  │    │ Pi     │    │ Lightpanda│  ← Specialists
  │ (brain) │    │ (code) │    │ (scrape) │
  └────┬────┘    └────────┘    └──────────┘
       |
  ┌────┴────┐
  │ PDF refs│  ← Source material (Casarett, Hayes, regs)
  └─────────┘
```

Hermes stays the orchestrator. gbrain becomes the brain layer for knowledge queries. Pi handles code. Lightpanda handles scraping. No replacement — pure addition.

## DABT Reference Material State

Actual files on disk (NOT yet extracted to markdown):

| Source | Format | Location |
|--------|--------|----------|
| Casarett & Doull 9e | ~35 ch, ~10 MB | reference/textbooks/casarett-doull-9e.pdf |
| Hayes 7e | ~39 ch, ~11 MB | reference/textbooks/hayes-7e.pdf |
| OECD guidelines | 12+ PDFs | reference/regulations/oecd/ |
| ICH guidelines | 9+ PDFs | reference/regulations/ich/ |
| FDA documents | 3+ PDFs | reference/regulations/fda/ |

**Critical:** The AGENTS.md references a `reference/extracted/` directory with 35 C&D chapters, 39 Hayes chapters, and 29 regulations as markdown. **This directory does not exist.** All source material is in raw PDF. Any gbrain integration would require an extraction step first (PDF→markdown), then `gbrain import` to ingest.

## gbrain Installation Path

```bash
git clone https://github.com/garrytan/gbrain.git ~/gbrain && cd ~/gbrain
curl -fsSL https://bun.sh/install | bash  # if not installed
export PATH="$HOME/.bun/bin:$PATH"
bun install && bun link
```

Requires: bun (already installed), OpenAI API key (for embeddings), optional Anthropic API key (for query expansion).

Search mode confirmation required at setup (cost matrix — 25x spread between conservative/tokenmax modes).

## Full Collision-Matrix Audit (2026-05-25)

A systematic 10-dimension audit against the existing Hermes v0.14.0 installation before installation.

### ✅ No Conflict (Safe)

| Dimension | Result | Details |
|-----------|--------|---------|
| **Runtime** | ✅ Clean | Bun 1.3.14 already at `/root/.bun/bin/bun` (used by `herm` CLI). gbrain is TypeScript/Bun. Hermes is Python. No venv overlap. |
| **Ports** | ✅ Clean | Only ports 22 (SSH), 631 (CUPS), 8642 (Hermes API). gbrain MCP uses stdio by default. |
| **Env vars** | ✅ Clean | gbrain needs `OPENAI_API_KEY` (required) + `ANTHROPIC_API_KEY` (optional). Hermes uses `NOUS_API_KEY`, `OPENCODE_GO_API_KEY`, `OPENROUTER_API_KEY` — zero name collision. |
| **Config files** | ✅ Clean | gbrain → `~/.gbrain/`. Hermes → `~/.hermes/` + `/usr/local/lib/hermes-agent/`. Separate homes. |
| **Databases** | ✅ Clean | gbrain → PGLite (Postgres WASM, local file). Hermes → SQLite + Mnemosyne (separate). Different engines, different data. |
| **Cron** | ✅ Clean | gbrain has internal Minions queue. Hermes cron is Hermes-managed. No shared tables. |
| **Filesystem paths** | ✅ Clean | gbrain repo → `~/gbrain/`. Hermes → `~/.hermes/` and `/usr/local/lib/hermes-agent/`. |
| **Plugins** | ✅ Clean | Installed: doga, hermes-achievements, mnemosyne. All operate in different domains. |
| **MCP/API** | ✅ Clean | Hermes config has `mcp_servers: {}` — empty. gbrain can be added as an MCP server when ready. |
| **Disk space** | ⚠️ Tight | 38 GB disk, 94% full (34 GB used), only **2.4 GB free**. gbrain repo (~40 MB) + bun deps (~100-200 MB) + PGLite DB with embeddings (~500 MB–2 GB for 25 MB of source material) = 0.6–2.4 GB estimated need. See Disk Space Analysis below. |

### Root Cause of 94% Disk Usage

The disk consumption is **not** from Hermes base installation (~2 GB for code + dependencies). The `.git` directory within `/usr/local/lib/hermes-agent/` had accumulated **14.6 GB of garbage**:

- **856 orphaned `tmp_pack_*` files** (17-20 MB each) in `.git/objects/pack/`
- Caused by repeated `hermes update` — each run does `git fetch` + `git pull`, and failed/interrupted operations leave temporary pack files that git never cleans up
- `git count-objects -vH` confirms: `garbage: 856, size-garbage: 14.64 GiB`

**Cleanup plan:**
1. Remove stale `tmp_pack_*` files (orphaned since May 20 — weeks old)
2. Run `git gc --prune=now` to repack valid objects and prune unreachable ones
3. Expected: 14-16 GB recovered, bringing usage from 94% → ~50-55%

### Other Disk Usage (Before Cleanup)

| Path | Size | Notes |
|------|------|-------|
| `/usr/local/lib/hermes-agent/.git/` | 16 GB | 14.6 GB garbage + ~1.4 GB valid |
| `/usr/local/lib/hermes-agent/venv/` | 1.6 GB | Python deps (pip packages) |
| `/usr/local/lib/hermes-agent/web/` | 286 MB | Node frontend |
| `/usr/local/lib/hermes-agent/ui-tui/` | 243 MB | Ink terminal UI |
| `/root/.hermes/state-snapshots/` | 1.1 GB | Hermes checkpoints |
| `/root/.hermes/mnemosyne/` | 666 MB | Memory provider |
| `/root/.hermes/node/` | 460 MB | Node.js runtime |
| `/root/.hermes/state.db` | 397 MB | SQLite state |
| `/root/.hermes/sessions/` | 169 MB | Session history |
| `/root/work/dabt/` | 497 MB | DABT study materials |

## Pitfalls

- **`reference/extracted/` is aspirational** — Don't assume extracted markdown exists. Verify directories before running `gbrain import`.
- **Not an orchestrator** — Don't try to replace Hermes with it. They serve different roles. gbrain is a brain to *query*, not an agent framework.
- **Search mode costs matter** — User is token-conscious (OpenCode Go subscription). Always confirm search mode (`conservative`/`balanced`/`tokenmax`) before integrating. Default `balanced` is the safe starting point.
- **No coding agent** — Any evaluation that claims gbrain replaces Pi/Codex is wrong. gbrain has no code execution capability.
- **API keys needed** — Requires OpenAI for vector search. User doesn't have an active OpenAI key in this profile. Prerequisite blocker.
