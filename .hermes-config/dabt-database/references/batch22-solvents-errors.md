# Batch 22 Errors — Solvents & Hydrocarbons (Domain IV)

## Source
**2000Q Bank** (source_file_id=2). Questions DABT-1269 to DABT-1318 (50 questions, the second half of the Solvents & Hydrocarbons chapter from the 2000Q Bank).

## Summary

| Metric | Count |
|--------|-------|
| Total questions examined | 50 |
| Wrong-standard-answer | ~7 (14%) |
| Letter-E corruption | 6 (12%) |
| Zero-option questions | 0 |
| Scrambled matching items | 1 (DABT-1317) |

---

## Letter-E Corruptions (6 items)

These questions have `correct_answer_letter='E'` but only A-D options exist in `answer_options`. The 'E' is a parsing artifact from the 2000Q Bank CSV import.

| ID | Source Letter-E | Likely Correct Answer | Rationale |
|----|----------------|----------------------|-----------|
| DABT-1271 | E (only A-D) | **D** (all of the above) | Methanol toxicity treatment includes hemodialysis, sodium bicarbonate, AND methylpyrazole/fomepizole. All three are standard of care — "all of the above" (D) is correct. |
| DABT-1274 | E (only A-D) | **B** (phenol) | Toluene metabolism: toluene → benzyl alcohol → benzaldehyde → benzoic acid → hippuric acid. Phenol is NOT a metabolite of toluene — it is from benzene ring hydroxylation. B is the correct exception. |
| DABT-1278 | E (only A-D) | **B** (increased risk of cancer) | ALDH2 deficiency → acetaldehyde accumulation (IARC Group 1 carcinogen) → elevated cancer risk in drinkers. The aversive flushing reaction reduces alcoholism rates (A is false). |
| DABT-1299 | E (only A-D) | **B** (osteosclerosis) | Chronic fluoride exposure → skeletal fluorosis (osteosclerosis). Osteosarcoma has animal evidence but is not the classic human finding from HF. Hepatitis and anemia are not characteristic. |
| DABT-1305 | E (only A-D) | **C** (toluene) | Chronic toluene abuse → hypokalemia + normal anion gap metabolic acidosis. Toluene metabolites (hippurate) consume bicarbonate; renal adaptation can produce normal gap acidosis. |
| DABT-1312 | E (only A-D) | **None clearly — all A-D are true** | All four listed statements about organic solvents are true (GI absorption, hydrophilic/hydrophobic steady-state kinetics, rodent vs human dermal absorption, corn oil effect on CCl4). The question asks for an exception but none of A-D is false. E likely represents a corrupted 5th option or the question is flawed. |

---

## Wrong-Standard-Answers (7 items)

### DABT-1275 — Toluene Primary Target Organ
**Question:** "The primary toxic target organ for toluene is _____."
**Options:** A: liver, B: lung, C: CNS, D: adrenal gland
**DB says:** B (lung)
**Correct:** **C** (CNS)
**Evidence:** Toluene is primarily a neurotoxicant — chronic abuse causes encephalopathy, cerebellar degeneration, optic neuropathy, and cognitive deficits. The CNS is the most sensitive target organ. The common trap is identifying the portal of entry (lung) as the target organ. (Casarett & Doull Ch.24, Toluene section)

### DABT-1283 — Benzene Cancer Association
**Question:** "Benzene exposure has been associated with an increased risk of _____."
**Options:** A: liver cancer, B: renal cell carcinoma, C: acute myelogenous leukemia, D: lung cancer
**DB says:** B (renal cell carcinoma)
**Correct:** **C** (acute myelogenous leukemia)
**Evidence:** Benzene is a well-established cause of AML and other hematopoietic malignancies. Renal cell carcinoma is not a benzene-associated cancer — that is associated with trichloroethylene. Benzene targets bone marrow, not kidney. (Casarett & Doull Ch.24, Benzene section; IARC Group 1)

### DABT-1288 — Cyclic Ether Identification
**Question:** "Which of the following is a cyclic ether?"
**Options:** A: dioxane, B: dioxin, C: styrene, D: A and B
**DB says:** B (dioxin)
**Correct:** **A** (dioxane)
**Evidence:** Dioxane (1,4-dioxane) is a cyclic ether — a six-membered ring with two oxygen atoms (C4H8O2). Dioxin (TCDD) is a polychlorinated dibenzo-p-dioxin — its structure contains two benzene rings connected by a dioxin bridge, but it is NOT classified as a cyclic ether. The trap is confusing the structural term "dioxin" (referring to the ether bridge in its name) with the functional group classification. Option D (A and B) is also incorrect because dioxin is not a cyclic ether. (Casarett & Doull Ch.24)

### DABT-1292 — Percutaneous Absorption of Xylene/Toluene
**Question:** "Percutaneous absorption of xylene and toluene vapors in humans _____."
**Options:** A: is usually insignificant, B: can lead to metabolism in the stratum corneum and production of metabolites that can cause squamous cell carcinoma, C: accounts for about 10% of total body absorption, D: can be equal to pulmonary absorption in a person who is sweating
**DB says:** B ("can lead to metabolism... and SCC")
**Correct:** **A** (is usually insignificant)
**Evidence:** Dermal absorption of volatile organic solvents like xylene and toluene from vapor phase is minimal in humans — typically <1-2% of total uptake compared to inhalation. The statement in B is not supported for these solvents: they are not known to be metabolized in the stratum corneum to SCC-causing metabolites. Option C (10%) overestimates dermal contribution, and D is only true under extreme sweating conditions. (Casarett & Doull Ch.24, Percutaneous Absorption section)

### DABT-1300 — Acrylamide Associated Effects
**Question:** "Acrylamide exposure has been associated with all of the following except _____."
**Options:** A: peripheral neuropathy, B: sweating, C: ataxia, D: hypertension
**DB says:** A (peripheral neuropathy — treating it as NOT associated)
**Correct:** **D** (hypertension — this is the true exception)
**Evidence:** Acrylamide IS a well-established cause of peripheral neuropathy in occupationally exposed humans (distal axonopathy). It also causes autonomic dysfunction with excessive sweating (B ✓) and cerebellar/vestibular ataxia (C ✓). Hypertension (D) is not a classic feature of acrylamide neurotoxicity and is the true exception. The DB answer appears to invert the intended logic. (Casarett & Doull Ch.24, Acrylamide section)

### DABT-1301 — Urinary p-Aminophenol Biomarker
**Question:** "Urinary p-aminophenol is a biologic monitor for exposure to _____."
**Options:** A: benzene, B: toluene, C: aniline, D: xylene
**DB says:** B (toluene)
**Correct:** **C** (aniline)
**Evidence:** p-Aminophenol is the major urinary metabolite of aniline (C6H5NH2), formed via CYP-mediated N-hydroxylation followed by rearrangement. Toluene's urinary biomarker is hippuric acid. Benzene's biomarkers include t,t-muconic acid and S-phenylmercapturic acid. The trap is confusing aromatic amine metabolism with aromatic hydrocarbon metabolism. (Casarett & Doull Ch.24, Aniline section; ACGIH BEI documentation)

### DABT-1311 — Most Frequent VOC in Drinking Water
**Question:** "The most frequently found volatile organic compound (VOC) in finished drinking water supplies in the United States is _____."
**Options:** A: chloroform, B: carbon tetrachloride, C: 1,3-butadiene, D: methylene chloride
**DB says:** B (carbon tetrachloride)
**Correct:** **A** (chloroform)
**Evidence:** Chloroform is the most common trihalomethane (THM) formed during water chlorination as a disinfection byproduct, and is consistently detected at the highest frequency in finished drinking water across the US. Carbon tetrachloride, while historically used and detected, is less commonly found than THMs. 1,3-butadiene and methylene chloride are not typical drinking water contaminants at the same detection frequency. (EPA National Drinking Water Contaminant Occurrence Database; AWWA reports)

---

## Scrambled Matching Items (1 item)

### DABT-1317 — Benzidine Association
**DB says:** benzidine → inorganic lung carcinogen (C)
**Correct:** benzidine → **bladder carcinogen** (organic aromatic amine)
**Evidence:** Benzidine is a known human bladder carcinogen (IARC Group 1). It is an ORGANIC aromatic amine, not inorganic. It causes transitional cell carcinoma of the bladder, not lung cancer. The DB's pairing is wrong on both counts (wrong organ, wrong classification). This is likely a circular permutation artifact where the answer shifted by one position during CSV extraction. (Casarett & Doull Ch.24, Aromatic Amines section)

---

## Additional Wrong-Standard-Answers Identified During Detailed Review

Two more items surfaced during the explanation authoring process:

### DABT-1281 — Chloroform Toxic Metabolite
**DB says:** C (hypochlorous acid)
**Correct:** **B** (phosgene)
**Evidence:** Chloroform (CHCl3) is metabolized by CYP2E1 to trichloromethanol, which spontaneously dehydrochlorinates to phosgene (COCl2). Phosgene is the reactive intermediate that covalently binds cellular macromolecules, depletes glutathione, and causes hepatotoxicity. Hypochlorous acid (HOCl) is an endogenous compound produced by myeloperoxidase in neutrophils — it has nothing to do with chloroform metabolism. (Casarett & Doull Ch.24, Chloroform section)

### DABT-1296 — Vinyl Chloride Effects
**DB says:** B (thyroid dysfunction)
**Correct:** **C** (Raynaud's phenomenon) or **D** (peripheral neuropathy)
**Evidence:** Vinyl chloride monomer is classically associated with acro-osteolysis, Raynaud's phenomenon (a vascular effect), peripheral neuropathy, and hepatic angiosarcoma. Thyroid dysfunction is NOT a recognized effect. The DB-stored answer appears to be a random association with endocrine organs that has no basis in the vinyl chloride toxicology literature. (Casarett & Doull Ch.24, Vinyl Chloride section; IARC Monograph)

---

## Summary of Total Batch 22 DB Errors

| Type | Count |
|------|-------|
| Letter-E corruption | 6 |
| Wrong-standard-answer (confirmed) | 7 |
| Wrong-standard-answer (additional from detailed review) | 2 (DABT-1281, DABT-1296) |
| Scrambled matching item | 1 (DABT-1317) |
| **Total questions with DB issues** | **~13-15 (26-30%)** |

The error rate (~26-30%) is consistent with other 2000Q Bank batches (batch21: 33%, batch20: 20%, batch19: 56%). The most common patterns remain: (1) parsing artifacts producing letter-E with only A-D options, (2) benzene/toluene metabolism pathway confusion, (3) misattributed end-organ effects for industrial chemicals, and (4) scrambled matching-test pairings from CSV extraction shifts.
