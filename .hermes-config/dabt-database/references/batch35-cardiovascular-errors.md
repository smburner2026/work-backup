# Batch35: Cardiovascular Toxicity (Domain IV) — DB Answer Errors

**Batch:** batch35 (DABT-1919 to DABT-1968)
**Source:** 2000Q Bank (source_file_id=2) — comprehensive question bank
**Domain:** Domain IV (Applied Toxicology)
**Topic:** Cardiovascular Toxicity (Cardiac Toxicology)
**Error rate:** ~10/50 (20%) — moderate; lower than neuro (58%) or lung (48%) but higher than metals (20%)

**Primary reference chapter:** Casarett & Doull Ch.18 "Toxic Responses of the Heart and Vascular System" (formerly Ch.17 in older editions)

---

## Definite Errors (7)

These DB answers clearly contradict standard toxicology/cardiology:

| DB ID | DB Answer | Correct Answer | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1928 | A: CK-MM | **D: C-reactive protein** | CV inflammation biomarker | CK-MM (creatine kinase, muscle isoform) is a marker of muscle injury, NOT a biomarker of inflammation predicting cardiac events. C-reactive protein (hs-CRP) is the established inflammatory biomarker for cardiovascular risk stratification in asymptomatic individuals per AHA/CDC guidelines. (C&D Ch.18) |
| DABT-1929 | C: increase in systemic BP | **A: unbalanced Purkinje fiber distribution** | Arrhythmia in hypertrophy | The primary electrophysiological mechanism for arrhythmia secondary to cardiac hypertrophy is the heterogeneous distribution of the conduction system (Purkinje fibers) in the remodelled ventricle, creating repolarization gradients that predispose to reentry. Increased BP is a *cause* of hypertrophy, not a mechanism for arrhythmia *from* hypertrophy. (C&D Ch.18) |
| DABT-1951 | A: AST is most sensitive MI marker | **D: none of the above** (or B/C false) | MI biomarkers | Aspartate transaminase (AST) is NOT the most sensitive marker of myocardial damage — cardiac troponin (I or T) is the gold standard. AST was used historically but is non-specific (also elevated in liver disease, muscle injury). The DB labels A as correct, but per modern cardiology, A is false. (C&D Ch.18; universal definition of MI) |
| DABT-1961 | C: chloride channel blockers | **B: potassium channel blockers** | Class III antiarrhythmics | Vaughan Williams Class III antiarrhythmics (sotalol, amiodarone, dofetilide, ibutilide) prolong the action potential duration by blocking the rapid delayed rectifier potassium current (IKr/hERG). They are definitively K⁺ channel blockers, not Cl⁻ channel blockers. (C&D Ch.18; Vaughan Williams classification) |
| DABT-1966 | homocysteine → E: cardiac hemangiosarcomas | **No established match** | Matching test | Homocysteine is an established independent risk factor for atherosclerosis, venous thromboembolism, and endothelial dysfunction — NOT for cardiac hemangiosarcomas. The stored match is toxicologically incorrect and reflects a source-scrambled matching-test entry. See matching-test pattern below. |
| DABT-1967 | beta-amyloid → A: abortions and abruption placentae | **No established match** | Matching test | Beta-amyloid (Aβ) is a peptide involved in Alzheimer's disease pathogenesis — it has no established causal link to abortions or placental abruption. Cadmium and other heavy metals are associated with placental toxicity. This match is toxicologically incorrect. |
| DABT-1968 | carbon disulfide → A: noncirrhotic portal hypertension | **No established match** | Matching test | Carbon disulfide (CS₂) is an industrial solvent classically associated with accelerated atherosclerosis, coronary heart disease, peripheral neuropathy, and parkinsonism — NOT noncirrhotic portal hypertension. Vinyl chloride and arsenic are linked to hepatic angiosarcoma and portal hypertension, not CS₂. |

---

## Probable Errors (3)

These DB answers are likely wrong but have some ambiguity in how the question is framed:

| DB ID | DB Answer | Likely Correct | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1922 | C: dilation | **A: fetal gene expression** or **D: all of the above** | Hypertrophy vs. failure | Dilation is a hallmark of decompensated heart failure, NOT of hypertrophy. Fetal gene expression (A) and apoptosis (B) are both associated with pathological hypertrophy. The DB may have intended "adverse remodeling" rather than dilation. (C&D Ch.18) |
| DABT-1939 | A: ischemic cardiomyopathy | **D: adaptive hypertrophy** | Collagen/fibrosis | Ischemic cardiomyopathy DOES involve collagen deposition (replacement fibrosis after infarct + reactive fibrosis in remote myocardium). Adaptive (physiologic) hypertrophy from exercise or pregnancy is the entity NOT associated with collagen accumulation. (C&D Ch.18) |
| DABT-1958 | E: (unlisted exception) — Statement A accepted as true | **A is the exception** (duration IS related) | Alcoholic cardiomyopathy | Statement A: "Alcoholic cardiomyopathy is unrelated to the duration of alcohol exposure" is FALSE — it IS related to both dose and duration (>80 g/day for >5 years). The DB accepts A as true (making it not the exception), but per C&D Ch.18, alcoholic cardiomyopathy is dose- and duration-dependent. The intended exception should be A. |

---

## Pitfall/Borderline (2)

These have reasonable ambiguity in the question format but warrant attention:

| DB ID | Issue | Explanation |
|-------|-------|-------------|
| DABT-1931 | Letter E with only A–D options | Question asks how toxicants cause cardiac toxicity at the cellular level. D (increasing intracellular calcium) is the standard textbook mechanism (calcium overload → mPTP opening → cell death). The DB stores E (likely "all of the above" or "none of the above" as an implicit option). If E = "all of the above," then it includes D as correct — plausible. If E = "none of the above," then the DB answer conflicts with standard cardiotoxicology. |
| DABT-1955 | Letter E with only A–D options | Question asks which statement about adaptive vs. maladaptive hypertrophy is false. Statement B ("Both are associated with accumulation of collagen") is false because adaptive hypertrophy does NOT involve fibrosis. DB stores E as exception. The correct exception among A–D is B. |

---

## Systematic Error Patterns

### Pattern A: Matching-Test Multi-Position Offset

The 4 matching-test items (DABT-1965 to DABT-1968) follow the same corruption pattern seen in batch29 (food toxins): **the stored associations are toxicologically wrong and appear to be displaced from a multi-column source**. Unlike batch19's circular permutation (+1 shift), these have no discernible single-offset pattern — likely column misalignment during extraction.

Evaluation of all 4:
- **DABT-1965** (oral contraceptives → A: metal associated with hypertension): Oral contraceptives increase hypertension risk via RAAS activation and fluid retention, but the stored match references "metal" — this is odd phrasing. Cadmium IS associated with hypertension; the pairing may reflect a misaligned row.*
- **DABT-1966** (homocysteine → E: cardiac hemangiosarcomas): No known mechanism linking homocysteine to hemangiosarcoma. **Definitely wrong.**
- **DABT-1967** (beta-amyloid → A: abortions and abruption placentae): No known link. **Definitely wrong.**
- **DABT-1968** (carbon disulfide → A: noncirrhotic portal hypertension): CS₂'s classic CV effects are atherosclerosis/CHD. **Definitely wrong.**

**Recommendation:** For batch35 matching items, assume all 4 stored associations are unreliable and write explanations based on the standard toxicology of each term, noting the discrepancy.

### Pattern B: Biomarker Confusion

The 2000Q Bank has systematic errors in cardiovascular biomarker questions:
- **DABT-1928**: CK-MM called an inflammatory biomarker → should be CRP
- **DABT-1951**: AST called the most sensitive cardiac marker → should be troponin
- **DABT-1963**: E answer (troponin) — the DB stores E but it's correct
- **DABT-1964**: DB says serum CPK is indicator of fluid overload → should be BNP

This suggests the source material used outdated biomarker knowledge from before troponin and BNP became the standard of care.

### Pattern C: Antiarrhythmic Drug Classification Error

**DABT-1961**: Class III antiarrhythmics stored as chloride channel blockers. This is a fundamental pharmacology error — the Vaughan Williams classification is standard across all pharmacology and toxicology textbooks:
- Class I = Na⁺ channel blockers
- Class II = β-blockers
- Class III = K⁺ channel blockers (prolong repolarization)
- Class IV = Ca²⁺ channel blockers

Always verify drug classification questions against C&D Ch.18 or Goodman & Gilman.

### Pattern D: Letter-E Corruptions with Only A–D Options

| DB ID | Implicit Answer | Question Topic |
|-------|----------------|----------------|
| DABT-1931 | D (increasing intracellular calcium) | Cellular cardiotoxicity mechanism |
| DABT-1955 | B (adaptive hypertrophy NOT associated with collagen) | Adaptive vs. maladaptive hypertrophy |

Both are plausible as "none of the above" type E answers but should be cross-verified.

---

## Key Lessons for Future Cardiovascular Toxicity Batches

1. **Cardiovascular biomarkers are a weak area for the 2000Q Bank.** The source material appears to use pre-2000 biomarker knowledge. Troponin, BNP, and hs-CRP are the modern standards; the DB may reference AST, CK-MM, and CK-MB as if they were still first-line.

2. **Antiarrhythmic drug classification (Vaughan Williams) must be independently verified.** The DB confused Class III (K⁺ blockers) with Cl⁻ channel blockers — a basic pharmacology error not seen in other organ systems.

3. **Matching-test items from the same 2000Q Bank cardiovascular test** are almost certainly scrambled (same pattern as batch7 antidotes, batch19 pesticides, batch29 food toxins, batch30 analytical tox). All 4 batch35 matching items have toxicologically implausible associations.

4. **Hypertrophy vs. heart failure distinctions** are subtle and the DB sometimes blurs them. Dilation marks the transition to failure, not hypertrophy itself.

5. **Alcoholic cardiomyopathy** questions may have the duration/dose relationship inverted in the DB.

6. **Class I antiarrhythmics (DABT-1959)** — the CAST trial finding (proarrhythmia in post-MI patients) is a critical high-yield fact that the DB correctly captures.

7. **Anthracycline cardiotoxicity (DABT-1933)** — the DB correctly identifies inhibition of angiogenesis as one mechanism. This is well-established per C&D Ch.18 and should not be second-guessed.

---

## Self-Review Checklist for Cardiovascular Toxicity Batches

- [ ] All 50 entries present (DABT-1919 through DABT-1968)
- [ ] All domain = "Domain IV"
- [ ] Matching-test items (DABT-1965–1968): explanations describe the TERM's actual toxicology, not the stored match
- [ ] Antiarrhythmic class questions (DABT-1959–1961): Vaughan Williams classification is correct
- [ ] Biomarker questions (DABT-1928, 1951, 1963, 1964): verified against modern standards
- [ ] Hypertrophy vs. heart failure (DABT-1922, 1939, 1941, 1942, 1955): dilation = failure, not hypertrophy
- [ ] Alcoholic cardiomyopathy (DABT-1958): duration/dose dependency is affirmed
