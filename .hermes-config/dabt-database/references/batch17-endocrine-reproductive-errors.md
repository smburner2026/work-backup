# Batch 17 Endocrine Toxicology DB Answer Discrepancies

Batch: DABT-1019 through DABT-1068 (50 questions)
Source: 2000Q Bank (source_file_id=2)
Domain: Domain IV — Applied Toxicology
Topics: Endocrine & Reproductive Toxicology
Date processed: 2026-05-20

## Summary

**Total DB errors/discrepancies: 14 out of 50 questions (28%)**

Of the 14 errors:
- 6 are **letter-E issues** (correct_answer_letter='E' but only A–D options stored — import corruption)
- 13 are **wrong-standard-answer** (the stored answer contradicts established toxicology in Casarett & Doull or Hayes)
- 14 total distinct wrong answers that would mislead a student

---

## Category 1: Wrong Standard Answers (textbook contradicts DB)

### DABT-1019 — Ethinyl Estradiol vs DES in Aquatic Systems

| Field | Value |
|-------|-------|
| Question | "An estrogen receptor agonist present in oral contraceptives that enters aquatic systems from human sewage is _____." |
| Options | A: estradiol, B: DES, C: ethinyl estradiol, D: pregnenolone |
| **DB answer** | **B (DES)** |
| **Correct** | **C (ethinyl estradiol)** |
| Reference | Casarett & Doull Ch.30 (Ecotoxicology, lines 565-567): "ethinyl estradiol, a synthetic estrogen used in birth control pills and observed in municipal effluents and surface waters." |
| Trap | DES is also a synthetic estrogen but was used for miscarriage prevention and livestock, not modern oral contraceptives. |

### DABT-1029 — Plasticizer Causing Delayed Puberty via Leydig Cell Inhibition

| Field | Value |
|-------|-------|
| Question | "A plasticizer that causes delayed puberty in the rat due to Leydig cell inhibition is _____." |
| Options | A: atrazine, B: ketoconazole, C: dibutyl phthalate, D: aniline |
| **DB answer** | **D (aniline)** |
| **Correct** | **C (dibutyl phthalate)** |
| Reference | Casarett & Doull Ch.21 (lines 3785-3802): Phthalates inhibit fetal Leydig cell testosterone and insl-3 synthesis. |
| Trap | Aniline is an aromatic amine used in dye manufacturing — not a plasticizer and not known for Leydig cell inhibition. |

### DABT-1035 — Endocrine Disruptor Effects on Wildlife

| Field | Value |
|-------|-------|
| Question | "Examples of endocrine disruptor effects on wildlife include all of the following except _____." |
| Options | A: sulfur dioxide effects on rodents, B: DDT metabolites in birds, C: PCB effects on fish, D: environmental estrogen effects on domestic animals |
| **DB answer** | **C (PCB effects on fish)** |
| **Correct** | **A (sulfur dioxide effects on rodents)** |
| Reference | Casarett & Doull Ch.30: DDT → eggshell thinning (birds), PCBs → endocrine disruption (fish), phytoestrogens → clover disease (sheep). SO₂ is a respiratory irritant, not an endocrine disruptor. |
| Trap | PCBs are classic EDCs — the trap is selecting them as the exception. |

### DABT-1037 — Estrogenic Effects in Domestic Animals

| Field | Value |
|-------|-------|
| Question | "Adverse estrogenic reproductive effects in domestic animals are produced by feeds contaminated with _____." |
| Options | A: solanaceous glycoalkaloids, B: zearalenone from Fusarium, C: ergot alkaloids from Claviceps, D: nitrosoamines |
| **DB answer** | **C (ergot alkaloids from Claviceps)** |
| **Correct** | **B (zearalenone from Fusarium)** |
| Reference | Hayes Ch.14 (Food Safety): Zearalenone has potent estrogenic activity causing infertility in swine. Ergot alkaloids cause vasoconstriction/ergotism — not estrogenic effects. |
| Trap | Both are mycotoxins, but only zearalenone is estrogenic. |

### DABT-1044 — Lisuride and Bromocriptine Mechanism

| Field | Value |
|-------|-------|
| Question | "Lisuride and bromocriptine act as _____." |
| Options | A: serotonin agonists, B: dopamine agonists, C: cholinergic agonists, D: dopamine antagonists |
| **DB answer** | **D (dopamine antagonists)** |
| **Correct** | **B (dopamine agonists)** |
| Reference | Both are D₂ dopamine receptor AGONISTS used in Parkinson's disease and hyperprolactinemia (Casarett & Doull Ch.20, line 836 mentions bromocriptine). |
| Trap | Because dopamine INHIBITS prolactin, examinees may think prolactin-lowering drugs are dopamine antagonists. They are agonists mimicking dopamine's inhibitory tone. |

### DABT-1045 — Zona Glomerulosa Secretion

| Field | Value |
|-------|-------|
| Question | "The zona glomerulosa of the adrenal gland primarily produces ____." |
| Options | A: sex hormones, B: aldosterone, C: glucocorticoids, D: catecholamines |
| **DB answer** | **C (glucocorticoids)** |
| **Correct** | **B (aldosterone)** |
| Reference | Casarett & Doull Ch.20 (lines 522-527): "The zona glomerulosa is responsible for production of the mineralocorticoid hormone aldosterone." |
| Trap | Classic mnemonic mix-up: GFR = glomerulosa → mineralocorticoids, fasciculata → glucocorticoids, reticularis → androgens. |

### DABT-1047 — Phospholipidosis Induction

| Field | Value |
|-------|-------|
| Question | "All of the following are known to induce phospholipidosis except _____." |
| Options | A: phenobarbital, B: chloroquine, C: triparanol, D: chlorphentermine |
| **DB answer** | **D (chlorphentermine)** |
| **Correct** | **A (phenobarbital)** |
| Reference | Casarett & Doull Ch.13: Phospholipidosis is caused by cationic amphiphilic drugs (CADs) — chlorphentermine is a known CAD inducer. Phenobarbital induces CYP450/SER proliferation, not phospholipidosis. |

### DABT-1049 — Adrenal Cortex Function Tests

| Field | Value |
|-------|-------|
| Question | "An assessment of the function of the adrenal cortex is provided by all of the following except _____." |
| Options | A: 24-hour urine for cortisol, B: 24-hour urine for metanephrine, C: morning serum cortisol, D: cortisol response to exogenous ACTH |
| **DB answer** | **A (24-hour urine for cortisol)** |
| **Correct** | **B (24-hour urine for metanephrine)** |
| Reference | Casarett & Doull Ch.20: Metanephrines are catecholamine metabolites — they assess adrenal MEDULLA function. 24h urine cortisol, morning serum cortisol, and ACTH stimulation test all assess CORTEX function. |

### DABT-1050 — Iodide Transport Protein

| Field | Value |
|-------|-------|
| Question | "The protein responsible for the transport of iodide into the thyroid follicular lumen is _____." |
| Options | A: activin, B: pendrin, C: transportin, D: connexin |
| **DB answer** | **A (activin)** |
| **Correct** | **B (pendrin)** |
| Reference | Casarett & Doull Ch.20: Pendrin (SLC26A4) transports iodide across the apical membrane into the follicular lumen. Activin is a TGF-β growth factor. |
| Trap | NIS (basolateral uptake) is more famous; pendrin (apical efflux) is less commonly tested. |

### DABT-1051 — Thyroxine-Binding Globulin Species Distribution

| Field | Value |
|-------|-------|
| Question | "Thyroxine is bound to thyroxine-binding globulin in all of the following species except _____." |
| Options | A: monkeys, B: rats, C: humans, D: dogs |
| **DB answer** | **C (humans)** |
| **Correct** | **B (rats)** |
| Reference | Casarett & Doull Ch.6 (lines 17805-17806): "in humans and monkeys, circulating T4 is largely bound to TBG. This high-affinity binding protein is not present in rodents." |
| Trap | DB answer actively misinforms — humans DO have TBG. Rats (rodents) lack it. |

### DABT-1054 — Most Common Endocrine Neoplasm

| Field | Value |
|-------|-------|
| Question | "The most common endocrine neoplasm in humans is _____." |
| Options | A: pituitary carcinoma, B: adrenal carcinoma, C: parathyroid carcinoma, D: thyroid carcinoma |
| **DB answer** | **B (adrenal carcinoma)** |
| **Correct** | **D (thyroid carcinoma)** |
| Reference | Thyroid carcinoma accounts for >90% of endocrine malignancies. Adrenal carcinoma is very rare (0.5-2 per million/year). |
| Trap | Selecting a rare tumor as "most common" is a significant epidemiological error. |

### DABT-1056 — RET Proto-Oncogene Mutation

| Field | Value |
|-------|-------|
| Question | "Mutations in the ret proto-oncogene are involved in the hereditary form of _____." |
| Options | A: parathyroid carcinoma, B: adrenal cortex carcinoma, C: medullary thyroid carcinoma, D: islet cell carcinoma of the pancreas |
| **DB answer** | **B (adrenal cortex carcinoma)** |
| **Correct** | **C (medullary thyroid carcinoma)** |
| Reference | RET mutations cause MEN2 including medullary thyroid carcinoma. Adrenal cortex carcinoma is associated with p53 (Li-Fraumeni). |
| Trap | Both involve endocrine organs, but only MTC is linked to RET. |

### DABT-1060 — Experimental Diabetes Agent

| Field | Value |
|-------|-------|
| Question | "Experimental diabetes mellitus in animals can be produced by destroying beta cells with _____." |
| Options | A: chloramphenicol, B: streptozocin, C: phenylbutazone, D: phenyramidol |
| **DB answer** | **C (phenylbutazone)** |
| **Correct** | **B (streptozocin)** |
| Reference | Casarett & Doull Ch.20 (lines 2414-2415): "pancreatic beta cell toxins are alloxan and streptozotocin (STZ)." |
| Trap | Streptozocin sounds antibiotic-like, which may cause doubt, but it is the standard chemical diabetes model. |

### DABT-1067 — Growth Hormone Level Increases

| Field | Value |
|-------|-------|
| Question | "All of the following will increase growth hormone levels except _____." |
| Options | A: arginine, B: L-DOPA, C: somatostatin, D: clonidine |
| **DB answer** | **B (L-DOPA)** |
| **Correct** | **C (somatostatin)** |
| Reference | Casarett & Doull Ch.20: Arginine, L-DOPA, and clonidine are used as GH stimulation tests. Somatostatin is the GH-inhibiting hormone. |
| Trap | L-DOPA is a well-established GH secretagogue — its selection as the exception is an obvious error. |

---

## Category 2: Letter-E Issues (correct_answer_letter='E' with only A-D options)

Six questions have `correct_answer_letter='E'` but only A-D options exist. The correct answer can be reconstructed from toxicology knowledge:

| QID | DB Ans | Correct | Correct Text | Rationale |
|-----|--------|---------|--------------|-----------|
| DABT-1025 | E | **C** | hypertension | Least directly linked to decreased male fertility vs orchitis, varicocele, Klinefelter's |
| DABT-1033 | E | **D** | 8 days | Fertilization-to-implantation ≈ 8 days (human) |
| DABT-1034 | E | **B** | sexual dysfunction at age 50 | Not part of TDS hypothesis (sperm counts, cryptorchidism, testicular cancer are) |
| DABT-1041 | E | **C** | peptide hormones | Only peptide/protein hormones stored in secretory granules; steroids made on demand |
| DABT-1053 | E | **A** | guinea pig | Least sensitive species to sulfonamide goiter; rats most sensitive |
| DABT-1064 | E | **B** | aspartate transaminase | AST is liver enzyme, not thyroid metabolic effect test |

---

## Error Statistics

| Category | Count |
|----------|-------|
| Wrong Standard Answer (textbook contradicts DB) | 13 (26%) |
| Letter-E import corruption (E with no option) | 6 (12%) |
| Overlap (wrong answer that is also letter E) | 5 |
| **Total distinct errors** | **14 (28%)** |

## Key Error Patterns

1. **Fundamental endocrine physiology reversals** — DABT-1044 (agonist vs antagonist), DABT-1045 (zona glomerulosa), DABT-1050 (activin vs pendrin), DABT-1049 (medulla vs cortex tests) — these teach basic concepts backward.

2. **Species-specific knowledge errors** — DABT-1051 (rats lack TBG, not humans) — the DB answer actively misinforms about a tested species difference.

3. **Endocrine neoplasm epidemiology** — DABT-1054 (most common = thyroid, not adrenal), DABT-1056 (RET → MTC, not adrenal cortex).

4. **Experimental model errors** — DABT-1060 (STZ, not phenylbutazone for diabetes induction).

5. **Letter-E import corruption** — Same 2000Q Bank bug seen in every prior batch: ans='E' with no matching option.

## Reference Chapters for Verification

| Topic | Reference | Notes |
|-------|-----------|-------|
| Endocrine Toxicology | Casarett & Doull Ch.20 | Pituitary, adrenal, thyroid, pancreas |
| Reproductive Toxicology | Casarett & Doull Ch.21 | Testicular toxicity, phthalate syndrome, TDS |
| Ecotoxicology / EDCs | Casarett & Doull Ch.30 | Ethinyl estradiol, wildlife EDC effects |
| Developmental Toxicology | Casarett & Doull Ch.10 | Fertilization-implantation timeline |
| Biotransformation / Species Diff. | Casarett & Doull Ch.6 | TBG species distribution |
| Food Toxicology / Mycotoxins | Hayes Ch.14 | Zearalenone, ergot alkaloids |
