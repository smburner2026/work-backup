# Domain I — Conduct of Toxicological Studies (36% of exam)

**Sub-domains:** A. Design (11%), B. Execute (9%), C. Interpret (16%)
**Primary reference:** Casarett & Doull Ch.1-3, Ch.5-7; Hayes Ch.1-3, Ch.6-8
**Question DB volume:** General Principles & Concepts (447 Q), General Toxicology (325 Q), ADME/Toxicokinetics (125 Q), Biotransformation (257 Q)

---

## 1. Dose-Response Relationships

### Definition-First Probes
| Term | Ask | Trap |
|------|-----|------|
| **Graded vs quantal** | "What's the difference conceptually?" | Graded = continuous response in one system; quantal = all-or-none in a population |
| **LD₅₀ vs ED₅₀** | "Which is more precisely estimated and why?" | LD₅₀ uses quantal mortality, wider CI; ED₅₀ depends on what effect you pick |
| **Therapeutic index** | "TI = LD₅₀/ED₅₀ — what does a TI of 100 mean vs 2?" | High TI = safe, low TI = narrow margin. Exam trap: TI uses LD₅₀, not LD₀₁ |
| **Margin of safety** | "How does it differ from TI?" | (LD₀₁/ED₉₉) — more conservative, uses tails not midpoints |
| **NOAEL vs LOAEL** | "Which comes first in a dose-response curve?" | In a well-designed study, NOAEL is one dose level below LOAEL. Trap: they're not fixed properties — they depend on dose spacing, sample size, and endpoint sensitivity |
| **BMD vs NOAEL** | "Why does the EPA prefer BMD?" | Uses the whole dose-response curve, accounts for study power, isn't constrained to tested dose levels. BMDL is the lower bound — analogous to NOAEL but curve-derived |

### High-Yield Exam Traps
- **LD₅₀ ≠ potency** — a highly toxic compound has a LOW LD₅₀ (small dose kills). Students intuitively reverse this.
- **No true threshold for genotoxic carcinogens** — linear low-dose extrapolation. Non-genotoxic carcinogens may have a threshold.
- **Hormesis** — low-dose stimulation, high-dose inhibition. Biphasic dose-response. Know the J-shaped curve. Often tested as "which is NOT a typical dose-response pattern."

### Concrete Anchors
- Ethanol: oral LD₅₀ ~10 g/kg (human). TI ~5-10.
- Botulinum toxin: IP LD₅₀ ~0.3 ng/kg (mouse). One of the most potent known toxins.
- Botox vs arsenic: Botox has lower LD₅₀ (more potent) → sometimes students confuse "more potent" with "higher risk."

---

## 2. ADME / Toxicokinetics

### Absorption Routes
| Route | Key Features | Exam Angle |
|-------|------------|------------|
| **Oral (GI)** | First-pass metabolism (liver), pH partitioning, transporters | Bioavailability F = fraction reaching systemic circulation. Product of absorption × first-pass escape |
| **Inhalation** | Rapid absorption via alveolar epithelium | Gases reach equilibrium: Cₐᵢᵣ × partition coefficient = C_bᵤₗₒₒd. Alveolar area ~100 m² |
| **Dermal** | Stratum corneum barrier; 500 Da rule | Rate-limiting step is stratum corneum for most compounds. Hydration, damage, and occlusion increase absorption |
| **IV** | 100% bioavailability | Reference route. Bypasses all barriers |

### Distribution Barriers
- **BBB**: Tight junctions (endothelial — unlike most capillaries). P-gp efflux limits CNS penetration. Only lipophilic (unionized, low MW) compounds cross. Newborn BBB more permeable.
- **Placental**: Not a tight barrier. Most small molecules cross by passive diffusion. MeHg → methionine mimic → active transport. IgG crosses (FcRn), IgM doesn't.
- **Volume of distribution (Vd)**: Vd = dose/C₀. High Vd (>0.6 L/kg) → extensive tissue binding. Low Vd → stays in plasma/ECF. Trap: Vd doesn't correspond to a real physiological volume — it's a proportionality constant.

### Biotransformation (Phase I & II)
**Phase I** — Introduce or expose functional group (oxidation, reduction, hydrolysis)
- CYP450s: major Phase I enzymes. Families 1-3 handle most xenobiotics
- CYP3A4: most abundant (~30% of liver CYPs), broadest substrate range
- CYP2D6: polymorphic — poor metabolizers (7-10% of Caucasians) are at risk for toxicity of drugs metabolized by this route
- Phase I products are often MORE reactive than parent (bioactivation)

**Phase II** — Conjugate Phase I metabolite (or parent if it already has a handle)
- Glucuronidation (UGTs) — most abundant Phase II
- Sulfation (SULTs) — high-affinity, low-capacity. Easily saturated
- Glutathione conjugation (GSTs) — detoxification of electrophiles. GSH depletion → cell death
- Acetylation (NAT1/NAT2) — polymorphic. Slow acetylators: more toxicity from isoniazid, procainamide, hydralazine

**Exam trap**: "Which pathway is saturated at lower doses?" → SULTs (high-affinity, low-capacity). Glucuronidation is low-affinity, high-capacity — takes over when sulfation saturates.

### Excretion
- **Renal**: Glomerular filtration (free drug only, not protein-bound) + tubular secretion (transporters) + reabsorption (lipophilic drugs). pH trapping: basic urine → acidic drugs excreted faster. Acidic urine → basic drugs excreted faster.
- **Biliary/Fecal**: For compounds >325 Da (biliary threshold in rats) or conjugated. Enterohepatic recirculation — conjugate hydrolyzed by gut flora, parent reabsorbed. Extends half-life.
- **Respiratory**: Gases and volatile organics. Vapor pressure drives elimination rate.

### Toxicokinetic Models
| Model | Description | When applicable |
|-------|------------|----------------|
| **One-compartment** | Body = single well-mixed compartment. Monophasic elimination | Simple drugs, rapid distribution |
| **Two-compartment** | Central (blood + well-perfused tissues) + peripheral (poorly perfused). Distribution phase + elimination phase | Most xenobiotics. α half-life (distribution) then β half-life (elimination) |
| **Non-compartmental** | AUC-based. No model assumption | PK studies, regulatory submissions |
| **PBPK** | Physiological compartments (liver, kidney, fat, etc.) with real blood flows | High-fidelity prediction, cross-species scaling, pregnancy/lifespan models |

**Exam trap:** "First-order vs zero-order kinetics" — First-order: rate ∝ concentration (linear in log plot). Zero-order: constant rate regardless of concentration (saturable). Ethanol at high doses = zero-order. Most drugs at therapeutic doses = first-order.

---

## 3. Study Design

### Experimental Design Essentials
| Element | What the exam tests |
|---------|-------------------|
| **Negative control** | Vehicle-only or sham-treated. Establishes baseline response |
| **Positive control** | Known toxicant at known response level. Validates the assay works |
| **Historical control** | Accumulated control data across studies. Detects drift in animal colony response |
| **Concurrent vs historical** | Concurrent is always preferred. Historical supports but doesn't replace concurrent |
| **Blinding** | Single-blind (subject) vs double-blind (subject + assessor). Prevents expectation bias |
| **Randomization** | Allocates subjects to groups by chance. Prevents selection bias |

### Species Selection Criteria
1. **Metabolic profile matches human** (most important for toxicokinetics)
2. **Sensitivity** to the toxic endpoint
3. **Life-stage relevance** (developmental studies need pregnant animals)
4. **Regulatory acceptance** — most guidelines specify rat (general tox) and mouse (carcinogenicity) as default

**Regulatory standard battery** (most common for general tox):
- Rodent (rat) + non-rodent (dog, minipig, or NHP)
- Both sexes
- Three dose levels + control
- Adequate group sizes for statistical power

### Duration Classification
| Duration | Rodent | Non-rodent | Purpose |
|----------|--------|-----------|---------|
| Acute | Single dose ≤14 days observation | Same | Identify target organs, MTD |
| Subacute | 14-28 days | 14-28 days | Repeat-dose toxicity |
| Subchronic | 30-90 days | 30-90 days | Clinical candidate tox |
| Chronic | ≥6 months (usually 2yr) | ≥6 months (usually 1yr) | Carcinogenicity, lifetime exposure |
| Developmental | GD6-GD15 (rat) or throughout organogenesis | ICH guidelines | Teratogenicity |

### GLP (Good Laboratory Practice)
- **GLP ≠ GMP ≠ GCP** — know the difference: GLP = nonclinical lab studies, GMP = manufacturing, GCP = clinical trials
- GLP governs: study protocol, personnel training, SOPs, equipment calibration, data recording, archiving
- **QA unit** is independent of study director — reads protocols, inspects facilities, audits final report
- Key GLP principle: "What isn't written down didn't happen"

### Route Selection
- Should match **intended human exposure route** (if known)
- Oral is default for food/water contaminants
- Inhalation for airborne toxicants
- Dermal for occupational/workplace exposure
- Common exam trap: "Which route gives the MOST rapid absorption?" → inhalation (alveolar area, no first-pass). IV is fastest but not an 'absorption' route — it's direct administration.

### 3Rs
- **Replace** — use non-animal methods when possible (in vitro, computational)
- **Reduce** — minimize animal numbers without losing statistical power
- **Refine** — minimize pain/distress (analgesia, humane endpoints, enriched housing)

---

## 4. Data Interpretation

### Key Statistical Concepts for DABT
| Concept | Definition | Exam use |
|---------|-----------|----------|
| **Type I error (α)** | False positive — saying there's an effect when there isn't | α = 0.05 is standard. But p < 0.05 ≠ biological significance |
| **Type II error (β)** | False negative — saying there's no effect when there is | Power = 1-β. Low N = low power = can't detect true effects |
| **Multiple comparisons** | More endpoints → higher chance of false positives | Bonferroni correction divides α by number of comparisons |
| **Dose-response trend** | Monotonic increasing effect with dose | Strongest evidence for causation. Non-monotonic doesn't disprove, but is harder to interpret |
| **Historical control range** | Mean ± 2-3 SD from accumulated data | Helps distinguish treatment effect from background fluctuation |

### Interpreting Negative Studies
A study with "no statistically significant findings" ≠ proven safe. Common reasons:
- Low sample size (low power)
- Wrong species (metabolizes the compound differently)
- Wrong route (not matching human exposure)
- Wrong endpoint (not looking at the relevant organ)
- Too-short duration (chronic effects need chronic studies)

### Thresholds vs NOAELs
| Concept | What it's NOT | What it IS |
|---------|--------------|-----------|
| **NOAEL** | Not a threshold (adding more animals could shift it) | The highest dose with no statistically/adversely significant effect |
| **Threshold** | Not directly observable | Concept: a dose below which no adverse effect occurs in a population. Operationalized via NOAEL + UFs |

---

## Integration Points with Other Domains

| Domain I concept | Connects to | Why |
|-----------------|------------|-----|
| Dose-response (NOAEL → BMD) | Domain III (Risk Assessment) | Basis for RfD, slope factor, MOE calculations |
| ADME (bioactivation) | Domain II (Mechanistic) | Why liver is common target; species differences in toxicity |
| Study design (controls) | Domain IV (Applied) | How we know metals/pesticides cause specific organ damage |
| Data interpretation (statistical vs biological) | Domain III (Hazard ID) | Distinguishing adverse from adaptive in risk assessment |
| Biotransformation (CYP induction/inhibition) | Domain II (Mechanisms) + Domain IV (DDIs) | Basis for drug-drug interactions, species extrapolation |

---

## Quick-Reference: High-Yield Exam Traps in Domain I

1. **LD₅₀ = potency, not risk** — botulinum toxin has tiny LD₅₀ (highly potent) but low real-world exposure risk. Ethanol has high LD₅₀ (low potency) but causes more deaths.
2. **Volume of distribution ≠ real volume** — Vd = dose/C₀. High Vd means extensive tissue binding. Not the same as plasma volume or TBW.
3. **First-pass ≠ absorption** — they're separate. F = f_abs × (1 - E_hepatic). A drug can be fully absorbed (f_abs = 1) but have low F due to extensive hepatic extraction.
4. **GLP ≠ research quality** — GLP is about documentation, traceability, and reproducibility. Exploratory research can use non-GLP methods. Registration studies must be GLP-compliant.
5. **NOAEL increases with dose spacing** — poorly designed study with wide dose spacing gives a higher NOAEL (less protective). BMD doesn't have this problem.
6. **p < 0.05 ≠ biologically significant** — a 2% change in organ weight in 1000 animals may be statistically significant but biologically meaningless.
7. **One-compartment model ≠ reality** — it's a mathematical simplification. Most toxicants follow at least two-compartment kinetics.
