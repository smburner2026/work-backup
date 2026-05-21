# Batch34 CYP450 Biotransformation Matching Test Errors

## Overview

Batch34 (DABT-1869-1918) is the first CYP450/biotransformation batch processed from the 2000Q Bank (source_file_id=2). It spans three domains — Domain II (biotransformation, 24 Qs), Domain I (toxicokinetics, 18 Qs), and Domain IV (cardiac electrophysiology, 8 Qs). This file documents errors found in the CYP450 matching subsections (DABT-1879-1891) and other factual errors in the batch.

## Error Type A: CYP450 Matching Test — Systematic Scrambling (DABT-1879-1891)

These are single-term questions (`question_text` = just the chemical name, no answer options in DB) that form a matching test. The answer pool (from DABT-1892) has 8 categories: A=substrate for CYP2A6, B=inducer of CYP2E1, C=inducer of CYP2D6, D=inhibitor of CYP3A4, E=inducer of CYP1A2, F=substrate for CYP1A2, G=inhibitor of CYP2C8, H=substrate for CYP2E1. The DB-stored answer letters are almost entirely wrong vs. textbook CYP450 pharmacology.

| Item | Chemical | DB Answer | DB Category | Textbook-Correct Category |
|------|----------|-----------|-------------|--------------------------|
| DABT-1879 | omeprazole | E | inducer of CYP1A2 | Substrate for CYP2C19/3A4 (also weak CYP1A2 inducer via AhR) |
| DABT-1880 | aniline | E | inducer of CYP1A2 | Substrate for CYP2E1 (aniline hydroxylation is a CYP2E1 marker) |
| DABT-1881 | debrisoquin | D | inhibitor of CYP3A4 | Probe substrate for CYP2D6 (4-hydroxylation) |
| DABT-1882 | alprazolam | C | inducer of CYP2D6 | Substrate for CYP3A4 |
| DABT-1883 | diclofenac | D | inhibitor of CYP3A4 | Substrate for CYP2C9 (4'-hydroxylation) |
| DABT-1884 | bupropion | D | inhibitor of CYP3A4 | Probe substrate for CYP2B6 (hydroxylation) |
| DABT-1885 | fluvoxamine | B | inducer of CYP2E1 | Potent INHIBITOR of CYP1A2 (also inhibits CYP2C19/3A4) |
| DABT-1886 | paroxetine | A | substrate for CYP2A6 | Potent INHIBITOR AND substrate of CYP2D6 |
| DABT-1887 | beta-naphthoflavone | B | inducer of CYP2E1 | Inducer of CYP1A1/1A2 via AhR activation |
| DABT-1888 | isoniazid | E | inducer of CYP1A2 | Inducer of CYP2E1 (via hydrazine metabolite), substrate of NAT2 |
| DABT-1889 | no known agent | D | inhibitor of CYP3A4 | Should be no-match or null — but CYP3A4 has known inhibitors |
| DABT-1890 | carbemazepine | B | inducer of CYP2E1 | INducer of CYP3A4 (also CYP2B6/2C9), autoinducer |
| DABT-1891 | mibefradil | B | inducer of CYP2E1 | Potent mechanism-based INHIBITOR of CYP3A4 (withdrawn for this) |

**Pattern:** The DB stored answers do NOT align with any single systematic shift (not a one-position rotation). The errors appear random or from a completely different matching pool key.

## Error Type B: Factual Identity Errors in Single-Answer Questions

| QID | Topic | DB Answer | Textbook-Correct Answer | Reference |
|-----|-------|-----------|----------------------|-----------|
| DABT-1869 | Heteroatom dealkylation exception | A (caffeine IS the exception) | Styrene (B) should be exception — caffeine undergoes N-demethylation via CYP1A2; styrene undergoes epoxidation (not dealkylation) | Casarett Ch.6 |
| DABT-1870 | Oxidative desulfuration | E (none correct) | A (parathion to paraoxon) — the textbook example per Casarett Ch.6: "The oxidative desulfuration of parathion" | Casarett Ch.6 |
| DABT-1876 | CYP3A7 location | C (rodent liver) | Fetal human liver — Casarett Ch.6: "CYP3A7 is expressed in the fetal liver" and "human fetal liver expresses CYP3A7, an enzyme capable of activating aflatoxin... whereas no such enzyme is expressed in the fetus of rodents" | Casarett Ch.6 |
| DABT-1878 | CYP450 most abundant in liver+intestine | D (CYP1B1) | CYP3A4 — ~30% of hepatic CYP, ~70-80% of intestinal CYP, metabolizes ~50% of drugs | Casarett Ch.6 |
| DABT-1892 | gemfibrozil glucuronide | D (inhibitor of CYP3A4) | Inhibitor of CYP2C8 — mechanism-based inhibitor, clinically significant interaction with cerivastatin (withdrawn) | FDA guidance, Casarett Ch.6 |

## Error Type C: Toxicokinetics Answer Reversals (Domain I)

| QID | Topic | DB Answer | Textbook-Correct Answer | Reference |
|-----|-------|-----------|----------------------|-----------|
| DABT-1893 | Bioavailability determinants | A (GI absorption only) | D (all of the above) — F = f_abs x (1-E_gut) x (1-E_hep) | Casarett Ch.7 |
| DABT-1894 | Autoinduction example | E (none) | C (carbamazepine) — classic autoinducer of CYP3A4 | Casarett Ch.6 |
| DABT-1896 | Fick's law | C (applies to active transport) | Describes passive diffusion only; active transport requires carriers and ATP | Casarett Ch.7 |
| DABT-1897 | Cross-species scaling | B (benchmark kinetics) | C (allometric scaling) — allometric scaling of parameters is standard in PBPK | Casarett Ch.7 |
| DABT-1901 | PBPK advantage | C (math less complicated) | A (can predict tissue concentrations) — PBPK math is MORE complex | Casarett Ch.7 |
| DABT-1902 | High-E drug clearance | A (protein binding) | B (hepatic blood flow) — CLh approaches Qh when E > 0.7 | Casarett Ch.7 |
| DABT-1906 | 93.8% elimination | E | B (4 half-lives = 93.75%) | Casarett Ch.7 |
| DABT-1909 | Clearance units | B (mg/min) | C (mL/min) — clearance = volume/time | Casarett Ch.7 |

## Error Type D: Cardiac Electrophysiology Answer Reversals (Domain IV)

| QID | Topic | DB Answer | Textbook-Correct Answer | Reference |
|-----|-------|-----------|----------------------|-----------|
| DABT-1912 | Ions in cardiac bioelectricity | B (Na+ is exception) | A (Mg2+ is the exception — Na+, K+, and Ca2+ carry action potential currents; Mg2+ is a cofactor, not a charge carrier) | Casarett Ch.16 |
| DABT-1916 | Cardiac myocyte coordination | E | C (electronic cell-to-cell coupling via gap junctions/connexin-43) | Casarett Ch.16 |
| DABT-1917 | QRS represents | E | B (conduction time through the ventricles / ventricular depolarization) | Casarett Ch.16 |

## Error Rate Summary

- **CYP450 matching test (13 items):** ~100% affected by scrambled answer key
- **CYP450 single-answer (5 items):** 80% (4/5) have wrong stored answers
- **Toxicokinetics (18 items):** ~44% (8/18) have DB discrepancies
- **Cardiac electrophysiology (8 items):** ~38% (3/8) have DB discrepancies
- **Overall batch34:** ~48% (24/50) of questions have at least one DB discrepancy flagged against Casarett & Doull
