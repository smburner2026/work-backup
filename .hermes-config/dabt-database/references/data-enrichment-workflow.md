# Data Enrichment Workflow — Bloom Levels & Explanations

## Purpose

Systematically enrich the DABT question database with:
- **Bloom levels** (cognitive classification: Remember/Understand, Apply, Analyze)
- **Explanations** (mechanism + trap + citation for each question)

All 4,841 questions are now bloom-classified. Explanations are in progress — Domain III complete, others pending.

## Bloom Level Classification

### Criteria

| Level | Definition | Typical Question Patterns |
|-------|-----------|-------------------------|
| **remember-understand** | Recall facts, definitions, or recognize correct statements | "What is", "Define", "Which of the following is a/the", "Refers to", "Is characterized by", "Is called" — single-sentence, direct recall |
| **apply** | Apply concepts to novel scenarios, calculate, interpret data | Numerical values (dose, LD50, mg/kg), regulatory scenarios, study design choices, "If...then", "What would happen", "Determine", case vignettes |
| **analyze** | Compare, differentiate, integrate multiple concepts, weight of evidence | "Which statement is correct/true/false", "Compare/contrast", "Most accurately describes", "Mechanism of action", "Why does", "Primary reason", Evaluates multiple options against each other |

### Batch Processing Protocol

1. Query questions by domain, ordered by ID (which preserves chapter clustering for 2000Q Bank)
2. Apply pattern-matching heuristic based on question text and answer options
3. Commit classifications to DB via `UPDATE questions SET bloom_level = ? WHERE id = ?`
4. Verify distribution — each domain should show roughly: 40-55% Remember, 30-40% Apply, 5-15% Analyze

### Heuristic Logic (Python)

```python
import re

def classify_bloom(question_text):
    t = question_text.strip().lower()
    
    # Analyze indicators — evaluative, comparative, mechanistic
    if re.search(r'(which of the following .* (correct|true|false|incorrect|most appropriate)'
                 r'|best (describes|explains|characterizes)'
                 r'|compare|contrast|difference between|distinguish'
                 r'|mechanism|mode of action|why (does|would)|accounts for'
                 r'|primary (reason|cause|factor)|most (likely|important)'
                 r'|integrat|synthesize|weight of evidence)', t):
        return "analyze"
    
    # Apply indicators — calculation, scenario, procedure
    if re.search(r'(calculat|dose|mg/kg|ppm|therapeutic index|ld50|ed50|lc50|noael|loael|bmd'
                 r'|if .* then|what (would|will) |how (would|should) |determine '
                 r'|treatment|therapy|antidote|chelator'
                 r'|exposure|biomarker|biomonitor'
                 r'|regulat|guideline|standard|limit|oel|pel|twa|tlv'
                 r'|in (vivo|vitro|silico)|study (design|type) )', t):
        return "apply"
    
    # Remember indicators — definition, fact, identification
    if re.search(r'(what is|define|refers to|is called|characterized by|the term|definition'
                 r'|identify |list |one of the|the most common|is associated with|is known as)'
                 r'', t):
        return "remember-understand"
    
    # Fallback: depth heuristic
    sentences = len([s for s in t.split('.') if len(s.strip()) > 20])
    return "remember-understand" if (sentences <= 1 and len(t) < 150) else "apply"
```

### Priority Order

Process domains by exam weight (highest first):
1. Domain III (Risk Assessment) — 38% exam weight, 210 Qs ← DONE
2. Domain I (Conduct of Studies) — 36% exam weight, 981 Qs ← DONE
3. Domain II (Mechanistic) — 13% exam weight, 673 Qs ← DONE
4. Domain IV (Applied) — 13% exam weight, 2,850 Qs ← DONE

## Explanation Writing

### Format

Each explanation follows this structure:

```
[Mechanism/Concept statement of 1-3 sentences explaining WHY the correct answer is right].
[If applicable: Trap — explains why the most common wrong answer is tempting but wrong].
[Source: Reference citation]
```

### Examples

**Definition question** (DABT-0064):
> "Alpha particles are the least penetrating form of ionizing radiation — they are stopped by a sheet of paper or the outer layer of skin. Beta particles penetrate deeper (few mm), and x-rays/gamma rays penetrate deepest. The high mass and charge of alpha particles causes dense ionization along a short path. [Source: Casarett Ch.25, Radiation]"

**Calculation question** (DABT-0052):
> "Therapeutic Index = TD50 ÷ ED50 = 200 ÷ 25 = 8. TI > 10 is generally considered a good safety margin. TI < 3 indicates a narrow therapeutic window requiring therapeutic drug monitoring. [Source: Casarett Ch.2, Principles]"

**Mechanism question** (DABT-0103):
> "TCDD binds the Ah receptor, which is highly expressed in thymic epithelium, leading to thymic atrophy and impaired T-cell maturation — a direct effect on thymic stroma rather than on T- or B-cells directly. Thymic epithelial damage disrupts the microenvironment needed for T-cell development. [Source: Casarett Ch.12, Immune System]"

**Evaluative question** (DABT-3715):
> "The NOAEL approach has several limitations: (1) it depends on dose selection and spacing, (2) it uses a single dose group rather than the full dose-response curve, (3) it does not account for the slope or shape of the dose-response relationship, (4) it is constrained by sample size, and (5) it can only be one of the tested doses. The Benchmark Dose (BMD) approach addresses all of these. [Source: Casarett Ch.4; EPA BMD Guidance]"

### Ground Truth Sources

Before writing an explanation, verify the correct answer and mechanism against the reference texts:

1. **First pass**: Search `dabt-reference` (three-pass search across extracted/ sources)
2. **Priority sources**: Casarett & Doull 9e (chapters by topic), Hayes 7e (methodology), EPA guidelines (risk assessment), ICH guidelines (regulatory)
3. **Handbook check**: Verify the question maps to a handbook task/knowledge statement at `extracted/abt-handbook/exam-content-outline.txt`
4. **Fallback**: If the topic isn't in extracted references, use the ABT sample questions or known regulatory values

### Priority Order

Same as bloom levels — process by exam weight, highest first:
1. Domain III (Risk Assessment, 38%) — 54/54 DONE
2. Domain I (Conduct of Studies, 36%) — 54/388 in progress
3. Domain II (Mechanistic, 13%) — 1/244
4. Domain IV (Applied, 13%) — 5/1,375

### Known Gaps

- 1,246 questions are missing the correct_answer_letter entirely — explanations cannot be written until answers are recovered from source files
- 1,947 questions with known answers still need explanations (as of 2026-05-20)
- Questions from 2000Q Bank cluster by chapter (same ID range ≈ same topic) — batch by ID range for efficiency
- Mini-ABT 1-11 questions (IDs DABT-0001 to DABT-0446) are well-structured with clean answers — these are the lowest-hanging fruit
