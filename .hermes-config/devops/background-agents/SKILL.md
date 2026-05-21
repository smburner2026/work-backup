---
name: background-agents
description: Using cronjob to spawn background autonomous agent sessions that run independently while the main conversation continues. For long-running web research, multi-file downloads, batch processing — anything that would block the conversation for >30 seconds or that the user might interrupt by sending a new message.
version: 1.0.0
---

# Background Agent Workflows

## When to Use

Spawn a background autonomous agent via cronjob when:

- **Long-running web research** — searching multiple mirrors, downloading files, iterating through paginated results
- **Multi-file downloads from external sources** — Anna's Archive, LibGen, Internet Archive, GitHub releases
- **Any task that takes >30 seconds** and would block the conversation
- **Tasks the user might interrupt** — cronjob runs in its own session, immune to user messages interrupting it
- **Batch processing** — converting, cleaning, or processing files in independent sessions

## Do NOT Use Background Agent When (use these instead)

| Method | When |
|--------|------|
| `terminal(background=true, notify_on_complete=true)` | Scriptable tasks with deterministic output — compilers, linters, test suites, file conversions |
| `delegate_task(tasks=[...])` | Reasoning-heavy tasks that must complete within the turn and return structured results |
| Direct tool calls | Single-file reads, writes, or simple web lookups under 10 seconds |

## Setup Parameters

```python
cronjob(
    action='create',
    name='Descriptive job name — <project>-<action>',
    schedule='1m',              # fires in 1 minute — minimum reliable delay
    repeat=1,                   # runs exactly once
    deliver='origin',           # reports back to the current conversation
    enabled_toolsets=['web','terminal','file'],  # restrict to only what's needed
    prompt='''Self-contained instructions. The agent has NO context of the main
conversation — spell out every file path, URL, ISBN, and constraint.
Include: goal (what to accomplish), context (where to search, what to find),
and expected output format (report what was found and what wasn't).'''
)
```

### Key Parameter Details

| Parameter | Value | Why |
|-----------|-------|-----|
| `schedule` | `'1m'` | Fires ~1 minute after creation. Don't use `'0m'` or `'0'` — not accepted. |
| `repeat` | `1` | One-shot execution. No recurring job. |
| `deliver` | `'origin'` | Auto-delivers back to the current chat. Omit for default behavior. |
| `enabled_toolsets` | minimal set | Dramatically reduces input token overhead and keeps the agent focused. Only include tools it actually needs. |
| `prompt` | full self-contained | Must be completely independent. The agent has zero context about the main conversation. |

## Workflow

1. **State the plan** — tell the user what you'll run in the background, what each agent will do
2. **Get explicit confirmation** — do NOT fire until the user says go (user has corrected this pattern: "You kinda got ahead of me")
3. **Create the cronjob** — use the parameters above
4. **Continue conversation** — the agent runs independently, reports back when done
5. **Verify output** — when the report arrives, check file paths and sizes before telling the user it's done

## Recurring Self-Maintenance Jobs

A separate class from one-shot background agents — these are **recurring cron jobs** that run on a schedule (daily, weekly) with no user present. Examples: nightly self-improvement, weekly audit, daily data digest.

### When to Use

- **Periodic self-improvement** — reviewing recent sessions for user corrections/preferences and committing to memory
- **Scheduled audits** — checking scripts, skills, configs, file paths, plugins for breakage
- **Recurring cleanup/tidy** — reorganising work directories, moving scattered files to staging
- **Any routine maintenance** that benefits from automatic detection rather than waiting for damage

### Key Design Differences vs One-Shot

| Aspect | One-Shot Background Agent | Recurring Self-Maintenance |
|--------|--------------------------|----------------------------|
| `repeat` | `1` | Omit (forever) or set to a count |
| `schedule` | `'1m'` (fires in 1 min) | `'0 6 * * *'` (cron expression) |
| Delivery | Reports back immediately | Reports on every run to origin |
| Prompt style | Task-specific goal | Multi-phase structured workflow |
| User presence | User may be online waiting | User is offline — report must be self-explanatory |

### Design Principles

1. **Phase-based structure** — Split the job into independent phases (e.g. assessment → audit → tidy). Each phase should be self-contained so a failure in one doesn't abort the rest.
2. **Threshold-gated reporting** — "Nothing notable" is a valid result. Don't create noise entries in memory or output when nothing changed.
3. **Safety-first tidy patterns** — When moving/reorganising files, use a staging pattern: `~/recycle-bin/YYYY-MM-DD/` with original path structure preserved. NEVER delete anything. Report what was moved and let the user review.
4. **Self-contained prompt** — The agent has zero context from any conversation. Every path, constraint, tool, and preference must be in the prompt. Include the user's voice/stance directive so the agent doesn't default to a bland tone.
5. **Phase summaries in output** — Deliver a structured report per phase so the user can quickly scan pass/fail across all categories.

### Parameters Pattern

```python
cronjob(
    action='create',
    name='<area>-self-improvement',
    schedule='0 6 * * *',        # daily at 6:00 UTC
    # repeat is omitted = forever
    deliver='origin',
    prompt='''# Phase 1: Assessment\n...\n# Phase 2: Audit\n...\n# Phase 3: Tidy\n...'''
)
```

### Prompt Template (Three-Phase)

Each phase in the prompt should be bracketed and **error-independent** — if assessment fails, audit and tidy still run. Include a constraint line like `"If a phase encounters an unexpected error, log it and continue. Do not abort the entire run."`

```
## Phase 1: Assessment
- Search sessions from last N hours using session_search()
- For each session, extract: corrections, preferences, environment facts, workflow patterns
- Save to memory only when genuinely NEW (threshold-gated). Do NOT create noise entries — if nothing notable was found, report "Nothing notable to commit."
- Report summary of what was saved

## Phase 2: Audit
- Check scripts (syntax: python -m py_compile .py, bash -n .sh)
- Check skills (YAML frontmatter validity — parse with yaml.safe_load, verify required name/description fields)
- Check config YAML structural integrity (parseable, required keys present)
- Check file paths from memory for existence (stat or path.exists())
- Check plugin/profile/soul structure (each profile dir needs config.yaml or SOUL.md)
- Check cron job schedules (cronjob action='list' — verify no expired/broken schedules)
- Check for broken symlinks in ~/.hermes
- Report pass/fail per category
- Report ALL findings — healthy AND broken, not just failures

## Phase 3: Tidy
- Scan work directories for scattered files: build artifacts, temps older than 7 days, orphaned logs, stray __pycache__ outside venvs, files in wrong directories
- Create staging dir: ~/recycle-bin/YYYY-MM-DD/
- Move misplaced files there, preserving original path structure
- NEVER delete anything — only move
- Skip: .env, config.yaml, .git/, node_modules/, venv/, .venv/, hidden dot files in home dir
- Report what was moved and why, or "All clean" if nothing
```

### Operational Constraints (baked into every recurring job prompt)

Add these as explicit lines near the top of the prompt to prevent common failure modes:

```
## Constraints
- You cannot use clarify() — no user present to answer questions
- You cannot use delegate_task() — subagents consume extra tokens; do it yourself
- If a phase encounters an unexpected error, log it and continue. Do not abort the entire run.
- Token budget: ~90 turns maximum. Be efficient — batch checks where possible.
- Verify your own output: if you claim a file was written or a config was changed, stat or read it back to confirm.
```

### Output Format

Specify the delivery format explicitly in the prompt so the user can quickly scan results:

```
## Output Format

Deliver your final summary with these sections:
- **📋 Assessment:** (what was saved or "Nothing new")
- **🔍 Audit:** (pass/fail per category, details on failures)
- **🗑️ Tidy:** (what was moved, or "All clean")

Use **bold** for section/category names, `code` for file paths. If everything passed, say "All clear."
```

### Pitfalls

- **No_agent mode is wrong for this** — These jobs need reasoning and tool selection. Use the default LLM-driven mode, not `no_agent=True`.
- **Overly broad enabled_toolsets** — A maintenance job typically needs `terminal`, `file`, `search`, `session_search`, and `memory`. Don't include `web`, `browser`, or `vision` unless actually needed for the audit scope.
- **Recursive scheduling** — Don't have a maintenance cron job create other cron jobs or modify its own schedule. The cron infrastructure handles that.
- **Compression/outcome fatigue** — If the job reports "nothing changed" every day, the user stops reading it. Design the prompt to flag only material changes and use a terse "All clear" for routine passes.
- **Threshold-gating** — "Search sessions → extract items → check if genuinely new → save only if non-empty" is the correct flow. Saving every day with "nothing notable" trains the user to ignore reports. A section that says "Nothing notable to commit" as a positive statement (not an error) keeps the report useful.
- **Error independence** — A failure in Phase 1 must not prevent Phase 2 from running. Use sequential try/except framing in the prompt ("if Phase 1 fails, continue to Phase 2"). The user gets a partial report instead of a dead job.

## Example: Sourcing Copyrighted Translations

```
# Research which editions are needed → compile ISBNs and translator names
# Present plan to user → get confirmation → fire as background cronjob

cronjob(
    action='create',
    name='Nietzsche sourcing — Batch 1',
    schedule='1m',
    repeat=1,
    deliver='origin',
    enabled_toolsets=['web', 'terminal', 'file'],
    prompt=f'''Search Anna's Archive, LibGen, and Internet Archive for:
    - Work (tr. Translator, Publisher, YEAR) — ISBN XXXXX
    ...'''
)
```

For multiple independent batches, create multiple cronjobs — they fire independently and deliver separate reports. This is better than one monolithic prompt because each agent runs in isolation and failure in one doesn't block the others.

## Pitfalls

- **No recursive scheduling** — Do NOT use cronjob within a cronjob session. The tool blocks it but don't design for it.
- **Completely self-contained prompts** — No context from the main conversation is carried over. Every file path, search term, ISBN, and constraint must be in the prompt.
- **Schedule minimum 1m** — Trying `'0m'` or blank schedule fails. The 1-minute delay is the minimum.
- **Tool restriction saves tokens** — A background agent doing web research doesn't need `terminal` (or might need it for downloads). Be precise about `enabled_toolsets` — removing unused tools can cut input tokens by 30-50%.
- **No user interaction** — Background cronjob sessions cannot use `clarify` or `send_message` (beyond delivering the final output to origin). The prompt must be complete enough that the agent never needs to ask a question.
- **Each cronjob is a fresh session** — all state resets between runs. If you need state, write files to disk and read them next time.
- **Multiple batches run concurrently** — Two cronjobs both set to `schedule='1m'` fire roughly simultaneously. Reports arrive independently as each finishes.
- **Check output files** — The agent self-reports "downloaded successfully" but the actual file may be truncated or in a wrong format. Verify file sizes and page counts before reporting completion.
