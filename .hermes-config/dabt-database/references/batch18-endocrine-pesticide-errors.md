# Batch 18 — Endocrine Toxicology & Pesticides: DB Answer Audit

**Batch:** 50 questions (DABT-1069 to DABT-1118)
**Topics:** Endocrine Toxicology (24 Qs, DABT-1069-1092), Pesticides – Insecticides (26 Qs, DABT-1093-1118)
**Source:** 2000Q Bank (source_file_id=2)
**Domain:** All Domain IV / Applied
**Explanations written:** 2026-05-20

## Summary

| Metric | Count |
|--------|-------|
| Total questions | 50 |
| DB answers matching standard toxicology | ~30 (60%) |
| E-answer with only A-D options (plausible, e.g., "none of the above") | ~10 (20%) |
| DB answer contradicts Casarett & Doull reference text | ~5 (10%) |
| Parsing issues (concatenated options, missing options) | 2 (4%) |
| Answer key quirk (debatable, schema-specific) | ~4 (8%) |

## Parsing Issues

### DABT-1070 — All 4 options crammed into option A

The `answer_options` table has only 1 row for this question (option_letter="A"), whose text contains all four statements concatenated:

```
"The cytosolic calcium concentration is 10,000 times higher than the extracellular fluid concentration. B. Ninety-nine percent of body calcium is present in bone. C. Free calcium in serum will increase in the presence of acidosis. D. Protein-bound calcium is predominantly on albumin."
```

The actual separate options were lost during import. The DB's `correct_answer_letter` = D (designating "Protein-bound calcium is predominantly on albumin" as the false statement). Note: physiologically, protein-bound calcium IS predominantly on albumin (~80-90%), and the cytosolic/extracellular ratio statement in A is backwards (extracellular Ca²⁺ is ~10,000× higher than cytosolic, not the reverse), making A the more obvious false statement.

### DABT-1092 — Zero options stored

Question text: "All of the following are true of raloxifene except _____."
The `answer_options` table has 0 rows for this question. The `correct_answer_letter` = B, but no options are available to reconstruct which statement B refers to.

## Known DB Errors (DB answer contradicts Casarett & Doull)

### DABT-1081 — Adrenal medullary tumors

| Field | Value |
|-------|-------|
| DB answer | A — "adrenal adenomas" |
| Casarett & Doull (Ch.20) | "Larger benign adrenal medullary proliferative lesions are designated **pheochromocytomas**." |
| Assessment | Answer wrong. Adrenal adenomas are cortical tumors. Pheochromocytomas arise from medullary chromaffin cells. |

### DABT-1100 — Cause of death in acute OP poisoning

| Field | Value |
|-------|-------|
| DB answer | C — "status epilepticus" |
| Standard teaching | Respiratory failure (muscarinic bronchorrhea/bronchospasm + nicotinic diaphragmatic paralysis + central depression) is the usual cause of death |
| Assessment | DB answer contradicts standard clinical toxicology. Status epilepticus can occur but is not the primary cause of mortality. |

### DABT-1107 — Sodium fluoroacetate MOA

| Field | Value |
|-------|-------|
| DB answer | A — "inhibition of glucose-6-phosphate dehydrogenase" |
| Casarett & Doull (Ch.22) | Sodium fluoroacetate → fluorocitrate → **inhibits aconitase** in the TCA cycle → citrate accumulation |
| Assessment | Answer wrong. G6PD is in the pentose phosphate pathway; fluoroacetate targets the TCA cycle. |

### DABT-1095 — Most commonly used rodenticide

| Field | Value |
|-------|-------|
| DB answer | C — "rotenone" |
| Standard practice | Anticoagulants (warfarin, brodifacoum) are the most widely used rodenticides worldwide |
| Assessment | Answer questionable. Rotenone is primarily an insecticide/piscicide, not a rodenticide. Anticoagulants dominate rodenticide formulations. |

### DABT-1096 — Plant growth regulator

| Field | Value |
|-------|-------|
| DB answer | D — "asulam" |
| Standard classification | Gibberellic acid (A) is the textbook plant growth regulator (PGR). Asulam is an herbicide (carbamate). |
| Assessment | Answer questionable. Asulam is not classified as a PGR in standard references. |

## Debatable / Schema-Specific Answers

### DABT-1086 — Thyroid cancer gender dimorphism

| Field | Value |
|-------|-------|
| DB answer | A — "Androgens play a role in tumorigenesis" |
| Interpretation | Thyroid cancer is 2-3× more common in women, suggesting estrogen involvement. The answer key designating androgens may reflect androgen receptor data in certain thyroid cancer subtypes or a male-specific risk factor. |

### DABT-1116 — Imidacloprid selective toxicity

| Field | Value |
|-------|-------|
| DB answer | B — "It has selective toxicity for insects over mammals" is designated as the FALSE statement |
| Standard pharmacology | Neonicotinoids are explicitly designed for selective toxicity — they bind insect nAChRs with much higher affinity than mammalian nAChRs |
| Assessment | The answer key's designation of selective toxicity as the exception contradicts neonicotinoid pharmacology. |

### DABT-1112 — Paraquat characteristics

| Field | Value |
|-------|-------|
| DB answer | D — "is transported into the lung" (designated TRUE) |
| Standard fact | Paraquat IS actively transported into the lung via the polyamine transport system |
| Assessment | D is factually correct. The issue is the question structure — if asking "which is TRUE," D is valid. But if B ("interferes with calcium channels") or C ("is well absorbed orally") were also plausible options, the answer may depend on question framing. |

### DABT-1115 — DEET characteristics

| Field | Value |
|-------|-------|
| DB answer | A — "is cardiotoxic" (designated TRUE) |
| Standard fact | DEET has an excellent safety record; neurotoxicity is the rare serious effect, not cardiotoxicity |
| Assessment | The answer key's designation of cardiotoxicity as true is atypical. |

### DABT-1109 — Elemental sulfur primary toxicity

| Field | Value |
|-------|-------|
| DB answer | D — "polycythemia" |
| Standard fact | Elemental sulfur is low-toxicity; primary effects are dermal/respiratory irritation. Polycythemia is not a known effect. |
| Assessment | Likely a misassociation with H₂S or other sulfur compounds. |

## E-Answer Pattern (No Option E in Answer_Options)

The following questions have `correct_answer_letter = "E"` but the DB only stores options A-D in `answer_options`. In most cases, E plausibly represents "none of the above" — this is common in the 2000Q Bank where answer keys used "E" as a catch-all:

| Question | DB Answer | Options | Verdict |
|----------|-----------|---------|---------|
| DABT-1069 | E | A-D (hormone-class pairs) | Plausible — TRH (tripeptide) is incorrectly paired as biogenic amine, making C the obvious exception. E likely = "none of the above" or key artifact. |
| DABT-1078 | E | A-D (phenobarbital statements) | All four statements are true per Casarett Ch.20 (species difference: rat thyroid vs human liver). E is likely the intended answer. |
| DABT-1082 | E | A-D (phenobarbital, bromocriptine, cobalt, none of the above) | E = "none of the above" makes sense — none of the listed agents causally cause human pituitary tumors. |
| DABT-1085 | E | A-D (polio virus, rifampin, radiation exposure, TCDD) | Radiation exposure (C) is clearly correct. E likely = key artifact. |
| DABT-1089 | E | A-D (pancreas, parathyroid, adrenal, pituitary) | The thyroid is the most commonly affected endocrine organ, which isn't listed. E likely = "none of the above" or key artifact. |
| DABT-1102 | E | A-D (parathion, ANTU, aldicarb, resmethrin) | Resmethrin (pyrethroid) has the lowest oral LD50 (~500+ mg/kg). E likely = key artifact. |
| DABT-1105 | E | A-D (arrhythmias, seizures, NMJ action, delayed neuropathy) | Option C (acts at NMJ) is a genuine advantage of 2-PAM over atropine. E likely = key artifact. |
| DABT-1111 | E | A-D (propoxur, dichlorvos, fenvalerate, heptachlor) | Dimethylphosphate is an OP metabolite, so dichlorvos (B) should be correct. E likely = key artifact. |
| DABT-1113 | E | A-D (bone marrow toxic, cataracts, teratogenic, liver accumulation) | Diquat causes cataracts in animals (B is true). E likely = key artifact. |
| DABT-1117 | E | A-D (preemergent herbicide, pheromone, recently introduced pesticide, banned fungicide) | Lepidoptera is an insect order, none of the classifications fit. E = valid "none of the above." |

## Reference Chapters for Endocrine Toxicology & Pesticides

| Topic | Primary Reference | Key Sections |
|-------|------------------|-------------|
| Endocrine Toxicology (general) | Casarett & Doull Ch.20 (3,203 lines) | Hormone classes, pituitary, adrenal cortex/medulla, thyroid, parathyroid, pancreas |
| Pesticides (general) | Casarett & Doull Ch.22 (6,934 lines) | Organophosphates, carbamates, organochlorines, pyrethroids, neonicotinoids, bipyridyls, rodenticides, fungicides |

**Hayes Ch.36** "Toxicology of the Endocrine System" is the alternative reference for endocrine topics.
