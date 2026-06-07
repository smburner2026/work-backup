---
name: gbrain-to-plain-markdown-migration
description: Pattern for re-platforming a G-Brain-coupled skill (miss journal, recall, takes, dream-cycle synthesis) to filesystem when G-Brain is decommissioned. What survives the migration, what doesn't, and the minimum-viable rebuild that gives the user their loop back.
---

# G-Brain → Plain Markdown Migration

G-Brain was a markdown knowledge base + LLM "dream cycle" (nightly consolidation via PGLite + OpenAI embeddings + LLM phases). The dream cycle did what backlinks would do, but with semantic search instead of wikilinks. It kept breaking — PGLite lock contention, dimension mismatches, OOM, gateway auto-restart races. On 2026-06-05 G-Brain was decommissioned.

This reference covers how to migrate a G-Brain-coupled skill to plain markdown when the user comes back asking "where's my X" / "the miss journal is broken" / "I want the synthesis back."

## The core principle

**The G-Brain value the user actually felt was: agent does the synthesis on demand, in plain text, with a way to find prior work.** That value survives the migration. What doesn't survive: background automation, semantic similarity search, "taste" of LLM-suggested connections surfaced overnight.

The migration target is **plain markdown + the agent doing on-demand synthesis + Obsidian's backlink panel for "where have I seen this" queries.** No database. No cron. No dream cycle. The trade-off is explicit: less ambient, more on-demand.

## What survives

| G-Brain feature | Plain markdown substitute | What you lose |
|---|---|---|
| `mcp_gbrain_put_page` (write a page) | `write_file` to the project's wiki dir | None — same outcome |
| `mcp_gbrain_recall` (cross-session memory) | `read_file` the recent miss journal daily files; `grep -r` for a concept | The semantic ranking; you get a recency-ordered list instead |
| `mcp_gbrain_query` (semantic search) | The agent reads the vault and answers | You need the agent to be available (session-bound) |
| `mcp_gbrain_think` (multi-hop reasoning) | The agent's own analysis with the vault as context | Loss of pre-computed caches — but re-running takes seconds |
| Backlink panel | Obsidian's built-in backlink panel | None — Obsidian does this natively |
| Dream cycle (nightly consolidation) | The agent on request | Loss of background discovery; must be prompted |
| Embedding-based "find similar notes" | None (use Bases queries or `grep` for keywords) | Loss of semantic similarity for novel phrasing |

The pattern that holds across all of these: **the agent becomes the substitute for the dream cycle, on demand.** G-Brain's automation wasn't paying for itself; on-demand works.

## Migration recipe: G-Brain-coupled skill → filesystem skill

Concrete steps for migrating a skill like `dabt-gbrain-miss-journal`:

### 1. Read the existing skill

```python
from hermes_tools import read_file
content = read_file('/root/.hermes/skills/education/dabt-gbrain-miss-journal/SKILL.md')
# Read its references/ too
```

Identify:
- The G-Brain tools used (`mcp_gbrain_*`, `gbrain put`, `gbrain recall`, `gbrain think`)
- The page slug convention (e.g. `dabt/miss-journal/YYYY-MM-DD-<topic>`)
- The structured summary format
- The failover-to-filesystem path (most G-Brain-coupled skills have this as a "PGLite is down" section)

### 2. Write a new skill with the same workflow

File path: same class, drop the "gbrain" prefix.

```bash
# Old:  /root/.hermes/skills/education/dabt-gbrain-miss-journal/SKILL.md
# New:  /root/.hermes/skills/education/dabt-miss-journal/SKILL.md
```

In the new SKILL.md:
- Replace the "G-Brain tools used" section with a "Storage" section pointing at the filesystem path
- The failover section becomes the primary path
- Drop the G-Brain "PGLite is down" detection section — it's no longer relevant
- Add a "Migration from G-Brain" section noting the deprecation date and what the user lost
- Keep the page slug convention unchanged (so old entries could be re-imported if any survived)

### 3. Create the directory structure

```bash
mkdir -p <wiki-root>/miss-journal/synthesis
```

Files to create:
- `<wiki-root>/miss-journal/README.md` — workflow MOC, links to the new skill
- `<wiki-root>/miss-journal/learner-profile.md` — stable learner facts (template, fill in user-specific data)
- Optionally, a backfill file: `<wiki-root>/miss-journal/backfill-YYYY-MM-DD.md` for any historical entries you can reconstruct

### 4. Update related skills

- `dabt-project-workflow` (or equivalent) — change the session-start reference from `dabt-gbrain-miss-journal` to `dabt-miss-journal`
- `dabt-drill-mode`, `dabt-deep-dive` — change inline-write hook references
- Any other skill that imports the old one

### 5. Mark the old skill as deprecated, don't delete

The old skill file may have content the user wants to reference. Move it to a deprecated dir or rename the dir with a `.deprecated` suffix. The curator can handle final consolidation at scale.

```bash
mv /root/.hermes/skills/education/dabt-gbrain-miss-journal \
   /root/.hermes/skills/education/dabt-gbrain-miss-journal.deprecated
```

## Common pitfalls

- **Don't try to recreate the dream cycle.** The user has already accepted the trade-off. Building a "lite dream cycle" with a cron + small LLM is just G-Brain with extra steps. The plain markdown + on-demand agent IS the simplification.
- **Don't preserve G-Brain tooling references "for when it comes back."** If G-Brain comes back, the new skill will need a different design (because the failure mode will be different). The old references are noise.
- **Don't backfill from session_search unless the user specifically asks.** Session reconstruction is expensive and often produces reconstructions that don't match the original G-Brain page quality. The user can re-record important misses in a single backfill session if they want.
- **Don't skip the learner-profile.md.** A miss journal without a learner profile is a pile of dated notes with no orientation. The profile is the index that says "this user is preparing for X exam, weak in Y, strong in Z" — it's the agent's standing reference for "where is this user and what are they doing."

## When the user says "I want the dream cycle back"

Push back. The dream cycle was the broken part. What they probably actually want is:
- Auto-discovery of new links (the agent can do this on demand — ask: "scan the vault and suggest 5 new concept links")
- Cross-session pattern detection (the agent can do this — ask: "find the recurring weak areas in the last 10 sessions")
- Pre-classified lookups (Obsidian Bases can do this — write a `.base` file with a filter)

If they really do want background automation, the *modern* answer is an LLM-driven cron that runs the agent on a schedule over plain text. The skill `background-agents` covers this pattern.

## Reference: the DABT migration (executed 2026-06-05)

The exact migration run on this user's DABT project:

**Old skill:** `/root/work/.hermes-config/education/dabt-gbrain-miss-journal/SKILL.md`
- G-Brain tools: `mcp_gbrain_put_page`, `mcp_gbrain_recall`, `mcp_gbrain_think`, `mcp_gbrain_query`
- Filesystem failover: `wiki/miss-journal-backup/<YYYY-MM-DD>-<topic>.md`
- Page slug convention: `dabt/miss-journal/YYYY-MM-DD-<topic>`

**New skill:** `/root/.hermes/skills/education/dabt-miss-journal/SKILL.md`
- Primary storage: `wiki/miss-journal/<YYYY-MM-DD>-<topic>.md` (filesystem, plain markdown)
- No database dependency
- Wikilinks from miss entries to concept notes (the loop)
- Pre-session pattern detection via `grep -rhoE '\[\[concept\]\]' wiki/miss-journal/ | sort | uniq -c | sort -rn`

**Files written:**
- `/root/work/dabt/dabt-tutor/wiki/miss-journal/README.md` (workflow MOC)
- `/root/work/dabt/dabt-tutor/wiki/miss-journal/learner-profile.md` (Abud, 2026 DABT, weak areas)
- Updated `/root/work/dabt/dabt-tutor/wiki/README.md` (added miss-journal pointer and link-on-miss rule)

**Net result:** the miss journal loop is unblocked, no G-Brain dependency, the agent does the same synthesis on demand, the user can see backlinks in Obsidian.
