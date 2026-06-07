---
tags: [moc, miss-journal]
type: map-of-content
---

# Miss Journal

Persistent record of every drill miss, weak area, and precision gap from DABT prep sessions. Cross-session gap tracking that doesn't depend on the agent's context window.

## Why it exists

After 20+ sessions across 4+ months, the agent won't have reliable recall of what you were weak on in Session 3 vs Session 17. Plain markdown does — and so does `grep`.

## Layout

```
wiki/miss-journal/
├── README.md                 ← this file
├── learner-profile.md        ← stable learner facts (exam date, strengths, weak areas)
├── YYYY-MM-DD-drill-<topic>.md        ← drill session summaries
├── YYYY-MM-DD-flashcard-review-<topic>.md  ← flashcard review results
├── YYYY-MM-DD-deep-dive-<topic>.md    ← deep-dive follow-up
└── synthesis/
    └── YYYY-MM-<topic>.md     ← monthly cross-session synthesis
```

## When to write

- **After every drill block (5-10 questions)** — write weak areas, precision errors
- **After any mistake with root-cause analysis** — concept, what went wrong, why
- **After flashcard creation** — record the topic and number of cards
- **After flashcard review** — rating breakdown, root cause for each miss
- **After any topic transition** — mini-summary of what was covered

**Don't batch writes to session end.** Sessions span multiple days with context resets. Write inline.

## Inline write format

Append a section to today's daily file using this structure:

```
## Block: <topic>
Questions: <N>, Correct: <N>
Weak areas: <concept> (root cause: <cause>)
Precision gaps: <term> → <correction>
Flashcards: <topic list>
```

## Session start procedure

Before starting a drill or deep-dive session:

1. Open the most recent 3-5 daily files in this directory
2. Look for patterns in weak areas (recurring concepts)
3. Surface them in the session-start message: "Last 3 sessions — recurring weak areas: adversity determination (3x), benchmark dose (2x)"
4. Use the patterns to set today's focus

## Cross-references

When you write a miss entry on a specific concept, add a wikilink from that concept's note in `concepts/`. The Obsidian backlink panel then shows: "Adversity Determination — referenced from 4 miss journal entries, last miss 2026-05-15."

This is the loop. Concept note → drill → miss → write miss → wikilink to concept → backlink visible at next study session.

## Migration note (2026-06-05)

Previously the miss journal lived in G-Brain pages (`mcp_gbrain_put_page`). G-Brain was decommissioned due to fragility. All historical miss journal entries are presumed lost; future entries go here in plain markdown. The skill `dabt-miss-journal` (replacing `dabt-gbrain-miss-journal`) is the canonical reference for the workflow.
