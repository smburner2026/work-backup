# Pyramid Naming & Path Conventions

## Directory Structure

```
euphy/llm-wiki/
├── index.md                          # Master content catalog (update on every build)
├── pyramids/
│   ├── dabt/
│   │   └── dabt-flashcards-L1-summary.md
│   └── vstb/
│       ├── vstb-4-lenses-L1-summary.md
│       ├── vstb-4-lenses-L2-burckhardt.md
│       ├── vstb-4-lenses-L2-vitalism.md
│       ├── vstb-4-lenses-L2-class.md
│       ├── vstb-4-lenses-L2-strategic.md
│       └── vstb-background-to-betrayal-L1-summary.md
```

## Naming Rules

- L1: `topic-L1-summary.md` — mandatory for every new artifact group
- L2: `topic-L2-[dimension].md` — one per domain/lens/volume that has clear analytical dimensions
- Topic slug: lowercase, hyphens, derived from the artifact group name

## Frontmatter Template

```yaml
---
title: Human-Readable Title — L1 Summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: summary | analysis
tags: [dabt|vstb, topic-keywords, pyramid, l1|l2]
sources:
  - path/to/source/file.md
  - path/to/another/source.md
confidence: high | medium | low
---
```

## Provenance Marker Format

At end of paragraphs whose claims trace to a specific source:
```
^[path/to/specific/source.md]
```

At end of file, list all source provenance markers:
```
^[sources/vstb/synthesis-report.md]
^[historian-collections/analysis/lens1-burckhardtian-deep.md]
```

## What Qualifies for L2

Create L2 files when:
- The artifact group has clear analytical dimensions (e.g., 4 historiographical lenses)
- Each dimension has substantial standalone content (>200 lines in source)
- A downstream agent would benefit from reading just one dimension without the full synthesis

Do NOT create L2 when:
- The artifact is a single flat list (e.g., flashcards without analytical dimensions)
- The source material is too thin to warrant decomposition

## Historical Scan Dates

| Date | Action | Files Created | Notes |
|------|--------|---------------|-------|
| 2026-06-09 | Initial build | 7 (3 L1 + 4 L2) | First run. No prior pyramid structure existed. |
