# Root Cause Assessment: Why the 2026 ABT Handbook Wasn't Being Used

## Discovery

The handbook PDF existed at `reference/exam-materials/ABT-Candidate-Handbook-2026.pdf`
since the project directory was created. It was never consulted by the Mike persona's
skills for study planning, drill weighting, or topic prioritization.

## Three Convergent Failures

### 1. Wrong Path in AGENTS.md

AGENTS.md line 44 referenced:
```
reference/ABT-Candidate-Handbook-2026.pdf
```
The file is actually at:
```
reference/exam-materials/ABT-Candidate-Handbook-2026.pdf
```

Any agent that reads AGENTS.md (the project's own configuration file) would try the
wrong path and silently get nothing. There was no "file not found" guard — the path
just didn't resolve. **[Fixed: corrected path in AGENTS.md]**

### 2. Skills Self-Contained, Not Project-Aware

The Hermes skills (`dabt-reference`, `dabt-deep-dive`, `dabt-drill-mode`,
`dabt-database`) are self-contained SKILL.md files that define their own procedures
independently. None of them consult AGENTS.md or the project directory for
configuration. They hardcode database paths, reference search paths, and weight
distributions internally. This makes them portable but also means they never
"discover" new files added to the project directory unless explicitly patched.

The `dabt-reference` skill's search pipeline only covered files under `extracted/`
(Casarett & Doull, Hayes, regulations). The handbook was in `exam-materials/` —
outside the search scope entirely. **[Fixed: handbook extracted to extracted/abt-handbook/,
dabt-reference patched to include it, exam-weights.json created as shared config]**

### 3. Domain Weights Were Guessed, Not Authoritative

The MASTER_INDEX.md at `/root/dabt-curated/MASTER_INDEX.md` said Risk Assessment was
~26% of the exam. The actual handbook p.24 says 38%. The blueprint reference within
`dabt-drill-mode` said "percentages based on task distribution from the Practice
Analysis, not ABT-published exam weights." This meant the entire study pipeline was
calibrated to approximate weights, never anchored to the authoritative source.

The AGENTS.md actually had the correct weights (Domain III = 38%) — someone updated
it at some point — but the skills never read AGENTS.md. **[Fixed: exam-weights.json
created as the canonical shared config; skills now reference it directly]**

## Why This Matters

The cost of these three failures compounding:

| Metric | Before Fix | After Fix |
|--------|-----------|----------|
| Domain III questions per 10-drill | ~2 (underweight) | 4 (exam-correct) |
| Domain I questions per 10-drill | ~2 (underweight) | 3-4 (exam-correct) |
| Domain IV questions per 10-drill | ~5 (overweight, by DB) | 0-1 (exam-correct) |
| Handbook lookup by reference skill | Not possible | Full text searchable |
| Study plan generation basis | DB availability | Exam weight config |

## Structural Lesson

The project directory (workdir) contains configuration — AGENTS.md, exam-weights.json,
progress/state.json — that should govern skill behaviour. Skills should read from the
workdir at runtime, not embed all assumptions in their SKILL.md definition. Future
patches should add a "consult AGENTS.md" step to the session start procedure of all
DABT skills so new project-level config changes propagate automatically.

## What Was Changed

| File | Change |
|------|--------|
| `AGENTS.md` | Handbook path corrected |
| `reference/exam-weights.json` | **NEW** — canonical exam weight config |
| `reference/extracted/abt-handbook/` | **NEW** — full handbook + outline extraction |
| `dabt-reference` skill | Handbook added to search pipeline, source abbreviations, reference library docs |
| `dabt-deep-dive` skill | Exam-weight pre-flight check, topic priority by exam % |
| `dabt-drill-mode` skill | Weight gap table, corrected drill targeting, Domain III conservation rules |
| `dabt-database` skill | `sample_by_exam_weight()` function, exam-weight config integration |
