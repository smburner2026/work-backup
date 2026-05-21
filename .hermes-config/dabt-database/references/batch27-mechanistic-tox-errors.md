# Batch 27 — Mechanistic Toxicology (Domain II) Errors

**Batch:** 50 questions (DABT-1519 through DABT-1568)
**Domain:** All Domain II (Mechanistic Toxicology)
**Source:** 2000Q Bank (source_file_id=2)
**Processed:** 2026-05-20

## Summary

This is the first batch of **Domain II (Mechanistic Toxicology)** questions processed from the 2000Q Bank. Unlike Domain IV (organ system toxicology) batches where error rates ranged from 8%–58%, Domain II has a **lower but still significant error rate of ~6 confirmed issues in 50 questions (12%)**. The error profile is distinct: fewer matching-test scrambles, more **answer-key semantic ambiguity** and **wrong-standard-answer for specific mechanisms**.

**Key finding:** Domain II questions are generally more reliable than Domain IV from the same source, but answer-key extraction errors for "EXCEPT" questions and for enzyme/receptor pairing items persist.

## Verified DB Errors

| DB ID | Question Topic | DB says | Correct answer | Rationale |
|-------|---------------|---------|---------------|-----------|
| DABT-1528 | Receptor-agonist pairs | C: GABA(A) receptor–muscimol is incorrect | GABA(A) receptor–muscimol IS a correct agonist pair | Muscimol is a well-established GABA(A) receptor agonist. Some sources note higher potency at GABA-C (ρ subunit) receptors, but it is unambiguously a GABA(A) agonist. The DB designates this as "incorrect" — unclear if this is an answer-key reversal or extraction error. |
| DABT-1529 | Receptor-antagonist pairs | A: adrenergic beta1–metoprolol is incorrect | Metoprolol IS a correct beta-1 antagonist | The `correct_answer_text` field stores all 4 options merged into one text field (parsing error). Metoprolol is a selective beta-1 blocker — a correct antagonist pair. The other listed pairs contain inaccuracies (avermectins are not GABA-A antagonists), making the answer key's selection of A questionable. |
| DABT-1559 | Enzyme that repairs oxidized protein thiols | A: HMG-coenzyme A reductase | D: none of the above | HMG-CoA reductase is the rate-limiting enzyme in cholesterol biosynthesis — it does NOT repair oxidized protein thiols. The actual enzymes are thioredoxin reductase and glutaredoxin (using NADPH). None of the listed options (HMG-CoA reductase, adenyl cyclase, phospholipase) are correct. |
| DABT-1568 | Glutathione false statement | D: "It is a substrate for glutathione peroxidase" | B: "It is a dipeptide" | Glutathione is a tripeptide (γ-glutamyl-cysteinyl-glycine), making option B factually false. However, GSH IS consumed by GPx as a reducing co-substrate — making D arguably true. The answer key designates D as the false statement, which conflicts with standard enzymology. |

## E-Answer Corruptions (Answer ≥ E but only A-D options stored)

| DB ID | Question | DB answer | Likely meaning | Verdict |
|-------|----------|-----------|----------------|---------|
| DABT-1527 | Receptor-exogenous ligand pairs | E (no E option in DB) | None of the above are all correct | Plausible — A-D are all correct pairs (AhR-rifampicin IS incorrect, so if E = "none of the above are incorrect" it would be false unless 5th option exists) |
| DABT-1530 | Clonidine overdose mimic | E | None of the above | Valid — clonidine produces a sympatholytic toxidrome not matching morphine, cocaine, PCP, or amphetamine |
| DABT-1531 | TCA cycle inhibitors | E | All of the above are inhibitors | Valid — 4-pentenoic acid, fluoroacetate, DCVC, and malonate all inhibit the TCA cycle |
| DABT-1546 | Hypoxia response | E | Production of aerobic ATP is NOT part of hypoxia response | Ambiguous — hypoxia response shifts cells to glycolytic (anaerobic) ATP, so option C ("proteins that stimulate aerobic ATP synthesis from glucose") IS not an element. If E = "none of the above," this contradicts because C is indeed excluded. |
| DABT-1547 | Oncogene mutation product | E | Likely a 5th option not captured | All 4 stored options (ICAM-I, RAS, STAT, C/EBP) are plausible, but RAS is the classic oncogene mutation product |

## Parsing Issues

- **DABT-1529:** All 4 options concatenated into the `correct_answer_text` field: "adrenergic beta 1 receptor–metoprolol B. serotonin (2) receptor–ketanserin C. glutamate receptor–ketamine D. GABA (A) receptor–avermectins". The DB only has one `answer_options` row for this question (option A). The remaining 3 option texts were merged into the correct_answer_text.

## Pattern Observations

| Pattern | Present? | Detail |
|---------|----------|--------|
| E-answer corruption | ✅ | 5/50 questions with answer ≥ E but only A-D options (10%) |
| Wrong-standard-answer | ✅ | 4 questions (DABT-1528, 1529, 1559, 1568) with DB answers contradicting standard toxicology |
| Matching-test scramble | ❌ | 0 matching items in this batch |
| "EXCEPT" reversal | ❌ | No clear reversal pattern; DABT-1568 is the closest (ambiguous false statement) |
| Parsing issue (merged options) | ✅ | 1 question (DABT-1529) |
| Zero stored options | ❌ | None found |

## Reference Chapter

All questions in this batch are best verified against:
- **Casarett & Doull Ch.3 "Mechanisms of Toxicity"** — covers redox cycling (DABT-1519), electrophile formation/detoxication (1520-1523), free radicals (1525, 1533-1535, 1554-1555), covalent binding (1526), receptor interactions (1527-1529), mitochondrial toxicity (1531-1532, 1539-1540), cell death (1535, 1538, 1549, 1558), calcium signaling (1533), heat-shock stress response (1544), hypoxia (1546), oncogenes (1547-1548), tissue regeneration (1541), distribution (1550-1551), bioactivation (1552-1553), DNA damage (1561), lipid peroxidation (1563), PPAR receptors (1565), RAR (1566), brown adipose tissue (1567), and glutathione (1568).
- **Casarett & Doull Ch.9 "Drug Metabolism"** — for bioactivation, detoxication, and conjugation pathways (1521-1522, 1552-1553, 1559)
- **Casarett & Doull Ch.1 "Introduction and Historical Perspective"** — foundational mechanism concepts

## Prevention Checklist for Future Domain II Batches

1. **Source_file_id check — 2000Q Bank (id=2):** Assume Domain II questions have ~10-15% error rate. Most reliable: TCA cycle, redox cycling, and free radical questions. Least reliable: receptor-pairing questions (especially "which pair is incorrect" format).
2. **Receptor-pairing questions:** The 2000Q Bank has reliable receptor-ligand knowledge from Chapter 1 questions but the matching/extraction format introduces errors. Always verify against C&D Ch.3 receptor tables.
3. **"Enzyme that repairs X" / "Protein that does Y" questions:** These single-definition questions are prone to column-shift errors. Verify the DB-stored answer against C&D Ch.3 before accepting.
4. **Glutathione questions (DABT-1568 pattern):** The distinction between "substrate" and "co-substrate" for GPx is a known source of ambiguity. Expect nuanced questions about GSH's role.
5. **E-answer pattern:** ~10% of batch27 has answer letter E with only A-D options. Follow the existing pattern from batch6/9/11: verify each against standard toxicology. Most are valid as "none/all of the above," but some require re-derivation.
6. **General quality:** Domain II questions from the 2000Q Bank are significantly better than Domain IV questions processed in batches 11-25. The extraction likely came from a cleaner sub-source (Chapter 1 General toxicology vs. organ-system specific chapters). Treatment: high confidence for mechanism/biochemistry questions, moderate-high for receptor-pairing questions, moderate for enzyme-definition questions.
