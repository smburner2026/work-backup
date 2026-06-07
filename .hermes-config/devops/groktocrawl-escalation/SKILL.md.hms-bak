---
name: groktocrawl-escalation
description: Escalate web research to GroktoCrawl when Hermes native tools fail. Four-level decision tree (search → scrape → browser → agent) with workflow-pattern-kit integration. Includes intelligent scrape cache (ETag/revalidation, per-domain TTLs), observability (health probes, /metrics), and site-specific adapters (Substack RSS). Use ONLY when native web_search/web_extract returns empty, browser crashes, or a barrier is detected — never as a first call.
version: 0.2.0
author: Hermes Agent
tags: [groktocrawl, fallback, web-research, escalation, dag, tool-registry, output-gate, loop-detector, dedup]
prerequisites:
  python:
    - pydantic>=2.0
    - workflow_pattern_kit (from workflow-pattern-kit skill — symlink + .pth required, see Pitfalls)
  external:
    - GroktoCrawl Docker stack — either VPS localhost:8080 or WSL @ 100.110.237.89:8080 (Levels 1-2 only; Level 0 is pure Python)
    - Docker installed (for Levels 1-2; Level 0 needs nothing)
platforms: [linux, macos, wsl]
metadata:
  hermes:
    related_skills: [workflow-pattern-kit, engineering-discipline, kanban-orchestrator]
---

# GroktoCrawl Escalation — Four-Level Fallback Tree

> **The core rule**: Hermes native tools (`web_search`, `web_extract`, `browser`) are always the first call. GroktoCrawl is a fallback. Each level is gated by a **concrete failure signal**, not a vibe check. If the level returns useful results, you stop there — you don't cascade.

## When to load this skill

**Always load this skill before any web research task** so the escalation logic is in mind from the start. The skill's `RECIPES.md` (under references) and `escalate.py` (under scripts) handle the actual mechanics.

## The Updated Levels

```
LEVEL 0 — Hermes native tools + plugin + quality gates
────────────────────────────────────────────────────────
  web_search, web_extract, browser (default, always first)
  hermes-web-search-plus plugin (auto-routing across providers)
  /llms.txt check (Tier 1 — single GET before full extraction)
  barrier_classifier → detects Cloudflare/CAPTCHA/rate-limit in response
  quality_gates → rejects boilerplate/empty/block-page responses

  RAM: ~30MB (plugin), 0MB Docker
  Always on, always the first call

  → If all pass & quality ≥ 0.3: return content. Done.

LEVEL 0.5 — Plugin-enhanced search (zero Docker)
─────────────────────────────────────────────────
  web_search_plus / web_extract_plus
  Auto-routes across Tavily + any other provider keys you have
  Trigger: Level 0 returned Signal A (thin search) or G (quality fail)

  → If results pass quality gates: return. Done.

LEVEL 1 — SearXNG search (1 Docker container, on-demand, ~150MB)
─────────────────────────────────────────────────────────────────
  Trigger: Plugin fallback chain also failed
  groktocrawl start → SearXNG self-hosted meta-search → groktocrawl stop

LEVEL 2 — Playwright browser (1 Docker container, on-demand, ~300MB)
─────────────────────────────────────────────────────────────────────
  Trigger: barrier_classifier detected Cloudflare/etc at Level 0
  groktocrawl start → browser-svc → groktocrawl stop

LEVEL 3 — Autonomous agent (last resort)
─────────────────────────────────────────
  Trigger: All lower levels failed
  web_search_plus with research mode, or escalate to user
  Full failure chain reported.
```

## Intelligent Scrape Cache (ADR-0019)

The `/v2/scrape` endpoint now has a **freshness-aware cache** in Valkey (Redis). Repeated scrapes of the same URL skip the full tier pipeline when content hasn't changed.

**How it works:**
- First fetch: full tier pipeline → stores result + `ETag`/`Last-Modified` headers + SHA-256 content hash
- Subsequent fetches: conditional GET using stored headers → `304 Not Modified` extends TTL without re-download
- Sources without HTTP headers: content-hash comparison — stable content doubles TTL, volatile content gets capped at 300s

**Per-domain TTLs** via env config:
```bash
# In .env or docker-compose environment:
SCRAPE_CACHE_DOMAIN_TTLS='{
  "news.ycombinator.com": 300,
  "docs.python.org": 86400,
  "github.com": 1800
}'
# Longest suffix match wins (e.g. docs.python.org before python.org)
```

**Performance impact:** ETag-capant sites see **100x+ speedup** on cache hits (e.g. schema.org: 2s → 19ms).

**Cache metadata per entry:** `source_tier`, `etag`, `last_modified`, `content_hash`, `fetch_count`, `change_count`, `ttl`, `first_fetched_at`, `last_checked_at`.

## Substack Adapter (RSS-based extraction)

Site-specific adapter for Substack publications — extracts full article content via RSS feeds with **zero API keys**.

**Handles:**
- `*.substack.com/p/*` and `*.substack.com/pub/*`
- Vanity/custom domains (e.g. `lennysnewsletter.com/p/...`) — auto-detected via RSS probe

**Tiered extraction:**
1. RSS feed (`{origin}/feed`) → `<content:encoded>` → clean Markdown (fastest, most reliable)
2. Readability-lxml fallback
3. Playwright browser (last resort)

**Returns:** Clean Markdown + YAML frontmatter (`title`, `author`, `publication`, `published_date`, `source: substack-rss`).

**Domain probe cache:** 1-hour TTL to avoid repeated checks for same publication.

**Correctly rejects:** Non-Substack URLs with `/p/` in path (e.g. `danielmiessler.com/p/...` → falls through to generic pipeline).

## Failure signals (what triggers escalation)

These are the **only** valid triggers. Use exactly these. Don't escalate on "I think this is going to be hard."

| Signal | Detect | Escalates to |
|---|---|---|---|
| **A — thin search** | `len(web_search_results) <= 2` for a well-formed query | Level 0.5 (plugin) |
| **B — empty extract** | `web_extract` returns `error`, empty string, or `< 200 chars` | Level 0.5 (plugin) |
| **C — browser crash** | browser tool returns `OOM`, `crashed`, `timeout` | Level 2 (Playwright) |
| **D — barrier detected** | `barrier_classifier` returns `detected=True` with `confidence>0.7` | Level 2 (Playwright) |
| **E — need site crawl** | Task requires "all pages", "every URL", site map | Level 2 (Playwright) |
| **F — total failure** | All lower levels returned no useful content | Level 3 (agent, surface chain) |
| **G — quality fail** | `quality_gates` returns `score < 0.3` (boilerplate/block) | Level 0.5 (plugin)

## Workflow kit integration

| Pattern | Use in this skill |
|---|---|
| `DAG` | The 4 levels as serial task layers — each runs only if the previous escalated |
| `ToolRegistry` | GroktoCrawl endpoints (`/v2/search`, `/v2/scrape`, `/v2/crawl`, `/v2/agent`, `/v2/answer`) registered as typed actions |
| `OutputGate` | Validates each level's output — rejects empty/boilerplate/fabricated responses, triggers escalation on rejection |
| `LoopDetector` | Catches escalation loops — if you've escalated 3+ times without success, surface to user instead of retrying |
| `Dedup` | Pre-checks queries against recent history — skip re-escalation for queries already failed within the last hour |

## Architecture: Minimal Hermes-Native (with optional on-demand Docker)

The valuable parts of GroktoCrawl have been **extracted as pure Python** (MIT license):
- `barrier_classifier.py` — Cloudflare/CAPTCHA/rate-limit detection (~100 lines)
- `quality_gates.py` — boilerplate/completeness/block-page assessment (~150 lines)
- `llms_txt_fetcher.py` — Tier 1 /llms.txt single-GET (~20 lines)
- `groktocrawl_client.py` — HTTP client to Docker-based services

These run at Level 0 — zero Docker, zero extra RAM beyond the plugin (~30MB).

**Docker is only needed for:**
1. **SearXNG** (1 container, ~150MB on-demand) — self-hosted search if plugin providers fail
2. **Playwright** (1 container, ~300MB on-demand) — browser rendering if barrier detected

```
┌─────────────────────────────────────────────────────────────────┐
│  ALWAYS ON (zero Docker, ~30MB RAM total)                       │
│                                                                  │
│  hermes-web-search-plus plugin (multi-provider routing)          │
│  barrier_classifier.py    (MIT extract — barrier detection)      │
│  quality_gates.py         (MIT extract — content quality)        │
│  llms_txt_fetcher.py      (MIT extract — /llms.txt check)       │
│  escalate.py              (DAG → OutputGate → LoopDetector →     │
│                            Dedup + all extracts)                 │
│                                                                  │
│  → Handles 90%+ of web research without any Docker               │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼  (only if plugin + extracted modules all fail)
┌─────────────────────────────────────────────────────────────────┐
│  ON-DEMAND (start/stop, 0MB when idle)                          │
│                                                                  │
│  1 container: SearXNG (~150MB) — self-hosted search              │
│  1 container: browser/Playwright (~300MB) — JS rendering         │
│  groktocrawl start  →  groktocrawl stop                          │
└─────────────────────────────────────────────────────────────────┘
```

### When to start Docker (and when not to)

| Trigger | Action |
|---|---|
| Level 0.5 plugin all fails (all providers returned no results) | `groktocrawl start` (SearXNG) |
| barrier_classifier detects Cloudflare/CAPTCHA in native response | `groktocrawl start` (Playwright) |
| Stack already up from earlier in session | reuse, don't restart |
| Work complete | `groktocrawl stop` |

**Never start Docker when:** Level 0 is succeeding, or the plugin handles the query. The whole point of having the extracted Python modules is to avoid Docker for the common case.

## Why this prevents model-disuse

1. **Default path is always Level 0.** GroktoCrawl is a fallback, never a first call. The model has to first try the native tools.
2. **Concrete triggers only.** No "feels like I should escalate" — exact signals (≤2 results, <200 chars, OOM, barrier detected).
3. **Each level has a stop signal.** If Level 1 returns useful results, the DAG stops. No automatic cascade.
4. **Loop detector prevents infinite escalation.** If you've tried Level 4 twice without success, the skill surfaces the full failure chain to you instead of silently retrying.
5. **Dedup prevents redundant work.** Same query + same failure within the last hour → returns the cached failure result instead of re-escalating.

## Quick reference

```python
# Trigger escalation
from groktocrawl_escalation import escalate

result = await escalate(query, url=None, level=0, ctx=session_ctx)
if result.success:
    return result.content
# Otherwise result.escalation_trace contains the full chain to surface to user
```

```bash
# ── Health & Observability ──────────────────────────────────────────
# Health endpoint with per-dependency probes (valkey, searxng, scraper, browser)
curl -fsS http://localhost:8080/health
# Returns: {"status":"ok","checks":{"valkey":{"status":"ok","latency_ms":1,...},"searxng":{...},"scraper":{...},"browser":{...}}}

# OpenMetrics endpoint for Prometheus scraping
curl -fsS http://localhost:8080/metrics

# ── Scraping ───────────────────────────────────────────────────────
# Trigger /v2/scrape manually (results are cached — see Intelligent Cache below)
curl -X POST http://localhost:8080/v2/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://gallica.bnf.fr/ark:/12148/..."}'

# Grounded Q&A with citations (v0.7.0+)
curl -X POST http://localhost:8080/v2/answer \
  -H "Content-Type: application/json" \
  -d '{"query": "your question", "num_sources": 3}'

# ── CLI ────────────────────────────────────────────────────────────
cd ~/groktocrawl && ./groktocrawl answer "your question" --num-sources 5 --json

# ── Stack Management ───────────────────────────────────────────────
groktocrawl start     # wraps: cd ~/groktocrawl && docker compose up -d
groktocrawl stop      # wraps: cd ~/groktocrawl && docker compose down
groktocrawl status    # wraps: docker compose ps
```

## Pitfalls

- **Don't make GroktoCrawl the first call.** Level 0 is always the default. The model has to first try Hermes native tools — otherwise this whole thing is pointless.
- **Don't auto-cascade levels.** If Level 1 returns good results, the DAG stops there. Don't keep escalating "just in case."
- **Check stack health before each call.** A simple `curl /health` first; if the stack is down, surface to the user rather than waste 30s on timeouts.
- **The Tailscale IP can change.** If `100.110.237.89` is unreachable, check `tailscale status` and update `GROKTOCRAWL_URL` in this skill's config.
- **Loop detector threshold is 3, not 10.** Three escalations without success is a clear signal to stop and report, not a prompt to keep trying.
- **`search()` sources must be a list.** The API expects `"sources": ["web"]`, not `"sources": "web"`. Passing a string returns 422 Unprocessable Content.
- **`extract_markdown()` checks nested `data` first.** GroktoCrawl responses nest content under `{"success": true, "data": {"markdown": "..."}}`. The helper checks `data` dict first, then falls back to top-level.
- **`extract_quality()` same nesting.** Quality scores are under `data.quality`, not top-level.
- **Docker on-demand on 2GB VPS.** Don't leave containers running permanently. Use `groktocrawl start` / `groktocrawl stop`. Full stack uses ~392MB; minimal (no browser) uses ~315MB.
- **Tweets/social content: use `web_extract` first, never browser.** Browser sessions on thin-margin providers (opencode-go/DeepSeek) can choke on heavy tool-use turns. `web_extract` handles Twitter/X URLs via Firecrawl and returns clean markdown. Reserve browser for JS-rendered pages or login-required content only.
- **`classify_barrier` first arg is `url`, not content.** Passing text as the first positional arg sets `url=text` with `html=""` and `content=""` → always returns `detected=False`. Use `classify_barrier(url="...", content="text")` with explicit kwargs.
- **`escalate.py` requires `workflow_pattern_kit`.** If import fails with `ModuleNotFoundError`, the symlink + .pth from the workflow-pattern-kit skill is missing. Quick fix: `cd /root/.hermes/skills/devops/workflow-pattern-kit && ln -sf python workflow_pattern_kit && SITE_PACKAGES=$(python3 -c 'import site; print(site.getsitepackages()[0])') && echo '/root/.hermes/skills/devops/workflow-pattern-kit' > $SITE_PACKAGES/workflow_pattern_kit.pth`
- **Scrape cache is automatic — no config needed.** The intelligent cache (ADR-0019) activates on all `/v2/scrape` calls. First fetch is always a full pipeline; subsequent fetches use conditional revalidation. Per-domain TTLs are optional via `SCRAPE_CACHE_DOMAIN_TTLS` env var. Content without ETag/Last-Modified uses SHA-256 hashing — stable content doubles TTL, volatile content caps at 300s.
- **Substack adapter is auto-registered.** No config needed — it detects `*.substack.com` URLs and vanity domains via RSS probe. If you're scraping a non-Substack site that happens to have `/p/` in the URL path, it correctly falls through to the generic pipeline.

## Files in this skill

- `SKILL.md` — this file (always loaded)
- `scripts/barrier_classifier.py` — Cloudflare/CAPTCHA/rate-limit detector (MIT extract, zero Docker)
- `scripts/quality_gates.py` — Boilerplate/completeness/block-page assessment (MIT extract, zero Docker)
- `scripts/llms_txt_fetcher.py` — Tier 1 scrap: /llms.txt single-GET (MIT extract, zero Docker)
- `scripts/groktocrawl_client.py` — HTTP client to GroktoCrawl endpoints (Docker API)
- `scripts/groktocrawl` — bash wrapper for start/stop/status/logs/minimal/install
- `scripts/escalate.py` — the actual escalation logic (uses DAG, OutputGate, LoopDetector, Dedup + all extracts)
- `references/RECIPES.md` — concrete invocation examples for each level
- `references/troubleshooting.md` — common failures and fixes
- `references/api-quirks.md` — API quirks, response nesting, Docker memory usage, VPS deployment notes
- `references/diagnostic-checklist.md` — step-by-step health check when reporting failures
