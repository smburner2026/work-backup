# Classification Distribution

Computed from `reference/data/question_classifications.csv` (446 questions).

## Domain Distribution

| Domain | Count | % of Total | Blueprint Target |
|--------|-------|-----------|-----------------|
| Domain I (Conduct of Studies) | 151 | 33.9% | 36% |
| Domain II (Mechanistic) | 66 | 14.8% | 13% |
| Domain III (Risk Assessment) | 38 | 8.5% | 38% |
| Domain IV (Applied) | 191 | 42.8% | 13% |

**Note:** The classification CSV does not perfectly match the ABT blueprint weights. Domain III (RA) is severely underrepresented (8.5% vs 38% target), while Domain IV is overrepresented (42.8% vs 13% target). Domain I is close (33.9% vs 36%). This means blueprint-weighted sampling from the database will deplete the RA pool quickly (~38 questions available total) and lean heavily on Applied questions for the odd slots.

## Sub-Domain Distribution

| Sub-Domain | Count | Domain |
|-----------|-------|--------|
| Applied | 191 | IV |
| C.Interpret | 136 | I |
| Mechanistic | 66 | II |
| D.RiskChar&Mgmt | 38 | III |
| B.Execute | 9 | I |
| A.Design | 6 | I |

Sub-domains A.Design and B.Execute are very small pools — handle with care during targeted sampling.

## Bloom Level Distribution

| Bloom Level | Count |
|-------------|-------|
| Apply | 224 |
| Remember/Understand | 219 |
| Analyze | 3 |

The Analyze pool is tiny (3 questions). Treat Analyze-classified questions as rare events.

## Practical Sampling Guidance

When selecting 5-question mixed sets (2 RA + 2 Conduct + 1 odd):

- **RA pool:** Only 38 questions. After ~15 mixed sets the pool will be depleted. Start rotating odd to RA instead of Mech/Applied once the RA pool drops below ~15.
- **Conduct pool:** 151 questions, comfortable. C.Interpret (136) dominates within-Conduct — if sub-domain diversification is desired, explicitly filter for A.Design and B.Execute.
- **Mech pool:** 66 questions. Manageable but finite.
- **Applied pool:** 191 questions. Most abundant. Use for odd slot rotation when preserving Mech and RA pools.
