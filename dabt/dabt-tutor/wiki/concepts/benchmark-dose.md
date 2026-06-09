# Benchmark Dose (BMD)

## Definition
The Benchmark Dose (BMD) is a statistically derived point of departure (POD) that corresponds to a predetermined benchmark response (BMR), typically defined as an extra risk of 1%, 5%, or 10% over background. The BMD is obtained by fitting a dose‑response model to observed data and calculating the dose that produces the chosen BMR.

## Key Concepts
- **Benchmark Response (BMR)**: The extra risk level selected *before* modeling (e.g., 10% extra risk). Extra risk = (Incidence_at_dose – Background) / (1 – Background).
- **BMDL**: The 95% lower confidence limit on the BMD. EPA typically uses the BMDL as the POD because it provides a conservative estimate: we are 95% confident that the true BMD is not lower than the BMDL.
- **Modeling Process** (performed by EPA’s Benchmark Dose Software, BMDS):
  1. Fit several candidate models (logistic, Weibull, multistage, Hill, etc.) to incidence‑vs‑dose data.
  2. Select models with adequate fit (goodness‑of‑fit p‑value > 0.1 or similar).
  3. For each acceptable model, compute the dose that yields the chosen BMR → BMD for that model.
  4. If multiple models pass, report a model‑averaged BMD or the BMD from the best‑fitting model.
- **Uncertainty Factors (UFs)**:
  - When a BMDL is used as the POD, the **LOAEL‑to‑NOAEL UF** (often 10) is typically omitted because the BMDL already functions like a NOAEL derived from modeling.
  - The standard UFs for **inter‑species differences** (animal → human) and **intra‑species variability** (human variability) are still applied because the BMDL only accounts for statistical uncertainty in the animal data, not for species or human differences.

## Exam Relevance
- Domain III – Risk Assessment (38%) → Sub‑domain C – Dose‑Response Assessment (9%).
- Expect ~1–3 scored questions on the 140‑question exam.
- Common distractors:
  - Confusing BMD with BMDL.
  - Mis‑interpreting BMR as a simple percentage increase over background without adjusting for background incidence.
  - Assuming the BMDL eliminates all uncertainty factors.
  - Believing a specific model (e.g., logistic) is always used.
  - Mixing up cancer vs. non‑cancer BMR defaults.

## References
- U.S. EPA. Benchmark Dose Technical Guidance Document (EPA/100/R-12/001, 2012a).
- Casarett & Doull’s Essentials of Toxicology, Chapter 4 (Risk Assessment).
- Hayes’ Principles and Methods of Toxicology, Chapter 2 (Use of Toxicology in the Regulatory Process).