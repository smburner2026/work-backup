---
name: dabt-gbrain-miss-journal
description: "Persistent miss journal for DABT prep using G-Brain. During each session, inline-write misses, weak areas, and precision gaps as G-Brain pages. Before each session, query G-Brain recall + think for gap patterns. Enables data-driven weakness triage across 30+ sessions without relying on agent context window."
category: education
---

# DABT G-Brain Miss Journal

## Purpose

Persistent cross-session gap tracking that doesn't depend on the agent's context window. After 20+ sessions across 4+ months, the agent won't have reliable recall of what you were weak on in Session 3 vs Session 17. G-Brain does.

## Two-Phase Workflow

**Session start:** Load `dabt-project-workflow` first for config — reads `config['progress']['miss_journal_backup_dir']` (resolved against `config['project']['workdir']`) for the filesystem failover path.

## Phase A — Write Inline During Session (NOT at session end)

Sessions can span multiple days with context resets. Never wait for "session end." Write as you go.

### When to Write

After each of these events, write to G-Brain immediately:
1. **After a drill block** (5-10 questions) — write weak areas identified and precision errors
2. **After any mistake with root cause analysis** — write the concept, what went wrong, and the root cause
3. **After creating flashcards** — write the flashcard topics to `dabt/flashcards/<topic-slug>` and update master index
4. **After a flashcard review session** — write results to `dabt/miss-journal/YYYY-MM-DD-flashcard-review-<topic>`
   - Include: cards reviewed count, ratings breakdown, each miss with root cause, precision gaps
   - Update the collection page's Review History
   - Update learner-profile with new weak areas
5. **After a topic transition** — write a mini-summary of what was covered

### Structured Summary Format (for any inline write)

Each write appends a section to the daily session page:
```
## Block: <topic>
Questions: <N>, Correct: <N>
Weak areas: <concept> (root cause: <cause>)
Precision gaps: <term> → <correction>
Flashcards: <topic list>
```

### Recovery If Context Resets Mid-Session

When resuming a session after 1+ days or a model switch:
1. Query G-Brain recall for `entity="tempmoon-dabt"` — surfaces all inline writes from prior turns
2. Check `dabt/miss-journal/YYYY-MM-DD-<topic>` for the active session's page
3. If the page exists, continue: surface the weak areas found so far and ask which to drill
4. If no page exists for this session date, check session_search for the last DABT conversation and reconstruct

## Pitfall: G-Brain Unavailable

The gbrain MCP server (and thus all `mcp_gbrain_*` tools) may be unavailable — the PGLite WASM runtime can fail to initialize on an existing database even while fresh instances work fine (data directory corruption/incompatibility). This blocks all inline writes and pre-session recall queries.

### Detection
- `mcp_gbrain_*` tools are absent from the available tools list
- `gbrain get/put/search/query` all fail with "PGLite failed to initialize its WASM runtime"
- `gbrain doctor` still returns health score 90+ (filesystem checks pass, DB connection fails)

### Failover: Filesystem + Memory

When gbrain is down, do NOT skip recording. Use this stack instead:

#### 1. Write to Filesystem
Save structured markdown to the project's miss-journal-backup directory (resolved from config):
```
WORKDIR = CONFIG['project']['workdir']
BACKUP_DIR = os.path.join(WORKDIR, CONFIG['progress']['miss_journal_backup_dir'])
# save at {BACKUP_DIR}/<YYYY-MM-DD>-<topic>.md
```
Use the same page slug convention and structured summary format as the gbrain page would have had. This creates files ready for re-import when gbrain recovers.

#### 2. Write to Memory (context-level)
Save a compressed summary to `memory` target — enough to reconstruct the session if gbrain never recovers:
- Card count, rating breakdown, new precision gaps identified
- Pattern observations (e.g., "direction errors are primary failure mode")
- Path to the filesystem backup file

Do NOT save the full assessment to memory — that's what the filesystem backup is for.

#### 3. Note the Gap in the Summary
When delivering the session summary, explicitly mention "G-Brain was down — assessment saved to filesystem for later import." This tells the user the normal pipeline is degraded, not broken.

### Recovery When G-Brain Comes Back
1. Read the filesystem backup(s)
2. Run `gbrain put <slug>` for each page
3. Verify with `gbrain get <slug>`
4. Re-import any source documents that were added while gbrain was down

## Phase B — Before Session: Query Weak Areas

During session start procedure (after loading project-workflow, before selecting mode):

```
1. mcp_gbrain_recall(
     entity="tempmoon-dabt",
     since="4 months ago",
     limit=20
   )
2. If the learner switches between DABT and other work, add session_id filter:
   mcp_gbrain_recall(
     entity="tempmoon-dabt",
     session_id="<DABT-session-prefix>",
     limit=20
   )
3. Optionally for pattern detection across sessions:
   mcp_gbrain_think(
     question="What are the recurring weak areas in TempMoon's DABT sessions over the past 4 months? List by frequency.",
     anchor="tempmoon-dabt"
   )
```

This produces a prioritized list of weak areas to target in the session.

## Page Slug Convention

- `dabt/miss-journal/YYYY-MM-DD-<topic>` — individual session summaries (drills, deep dives)
- `dabt/miss-journal/YYYY-MM-DD-flashcard-review-<topic>` — flashcard review session results
- `dabt/flashcards/master-index` — master index of all flashcard collections
- `dabt/flashcards/<topic-slug>` — individual flashcard collection pages (card concepts, review history)
- `dabt/learner-profile` — stable learner facts (exam date, background, strengths, weaknesses)
- `dabt/synthesis/<topic>` — cross-session synthesis results

## When

- Phase A runs INLINE during every drill/deep-dive session — after each drill block, mistake analysis, flashcard creation, or topic transition
- Phase B runs at the START of every drill/deep-dive session
- Backfill run whenever a session from before the skill's creation date needs recording (audit session_search, reconstruct structured summaries)
- Monthly synthesis runs during Phase 2 (Week 5-8) of the 3-month plan

## G-Brain Tools Used

- `mcp_gbrain_put_page` — write session summaries as wiki pages
- `mcp_gbrain_extract_facts` — extract structured facts from session takeaways
- `mcp_gbrain_recall` — retrieve past session facts
- `mcp_gbrain_think` — multi-hop pattern detection across sessions
- `mcp_gbrain_query` — semantic search across all DABT pages

## Support Files

- `references/backfill-procedure.md` — reconstruct miss journal entries for sessions that predate this skill's creation
- `references/flashcard-gbrain-recording.md` — page templates and cascade order for flashcard gbrain recording (master index → collection page → miss journal entry → learner profile)

## Integration Points

- **dabt-project-workflow**: Session start procedure — loads config (provides `config['progress']['miss_journal_backup_dir']`), miss journal inline write check on context reset
- **dabt-deep-dive / dabt-drill-mode**: Inline write hook — write to G-Brain after each drill block, mistake analysis, or topic transition
