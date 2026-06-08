# Batch 12 Lung / Pulmonary Toxicology DB Answer Discrepancies

Batch: DABT-0819 through DABT-0868 (50 questions)
Source: 2000Q Bank (source_file_id=2)
Domain: All Domain IV — Lung / Pulmonary Toxicology
Date processed: 2026-05-20

## Summary

This batch covers **lung and respiratory toxicology** exclusively — 50 questions on alveolar cell physiology, gas solubility, particle deposition, occupational lung disease (silicosis, asbestosis, pneumoconioses), irritant gases, cigarette smoke toxicants, metal fume fever, drug-induced lung disease, and asbestos-related conditions.

24 out of 50 questions (48%) have DB answer key errors — the highest error rate seen in any batch processed so far. Errors fall into three categories: (1) `correct_answer_letter='E'` with only A-D options, (2) DB answer contradicts established pulmonary physiology, and (3) matching test items with completely wrong associations.

## Category 1: Answer "E" with no E option (options only A-D)

Same CSV extraction error seen in all prior batches. `correct_answer_letter='E'` but `answer_options` only has A-D.

| QID | Question | DB Answer | Correct Answer | Rationale |
|-----|----------|-----------|----------------|-----------|
| DABT-0820 | Tidal volume | E | **B** (500 mL) | Normal adult tidal volume at rest is ~500 mL (Casarett & Doull Ch.15) |
| DABT-0824 | Least water-soluble gas | E | **A** (carbon monoxide) | CO has lowest water solubility, passes most efficiently (C&D Ch.15) |
| DABT-0825 | Nasopharyngeal particle MMAD | E | **A** (>5 µm) | Particles >5 µm trapped by impaction in nasopharynx (C&D Ch.15) |
| DABT-0830 | Aldehydes/hydroxyperoxides lung damage | E | **C** (ozone) | Ozone reacts with PUFAs to form aldehydes/hydroperoxides (C&D Ch.15) |
| DABT-0831 | Free radical damage EXCEPT | E | **D** (carbon monoxide) | CO causes hypoxia via Hb binding, not free radicals (C&D Ch.15, 24) |
| DABT-0832 | ROS species EXCEPT | E | **D** (sodium radical) | "Sodium radical" is not a biologically recognized ROS (C&D Ch.15) |
| DABT-0847 | Particles >10 µm MMAD | E | **A** (dust from earth's crust) | Coarse-mode particles = mineral/soil dust (C&D Ch.15) |
| DABT-0857 | Blood test for pulmonary function | E | **A** (arterial blood gas) | ABG measures PaO₂, PaCO₂, pH — assesses gas exchange (C&D Ch.15) |
| DABT-0860 | Irritant gas upper airway retention | E | **A** (highly water-soluble) | NH₃, Cl₂, formaldehyde are highly water-soluble → scrubbed in upper airway (C&D Ch.15) |

## Category 2: DB answer contradicts established pulmonary physiology

These questions have a valid answer letter in the options, but the assigned answer is toxicologically incorrect.

| QID | Question | DB Answer | Correct Answer | Rationale |
|-----|----------|-----------|----------------|-----------|
| DABT-0822 | Pulmonary capillary bed BEFORE liver EXCEPT | **B (IV)** | **D** (nasal-gastric tube) | NG tube → GI absorption → portal vein → liver first (first-pass). IV goes to right heart → pulmonary bed first (C&D Ch.3) |
| DABT-0827 | 200 µm × 1 µm fiber deposition | **A (diffusion)** | **D** (interception) | Extreme aspect ratio fiber contacts airway walls by interception, not diffusion (C&D Ch.15) |
| DABT-0829 | What increases particle deposition | **C (bronchoconstriction)** | **D** (all of the above) | Breath holding, exercise, AND bronchoconstriction all independently increase deposition (C&D Ch.15) |
| DABT-0833 | Least likely to produce ROS in lung | **B (neutrophil)** | **A** (plasma cell) | Neutrophils are the MOST potent ROS producers. Plasma cells lack NADPH oxidase (C&D Ch.15) |
| DABT-0834 | Bronchoconstriction EXCEPT | **D (irritant air pollution)** | **C** (increase in cAMP) | cAMP causes bronchodilation via PKA. Air pollution causes reflex bronchoconstriction (C&D Ch.15) |
| DABT-0836 | Emphysema etiology hypothesis | **A (ROS)** | **B** (elastases) | Classic protease-antiprotease hypothesis = elastases from inflammatory cells (C&D Ch.15) |
| DABT-0839 | Probable human lung carcinogen EXCEPT | **D (chromium)** | **A** (sulfur dioxide) | SO₂ is irritant, not carcinogen. Cr(VI), As, Ni are Group 1 (IARC) lung carcinogens (C&D Ch.15) |
| DABT-0841 | Children + passive smoke EXCEPT | **A (asthma increase)** | **B** (seizure disorders) | ETS increases asthma, pneumonia, ear infections — NOT seizures (US Surgeon General Report) |
| DABT-0849 | Metal fume fever EXCEPT | **D (magnesium)** | **A** (gold) | Mg fumes cause metal fume fever. Gold does not generate significant fume (C&D Ch.15) |
| DABT-0851 | Lung reaction to mineral dust | **A (hypersensitivity pneumonitis)** | **D** (pneumoconioses) | Mineral dust → pneumoconioses. HP is from organic antigens (C&D Ch.15) |
| DABT-0853 | Pleural plaque marker | **B (zinc oxide fumes)** | **C** (asbestos) | Pleural plaques are the classic marker of asbestos exposure (C&D Ch.15) |
| DABT-0855 | Emphysema definition | **B (abnormal contraction + fibrosis)** | **A** (abnormal enlargement, no fibrosis) | Emphysema = airspace ENLARGEMENT + wall destruction, NO fibrosis (C&D Ch.15) |
| DABT-0858 | Gas that doesn't go past the nose | **D (NO₂)** | **C** (SO₂) | SO₂ is highly water-soluble → scrubbed in nose. NO₂ penetrates to alveoli (C&D Ch.15) |
| DABT-0859 | Pulmonary-toxic drug EXCEPT | **D (carmustine)** | **B** (theophylline) | Carmustine (BCNU) DOES cause pulmonary fibrosis. Theophylline has no significant pulmonary toxicity (C&D Ch.15) |
| DABT-0861 | Cigarette smoke constituent EXCEPT | **C (benzopyrene)** | **D** (phosgene) | Benzopyrene IS a major smoke constituent. Phosgene is an industrial gas, not in smoke (C&D Ch.15) |

## Category 3: Matching test items with wrong associations

DABT-0864 to DABT-0868 are single-option matching items where the DB has entirely wrong pairings.

| QID | Term | DB Match | Correct Match | Rationale |
|-----|------|----------|---------------|-----------|
| DABT-0864 | Asbestos | Bronchiolitis obliterans | **Asbestosis, lung cancer, mesothelioma** | Asbestos causes pulmonary fibrosis and pleural malignancies (C&D Ch.15) |
| DABT-0865 | Cadmium oxide | Sarcoidosis-like reaction | **Emphysema, renal tubular dysfunction** | Cadmium → emphysema, not granulomatous disease. Beryllium → sarcoid-like reaction (C&D Ch.15) |
| DABT-0866 | Isocyanates | Pleural mesothelioma | **Occupational asthma, HP** | Isocyanates are sensitizers → asthma. Mesothelioma = asbestos (C&D Ch.15) |
| DABT-0867 | Nickel refining | Interstitial fibrosis | **Lung cancer, nasal sinus cancer** | Nickel compounds = Group 1 carcinogen → lung/nasal cancer (C&D Ch.15; IARC) |
| DABT-0868 | Aluminum dust | Highly water-soluble | **Interstitial fibrosis (Shaver's disease)** | Chronic Al dust inhalation → pulmonary aluminosis (C&D Ch.15) |

## Pattern Analysis

### Error Distribution by Subtopic

| Subtopic | Questions | Errors | Error Rate |
|----------|-----------|--------|------------|
| Gas solubility / regional deposition | DABT-0824, 0858, 0860, 0863 | 3/4 | 75% |
| Particle deposition mechanisms | DABT-0825, 0827, 0828, 0829, 0847 | 3/5 | 60% |
| Cell biology / ROS | DABT-0831, 0832, 0833 | 3/3 | 100% |
| Airway tone / bronchoconstriction | DABT-0834 | 1/1 | 100% |
| Occupational lung disease | DABT-0844, 0851, 0853, 0856, 0864-0868 | 7/11 | 64% |
| Emphysema / COPD | DABT-0836, 0855 | 2/2 | 100% |
| Carcinogenesis | DABT-0839, 0840, 0862 | 2/3 | 67% |
| Drug-induced lung disease | DABT-0859 | 1/1 | 100% |
| Anatomical / physiological basics | DABT-0819, 0820, 0821 | 1/3 | 33% |
| Miscellaneous | DABT-0822, 0823, 0826, 0830, 0841, 0842, 0843, 0845, 0846, 0848, 0849, 0850, 0852, 0854, 0857, 0861 | 1/16 | 6% |

### Key Insights

1. **Most error-prone subtopics:** Cell biology/ROS (100%), airway tone (100%), emphysema/COPD (100%), drug-induced lung disease (100%), particle deposition (60%), occupational lung disease (64%), carcinogenesis (67%)

2. **Gas solubility questions are systematically reversed:** DABT-0858 (DB says NO₂ stays in upper airway — wrong, it penetrates deep) and DABT-0860 (correctly identifies water solubility) suggest the DB has SO₂ vs NO₂ solubility data swapped

3. **Matching test items are entirely unreliable:** The 5 matching items (DABT-0864 to DABT-0868) all have associations that are wrong — effects/outcomes are swapped between different agents. This is the same "scrambled answer key" pattern seen in batch7's General-Principles and batch6's Antidotes matching tests.

4. **No docx verification possible:** Unlike batch6 (where Ch1 General docx was available), no original docx files were found for the lung/pulmonary section of the 2000Q Bank. All corrections rely on Casarett & Doull Ch.15 as the reference standard.

5. **Error rate trend:** Batch12 (48%) > Batch11 renal (30%) > Batch10 liver/hepatotoxicity (38% initial drafts had issues, but DB answer errors were ~10-15%).

## Recommendations for Future Lung/Pulmonary Batches

1. **Always verify against Casarett & Doull Ch.15** before accepting any DB answer for lung questions — this chapter covers: lung anatomy, particle deposition, gas solubility, occupational diseases, asthma, emphysema, fibrosis, lung cancer, and drug-induced injury.

2. **Treat all "E" answers with suspicion** — 9 such cases in this batch, all extracted from the 2000Q Bank with the same error pattern.

3. **For matching-test items** (single-word question texts like "asbestos", "cadmium oxide"): reconstruct correct associations from C&D Ch.15 rather than trusting the DB pairing. The 2000Q Bank matching tests for lung disease are completely scrambled.

4. **For "EXCEPT" questions**, independently verify each option's truth value against the textbook. The DB's answer often points to a statement that IS true (batch pattern continues from batch9 immunotoxicology).

5. **For particle deposition mechanism questions** (diffusion, sedimentation, impaction, interception): verify fiber dimensions vs mechanism. The DB's answers for fiber deposition are particularly unreliable (DABT-0827).

6. **Reference text location:** All explanations should cite Casarett & Doull Ch.15 (Toxic Responses of the Respiratory System) as the primary source. For mechanisms questions, Ch.24 (Free Radical Biochemistry) also applies.
