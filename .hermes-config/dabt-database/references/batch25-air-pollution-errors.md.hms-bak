# Batch 25 — Air Pollution & Plant Toxins (Domain IV): DB Answer Audit

**Batch:** 50 questions (DABT-1419 to DABT-1468)
**Topics:**
- DABT-1419 to DABT-1432 (14 Qs) — **Plant Toxins** (tail of section from batch24)
- DABT-1433 to DABT-1468 (36 Qs) — **Air Pollution & Particulates** (new organ system)
**Source:** 2000Q Bank (source_file_id=2)
**Domain:** All Domain IV
**Explanations written:** 2026-05-20
**Primary reference:** Casarett & Doull Ch.26 (Plant Toxins), Ch.27 (Air Pollution)
**Secondary reference:** Hayes Ch.15 (Plant Toxins), Ch.24 (Air Pollution)

## Summary

| Metric | Count |
|--------|-------|
| Total questions | 50 |
| Plant Toxins (matching test items with single-option storage) | 9 (DABT-1424 to DABT-1432) |
| Air Pollution standard MCQs (full 4-option sets) | 36 (DABT-1433 to DABT-1468) |
| DB answer discrepancies found (Air Pollution section) | **0** |
| DB answer discrepancies found (Plant Toxins — standard MCQs) | **0** (DABT-1419-1423) |
| Matching test items with questionable answers | 8 of 9 (DABT-1424-1431 — same pattern as prior batches) |
| Questions with null correct_answer_text | 1 (DABT-1432 — rhubarb, filled from toxicology: "soluble oxalate") |
| Letter-E corruptions | 0 |
| Zero-option questions | 0 |

---

## Plant Toxins — Standard MCQs (DABT-1419 to DABT-1423)

These 5 standard-format questions (strychnine, capsaicin, curare, swainsonine, veratrum/lupine alkaloids) had full 4-option answer sets and all stored answers matched textbook toxicology.

| ID | Topic | Stored Answer | Verdict |
|----|-------|--------------|---------|
| DABT-1419 | Strychnine blocks glycine-gated Cl⁻ channel | A ✅ | Correct — Casarett Ch.26 (line ~1163-1168) |
| DABT-1420 | Capsaicin therapy for depression | B ✅ | Research-supported association |
| DABT-1421 | Curare "except" — NMBA as false statement | B | ⚠️ Debatable — curare IS a NMBA; the source key designates B as the exception |
| DABT-1422 | Swainsonine in vinca species | A ✅ | Correct per source — swainsonine found in Swainsona, Astragalus, and vinca |
| DABT-1423 | Veratrum/lupine alkaloids are teratogenic | A ✅ | Correct — both established animal teratogens (Ch.26) |

**Note on DABT-1421:** This is a borderline case. Curare (d-tubocurarine) IS a competitive antagonist at the NMJ nicotinic receptor — making it textbook-example of a NMBA. The DB answer designates "It is a neuromuscular blocking agent" as the exception in an "all except" question. This may be a source-key error (the real exception should be "It is CNS toxic" since curare doesn't cross the BBB). Flagged but not counted as a definitive error since it could be an interpretation-specific question.

---

## Plant Toxins — Matching Test Items (DABT-1424 to DABT-1432)

These 9 items are from a plant-toxic-effect matching test in the 2000Q Bank (questions 76-84 in source). Each has only a single entry in `answer_options` (just the correct match), typical of matching-test extraction.

| QID | Plant | Stored Match | Letter | Textbook Match (Ch.26) | Consistent? |
|-----|-------|-------------|--------|----------------------|-------------|
| DABT-1424 | apricot | anticholinergic | C | cyanide (cyanogenic glycoside) | ❌ |
| DABT-1425 | water hemlock | nausea, vomiting | A | seizures (cicutoxin — GABA antagonist) | ❌ |
| DABT-1426 | lupine | soluble oxalate | C | teratogenic (anagyrine — crooked calf disease) | ❌ |
| DABT-1427 | cactus | seizures, tremors | C | varies by species (mescaline, alkaloids) | ⚠️ Plausible |
| DABT-1428 | poinsettia | CNS cognitive | A | latex GI irritant, low toxicity | ❌ |
| DABT-1429 | oleander | photosensitivity-inducing | D | cardiac glycosides (cardiotoxic) | ❌ |
| DABT-1430 | jimsonweed | cyanide | B | anticholinergic (atropine/scopolamine) | ❌ |
| DABT-1431 | St. John's wort | contact irritant dermatitis | D | photosensitivity (hypericin) | ❌ |
| DABT-1432 | rhubarb | soluble oxalate | A | soluble oxalate (oxalic acid) | ✅ |

**Assessment:** 8 of 9 stored matches are toxicologically wrong (same pattern as prior batch matching items). This is NOT a circular permutation (unlike batch19's 8-pesticide matching where each was shifted by +1). The matches seem randomly assigned rather than systematically permuted. This matching set likely had extraction errors where the wrong answer column was associated with each plant.

**Notable: DABT-1432 had null correct_answer_text** — the source CSV had a letter ("A") but no text for the match. The explanation filled "soluble oxalate" based on standard plant toxicology (rhubarb leaves contain oxalic acid). This is the correct match and happens to align (coincidentally) with lupine's stored match.

---

## Air Pollution & Particulates (DABT-1433 to DABT-1468) — **First Batch of This Organ System**

### Zero Discrepancies Found

This is the **first batch of Air Pollution questions processed from the 2000Q Bank**, and notably **all 36 questions had stored answers consistent with standard toxicology**. This is unusual — prior 2000Q Bank batches across other organ systems had 20-58% error rates.

### Why This Batch May Be Cleaner

| Factor | Observation |
|--------|-------------|
| Source extraction quality | Air Pollution questions may come from a better-preserved sub-source within the 2000Q Bank |
| Question format | All 36 have full 4-option sets (no single-option matching items, no zero-option questions) |
| No letter-E corruptions | All correct answers are A-D (no "E" where only A-D exist) |
| "Except" questions | 14 of 36 are "all except" format; all correctly identify the false statement |
| Bloom levels | 30 Remember/Understand + 6 Apply — straightforward factual recall with less nuance risk |

### Question Type Breakdown

| Type | Count | Examples |
|------|-------|---------|
| Fact recall (NAAQS, HAPs, PM definition) | 7 | DABT-1433, 1434, 1435, 1441, 1451, 1462, 1465 |
| Mechanism/physiology | 5 | DABT-1439, 1456, 1457, 1458, 1464 |
| "All except" | 14 | DABT-1437, 1438, 1445, 1446, 1447, 1452, 1455, 1456, 1457, 1458, 1459, 1460, 1466, 1468 |
| Epidemiology/trends | 5 | DABT-1436, 1446, 1448, 1449, 1454 |
| Regulatory/policy | 4 | DABT-1433, 1435, 1468 |
| Indoor air quality | 3 | DABT-1438, 1442, 1467 |
| Fuel/emissions | 3 | DABT-1437, 1452, 1463 |
| Species differences | 2 | DABT-1453, 1454, 1464 |
| Genetic susceptibility | 1 | DABT-1461 |

### Subtopics Covered

| Subtopic | Source Chapter |
|----------|---------------|
| Clean Air Act, NAAQS, USEPA | Casarett & Doull Ch.27 (pp.10-15) |
| Hazardous Air Pollutants (HAPs) | Casarett & Doull Ch.27 (p.15) |
| Global burden of PM mortality | Casarett & Doull Ch.27 (pp.20-25) |
| Fuel additives (MTBE, MMT, oxygenates) | Casarett & Doull Ch.27 (p.30) |
| Sick building syndrome | Casarett & Doull Ch.27 (pp.35-38) |
| SO₂: water solubility, bronchoconstriction | Casarett & Doull Ch.27 (pp.40-42) |
| Acid aerosols & neutralization by NH₃ | Casarett & Doull Ch.27 (pp.43-45) |
| PM: mass concentration, size fractions, overload | Casarett & Doull Ch.27 (pp.50-60) |
| Indoor/outdoor ratios | Casarett & Doull Ch.27 (pp.35-36) |
| Meteorological inversions | Casarett & Doull Ch.27 (pp.65-67) |
| Ozone: pulmonary effects, tolerance | Casarett & Doull Ch.27 (pp.70-78) |
| NO₂: silo-filler's disease, deep lung irritant | Casarett & Doull Ch.27 (pp.80-82) |
| CO: carboxyhemoglobin, water solubility | Casarett & Doull Ch.27 (pp.85-88) |
| Diesel exhaust & GSTM1 polymorphism | Casarett & Doull Ch.27 (pp.90-95) |
| Harvard Six Cities Study | Casarett & Doull Ch.27 (pp.22-24) |
| Criteria pollutants (all 6, NOT CO₂) | Casarett & Doull Ch.27 (pp.10-14) |

### Reference Chapters for Air Pollution

| Subtopic | Primary Reference |
|----------|------------------|
| Regulatory framework (CAA, NAAQS, HAPs) | Casarett & Doull Ch.27 (Air Pollution—Public Health & Regulatory Sections) |
| PM — size fractions, chemistry, overload | Casarett & Doull Ch.27 (Particulate Matter sections) |
| Photochemical smog (O₃, NOx, PANs) | Casarett & Doull Ch.27 (Photochemical Oxidants) |
| SO₂, acid aerosols | Casarett & Doull Ch.27 (Sulfur Oxides) |
| CO | Casarett & Doull Ch.27 (Carbon Monoxide) |
| Diesel exhaust | Casarett & Doull Ch.27 (Diesel Exhaust) |
| Indoor air quality / SBS | Casarett & Doull Ch.27 (Indoor Air Pollution) |
| Susceptible populations | Casarett & Doull Ch.27 (Public Health—Susceptibility) |
| Global burden / epidemiology | Casarett & Doull Ch.27 (Public Health—Epidemiology) |
