---
name: dabt-miss-journal
description: "Persistent miss journal for DABT prep using plain markdown in the Obsidian vault. During each session, inline-write misses, weak areas, and precision gaps to wiki/miss-journal/. Before each session, read recent entries for pattern detection. Replaces the G-Brain-coupled version after G-Brain decommissioning 2026-06-05."
category: education
---

# DABT Miss Journal (Plain Markdown)

## Purpose

Persistent cross-session gap tracking that doesn't depend on the agent's context window or any database. After 20+ sessions across 4+ months, the agent won't have reliable recall of what you were weak on in Session 3 vs Session 17. Plain markdown in the vault + `grep` does.

This skill **replaces** `dabt-gbrain-miss-journal` (deprecated 2026-06-05 when G-Brain was decommissioned). Workflow is the same; storage moved from G-Brain pages to plain markdown files.

## Two-Phase Workflow

**Session start:** Load `dabt-project-workflow` first for config — reads `config['progress']['miss_journal_backup_dir']` and `config['progress']['wiki_dir']` to resolve paths. The miss journal lives at `<workdir>/wiki/miss-journal/`.

## Phase A — Write Inline During Session (NOT at session end)

Sessions can span multiple days with context resets. Never wait for "session end." Write as you go.

### When to Write

After each of these events, write to a daily file in the miss journal directory:

1. **After a drill block** (5-10 questions) — weak areas identified + precision errors
2. **After any mistake with root cause analysis** — concept, what went wrong, root cause
3. **After creating flashcards** — flashcard topics, number of cards
4. **After a flashcard review session** — card count, rating breakdown, each miss with root cause
5. **After a topic transition** — mini-summary of what was covered

### Filename Convention

```
wiki/miss-journal/YYYY-MM-DD-drill-<topic-slug>.md
wiki/miss-journal/YYYY-MM-DD-flashcard-review-<topic-slug>.md
wiki/miss-journal/YYYY-MM-DD-deep-dive-<topic-slug>.md
wiki/miss-journal/synthesis/YYYY-MM-<topic-slug>.md   ← monthly cross-session
```

### Inline Write Format

Each write appends a section to the daily file:

```markdown
## Block: <topic>
Questions: <N>, Correct: <N>
Weak areas: [[concept-name]] (root cause: <cause>)
Precision gaps: <term> → <correction>
Flashcards: <topic list>
Related: [[concept-name-2]], [[concept-name-3]]
```

**Critical**: use `[[wikilinks]]` to link from the miss entry to the concept note in `wiki/concepts/`. This is the loop — drill → miss → write miss → wikilink concept → next study session, the backlink panel surfaces every prior miss on that concept.

### Recovery If Context Resets Mid-Session

When resuming a session after 1+ days or a model switch:

1. Read the most recent 3-5 daily files in `wiki/miss-journal/` (sorted by filename)
2. Look for repeated concept names across files
3. If a daily file already exists for today's date, append to it
4. If no file exists for today, create one — but first check the most recent session for context

## Phase B — Before Session: Surface Recurring Weak Areas

During session start procedure (after loading project-workflow, before selecting mode):

```bash
# Show the 5 most recent daily files
ls -t wiki/miss-journal/*.md 2>/dev/null | head -5

# Grep for [[concept-name]] wikilink references — most-linked concept is the top weakness
grep -rhoE '\[\[[a-z0-9-]+\]\]' wiki/miss-journal/ | sort | uniq -c | sort -rn | head -10
```

This produces a prioritized list of weak areas to target in the session. Compare against `wiki/concepts/` to see which concepts don't yet have a concept note — those are the candidates for new entries.

## When

- **Phase A** runs INLINE during every drill/deep-dive session
- **Phase B** runs at the START of every drill/deep-dive session
- **Backfill** runs whenever a session from before the skill's creation date needs recording (audit session_search, reconstruct structured summaries)
- **Monthly synthesis** runs during the second half of each month (cross-reference miss entries with concept notes for cross-session patterns)

## Integration Points

- **dabt-project-workflow** — Session start procedure: reads config for wiki_dir + miss_journal_backup_dir
- **dabt-deep-dive** — Inline write hook: write to miss-journal after each drill block or topic transition
- **dabt-drill-mode** — Inline write hook: write weak areas + precision gaps after each drill block
- **dabt-notebook** — Concept note creation: when a new concept note is created, check miss journal for prior misses on that concept and link them

## Storage

- Primary: `wiki/miss-journal/*.md` (plain markdown, vault-relative)
- Backlink visibility: Obsidian's backlink panel on each concept note shows every miss entry that references it
- Search: `grep -r "concept-slug" wiki/miss-journal/` finds all historical misses
- Durability: plain text, version-control friendly, no database

## Backfill from existing project files (do this before declaring entries "lost")

Before declaring historical miss entries lost, **search the project for any plain-markdown miss files that already exist**. The DABT case had a real entry sitting in `reference/data/miss-journal-2026-05-28-risk-assessment-flashcards.md` — easy to miss if you only look in the G-Brain-coupled skill's expected location.

Pattern:

```bash
# Find any miss-journal files anywhere in the project
find <project-root> -type f -name "*miss-journal*" 2>/dev/null

# Find any flashcard or session-summary files in the data dir
find <project-root>/reference -type f -name "*.md" 2>/dev/null
```

When found:
1. Move (or copy) the file to `wiki/miss-journal/`
2. Rename to the canonical `YYYY-MM-DD-flashcard-review-<topic>.md` format
3. Add frontmatter: `date: YYYY-MM-DD`, `source: backfilled from <original-location> on YYYY-MM-DD`, `related: [[concept-1]], [[concept-2]]`
4. Backfill the `wiki/miss-journal/README.md` MOC if needed

This recovers real session data that would otherwise be lost. The G-Brain-coupled entries are presumed lost; plain-markdown files in the project are recoverable.

## Maintenance loop (cron scripts)

Two no-LLM cron scripts keep the vault healthy. Both are `no_agent: true` and deliver to Telegram:

- **`dabt-vault-orphan-audit.sh`** — weekly. Reports concept notes with no incoming `[[wikilinks]]`. Output: "11 orphans, top priority to expand: X, Y, Z."
- **`dabt-weak-areas-summary.sh`** — every 3 days. Reads the last 7 days of miss journal entries, surfaces the most-referenced concept names. Output: "Top 3 weak areas this week: adversity-determination (4 refs), BMD (2 refs), POD (2 refs)."

The weak-areas script is essentially Phase B (Before-Session) automated — same grep logic, just scheduled. Schedule both at session-start so the user sees coverage gaps and weak areas without asking.

Full pattern, scripts, and cron registration: see the `obsidian` skill's `references/vault-maintenance-cron.md`.

## Migration from G-Brain Version

The previous skill `dabt-gbrain-miss-journal` is preserved at `/root/work/.hermes-config/education/dabt-gbrain-miss-journal/` for reference. All G-Brain tooling (mcp_gbrain_*, gbrain put/get/recall/think) is no longer used. If you find yourself reaching for those tools, write to the filesystem instead.

Historical miss journal entries that lived in G-Brain are presumed lost. If you have specific old entries you want to preserve, write them as a backfill file at `wiki/miss-journal/backfill-2026-06-05.md` with the original date and a "backfilled from memory" note.
