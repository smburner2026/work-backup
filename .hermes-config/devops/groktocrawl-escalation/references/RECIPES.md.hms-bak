# Recipes — Concrete Invocations for Each Level

## Setup (one-time)

```bash
# Install GroktoCrawl + wrapper
groktocrawl install

# Edit the .env to set your LLM provider
nano ~/groktocrawl/.env

# Bring up the stack
groktocrawl start

# Verify
groktocrawl status
```

## Level 0 — Native tools (the default)

```python
# Always try this first. The escalation skill should never be the
# first thing you reach for.

# In a Hermes agent context, the model just calls these directly:
#   web_search(query, limit=10)
#   web_extract(url)
#   browser(url)

# If the model is using this skill programmatically:
from escalate import SessionContext, NativeTools

ctx = SessionContext(
    native=NativeTools(
        web_search=my_hermes_web_search,
        web_extract=my_hermes_web_extract,
        browser=my_hermes_browser,
    ),
    gc=GroktoCrawl(),  # client ready but stack may be down
)

result = await escalate("Napoleon strategy primary sources", ctx=ctx)
```

## Level 1 — SearXNG fallback (Signal A)

**Trigger**: `len(web_search_results) <= 2` for a valid query.

```bash
# Stack must be running
groktocrawl status   # check first
groktocrawl start    # if not
```

```python
# Programmatic invocation (called automatically by escalate() at Level 1)
result = gc.search("VSTB quyen 1 nguon goc", sources="web", limit=5)

# Manual curl (for debugging)
curl -X POST http://localhost:8080/v2/search \
  -H "Content-Type: application/json" \
  -d '{"query": "VSTB quyen 1 nguon goc", "limit": 5}'
```

**Output shape:**
```json
{
  "data": [
    {"url": "https://...", "title": "...", "snippet": "..."},
    ...
  ]
}
```

## Level 2 — Three-tier scraper (Signal B)

**Trigger**: `web_extract` returned `error`, empty, or `< 200 chars`.

```python
# Auto-degrades through:
#   Tier 1: GET /llms.txt (whole site in markdown)
#   Tier 2: Accept: text/markdown header
#   Tier 3: Playwright render + readability

result = gc.scrape("https://gallica.bnf.fr/ark:/12148/btv1b9002548p")

# Manual
curl -X POST http://localhost:8080/v2/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://gallica.bnf.fr/ark:/12148/btv1b9002548p"}'
```

**Output shape on success:**
```json
{
  "markdown": "...",
  "quality": {"score": 0.87, "breakdown": {...}},
  "source": "tier-2-accept-markdown"
}
```

**Output shape on barrier (escalate to Level 3):**
```json
{
  "error": "Barrier detected: cloudflare (confidence: 0.85)",
  "barrier": {
    "detected": true,
    "type": "cloudflare",
    "confidence": 0.85,
    "detail": "Matched: cloudflare-title, empty-content"
  },
  "markdown": "",
  "source": "barrier-detection"
}
```

## Level 3 — Full browser / crawl (Signals C, D, E)

**Triggers**:
- Hermes browser crashed/OOM
- Level 2 returned `barrier.detected == True` with `confidence > 0.7`
- Task requires "all pages" or "every URL" (crawl/map)

```python
# Force Playwright tier
result = gc.scrape_with_browser("https://example.com/login-wall")

# Crawl a whole site (capped at depth + limit)
crawl = gc.crawl("https://example.com/collection", max_depth=2, limit=20)

# Just discover URLs
urls = gc.map_urls("https://example.com/sitemap-section", limit=100)
```

## Level 4 — Autonomous agent (Signal F)

**Trigger**: all lower levels failed. **Always last resort** — surfaces full failure chain to user.

```python
result = gc.agent(
    prompt=(
        "Find primary source references for the 1789 Declaration of "
        "the Rights of Man and Citizen in the original French. "
        "Try archive.org, Gallica, and BAnQ. Accept that some "
        "digitized sources may not be reachable and report what "
        "you found vs. what you tried."
    ),
)

# Or use a specific model for the research loop
result = gc.agent(
    prompt="...",
    model="deepseek-v4-flash",  # override LLM_MODEL for this job
)
```

**Output shape:**
```json
{
  "job_id": "agent-abc123",
  "status": "completed",
  "answer": "...",
  "sources": [...],
  "attempted_chain": ["search", "scrape", "browser", "agent"]
}
```

## Stack management

```bash
# Full stack (~750MB RAM, default)
groktocrawl start

# Minimal: no browser, no parse, no ofelia (~315MB RAM)
# Use this for search-only and scrape-only workloads
groktocrawl minimal

# Check status
groktocrawl status

# Tail logs
groktocrawl logs

# Tear down (frees RAM)
groktocrawl stop
```

## Common patterns

### Pattern: archive page known to fail native

```python
# Native extract returns 0 chars on Gallica due to ARK resolver
result = await escalate(
    query="Déclaration des droits de l'homme 1789 texte original",
    url="https://gallica.bnf.fr/ark:/12148/btv1b9002548p",
    ctx=ctx,
)
# escalate() detects Signal B, escalates to Level 2 (GC scrape),
# which may then escalate to Level 3 (Playwright) if blocked.
```

### Pattern: "all pages on this archive" task

```python
# Set the signal manually before calling
result = await escalate(
    query="sitemap gallica collection viet-nam",
    url="https://gallica.bnf.fr/services/engine/search/sru?...",
    ctx=ctx,
)
# When the URL is discovered, escalate.py uses gc.crawl() at Level 3
```

### Pattern: 3 failed escalations → surface to user

```python
# Loop detector triggers at 3 escalations. If escalate() returns
# success=False and full_failure_chain starts with "loop detected",
# show the user the chain — don't try again.
result = await escalate("...", ctx=ctx)
if not result.success and "loop detected" in (result.full_failure_chain or ""):
    print(result.full_failure_chain)
    # User decides: try a different query, or accept that the
    # information isn't reachable.
```

### Pattern: Substack article extraction

```bash
# Vanity domain — auto-detected as Substack
curl -X POST http://localhost:8080/v2/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.lennysnewsletter.com/p/why-were-at-the-beginning-of-the"}'
# → source: substack-rss, clean markdown + YAML frontmatter

# Native substack.com domain
curl -X POST http://localhost:8080/v2/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://platformer.substack.com/p/some-article"}'
```

**Note:** Non-Substack URLs with `/p/` in path (e.g. `danielmiessler.com/p/...`) are correctly rejected — they fall through to the generic pipeline.

### Pattern: Cache-aware scraping

```bash
# First scrape — full pipeline, creates cache entry
curl -X POST http://localhost:8080/v2/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.python.org/3/"}'
# → source: content-negotiation, fetch_count: 1

# Second scrape — cache hit, conditional revalidation
curl -X POST http://localhost:8080/v2/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.python.org/3/"}'
# → source: content-negotiation, fetch_count: 2, change_count: 0
```

### Pattern: Observability check

```bash
# Full health with per-dependency probes
curl -fsS http://localhost:8080/health | python3 -m json.tool

# Prometheus metrics
curl -fsS http://localhost:8080/metrics
```
