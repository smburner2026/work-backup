# Cron Tool-Scoping Audit — Concrete Examples

Source: Hermes session reviewing Shann Holmberg's 9-step agent design framework against existing cron infrastructure. Result: 7 cron jobs scoped from full tool access down to minimal sets.

## Audit Method

1. List all cron jobs via `cronjob(action='list')`
2. Classify: no-agent script (shell/python, bypasses LLM) vs agent-driven (LLM-powered, uses tools)
3. For each agent-driven job: enumerate what the job actually does → map to toolset names → exclude everything else

## Classification Results

### No-Agent Scripts (no tool scoping needed — they just run a script)

| Cron | Type | Status |
|------|------|--------|
| work-backup | shell script, weekly | Left as-is |
| nightly-self-audit | shell script, daily | Left as-is |
| gbrain-dream-cycle | shell script, nightly | Left as-is |
| Daily flashcard briefing | python script, paused | Left as-is |
| Saturday flashcard kickoff | python script, one-shot | Left as-is |

### Agent-Driven Crons (scoped down)

#### Euphy Journal Jobs (4 crons)

**Jobs:** Euphy Daily/Weekly/Monthly Bullet Journal + Euphy Nightly Journal Prompt
**Skills:** `euphy-bullet-journal`, `euphy-personal-journal`
**What they do:** Generate a personal journal entry using the euphy skill, write/read journal files, check prior entries for continuity, deliver to Discord (handled by cron framework)
**Scoped to:** `terminal`, `file`, `memory`, `search`, `skills`
**Cut:** browser, web, cronjob, delegation, computer_use, image_gen, tts, vision, code_execution, messaging, todo
**Rationale:** Personal journaling needs file access (read/write entries), memory (recall patterns), search (find past entries), skills (load journal skill), terminal (may invoke local commands). No reason to browse the web, generate images, or spawn sub-agents for this task.

#### Nightly Self-Improvement Loop

**Skill:** `profile-compression`
**What it does:** Reviews recent sessions for user corrections, audits scripts/skills/configs, tidies work directories, commits findings to memory
**Scoped to:** `terminal`, `file`, `memory`, `search`, `skills`
**Cut:** browser, web, cronjob, delegation, computer_use, image_gen, tts, vision, code_execution, messaging, todo
**Rationale:** Self-improvement works with local state — files, memory, skills, session archives. Web access is not needed (audits are local). Browser and sub-agents would bloat the job's token budget.

#### DABT Weekly Truth Audit (already scoped — left as-is)

**Skills:** `dabt-database`, `dabt-reference`, `batch-data-enrichment`
**Scoped to:** `terminal`, `file`, `search`
**Note:** Already had least-privilege scope before this audit. Exemplar.

#### gbrain-dabt-maintenance

**What it does:** Runs G-Brain health checks (via MCP/terminal), logs results
**Scoped to:** `terminal`, `file`
**Cut:** Everything else (14+ toolsets removed)
**Rationale:** This is purely a maintenance script runner. It starts G-Brain, checks health, logs to file. Needs nothing else.

#### DABT Miss Journal Weekly Synthesis

**What it does:** Queries G-Brain for new miss journal entries, aggregates gaps, may cross-reference against external sources
**Scoped to:** `terminal`, `file`, `memory`, `search`, `web`
**Rationale:** G-Brain access via terminal, file for reading/writing synthesis output, memory/search for past patterns, web for optional external fact-checking. Browser and sub-agents would distract from the synthesis goal.

## Key Insights

1. **No cron needed `messaging`, `cronjob`, `browser`, or `delegation`** — the scheduler handles delivery, and none of the jobs needed to schedule other work, interact with live pages, or spawn sub-agents.
2. **`web` was only granted to one job** (miss journal synthesis) — the rest work entirely with local data. This is the most commonly over-granted toolset.
3. **`code_execution` was never needed** — all analysis was done via terminal commands (Python via MCP, shell scripts). The cron agent's own reasoning handles synthesis; it doesn't need to run inline Python.
4. **The user's heuristic is correct** — "worst case, turn it back on" makes the scoping decision reversible and low-risk. No job failed after scoping.

## Related

See the main SKILL.md "Least-Privilege Tool Scoping" section for general methodology and reference patterns.
