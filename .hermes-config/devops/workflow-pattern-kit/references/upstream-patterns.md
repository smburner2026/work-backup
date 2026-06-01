# Upstream Pattern Origins

This document traces each pattern in the `workflow-pattern-kit` back to its
source project and explains what was adapted vs copied.

---

## ToolRegistry → browser-use `Registry`

**Source:** `browser_use/tools/registry/service.py` — `class Registry`
**Lines in source:** ~500
**Lines in kit:** ~320

**What browser-use does:**
Registers typed actions (Pydantic models as param schemas). Auto-injects special
params (`browser_session`, `page_url`, `cdp_client`, `file_system`) by inspecting
the function signature. Generates LLM-friendly prompt descriptions. Supports
domain-based action filtering. Async + sync.

**What we changed:**
- Removed CDP/browser-specific special params, kept the generic ones
- Simplified param model building: supports Type 1 (BaseModel param) and Type 2
  (flat individual params) without complex signature normalization
- Added `exclude_action()` for runtime filtering
- Removed telemetry/observability hooks
- Made `execute()` accept dict OR BaseModel

**Key design decision:** browser-use's Registry is deeply coupled to its CDP-based
browser session. Our version is agnostic — context injection works with any infra.

---

## LoopDetector → browser-use `ActionLoopDetector`

**Source:** `browser_use/agent/views.py` — `class ActionLoopDetector`
**Lines in source:** ~200
**Lines in kit:** ~230

**What browser-use does:**
SHA-256 hashes of normalized action parameters tracked in a rolling 20-step window.
Escalating nudges at 5/8/12 repeats. Page fingerprinting for stagnation detection.
Never hard-blocks — only emits context messages for the LLM.

**What we changed:**
- Added cooldown suppression (3-step minimum between nudges, with first-nudge fix)
- Same hash normalization strategies (search/click/input/navigate/scroll)
- Added `reset()` and `summary()` for testability
- Made cooldown configurable

**Key design decision:** Standalone dataclass vs browser-use's Pydantic model with
serialization. Simpler, no checkpoint overhead.

---

## OutputGate → Vibe-Trading `_classify_deliverable`

**Source:** `worker.py` in Vibe-Trading — `_classify_deliverable`
**Lines in source:** ~80
**Lines in kit:** ~180

**What Vibe-Trading does:**
After a swarm worker completes its ReAct loop, classifies the output summary.
Rejects: empty, unparsed tool-call markup, fabricated data markers, plan-only
stubs, data agents with zero tool calls and no report.md.

**What we changed:**
- Added raw tool-result envelope detection (JSON blobs with `status`/`ok`)
- Generalized from markdown report.md to any report file
- Added convenience wrappers (`is_valid_deliverable`, `check_with_report`)
- Made threshold lengths configurable

**Key design decision:** Pure function (string in → reason or None) vs
Vibe-Trading's worker-coupled version with iteration state references.

---

## DAG Orchestrator → Vibe-Trading `SwarmRuntime`

**Source:** `swarm/runtime.py` + `swarm/task_store.py` in Vibe-Trading
**Lines in source:** ~800 combined
**Lines in kit:** ~290

**What Vibe-Trading does:**
Full DAG with file-based task persistence, event callbacks, ThreadPoolExecutor,
cancellation via threading Events, grounding pre-fetch, YAML-preset config.
Topological layering, `depends_on`/`input_from` for pipelining.

**What we changed:**
- Removed persistence — tasks live in memory
- Removed event callbacks — simpler return value
- Removed YAML presets — Python decorator API
- Switched ThreadPoolExecutor → asyncio.Semaphore
- Added `simple_chain()` for linear pipelines
- Added error isolation with downstream skip cascade
- Added `shared_context` for infrastructure injection

**Key design decision:** Lean programmatic use (caller wants results, not
observability). Tradeoff: no streaming progress or crash recovery, in exchange
for simplicity and zero boilerplate.

---

## Patterns Not Included (and why)

### Grounding Pre-fetch (Vibe-Trading `grounding.py`)
Pre-fetches OHLCV before agent runs to prevent hallucinated prices. Domain-
specific to financial data. Concept is universally useful but implementation
depends on market data loaders.

### Shadow Account Loop (Vibe-Trading `shadow_account/`)
Extracts implicit rules from broker exports and backtests. Novel idea but
deeply domain-specific. Not generalizable without a behavioral pattern
extraction framework.

### Event-Driven Browser (browser-use `BrowserSession`)
CDP-based browser control with bubus EventBus. Replaced by Hermes' native
browser stack (lightpanda/agent-browser).

### Message Compaction (browser-use `MessageManager`)
Summarizes older history into compact memory. Best at the agent framework
level (Hermes LCM handles this).
