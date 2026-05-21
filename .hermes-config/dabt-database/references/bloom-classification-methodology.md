# Bloom Level Classification — Methodology (2026-05-20)

## Source

All 4,841 questions in the SQLite database (`reference/data/dabt.db`), classified into the
cognitive demand levels used by the ABT exam blueprint. Unlike the domain classification
(which uses a topic-to-domain lookup table), bloom levels were assigned by analyzing
question text + answer structure + option complexity.

## Three Classification Tiers

### Remember/Understand
Recall facts, definitions, or recognize correct statements. One-step retrieval from memory.

**Indicators:**
- Opens with "What is", "Define", "The term", "Refers to", "Is called", "Is characterized by"
- "Which of the following is a/an/the" (simple fact, not evaluative)
- "Identify the", "List the"
- Single sentence, <150 characters, one correct answer among obvious distractors
- Direct definition: "Incidence rate is _____"
- Chemical-to-class matching: "Rotenone is what type of pesticide?"

### Apply
Apply concepts to novel scenarios, calculate, interpret data, determine outcomes. Multi-step.

**Indicators:**
- Contains numbers or calculations: "mg/kg", "LD50", "therapeutic index", "half-life", "ppm"
- Scenario framing: "If...then", "What would happen", "How would you", "Determine whether"
- Procedural: "In a primary skin irritation test performed according to FIFRA guidelines"
- Regulatory application: "Under this law an additional uncertainty factor of 10x is added"
- Data interpretation: "Two of the more common approaches for estimating the threshold..."
- Clinical vignette: "A farmer came into the emergency department complaining of..."
- Multiple sentences (3+ lines) with step-by-step reasoning required

### Analyze
Compare, differentiate, integrate multiple concepts, weight of evidence, evaluate conflicting information.

**Indicators:**
- Evaluative: "Which of the following statements is CORRECT/TRUE/FALSE/INCORRECT"
- "Best describes", "Best explains", "Most accurately"
- Compare/contrast: "Difference between", "Distinguish"
- Mechanism reasoning: "Why does", "Accounts for", "Can be explained by"
- Integrative: "Weight of evidence", "Primary reason", "Most important factor"
- Multi-statement items: "A. ..., B. ..., C. ..., D. ..." (evaluate each independently)

## Classification Algorithm (per question)

### Step 1 — Analyze Check (highest priority)
- Tests for evaluative, comparative, or mechanism-reasoning language
- If True → Analyze

### Step 2 — Apply Check
- Tests for calculation terms, scenario framing, procedural language
- Must not already be classified as Analyze

### Step 3 — Remember Check
- Tests for definitional openings, identification language
- Must not already be classified as Analyze

### Step 4 — Depth Heuristic (fallback)
- If no pattern matched: single sentence <150 chars → Remember
- 3+ sentences or vignette → Apply

### Domain-Specific Adjustments
- Domain I: GLP/OECD/study-design → Apply
- Domain II: "What is the mechanism" → Remember; "Why" or comparing → Analyze
- Domain III: Calculation-heavy → Apply; Evaluative → Analyze
- Domain IV: Clinical vignettes → Apply; Direct fact recall → Remember

## Results (2026-05-20, all 4,841 questions)

| Bloom Level | Count | Pct |
|-------------|-------|-----|
| Remember/Understand | 2,479 | 51% |
| Apply | 1,798 | 37% |
| Analyze | 564 | 12% |

### By Domain

| Domain | Remember | Apply | Analyze | Total |
|--------|----------|-------|---------|-------|
| Domain I (Conduct) | 500 | 399 | 82 | 981 |
| Domain II (Mechanistic) | 360 | 198 | 115 | 673 |
| Domain III (Risk Assessment) | 114 | 69 | 27 | 210 |
| Domain IV (Applied) | 1,416 | 1,107 | 327 | 2,850 |

The distribution shows roughly 50% recall-based, 37% application, 12% analysis —
a reasonable spread for a general toxicology certification exam.

## Limitations

- Pattern-matching is approximate. Multi-statement evaluative questions may require
  only single-fact recall, inflating Analyze count slightly.
- Clinical vignettes ending in simple recall may be over-classified as Apply.
- No per-question human review pass (unlike the batch explanation pipeline).
- Not validated against ABT's actual bloom distribution (ABT does not publish this).

## Use in Study Planning

Bloom levels enable granular diagnostic feedback:
- Miss Apply on Domain III → practice calculation/scenario questions
- Miss Analyze on Domain I → practice comparing protocols/study designs
- Miss Remember on Domain IV → flashcard work on specific toxicants

Config tracks cumulative performance by bloom level in state.json → cumulative.by_bloom.
