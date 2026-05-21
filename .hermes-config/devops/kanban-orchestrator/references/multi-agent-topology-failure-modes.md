# Multi-Agent Topology Failure Modes — Research Summary

> Compiled May 2026 from production postmortems, academic papers, and framework audits. Use this as depth context when the orchestrator skill's topology-awareness section needs evidence backing.

## The Six Production Patterns (Beam AI, Apr 2026)

| # | Pattern | Structure | Dominant Failure | Use Case |
|---|---------|-----------|-----------------|----------|
| 1 | Orchestrator-worker | Central decompose/delegate/aggregate | Context window overflow at 4+ workers; cost explosion ($0.50 test → $50K/month at 100K runs) | Customer service routing, cross-functional workflows |
| 2 | Sequential Pipeline | Deterministic linear chain | Error propagation (no backtracking); 950ms coordination overhead vs 500ms actual work; 3x token cost vs single agent | Document processing, contract generation |
| 3 | Fan-out / Fan-in | N parallel agents, collector aggregates | Quadratic race conditions N(N-1)/2 (5 agents=10 conflicts, 10 agents=45); aggregation hallucination (LLM invents consensus) | Multi-perspective analysis, concurrent code review |
| 4 | Multi-agent Debate | Shared conversation, challenge/refine | Non-convergence; sycophancy cascade (agents agree with majority even when wrong); Microsoft recommends max 3 agents | Maker-checker loops |
| 5 | Dynamic Handoff | No central coordinator, each agent decides to handle or pass | Infinite handoff loops (#1 failure mode); context loss compounds on each transfer | Customer support (unknown expertise path) |
| 6 | Swarm | Decentralized emergent coordination | Lowest observability; highest token cost; zero blame assignment; consensus inertia | Romantic-but-fragile; survives only as bounded subroutine with arbiter |

## Cascade Infection Rates (2025-26 Multi-Framework Study)

Analysis of 5 frameworks across 150+ tasks. Identified 14 distinct failure modes. Single falsehood cascade rates:

| Topology | Leaf Failure | Hub Failure |
|----------|-------------|-------------|
| LangGraph | 9.7% | 100% |
| CrewAI | 15.9% | 100% |
| MetaGPT | (extended) | Near-saturating |
| AutoGen | (extended) | Near-saturating |
| LangChain chains | 89.2% (cross-topology) | N/A |

**Defense**: Governance layer pushed resistance from 0.32 to >0.89, with safety overhead costs.

**ChatDev ProgramDev fix**: topology redesign improved 25% → 40.6% — still far below production tolerance.

## MIT Decision Theory Result (Simchi-Levi et al., 2025-26)

**Core finding**: *Without new exogenous signals, any delegated acyclic network is decision-theoretically dominated by a centralized Bayes decision maker looking at the same information.*

**Accuracy collapse by pipeline depth:**
- 90.7% (1 stage) → 41.2% (2) → 43.5% (3) → 22.5% (5) — *below 25% chance baseline at 5 stages*

**Relay degradation rates:**
- Structured relay: degraded 2.8 pts/stage
- Prose relay: degraded 8.5 pts/stage

**When new information was added** (tool-augmented KB lookup): jumped 24.3% → 82.7%

**Implication**: Multi-agent only wins when each agent accesses a *different external data source*. Managers summarizing subordinates who see the same data loses information.

## Google 2026 Scaling Study

180 configurations across 5 architectures:

- Centralized coordination improved Finance-Agent 80.9% on parallel work
- On sequential planning tasks, **every** multi-agent variant degraded performance 39-70%
- Independent systems amplified errors 17.2x; centralized contained them to 4.4x
- **Architecture matters, but task shape matters more.**

## What Survived Production (Micheal Lanham, Apr 2026)

### Flow (alive and well)
- Meta Ranking Engineer Agent: validation → combination → exploitation. Doubled average model accuracy across 6 models. 2 engineers per model → 3 engineers across 8 models.
- Meta tribal-knowledge precompute: 50+ specialized agents (explorers, analysts, writers, critics, fixers, testers, gap-fillers) building 59 durable knowledge objects.

### Orchestration (the default — fragile at scale)
- Central hub fragility: one bad routing decision cascades everywhere
- Central paraphrase loss as supervisor compresses output

### Collaboration (most romantic, least durable)
- Survives only as bounded subroutine with hidden selectors, phase gates, or final arbiter

### Comparison Chart

| Dimension | Flow | Orchestration | Collaboration |
|-----------|------|---------------|---------------|
| Observability | Highest | High | Lowest |
| Engineering Ambiguity | Low | Medium | Highest |
| Token Cost | Moderate | Moderate-High | Highest |
| Blame Assignment | Easy | Moderate | Impossible |
| Scale Pattern | Stage boundaries | Domain routing | None |

## Key Sources

- Beam AI, "6 Multi-Agent Orchestration Patterns That Actually Work in Production" (Apr 2026)
- Micheal Lanham, "Multi-Agent in Production in 2026: What Actually Survived" (Medium, Apr 2026)
- "From Spark to Fire" cascade paper (2025-26) — multi-framework failure propagation study
- Simchi-Levi et al. (MIT, 2025-26) — decision-theoretic limits of delegation networks
- Google 2026 Scaling Study — 180 configurations, 5 architectures
- Will Allred (@WillAllred117) — kanban-as-observation-layer critique, May 2026
- Microsoft group-chat recommendations (max 3 agents per conversation)
