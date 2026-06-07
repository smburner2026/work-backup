---
name: vault-bootstrap-for-study-projects
description: Class-level recipe for bootstrapping an Obsidian vault for a long-running self-study or exam-prep project that already has extracted source material, a drill question bank, and a miss journal. Distinct from the generic vault-bootstrap.md (which is for a greenfield vault).
---

# Vault Bootstrap for Study Projects

When the user is preparing for a board exam (DABT, USMLE, CFA, PE, bar, etc.) and already has:
- A directory of extracted reference material (textbook chapters as `.md` / `.txt`)
- A drill question bank (SQLite, JSON, or similar)
- A miss journal skill, possibly coupled to a now-decommissioned tool (G-Brain, Anki sync, Notion, etc.)
- An empty or near-empty `wiki/` folder in the project directory

…they do not need a generic vault. They need a **study project vault** with one specific shape. This is the recipe.

## When to use this recipe (vs. the generic bootstrap)

| Signal | Recipe |
|---|---|
| User mentions "prep", "exam", "study", "drill" | study-projects |
| Vault path points inside a `dabt-tutor/`, `bar-prep/`, `cfa/`, etc. project dir | study-projects |
| User has extracted textbook chapters in `reference/extracted/` | study-projects |
| User has a `dabt.db`, `questions.json`, or similar question bank | study-projects |
| User mentions a previous AI tool that "crashed" or was "decommissioned" | study-projects (also use gbrain-to-plain-markdown-migration) |
| Otherwise | generic vault-bootstrap.md |

## The 5-step recipe (proof-of-concept, low-risk rollout)

### Step 1 — Inventory the existing material

Before writing anything, list what's actually on disk. Don't ask the user — they often don't remember the exact layout. Use `terminal` to:

```bash
ls <project-root>/
ls <project-root>/reference/extracted/        # textbook chapters
ls <project-root>/wiki/                       # existing vault
ls <project-root>/dabt.db | head -c 100       # check if DB is real or 0 bytes
find <project-root> -name "*.md" -path "*wiki*" | head -20
```

Then load the relevant project skills (e.g. `dabt-project-workflow`, `dabt-reference`, etc.) to get the project's own conventions.

**Critical pitfall:** when the project has a config (AGENTS.md, `dabt-config.json`, `package.json`) that explicitly names a path, follow *that* path. The DABT project has both a stub `dabt.db` at the project root (0 bytes) AND a real `reference/data/dabt.db` (9.3 MB, 7,567 questions). AGENTS.md says the real one is at `reference/data/dabt.db`. Checking the wrong file and flagging "the DB is empty!" is a hard-fail.

### Step 2 — Use the existing `wiki/` folder, don't create a parallel vault

The project likely has a `wiki/` directory in its config. The user's existing `wiki/README.md` will often have a *minimalist philosophy* written into it ("no schema, no index, no log, no obligations"). **Respect it.** Add only:
- A `concepts/` subdir (one file per concept, lowercase-hyphen names)
- A `miss-journal/` subdir (for cross-session miss tracking)
- Tag conventions in YAML frontmatter (light, optional)
- The "link on miss" rule (when you write a miss entry, wikilink the concept)

Don't impose: numbered folders, mandatory daily templates, MOC indexes, status trackers, exhaustive frontmatter schemas.

### Step 3 — Pick ONE proof-of-concept concept and link it end-to-end

The single most valuable thing the agent can do is demonstrate the loop. Pick a concept that:
- Has the highest exam weight (use the project's blueprint/curriculum config)
- Has been actively discussed in prior sessions (look in session_search)
- Has a clear textbook citation you can grep in the extracted material

For that concept, write a `concepts/<slug>.md` with:
- YAML frontmatter: tags, domain, exam_weight, sources, related
- One-line definition at the top
- 2-3 layer mental model (foundational → operational → modern framework)
- 3-5 cited source lines (chapter + line number) from the extracted material
- "Exam traps" section with concrete examples
- Outgoing `[[wikilinks]]` to related concepts (the agent's predicted future concepts)
- "Backlinks" section noting who currently links here (usually empty on day 1)

This is the artifact that makes the value prop visible. If it's good, the user sees backlinks light up in Obsidian and gets it. If it's bad, the user concludes "Obsidian doesn't help" and you lose the chance. Quality matters.

### Step 4 — Re-platform the miss journal (if G-Brain-coupled)

If the project has a miss journal skill that's coupled to a now-decommissioned tool (G-Brain is the common case), re-platform it to plain markdown. The pattern:

1. Read the existing miss journal SKILL.md fully
2. Identify the storage path (usually `wiki/miss-journal/` or project-configured backup dir)
3. Write a new SKILL.md at the same class level (e.g. `dabt-miss-journal` replacing `dabt-gbrain-miss-journal`) with filesystem as primary
4. Migrate the "failover" section to be the primary path; the G-Brain section becomes a deprecated reference
5. Create the `wiki/miss-journal/README.md` MOC and a `learner-profile.md` template
6. Keep the old skill on disk as a `.bak` or in a deprecated skills dir for reference — historical entries may need to be reconstructed from session_search

**Backfill nuance:** historical entries may also be sitting in plain markdown inside the project (e.g., `reference/data/miss-journal-2026-05-28-risk-assessment-flashcards.md`). Before declaring them "presumed lost," `find` the project for any file matching `*miss-journal*` and migrate them into `wiki/miss-journal/` with a `source: backfilled` frontmatter note. The G-Brain → plain markdown migration reference covers the broader pattern.

### Step 5 — Hand off, then iterate

After the proof-of-concept concept note is written and the miss journal is re-platformed:
- Tell the user what to look for when they open Obsidian (backlink panel, the one line of "this concept is referenced from 1 place" they should see)
- Identify the next 2-3 concept notes to write (use the curriculum's prerequisite ordering — usually start with the next-highest-weight, still-uncovered concept)
- Set a trigger: "next time you miss a drill question, write the miss and link it back to the concept"

Don't try to do all 14 Domain IV concepts in one session. Do one, get the loop working, then expand.

## Phase 2 — Full population (when the user says "I have N months, just start filling it")

When the user gives an explicit "proceed / set it up now / start populating" mandate and the curriculum is already indexed (e.g., `dabt-config.json` has 81 topics with weight tags), the next step is a one-shot full population, not a 5-step rollout. The pattern that worked for DABT 2026-06-05:

### Step 6 — Templated concept-stub generation

For every indexed topic, write a *functional stub* (not empty) with this template:

```markdown
---
tags: [concept, <domain-tag>, weight-<N>]
domain: <domain label>
exam_weight: <N>
status: stub
sources: [<source-id-1>, <source-id-2>]
related: [[concept-1]], [[concept-2]]
---

# <Topic Name>

<one-line definition>

## Why it matters

Exam weight: **<N>%** (Domain <X>). Stub — pull on this to expand.

## Source pointers

- Casarett & Doull 9e ch N — `<chapter-slug>`
- Hayes 7e ch N — `<chapter-slug>`
- `reference/extracted/` for the raw text

## Related concepts

[[concept-1]], [[concept-2]]
```

Generate via a Python script (`wiki/populate-vault.py`) that:
- Reads the curriculum config (e.g., `dabt-config.json` → `curriculum.domains[*].topic_list`)
- Slugifies topic names (lowercase, hyphens; em-dash + en-dash + forward-slash → hyphen; collapse repeats)
- Inlines a curated `DEFINITIONS` dict (one-liner per topic, exam-oriented)
- Inlines `CD_CHAPTERS` and `HAYES_CHAPTERS` maps (curated; conservative — when in doubt, point at the whole source, not a wrong page)
- Idempotent: skips existing files (so re-runs are safe)

Key discipline: **stubs are pull targets, not empty placeholders**. Definition + weight + source pointers + 1–2 related links is the minimum. Anything less erodes trust in the system.

### Step 7 — MOC notes per domain/grouping

For each top-level grouping (4 exam domains + 1 organ-system cross-cutting in DABT's case), write a Map of Content. Template:

```markdown
---
tags: [moc, <domain-tag>]
type: map-of-content
domain: <domain label>
exam_weight: <N>
---

# Domain <X> — <Label>

> <Label> — <N>% of the exam. Master index of concept notes, source pointers, and exam traps.

## Exam weight breakdown

- **<subdomain>** — N%

## Concept notes (this domain)

- [[slug-1]] *(subdomain-a)*
- [[slug-2]]
- ...

## Source pointers

- **Primary text**: ...
- **Mechanistic depth**: ...
- **Regulatory anchor**: ...

## Exam traps

- <one-liner exam traps that connect multiple concepts in this domain>
```

5 MOC notes is usually enough; MOC-per-domain is the right granularity. MOC-per-week or MOC-per-chapter is over-engineering.

### Step 8 — Surgical wikilink injection into source chapters

Source chapters in `reference/extracted/` are valuable context. Append a "## Cross-references (vault)" section to each chapter that has matching concepts. Use an **inverse map** (chapter-slug → [concept-names]) and a marker comment so the section is idempotent and reversible.

Script pattern (`wiki/inject-wikilinks.py`):
- Iterate `chapter_to_concepts[("cd" | "hayes", chapter-slug)]`
- For each, read the file, check for the marker `## Cross-references (vault)`
- If present, replace the existing section (in case the concept list changed)
- If absent, append at the end of the file
- Sort concepts by exam weight within the section (most important first)

Marker pattern:

```markdown
---

## Cross-references (vault)

Auto-generated by `wiki/inject-wikilinks.py`. Concept notes that cite this chapter as a source, ordered by exam weight.

- [[slug-1]]
- [[slug-2]]
- [[slug-3]]

> Backlinks from these concept notes will appear in the Obsidian backlink panel when this vault is opened. To regenerate, re-run the script.
```

This makes the backlink graph work in both directions: concept note → source chapter (in the related list), source chapter → concept note (in the cross-ref section). The user's Obsidian graph is now navigable from either side.

### Step 9 — Cron-based maintenance loop

See `references/vault-maintenance-cron.md` for the two-scripts-and-two-cron-jobs pattern (orphan audit + weak-areas summary). Schedule on creation, not after-the-fact. The user said "a couple of automatic prompts" — deliver exactly that, not 5.

### Step 10 — Kanban board as a markdown file (when kanban MCP isn't available)

If the kanban MCP server isn't exposed in the session, write the work as `wiki/kanban-board.md` with tiered priorities (Tier 1: active study focus, Tier 2: secondary, Tier 3: cross-cutting, Tier 4: maintenance). The user can paste it into their actual kanban. Don't block the work waiting for kanban.

## What this recipe does NOT do

- It does not install Smart Connections, Dataview, Templater, or any other Obsidian plugin. The user can add those later if they want.
- It does not migrate history / projects outside the active study area. The user may have other vaults (Burckhardt research, post-colonial Vietnam) — keep them separate.
- It does not backfill historical miss journal entries from G-Brain by default. Those are presumed lost; if specific entries need preservation, write them as a backfill file with a "backfilled from memory" note. But first `find` the project for any plain-markdown miss files that already exist.
- It does not provide a daily template, weekly review template, or any other recurring structure. The user can add these if they want.

## Worked example (DABT 2026)

The exact pattern executed 2026-06-05:

```
Project:      /root/work/dabt/dabt-tutor/
Reference:    /root/work/dabt/dabt-tutor/reference/extracted/{cd-9e, hayes-7e, regulations, abt-handbook}/
Drill DB:     /root/work/dabt/dabt-tutor/reference/data/dabt.db (SQLite, 7,567 questions — NOT the 0-byte stub at /root/work/dabt/dabt-tutor/dabt.db)
Config:       /root/work/dabt/dabt-tutor/dabt-config.json (v1.1.0)
Wiki:         /root/work/dabt/dabt-tutor/wiki/  (existed, near-empty)
Miss journal: /root/work/.hermes-config/education/dabt-gbrain-miss-journal/  (G-Brain-coupled, deprecated)
              /root/work/dabt/dabt-tutor/reference/data/miss-journal-2026-05-28-risk-assessment-flashcards.md  (real entry, found by find, moved to vault)

Phase 1 (Steps 1-5):
  - Concepts chosen: Adversity Determination (Domain I-C, 16%), MOA (Domain I-C + III-D, ~25%)
  - Files: concepts/adversity-determination.md, concepts/mode-of-action-analysis.md,
          miss-journal/README.md, miss-journal/learner-profile.md, wiki/README.md
  - Skill re-platformed: /root/.hermes/skills/education/dabt-miss-journal/SKILL.md
  - Skills installed (kepano): ~/.opencode/skills/obsidian-skills/skills/{obsidian-markdown,obsidian-bases,json-canvas,obsidian-cli,defuddle}

Phase 2 (Steps 6-10):
  - 81 concept stubs generated (1 per indexed topic) via populate-vault.py
  - 5 MOC notes written (Domain I/II/III/IV + Organ Systems)
  - 36 source chapters received "## Cross-references (vault)" sections via inject-wikilinks.py
  - 2 cron jobs scheduled: orphan audit (Sun 04:00 UTC), weak-areas summary (every 3 days, 09:00 UTC)
  - kanban-board.md written for kanban import
```

Result: 92 markdown files in the vault, 71/82 concept notes linked, 11 orphans flagged for the next pass. Vault is ready for the first drill session to write a real miss entry and close the loop.
