# Batch 11 Renal & Respiratory Toxicology DB Answer Discrepancies

Batch: DABT-0769 through DABT-0818 (50 questions)
Source: 2000Q Bank (source_file_id=2)
Domain: All Domain IV (renal + respiratory toxicology)
Date processed: 2026-05-20

## Summary

This batch covers renal toxicology (~45 questions on nephron anatomy, physiology, nephrotoxicants) and respiratory toxicology (~5 questions on mucus, surfactant, alveolar cells). The renal physiology section has the highest rate of DB answer key errors seen across any organ system batch so far.

## DB Answer Discrepancies

### Category 1: Answer "E" with no E option (options only A-D)

These questions have `correct_answer_letter='E'` in the DB but only options A-D exist in `answer_options`. This is the same extraction error seen in earlier batches (batch6, batch7, batch9). The correct answer is one of A-D based on standard toxicology.

| QID | DB Answer | Correct Answer (per reference) | Notes |
|-----|-----------|-------------------------------|-------|
| DABT-0777 | E | A (thromboxane) | Cyclosporin increases thromboxane → vasoconstriction |
| DABT-0780 | E | D (none of the above) | PAH clearance measures renal blood flow, not insulin/creatinine/cystatin C |
| DABT-0782 | E | D (brush border) | Alkaline phosphatase + GGT are brush border enzymes |
| DABT-0805 | E | A (glomerulonephritis) | GN is intrinsic renal, not prerenal |
| DABT-0808 | E | A (nonionic at physiologic pH) | Nonionic low-osmolar contrast has lower nephrotoxicity |
| DABT-0813 | E | B (cationic restriction > anionic) | False: GBM is negative → anionic repelled more than cationic |

### Category 2: DB answer contradicts established physiology

| QID | DB Answer | Standard Physiology | Textbook |
|-----|-----------|-------------------|----------|
| DABT-0787 | A (dehydration) — dehydration does NOT increase BUN | Dehydration increases BUN via prerenal azotemia. The actual exception should be "immediately postdialysis" (D) | C&D Ch.25 |
| DABT-0792 | B (renal blood flow) — interfering with RBF does NOT cause ischemic injury | Vasoconstriction → reduced RBF → ischemic ATN is a classic pathway | C&D Ch.25 |
| DABT-0798 | C (basophils and plasma cells) — casts composed of basophils/plasma cells | ATN casts = necrotic tubular epithelial cells + cellular debris + Tamm-Horsfall protein | C&D Ch.25 |
| DABT-0799 | C (dedifferentiated capillary endothelial cells) — these repair tubules | Surviving tubular epithelial cells dedifferentiate, proliferate, and redifferentiate | C&D Ch.25 |
| DABT-0804 | A (glomerular filtration) — ADH interference most impairs GFR | ADH regulates water permeability in collecting duct (V2); blocking it impairs concentrating ability | C&D Ch.25 |
| DABT-0810 | D (vitamin D) — JGA secretes vitamin D | JGA secretes renin. Vitamin D 1α-hydroxylation occurs in proximal tubule cells | C&D Ch.25 |
| DABT-0811 | D (collecting duct) — most common renal injury site | Proximal tubule is the most common site (high metabolic rate, active transport, concentration) | C&D Ch.25 |
| DABT-0817 | A (mucus producing cells) — surfactant source | Surfactant is produced by type II alveolar cells (pneumocytes) | C&D Ch.25 |

### Category 3: Data quality issues

| QID | Issue |
|-----|-------|
| DABT-0814 | Zero options in answer_options table; question "Which of the following is the correct toxicant-target organ pair?" has no stored options |
| DABT-0818 | All 4 option statements concatenated into option A's text field: "They cover approximately 90 % of the alveolar surface. B. They can show preferential damage by toxic agents. C. They have an attenuated cytoplasm. D. They are cuboidal in shape." |

## Pattern Analysis

These errors are concentrated in the **renal physiology** portion of the 2000Q Bank extraction. Likely causes:

1. **Misaligned answer key rows** — The CSV extraction for renal questions (Ch25-equivalent section) appears to have shifted answer letters by 1-2 positions systematically
2. **Matching test misalignment** — Similar to the General Principles matching test (batch7), the renal anatomy matching items may have suffered column misalignment during extraction
3. **No docx verification** — Unlike batch6 (where the original docx was available for Ch1 General), no original docx files were available for the renal toxicology section, so these errors went undetected until now

## Recommendations for Future Renal/Respiratory Batches

1. **Always verify against C&D Ch.25** (renal) and **C&D Ch.15** (respiratory) before accepting any DB answer for renal physiology questions
2. **Treat all "E" answers with suspicion** when only A-D options exist
3. **For "all of the following EXCEPT" questions**, independently verify each option's truth value against the textbook — at least one EXCEPT question in this batch (DABT-0805, DABT-0813) has the DB answer pointing to the wrong statement
4. **For respiratory questions** (DABT-0815 to DABT-0818), the DB answers for type I/II alveolar cell characteristics are also unreliable; verify against C&D Ch.15
