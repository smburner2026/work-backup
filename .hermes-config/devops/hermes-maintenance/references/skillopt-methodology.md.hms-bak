# SkillOpt Methodology — Reference

Microsoft Research papers on optimizing LLM instructions through execution testing, not text evaluation. User intends to apply to extraction pipelines and backtesting/research pipelines.

## Papers

- **SkillOpt** (arXiv 2605.23904, May 2026) — The optimizer. 52/52 settings improved across 7 models, 6 benchmarks, 3 harnesses.
- **SkillLens** (arXiv 2605.23899, May 2026) — The diagnostic. Proves reading skills to judge quality is worse than random.

## Core Insight

**Don't evaluate instructions by reading them — evaluate by execution.** LLM judges picking "better" skills by reading: 46.4% accuracy (worse than coin flip). On high-utility-gap pairs: 15.8% (actively inverted).

## The Pipeline (6 phases)

1. **Rollout** — Execute current skill against training tasks, collect trajectories
2. **Reflect** — Batch-review trajectories, identify systematic failure patterns
3. **Propose** — Generate 1-4 bounded edits (add/replace/delete) with rationale
4. **Validate** — Test each edit on **held-out validation tasks** (distinct from training). Accept only if pass rate maintained + weighted score not regressed
5. **Merge** — Apply accepted edits, run post-merge validation
6. **Slow/Meta** — Every 4 epochs, analyze rejected-edit buffer for meta-patterns

## Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| Train/val separation | Non-negotiable. 3+ distinct tasks each minimum |
| Bounded edits | Acts as "learning rate" — Lt=4 outperforms Lt=1 and Lt=16 |
| Validation gate | Hard pass/fail + weighted multi-objective score |
| Rejected-edit buffer | Negative feedback prevents repeating failed changes |
| Slow/meta update | Long-term lessons across epochs (momentum analog) |

## Multi-Objective Validation Metrics (default weights)

- `pass_rate: 0.55` — primary gate
- `quality_score: 0.30`
- `speed_score: 0.10`
- `token_efficiency: 0.05`

## What Makes Skills Effective (from SkillLens)

High-utility skills contained:
1. **Concrete failure mechanisms** — *why* agents fail, not just *that* they fail
2. **Actionable specificity** — step-level procedures referencing domain objects/tools
3. **High-risk action blacklist** — forbids specific harmful actions

Low-utility skills offered generic procedural advice.

## Generalizable Applications

The methodology applies to **any natural language instruction that shapes LLM behavior**:

| Domain | Applicability | Notes |
|--------|--------------|-------|
| Agent skills/procedures | ✅ Direct | What papers tested |
| System prompts | ✅ Yes | Same mechanism — text shapes behavior |
| Tool-use instructions | ✅ Yes | Tested on BFCL-v4 |
| Chain-of-thought templates | ✅ Yes | Procedural reasoning instructions |
| Extraction prompts | ✅ Yes | User's primary use case |
| Backtesting pipelines | ✅ Yes | If measurable outcomes defined |
| Safety guardrails | ✅ Yes | High-stakes extraction |
| Creative writing prompts | ⚠️ Weak | Harder to define pass/fail |

## Setup for Extraction Pipelines

When applying to extraction work:
1. Define ground truth for 3+ training examples
2. Define ground truth for 3+ validation examples (different data)
3. Score: precision/recall of extracted entities against ground truth
4. Run bounded edits (1-4 per epoch) with validation gate
5. Accept only edits that maintain or improve extraction quality

## Implementation Notes

- This pipeline can be implemented with custom scripts
- Community repo (magnus919/hermes-SkillOpt) is a kanban-based wrapper — not needed with built-in
- Final optimized skills: 379-1,995 tokens, from only 1-4 accepted edits
- Cross-model transfer works (optimize for one model, helps others)
