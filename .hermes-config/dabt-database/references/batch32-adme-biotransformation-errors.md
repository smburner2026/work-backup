# Batch32: Domain I (ADME/Toxicokinetics) + Domain II (Biotransformation) DB Answer Errors

**Batch:** batch32 (DABT-1769 to DABT-1818)
**Source:** 2000Q Bank (source_file_id=2) — comprehensive question bank
**Domain I:** 24 questions (DABT-1769 through DABT-1792) — Absorption, Distribution, Excretion, Plasma Binding
**Domain II:** 26 questions (DABT-1793 through DABT-1818) — CYP450, Phase 1/2 Reactions, Enzyme Induction/Inhibition
**Error rate:** ~15/50 (30%) answers diverge from standard toxicology per Casarett & Doull Ch.5–7

**Primary reference chapters:**
- Casarett & Doull Ch.5 — Absorption, Distribution, and Excretion of Toxicants
- Casarett & Doull Ch.6 — Biotransformation of Xenobiotics
- Casarett & Doull Ch.7 — Toxicokinetics

---

## Systematic Error Patterns

### Pattern A: Fundamental Physiological Reversals (High Confidence)

These DB answers state the **opposite** of established physiology:

| DB ID | DB Answer | Correct Answer | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1771 | A: warfarin | **C: diethylstilbestrol** | Transplacental carcinogen | C&D Ch.5: "The most well-known transplacental carcinogen in humans is diethylstilbestrol." Warfarin is a teratogen, not a transplacental carcinogen. |
| DABT-1773 | D: well-stirred effect | **B: enterohepatic cycling** | Hydrolysis + reabsorption | C&D Ch.5 defines enterohepatic cycling as biliary excretion → hydrolysis by gut bacteria → reabsorption. The well-stirred effect is a hepatic clearance model (Ch.7). |
| DABT-1774 | B: albumin | **A: arsenic** | Bile-to-plasma ratio | C&D Ch.5 classifies: Class B (ratio >1, 10-1000) = arsenic, lead, manganese. Class C (ratio <1) = albumin, zinc, iron, gold. Albumin has the LOWEST ratio of the four. |
| DABT-1776 | C: kidney | **D: skin** | % cardiac output | Kidney receives ~25% of CO — one of the highest. Skin receives ~5-10% at rest — the smallest fraction among the listed organs (C&D Ch.5). |
| DABT-1777 | B: exhalation | **C: diffusion into fecal fat** | TCDD excretion | TCDD is highly lipophilic (log P 7.05), accumulates in fat, and is primarily eliminated via biliary-fecal route, not exhalation (C&D Ch.5). |
| DABT-1779 | B: ceruloplasmin & RBP | **C: albumin & α₁-acid glycoprotein** | Plasma protein binding | Albumin and α₁-acid glycoprotein are the two major xenobiotic-binding proteins. Ceruloplasmin (copper) and RBP (vitamin A) are specific carriers (C&D Ch.5). |
| DABT-1810 | C: causes liver tumors in primates, not rodents | **B: causes liver tumors in rodents, not humans** | Phenobarbital carcinogenesis | Phenobarbital is a rodent-specific hepatocarcinogen via CAR activation; primate/human studies show no increased liver tumor risk (C&D Ch.6, Ch.8). |

### Pattern B: Transporter & Protein Misclassification

DB answers that misidentify which molecule is a transporter or what it does:

| DB ID | DB Answer | Correct Answer | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1775 | B: Mrp2 (as exception) | **D: ras (as exception)** | Biliary transporters | C&D Ch.5 lists MRP2, BCRP, MDR1 (P-gp), MATE1, BSEP as canalicular transporters. Mrp2 IS a biliary transporter. ras is a GTPase signaling protein — the true exception. |
| DABT-1784 | C: P-gp is an example (as exception) | **D: found only in liver and kidney** | ABC transporter location | P-gp (MDR1) is definitively an ABC transporter. ABC transporters are expressed broadly (intestine, BBB, placenta, testis, liver, kidney) — statement D is the genuine false statement. |
| DABT-1811 | A: carboxylesterase (as exception) | **B: alcohol dehydrogenase (as exception)** | Hydrolytic enzymes | Carboxylesterases ARE hydrolases. Alcohol dehydrogenase is an OXIDOREDUCTASE (not hydrolytic), converting ethanol to acetaldehyde via NAD⁺ (C&D Ch.6). |

### Pattern C: Wrong Mechanism / Association

DB answers that assign the wrong mechanism or metabolic pathway:

| DB ID | DB Answer | Correct Answer | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1799 | A: hydrolysis (as exception) | **B: conjugation (as exception)** | Phase 1 vs Phase 2 | Hydrolysis IS Phase 1. Conjugation is Phase 2 (C&D Ch.6). The DB has the classification reversed. |
| DABT-1803 | A: enzyme inducers | **C: victim drug and perpetrator** | Terfenadine/ketoconazole | Terfenadine is the victim (CYP3A4 substrate), ketoconazole is the perpetrator (CYP3A4 inhibitor). This is a classic DDI, not enzyme induction (C&D Ch.6). |
| DABT-1804 | C: rifampin | **D: fasting** | UDPGA/PAPS depletion | Fasting depletes hepatic UDPGA (UDP-glucose shortage) and PAPS (ATP shortage). Rifampin is an inducer that increases conjugation, not a depletor (C&D Ch.6). |
| DABT-1814 | B: chloramphenicol | **D: sulindac** | Sulfoxide reduction | Sulindac is the classic example: its sulfoxide prodrug is reduced to the active sulfide by gut microflora. Chloramphenicol undergoes nitroreduction, not sulfoxide reduction (C&D Ch.6). |
| DABT-1813 | C: white blood cells | **D: intestinal microflora** | Nitroreductase location | Gut bacteria are the most important site of nitroreduction in vivo (C&D Ch.6). |

### Pattern D: Incomplete Answers (Partial Truth Presented as Complete)

DB answers that are technically true but incomplete:

| DB ID | DB Answer | Correct Answer | Topic | Rationale |
|-------|-----------|---------------|-------|-----------|
| DABT-1818 | C: peroxisomes | **D: all of the above** | Ethanol oxidation | Ethanol is oxidized by ADH (cytosol), CYP2E1 (microsomes), AND catalase (peroxisomes). The DB picks only one pathway (C&D Ch.6, Ch.24). |

### Pattern E: Letter-E Corruptions (Answer E with Only A-D Options)

Questions where `correct_answer_letter = 'E'` but stored options only go up to D. The intended answer must be inferred from toxicology:

| DB ID | Likely True Answer | Question Topic |
|-------|-------------------|----------------|
| DABT-1769 | D (all of the above) | Species differences in GI absorption — all three factors contribute |
| DABT-1772 | C (both) | Microflora hydrolyze both glucuronide and sulfate conjugates |
| DABT-1781 | C (significant endocytosis) | BBB: endocytosis is restricted, NOT a component |
| DABT-1782 | A (false statement) | Free (not total) concentration determines efficacy |
| DABT-1785 | A (charged molecules) | Charged molecules require active transport |
| DABT-1791 | A (high fever) | Fever is not a particle clearance mechanism |
| DABT-1793 | A (mephenytoin) | S-mephenytoin is the CYP2C19 probe drug |
| DABT-1794 | C (induced by quinidine) | Quinidine INHIBITS CYP2D6, does not induce it |
| DABT-1800 | D (parathyroid hormone) | UGTs do not conjugate peptide hormones |
| DABT-1805 | D (quinidine and quinine) | Quinidine is a potent CYP2D6 inhibitor; quinine is not (C&D Ch.6) |
| DABT-1809 | D (always enzymatic) | GSH conjugation can occur non-enzymatically |
| DABT-1812 | A (adds oxygen, forms 3-member ring) | That describes P450 epoxidation, not epoxide hydrolase |

---

## Key Lessons for Future ADME/Toxicokinetics Batches

1. **Bile-to-plasma classification is a known weak area for the 2000Q Bank.** Class B (arsenic, lead, Mn → ratio >1) vs Class C (albumin, gold, iron → ratio <1) — the DB consistently gets this backwards.

2. **Transporters: all ABC transporters (P-gp, MRP2, BCRP) on the canalicular membrane are biliary exporters.** The DB sometimes treats Mrp2 or P-gp as if they are not biliary transporters — they are.

3. **Plasma protein binding: albumin + α₁-acid glycoprotein are the major xenobiotic binders.** The DB substitutes specialized transport proteins (ceruloplasmin, RBP) as if they were general xenobiotic binders.

4. **Cardiac output distribution: kidney is high-perfusion (~25%).** Skin is the lowest-perfusion organ at rest of those listed.

5. **Phase 1 (oxidation/reduction/hydrolysis) vs Phase 2 (conjugation):** Hydrolysis is Phase 1 — the DB sometimes classifies it as Phase 2.

6. **Terfenadine-ketoconazole:** This classic DDI pair is victim + perpetrator, not inducers.

7. **Phenobarbital rodent carcinogenicity:** Rodents (not primates/humans) — the DB reverses the species-specificity.

8. **Ethanol oxidation: all three locations (ADH-cytosol, CYP2E1-microsomes, catalase-peroxisomes).** The DB picks only one.

9. **Sulindac sulfoxide reduction:** Classic example of gut-microflora-catalyzed reduction of a prodrug.
