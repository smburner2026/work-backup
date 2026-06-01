---
name: workflow-pattern-kit
description: "Reusable agent workflow architecture: tool registry, loop detection, output contract gates, and DAG task orchestration."
version: 1.1.0
author: Hermes Agent
tags: [patterns, architecture, orchestration, tools, agents]
related_skills: [engineering-discipline]
platforms: [linux, macos]
python:
  path: python/
  module: workflow_pattern_kit
prerequisites:
  python:
    - pydantic>=2.0
---

# Workflow Pattern Kit

Four reusable patterns for building reliable agent workflows, extracted from browser-use and Vibe-Trading.

## Modules

### 1. ToolRegistry (`python/tool_registry.py`)

Typed action registration with context injection. Actions declare Pydantic params; shared context (browser_session, file_system, etc.) is auto-injected.

```python
from workflow_pattern_kit import ToolRegistry
from pydantic import BaseModel

registry = ToolRegistry()

class SearchParams(BaseModel):
    query: str
    limit: int = 5

@registry.action("Search the web", param_model=SearchParams)
async def search(params: SearchParams, browser_session=None):
    # browser_session auto-injected; params.query from LLM
    return await browser_session.navigate(f"https://google.com/search?q={params.query}")

# LLM sees:
print(registry.get_prompt_description())
# → search(query: str, limit: int = 5) — Search the web

# Execute:
result = await registry.execute("search", {"query": "NVDA stock"})
```

**Key features:**
- Auto-builds Pydantic models from function signatures (Type 1: BaseModel param; Type 2: flat individual params)
- Domain filtering: `@registry.action(..., domain_filter="github.com")` — only shows on matching pages
- Exclude actions: `registry.exclude_action("dangerous_op")`
- Async + sync support
- Context injection: `file_system`, `browser_session`, `page_url`, etc. auto-injected by the registry — tools never import infrastructure

### 2. LoopDetector (`python/loop_detector.py`)

Tracks action repetition and page stagnation. Emits escalating nudges (never hard-blocks).

```python
from workflow_pattern_kit import LoopDetector

detector = LoopDetector(window_size=20)

# After each action:
detector.record_action("click", {"index": 3})
detector.record_action("search", {"query": "NVDA stock"})
detector.record_page_state(url="...", dom_text="...", element_count=42)

# Before next LLM call:
nudge = detector.get_nudge_message(tick=step_number)
if nudge:
    print(f"Nudge: {nudge}")
    # → "You have repeated a similar action 8 times..."
```

**Nudge levels:**
- 5x repeat: mild "are you still making progress?"
- 8x repeat: stronger "try a different approach"
- 12x repeat: "try something fundamentally different"
- 5x stagnant pages: "page hasn't changed — try a different element"
- 3-step cooldown between nudges prevents spam

### 3. OutputGate (`python/output_gate.py`)

Classifies agent output as valid deliverable vs. plan stub/fabrication/raw tool output.

```python
from workflow_pattern_kit import OutputGate

gate = OutputGate()

reason = gate.check_deliverable(
    summary=agent_output_text,
    is_data_agent=True,       # Has data-fetching tools
    report_written=True,      # Wrote a final file
    data_tool_calls=5,        # Called data tools
)
if reason:
    print(f"Rejected: {reason}")  # Send back for retry
else:
    print("Accepted")             # Proceed
```

**Rejection reasons:**
- `empty deliverable` — nothing produced
- `unparsed tool-call markup` — LLM output contained raw tool call syntax
- `explicitly fabricated or mock data` — "without actual data" markers
- `raw tool-result envelope` — returned JSON blob instead of analyzing it
- `plan-only stub` — described a plan instead of executing it
- `data agent with no evidence` — has tools but didn't use them

### 4. DAG Orchestrator (`python/dag_orchestrator.py`)

Task dependency graph with topological layering. Tasks in the same layer run in parallel; layers run in dependency order.

```python
from workflow_pattern_kit import DAG

dag = DAG(max_concurrency=4)

@dag.task(depends_on=[])
async def fetch_macro():
    return {"gdp": "2.1%", "cpi": "3.2%"}

@dag.task(depends_on=["fetch_macro"], input_from={"macro": "fetch_macro"})
async def analyze_sector(macro):
    print(macro["gdp"])  # "2.1%"
    return {"sector": "tech"}

@dag.task(depends_on=["analyze_sector"])
async def generate_report(sector, ctx):
    return {"report": f"Sector: {sector['sector']}"}

# Run everything in order
result = await dag.run()
print(result.all_succeeded)  # True
print(result.output("analyze_sector"))
```

**For linear chains, use the shortcut:**
```python
from workflow_pattern_kit import simple_chain
dag = simple_chain(fetch_macro, analyze_sector, generate_report)
result = await dag.run()
```

---

## Immediate Workflows

### A: Kanban Task Quality Gate
Before accepting a Kanban worker's output, run it through the OutputGate.
The `kanban-worker` skill now includes this as a pre-completion step.

```
[Worker] → [OutputGate.check_deliverable()] → (pass) → Mark card done
                                           → (fail) → Return to worker with reason
```

### B: Parallel Research Pipeline
Parallel fetch tasks feeding into a synthesis task. DAG makes trivial what was serial before.

```
Layer 0: fetch-topic-a ────┐
          fetch-topic-b ────┤ parallel
          fetch-topic-c ────┘
Layer 1: synthesize ←── all three merged
```

### C: Browser Agent with Loop Detection
ToolRegistry + LoopDetector together. Detector catches stuck loops before they burn the budget.

### D: Multi-Step OCR Pipeline
`simple_chain(ocr, clean, translate, compile)` with per-step error isolation.

### E: Dual-Agent Review Loop
One agent drafts, another reviews. OutputGate validates both produce real evidence.

### F: Cron Job with Deliverable QA
Unattended scheduled tasks use OutputGate to catch stubs and trigger retry.

---

## Verification

```bash
# Run the stress test from the skill root:
python3 scripts/stress_test.py

# Or test each module individually:
python3 -c "
import asyncio
from workflow_pattern_kit import ToolRegistry, LoopDetector, OutputGate, DAG
# ... (see scripts/stress_test.py for the full test)
"
```

## Pitfalls

- **ToolRegistry** — Context injection requires `injected_context` dict at execution time. Without it, handlers get default values. Always pass what the handler needs.
- **LoopDetector** — Nudges are advice, not commands. Agents can ignore them. That's by design — form filling legitimately needs 20 similar clicks.
- **OutputGate** — Checks the *final* output text. If your agent writes to a file and only says "done," pass `report_written=True`.
- **DAG** — Same-layer tasks MUST be independent. Use `shared_context` for coordination — it's the only thread-safe shared state.
- **DAG error handling** — When a task fails, downstream tasks that depend on it are skipped. Independent chains continue unaffected.

## Reference Files

- `references/upstream-patterns.md` — detailed origins, architectural decisions, and differences from the upstream projects (browser-use, Vibe-Trading) for each pattern.

## Scripts

- `scripts/stress_test.py` — end-to-end verification that exercises all 4 modules (OCR pipeline simulation, OutputGate bad-output detection, DAG error isolation, LoopDetector). Run from skill root: `python3 scripts/stress_test.py`
