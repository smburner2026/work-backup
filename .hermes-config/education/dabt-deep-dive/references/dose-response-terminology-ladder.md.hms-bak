# Dose-Response Terminology Ladder — Risk Assessment

**Domain:** III. Risk Assessment — Dose-Response Assessment (9% of exam)
**Sub-domain:** C. Dose-Response Assessment, D. Risk Characterization
**Source session:** 2026-05-26
**Learner:** TempMoon (Advanced DABT candidate, Oct 2026)
**Prerequisite:** NOAEL/LOAEL framework, basic dose-response curve concepts

---

## Progression (fixed order)

Each rung builds on the last. Do not skip rungs.

1. **NOAEL vs LOAEL** — what each is, where they sit on the curve, study design dependency
2. **BMD / BMDL** — why it exists, what problem it solves vs NOAEL
3. **Uncertainty Factors (UFs) + Modifying Factors (MFs)** — when 10× is 10× and when it's not
4. **RfD / RfC** — the downstream regulatory product
5. **Linear vs nonlinear low-dose extrapolation** — the cancer vs non-cancer fork
6. **Cancer Slope Factor (CSF) vs Unit Risk** — what they express, how derived
7. **Margin of Exposure (MOE)** — where and why

---

## Rung 1 — NOAEL vs LOAEL

### Definitions (ABT Handbook)

- **NOAEL (No-Observed-Adverse-Effect Level):** The highest dose at which no *adverse* effects are detected. "Adverse" is key — statistically significant changes that are biologically adaptive (e.g., mild body weight decrease without correlating pathology) do not qualify.
- **LOAEL (Lowest-Observed-Adverse-Effect Level):** The lowest dose at which an *adverse* effect is detected.

### Key Properties

| Property | NOAEL | LOAEL |
|---|---|---|
| Study-design dependent | Yes — must be a tested dose | Yes — must be a tested dose |
| Sample-size dependent | Yes — higher n = more power to detect effects | Same |
| Requires expert judgment | Yes — distinguishing adverse vs adaptive | Same |
| Has confidence interval | No | No |
| Accounts for slope | No | No |
| Affected by dose spacing | Heavily — gaps between doses can mask the true threshold | Heavily |

### Classic Exam Confusions

1. **"Statistical significance = adversity."** This is the single most common error. A p<0.05 finding without histopathological, clinical, or biological correlation is not automatically adverse. Body weight changes of 5-10% without target organ pathology are often adaptive, not adverse.
2. **"NOAEL = no effect."** NOAEL means no *adverse* effect. There can be (and often are) statistically significant non-adverse effects at the NOAEL.
3. **"NOAEL applies across studies."** The NOAEL is study-specific — tied to the dose levels, duration, species, and endpoint selection of that specific study.
4. **"The NOAEL is a biological threshold."** It's an artifact of the test doses chosen, not an intrinsic property of the chemical.

### MCQ Example

A 28-day oral toxicity study tested a chemical at 0, 10, 50, or 250 mg/kg/day (n=10/sex/dose). Results:
- 10 mg/kg: all endpoints normal
- 50 mg/kg: body weight gain decreased 8% (p<0.05), no other changes
- 250 mg/kg: ALT/AST 3× (p<0.001), centrilobular hypertrophy

**Correct NOAEL: 50 mg/kg.** The 8% body weight decrease at 50 is statistically significant but not adverse (no correlating histopathology, clinical chemistry, or organ weight changes). The LOAEL is 250 mg/kg.

**Distractor rationale:**
- *10 mg/kg (Option A):* Targets confusion of "statistical significance" with "adversity." Reasoning error: treating a significant-but-non-adverse finding as if it were adverse, forcing the NOAEL down to the next tested dose.
- *250 mg/kg (Option C):* Targets endpoint cherry-picking. Reasoning error: "ALT was normal at 50, so 250 must be fine too" — ignores clear adverse effects (ALT 3× + histopathology) at 250.
- *Cannot determine — 28 days is too short (Option D):* Targets study-type confusion. Reasoning error: 28-day OECD 407 studies are standard for NOAEL determination. You absolutely can and must identify NOAELs from them. The NOAEL is *descriptive* for the study, not *prescriptive* for lifetime exposure.

---

## Rung 2 — BMD / BMDL

### Definitions

- **BMD (Benchmark Dose):** The dose that produces a pre-specified **benchmark response (BMR)** — typically 10% increase in adverse effect incidence above background for quantal data, or 1 SD change for continuous data. Derived by fitting a statistical model to the full dose-response data.
- **BMDL (Benchmark Dose Lower bound):** The 95% lower confidence bound on the BMD. The frequentist interpretation: if the study were repeated many times, 95% of BMDLs would be ≤ the true dose that produces the BMR.

### Why BMD Exists (Problems Solved vs NOAEL)

| NOAEL Problem | BMD Solution |
|---|---|
| Must be a tested dose (dose-spacing artifact) | Interpolated from the fitted model — not limited to tested doses |
| No confidence interval | BMDL provides a 95% lower bound that reflects study quality |
| Ignores dose-response slope | Uses the full curve shape, not just one point |
| Sensitive to sample size (small n → higher NOAEL) | BMDL narrows with better data, widens with poorer data |

### Classic Confusions

1. **"BMDL = threshold for no effect."** The BMDL corresponds to the BMR (e.g., 10% extra risk). A dose at the BMDL means the model projects a BMR-level effect at or above that dose — it is NOT a "no-effect level."
2. **"95% confident that anything below the BMDL is safe."** That's not how confidence intervals work. The frequentist interpretation is about the estimation procedure, not a specific probability of safety.
3. **"BMD replaces NOAEL entirely."** BMD is preferred when the data support it (3+ dose groups, good model fit), but NOAEL is still accepted as a fallback when data are too sparse.

### Teaching Analogies

**The famine analogy (BMD vs BMDL):**

Imagine you're figuring out how many days of food shortage it takes before 10% of oxen in a village die. Four villages are tested at different ration durations:

- 0 days: 0% die
- 10 days: 0% die
- 30 days: 0% die
- 90 days: 60% die

**NOAEL approach:** 30 days — no deaths observed. You'd say the NOAEL is 30 days. But you never tested 40, 50, 60, or 70 days. The true threshold could be anywhere in that gap.

**BMD approach:** A model is fitted to the 4 data points. The model estimates that at **38 days**, 10% excess mortality occurs (BMD₁₀). The 95% lower bound, accounting for limited sample size, is **24 days** (BMDL₁₀).

**What each means:**
- BMD₁₀ = 38 days: best-estimate dose for 10% excess mortality
- BMDL₁₀ = 24 days: we're 95% confident the true BMD is ≥ 24 days

The regulator uses 24 days (BMDL), not 38 days (BMD). Not because 24 days itself kills 10% of oxen — but because the data are noisy enough that the *true* dose for 10% mortality could be as low as 24, and the BMDL accounts for that uncertainty. The BMDL is the conservative lower fence, not the best guess.

*Validated in the 2026-05-26 Dose-Response Terminology Ladder session (TempMoon stuck on BMDL concept — this analogy was the breakthrough).*

### MCQ Example

A chronic rat bioassay yields BMD₁₀ = 12 mg/kg, BMDL₁₀ = 4 mg/kg for hepatocellular adenoma. A parallel 90-day study reported NOAEL = 8 mg/kg for liver weight changes.

**Most correct statement:** The BMDL₁₀ (4 mg/kg) should be used as the point of departure because it accounts for study uncertainty, while the NOAEL of 8 mg/kg is an artifact of dose spacing and should be discarded (if sufficient data exist for BMD modeling).

**Distractor rationale:**
- *NOAEL preferred because 90-day has better statistical power for liver effects:* Targets the assumption that NOAEL is robust. Reasoning error: BMD uses ALL dose data, not just one dose level. The 90-day study's NOAEL may be no better than the 4 mg/kg BMDL — and the BMDL has a built-in uncertainty bound.
- *BMD₁₀ (12 mg/kg) preferred because it's the best estimate:* Targets confusion between "point estimate" and "conservative POD." Reasoning error: EPA guidance uses the BMDL (lower bound), not the BMD (point estimate), when deriving the point of departure. The 12 mg/kg BMD is the best estimate of the true BMD₁₀, but regulatory risk assessment uses the lower bound to account for uncertainty.
- *Average the two values:* Targets false synthesis. Reasoning error: These are from different studies, different durations, different endpoints. Averaging them has no scientific or regulatory basis.

---

## Rung 3 — Uncertainty Factors (UFs) + Modifying Factors (MFs)

### Definitions

**Uncertainty Factors (UFs):** Numerical adjustments applied to the POD (NOAEL or BMDL) to account for specific gaps or uncertainties in the data. Each UF defaults to 10× and is reduced when chemical-specific data justify a lower value.

Standard UF framework (from NRC Red Book, EPA, and international guidance):

| Factor | Symbol | Default | Purpose |
|---|---|---|---|
| Interspecies (animal → human) | UFA | 10 | Accounts for TK/TD differences |
| Intraspecies (human variability) | UFH | 10 | Accounts for sensitive subpopulations |
| Subchronic → chronic | UFS | 10 | Extrapolating study duration |
| LOAEL → NOAEL | UFL | 10 | When only LOAEL is available |
| Database deficiency | UFD | ≤10 | Incomplete toxicological database |

**Modifying Factor (MF):** An additional professional judgment factor (≤10) applied when no UF captures a specific uncertainty. Used rarely in modern practice — EPA has moved to chemical-specific adjustment factors (CSAFs) instead.

### When 10× Is Not 10×

A UF defaults to 10× unless chemical-specific data allow **data-derived extrapolation factors (DDEFs)** or **chemical-specific adjustment factors (CSAFs)** . For example:

- **UFA (10×) splits into 10^(0.6) ≈ 4× TK + 10^(0.4) ≈ 2.5× TD.** If the chemical has PBPK data allowing TK cross-species scaling, the TK component can be replaced with a measured value, reducing the default 10× to as low as 2-3×.
- **UFH (10×) splits into 10^(0.5) ≈ 3.16× TK + 10^(0.5) ≈ 3.16× TD.** Human data (pharmacokinetic studies in sensitive groups) can reduce or replace components.
- **UFL** is applied only when the POD is a LOAEL instead of NOAEL. If BMDL is used, this factor drops out entirely (BMD addresses the LOAEL-to-NOAEL gap through modeling).
- **MF** is rarely used by EPA today. EFSA does not use MFs at all.

### Classic Confusions

1. **"10× UFs are additive."** They are multiplicative: RfD = POD / (UFA × UFH × UFS × UFL × UFD). Default total UF = 100 (for animal subchronic → human) or up to 10,000 when all factors apply.
2. **"UFs are always 10."** The 10 is a default. Chemical-specific data can reduce each factor. Presence of human data eliminates UFA entirely.
3. **"The total UF says something about the chemical's potency."** Total UF reflects *data quality and uncertainty*, not inherent toxicity. A NOAEL from a high-quality chronic human study needs UF = 10 (UFH only). A LOAEL from a subchronic rat study with minimal database needs UF = 10,000 (UFA + UFH + UFS + UFL + UFD = 10^4).
4. **"LOAEL-to-NOAEL UF and BMDL are redundant."** When BMDL is used as the POD, UFL is NOT applied — the BMD modeling already extrapolates from the study's observable effects to a lower dose. This is a common exam trap: applying UFL when BMDL is the POD is double-counting.

---

## Rung 4 — RfD / RfC

### Definitions

- **RfD (Reference Dose):** An estimate (with uncertainty spanning perhaps an order of magnitude) of a daily oral exposure to the human population (including sensitive subgroups) that is likely to be without an appreciable risk of deleterious effects during a lifetime.
- **RfC (Reference Concentration):** Same concept, but for inhalation exposure — a concentration in air (not a dose).

### Derivation

RfD = POD / (UFA × UFH × UFS × UFL × UFD)

where POD is the NOAEL or BMDL from the critical study (the study showing the most sensitive adverse effect).

**Units:** RfD = mg/kg/day; RfC = mg/m³

### Relationship to Earlier Rungs

```
Study data → POD (NOAEL or BMDL) → UFs applied → RfD
```

The RfD is the *regulatory product* — the number a risk manager uses. It's the end of the non-cancer line.

### Classic Confusions

1. **"RfD is a threshold."** It's not — it's a *regulatory benchmark* incorporating UFs. The true biological threshold (if it exists) could be higher or lower than the RfD. The RfD is designed to be protective, not predictive.
2. **"If exposure < RfD, zero risk."** Below the RfD, risk is *negligible and acceptable* — not zero. The RfD includes UFs to account for uncertainty.
3. **"RfD replaces NOAEL."** No — the RfD is derived FROM the NOAEL or BMDL by dividing by UFs. Different concept entirely.
4. **"RfD applies to cancer."** No — RfD/RfC are for non-cancer threshold effects. Cancer risk is handled through slope factors and linear extrapolation (Rung 5-6).

---

## Rung 5 — Linear vs Nonlinear Low-Dose Extrapolation

### The Fork

This is the fundamental fork in risk assessment:

| | Nonlinear (Threshold) | Linear (Non-Threshold) |
|---|---|---|
| Applies to | Non-cancer endpoints | Cancer (unless MOA shows threshold) |
| Low-dose shape | No effect below threshold | Effect at any dose > 0 |
| POD use | Divide by UFs → RfD | Extrapolate to low dose → slope factor |
| Supporting evidence | Threshold MOA (e.g., cytotoxicity, receptor-mediated) | DNA reactivity, no observed threshold |

### When Linear Applies

EPA's 2005 Cancer Guidelines use a **weight-of-evidence** approach:

- **Mutagenic mode of action (MOA):** Default to linear extrapolation. DNA-reactive carcinogens are assumed to have no threshold.
- **Non-mutagenic MOA:** May use nonlinear (threshold) approach if the MOA supports it (e.g., cytotoxicity → regenerative hyperplasia → tumor, with a clear threshold).
- **Unknown MOA:** Default to linear — conservative assumption.

### The Shape Matters

A chemical with a *steep* dose-response curve has a similar RfD as one with a *shallow* curve (both get the same UFs from the same POD). But the cancer risk at sub-regulatory doses depends entirely on the slope of the linear extrapolation — this is where cancer slope factor and unit risk come in (Rung 6).

### Classic Confusions

1. **"All carcinogens use linear extrapolation."** EPA's 2005 guidelines explicitly allow nonlinear approaches for non-mutagenic MOA. Phenobarbital and certain hormones are carcinogenic with clear thresholds.
2. **"Linear means the dose-response is a straight line."** The term "linear" in this context refers to the *low-dose* region — the model assumes proportionality between dose and response at doses below the observable range. The full curve is typically sigmoidal.
3. **"RfD for carcinogens = acceptable risk."** For linear carcinogens, there is no RfD. Instead, risk is estimated as a probability (e.g., 10⁻⁵ excess lifetime risk).

---

## Rung 6 — Cancer Slope Factor (CSF) vs Unit Risk

### Definitions

- **CSF (Cancer Slope Factor):** The slope of the dose-response curve in the low-dose (linear) region. Upper-bound estimate of excess cancer risk per unit dose. Units: (mg/kg/day)⁻¹
- **Unit Risk:** The same concept but expressed as risk per unit *concentration* (usually μg/m³ for inhalation or μg/L for drinking water). Derived by applying the CSF to standard exposure assumptions.

### Derivation

From the linear portion of the dose-response model (usually the 95% upper bound on the slope, not the central estimate):

CSF = risk per (mg/kg/day)

Cancer risk = exposure dose × CSF

Example: CSF = 0.1 (mg/kg/day)⁻¹, exposure = 0.01 mg/kg/day → estimated excess lifetime cancer risk = 0.001 = 10⁻³

### Relationship to RfD/C

A single chemical can have BOTH an RfD (for non-cancer effects) and a CSF (for cancer effects). The more sensitive endpoint drives the regulatory limit.

### Classic Confusions

1. **"CSF is the slope of the full curve."** No — it's the slope in the *low-dose linear region*, which is the upper-bound estimate. The true slope at higher doses may be steeper or shallower.
2. **"CSF gives the actual risk."** No — it's an *upper bound* (95th percentile on the slope). The true risk could be much lower (including zero). CSF is intentionally conservative.
3. **"Unit risk = CSF in different units."** Yes — unit risk is the CSF translated to ambient concentration units using default exposure assumptions (20 m³ inhaled/day, 70 kg body weight, etc.).
4. **"Asbestos → lung cancer → high CSF → must be very potent."** CSF reflects the low-dose extrapolation, not the overall potency. A chemical with a shallow dose-response but well-characterized at high doses may have a similar CSF to one that's poorly characterized with a steep slope.

---

## Rung 7 — Margin of Exposure (MOE)

### Definition

MOE = POD / Estimated Human Exposure

Where POD is the NOAEL or BMDL. MOE is dimensionless — a ratio, not a risk probability.

### Interpretation

- Larger MOE = safer (more distance between the effect level and actual exposure)
- No universal "acceptable" MOE — depends on data quality:
  - Chronic human data at realistic doses → MOE of 10-100 may be adequate
  - Subchronic animal data → MOE of 500-5000 may be needed
  - LOAEL-based POD → MOE of 100-10000

### Relationship to Hazard Index (HI)

- **MOE:** Used for individual chemicals. A ratio of effect level to exposure.
- **HI (Hazard Index):** Sum of HQs across chemicals affecting the same target organ.
- **HQ (Hazard Quotient):** Exposure / RfD. HQ < 1 = acceptable; HQ > 1 = potential concern.

### Where MOE Is Used

- **FDA:** Food contaminants, packaging migrants — where an ADI cannot be established because data are insufficient or the chemical is an unavoidable contaminant
- **EFSA:** Genotoxic carcinogens — where no threshold exists, MOE replaces HQ
- **WHO JECFA:** Food contaminants — compare MOE to a "reference MOE" (typically 10,000 for genotoxic carcinogens using a BMDL₁₀ from animal data)

### Classic Confusions

1. **"MOE < 1 = unacceptable."** MOE is a ratio of POD to exposure. A MOE of 1 means the exposure equals the POD (e.g., BMDL₁₀). That doesn't mean "risk is certain" — the POD already includes a 10% extra risk, and UFs haven't been applied. MOE is a *distance metric*, not a binary threshold.
2. **"MOE is calculated with the RfD."** No — MOE uses the POD (NOAEL or BMDL), NOT the RfD. The RfD already includes UFs. Using the RfD would double-count protection.
3. **"Large MOE = no toxicity."** MOE says nothing about toxicity — it says how far the exposure is from a toxic effect level. A chemical with a high NOAEL and low exposure produces the same large MOE whether it's mildly toxic or extremely toxic.
4. **"MOE and HQ are interchangeable."** Different formulas: MOE = POD / exposure; HQ = exposure / RfD. They're inverses with the RfD replacing the POD.

---

## Summary Table

| Term | Definition | Units | When Used |
|---|---|---|---|
| **NOAEL** | Highest dose with no *adverse* effect | mg/kg/day | POD for non-cancer RfD derivation |
| **LOAEL** | Lowest dose with an *adverse* effect | mg/kg/day | When no NOAEL is identified |
| **BMD** | Dose producing a specified BMR from modeled data | mg/kg/day | Preferred POD (vs NOAEL) when data support |
| **BMDL** | 95% lower bound on BMD | mg/kg/day | Regulatory POD (more conservative than BMD) |
| **BMR** | Pre-specified effect level (default 10%) | unitless | Defines the response level for BMD |
| **UF** | Multiplicative factor applied to POD for uncertainty | unitless (10ⁿ) | Adjusting POD → RfD |
| **RfD** | Daily oral dose likely without appreciable risk | mg/kg/day | Non-cancer regulatory limit |
| **RfC** | Inhalation concentration likely without risk | mg/m³ | Non-cancer inhalation limit |
| **CSF** | Upper-bound excess cancer risk per unit dose | (mg/kg/day)⁻¹ | Cancer risk calculation |
| **Unit Risk** | Risk per unit concentration | (μg/m³)⁻¹ or (μg/L)⁻¹ | Ambient exposure cancer risk |
| **MOE** | Ratio of POD to actual exposure | dimensionless | Margin-of-safety indicator |
| **HQ** | Ratio of exposure to RfD | dimensionless | Single-chemical risk characterization |
| **HI** | Sum of HQs across chemicals | dimensionless | Mixture/cumulative risk |

---

## Prep Flashcards (48 cards loaded to Memento under "DABT - Risk Assessment")

A full **48-card deck** is loaded in Memento covering every term in this ladder (NOAEL, LOAEL, BMD, BMDL, BMR, POD, UFₐ/UFₕ/UFₛ/UF_L, MF, CSAF, RfD, RfC, ADI, linear vs nonlinear, CSF, Unit Risk, MOE, HQ, HI). Review via `review` command in flashcard channel.

### Quick-start sample (5 cards for Memento)

**Card 1 — NOAEL vs LOAEL**
Q: A 90-day study with doses 0, 5, 25, 100 mg/kg shows body weight ↓ 12% at 100 (p<0.01) with correlating organ weight changes, but body weight ↓ 6% at 25 (p<0.05) with no correlating pathology. What is the NOAEL/LOAEL?
A: NOAEL = 25 mg/kg (non-adverse change only). LOAEL = 100 mg/kg (adverse change). "Significant but not adverse" is the key distinction — the body weight decrease at 25 is biologically adaptive, not toxicologically adverse.

**Card 2 — BMDL Interpretation**
Q: A study reports BMD₁₀ = 45 mg/kg, BMDL₁₀ = 12 mg/kg for kidney toxicity. Which POD should be used for risk assessment, and why?
A: BMDL₁₀ (12 mg/kg). The BMDL incorporates study uncertainty (95% lower bound on the dose producing a 10% response). Regulatory risk assessment uses the lower bound for conservatism. Using the BMD (45 mg/kg) would ignore the uncertainty reflected in the confidence interval width.

**Card 3 — UF Application**
Q: You have a subchronic NOAEL from a rat study. NOAEL = 10 mg/kg. What UFs apply to derive an RfD, and what is the total UF?
A: UFA (10×, rat→human) + UFH (10×, human variability) + UFS (10×, subchronic→chronic) = total 10³ = 1000. UFL does NOT apply (NOAEL is available, not LOAEL). UFD does NOT apply unless database is deficient. Total UF = 1000; RfD = 10/1000 = 0.01 mg/kg/day.

**Card 4 — Linear vs Nonlinear Fork**
Q: A new chemical is identified as a DNA-reactive carcinogen in animal studies. What low-dose extrapolation approach is appropriate?
A: Linear (non-threshold). EPA's 2005 Cancer Guidelines default to linear low-dose extrapolation for mutagenic MOA carcinogens because there is no evidence of a threshold for DNA-reactive agents. Nonlinear (threshold) would only be appropriate if the MOA were non-mutagenic (e.g., cytotoxicity-based) with demonstrable threshold.

**Card 5 — MOE Application**
Q: A food contaminant has a BMDL₁₀ of 0.5 mg/kg/day from a chronic rat carcinogenicity study. Estimated human dietary exposure is 0.0001 mg/kg/day. Calculate the MOE. Is this MOE likely adequate?
A: MOE = 0.5 / 0.0001 = 5,000. For a genotoxic carcinogen with a BMDL₁₀ from chronic animal data, an MOE of 10,000 is EFSA's default benchmark for "low concern." An MOE of 5,000 is below that benchmark and would likely trigger risk management actions. For a non-cancer endpoint, an MOE of 100-500 might suffice. Context matters: this is a carcinogen MOE, so 5,000 is borderline.
