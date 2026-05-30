# Open vs Closed Specialist Agents

An architectural pattern for structuring autonomous agent work. Relevant whenever designing how Hermes interacts with subagents, scheduled tasks, or vertical workflows.

## The Pattern

**Two categories of specialist agents, differentiated by repeatability:**

### 1. Open Specialists
Flexible, conversational agents for dynamic/unstructured work. You steer, back-and-forth, change direction mid-stream.

Examples (domain-agnostic):
- Coding agent when building/debugging exploratory code
- Research agent when the question is still fuzzy
- Creative agent when exploring directions
- Writing/analysis agent when iterating on structure

**Workflow:** Not rigid. Go back and forth, ask follow-ups, change direction mid-stream. It's like working with a smart teammate who knows the domain but needs guidance on the specific path.

**Hermes mapping:** Direct interaction. The agent uses tools, loads skills, iterates with the user. No fixed pipeline.

### 2. Closed (End-to-End) Specialists
Repeatable workflows with dedicated model, dedicated context, and a clear process. They know the steps, the standards, and what "done" looks like. Trigger manually or schedule as recurring tasks.

Examples (domain-agnostic):
- Weekly literature digest / competitor analysis
- Automated report generation (analytics, metrics, QA)
- Content repurposing pipeline
- Data enrichment / batch processing workflow
- Code review or bug-triage automation

**Workflow:** Deterministic. Same inputs → same process → same output shape every time. Designed for reliability, not creativity.

**Hermes mapping:** cron jobs + skills + model overrides. `cronjob(action='create', schedule='weekly', prompt='...', skills=['skill-name'], model='provider/model')`.

## The Graduation Pattern

**Most useful open specialists eventually become closed specialists.**

The lifecycle:
1. Run the workflow dynamically (open mode) — iterate, adjust, find the shape
2. Once the shape stabilizes, lock it in as a repeatable agent (closed mode)
3. The closed version runs the same way every time, freeing attention for new open work

This is the natural maturation path. Don't try to build a closed specialist from scratch — run it open first, discover the steps, then codify.

## Domain-Blind Generalization

The pattern is universal; the examples are not. An AI marketer will give marketing examples (SEO articles, lead enrichment, landing page QA). A bioscientist would instantiate the same pattern differently (literature synthesis pipelines, assay QC reports, grant-writing pre-screening).

**The floor plan is the abstraction. The furniture is the local binding.**

When evaluating any framework that uses this pattern, strip the examples and test whether the abstraction survives into your domain. It's the architecture that transfers, not the instantiation.

## Why This Matters for the Orchestrator

Hermes is the orchestrator layer. It:
- Knows the user and their workflows
- Routes work to the right specialist (open conversation or closed cron job)
- Verifies outputs and surfaces anomalies
- Reports back with synthesis, not raw data
- Does NOT need to be the one doing every task

The orchestrator's job is reducing the user's cognitive load — making the choice of "which agent handles this" invisible. The user says "fix the landing page" or "run this week's analysis" and Hermes determines whether that's an open conversation, a scheduled task, or a delegation to a subagent.