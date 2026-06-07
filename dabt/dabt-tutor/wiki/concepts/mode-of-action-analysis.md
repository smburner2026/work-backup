---
tags: [concept, domain-i-c, domain-iii-d, weight-25, risk-assessment, mechanisms]
domain: I-C Interpret / III-D Risk Characterization
exam_weight: 25
sources: [cd-8, hayes-3, epa-cancer-2005, ich-m7r2]
related: [[adversity-determination]], [[dose-response-assessment]], [[human-relevance-framework]]
---

# Mode of Action (MOA) Analysis

> A structured framework for *how* a chemical causes an adverse outcome — the chain of key events from initial molecular interaction to apical effect — used to decide whether a default safety assumption (linear, threshold) is justified or should be replaced with mechanism-based extrapolation.

## Why it matters

MOA is the bridge between **mechanism** (Domain II, 13%) and **risk characterization** (Domain III-D, 9%) and **interpretation** (Domain I-C, 16%). Total exposure across the exam: roughly **25% when you count the cross-domain spillover**. The 2026 ABT blueprint explicitly elevates MOA analysis — and the 2005 EPA Cancer Guidelines made it a hard requirement for any cancer risk assessment that wants to deviate from default linear extrapolation.

## The framework

A complete MOA analysis has four components, in this order:

### 1. Identify the hypothesised MOA
- Molecular initiating event (MIE) — first interaction at the molecular level
- Key events (KE) — measurable intermediate steps
- Adverse outcome (AO) — the apical effect of regulatory concern
- This is the *Adverse Outcome Pathway (AOP)* at its most reduced: MIE → KEs → AO

Source: C&D ch 8 (Carcinogenesis), p. line 5639, 5729-5758 — AOP framework with MIE/KE/AO diagram.

### 2. Test the MOA against modified Bradford Hill criteria
EPA's 2005 Cancer Guidelines adapted Bradford Hill's epidemiological criteria for mode-of-action analysis. The 9 considerations:

| # | Criterion | Question it answers |
|---|-----------|---------------------|
| 1 | Dose-response concordance | Do MIE/KE/AO all rise with dose? |
| 2 | Temporal concordance | Does MIE precede KE precedes AO? |
| 3 | Strength, consistency, specificity of association | Is the MIE→AO link reproducible? |
| 4 | Biological plausibility | Is the chain mechanistically credible? |
| 5 | Coherence | Does it fit what we know from other evidence? |
| 6 | Alternative MOAs | Are there competing explanations we ruled out? |
| 7 | Uncertainties, inconsistencies | Where's the data weakest? |
| 8 | Quantitative relationships | Can we model the dose-response at each step? |
| 9 | Human relevance | Does the chain operate in humans? |

Source: EPA Cancer Guidelines 2005, p. lines 951, 1905 — MOA analysis framework with human-relevance requirement.

### 3. Decide on the dose-response extrapolation approach
Once the MOA is established, the choice is binary:

- **Linear extrapolation (default for DNA-reactive genotoxic carcinogens)** — one molecule can theoretically cause a mutation, so any dose carries risk proportional to dose. LNT model. Default under EPA unless MOA justifies otherwise.
- **Nonlinear / threshold extrapolation (justified when MOA has a clear threshold)** — e.g., cytotoxicity-driven tumors at high doses only, receptor-mediated effects with spare receptors, nongenotoxic mechanisms with detoxification. Below threshold, risk is effectively zero.

### 4. Address human relevance explicitly
Even if the MOA is established in animals, you must show the key events operate in humans (or don't). The IPCS Human Relevance Framework is the standard:

- Is the MIE active in humans?
- Are the KEs operative in humans?
- Is the AO a human concern?

If any link breaks, the animal MOA may be irrelevant to human risk.

## MOA vs. mechanism — the exam trap

| | MOA | Mechanism |
|---|---|---|
| Question answered | "How does it work in this *specific* case, dose-response shape implied?" | "What biological process is involved at a fundamental level?" |
| Required for | Risk assessment, regulatory decision | Scientific understanding |
| Granularity | MIE → KEs → AO (pathway) | Any level of biological detail |
| Exam question shape | "What is the MOA of X?" → "What dose-response model follows?" | "What is the mechanism of toxicity for X?" → "What is the molecular target?" |

If a question asks for **dose-response implications** (linear vs nonlinear, threshold, default assumptions), it's asking for MOA. If it asks for **biological understanding** (what receptor, what pathway), it's asking for mechanism.

## Worked example: A alpha (alpha-particle) emitters

**MIE**: direct DNA double-strand break from alpha particle track
**KEs**: unrepaired DSB → chromosomal aberration → mutation → clonal expansion
**AO**: cancer
**Bradford Hill**: dose-response concordance ✓, temporal concordance ✓, biological plausibility ✓, strength ✓
**Extrapolation**: linear (DNA-reactive, no threshold plausible for the MIE itself)
**Human relevance**: yes — DNA damage is human-relevant

→ Cancer slope factor (CSF), linear low-dose extrapolation. No threshold.

Contrast with **chloroform**:
**MIE**: cytotoxicity at high doses → regenerative hyperplasia → tumors
**KEs**: cell death → proliferation → mutation in proliferating cells
**AO**: kidney/liver tumors
**Extrapolation**: nonlinear / threshold (cytotoxicity is the rate-limiting step, not direct DNA damage)
**Human relevance**: yes

→ RfD approach, applied UFs to a NOAEL or BMDL. Threshold model justified.

## Exam traps

- **"MOA" ≠ "mechanism"** — mechanism is the broad biology; MOA is the regulatory chain that justifies a dose-response choice.
- **Default is linear for carcinogens** — you have to *argue* for nonlinear with a documented MOA, not assume it.
- **Human relevance is a separate step** — an animal MOA, however well-established, doesn't transfer to humans without IPCS HRF analysis.
- **AOP is descriptive; MOA is analytical** — AOP maps the pathway; MOA tests it against Bradford Hill and picks the dose-response model.
- **Receptor-mediated ≠ automatically threshold** — depends on spare receptors, irreversibility, downstream kinetics.

## Drill signal

When a question says: "What is the most appropriate dose-response model for X?" — that's MOA. When it says: "Explain how X causes toxicity at the cellular level" — that's mechanism. When it says: "Justify the regulatory approach for X" — that's MOA + human relevance.

Linked from [[adversity-determination]] (Layer 3 framework) and from [[miss-journal/2026-05-28-flashcard-review-risk-assessment]] (BMR defaults and POD selection are downstream MOA decisions).
