---
name: dabt-notebook
description: Lightweight markdown concept notebook for DABT study — create, update, and cross-reference topic pages during deep-dives and drill review.
category: education
---

# DABT Notebook

Persistent concept notes written during study sessions. One page per topic,
interlinked with `[[wikilinks]]` when it helps. The reference texts are the
source of truth; the notebook is synthesis and sense-making.

## Location

The wiki directory is defined in `/root/work/dabt/dabt-tutor/dabt-config.json`. At session start, load config:

```python
import json
with open('/root/work/dabt/dabt-tutor/dabt-config.json') as f:
    CONFIG = json.load(f)
WIKI_DIR = f"{CONFIG['project']['workdir']}/wiki"
```

Default: `/root/work/dabt/dabt-tutor/wiki/`

## Trigger

Load this skill whenever:
- A drill or deep-dive uncovers a concept worth distilling into a page
- The user asks to update or review a notebook page
- A missed question gets explained and the explanation is worth saving

**Session start:** Load `dabt-config.json` first for project paths (wiki directory, etc.).

## Structure

```
wiki/
  README.md     # Conventions (3 rules, no obligations)
  concepts/     # Topic pages, one per file
```

## Rules (from README)

1. One file per topic in `concepts/`. Lowercase-hyphen names.
2. Start with a one-line definition. Write the rest however it makes sense.
3. `[[wikilinks]]` when it helps navigation. Don't force them.

No schema, no index, no log, no linting.

## Usage

### Create a new page

When a concept comes up during a drill or deep-dive that would benefit from a
written synthesis:

```
write_file(
  path="/root/work/dabt/dabt-tutor/wiki/concepts/topic-name.md",
  content="..."
)
```

### Update an existing page

When new information or a better understanding of the concept emerges:

Use `patch` or `read_file` + `write_file` to update the relevant page.

### Review pages

Read a page, or list all pages with `search_files("*")` on the concepts directory.

## Integration with other DABT skills

- **dabt-deep-dive**: At the end of a deep-dive session, offer to write or update
  a notebook page with the synthesis. This is the main way the notebook grows.
- **dabt-drill-mode**: When a question is missed and the explanation reveals a
  concept gap, offer to create or update the relevant page.
- **dabt-reference**: Use reference lookups to source the notebook page content,
  then cite the source in the page.

## Pitfalls

- Don't create pages for every question — only for topics that keep costing points
  or that genuinely benefit from cross-reference synthesis
- Don't over-structure. If a page is more than about 200 lines, split it into
  sub-topics with cross-links
- The notebook is a learning tool, not a reference system. Prefer `dabt-reference`
  for factual lookups into the textbooks
