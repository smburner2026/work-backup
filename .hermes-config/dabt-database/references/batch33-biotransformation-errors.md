# Batch 33 — Biotransformation (Domain II) Errors

**Batch:** 50 questions (DABT-1819 through DABT-1868)
**Domain:** All Domain II (Mechanistic Toxicology — Biotransformation emphasis)
**Source:** 2000Q Bank (source_file_id=2)
**Processed:** 2026-05-20

## Summary

This batch focuses on **biotransformation enzymology** — CYP450, FMOs, GSTs, SULTs, UGTs, NATs, methyltransferases, epoxide hydrolase, aldehyde oxidase, rhodanese, and MPO. Unlike batch27 (cell death/signaling mechanisms, 12% error) or batch32 (mixed ADME+biotransformation, 30% error), this **purely biotransformation batch has an ~82% error rate (41/50)** — the highest for any Domain II batch and the second-highest of any 2000Q Bank section processed (after batch31 ADME at 69%).

**Key finding:** The DABT-1800+ range from the 2000Q Bank appears to come from a late-extraction run with fundamentally degraded data quality. The extraction likely captured incorrect `correct_answer_letter` values to match erroneous display-line positions rather than actual answer keys.

## Verified DB Errors

### Pattern A: Fundamental Enzyme Location Reversals (4 questions)

These DB answers state the **wrong cellular compartment** for well-established enzyme locations:

| DB ID | DB Answer | Correct Answer | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1820 | B: cytosol | **A: mitochondria** | ALDH2 location | ALDH2 is the low-Km mitochondrial isoform. ALDH1 is cytosolic. The question specifies ALDH2. |
| DABT-1827 | B: cytosol | **A: endoplasmic reticulum** | CYP450 location | CYP450s are membrane-bound in the ER (microsomes). The DB says cytosol — a fundamental reversal. |
| DABT-1834 | B: microsomes | **D: all of the above** | GST location | GSTs are found in cytosol (Alpha, Mu, Pi), microsomes (MGST1-3), AND mitochondria (GSTK1). |
| DABT-1846 | B: cytosol | **B: cytosol (correct)** | NAT location | NAT1/2 are cytosolic. This ONE is correct in the DB. |

### Pattern B: Wrong Enzyme Cofactor / Metal (2 questions)

| DB ID | DB Answer | Correct Answer | Rationale |
|-------|-----------|---------------|-----------|
| DABT-1821 | D: copper | **B: molybdenum** | Aldehyde oxidase and xanthine oxidoreductase are molybdenum-containing hydroxylases (molybdopterin cofactor + FAD + [2Fe-2S]). Neither contains copper. |
| DABT-1855 | A: 5 | **C: 22** | The human UGT superfamily has ~22 functional enzymes (9 UGT1A, 2 UGT2A, 11 UGT2B). "5" was the earliest estimate from the 1990s. |

### Pattern C: Wrong "EXCEPT" Designation — TRUE Statement Marked as Exception (14 questions)

The DB marks a TRUE statement as the exception/false statement in "all except" questions. These are the most dangerous errors because they teach the wrong fact:

| DB ID | DB says exception is | Actual false statement | Topic |
|-------|---------------------|----------------------|-------|
| DABT-1824 | A: present in neutrophils (TRUE) | **B:** "induced by cyanide" — FALSE (cyanide inhibits MPO) | MPO |
| DABT-1825 | C: inhibited by drugs (TRUE) | **D:** PHS toxicity in CYP-rich tissues — FALSE (PHS toxicity in PHS-rich tissues) | PHS/COX |
| DABT-1828 | D: directly binds substrate+O₂ (TRUE) | **C:** "binds CO₂" — FALSE (binds CO, not CO₂) | CYP450 |
| DABT-1829 | C: carbamazepine (TRUE — it IS epoxidated by CYP3A4) | **D:** chloroform — undergoes oxidative dechlorination, not epoxidation | CYP450 epoxidation |
| DABT-1831 | D: APAP→NAPQI (TRUE — classic toxification) | **B:** ethanol→acetic acid — this is DETOXIFICATION | Toxic metabolite pairs |
| DABT-1838 | A: amino acids form amide linkage (TRUE) | **D:** "Acetyl CoA can be involved" — FALSE (CoA-SH, not Acetyl-CoA, for amino acid conjugation) | Amino acid conjugation |
| DABT-1839 | B: high concentration in hepatocytes (TRUE) | **A:** "stereoselective conjugation occurs non-enzymatically" — FALSE (stereoselectivity implies enzymatic catalysis) | GST |
| DABT-1843 | B: nicotine (TRUE — N-methylated by NNMT) | **A:** acetone — NOT methylated (metabolized by CYP2E1) | Methylation substrates |
| DABT-1845 | C: major route for hydrazines (TRUE — INH, hydralazine) | **A:** "increases water solubility" — FALSE (acetylation often DECREASES solubility, e.g., sulfonamides) | Acetylation |
| DABT-1850 | A: can decrease lipid solubility (TRUE — adds polar sulfate) | **B:** "always detoxify" — FALSE (e.g., N-hydroxy-AAF sulfonation bioactivates) | Sulfonation |
| DABT-1851 | C: Hg/As can be dimethylated (TRUE) | **D:** "high MT activity lowers homocysteine" — FALSE (SAM consumption increases homocysteine flux) | Methylation |
| DABT-1853 | C: substrates for β-glucuronidase (TRUE) | **B:** "formed from activated xenobiotics" — FALSE (UDPGA is the activated cofactor, not the xenobiotic) | Glucuronidation |
| DABT-1860 | A: UGTs are inducible (TRUE) | **B:** "use UDP-glucose" — FALSE (use UDP-GLUCURONIC ACID / UDPGA) | UGT |

### Pattern D: Wrong Mechanism / Association Reversal (10 questions)

| DB ID | DB Answer | Correct Answer | Rationale |
|-------|-----------|---------------|-----------|
| DABT-1819 | E (no E option) | **C: trichloromethyl radical** | Reductive dehalogenation of CCl₄ yields •CCl₃, not phosgene (which is from CHCl₃) |
| DABT-1823 | A: COMT | **D: MAO-B** | MAO-B is elevated in PD substantia nigra; COMT is not specifically elevated there |
| DABT-1826 | D: xanthine oxidase | **B: cytochrome P450** | FMO and CYP450 are both microsomal NADPH-dependent monooxygenases |
| DABT-1830 | E (no E option) | **A: toluene** | Toluene lacks a heteroatom (C₆H₅CH₃) — undergoes side-chain hydroxylation, not heteroatom oxygenation |
| DABT-1832 | C: cleavage of peptide bond | **D: dehydrogenation** | CYP450 catalyzes dehydrogenation/desaturation; peptide cleavage is proteolysis |
| DABT-1833 | B: dibromoethane (exception) | **C: aflatoxin B1 8,9-epoxide** | GSH conjugation of the pre-formed epoxide is DETOXIFICATION; dibromoethane IS activated to episulfonium ion |
| DABT-1836 | D: nitrous oxide | **B: hydrogen sulfide** | Rhodanese detoxifies cyanide (not listed) and participates in H₂S metabolism |
| DABT-1840 | C: trinitroglycerine | **D: all of the above** | All three compounds undergo GSH displacement (CDNB is THE classic GST substrate) |
| DABT-1841 | A: hexane | **C: β-propiolactone** | GSH addition (Michael addition) to β-propiolactone ring; hexane is not a GSH substrate |
| DABT-1842 | C: glutaric acids | **A: mercapturic acid** | GSH conjugates → cysteine conjugates → N-acetylated → MERCAPTURIC ACIDS in urine |
| DABT-1844 | D: histamine→N-methylhistamine | **C: cocaine→ethylcocaine** | Transesterification = cocaine + ethanol → cocaethylene; histamine methylation is N-methylation |
| DABT-1848 | A: low-affinity, low-capacity | **D: high-affinity, low-capacity** | Sulfonation has HIGH affinity (low Kₘ) but LOW capacity (limited PAPS) |
| DABT-1856 | D: genetic sensitivity to parent molecule | **A: acyl glucuronide→neoantigen** | NSAID immune hepatitis via reactive acyl glucuronide haptenation |
| DABT-1859 | A: oxazepam glucuronide | **C: morphine-6-glucuronide** | M6G is MORE potent than morphine; oxazepam glucuronide is inactive |
| DABT-1861 | A: more affected by polymorphisms | **B: can bind 2 substrates at once** | CYP3A4 shows cooperativity (large active site, multi-substrate binding); it's HIGHLY conserved (low polymorphism) |
| DABT-1862 | B: erythromycin | **C: chlorzoxazone** | Chlorzoxazone 6-OH is the classic CYP2E1 probe; erythromycin is a CYP3A4 probe |
| DABT-1867 | A: rifampin | **D: quinidine** | Quinidine is the classic potent CYP2D6 inhibitor; rifampin is a CYP3A4 INDUCER |
| DABT-1868 | E (no E option) | **B: S-oxygenation** | FMO catalyzes oxygenation of nucleophilic heteroatoms (N, S, P) |

### Pattern E: E-Answer Corruptions (6 questions)

| DB ID | DB Answer | Correct Answer | Topic |
|-------|-----------|---------------|-------|
| DABT-1819 | E (no E option) | C (trichloromethyl radical) | CCl₄ reductive dehalogenation |
| DABT-1830 | E (no E option) | A (toluene) | Heteroatom oxygenation exception |
| DABT-1852 | E (no E option) | A (SAM) | SAM is methyl DONOR, not a methyltransferase enzyme |
| DABT-1857 | E (no E option) | D (Golgi apparatus) | SULT non-cytosolic location |
| DABT-1858 | E (no E option) | C (cytosol) | Most conjugation reactions occur in cytosol |
| DABT-1868 | E (no E option) | B (S-oxygenation) | FMO-catalyzed reaction type |

## New Pattern Discovery: DABT-1800+ Data Quality Cliff

This batch (DABT-1819–1868) shows a **dramatic quality drop** compared to earlier Domain II batches from the same source:

| Batch | ID Range | Domain | Error Rate |
|-------|----------|--------|------------|
| batch27 | DABT-1519–1568 | Domain II (cell death, signaling) | 12% |
| batch28 (cell death) | DABT-1569–1593 | Domain II (cell death, UPR) | 8% |
| batch32 (biotransformation) | DABT-1793–1818 | Domain II (biotransformation) | 25% |
| **batch33** | **DABT-1819–1868** | **Domain II (biotransformation)** | **82%** |

The error rate jumps from ~8–25% in the DABT-1500–1818 range to **82% in the DABT-1819+ range**. This suggests a different extraction process or answer-key source for higher-ID questions. Any future batch with IDs starting above DABT-1819 should be treated with **extreme suspicion** — verify every answer against Casarett & Doull Ch.6 before writing explanations.

## Reference Chapter

- **Casarett & Doull Ch.6 "Biotransformation of Xenobiotics"** — the single authoritative reference for ALL questions in this batch. Covers CYP450 catalytic cycle (DABT-1827-1832), FMO chemistry (DABT-1826, 1868), GSTs (DABT-1833-1835, 1839-1842), SULTs (DABT-1848-1850, 1854, 1857), UGTs (DABT-1853, 1855, 1860), NATs (DABT-1845-1847), methyltransferases (DABT-1843-1844, 1851-1852), epoxide hydrolase, aldehyde oxidase (DABT-1821), rhodanese (DABT-1836-1837), MPO (DABT-1824), PHS (DABT-1825), amino acid conjugation (DABT-1838), and hydrolysis (DABT-1832).

## Prevention Checklist for Future Biotransformation Batches

1. **Treat DABT-1800+ questions as unreliable.** Verify EVERY answer against C&D Ch.6 before writing. Do NOT assume the DB-stored answer letter is correct — the extraction process for this range is fundamentally broken.
2. **"EXCEPT" questions are especially dangerous.** 14/50 questions (28%) mark a TRUE statement as the exception. Always independently verify each option's truth value.
3. **Enzyme location questions (cytosol vs mitochondria vs ER) are systematically wrong.** Particularly: ALDH2 (mitochondrial), CYP450 (ER/microsomes), GSTs (all three compartments), NATs (cytosol — actually correct).
4. **Mercapturic acid pathway:** The DB says "glutaric acids" as the GSH-conjugate urine product. Always write "mercapturic acids" (N-acetylcysteine conjugates).
5. **CYP probe drugs:** Verify against standard probe lists: chlorzoxazone = 2E1, midazolam/erythromycin = 3A4, dextromethorphan = 2D6, S-mephenytoin = 2C19, caffeine = 1A2.
6. **Morphine-6-glucuronide > morphine:** Classic example of a conjugation product more potent than parent. The DB says oxazepam glucuronide (inactive) — this is wrong.
7. **CYP3A4 cooperativity:** CYP3A4 can bind 2 substrates simultaneously (homotropic/heterotropic cooperativity). The DB denies this. Know this as a unique CYP feature.
8. **Quinidine as CYP2D6 inhibitor:** The most potent and specific CYP2D6 inhibitor. Rifampin is an inducer on a different CYP.
