---
name: historiographical-style-guide
description: "Working style guide for history projects — synthesizes Nietzsche, Burckhardt, Luttwak, Wickham, Norwich, and Kantorowicz/Stefan George into a coherent historiographical method. Load before any history writing, research, or translation project."
version: 1.0.2
source: hybrid
tags: [research, history, methodology, historiography, vietnam, burckhardt, nietzsche, luttwak, wickham]
---

## Source Verification Protocol

All methodology loaded by this guide must carry a **provenance marker**. No foundation skill is treated as authoritative until it has been cross-verified against primary sources.

| Marker | Meaning |
|--------|---------|
| `source: primary` | Read directly from the author's text; method claims bound to specific passages |
| `source: verified-user` | User has engaged with the primary text in this project |
| `source: training-extracted` | Derived from model training — cross-check needed before critical use |
| `source: unverified` | No primary source on disk, no user engagement, no cross-check performed |

## Kanban-First Verification Pattern

When a foundation skill is `unverified` or `training-extracted` and the user requests verification:

1. Create a dedicated board: `<project>-sourcing`
2. Create one acquisition task per author/skill
3. Create a synthesis task with explicit dependency on the sourcing tasks
4. Set acquisition task priorities higher than synthesis
5. Write provenance notes to `/root/work/<project>-sourcing-board/<author>-primary.md`
6. Do NOT mark skills as verified until primary passages or documented acquisition blockers are in those notes

## When to Use

- Any history writing project
- Translation of colonial/post-colonial Vietnamese or French texts
- Research on Vietnamese historical figures
- Biographical writing about historical individuals
- Any project where the user references this historiographical framework