# DABT Exam Blueprint — Updated May 2026 (2022 Practice Analysis)

## Source

The current DABT exam blueprint is based on the **2020-2021 Practice Analysis** published in the *International Journal of Toxicology* (2023, PMC10493040). This replaced the pre-2017 5-domain structure with 4 testable domains + 1 non-testable domain. The exam was shortened from 300 to 200 questions (2017) then to 140 scored + 20 pretest = 160 total (2022).

## The 4 Testable Domains

The 2026 ABT Candidate Handbook (p.24) publishes exact domain weights. These are the authoritative blueprint for question selection and study prioritization.

| Domain | Tasks | Exam Weight | Sub-domain Weights | Focus |
|--------|-------|-------------|---------------------|-------|
| **I. Conduct of Toxicological Studies** | 13 | **36%** | Design 11%, Execute 9%, **Interpret 16%** | Design, execute, interpret toxicology studies |
| **II. Mechanistic Toxicology** | 8 | **13%** | — | MOA/AOP, species differences, susceptibility |
| **III. Risk Assessment** | 15 | **38%** | Hazard ID 12%, Exposure 8%, Dose-Response 9%, Risk Char 9% | Hazard ID, exposure, dose-response, characterization |
| **IV. Applied Toxicology** | 12 | **13%** | — | Ecotox, forensic, regulatory, occupational |

Domain V (Contribution to Profession, 9 tasks) is **non-testable**.

**CRITICAL NOTE:** The question database (4,841 Qs) does NOT reflect these weights. Domain III (38% of exam) has only ~210 questions (4.5% of DB). Domain IV (13% of exam) has ~2,850 questions (60.5% of DB). Blueprint-weighted sampling will deplete Domain III rapidly — supplement with textbook-based custom questions (Casarett Ch.4, Hayes Ch.3, EPA guidelines). The `dabt-deep-dive` skill's `references/abt-handbook-blueprint.md` has the full task statement and knowledge topic breakdown.

### Domain I — Conduct of Toxicological Studies
- Study design principles, GLP compliance, OECD/ICH guidelines
- Dose selection, route, species/strain, sample size, statistics
- Study execution: data collection, QA, histopathology, clinical pathology, necropsy
- **Data interpretation** — largest single competency area on the exam
- NOAEL/LOAEL identification, adversity determination
- Weight-of-evidence conclusions

### Domain II — Mechanistic Toxicology
- Mode of Action (MOA) / Adverse Outcome Pathway (AOP) framework
- Species differences in toxic response
- Susceptibility factors (genetic, age, sex, health status)
- Direct vs indirect toxic action
- Translation: in vitro → in vivo → human
- Disease and genetic models

### Domain III — Risk Assessment
- Hazard identification: weight of evidence, cancer classification (EPA, IARC)
- Epidemiology, SAR, read-across
- Exposure assessment: biomonitoring, occupational, environmental, consumer
- Dose-response: BMD modeling, NOAEL/LOAEL, POD selection
- Uncertainty factors (UF), modifying factors (MF), database UF
- Margin of Exposure (MOE), risk characterization
- Risk management and communication

### Domain IV — Applied Toxicology
- Ecotoxicology and environmental toxicology
- Public health response and emergency management
- Exposure reconstruction and biomonitoring programs
- Susceptible subpopulations (children, elderly, pregnant)
- Forensic toxicology, clinical toxicology
- Occupational toxicology, industrial hygiene
- Regulatory toxicology (FDA, EPA, OSHA frameworks)
- Sustainable product development / green chemistry
- Food toxicology, natural toxins

## Mapping Old-Format Questions to Current Domains

Our question banks (2000Q, Chapter Tests, Kristen materials) are organized by C&D chapters. Use this mapping to reframe old-format questions into the current domain structure:

| Old Chapter / Topic | Maps Primarily To | Also Relevant To |
|---------------------|-------------------|------------------|
| General Principles (Ch1-2) | Domain I | Domain II |
| Mechanisms of Toxicity (Ch3) | Domain II | Domain I |
| Risk Assessment (Ch4) | Domain III | - |
| ADME / Toxicokinetics (Ch5-7) | Domain I | Domain II |
| Biotransformation (Ch6) | Domain II | Domain I |
| Carcinogenesis (Ch8) | Domain II | Domain III |
| Genetic Toxicology (Ch9) | Domain I | Domain II |
| Developmental/Repro (Ch10,20) | Domain I | Domain II |
| Organ System Toxicity (Ch11-19) | Domain II | Domain IV |
| Pesticides (Ch22) | Domain IV | Domain III |
| Metals (Ch23) | Domain IV | Domain II |
| Solvents (Ch24) | Domain IV | Domain II |
| Radiation (Ch25) | Domain IV | Domain I |
| Food Toxicology (Ch30) | Domain IV | Domain III |
| Analytical/Forensic (Ch31) | Domain IV | Domain I |
| Occupational (Ch33) | Domain IV | Domain III |
| Ecotoxicology (Ch28-29) | Domain IV | Domain III |
| Clinical Toxicology | Domain IV | Domain II |

## Exam Logistics

- **Length:** 140 scored + 20 pretest = **160 MCQs, 4 hours**
- **Delivery:** In-person at Pearson VUE centers (no online proctoring)
- **Scoring:** Single composite score, pass/fail only (scores not released)
- **Pass rate:** ~72% (consistent 2017-2024)
- **Passing standard:** Set via modified Angoff procedure (2022 standard setting study)

## Sample Questions (from ABT website, current 2026)

### Domain I Example: "In a reproductive toxicity study, what is the 'fertility index'?" — Answer: B) percentage of attempted matings resulting in pregnancies

### Domain II Example: "What is the mechanism of neurotoxicity for strychnine?" — Answer: A) glycine receptor antagonist

### Domain III Example: "What is a limitation of the benchmark dose approach in risk assessment?" — Answer: C) is based on a predefined benchmark response that is arbitrary

### Domain IV Example: "What was the regulatory response to the Delaney clause?" — Answer: C) prohibited FDA from approving food additives found to cause cancer in animals

## References

- 2022 Practice Analysis: PMC10493040 (Int J Toxicol, 2023)
- 2026 ABT Candidate Handbook: abtox.org/wp-content/uploads/2026/02/ABT-Candidate-Handbook-2026.pdf
- ABT Sample Questions: abtox.org/candidates/sample-questions/
- Full analysis reports: /root/dabt-curated/FULL_ANALYSIS_REPORT.md, /root/dabt_comprehensive_analysis.json
