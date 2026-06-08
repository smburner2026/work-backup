# Batch 29 — Food Safety / Applied Toxicology (Domain IV) + Analytical (Domain I)

## Overview

- **Batch ID:** 29
- **Questions:** DABT-1619 to DABT-1668 (50 questions)
- **Source:** 2000Q Bank (source_file_id=2)
- **Date reviewed:** 2026-05-20
- **Domains:** Domain IV (47 Qs: DABT-1619-1665), Domain I (3 Qs: DABT-1666-1668)

## Results Summary

| Category | Count | Notes |
|----------|-------|-------|
| Standard MCQs (clean) | 38 | DABT-1619-1652, DABT-1654-1656 — all correct answer keys |
| Domain I questions (clean) | 3 | DABT-1666-1668 — analytical tox, clean data |
| Matching items (single-option, wrong associations) | 9 | DABT-1657-1665 — all stored associations are wrong |
| Question-answer text mismatch | 1 | DABT-1643 |
| Parsing corruption (options crammed) | 1 | DABT-1652 |
| Severe truncation (question + options) | 1 | DABT-1653 |

**Overall discrepancy rate:** 12/50 (24%) — moderate, similar to batch22-batch24.

---

## 1. Matching Test Items — Single-Option Storage (DABT-1657 to DABT-1665)

All 9 items follow the same single-option storage pattern seen in every prior matching-test batch from source_file_id=2: only one row in `answer_options` (just the stored correct answer). Most stored associations are toxicologically wrong.

| ID | Question Text (Column A) | Stored Match | Correct Association |
|----|--------------------------|-------------|-------------------|
| DABT-1657 | E. coli | I (unknown letter, no stored text) | Enterotoxin-producing bacterium (Shiga toxin, LT/ST) |
| DABT-1658 | ciguatera poisoning | H → "GRAS substance" (wrong) | Dinoflagellate *Gambierdiscus toxicus* → ciguatoxins |
| DABT-1659 | endotoxin | C → "gram-negative bacterial toxin" (correct) | ✅ Correct — LPS is a defining feature of gram-negative bacteria |
| DABT-1660 | emetic toxin | G → "enzyme" (wrong) | *B. cereus* cereulide — cyclic dodecadepsipeptide K⁺ ionophore, NOT an enzyme |
| DABT-1661 | fluoride | J → "apple products" (wrong) | Patulin (mycotoxin in moldy apples) — fluoride is associated with tea, water, dental products |
| DABT-1662 | scombroid poisoning | A → "beets" (wrong) | Spoiled fish (mahi-mahi, tuna) → histamine from bacterial histidine decarboxylation |
| DABT-1663 | iron oxide | B → "B. cereus" (wrong) | Iron oxide is a food color additive (Fe₂O₃/Fe₃O₄), not a microorganism |
| DABT-1664 | rennet | D → "dinoflagellates" (wrong) | Rennet is a milk-coagulating enzyme complex (chymosin) from calf stomach |
| DABT-1665 | patulin | E (no stored text) | Mycotoxin from *Penicillium expansum* in moldy apple products |

**Only 1/9 stored associations is correct** (DABT-1659: endotoxin → gram-negative bacterial toxin).

**Pattern:** Unlike the circular permutation found in batch19 (pesticides matching) or random misassignment in batch28 (neuropharmacology), the batch29 matching errors appear to be a **different column-mapping corruption** during CSV import. The correct pairs for items like ciguatera→dinoflagellates, emetic toxin→B. cereus, scombroid→mahimahi, rennet→enzyme, and patulin→apple products all exist as option_text values in the database — but assigned to the WRONG question IDs. This suggests a multi-position column shift or row misalignment during the extraction.

### Writing Explanations for These Items

Format as: **"The DB-stored match is X → Y (which is toxicologically incorrect). **Correct association: X → Z** (explain toxicology)..."**

---

## 2. Question-Answer Text Mismatch — DABT-1643

**Question text:** "Solanine and chaconine are produced in _____."
**Correct answer (stored):** C: "raise LDL cholesterol"
**Options:** A: increase blood glucose, B: raise HDL cholesterol, C: raise LDL cholesterol, D: raise blood pressure

The question asks for a **source/production site** (potatoes, Solanaceae), but the answer options are all about **metabolic effects**. The stored answer "raise LDL cholesterol" relates to solanine's effect on lipid metabolism in some animal studies. This appears to be a **text corruption** where the wrong set of answer options was attached to this question, or the question text was replaced with text from a different question.

DABT-2943 in the same database has the extensive text about potato glycoalkaloids (α-solanine, α-chaconine, SGA, LD50 values) with no answer options stored — suggesting DABT-1643 and DABT-2943 may have had their question texts or option sets swapped during extraction.

---

## 3. Parsing Corruption — DABT-1652

**Question:** "All of the following statements are true regarding botulinum toxin except _____."

All 4 answer options are concatenated into a single `answer_options` row:
- `option_letter`: "A"
- `option_text`: "It is heat resistant to 150 ˚C. B. It is a zinc metalloprotein. C. The lethal dose is approximately 1 nanogram. D. It is structurally similar to tetanus toxin."

The correct answer (A: "It is heat resistant to 150 ˚C") IS correctly identified — botulinum toxin is heat-labile, not heat-resistant. However, the parsing failed to split the options into separate rows. This is the same "crammed into option A" pattern seen in DABT-1070 (batch18), DABT-1254 (batch21), and others from source_file_id=2.

---

## 4. Severe Truncation — DABT-1653

**Question text (complete):** "A common feature of toxins produced by"
**Answer options stored:**
- B: "cereus is _____."
- C: "perfringens,"
- E: "coli, and"

The full question was likely: "A common feature of toxins produced by *Bacillus cereus*, *Clostridium perfringens*, and *Escherichia coli* is _____." The question text, option letters (A, D missing), and option texts are all truncated or corrupted during extraction. The likely correct answer relates to these bacteria all producing enterotoxins that cause foodborne diarrheal illness through similar mechanisms (pore-forming enterotoxins, heat-labile/heat-stable toxins).

---

## 5. Standard MCQs — Verified Correct (38 questions)

**Food Additive Regulation (DABT-1619-1630):** All 12 questions about color additives, GRAS, Delaney Clause, DES proviso, ADI calculation, and indirect food additives have correct answer keys consistent with Casarett & Doull Ch. 27. This includes:
- DABT-1619: Color additive usage percentage (false: 50% is an overestimate)
- DABT-1620: ADI = NOAEL ÷ 100 ✓
- DABT-1624: Patulin is NOT GRAS ✓
- DABT-1625: GRAS substances NOT subject to Delaney Clause ✓
- DABT-1629: Xylitol NOT banned ✓
- DABT-1630: Secondary carcinogenesis reasoning ✓

**Drug-Food Interactions (DABT-1631):** Verified correct (vitamin C-carrots is the incorrect pair).

**Food Allergy/Idiosyncrasy (DABT-1632-1635):** All 4 verified correct — including cow's milk-gluten as wrong pair, immune mechanisms NOT involved in idiosyncrasy, anaphylactoid classification for scombroid, and peanuts as most common food anaphylaxis cause.

**Food-Induced Reactions (DABT-1636-1638):** Fava beans→hemolysis, beets→beeturia, sulfite→bronchospasm — all correct.

**Food-CYP / Food-Metabolic Interactions (DABT-1639-1640):** Verified correct — cheese-2D6 is incorrect pair; cycad flour-TEN is incorrect pair (cycad=BMAA/ALS-PDC).

**Natural Plant Compounds (DABT-1641):** Potato has least isothiocyanates/thiocyanates ✓.

**Mycotoxins (DABT-1642):** Fumonisins→cardiac beriberi is wrong pair ✓ (fumonisins cause leukoencephalomalacia/esophageal cancer).

**Shellfish/Marine Toxins (DABT-1644-1645):** Domoic acid→glutamine resemblance ✓. Tetrodotoxin blocks (does not increase) Na⁺ channels ✓.

**Iodine/Pesticides/Arsenic/Nitrate (DABT-1646-1649):** Kelp→iodine excess ✓, EPA regulates pesticides ✓, seafood→arsenic ✓, well water→nitrate ✓.

**N-Nitrosoproline (DABT-1650):** NOT a definite human carcinogen ✓ (used as endogenous nitrosation marker).

**Haff Disease (DABT-1651):** Rhabdomyolysis is the major complication ✓.

**BSE (DABT-1654):** Prion ✓.

**HCA/Acrylamide (DABT-1655):** Produced by cooking ✓.

**De Minimis (DABT-1656):** Risk so small it's of no concern ✓.

---

## 6. Domain I — Analytical Toxicology (DABT-1666-1668, Verified Clean)

All three Domain I questions from the 2000Q Bank have full 4-option sets, correct answer letters, and no parsing issues:

| ID | Topic | Verified |
|----|-------|----------|
| DABT-1666 | Largest group for analytical toxicologists (nonvolatile organic substances) | ✅ |
| DABT-1667 | pH-dependent L-L extraction (acidic drugs in final extract after acidification) | ✅ |
| DABT-1668 | Venom measurement (monoclonal antibodies + immunoassay) | ✅ |

---

## Recommendations for Future Batches

1. **Food Safety questions (Domain IV) from source_file_id=2** now have two clean sub-batches (batch28 at 0/11, batch29 at 38/38 standard MCQs). The matching items from the same bank remain unreliable at ~11% accuracy (1/9 correct in batch29). This is consistent with the broader pattern: standard MCQs within a topic may be clean while matching items from the same source are corrupted.

2. **When a single-option matching question has its "correct_answer_letter" stored but only one option row whose text describes a completely different item** (e.g., ciguatera→GRAS substance), check whether the option text (the stored "match") corresponds to the correct match for ANY OTHER item in the same batch. If so, it's a column-shift artifact.

3. **DABT-1643 pattern** (question asking X, options about Y) should be searched for in the same source: look for a question whose text matches the orphaned options.
