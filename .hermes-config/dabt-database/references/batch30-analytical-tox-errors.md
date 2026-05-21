# Batch 30: Analytical Toxicology / Occupational Exposure (Domain I)

**Total questions:** 50 (DABT-1669 to DABT-1718)
**Domain:** Domain I (Conduct of Studies)

## Overview

Batch30 covers:
- **Analytic toxicology principles** — precision vs accuracy, chain of custody, specimen selection, extraction methods, postmortem redistribution (DABT-1669–1689)
- **Urine drug testing** — screening vs confirmation, adulteration, false positives, biomarkers (DABT-1690)
- **Analytical techniques matching** — spot test, HPLC, TLC, GC, GC/MS, immunoassay, spectrochemical (DABT-1691–1697)
- **Occupational exposure** — dose determinants, inhalation vs dermal determinants, TLVs, biological monitoring (DABT-1698–1708)
- **Occupational respiratory disease** — pneumoconiosis, RADS, hypersensitivity pneumonitis, asphyxiants, aerosol classification (DABT-1709–1718)

## Error Summary

| Category | Count | Details |
|----------|-------|---------|
| Wrong stored association (matching items) | 5 | DABT-1692–1696 — 5/7 matching items have wrong pairings |
| Correct matching items | 2 | DABT-1691 (spot test), DABT-1697 (spectrochemical) — stored pairs are correct |
| Standard MCQs | 43 | All correct — no discrepancies found |
| **Overall error rate** | **5/50 (10%)** | Moderate — comparable to batch18 (11.5%) |

## Matching Item Corruption: Multi-Position Offset (DABT-1691–1697)

These 7 items from source_file_id=2 (2000Q Bank) are part of a "Match the analytical technique with its description" question. Each technique has exactly one stored option (single-option pattern). Five of the seven stored pairings are toxicologically wrong.

### Technique → Stored Description vs. Correct Description

| ID | Technique | Stored (DB) | Stored Correct? | Correct Should Be |
|----|-----------|-------------|-----------------|-------------------|
| DABT-1691 | spot test | D: nonquantitative, can screen many drugs at one time | **YES** ✓ | — |
| DABT-1692 | HPLC | E: Noncompetitive and competitive types exist | **NO** ✗ | C: typically uses reverse phase conditions |
| DABT-1693 | TLC | A: Detector bombards molecules with electron stream | **NO** ✗ | None of the stored options perfectly describe TLC (planar separation on silica plate) |
| DABT-1694 | GC | F: simplest and fastest test | **NO** ✗ | B: commonly uses flame ionization detector |
| DABT-1695 | GC/MS | C: typically uses reverse phase conditions | **NO** ✗ | A: Detector bombards molecules with electron stream (EI-MS) |
| DABT-1696 | immunoassay | B: commonly uses flame ionization detector | **NO** ✗ | E: Noncompetitive and competitive types exist |
| DABT-1697 | spectrochemical | H: detector adds or removes protons | **YES** ✓ | — |

### Corruption Pattern Analysis

**Unlike batch19 (circular permutation, +1 shift),** this pattern does not form a closed loop. The 5 wrong items have inconsistent offsets:
- HPLC(27)→E stored, should be C (offset -2 in letter number)
- GC(29)→F stored, should be B (offset -4)
- GC/MS(30)→C stored, should be A (offset -2)
- immunoassay(31)→B stored, should be E (offset +3)

The two correct items (spot test at position 26, spectrochemical at position 32) bracket the corrupted segment, suggesting a data-entry error affecting only the middle 5 rows of the matching set rather than a systematic shift during extraction.

**Recommendation:** When writing explanations for these, describe the analytical technique's ACTUAL characteristics and correct matching description. Do not propagate the DB's wrong pairing.

## Standard MCQ Verification

All 43 standard MCQs (DABT-1669–1690 and DABT-1698–1718) have correct DB answers verified against standard toxicological knowledge. No discrepancies were found in:

- Precision vs accuracy (DABT-1671)
- Urine as poor quantitation matrix (DABT-1673)
- Impurity profiling for source identification (DABT-1674)
- Postmortem redistribution — imipramine highest (DABT-1689)
- TLV-TWA, TLV-STEL, TLV-C definitions (DABT-1701–1702, 1708)
- Biological monitoring advantages/limitations (DABT-1704–1705)
- Biomarkers — aniline→para-aminophenol, ethylene glycol→oxalic acid (DABT-1706–1707)
- Simple vs toxic asphyxiants (DABT-1716–1717)
- Aerosol classification — mist vs fume vs dust (DABT-1715)

## Reference

- **Analytical toxicology:** Casarett & Doull Ch. 31 (Analytic/Forensic Toxicology)
- **Occupational exposure:** Casarett & Doull Ch. 28 (Toxic Effects of Exposures to Particles, Fibers, and Gases)
- **Biological monitoring:** Casarett & Doull Ch. 30 (Occupational Toxicology)
