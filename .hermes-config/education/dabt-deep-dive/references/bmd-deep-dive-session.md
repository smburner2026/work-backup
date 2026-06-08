# BMD Deep Dive Session Notes (2026-06-08)

## Scope
- Topic: Benchmark Dose (BMD) – statistically derived POD modeling dose-response, calculating lower confidence bound for a specified BMR (1%,5%,10%).
- Location: Domain III‑C (Dose‑Response Assessment), weight ~9% of exam.
- Exam relevance: ~1‑2% of scored items (2‑3 questions).

## Diagnostic Opening
- Asked user to explain BMD in own words, note any prior exposure, and identify confusing aspects.
- No prior deep‑dived artifact for BMD; 20 BMD‑related items in question bank.
- Common learner confounds: mixing BMD with NOAEL/LOAEL, misunderstanding BMR selection, missing which UFs are NOT applied when using BMDL as POD.

## Socratic Build (Outline)
1. **Concrete scenario**: Suppose a study shows 10% incidence of liver lesions at 50 mg/kg/day, 5% at 25 mg/kg/day, 0% at controls. How would you derive a POD?
   - Leads to discussion of modeling curve vs. NOAEL approach.
2. **Define BMD/BMDL**: BMD = dose producing predetermined BMR; BMDL = lower 95% confidence bound.
3. **BMR choice**: 10% for cancer (extra risk), 5% for non‑cancer severe effects, 1% for mild/reversible.
4. **Uncertainty factors**: When BMDL used as POD, default UFs for interspecies and intraspecies still applied; **no** additional UF for LOAEL-to-NOAEL conversion because BMDL already accounts for curve shape.
5. **Advantages over NOAEL**: uses all data, avoids dependence on selected dose spacing, provides confidence interval.
6. **Limitations**: requires adequate data points, model selection bias, software dependency (BMDS).

## Edge Cases / Distractors
- “BMDL already includes UF for LOAEL‑to‑NOAEL” → false; BMDL is a statistical bound, not a NOAEL.
- “BMD can be used only for continuous data” → false; applies to dichotomous, continuous, quantal.
- “If BMDL > NOAEL, choose NOAEL” → context‑dependent; BMDL is often preferred when data support modeling.

## Deliverables (Planned)
- Concept note: `wiki/concepts/benchmark-dose.md`
- Practice Qs: 3‑5 self‑generated flashcards covering BMD definition, BMR selection, UF application, advantage over NOAEL.

## Sources Consulted
- Casarett & Doull 9e, Ch.4 – Risk Assessment (lines 3697‑3760)
- Hayes 7e, Ch.2 – Use of Toxicology in Regulatory Process (lines 2971‑5668)
- EPA BMD Technical Guidance (2012) – extracted regulations/benchmark_dose_2012.txt
- Silver Book (NRC 2009) – referenced in drill_config.domain_iii_conservation