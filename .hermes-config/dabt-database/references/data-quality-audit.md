# DABT Database — Data Quality Audit

Compiled 2026-05-20 during batch explanation writing via delegate_task subagents.

## Scope

Subagents writing 2-4 sentence explanations for the 2000Q Bank questions cross-referenced the DB's stored correct_answer_letter against Casarett & Doull 9e and Hayes 7e reference texts. Multiple discrepancies were found.

## Known Issues by Category

### 1. Answer Key Parsing Errors (2000Q Bank CSV import)

The 2000Q_ANSWER_KEY.csv had systematic parsing errors where the answer column was misaligned during extraction. Common patterns:

| Pattern | Examples | Count |
|---------|----------|-------|
| Answer letter `E` assigned when only options A-D exist | DABT-0466, 0722, 0726, 0731, 0733, 0739, 0746, 0777, 0780, 0782, 0805, 0808, 0813 | ~20+ |
| Answer letter references the display-line option text instead of the actual correct pairing (matching tests) | DABT-0518-0530 antidotes matching | 12 |
| `E` mapped to options beyond A-D where no option E exists in the DB | Various 2000Q Ch1 questions | ~10 |

**Action:** For matching tests, the original docx answer keys need re-extraction to recover the actual pairings. For E-without-options, the correct answer must be inferred from toxicology knowledge and reference texts.

### 2. Concept Reversals (DB says the opposite of accepted toxicology)

Subagents found ~15+ instances where the DB's correct answer contradicts well-established toxicology:

| Domain | Issue | DB Answer | Reference Text |
|--------|-------|-----------|----------------|
| Hematology | Clotting factor VII has the shortest half-life (3-4h), not factor IX | DABT-0626 → factor IX | Casarett Ch.11 |
| Hematology | Acidosis shifts O₂ dissociation curve RIGHT (Bohr effect), not left | DABT-0629 → left shift | Casarett Ch.11 |
| Hematology | G6PD deficiency causes hemolytic anemia, not creatine phosphokinase deficiency | DABT-0631 → CPK deficiency | Casarett Ch.11 |
| Hematology | Globin chain imbalance characterizes thalassemia, not sideroblastic anemia | DABT-0633 → sideroblastic | Casarett Ch.11 |
| Hematology | Desmopressin treats von Willebrand disease, not megaloblastic anemia | DABT-0636 → megaloblastic | Casarett Ch.11 |
| Immunology | T cell education (positive/negative selection) occurs in the THYMUS, not spleen | DABT-0645, 0646, 0662 → spleen/Peyer's patches | Casarett Ch.12 |
| Immunology | T cells migrate to lymph nodes, not Peyer's patches (B cell territory) | DABT-0645 → Peyer's patches | Casarett Ch.12 |
| Immunology | Negative selection eliminates self-reactive T cells in the thymus, not spleen | DABT-0662 → spleen | Casarett Ch.12 |

### 3. "EXCEPT" Logic Reversals

Several "All of the following are true EXCEPT" questions appear to have the answer pointing to the TRUE statement rather than the exception. This is likely a systematic extraction error where the inverse logic wasn't captured correctly.

| Question | Pattern | Evidence |
|----------|---------|----------|
| DABT-0650, 0651, 0655, 0666 | "Except" answer maps to a true statement | Subagent noted the marked answer is factually correct |
| DABT-0787, 0792, 0798, 0799, 0804, 0811, 0817 | Answer key inconsistent with standard tox knowledge | Multiple subagents flagged independently |

### 4. Matching Test Answer Scrambling

2000Q Bank matching tests (column A → column B) had the answer key scrambled during CSV export. The DB stores the display-line option text as the answer, not the actual correct pairing.

**Example:** Antidotes matching (DABT-0518-0530)
- DB says "glucagon → heparin" but the actual correct pairing is "glucagon → beta-adrenergic antagonists"
- DB says "octreotide → sulfonylurea-induced hypoglycemia" but this was stored as the option display text, not the answer

## Resolution — Quarantine (2026-05-20)

All issues documented below were resolved by **physical quarantine**: 1,048 broken/non-standard questions moved to `quarantine` / `quarantine_answer_options` tables. The main `questions` table is now 100% clean — every remaining question has a valid answer letter matching a 4–5 option set.

The quarantine preserves all original data (question text, options, explanations, bloom levels) with a `q_issue` column documenting the specific defect. If a source's issues are later resolved (re-extraction, SME review), questions can be restored to the main table.

**Remaining concerns in the main table:** The 2000Q Bank questions that passed quarantine (1,351 of 1,801 original) still need cross-referencing. The quarantine only removed questions with structural defects (no options, non-standard option counts, non-standard answer letters). The 1,351 remaining 2000Q Bank questions may still have undetected **factual errors** — the truth audit cron (Sundays 5AM UTC) samples 5 per week for reference-text verification.
