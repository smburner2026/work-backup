# Batch 14 Ocular & Skin Toxicology DB Answer Discrepancies

Batch: DABT-0919 through DABT-0968 (50 questions)
Source: 2000Q Bank (source_file_id=2)
Domains: All Domain IV — Applied Toxicology
Topics:
- DABT-0919 to DABT-0935: Nervous System / Neurotoxicity (17 Qs)
- DABT-0936 to DABT-0962: Eye / Ocular Toxicity (27 Qs)
- DABT-0963 to DABT-0968: Skin / Dermatotoxicity (6 Qs)
Date processed: 2026-05-20

## Summary

8 DB answer key discrepancies found across the batch, concentrated in the Ocular Toxicity section (6/27 = 22%). The Skin section (6 Qs) had 1 discrepancy. The Neuro section continuation (DABT-0919-0935) had 1 discrepancy (DABT-0925) — see also `batch13-neuro-errors.md` for the earlier 29 errors in DABT-0869-0918.

## Category 1: Ocular Toxicity DB Errors

| QID | Question | DB Answer | Toxicologically Correct | Rationale |
|-----|----------|-----------|------------------------|-----------|
| DABT-0941 | Surfactant corneal damage order | **B** (anionic > neutral > cationic) | **D** (cationic > anionic > neutral) | Casarett & Doull Ch.17 states: cationic surfactants are the most damaging because they bind strongly to negatively charged corneal epithelial cell membranes. The DB order reverses the ranking. |
| DABT-0943 | False statement about the lens | **D** (lens is ~2/3 water, 1/3 protein) | **A** (lens has dual blood supply) | The lens IS ~65% water, 35% protein (true — highest protein tissue in body). The FALSE statement is A: the lens is avascular — it has NO blood supply. Statement D is true. |
| DABT-0947 | Oculotoxic antituberculosis drug | **A** (isoniazid) | **B** (ethambutol) | Ethambutol is the classic oculotoxic TB drug causing dose-dependent retrobulbar optic neuritis. Isoniazid CAN cause optic neuropathy (rare, in slow acetylators) but ethambutol is the well-known answer. |
| DABT-0949 | Chemical to assess corneal damage | **B** (hypertonic saline) | **D** (fluorescein) | Fluorescein is the standard: it stains disrupted corneal epithelium green under cobalt blue light. Hypertonic saline is used to dehydrate/treat corneal edema, not to assess damage. |
| DABT-0953 | Brain area associated with vision | **C** (temporal lobe) | **A** (occipital lobe) | The primary visual cortex (Brodmann area 17) is in the occipital lobe. The temporal lobe participates in higher-order visual processing (ventral stream) but is not the primary visual area. |
| DABT-0956 | Most severe corneal damage | **A** (strong acids) | Strong bases (alkalis) | Strong bases penetrate deeper via saponification of cell membranes, causing extensive destruction, collagen denaturation, and potential perforation. Strong acids cause coagulation necrosis that limits penetration. |

## Category 2: Skin Toxicology DB Error

| QID | Question | DB Answer | Toxicologically Correct | Rationale |
|-----|----------|-----------|------------------------|-----------|
| DABT-0966 | Highest skin penetration agent | **B** (hydrophobic, high MW) | **D** (hydrophobic, low MW) | The 500 Dalton rule: compounds >500 Da have poor skin penetration regardless of lipophilicity. Low molecular weight + moderate lipophilicity (log P ~1-3) optimizes skin penetration. Hydrophobic high MW compounds partition well but diffuse slowly. |

## Category 3: Neurotoxicology Continuation Error (see also batch13-neuro-errors.md)

| QID | Question | DB Answer | Toxicologically Correct | Rationale |
|-----|----------|-----------|------------------------|-----------|
| DABT-0925 | Non-developmental-neurotoxicant | **D** (methylmercury) | **C** (folic acid) | Methylmercury IS a potent developmental neurotoxicant (Minamata disease). Folic acid prevents neural tube defects — it is protective, not toxic. This appears to be a letter-reversal or answer transcription error. |

## Category 4: Format Issues (Missing or Incomplete Data)

| QID | Issue | Resolution |
|-----|-------|-----------|
| DABT-0928 to DABT-0935 | Matching test items — only correct option stored in `answer_options` | These are valid matching pairs (chemical/term → neurologic effect). All 8 matchings are toxicologically correct. See table below. |
| DABT-0962 | Zero options stored in `answer_options` table | Question: "Styrene has been associated with _____." Answer letter: B. Styrene is associated with color vision deficits (dyschromatopsia). |

### Verified Matching Pairs (DABT-0928 to DABT-0935)

| QID | Term | Match | Toxicologically Verified? |
|-----|------|-------|--------------------------|
| DABT-0928 | amantadine | withdrawal seizures | ✅ Yes — NMDA antagonist withdrawal causes rebound hyperexcitability |
| DABT-0929 | clarithromycin | myoclonus, hyperreflexia | ✅ Yes — macrolide CNS effects, esp. in elderly/renal impairment |
| DABT-0930 | beta-adrenergic blockers | concentration-related seizure disorder | ✅ Yes — lipophilic beta-blockers cross BBB, seizures at high [ ] |
| DABT-0931 | carbon monoxide | depression | ✅ Yes — delayed neuropsychiatric sequelae of CO poisoning |
| DABT-0932 | meperidine metabolite | muscle toxicity | ✅ Yes — normeperidine causes myoclonus, seizures, muscle toxicity |
| DABT-0933 | lovastatin | mania | ✅ Yes — statins associated with neuropsychiatric effects including mania |
| DABT-0934 | barbiturates | psychosis | ✅ Yes — withdrawal/chronic intoxication causes psychosis |
| DABT-0935 | salicylates | VIII cranial nerve toxicity | ✅ Yes — tinnitus, hearing loss, vertigo from salicylate ototoxicity |

## Reference Chapters Used for Verification

| Topic | Primary Reference | Secondary Reference |
|-------|-------------------|-------------------|
| Neurotoxicology (0919-0935) | Casarett & Doull Ch.16 (Nervous System) | — |
| Ocular Toxicology (0936-0962) | Casarett & Doull Ch.17 (Cornea, Retina, Visual System) | — |
| Skin Toxicology (0963-0968) | Casarett & Doull Ch.19 (Skin) | — |

## Lessons for Future Batches

1. **Ocular toxicity DB answers have a ~22% error rate** — always cross-check Casarett & Doull Ch.17 before accepting answers for eye questions. The matching tests (surfactant order, corneal assessment chemicals, visual cortex anatomy) are particularly unreliable.

2. **The 500 Dalton rule and skin penetration** — questions about percutaneous absorption need verification against Ch.19's physico-chemical property discussions. The DB has the wrong MW/lipophilicity combination.

3. **Single-option matching items are widespread** — DABT-0928-0935 join the pattern seen in batch 13 and earlier batches where the DB stores only the correct match. Unlike earlier batches where these were scrambled, these 8 matching pairs are all toxicologically correct.

4. **Questions with zero stored options** — DABT-0962 has no options in answer_options at all. When encountering such questions, reconstruct the answer from the `correct_answer_letter` field and standard toxicology knowledge rather than relying on missing DB data.
