# GroktoCrawl API Quirks

Discovered during VPS deployment and testing (2026-06-06).

## Endpoint: POST /v2/search

**Quirk:** `sources` must be a list, not a string.

```python
# WRONG — returns 422
{"query": "test", "sources": "web"}

# CORRECT
{"query": "test", "sources": ["web"]}
```

## Endpoint: POST /v2/scrape

**Response nesting:** All data is nested under `data` key.

```json
{
  "success": true,
  "data": {
    "markdown": "...",
    "metadata": {"source": "playwright"},
    "download": null
  }
}
```

The `extract_markdown()` and `extract_quality()` helpers in `groktocrawl_client.py` check `data` first, then fall back to top-level.

## Endpoint: POST /v2/scrape (Playwright)

**Trigger:** Add `"useBrowser": true` to the request body.

```json
{"url": "https://example.com", "useBrowser": true}
```

## Endpoint: POST /v2/answer (v0.7.0+)

**Synchronous grounded Q&A with citations.** No job IDs, no polling — one request, one answer.

```json
{
  "query": "What is the current Fed interest rate?",
  "num_sources": 3,
  "model": "optional-per-request-override",
  "stream": false
}
```

**Response:**
```json
{
  "success": true,
  "answer": "The current federal funds rate is 3.50% to 3.75% [1].",
  "sources": [{"url": "...", "title": "...", "relevance": "..."}],
  "citations": [{"index": 1, "url": "..."}],
  "search_type": "auto",
  "latency_ms": 8133
}
```

**Pipeline:** SearXNG search → scraper-svc (first 8K chars per result) → LLM synthesis with citation instructions → regex citation parser → response.

**Requires:** Real LLM configured in `.env` (not `fixture-model`). See troubleshooting.md for OpenRouter free model config.

**SSE streaming:** Set `"stream": true` for token-by-token output. Events: `sources` → `token` × N → `done` → `[DONE]`.

**Edge case — no results:** Returns `"answer": "I was unable to find or scrape any relevant web pages..."` with empty sources. Success is still `true`.

## Docker Stack Memory (measured)

| Container | RAM |
|---|---|
| agent-svc | ~29MB |
| browser-svc | ~59MB |
| scraper-svc | ~246MB |
| searxng | ~54MB |
| valkey | ~4MB |
| **Total (full)** | **~392MB** |
| **Total (minimal, no browser)** | **~333MB** |

## VPS Deployment Notes

- Docker installed via `curl -fsSL https://get.docker.com | sh`
- GroktoCrawl v0.6.0 cloned to `~/groktocrawl`
- `.env` created from `.env.sample` — no LLM key needed for search/scrape
- Containers use `restart: unless-stopped` — stop with `docker compose down`
- On 2GB VPS: use on-demand, not permanent
- `groktocrawl` wrapper auto-starts/stops Docker daemon on demand (saves ~100MB RAM when idle)

## VPS RAM Optimization (2GB plan)

Services safe to disable on headless VPS:
- `multipathd` — device-mapper multipath controller (28MB RAM, useless on VPS)
- `snapd` daemon — only needed if actively using snap packages (20MB RAM)
- Docker daemon — auto-stopped by `groktocrawl stop` when no containers running (100MB RAM)
- Journald — limit retention with `SystemMaxUse=50M` in `/etc/systemd/journald.conf.d/vacuum.conf`

Total savings: ~150-230MB RAM + ~85MB swap freed.
