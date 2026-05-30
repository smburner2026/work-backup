---
name: project-outcome-chaining
description: Link cross-session project memories by OUTCOME not just raw facts. Trace what decisions led to what results across sessions. Store relationship edges + outcome triples so the agent can traverse "how did we get from X to Y" queries.
---

# Project Outcome Chaining

Build a graph of cross-session project outcomes so you (and the agent) can traverse "what did we try, what happened, what did it lead to" across all sessions for a given project.

## When to use

- After completing a significant analysis session (trading research, code debugging, data pipeline)
- When you find yourself asking "what did session X conclude about Y"
- When a project spans multiple days/sessions and outcomes compound
- At natural pause points: a finding landed, a hypothesis disproved, a deliverable produced

## The Pattern

### Step 1: Consolidate the session outcome

At the end of each significant session (or at key pause points), store a memory with `scope='global'` and `source='analysis'` (or whatever project category) containing:

- WHAT was tried/explored
- OUTCOME: definitive result (positive, negative, inconclusive)
- IMPLICATION: what this means for next steps
- FILES/ARTIFACTS: what was produced or modified

```
mnemosyne_remember(
    content="PROJECT X — SESSION OUTCOME:\nWHAT: [what was tested/explored]\nOUTCOME: [verifiable result with numbers if applicable]\nIMPLICATION: [how this affects direction]\nARTIFACTS: [files, scripts, data produced]",
    source="analysis",
    scope="global",
    extraction=True,
    importance=0.9
)
```

### Step 2: Create temporal triples for outcomes

For each definitive finding, store a triple that captures the outcome:

```
mnemosyne_triple_add(
    subject="approach_or_experiment_name",
    predicate="outcome",
    object="the_verifiable_result"
)
```

Common predicates for outcome chaining:
- `led_to` — A's discovery enabled B's approach
- `informed` — A's results shaped B's design
- `supersedes` — B replaces A as the better approach
- `feeds_into` — A's output is input for B
- `contradicted` — B disproved A's hypothesis
- `built_on` — B uses A's methodology/data
- `produced` — A generated artifact B
- `blocked_by` — A couldn't progress because of B
- `unresolved` — A's question remains open after B

### Step 3: Link the memory nodes

Use `mnemosyne_graph_link()` to connect concrete memory IDs with relationship edges:

```
mnemosyne_graph_link(
    source_id="<memory_id_of_approach_A>",
    target_id="<memory_id_of_approach_B>",
    relationship="led_to" | "informed" | "supersedes" | etc,
    weight=0.8  # 0.0-1.0 confidence in the relationship
)
```

### Step 4: Add cross-cutting consolidated state

Store a "project state" memory that links TO all individual outcomes and FROM the previous consolidated state:

```
mnemosyne_remember(
    content="PROJECT X — CONSOLIDATED STATE:\n- Best approach: [current best result]\n- Dead ends: [what was ruled out]\n- Open questions: [what remains unknown]\n- Next likely direction: [recommended path]",
    source="analysis",
    scope="global",
    importance=0.95
)
```

Then link it to the individual outcome nodes.

### Step 5: Traverse

To query outcomes later, use mnemosyne_graph_query() from any seed memory:

```
mnemosyne_graph_query(seed_memory_id="<consolidated_state_id>", max_hops=2)
```

Or combine with mnemosyne_recall() for natural language entry points.

## Example patterns

**Trading research pattern:**
```
A_hypothesis → outcome(KS=0.270 significant) → led_to → B_hypothesis
                                                                  ↓
                                                      outcome(no improvement, F1 0.373)
                                                                  ↓
                                                      informed → C_approach → outcome(structural diff proven)
```

**Content pipeline pattern:**
```
method_v1 → outcome(truncation bug) → supersedes → method_v2 → outcome(37 clean .md files)
                                                               ↓
                                                       feeds_into → PDF_generation → 1 compiled book
                                                                                        ↓
                                                                                produced → Hermes_skill
```

## Pitfalls

- **Don't link temporary states** — only link definitive outcomes. A "hmm that's interesting" mid-session observation should not get a graph edge.
- **Use `supersedes` for approach pivots**, not `contradicted`. If you replaced method A with method B because B is better (not because A was wrong), use `supersedes`.
- **Weights** — 0.9 for direct causality (A's output was B's input), 0.7 for influence (A informed B's design but wasn't required), 0.5 for weak correlation.
- **Graph query is breadcrumbs, not a replacement for recall** — use graph entries to jump into the right memory, then mnemosyne_recall for full context.
- **Clean up stale links** — if a later finding supersedes an earlier outcome-pair, supersede the link too (invalidate old triple, add new one).
