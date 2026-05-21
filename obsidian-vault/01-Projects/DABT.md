# DABT Certification

> Toxicology board exam prep — Memento flashcards + drill mode

## Method

- **Flashcards (lunch):** Low-pressure spaced repetition via Memento. Free-response channel at `discord:1505365003983781939:1506339736556409022`
- **Drill (exam):** DABT drill mode — database of 446 practice questions. Full exam pressure simulation.
- **Workflow:** On-demand card generation from DABT Practice Questions Database → Memento batch import → spaced repetition review

## Source Database

`/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx`
- **446 questions** across 35 toxicology topics (Questions sheet)
- 11 Mini-ABT exams (exams 1–11)
- Fields: ID, Source Exam, Question, A–H, Correct Answer, Explanation, Topic
- Topic Index sheet with question counts per domain

### Topic Breakdown (top 10 by volume)
| Topic | Questions |
|-------|-----------|
| Metals & Metalloids | 61 |
| Solvents & Hydrocarbons | 54 |
| Carcinogenesis & Mutagenesis | 42 |
| Liver / Hepatotoxicity | 35 |
| Pesticides – Insecticides | 31 |
| General Toxicology | 29 |
| Kidney / Nephrotoxicity | 18 |
| Immunotoxicology / Allergy | 16 |
| Mechanisms of Toxicity | 14 |
| Drugs & Therapeutics – Toxicology | 11 |

*35 topics total — full list in vault note or Topic Index sheet.*

## Memento Flashcards

- **45 cards** live in 2 collections: `DABT - Chelators`, `DABT - Biomarkers`
- Cards stored at `~/.hermes/skills/productivity/memento-flashcards/data/cards.json`
- Spaced repetition schedule: hard=1d, good=3d, easy=7d (autoretire after 3× easy)
- CLI: `python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py`
- Flashcard channel: `discord:1505365003983781939:1506339736556409022` (free-response mode)

## Skills

- `dabt-reference` — 3-pass search across extracted reference texts
- `dabt-drill-mode` — exam-pressure testing from 446-question bank
- `dabt-deep-dive` — Socratic first-principles tutoring
- `dabt-database` — query the practice questions DB

## Reference Material

- 35 chapters of C&D (9.9 MB) — extracted to `reference/extracted/`
- 39 chapters of Hayes (11 MB)
- 29 regulations (4.2 MB)
- Each source has `index.json`

---

*Last updated: 2026-05-19*
