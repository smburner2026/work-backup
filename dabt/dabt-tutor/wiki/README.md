# DABT Notebook

Concept notes for topics that come up in drills and deep-dives.
Written during study sessions, not before. The textbooks are the source of truth;
this is where synthesis lives.

## Layout

```
wiki/
├── README.md                 ← this file
├── concepts/                 ← one file per concept, lowercase-hyphen
│   └── adversity-determination.md
└── miss-journal/             ← drill misses, weak areas, precision gaps (see miss-journal/README.md)
    ├── README.md
    ├── learner-profile.md
    └── YYYY-MM-DD-*.md       ← daily files
```

## Rules (there are three)

1. One file per topic in `concepts/`. Lowercase-hyphen names.
2. Start with a one-line definition. Write the rest however it makes sense to you.
3. Link to other pages with `[[wikilink]]` when it helps navigation. Don't force it.

That's it. No schema, no index, no log, no obligations — except: when you write a miss journal entry on a concept, link it to the concept note. That's the whole point.

## Wikilink conventions

- `[[concept-name]]` — link to a concept in `concepts/`
- `[[miss-journal]]` — link to the miss journal MOC
- `[[miss-journal/YYYY-MM-DD-drill-foo]]` — link to a specific daily file
- `[[learner-profile]]` — link to the learner profile

In concept notes, use the **first mention** of a related concept as a wikilink; subsequent mentions can be plain text. Avoid link spam.

## Tag conventions (YAML frontmatter)

```yaml
---
tags: [concept, domain-i-c, weight-16, risk-assessment]
domain: I-C Interpret
exam_weight: 16
sources: [cd-2, cd-3, hayes-3, epa-cancer-2005]
---
```

- `concept` — always present on concept notes
- `domain-<x>` — exam domain (i, ii, iii, iv); for sub-domains, use `domain-i-c` etc.
- `weight-N` — exam weight as a number
- Optional topical tags: `risk-assessment`, `mechanisms`, `carcinogenesis`, `statistics`, etc.

## Topics worth writing

Weak areas that keep costing you questions — drill them into a page and the
retrieval alone will tighten the concept. Currently: metals-chelation, antiviral-moa,
adversity-determination (Domain I-C, 16% — highest single weight).

## How concepts get written

When a concept becomes a recurring miss:
1. Create `concepts/<topic-slug>.md` using the conventions above
2. Pull citations from `reference/extracted/` with line numbers
3. Add wikilinks from related concepts (the backlink graph builds itself)
4. Update the daily miss entry to link back to the new concept
5. Next time you study the topic, the backlink panel shows you everything in one place

## How this connects to Obsidian

These notes are plain markdown and will open in any editor. Open them in Obsidian
on your local machine and the backlink panel becomes the "where have I seen this
concept?" view. The vault lives at `wiki/` — no Obsidian app required, but
Obsidian makes the relationship graph visible.
