# Batch 28 Findings: Neuropharmacology Matching + Food Safety (Domain II / Domain IV)

**Processed:** 2026-05-20  
**Questions:** DABT-1569 to DABT-1618 (50 questions)  
**Source:** 2000Q Bank (source_file_id=2), questions #80–104 (neuropharm matching & cell death) + #??–?? (food safety)  
**Domains:** Domain II (Mechanistic) — Q1569-1607; Domain IV (Applied/Food Safety) — Q1608-1618

## Overview

| Sub-section | Questions | DB Error Rate | Key Issue |
|-------------|-----------|---------------|-----------|
| Cell Death & Toxicity Mechanisms | DABT-1569–1592 (24 Qs) | ~8% (2/24) | Letter-E bug on DABT-1570; DABT-1580 "act locally" vs "specialized organs" ambiguity |
| Neuropharmacology Matching | DABT-1593–1607 (15 Qs) | **7/7 stored matches wrong (100%)** + 8 with zero option text | Classic circular-permutation + letter-only corruption |
| Food Safety | DABT-1608–1618 (11 Qs) | **0% — all clean** | All have full 4-option sets, correct answers |

## 1. Cell Death & Toxicity Mechanisms (DABT-1569–1592)

**Reference:** Casarett & Doull Ch.1 "General Principles" and Ch.3 "Mechanisms of Toxicity"

### Confirmed Errors

| QID | DB answer | Correct answer | Notes |
|-----|-----------|---------------|-------|
| DABT-1570 | E (no option E exists) | C — programmed cell death | Letter-E import corruption. Options are A=passive, B=accidental, C=programmed, D=immune. Apoptosis = programmed cell death. |

### Ambiguous / Noteworthy

| QID | Issue | Resolution |
|-----|-------|------------|
| DABT-1580 | DB says "act locally" is the exception (B), but cytokines DO act locally via paracrine/autocrine signaling. The statement that's actually NOT true is "produced in specialized organs" (C) — cytokines are produced by many cell types. | Explain both positions. The DB key marks B, but note the ambiguity: cytokines are locally-acting molecules produced by diverse cell types. |
| DABT-1590 | DB correct_answer_text = "blocking the effect of ADH on the collecting duct" for mercury nephrotoxicity. The correct mechanism involves a Hg(Cys)₂ complex mimicking endogenous cystine → uptake via rBAT/b⁰,⁺AT in proximal tubule. ADH blocking is lithium's MOA. | Note the discrepancy. The textbook mechanism is the dicysteinyl-mercury cystine mimicry. |

### Correct Questions (no issues found)

All remaining 21 questions (DABT-1569, 1571-1589 except 1580, 1591-1592) have correct DB answers matching standard toxicology for: necrosis features, apoptosis characteristics, cytochrome c in apoptosis, COX-2 inhibitors, JNK-apoptosis pathway, paclitaxel/mitosis, galactosamine/liver, practolol/oculomucocutaneous, mPT pore (hydrophobic bile acids), microcystins/phosphatase, cytokines (DABT-1580 handled above), chaperones, lipid repair/NADPH, peripheral nerve repair, apoptosis in neoplasia, TGF-β/fibrogenesis, fibrosis harms, idiosyncratic reactions, cellular stress response, organ-selective toxicity, soft nucleophiles, and Fenton reaction.

## 2. Neuropharmacology Matching (DABT-1593–1607)

**Reference:** Casarett & Doull Ch.9 "Drug Toxicity" and Ch.10 "Environmental Neurotoxicology"; standard pharmacology texts (Goodman & Gilman)

### Subsection A: DABT-1593–1599 — Single-Option Matching, 7/7 Wrong

These are matching-test items where each question has ONE entry in `answer_options` storing the correct match. **All 7 stored associations are factually wrong.** The pattern is NOT a simple circular permutation (unlike batch19 where each chemical was shifted by one position). Instead, the stored answers appear to be random/arbitrary assignments — possibly a column misalignment during extraction or a completely different answer key was used.

| QID | Term | DB stored match (WRONG) | Correct pharmacological mechanism |
|-----|------|------------------------|----------------------------------|
| DABT-1593 | muscimol | serotonin agonist | **Direct GABA-A receptor agonist** (Amanita muscaria toxin) |
| DABT-1594 | clonidine | inhibits norepinephrine uptake | **α₂-adrenergic receptor agonist** (centrally acting antihypertensive) |
| DABT-1595 | baclofen | direct nicotine antagonist | **GABA-B receptor agonist** (muscle relaxant) |
| DABT-1596 | bicuculline | direct dopamine agonist | **GABA-A receptor antagonist** (experimental convulsant) |
| DABT-1597 | theophylline | direct serotonin antagonist / glycine uptake inhibitor | **Phosphodiesterase inhibitor + adenosine antagonist** (bronchodilator) |
| DABT-1598 | nicotine | direct GABA-A agonist | **Nicotinic acetylcholine receptor agonist** |
| DABT-1599 | clozapine | indirect GABA-A agonist | **Dopamine D₄ > D₂ antagonist, 5-HT₂A antagonist** (atypical antipsychotic) |

**Pattern:** The stored associations consistently map drugs to mechanisms from completely different drug classes. None of the 7 is even close to correct. This is a new and particularly severe form of matching-test corruption — unlike the circular permutation pattern (batch19) or antidotes display-line corruption (batch6), these seem to have no systematic relationship to the correct pairings.

### Subsection B: DABT-1600–1607 — Letter-Only, Zero Option Text

These matching items have `correct_answer_letter` but **zero rows in `answer_options`** (no option text at all). This is a NEW sub-pattern of the "zero-option" problem — previously documented cases (DABT-0962, DABT-1092, DABT-1169, DABT-1170) had neither letter nor text. Here, the letter IS stored (suggesting correct answer key was partially parsed), but the actual option text was lost.

| QID | Term | Stored Letter | Correct mechanism |
|-----|------|--------------|-------------------|
| DABT-1600 | tecadenoson | E | **Selective A₁ adenosine receptor agonist** (PSVT treatment) |
| DABT-1601 | yohimbine | A | **α₂-adrenergic receptor antagonist** |
| DABT-1602 | cocaine | D | **Dopamine/norepinephrine reuptake inhibitor + Na⁺ channel blocker** |
| DABT-1603 | α-bungarotoxin | D | **Irreversible nicotinic acetylcholine receptor antagonist** (krait venom) |
| DABT-1604 | botulinum toxin | D | **SNARE protein cleavage → blocks ACh release** (presynaptic) |
| DABT-1605 | bromocriptine | D | **Dopamine D₂ receptor agonist** |
| DABT-1606 | haloperidol | E | **Dopamine D₂ receptor antagonist** |
| DABT-1607 | reserpine | B | **VMAT2 inhibitor → monoamine depletion** |

**Pattern significance:** Unlike the standard zero-option case (no data at all), the stored letters here may be the actual correct answers from the original test key. However, with no option text available, the correctness of each letter is unverifiable. The known wrong matches in DABT-1593-1599 (also from the same matching test, same source batch) suggest these letters may also be unreliable.

### Subsection C: Known-Correct Matching Pairs (for reference)

Based on standard pharmacology, the correct matching pairs for this test would be:

| Term | Mechanism |
|------|-----------|
| muscimol | Direct GABA-A agonist |
| clonidine | α₂-adrenergic agonist |
| baclofen | GABA-B agonist |
| bicuculline | GABA-A antagonist |
| theophylline | PDE inhibitor / adenosine antagonist |
| nicotine | nAChR agonist |
| clozapine | D₄/5-HT₂A antagonist |
| tecadenoson | A1 adenosine agonist |
| yohimbine | α₂-adrenergic antagonist |
| cocaine | DA/NE reuptake inhibitor + Na channel blocker |
| α-bungarotoxin | nAChR antagonist (irreversible) |
| botulinum toxin | SNARE cleavage (presynaptic ACh blocker) |
| bromocriptine | D₂ agonist |
| haloperidol | D₂ antagonist |
| reserpine | VMAT2 inhibitor |

## 3. Food Safety (DABT-1608–1618)

**Reference:** Casarett & Doull Ch.25 "Food Toxicology" and Ch.26 "Food Additives and Contaminants"

**All 11 questions are clean** — no errors, no parsing issues:

| QID | Topic | Correct Answer | Verified |
|-----|-------|---------------|----------|
| DABT-1608 | Major food safety concern worldwide | C — microbial contamination | ✓ |
| DABT-1609 | US food safety presumption | A — All food without additives or contaminants is safe | ✓ |
| DABT-1610 | Tripalmitin effect | D — increase lymph flow | ✓ (chylomicron → lymph) |
| DABT-1611 | GRAS substances | B — can be certified based on experience before 1958 | ✓ |
| DABT-1612 | Unavoidable contaminants | D — all of the above (tolerance limits, pesticide residues, aflatoxins) | ✓ |
| DABT-1613 | Color food additives GRAS status | D — They are not eligible for GRAS status | ✓ |
| DABT-1614 | Low toxicity of aromatic amine colors | A — Sulfonation to highly polar, poorly absorbable molecules | ✓ |
| DABT-1615 | Caramel food additive classification | A — exempt from certification | ✓ |
| DABT-1616 | BHA classification | C — a preservative | ✓ |
| DABT-1617 | Nonnutritive sweeteners exception | D — gum arabic | ✓ |
| DABT-1618 | Sodium benzoate food use | C — an antimicrobial agent | ✓ |

**Significance:** This is the SECOND clean sub-source from source_file_id=2 (2000Q Bank), after Air Pollution (batch25, 36/36 clean). Food Safety questions appear to have been extracted from a different sub-source within the 2000Q Bank with better quality control. This is consistent: both Air Pollution and Food Safety are Topic IV sub-domains that may have been extracted separately from the main organ-system chapters.

## Overall Batch Summary

**Total questions:** 50  
**Confirmed DB errors:** 1 (DABT-1570) + 7 wrong matching associations (DABT-1593-1599) + 8 zero-option-text items (DABT-1600-1607)  
**Ambiguous/questionable items:** 2 (DABT-1580, DABT-1590)  
**Clean questions:** 32 (64%)  
**Effectively unusable DB answers:** 15/50 (30%) — all from the neuropharmacology matching section

## Recommendations

1. The neuropharmacology matching items (DABT-1593-1607) need complete answer key reconstruction from original test source or a reference pharmacology text.
2. Food Safety questions can be marked as trusted for drilling without cross-verification.
3. The DABT-1570 letter-E bug follows the established letter-E corruption pattern and can be corrected to C.
4. DABT-1580 and DABT-1590 should present both DB and textbook answers with notes.
