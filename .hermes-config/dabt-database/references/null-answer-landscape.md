# Null-Answer Question Landscape

As of 2026-05-31: **670 questions** across 2 source files have `correct_answer_letter IS NULL` with `no_answer_key=1`.

## Source 7 — Past ABT Exams (PDFs)

| Property | Value |
|----------|-------|
| Source ID | 7 |
| Question IDs | DABT-4487 → DABT-4841 |
| Total in source | 351 |
| Without answer | 269 |
| With answer | 82 (randomly distributed across the range) |

### Content Split

The 269 unanswered questions in source 7 have two distinct content populations:

1. **Clinical/hepatology questions (DABT-4487 to ~DABT-4547):** Liver transplantation, HCV needle-stick, NAFLD/NASH, metabolic syndrome. These are NOT DABT toxicology content — they appear to be from a clinical medicine exam or USMLE-style questions mixed into the PDF collection.

2. **Toxicology questions (DABT-4548+):** Respiratory tract deposition, P450 enzymes, lead intoxication, risk assessment MOA, nanoparticles, grapefruit juice interactions, cerivastatin, QSAR, bioconcentration factors. Legitimate DABT content.

### Answer Strategy

Toxicology subset (DABT-4548+) → cross-reference Casarett & Doull / Hayes chapters.
Clinical subset (DABT-4487–~4547) → flag as non-DABT, leave unanswered or remove.

## Source 9 — 2017 ABT Certification Exam

| Property | Value |
|----------|-------|
| Source ID | 9 |
| Question IDs | DABT-4842 → DABT-5242 |
| Total in source | 401 |
| Without answer | 401 |

### Content Profile

All 401 are legitimate ABT toxicology content covering the full blueprint:
- Dermal sensitization (LLNA, Buehler, GPMT, Draize, split adjuvant)
- Percutaneous absorption (hydrophilicity, hexachlorophene hazard)
- Renal function (PSP clearance, inulin, NAG, beta2-microglobulin)
- Nephrotoxicity (proximal tubule damage from Hg/uranium)
- Endocrine disruption (Hershberger assay, multigeneration repro)
- Developmental toxicity (DNA alterations in embryo cells)
- Ocular irritation alternatives (Draize, in vitro replacements)
- Pulmonary immunotoxicity (guinea pig models)
- Immunosuppression testing
- UDS assay classification
- Lipofuscin and chronic CCl4 injury
- Hematologic malignancies from immunosuppression

### Answer Strategy

No official answer key ever published for the 2017 exam. Options:
- Web search for study-group answer keys / discussion forums
- Cross-reference each question against C&D/Hayes
- SME review for ambiguous items
- Keep `no_answer_key=1` permanently — these are discussion/practice prompts
