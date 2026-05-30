# DABT Tutor — Task Roadmap

Updated 2026-05-30 (post-quarantine, kanban integration established).

## Current DB State (main table: 3,796 Qs)

All main-table Qs have explanations, bloom levels, and answer letters. See `dabt-project-workflow` SKILL.md data quality table for full metrics.

## Active Kanban Cards (6, running on default profile)

| Priority | Card | Status | Notes |
|----------|------|--------|-------|
| P1 | Audit batch33 errors DABT-1800+ | Running | ~45 Qs, ~82% error rate per Casarett Ch.6 |
| P2 | Classify 62 domain-less Qs | Running | Source 6 Past ABT Exams 2008-2014 |
| P3 | Fill 1,725 null answer texts | Running | Bulk SQL from answer_options |
| P4 | Rewrite 61 placeholder explanations | Running | Stub explanations ≤50 chars |
| P5 | Update dabt-config.json to post-quarantine | Ready | Quality metrics, domain counts, source counts |
| P6 | Skills config consumption refactor | Ready | Complete hardcoded→config migration |

## Remaining Work Items (needs discussion)

### Strategic / Needs-Planning Items

**1. Domain III Synthetic Questions (target 600 Qs)**
- Domain III = 38% exam weight, only 170 Qs in DB (4.5%)
- Prereq: assign sub-domains to the 135 unassigned Domain III Qs first
- Ground truth: Casarett Ch.4, Hayes Ch.3, EPA Cancer Guidelines 2005, Silver Book, ABT Handbook task statements
- Decision needed: generation strategy, quality bar, distractor design

**2. Domain I Synthetic Questions (target 1,600 Qs)**
- Domain I = 36% exam weight, only 768 Qs in DB (20.3%)
- Covers A. Design (11%), B. Execute (9%), C. Interpret (16% — largest sub-domain)
- Sources: Casarett Ch.5-7 (ADME), Ch.31 (Analytical), handbook task statements

**3. Quarantine Recovery Strategy (1,048 Qs)**
- 626 Group A (broken answer data) — potentially recoverable via source re-extraction
- 273 Past ABT PDFs — real exam Qs, no answer keys, SME review needed
- 149 Group B — non-standard option counts, potentially salvageable
- Need approach decision before creating cards

**4. Past Exam PDF Ingestion**
- 2013 recert (6 files), 2015 recert (13 files), 2017 cert (4 files), Tox 2000 notecards
- Sitting at reference/exam-materials/practice-exams/
- Dedup against existing DB, extract new Qs, full explanation pipeline

**5. Curriculum/topics.json Decision**
- Orphan artifact with 5 domain entries and sub-structure
- Three options: adopt (wire into workflow), adapt (restructure first), archive (delete)
- Blocked on user decision

## Sequencing

```
Phase 0 (active):  Kanban cards (P1-P6) running on dispatcher
Phase 1 (next):    Domain III sub-domain classification → synthetic Q generation
Phase 2:           Domain I synthetic Qs
Phase 3:           Quarantine recovery + Past exam ingestion
Phase 4:           Curriculum decision
```

## Kanban Process Note

Strategy items (Domains I/III, quarantine, exams, curriculum) should NOT be created as kanban cards until discussed with the user and explicitly approved. Only bounded, executable tasks go on the board directly. See `dabt-project-workflow` → Kanban Workflow for DABT Items for the classification criteria.
