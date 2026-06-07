# Escalation Decision Tree Pattern

Generalizable pattern for tool-fallback chains. Use when no single tool covers all failure modes but you want a single interface.

## Core Principle

**Try native first, escalate on concrete failure signals only.** Never escalate on "this feels hard" — every escalation must be bound to a measurable trigger.

## The Tree Structure

```
                         ┌──────────┐
                         │  Query   │
                         └────┬─────┘
                              │
                    ┌─────────▼──────────┐
                    │  Level 0: Native   │
                    │  (first-line tool) │
                    └─────────┬──────────┘
                              │
                ┌─────────────┼──────────────┐
                ▼                             ▼
          ✅ Success                    ❌ Classification
          (return)                      (failure signal)
                                               │
                                               ▼
                    ┌──────────────────────────────────┐
                    │ Level 1: First fallback          │
                    │ (different backend, same class)  │
                    └────────────────┬─────────────────┘
                                     │
                        ┌────────────┼──────────────┐
                        ▼                            ▼
                  ✅ Success                     ❌ Escalate
                  (return — stop here!)          (next level)
                                                       │
                                                       ▼
                                          ┌───────────────────────┐
                                          │  Level 2+: deeper     │
                                          │  fallbacks or agent   │
                                          └───────────────────────┘
```

### Rules

1. **Hermetic levels** — each level is self-contained. It does not depend on results from the previous level (beyond knowing the previous level failed).
2. **Stop on success** — if a level returns useful results, DO NOT cascade further. The tree is a fallback chain, not a pipeline.
3. **Concrete triggers only** — every escalation requires a measurable failure signal:
   - `web_search ≤ 2 results for valid query`
   - `web_extract returned empty or ≤ 200 chars`
   - `browser crashed with OOM`
   - `barrier detected with confidence > 0.7`
4. **Max depth = 4** — beyond that, surface the full failure chain to the user. Don't retry.
5. **Failure chain trace** — if all levels fail, report: which levels were tried, which signals fired at each level, and the raw error from the deepest level.

## Mapping Workflow Pattern Kit to the Tree

| Pattern | Role in Tree |
|---|---|
| **DAG** | Orchestrates the serial escalation layers. Each level is a DAG task with `depends_on=[previous_level]`. On success, short-circuit by returning early (no subsequent task runs). |
| **ToolRegistry** | Registers each fallback as a typed tool. The registry handles param schemas, context injection, and generates the LLM-visible description so the model knows the tool exists. |
| **OutputGate** | Validates the response at each level. A response that passes OutputGate = success for that level. A response that fails OutputGate (empty, stub, raw noise) = escalate. |
| **LoopDetector** | Prevents infinite escalation loops: Level 4 fails → back to Level 0 → Level 0 fails again → Level 1 → ... → Level 4 → repeat. The detector catches repeated escalation cycles and forces a user-facing failure chain instead of retrying. |
| **Dedup** | Prevents redundant escalation. If the same query was already sent through the tree with the same results, return cache hit instead of re-escalating. |

### Integration sketch

```python
from workflow_pattern_kit import DAG, ToolRegistry, OutputGate, LoopDetector, Dedup

dag = DAG(max_concurrency=1)
registry = ToolRegistry()
gate = OutputGate()
detector = LoopDetector(window_size=20)
dedup = Dedup(duplicate_threshold=0.85)

@dag.task(depends_on=[])
async def level0_native(params):
    result = await native_search(params["query"])
    return result

@dag.task(depends_on=["level0_native"])
async def level1_fallback(prev, ctx):
    if _is_success(prev): return prev  # stop cascade
    return await fallback_search(prev.get("query"))
```

## Worked Example: GroktoCrawl Escalation Tree

Concrete tree designed for a historical research workflow on a 2GB VPS with a self-hosted Firecrawl-alternative stack as fallback.

### Level 0: Hermes native tools
- **Tools**: `web_search` (Tavily), `web_extract` (Tavily/Jina), `browser` (Lightpanda/agent-browser)
- **Trigger**: default — always try first
- **Fail signals**:
  - `web_search returns ≤ 2 results` for a specific, well-formed query
  - `web_extract returns empty or ≤ 200 chars` for a URL known to have content
  - `browser crashes or times out`

### Level 1: SearXNG search (GroktoCrawl /v2/search)
- **Backend**: SearXNG meta-search (aggregates DuckDuckGo, Google, Bing, others)
- **Trigger**: Level 0 search failed (≤ 2 results)
- **Fail signal**: still empty, or API unreachable

### Level 2: Three-tier scraper (GroktoCrawl /v2/scrape)
- **Trigger**: Level 0 web_extract failed (empty/error/boilerplate)
- **Backend**: auto-degrades through 3 tiers: /llms.txt → Accept: text/markdown → Playwright
- **Fail signal**: barrier detected (Cloudflare, CAPTCHA, empty-content)

### Level 3: Playwright browser / Crawl / Map
- **Trigger**: Level 2 returned a barrier, or need site-wide URL discovery
- **Tools**: GC /v2/scrape with `browser=true`, /v2/crawl, /v2/map, flare-solverr
- **Fail signal**: all browser methods blocked

### Level 4: Autonomous agent (GroktoCrawl /v2/agent)
- **Trigger**: All lower levels failed
- **Behavior**: LLM-driven research loop: search → scrape → evaluate → search deeper → synthesize
- **Fail signal**: agent returns empty → surface full failure chain to user, do not retry

### Full failure chain report

If all 4 levels fail, report back:
```
[Tried] Level 0: web_search → 0 results (signal A)
[Tried] Level 1: SearXNG → API unreachable  
[Tried] Level 2: GC scrape → barrier: cloudflare (confidence 0.95)
[Tried] Level 3: GC browser → flare-solverr also failed
[Tried] Level 4: GC agent → returned empty after 3 cycles
[Result] All 4 escalation levels exhausted. 
         Blocker: Cloudflare challenge at target domain (confirmed by 2 methods)
```

## When to use this pattern

Use when:
1. Multiple backends exist for the same capability (search, extraction, scrape)
2. Failure modes are diverse and need different remedies
3. The user wants structured fallback, not silent retries
4. Cost matters — cheaper backends first, expensive ones last

Do NOT use when:
1. A single reliable tool covers all cases
2. The task is latency-sensitive (each level adds time)
3. The user explicitly wants "try harder" without structure
