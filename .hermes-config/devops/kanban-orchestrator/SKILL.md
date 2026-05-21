---
name: kanban-orchestrator
description: Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do the work yourself" rule and the basic lifecycle are auto-injected into every kanban worker's system prompt; this skill is the deeper playbook when you're specifically playing the orchestrator role.
version: 3.2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing]
    related_skills: [kanban-worker]
---

# Kanban Orchestrator — Decomposition Playbook

> The **core worker lifecycle** (including the `kanban_create` fan-out pattern and the "decompose, don't execute" rule) is auto-injected into every kanban process via the `KANBAN_GUIDANCE` system-prompt block. This skill is the deeper playbook when you're specifically playing the orchestrator role whose whole job is routing.
>
> **Reference available**: `references/multi-agent-topology-failure-modes.md` contains the production evidence, cascade infection rates, and MIT/Google scaling studies that back the topology-awareness section below. Load it for depth when a user asks about multi-agent architecture trade-offs.
>
> **Dashboard UI**: The kanban board has a dedicated drag-drop dashboard tab at the Dashboard's `/kanban` route. Enable it with `hermes plugins enable kanban/dashboard` — it's a bundled dashboard plugin (manifest.json + JS bundle, separate from regular plugins). If the user asks for a visual kanban UI or how to see their board in a browser, this is the answer: point them to the Dashboard + the kanban tab. The Dashboard itself (port 9119 by default, localhost-only unless proxied) also shows session history, logs, profiles, and cron — the full agent tracking surface.

## Profiles are user-configured — not a fixed roster

Hermes setups vary widely. Some users run a single profile that does everything; some run a small fleet (`docker-worker`, `cron-worker`); some run a curated specialist team they've named themselves. There is **no default specialist roster** — the orchestrator skill does not know what profiles exist on this machine.

Before fanning out, you must ground the decomposition in the profiles that actually exist. The dispatcher silently fails to spawn unknown assignee names — it doesn't autocorrect, doesn't suggest, doesn't fall back. So a card assigned to `researcher` on a setup that only has `docker-worker` just sits in `ready` forever.

**Step 0: discover available profiles before planning.**

Use one of these:

- `hermes profile list` — prints the table of profiles configured on this machine. Run it through your terminal tool if you have one; otherwise ask the user.
- `kanban_list(assignee="<some-name>")` — sanity-check a single name. Returns an empty list (rather than an error) for an unknown assignee, so this only confirms a name you're already considering.
- **Just ask the user.** "What profiles do you have set up?" is a fine first turn when the goal needs more than one specialist.

Cache the result in your working memory for the rest of the conversation. Re-asking every turn wastes a tool call.

## When to use the board (vs. just doing the work)

Create Kanban tasks when any of these are true:

1. **Multiple specialists are needed.** Research + analysis + writing is three profiles.
2. **The work should survive a crash or restart.** Long-running, recurring, or important.
3. **The user might want to interject.** Human-in-the-loop at any step.
4. **Multiple subtasks can run in parallel.** Fan-out for speed.
5. **Review / iteration is expected.** A reviewer profile loops on drafter output.
6. **The audit trail matters.** Board rows persist in SQLite forever.

If *none* of those apply — it's a small one-shot reasoning task — use `delegate_task` instead or answer the user directly.

## Multi-agent topology awareness: when the board helps and when it hurts

A kanban board is fundamentally a **persistence and handoff substrate** — it makes work survive agent boundaries, crashes, and restarts. But it is not a multi-agent architecture in itself. Mistaking the board for the architecture is the most common failure mode in systems that deploy kanban for agent teams.

### The board as observation layer, not specification

The most persistent critique of kanban-in-agent-systems comes from Will Allred (Lavender cofounder, 2026):

> *"You end up designing the columns and process first ('Research column → Synthesis column → Execution column'), then assigning agents to each stage. That constrains the system to predefined transitions instead of letting agents pursue goals with autonomy. The board becomes the spec, not an observation layer."*

The disciplined practice: **design the agent's autonomy first** (goal, tooling, memory, planning capability), then lay a kanban board *over* that process as a visibility layer for humans. The board should reflect what agents decided to do, not dictate what they may attempt.

### What the board is actually good at

Production evidence (Beam AI, 2026; Meta internal tools; Google 2026 scaling study) converges on a narrow but clear set of strengths:

| Strength | Why it works | Topology |
|---|---|---|
| **Durable cross-agent handoffs** | SQLite persistence survives crashes | Orchestrator-worker, Pipeline |
| **Human-in-the-loop gating** | Block/unblock with comment thread is first-class | Any topology |
| **Structured result handover** | `kanban_complete(summary, metadata)` creates parseable history | All |
| **Same-profile queuing** | Dispatcher serializes, profile accumulates memory | Sequential queue |
| **Long-running work that must survive restarts** | Board state is in SQLite, not in a chat context | All |

### What the board is bad at

The three most common failure topologies that kanban amplifies rather than solves:

1. **Tightly-coupled collaborative reasoning** (multi-agent debate, group chat). The board serializes handoffs; debate needs parallel message exchange with shared context. Board rows are too slow — participants wait for completions instead of conversing. **Use delegate_task or a group-chat framework instead.**

2. **Real-time error recovery with state rollback.** If agent A produces a bad output and agent B consumes it, you have a poisoned chain. The board doesn't offer rollback — only `kanban_block` with a comment asking for manual cleanup. **Use a pipeline evaluator at each stage gate instead.**

3. **High-frequency micro-tasks.** Every kanban transition costs at least one dispatcher claim cycle (~s). For sub-second task routing, the board's overhead dominates. **Use direct tool delegation or function calling instead.**

### The accuracy evidence that every orchestrator should know

The 2025-26 cascade studies are the strongest argument against treating the board as a multi-agent architecture:

- **LangGraph**: 9.7% leaf-node error → 100% hub infection when a single falsehood propagates
- **CrewAI**: 15.9% → 100% on the same cascade
- **Accuracy by pipeline depth**: 90.7% (1 stage) → 41.2% (2) → 22.5% (5) — *below random chance at 5 stages*
- **Prose relay vs. structured relay**: prose degrades 8.5 pts/stage; structured relay degrades 2.8 pts/stage
- **The one thing that saved it**: agents bringing in *new exogenous signals* (tool-augmented KB lookup) jumped accuracy from 24.3% to 82.7%

**Implication for the orchestrator**: Kanban handoffs should prefer structured metadata over prose summaries (the `metadata` dict in `kanban_complete`). Every unstructured handoff erodes ~3x more accuracy than a structured one. When a card's output is consumed by a downstream agent, ensure the downstream has access to the same source data — don't rely on the upstream's summary alone.

### Decision rule: board vs. other patterns

Before creating any cards, ask: *does this workstream benefit from the board's strengths (persistence, human gates, structured handoff), or does it need tight collaboration the board serializes into fragility?*

- **Independent parallel research → fan-out via kanban.** N cards, no parents. Works perfectly.
- **Sequential pipeline with human review → kanban with block/unblock.** Pipeline with gates.
- **Two agents that need to converse iteratively → delegate_task or group chat.** Board will kill velocity.
- **High-frequency micro-decisions → direct tool call, not a card.** Board overhead dominates.

## The anti-temptation rules

Your job description says "route, don't execute." The rules that enforce that:

- **Do not execute the work yourself.** Your restricted toolset usually doesn't even include terminal/file/code/web for implementation. If you find yourself "just fixing this quickly" — stop and create a task for the right specialist.
- **For any concrete task, create a Kanban task and assign it.** Every single time.
- **Split multi-lane requests before creating cards.** A user prompt can contain several independent workstreams. Extract those lanes first, then create one card per lane instead of bundling unrelated work into a single implementer card.
- **Run independent lanes in parallel.** If two cards do not need each other's output, leave them unlinked so the dispatcher can fan them out. Link only true data dependencies.
- **Never create dependent work as independent ready cards.** If a card must wait for another card, pass `parents=[...]` in the original `kanban_create` call. Do not create it first and link it later, and do not rely on prose like "wait for T1" inside the body.
- **If no specialist fits the available profiles, ask the user which profile to create or which existing profile to use.** Do not invent profile names; the dispatcher will silently drop unknown assignees.
- **Decompose, route, and summarize — that's the whole job.**

## Decomposition playbook

### Step 1 — Understand the goal

Ask clarifying questions if the goal is ambiguous. Cheap to ask; expensive to spawn the wrong fleet.

### Step 2 — Sketch the task graph

Before creating anything, draft the graph out loud (in your response to the user). Treat every concrete workstream as a candidate card:

1. Extract the lanes from the request.
2. Map each lane to one of the profiles you discovered in Step 0. If a lane doesn't fit any existing profile, ask the user which to use or create.
3. Decide whether each lane is independent or gated by another lane.
4. Create independent lanes as parallel cards with no parent links.
5. Create synthesis/review/integration cards with parent links to the lanes they depend on. A child created with unfinished parents starts in `todo`; the dispatcher promotes it to `ready` only after every parent is done.

Examples of prompts that should fan out (using placeholder profile names — substitute whatever exists on the user's setup):

- "Build an app" → one card to a design-oriented profile for product/UI direction, one or two cards to engineering profiles for implementation, plus a later integration/review card if the user has a reviewer profile.
- "Fix blockers and check model variants" → one implementation card for the blocker fixes plus one discovery/research card for config/source verification. A final reviewer card can depend on both.
- "Research docs and implement" → a docs-research card can run in parallel with a codebase-discovery card; implementation waits only if it truly needs those findings.
- "Analyze this screenshot and find the related code" → one card to a vision-capable profile for the visual analysis while another searches the codebase.

Words like "also," "finally," or "and" do not automatically imply a dependency. They often mean "make sure this is covered before reporting back." Only link tasks when one card cannot start until another card's output exists.

Show the graph to the user before creating cards. Let them correct it — including which actual profile name should own each lane.

### Step 3 — Create tasks and link

Use the profile names from Step 0. The example below uses placeholders `<profile-A>`, `<profile-B>`, `<profile-C>` — replace them with what the user actually has.

```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="<profile-A>",  # whichever profile handles research on this setup
    body="Compare estimated infrastructure costs, migration costs, and ongoing ops costs over a 3-year window. Sources: AWS/GCP pricing, team time estimates, current Postgres bills from peers.",
    tenant=os.environ.get("HERMES_TENANT"),
)["task_id"]

t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="<profile-A>",  # same profile, run in parallel
    body="Compare query latency, throughput, and scaling characteristics at our expected data volume (~500GB, 10k QPS peak). Sources: benchmark papers, public case studies, pgbench results if easy.",
)["task_id"]

t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="<profile-B>",  # whichever profile does synthesis/analysis
    body="Read the findings from T1 (cost) and T2 (performance). Produce a 1-page recommendation with explicit trade-offs and a go/no-go call.",
    parents=[t1, t2],
)["task_id"]

t4 = kanban_create(
    title="draft decision memo",
    assignee="<profile-C>",  # whichever profile drafts user-facing prose
    body="Turn the analyst's recommendation into a 2-page memo for the CTO. Match the tone of previous decision memos in the team's knowledge base.",
    parents=[t3],
)["task_id"]
```

`parents=[...]` gates promotion — children stay in `todo` until every parent reaches `done`, then auto-promote to `ready`. No manual coordination needed; the dispatcher and dependency engine handle it.

If the task graph has dependencies, create the parent cards first, capture their returned ids, and include those ids in the child card's `parents` list during the child `kanban_create` call. Avoid creating all cards in parallel and linking them afterward; that creates a window where the dispatcher can claim a child before its inputs exist.

### Step 4 — Complete your own task

If you were spawned as a task yourself (e.g. a planner profile was assigned `T0: "investigate Postgres migration"`), mark it done with a summary of what you created:

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 research lanes in parallel, 1 synthesis on their outputs, 1 prose draft on the recommendation",
    metadata={
        "task_graph": {
            "T1": {"assignee": "<profile-A>", "parents": []},
            "T2": {"assignee": "<profile-A>", "parents": []},
            "T3": {"assignee": "<profile-B>", "parents": ["T1", "T2"]},
            "T4": {"assignee": "<profile-C>", "parents": ["T3"]},
        },
    },
)
```

### Step 5 — Report back to the user

Tell them what you created in plain prose, naming the actual profiles you used:

> I've queued 4 tasks:
> - **T1** (`<profile-A>`): cost comparison
> - **T2** (`<profile-A>`): performance comparison, in parallel with T1
> - **T3** (`<profile-B>`): synthesizes T1 + T2 into a recommendation
> - **T4** (`<profile-C>`): turns T3 into a CTO memo
>
> The dispatcher will pick up T1 and T2 now. T3 starts when both finish. You'll get a gateway ping when T4 completes. Use the dashboard or `hermes kanban tail <id>` to follow along.

## The User-as-Orchestrator Model (Human-Gated Pipeline)

This is the pattern this user works with. It's the most failure-resistant topology for knowledge-work projects where quality is the constraint, not throughput.

### Core constraint: no agent-to-agent communication

The defining rule: **agents never hand off to each other.** Every worker delivers to a human reviewer (you). The human reviews, corrects, and decides where the output goes next. This caps the error chain at exactly one hop — the cascade research (2.8 pts/stage structured, 8.5 pts/stage prose) never compounds because it never goes agent-to-agent.

### The three-layer architecture

This user's book-project pipeline uses three distinct profile types, each with a different automation ceiling:

| Layer | Automation Ceiling | Why |
|-------|-------------------|-----|
| **Researcher** | High | Constrained task: find sources on X, extract relevant passages, return structured notes. Cheap model, narrow tool scope (search, extract, file read). |
| **Writer** | Medium-High | Constrained output: take approved synthesis, render in fixed register, produce prose. Needs supervision on nuance but the shape is predictable. |
| **Master Historian (collaborative synthesizer)** | Low | Synthesis across six domains requires pattern-recognition judgement current models don't reliably have — knowing when to privilege a counterintuitive connection over a conventional one. The historian works *with* the human, not for the human. |

### The workflow

```
You ──→ parallel research cards (politics, wars, institutions, actors, demographics)
           ↓
       Researcher profile claims each card
           ↓
       N structured dossiers → YOU review each
                 ↓
       Approve or send back individual cards
                 ↓
       Master Historian profile (collaborative with you)
       → synthesize, critique, connect themes
       → you read, challenge, refine together
                 ↓
       YOU decide the synthesis is solid
                 ↓
       Writer profile
       → chapter draft in defined register
                 ↓
       YOU review, markup, approve or return
```

**Critical**: the master historian writes nothing for the writer. It talks to *you*, in comments or direct conversation. Only you decide when the synthesis is solid enough to hand to the writer.

### Why the board matters here

This pipeline doesn't *need* a kanban board for coordination — the human is the coordination. But the board adds:

1. **Crash survival** — the card's state, outputs, and comments live in SQLite. If a worker crashes mid-research, the card reclaims and another worker picks up where the handoff left off.
2. **Structured handoffs** — `kanban_complete(metadata={sources, key_findings, confidence})` creates parseable history you can query later.
3. **Parallel fan-out** — six research cards on the board run concurrently. The dispatcher handles the parallelism; you just create the cards.
4. **Audit trail** — every block, comment, and completion is timestamped. Three months later you can see what the researcher found and what you asked them to redo.

### The ceiling finding (important)

The progressive escalation model (Level 1: single agent → Level 2: multiple profiles → Level 3: orchestrated team → Level 4: automated team) treats Level 4 as the natural endpoint. **The research says Level 3 is the ceiling, not a stepping stone.** Removing the human from the synthesis gate collapses accuracy below random chance at 5 stages (MIT Simchi-Levi: 90.7% → 22.5%). The human at every gate is not a bottleneck to be automated away — it's the quality guarantee that makes the rest of the pipeline viable.

Do not treat this as "Level 3 for now, Level 4 when the models improve." The cascade evidence implies Level 4 requires a fundamentally different reliability regime than current LLMs provide. Operate at Level 3 by design.

## Progressive escalation model (for reference)

This user saw a tweet (May 2026) that framed the path cleanly:

**Level 1 — main agent.** You + Hermes. Prototype area, test workflows, refine. Doubles as orchestrator until you have something worth breaking out.

**Level 2 — specialized agents.** Once a workflow is solid, break it into its own profile with its own credentials, memory, and scope. Profiles are *capabilities*, not permanent identities — a profile with search tools works on whatever research card it claims today, regardless of domain.

**Level 3 — orchestrated team.** Bring the human orchestrator back in. The human steers the profiles by creating cards, reviewing outputs, and deciding the next step.

**Level 4 — automated.** Cron and events fire jobs, the orchestrator routes them through the task bus, the team handles the work without the human.

The progression is correct as a *build-up strategy* — test at Level 1, extract at Level 2, orchestrate at Level 3. But Level 4 is not reliably achievable with current models for non-trivial creative or analytical work. The operative principle: if your output at Level 1 is mediocre, you are about to scale mediocrity. 20 agents shipping low-quality work at speed is worse than 3 shipping great work slowly.

## Common patterns

**Fan-out + fan-in (research → synthesize):** N research-style cards with no parents, one synthesis card with all of them as parents.

**Parallel implementation + validation:** one implementer card makes the change while one explorer/researcher card verifies config, docs, or source mapping. A reviewer card can depend on both. Do not make the implementer own unrelated verification just because the user mentioned both in one sentence.

**Pipeline with gates:** `planner → implementer → reviewer`. Each stage's `parents=[previous_task]`. Reviewer blocks or completes; if reviewer blocks, the operator unblocks with feedback and respawns.

**Same-profile queue:** N tasks, all assigned to the same profile, no dependencies between them. Dispatcher serializes — that profile processes them in priority order, accumulating experience in its own memory.

**Human-in-the-loop:** Any task can `kanban_block()` to wait for input. Dispatcher respawns after `/unblock`. The comment thread carries the full context.

## Pitfalls

**Inventing profile names that don't exist.** The dispatcher silently fails to spawn unknown assignees — the card just sits in `ready` forever. Always assign to a profile from your Step 0 discovery; ask the user if you're unsure.

**Bundling independent lanes into one card.** If the user asks for two independent outcomes, create two cards. Example: "fix blockers and check model variants" is not one fixer task; create a fixer/engineer card for the fixes and an explorer/researcher card for the variant check, then optionally gate review on both.

**Over-linking because of wording.** "Finally check X" may still be parallel with implementation if X is static config, docs, or source discovery. Link it after implementation only when the check depends on the implementation result.

**Forgetting dependency links.** If the task graph says `research -> implement -> review`, do not create all tasks as independent ready cards. Use parent links so implement/review cannot run before their inputs exist.

**Reassignment vs. new task.** If a reviewer blocks with "needs changes," create a NEW task linked from the reviewer's task — don't re-run the same task with a stern look. The new task is assigned to the original implementer profile.

**Argument order for links.** `kanban_link(parent_id=..., child_id=...)` — parent first. Mixing them up demotes the wrong task to `todo`.

**Don't pre-create the whole graph if the shape depends on intermediate findings.** If T3's structure depends on what T1 and T2 find, let T3 exist as a "synthesize findings" task whose own first step is to read parent handoffs and plan the rest. Orchestrators can spawn orchestrators.

**Tenant inheritance.** If `HERMES_TENANT` is set in your env, pass `tenant=os.environ.get("HERMES_TENANT")` on every `kanban_create` call so child tasks stay in the same namespace.

## Recovering stuck workers

When a worker profile keeps crashing, hallucinating, or getting blocked by its own mistakes (usually: wrong model, missing skill, broken credential), the kanban dashboard flags the task with a ⚠ badge and opens a **Recovery** section in the drawer. Three primary actions:

1. **Reclaim** (or `hermes kanban reclaim <task_id>`) — abort the running worker immediately and reset the task to `ready`. The existing claim TTL is ~15 min; this is the fast path out.
2. **Reassign** (or `hermes kanban reassign <task_id> <new-profile> --reclaim`) — switch the task to a different profile (one that exists on this setup) and let the dispatcher pick it up with a fresh worker.
3. **Change profile model** — the dashboard prints a copy-paste hint for `hermes -p <profile> model` since profile config lives on disk; edit it in a terminal, then Reclaim to retry with the new model.

Hallucination warnings appear on tasks where a worker's `kanban_complete(created_cards=[...])` claim included card ids that don't exist or weren't created by the worker's profile (the gate blocks the completion), or where the free-form summary references `t_<hex>` ids that don't resolve (advisory prose scan, non-blocking). Both produce audit events that persist even after recovery actions — the trail stays for debugging.
