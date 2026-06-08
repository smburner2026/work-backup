# DABT Internal Truth Audit — 2026-05-19

## Audit Scope

- **Database**: 446 questions (Mini-ABT Exams 1-11), Excel
- **Classification**: 446 rows, domain/bloom tagged
- **Reference texts**: Casarett & Doull 9e (35 ch), Hayes 7e (39 ch), Regulations (29 docs)
- **Memento Flashcards**: 45 cards (18 chelators, 27 biomarkers)
- **Progress state**: state.json, drill snapshots
- **Deep-dive artifacts**: 4 summary files

## Methodology

### Database Integrity
1. Load with `pd.read_excel(path, sheet_name='Questions')`
2. Verify: column presence, ID format (DABT-XXXX), uniqueness, source-exam distribution, null ratios
3. Spot-check 5+ question rows: `Correct Answer` letter must match `Correct Answer Text` verbatim

### Flashcard Verification (two-pass)
1. **Cross-reference against database**: For each flashcard, search the database for questions matching the same keyword/topic. Verify the flashcard fact matches the database's `Correct Answer Text`.
2. **Cross-reference against reference texts**: For mechanistic/regulatory claims (half-lives, thresholds, transporters), search Casarett & Doull 9e Ch.23 (Metals) and Hayes 7e Ch.19 (Metals) using `search_files`. Cite specific passages.

### Path Verification
Check that all paths referenced in skill files resolve to real files/directories on disk.

### State Integrity
Compare `progress/state.json` `deep_dived_topics` list against files actually present in `deep-dives/` directory.

## Findings Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Database structure | ✅ | 446/446 unique IDs, all exams present, answer-letter-to-text consistency verified |
| Database content (spot-checked) | ✅ | No contradictions in sampled rows |
| Flashcards vs database | ✅ | 43/45 verified against DB questions, 2 general-principle cards reasonable |
| Flashcards vs reference texts | ✅ | Mees' lines, Cd half-life, methylmercury BBB, acrodynia, arsenobetaine — all match Casarett |
| Reference texts - existence | ✅ | All 35+39+29 files present, indexed, substantial |
| **Skill file paths** | ❌ **BROKEN (FIXED)** | All skills used `/home/vthen/work/dabt-tutor/` — data actually at `/root/work/dabt/dabt-tutor/`. Patched during this audit. |
| Classification - Domain III | ⚠️ Known limitation | 8.5% vs 38% blueprint. 38 questions will deplete fast. |
| State - missing deep dives | ⚠️ | `lead-toxicity` and `mercury-toxicity` exist on disk but not recorded in state.json |
| State - date | ⚠️ | session.date says "2025-05-14" — should be 2026 |
| Flashcards - coverage gap | ⚠️ | Only Chelators (18) and Biomarkers (27) collections exist. No Risk Assessment, Mechanistic, Conduct cards. |

## Key Verifications (with source citations)

### Casarett & Doull 9e — Ch.23 "Toxic Effects of Metals"

| Claim | Source line | Verdict |
|-------|-------------|---------|
| Mees' lines appear ~6-8 weeks after As exposure | "appear about 6 weeks to 2 months after the onset of symptoms" (L1159-1161) | ✅ |
| Arsenobetaine is non-toxic seafood arsenic | "much less toxic than the inorganic forms" (L1128-1129) | ✅ |
| Cd half-life >26 years | "estimated to be more than 26 years" (L1739-1740) | ✅ |
| Cd half-life approaches 30 years in kidney | "biological half-life in humans approaches 30 years" (L614-615) | ✅ |
| As half-life ~10 hours | "whole-body biological half-life of ingested arsenic is about 10 hours" (L1152) | ✅ |
| Methylmercury transported by AA/organic anion transporters | "methylmercury, which is transported by amino acid or organic anion transporters" (L774-776) | ✅ |
| Acrodynia (pink disease) from chronic Hg in children | "Acrodynia has occurred in children chronically exposed to inorganic mercury" (L2826-2830) | ✅ |
| Lead chelation at >60 µg/dL in workmen | "Chelation therapy is warranted in workmen with BLL more than 60 μg/dL" (L2501-2502) | ✅ |
| Cobalt beer cardiomyopathy | "Severe cardiomyopathies... excessive consumption of beer containing cobalt as a foaming agent" (L3138-3141) | ✅ |

### Database Cross-checks

| Flashcard topic | DB Question | Verdict |
|----------------|-------------|---------|
| Antimony chelator = CaEDTA | DABT-0102 | ✅ |
| Antimony → QT prolongation | DABT-0303 | ✅ |
| Cobalt → polycythemia (erythropoietin) | DABT-0252 | ✅ |
| Cobalt → hard metal disease | DABT-0369 | ✅ |
| Lead OSHA threshold = <40 µg/dL | DABT-0273 | ✅ |
| EDTA + Hg = ineffective pair | DABT-0033 | ✅ |
| Bismuth → myoclonic encephalopathy | DABT-0292 | ✅ |
| Bismuth: cessation over chelation | DABT-0302 | ✅ |
| PPIs increase bismuth absorption | DABT-0287 | ✅ |

## Periodic Audit Checklist

Run this every 3 months or before significant study sessions:

1. [ ] Verify database `Explanation` column progress (currently 42.2% filled)
2. [ ] Check `asked_question_ids` count in state.json — ratate pool when >400
3. [ ] Verify deep-dive artifact files match state.json `deep_dived_topics`
4. [ ] Verify all skill paths still resolve (data migrations happen)
5. [ ] Spot-check 5 new flashcards against database answers
6. [ ] Check flashcard coverage gaps — are new collections needed?
