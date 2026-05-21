# DABT Tutor — Task Roadmap

Generated from the 2026-05-20 architecture audit session. Updated 2026-05-20.

## The Six Tasks

### Task 1 — Synthetic Questions
**Goal:** Build exam-quality MCQs for domains the DB underrepresents.
**Priority domains:** Domain III (Risk Assessment, 38% exam, 210 Qs), Domain I (Conduct of Studies, 36% exam, 981 Qs — still -15.7% underweight).
**Requirements:**
- Must match 2026 DABT exam style (vignette-based, applied, Bloom-level diverse)
- Factually grounded in Casarett, Hayes, EPA guidelines, ICH guidelines
- Validated against the handbook's 48 task statements and 138 knowledge topics
- Distractors must be plausible but wrong — avoid straw-man options
- Each synthetic question must carry: explanation, bloom level, domain/sub-domain/task assignment, source citation
**Risk:** Wrong questions teach wrong patterns. Requires careful distractor design and ideally a subject-matter expert review pass.

### Task 2 — Supplementary Materials
**Decision:** LEAVE AS-IS. Mid-Amer Tox course summaries, C&D chapter support slides, lecture notes, and similar secondary materials are not ingested into the search pipeline. Rationale: noise risk outweighs value for a well-read candidate.

### Task 3 — Explanations + Bloom Levels

**Sub-task 3a — Explanations (scope: ~3,400 questions)**
- 4,841 questions in DB; only ~1,454 (30%) have explanations
- Each explanation should: state the correct mechanism/regulatory basis, name the trap (if one exists), cite the source reference
- Use `dabt-reference` three-pass search to find source material for each explanation. Alternatively, use the batch explanation pipeline documented at `dabt-database` → `references/batch-explanation-workflow.md`
- Prioritize: Domain III first (fewest questions, highest exam weight), then Domain I, then II/IV

**Progress:**
| Batch | Questions | Status |
|-------|----------|--------|
| batch1 | TBD | Pending |
| batch2 | TBD | Pending |
| batch3 | 50 | ✅ Done (2026-05-20) |

**Sub-task 3b — Bloom Levels (scope: all 4,841 questions)**
- 0% of questions have bloom levels populated
- Classify each as Remember/Understand, Apply, or Analyze
- Apply: questions requiring interpretation of data, calculation, or application of a concept to a new scenario
- Analyze: questions requiring differentiation of multiple factors, integration across domains, or evaluation of conflicting evidence

### Task 4 — Curriculum Topics
**What exists:** `curriculum/topics.json` with 5 entries (domain-i-conduct, domain-ii-mechanistic, domain-iii-risk-assessment, domain-iv-applied, organ-systems). Each has sub-structure, topics, and prerequisites.
**Status:** Material exists but is unconsumed. Needs user discussion to decide fate.

### Task 5 — Unified Project Config ✅ COMPLETE
**Goal:** One machine-readable config file (`dabt-config.json`) at `/root/work/dabt/dabt-tutor/` that all skills read at session start.
**Status:** MATERIALIZED as of 2026-05-20 (version 1.0.0). 13 sections covering exam blueprint, database, reference library, drill config, learner profile, task tracking. All 6 DABT skills patched to read from config. Old `exam-weights.json` deleted. `dabt-project-workflow` skill updated to declare config alive.
**Orchestrator:** `education/dabt-project-workflow` is the canonical entry point. Every DABT session starts here.

### Task 6 — Digest Past Exam Materials
**What exists but is not in the DB:**
- 2013 Recert exam — PDF + multiple PPTX answer files (~6 files, ~1.5 MB)
- 2015 Recert exam — PDF + multiple PPTX answer files (~12 files, ~2.5 MB)
- 2017 Certification exam — 4-part PDF (~750 KB total)
- Mini-ABT 1-11 — 22 docx files with full exams + answer keys (partially in DB via legacy xlsx)
- Tox 2000 NoteCards PDF
**What to do:**
- Extract question text from the PDFs/PPTX
- Cross-check against existing DB questions for dedup
- Add new questions to the DB with full explanations and domain assignments
- Add unique content (vignettes, regulatory scenarios) to the reference pipeline

## Sequencing

```
Phase 0: Task 5 — Unified Project Config ✅ COMPLETE
Phase 1: Task 3 — Explanations + Bloom Levels (batch3 ✅)
         Task 6 — Digest Past Exams
Phase 2: Task 1 — Synthetic Questions
Phase 3: Task 4 — Curriculum Topics decision
```

## Notes
- Exam date: **October 15, 2026**
- Domain III (Risk Assessment) is the single highest-leverage target — 38% of the exam, least material available
- Task 2 (Supplementary Materials) is explicitly deferred per user decision
