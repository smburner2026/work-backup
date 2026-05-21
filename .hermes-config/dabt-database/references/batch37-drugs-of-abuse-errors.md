# Batch 37 — Drugs of Abuse / Forensic Toxicology (Domain IV)

**File:** `/root/work/dabt/dabt-tutor/batches/batch37.json` → `batch37_done.json`
**Date:** 2026-05-20
**Questions:** DABT-2019 to DABT-2068 (50 Qs)
**Source:** dabt_extract_2000q.csv (2000Q Bank, source_file_id=2)
**Domain:** Domain IV — Applied Toxicology
**DB Error Rate:** 0/50 (0%) — third clean 2000Q Bank sub-source identified

## Topic Coverage

This batch covers Drugs of Abuse and Forensic Toxicology — the pharmacology, toxicology, and forensic detection of psychoactive substances:

| Topic | Questions | Key Content |
|-------|-----------|-------------|
| **Opioids** | DABT-2019–2046 | Codeine→morphine metabolism, heroin half-life, oxycodone epidemiology, morphine metabolites (M3G/M6G potency hierarchy), postmortem free vs total morphine, 6-AM as specific heroin marker (10 ng/mL cutoff), poppy seed vs heroin distinction (thebaine, 6-AM false negatives), endogenous opiate peptides (dynorphin, β-endorphin, endomorphin vs synthetic alfentanil), opiate receptor structure (7TM GPCR), drug adulterants (quinine, caffeine, diphenhydramine vs spironolactone), diluents (lactose, starch, mannitol vs methamphetamine), methadone pharmacology (hERG QT prolongation, CYP3A4/CYP2B6 metabolism, d/l isomer activity, AAG protein binding, tolerance via hair analysis) |
| **Hallucinogens** | DABT-2022–2028, 2064, 2067–2068 | Psilocybin pharmacology (tryptamine derivative, 5-HT2A-mGluR2 complex), LSD (5-HT2 mechanism, comparison to mescaline), sigma receptor reclassification, mescaline source (peyote cactus), MDMA classification (hallucinogenic amphetamine), CYP2D6 inhibition, monoamine release (DA/5-HT/NE), serotonin syndrome risk (meperidine, tramadol, DXM vs nadolol), Salvia divinorum (salvinorin A, KOR agonist), PCP (schizophrenia model, NMDA antagonism), ketamine (NMDA receptor binding, dissociative anesthetic) |
| **Cannabinoids** | DABT-2048–2051 | THC pharmacology (CB1/CB2, high Vd, rapid blood peak), THC-COOH as urine screening target (11-nor-9-carboxy-THC), postmortem THC interpretation difficulties, dronabinol indications (chemo nausea, AIDS wasting, false positive urine screen) |
| **Stimulants** | DABT-2052–2056 | Chronic amphetamine effects (permanent neuronal damage, vasculitis, pulmonary hypertension vs glioblastoma), methamphetamine as most common US clandestine lab drug, cocaine-induced ACS management (contraindication of β-blockers, preference for calcium channel blockers for SVT, propofol for refractory agitation), excited delirium |
| **Ethanol** | DABT-2057–2061 | Ethanol biomarkers (FAEEs, EtS, EtG vs pyruvate), lack of single ethanol receptor (GABA enhancement, NMDA blockade, withdrawal = NMDA upregulation), withdrawal syndrome management (benzodiazepines prevent seizures, NOT phenytoin), disulfiram-type reactions (cefoperazone, metronidazole, chlorpropramide vs zaleplon), thiamine deficiency sequelae (wet beriberi, Wernicke-Korsakoff vs pulmonary fibrosis) |
| **Other Drugs of Abuse** | DABT-2062–2066 | GHB pharmacology (endogenous NT, GH releaser, drug of abuse, 1,4-butanediol toy bead epidemic 2007), Kratom (mitragynine, partial μ-opioid agonist), amyl nitrite (methemoglobinemia), Salvia divinorum classification |
| **Anabolic Steroids** | DABT-2047 | Urine T/E ratio (testosterone/epitestosterone) as standard doping detection test |
| **Miscellaneous** | DABT-2022 | Nutmeg as hallucinogenic spice (myristicin→MMDA) |

## DB Answer Quality

**All 50 questions have correct DB answers.** No errors found:
- No letter-E corruptions (all answers are A, B, C, or D with corresponding options)
- No "EXCEPT" reversal issues
- No matching-test scrambled items (all are standard MCQs with full 4-option sets)
- No zero-option questions
- No parsing issues (no merged options, no concatenated text)

This makes Drugs of Abuse the **third clean 2000Q Bank sub-source** identified, alongside:
- **Air Pollution** (batch25, 36 Qs, 0% error)
- **Food Safety** (batch28, 11 Qs, 0% error)
- **Drugs of Abuse** (batch37, 50 Qs, 0% error)

These sub-sources appear to have been extracted with better QC than other 2000Q Bank sections.

## Primary Reference

**Casarett & Doull Ch.33 — Clinical Toxicology** is the most relevant reference for this topic area. This chapter covers:
- General approach to the poisoned patient
- Specific substance toxicology (opioids, stimulants, hallucinogens, ethanol, cannabinoids)
- Forensic toxicology principles (postmortem redistribution, specimen selection, interpretation)
- Biomarkers of exposure

For mechanism-level opioid pharmacology, also consult C&D Ch.6 (Biotransformation) for codeine→morphine CYP2D6 toxification and morphine glucuronidation patterns.

For specific forensic toxicology detail (6-AM cutoffs, T/E ratio, postmortem redistribution), also consult standard forensic toxicology references (e.g., Baselt's Disposition of Toxic Drugs and Chemicals).
