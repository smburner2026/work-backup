# Batch 38 — Clinical Toxicology / Overdose Management (Domain IV)

**50 questions:** DABT-2069–2070, DABT-2106–2153
**Source:** 2000Q Bank (source_file_id=2)
**Processed:** 2026-05-20

## Summary

**Apparent error rate: ~0% (0/50).** This is the **fourth clean 2000Q Bank sub-source** identified (after Air Pollution batch25, Food Safety batch28, and Drugs of Abuse batch37). All 50 questions had correct DB-stored answers and full 4-option sets with no letter-E corruptions, no zero-option items, no matching-test scrambling, and no EXCEPT reversals.

## Topics Covered

| Topic | Questions | Primary Reference |
|-------|-----------|-----------------|
| Chloroquine & cocaine antidotal mechanisms | DABT-2069–2070 | Goldfrank's Toxicologic Emergencies |
| Acetaminophen overdose management | DABT-2106–2109 | Goldfrank's |
| Salicylate toxicity | DABT-2110–2112 | Goldfrank's |
| COX inhibitor pharmacology & overdose | DABT-2113–2115 | Goldfrank's |
| Iron overdose | DABT-2116–2119 | Goldfrank's |
| Vitamin A, D, B₆, C toxicity | DABT-2120–2124 | Goldfrank's |
| Diabetes drug overdose | DABT-2125–2127 | Goldfrank's |
| Antibiotic adverse effects | DABT-2128–2131 | Goldfrank's |
| Anticoagulant rodenticide/warfarin overdose | DABT-2132–2135 | Goldfrank's |
| Thyroid hormone overdose | DABT-2136–2139 | Goldfrank's |
| Antihistamine overdose (H₁ & H₂) | DABT-2140–2142 | Goldfrank's |
| Decongestant & triptan overdose | DABT-2143–2147 | Goldfrank's |
| Topiramate & anticonvulsant ADRs | DABT-2148–2149 | Goldfrank's |
| Calcium channel blocker overdose | DABT-2150–2153 | Goldfrank's |

## Output File

`batches/batch38_done.json` — list of `{id, explanation, domain}` dicts.

## Important Limitation

**Goldfrank's Toxicologic Emergencies is NOT in the extracted reference library.** Unlike Casarett & Doull and Hayes chapters which are searchable, Goldfrank's could not be text-queried for cross-verification. The explanations were written based on clinical toxicology knowledge rather than extracted text search. This is a reference-gap issue — clinical toxicology/overdose management questions (which are common in Domain IV) would benefit from having Goldfrank's extracted and indexed.

Alternative reference sources available in the extracted library:
- **Casarett & Doull Ch.33** "Clinical Toxicology" — covers general principles of poisoning management, antidotes
- **Casarett & Doull Ch.30** "Therapy" — therapeutic interventions for poisoning
- These chapters were NOT used for this batch since the primary reference standard for clinical toxicology is Goldfrank's

## Explanation Format

Each explanation follows the pattern established in batch33+:
- "Correct answer: [letter] — [text]. [Mechanism/justification]. [Distractor trap: why wrong options are tempting]. Source: [reference]."
