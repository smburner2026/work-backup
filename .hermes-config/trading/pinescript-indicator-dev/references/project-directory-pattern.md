# Project Directory Snapshot Pattern

When the user plans to move work to a new machine, do offline analysis, or wants a clean context reset, create a project directory that a fresh Hermes agent can pick up without chat history.

## Structure

```
project-name/
├── README.md                 # Current state, confirmed facts, unresolved questions
├── prompts/
│   └── resume.md             # Directive prompt for the new agent
├── data/                     # All CSVs, exports, reference data
├── pinescript/               # All .pine files (indicator, strategy, variants)
├── scripts/                  # Python backtesters, sweep scripts (if any)
└── docs/                     # Setup guides, methodology notes
```

## README.md Template

```markdown
# Project Name

## Overview
One sentence on the project goal.

## Status
What's confirmed, what's unknown, what's next.

## Confirmed Facts
Bullet list — each fact attributed (chart test, compile error, user confirmed).

## File Inventory
Table of key files and what they contain.

## What We Know About X
Current best theory, evidence for/against.

## Brute-Force Plan (if applicable)
Filter space, sweep ranges, success criteria.

## Next Steps
Ordered list.
```

## resume.md Template

```markdown
# Resume: Project Name

You are resuming a project to [GOAL].

## Your task
[DIRECTIVE — what the agent should do]

## The data
List of files, what each contains, how to use them.

## Known facts
Bullet list of confirmed facts — anchor the agent against rediscovery.

## The search/problem space
Parameters to sweep, ranges, success criteria.

## Output
What format, what metrics, what files to produce.

## Important constraints
- No internet needed
- Do NOT propose [DISPROVEN THEORY]
- Do NOT ask to [THING THAT CAN'T BE DONE]
```

## Key Rules

1. **No internet dependencies** — bundle everything locally. If data must be downloaded, pre-download it.
2. **resume.md must be directive** — tell the agent exactly what to do. "You are resuming X. Your task is Y. Here's the data."
3. **Avoid context-dependent references** — the new agent won't have chat history. Be explicit.
4. **Include the disproven theories under constraints** — prevent the agent from retreading dead ends.

## Example: BAMBAM-FATCAT Handoff

Created at `/root/work/trading/bambam-fatcat-project/` with:
- 4 CSVs (PBB entries, FATCAT v1/v2/year)
- 3 Pine Scripts (OG indicator, gate indicator, strategy)
- 113 Binance 15m CSV files
- resume.md with the brute-force sweep instructions
- README.md with full project documentation
- Total: 1.5MB, fully self-contained
