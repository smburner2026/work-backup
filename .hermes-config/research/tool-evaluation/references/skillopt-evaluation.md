# SkillOpt Community Repo Evaluation (2026-06-04)

## What was evaluated
- **Repo:** https://github.com/magnus919/hermes-SkillOpt
- **Claim:** Controlled skill optimization pipeline derived from Microsoft Research's SkillOpt paper (arXiv 2605.23904)
- **User question:** "Is this useful? Let's research and see if it applies for general use."

## Phase 1-2: Surface + Depth
- Well-structured repo: SKILL.md, scripts/, references/, templates/
- MIT license, single contributor
- Claims: 52/52 settings improved across 7 models, 6 benchmarks, 3 harnesses
- Source papers verified: SkillOpt (arXiv 2605.23904) and SkillLens (arXiv 2605.23899) — both Microsoft Research, May 2026

## Phase 3: Compatibility (existing stack overlap)
**Built-in SkillOpt already covers this:**
- Native, database-backed, supports dry-run, epoch/batch/lr tuning
- Community repo is a kanban-based orchestration wrapper around the same methodology
- Verdict: **Redundant as a tool** — the built-in is more efficient

## Phase 4: Research value (the general-use question)
The methodology generalizes beyond "Hermes skills" to **any natural language instruction that shapes LLM behavior**:

### SkillLens key findings (the diagnostic paper)
- LLM judges evaluating skills by reading: **46.4% accuracy** (worse than coin flip)
- On high-utility-gap pairs: **15.8%** (actively inverted)
- Format (list vs checklist vs prose): **no significant effect** (p > 0.34)
- High-utility skills: concrete failure mechanisms + actionable remedies
- Low-utility skills: generic procedural advice
- Skills hurt performance in **25% of cases** (negative transfer)

### SkillOpt key findings (the optimizer)
- Treats skill editing as gradient descent analog: bounded edits + validation gate
- 52/52 improvements, gains up to +39 points
- Final skills: 379–1,995 tokens, from 1–4 accepted edits
- Cross-model transfer works (optimize for GPT-5.4 → helps Qwen3.5-9B)
- Cross-harness transfer works (Codex → Claude Code)

### Generalizable principles for prompt/instruction optimization
1. **Don't evaluate prompts by reading them** — test on real tasks
2. **Failure encoding > success description** — "when X fails because Y, do Z" outperforms "do A, then B, then C"
3. **Bounded edits beat wholesale rewrites** — 1–4 changes per iteration with validation
4. **25% negative transfer is real** — validation gates catch this
5. **Format doesn't matter, content does** — markdown structure didn't predict utility

### Where it applies
- Agent skills/procedures ✅ (direct)
- System prompts ✅ (same mechanism)
- Tool-use instructions ✅ (tested on tool-calling benchmarks)
- Chain-of-thought templates ✅ (procedural instructions for reasoning)
- Few-shot examples ⚠️ (partial — different structure)
- Safety guardrails ✅ (explicitly mentioned)
- Creative writing prompts ⚠️ (weak — hard to define pass/fail)

## Verdict
- **As a tool:** NO-GO — built-in SkillOpt is better
- **As research methodology:** Valuable — applicable to extraction pipelines, backtesting, any prompt optimization with measurable outcomes
- **Papers worth bookmarking:** SkillOpt (2605.23904) and SkillLens (2605.23899)
