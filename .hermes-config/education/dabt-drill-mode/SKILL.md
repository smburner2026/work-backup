---
name: dabt-drill-mode
description: "DABT certification exam drill mode — blueprint-weighted question sets across Kristen Mini Exams, 2000Q bank, Chapter Tests, and Past ABT Exams (5,000+ questions total). Per-question feedback with gap tagging, confidence calibration, and persistent state tracking. Updated May 2026: sources expanded, Mini-ABT 1-11 deprecated (duplicates of Kristen), 4-domain blueprint aligned with 2022 Practice Analysis. For Abud's 2026 DABT prep."
category: education
---

# DABT Drill Mode

## Trigger

Load this skill when Abud says "drill mode", "quiz me", "questions", "practice", "exam sim", "diagnostic", or starts a session in the DABT tutor project without specifying deep-dive. Also load `dabt-database` skill and `dabt-reference` skill alongside this one.

**Session start:** Load `education/dabt-project-workflow` first — it reads the unified project config (`dabt-config.json`) and establishes all paths and weights this skill relies on.

## Question Sources (Updated May 2026)

The question collection has been significantly expanded and reorganized. Source materials are at `/root/dabt-curated/`.

**⚠️ CRITICAL — Database-to-Exam Weight Gap:** The database is structurally biased by source availability, not exam weight. Before every drill session, read `/root/work/dabt/dabt-tutor/dabt-config.json` → `exam_blueprint.domains` for the authoritative weights. Key gaps:

| Domain | Exam Weight | DB Questions | DB % | Gap |
|--------|------------|-------------|------|------|
| III. Risk Assessment | **38%** | 210 | 4.3% | **−33.7%** |
| I. Conduct of Studies | **36%** | 981 | 20.3% | **−15.7%** |
| II. Mechanistic | 13% | 673 | 13.9% | +0.9% ✅ |
| IV. Applied | 13% | 2,850 | 58.9% | **+45.9%** |

Domain III has only 210 questions for 38% of the exam. Use them sparingly — they're your most valuable practice asset. When Domain III questions are depleted (config threshold: `drill_config.domain_iii_conservation.warning_threshold` = 50 unseen remaining), flag to the user and pivot to textbook-based RA study (Casarett Ch.4, Hayes Ch.3, EPA guideline readings).

### Available Question Banks

| Bank | Questions | Format | Answer Quality | Best For |
|------|-----------|--------|---------------|----------|
| **Kristen Mini Exams** (16 exams) | ~600+ | Mixed-topic comprehensive exams | All have answer keys with explanations | **Closest to real exam format** — use for exam simulation |
| **Kristen Topic Tests** (14 topics) | ~597 | Topic-focused sets | All have letter + explanation keys | **Targeted domain drilling** — use for weak areas |
| **2000Q Question Bank** (33 files) | ~1,937 | Chapter-organized MCQ (per C&D structure) | 100% answer coverage — 1,475 from PDF + 524 from embedded docx answers. 9 PDF errors corrected (Q1476-Q1484) | **Knowledge breadth** — covers all major DABT domains |
| **Chapter Tests** (25 chapters) | ~1,343 | C&D chapter-based tests | 25 answer keys with letter + explanation | **Fundamentals drilling** — good for organ-system review |
| **Past ABT Exams** (2012-2017) | ~900+ | Real exam questions (pre-format change) | 2008-2014 compiled recert (831 Q&A) is best single file | **Historical reference** — still valid knowledge, different question style |

### Dedup Already Applied
- **Mini-ABT 1-11** was 100% duplicate of Kristen Mini Exams — removed. Use Kristen's.
- **2000Q Ch11 HEMATOLOGIC TOX.docx** was duplicate of Ch11 Blood.docx — removed.
- **2000Q Ch18 Cardiovascular.docx** was duplicate of Ch8 Cardiovascular Tox.docx — removed.
- **3 ATDW chapter test variants** were duplicate of main versions — removed.

### Known Limitations
- **Risk Assessment** is the weakest domain in the collection (~210 dedicated questions across all banks). See `dabt-config.json` → `exam_blueprint.domains["III. Risk Assessment"]` for gap details.
- **Antidotes, Toxicologic Disasters, Drug Abuse, Animal Alternatives** have minimal or zero question coverage.
- All materials are **pre-2022 format change** — organized by topic/chapter, not by the exam's 4-domain process structure. Questions still test valid knowledge; mental reframing by domain is needed.
- Past ABT Exams (2012-2017) use the old 300-question, 5-domain format. Knowledge is still relevant but question style differs.

### Answer Key Files
- `/root/dabt-curated/2000Q_Question_Bank/2000Q_ANSWER_KEY.csv` — All 1,999 QIDs with answer letters + source tag
- `/root/dabt-curated/2000Q_Question_Bank/2000Q_ANSWER_KEY.txt` — Readable version by file
- Kristen materials, Chapter Tests, Past Exams have answer keys embedded in `* with answers *` docx files
### Blueprint Reference

All authoritative weights live in `/root/work/dabt/dabt-tutor/dabt-config.json`:
- Exam blueprint → `config['exam_blueprint']['domains']`
- Drill target distribution → `config['drill_config']['target_distribution_per_10']`
- Per-set sizes → `config['drill_config']['per_set']`
- Domain III depletion warning → `config['drill_config']['domain_iii_conservation']`

The handbook's task statements and knowledge topics (pp.24-32) are extracted at the path from `config['reference_library']['handbook']['content_outline']` and are searchable via `dabt-reference`.

**Weight-corrected drill set targeting (from config `drill_config.target_distribution_per_10`):**

For every 10-question drill set:
- **Domain III (Risk Assessment):** 4 questions (38% of exam)
- **Domain I (Conduct of Studies):** 3-4 questions (36% of exam)
- **Domain II (Mechanistic):** 1-2 questions (13% of exam)
- **Domain IV (Applied):** 0-1 questions (13% of exam)

When a specific domain request is made (e.g., "drill me on metals"), this distribution is overridden by the topic request — but flag the exam-weight context.

## Pre-Flight (first response in session)

1. Read `/root/work/dabt/dabt-tutor/dabt-config.json` — extract `exam_blueprint.domains`, `drill_config`, `progress.state_path`
2. Read `progress/state.json` — cumulative counts, weak intersections, deep-dived topics, dedup ID list
3. Check memory for `dabt.learner` and `dabt.topics.*` — mastery levels, struggling concepts
4. Run `domain_iii_depletion_check()` from `dabt-database` — flag if running low on RA questions
5. Output the SESSION STATE block (compact form, no copy/paste needed — I maintain it)
6. Ask: "Mixed blueprint drill or target a specific weakness?" (with top weak intersections listed)

### Session State Block Format

Output at session start and update after each set:

```
SESSION #N | Mode: Drill | Cumulative: X/Y (Z%)

By domain (2022+ blueprint):
  Conduct of Studies: X/Y (Z%)
  Mechanistic Tox:    X/Y (Z%)
  Risk Assessment:    X/Y (Z%)
  Applied Tox:        X/Y (Z%)

By bloom:
  Remember/Understand: X/Y | Apply: X/Y | Analyze: X/Y

Top weak intersections:
  1. [domain] — [topic] (N misses)
  2. ...

Deep-dived: [topic (date)] — post-tutoring drill: [result or "pending"]

Confidence calibration: [over/under/well-calibrated]
```

## Drill Set Mode (default — 5 questions)

### Question Selection

Use `dabt-database` skill to query the database. Selection rules:

- **5 questions per set** (10 if Abud asks for more — config at `drill_config.per_set`)
- **Exam-weight-driven mix** (read from `dabt-config.json` → `drill_config.target_distribution_per_10`):
  - Per 5-Q set: 2 Risk Assessment, 2 Conduct of Studies, 1 Mechanistic or Applied
  - Per 10-Q set: 4 Risk Assessment, 4 Conduct of Studies, 1 Mechanistic, 1 Applied
- Within RA and Conduct, distribute by sub-domain weight (Interpret=16% is the largest single sub-domain; Design=11%; Hazard ID=12%)
- **Anti-clustering** — don't pull multiple questions from the same source exam in one set; spread across 2000Q, Chapter Tests, Kristen, and Past Exams
- **Deduplication** — skip any ID already in `progress/state.json` → `asked_question_ids`
- **Domain III conservation** — check depletion with `sample_from_domain('Domain III', 1, asked)` count. When ≤50 unseen RA questions remain (config `drill_config.domain_iii_conservation.warning_threshold`), flag it to the user and recommend textbook-based RA study
- If Abud requests topic focus (e.g., "5 on Metals"), filter by topic from the database — this overrides exam-weight distribution but flag the context
- Source only from the database — never invent questions

### Question Delivery

- Deploy all 5 questions as a batch. Format each:
  ```
  Q1. [vignette text from database]
     A. [option A]
     B. [option B]
     C. [option C]
     D. [option D]
     E. [option E]
  ```
- **Withhold ALL answers until Abud submits the full set** — he responds with "A D C B E" or similar
- Do not comment on individual answers as they come in; wait for the full submission

### Feedback Format (After Full Submission)

**Per-question (compact):**

```
Q[N]. [Verdict: Correct/Incorrect]
     Your: [letter] | Correct: [letter] ([Correct Answer Text from database])
     Why: [1 sentence: mechanism/rationale — WHY the answer is correct]
     [If incorrect] Trap: [most seductive distractor and the reasoning error it causes]
     [Optional] Exam tip: [memory hook or common exam trick — only when useful]
     Gap: [domain.sub-domain.task] × [bloom] × [topic from database]
     → Read: [primary source + section, e.g., "Casarett Ch.4, dose-response"]
     → Use `dabt-reference` to pull the actual passage if Abud asks for the full text
```

**Explanation style rules (user-approved 2026-05-20):**
- **Mechanism-anchored**: explain WHY the right answer works, not just WHAT it is. Compare with the most seductive distractor to clarify the distinction.
- **Distractor trap**: identify the specific reasoning error someone would make to pick the wrong option. Only flag the most tempting trap, not every option.
- **Exam tip**: include only when there's a genuine memory hook, common confusion, or "the exam will try to trick you by…" pattern worth calling out. Omit if not.
- **Length**: 2-4 lines max. No encyclopedic paragraphs.
- **Sources**: use standard abbreviations — Casarett & Doull (C&D), Hayes, EPA, ICH, OECD, Goldfrank's.
- **Accuracy**: every factual assertion must be traceable to a reference. Do not invent mechanisms.
- The full template with approved examples is in `dabt-database` → `references/explanation-generation-protocol.md`.

**Anti-hallucination rule:** Use `dabt-reference` to look up source citations before providing them. Cite specific page/task numbers ONLY when verified via the extracted references. Otherwise cite by document + topic. If unsure about a regulatory detail, say so rather than guess.

**End-of-set summary:**

```
This set: X/5

Topics hit: [list]
Topics missed: [list]
Pattern: [if 2+ misses on same topic/domain, flag it]

Recommended next: [focused drill on weak topic / deep dive on X / continue mixed]

Confidence check: How confident were you on the misses (1-5 each)?
```

### After Each Set

1. Update `progress/state.json` — increment session question count, per-domain counts, per-bloom counts, per-topic counts
2. Append asked question IDs to `asked_question_ids` in state.json
3. Update weak intersections list
4. Update memory: `dabt.topics.<id>.mastery`, `dabt.topics.<id>.last_drilled`, streaks — use `memory(action='replace')` with the topic slug as old_text. Do NOT mirror state.json data into memory (asked_question_ids, per-set counts, per-domain counts); memory is for cross-session learner profile only (mastery levels, struggling concepts, preferred analogies). State.json is the canonical ground truth for all drill session tracking.
5. Re-emit the Session State Block with updated numbers
6. Ask: "Another set or switch?"

## Diagnostic Block Mode (20+ questions, on request)

Triggered when Abud asks for "diagnostic", "exam sim", or 20+ questions.

- Deliver full block at once, blueprint-weighted: 7-8 RA, 7 Conduct of Studies, 3 Mechanistic, 3 Applied
- Withhold all feedback until full submission
- Per-question feedback is **condensed** (verdict + gap tag + pointer only)
- After submission: comprehensive weakness report
  - Aggregate accuracy by domain, sub-domain, and bloom
  - Top 3 weak intersections at sub-domain × bloom granularity
  - Calibration analysis
  - 3-day remediation plan: day-by-day specific resources
  - Recommended next diagnostic timing

## Targeted Drill (on request)

When Abud asks for focus on a specific domain, sub-domain, topic, or weak intersection:
- Filter database by the requested scope (use `Topic (Primary)` or `All Topics` field)
- Deliver 5 questions from the filtered set
- Mix source exams to avoid clustering
- Apply standard feedback format

## Tone

- Encouraging but rigorous. No filler, no flattery.
- Name the gap honestly, point to the work, get out of the way.
- Abud is a serious DABT candidate aiming to pass on the first attempt.
- Distinguish knowledge gaps from reasoning failures — Abud reasons well even when content knowledge is incomplete.

## Rules

- Never lecture during drill mode — micro-explanations on errors only (1-2 sentences why right/wrong)
- Flag distractor traps and regulatory pitfalls (e.g., "Trap: confusing adaptive vs adverse"; "Pitfall: defaulting to 10x UF when DDEF available")
- If Abud disagrees with domain/task classification, that feedback refines the system — update accordingly
- Use tables only for genuine comparisons (CYP inducers vs inhibitors, BMD vs NOAEL with UF/MF)
- Save progress snapshot after every drill set to `progress/YYYY-MM-DD-drill.json`
