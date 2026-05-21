---
name: dabt-project-workflow
description: "Coordinating workflow skill for the DABT Tutor project. Defines the session start procedure (read unified config → load skills → execute), documents the config schema, and links all DABT skills together. All DABT skills should reference this as their entry point."
category: education
---

# DABT Project Workflow

## Mission

Govern how all DABT skills (`dabt-database`, `dabt-reference`, `dabt-deep-dive`, `dabt-drill-mode`, `dabt-synthesis-review`, `dabt-notebook`) interact with the project directory at `/root/work/dabt/dabt-tutor/`. Skills are stateless consumers of a unified project config — they discover the project state at session start rather than hardcoding assumptions.

## Session Start Procedure (ALL DABT sessions)

This is the canonical entry sequence. Every DABT session follows it:

```
1. LOAD this skill (dabt-project-workflow) — the orchestrator
2. LOAD dabt-config.json — the unified project config
   Path: /root/work/dabt/dabt-tutor/dabt-config.json
   Config is ALIVE (materialized 2026-05-20) — supersedes all fallback files.
   No fallback needed. If it's missing, something's wrong.
3. READ /root/work/dabt/dabt-tutor/progress/state.json → learner state
4. READ AGENTS.md → project-level notes and overrides
5. SELECT the appropriate mode skill based on user's request
6. EXECUTE with config values injected at runtime
```

**CRITICAL RULE:** Never hardcode a path, domain weight, or source list in a skill SKILL.md. All variable configuration must come from `dabt-config.json`. If a skill needs a value that isn't in the config, extend the config — don't patch the skill.

## Unified Config Schema (ALIVE — materialized at /root/work/dabt/dabt-tutor/dabt-config.json)

The config was materialized on 2026-05-20 as version 1.0.0. It contains 13 sections covering all project configuration. See the live file for the full schema — this section documents the key paths skills should read.

Key config paths for skills:

| Skill | Config keys to read |
|-------|-------------------|
| `dabt-database` | `database.primary.path`, `exam_blueprint.domains[*].weight_pct`, `drill_config` |
| `dabt-reference` | `reference_library.extracted_base`, `reference_library.searchable_sources` |
| `dabt-drill-mode` | `exam_blueprint.domains`, `drill_config.target_distribution_per_10`, `drill_config.domain_iii_conservation` |
| `dabt-deep-dive` | `exam_blueprint.domains`, `progress.state_path`, `reference_library.handbook.content_outline` |
| `dabt-synthesis-review` | `progress.state_path`, `progress.deep_dives_dir` |
| `dabt-notebook` | `project.workdir` (wiki/ subdirectory) |

**Config sections:**
- `project` — workdir, exam date, format
- `exam_blueprint` — domain weights, sub-domain weights, tasks, knowledge topics, DB coverage gaps
- `database` — primary SQLite path, legacy path, quality metrics, source banks, domain distribution
- `reference_library` — extracted sources, handbook paths, searchability flags
- `exam_materials` — undigested past exams inventory
- `drill_config` — target distribution, per-set sizing, Domain III conservation rules
- `curriculum` — pointer to curriculum/topics.json (needs discussion)
- `progress` — state.json, deep-dives, drills, template paths
- `learner` — profile, strengths, weak areas, tone preferences
- `skills` — all 6 DABT skills with paths and functions
- `task_tracker` — all 6 work items with priority, scope, status

When extending the project (adding synthetic questions, extracting new exams), update `dabt-config.json` first. Then skills automatically pick up the changes.

## Skill Map

```
dabt-project-workflow (this skill)
  ├── Orchestrates session start, reads project config
  ├── Points to the correct mode skill
  │
  ├── dabt-database
  │     SQLite interface — query patterns, domain filtering, weighted sampling
  │     Reads: config.database.primary, config.exam.domains
  │
  ├── dabt-reference
  │     Three-pass full-text search across extracted references
  │     Reads: config.references.extracted_dir, config.references.sources
  │
  ├── dabt-drill-mode
  │     Quiz engine — blueprint-weighted question sets, session tracking
  │     Reads: config.exam.domains, config.exam.drill_targets_per_5/_10
  │
  ├── dabt-deep-dive
  │     Socratic tutoring — first-principles topic exploration, artifacts
  │     Reads: config.exam.domains (for topic priority), config.progress
  │
  ├── dabt-synthesis-review
  │     Cross-topic consolidation — comparison matrices, flashcards
  │     Reads: config.progress.deep_dives_dir (for completed topics)
  │
  └── dabt-notebook
        Lightweight concept notes — create/update wiki pages
        Reads: config.progress.wiki_dir
```

## Data Quality Status (as of 2026-05-20, end of answer recovery + quarantine session)

| Metric | Value | Impact |
|--------|-------|--------|
| Questions in main table | **3,793** (4,841 total, 1,048 quarantined) | Clean — every question drillable |
| Answer letter coverage | **100% in main table** (3,793/3,793) | ✅ No NULL answer letters in active pipeline |
| Explanations | 2,892/3,793 (76%) | 901 drillable without feedback |
| Bloom levels | **100% (4,841/4,841)** | ✅ Across main + quarantine |
| Domain III coverage | 210 Qs (5.5% of bank vs 38% of exam) | **Severe underweight** — biggest exam risk |
| Domain III sub-domain granularity | 135/210 unassigned; only RiskChar tagged | Need reclassification before synthetic Q generation |
| 2000Q Bank residual risk | 1,351 passed quarantine | May still have factual errors — truth audit cron samples weekly |
| Quarantine size | 1,048 questions | Documented with `q_issue` labels; restorable if sources improve |

## Task Roadmap (updated 2026-05-20 — answer recovery + quarantine complete)

See `references/task-roadmap.md` for the full 6-task plan. Current status:

1. **Synthetic Questions** — Planned
2. **Supplementary Materials** — Declined (noise risk)
3. **Explanations + Bloom Levels** — **COMPLETE** ✅ Bloom levels done (100%, 4,841/4,841). Explanations done for 2,892/3,793 in main table. Answer recovery **COMPLETE** (1,474 answers recovered; 1,048 broken questions quarantined). Main table at 100% answer coverage.
4. **Curriculum Topics** — Pending discussion
5. **Unified Project Config** ✅ **COMPLETE** (dabt-config.json v1.0.0 materialized)
6. **Digest Past Exams** — Planned (quarantined 273 Past ABT PDF questions need SME review for re-entry)

## Batch Explanation Writing Workflow

Task Roadmap item 3 involves writing 2-4 sentence explanations for questions that lack them using parallel subagents via `delegate_task`.

### Trigger

- User provides a batch file path (e.g., `batches/batch8.json`) containing an array of QID strings
- User says "write explanations for batch N" or requests a specific set of QIDs

### Procedure

1. **Read the batch file** — `batches/batch{N}.json` is a JSON array of QID strings
2. **Query the database** — Select `id, question_text, correct_answer_letter, correct_answer_text, explanation` from `questions` table, plus `option_letter, option_text` from `answer_options` table
3. **Identify the chapter scope** — Group questions by topic (e.g., hematology, immunology, risk assessment) to target the right reference chapters
4. **Research reference texts** — Use `dabt-reference` three-pass search to find supporting passages in Casarett/Hayes/regulations
5. **Write each explanation** — Each explanation must contain:
   - The correct answer (letter + text)
   - The mechanism, regulatory basis, or toxicologic principle
   - A distractor trap (why the wrong options are tempting)
   - A source citation (e.g., `Casarett Ch.N "Title" pp.X-Y`)
   - 2-4 sentences, ~40-80 words
6. **Cross-verify** — Before finalizing, check the DB's correct answer against the reference text. If they contradict, note the discrepancy in the explanation rather than writing a factually wrong statement
7. **Save output** — Write to `batches/batch{N}_done.json` with schema `[{id, explanation, domain}]` — a list of dicts, each containing the question ID string, explanation text, and domain label (e.g., "Domain IV / Applied Toxicology"). This is the current standard format used by recent batches (batch33 onward). Do NOT use the older dict-keyed-by-QID format.
8. **Self-review** — Verify all entries present, all have source citations, all word counts within range, AND every explanation explicitly mentions the correct answer letter (not just the description). A scripted check: `if ans_letter not in item['explanation']: errors.append(...)`

### Critical Pitfalls

- **DB answers may contradict reference texts.** Batch 8 found ~15+ discrepancies across 50 questions where the DB's correct answer disagrees with Casarett & Doull. Common patterns:
  - Matching-type questions where the chemical-to-effect mapping is wrong
  - "All of the following are true EXCEPT" where the answer letter points to the TRUE statement instead of the exception
  - Basic immunology concept reversals (thymus vs spleen for negative selection, T cell migration sites)
  - Clotting factor half-life ordering (Casarett says factor VII has shortest half-life, DB says IX)
- **Never silently accept a wrong DB answer.** If the reference text contradicts the DB, note both the DB answer and what the textbook says, flagged with "Note:" or "Reference check:". Let the user judge which source the exam will follow.
- **Self-review is mandatory.** After writing all explanations, run a verification pass checking: every QID present, every explanation has a citation, answer letter matches.
- **Subagents produce varying JSON output formats.** Batch subagents saved explanations as: (a) list of `{id, explanation, domain}` dicts, (b) dict keyed by QID with `{correct_answer, explanation}` values, (c) dict keyed by QID with bare string values. Always check the format before bulk-committing — normalize to `[(qid, explanation_str)]` first.
- **Reference chapters are broad.** A single batch often spans 2+ textbook chapters. Pre-scan the batch to identify topic clusters before starting reference searches.
- **Explanation length varies by batch error rate.** When batches have many DB discrepancies (batch13 neuro: 58% error rate), explanations must be longer: they need to state the textbook-correct answer, explain the mechanism, AND note the DB discrepancy. Target 4-8 sentences (~80-150 words) for high-error-rate batches vs. 2-4 sentences (~40-80 words) for low-error batches.
- **Self-review check must use textbook-correct answer, not DB answer.** The check `if ans_letter not in item['explanation']: errors.append(...)` should use the textbook-correct answer letter, not the DB-stored answer. When DB is wrong, the explanation will contain the correct textbook answer, not the DB answer. Falsely flagging these as errors wastes time.
- **Always use Python json.dump for output, never raw string assembly.** When explanations contain quoted terms (e.g., `"except"`, `"aging"`, `"all of the above"`), constructing the JSON with `write_file` and raw string interpolation produces invalid JSON from unescaped double quotes. Write a Python script that builds the data structure in a list/dict and writes it with `json.dump(data, f, indent=2, ensure_ascii=False)`. This avoids: unescaped quotes, missing commas, encoding issues with em-dashes/accents, trailing whitespace, and miscounted braces.
- **Pesticide batches (Domain IV) from the 2000Q Bank have a 56% error rate.** Batch19 (DABT-1119-1168) showed the second-highest DB error rate of any processed batch (56%, second only to batch13 neuro at 58%). Key failure modes: (a) **circular permutation of matching-test items** — all 8 chemical→class pairs shifted by one position; (b) **mechanism confusions** — fipronil stored as Na channel blocker (should be GABA Cl channel), lindane stored as P450 inhibitor (should be GABA antagonist), rotenone stored as E (should be complex I inhibitor); (c) **counterintuitive "except" designations** — neonicotinoid selectivity, paraquat redox cycling, dithiocarbamate metal coordination all designated as false despite being textbook facts. Always verify pesticide questions against Casarett & Doull Ch.22 before accepting the DB answer.
- **Neurotoxicology batches (Domain IV) need extra caution.** Batch13 (DABT-0869-0918) had a 58% DB error rate — the highest of any processed batch. Key failure modes: (a) matching-test chemical→effect pairs are systematically scrambled (like all prior batches from source_file_id=2), (b) MPTP/dopamine subtopic had 100% error rate (MAO-B vs MAO-A, DAT transport, paclitaxel mechanism, amphetamine classification), (c) fundamental neurobiology reversals (Schwann cell → CNS myelin instead of PNS; oligodendrocytes → defense instead of astrocytes; cranial nerves → first in axonopathy instead of stocking-glove). Always verify neuro questions against Casarett Ch.16 before accepting the DB answer.
- **Zero-option questions from 2000Q Bank.** Some questions (e.g., DABT-1169 "chlorothalonil", DABT-1170 "norbormide") have only a single-word `question_text` and ZERO rows in the `answer_options` table. These originate from source_file_id=2 where the question structure is a single term the examinee must classify. Check the `question_topics` table for context (e.g., "Pesticides – Insecticides" → the single word is likely NOT an insecticide). Verify the correct classification against Casarett & Doull reference texts (Ch.22 for pesticides, Ch.23 for metals, etc.). Do not skip these — they need explaining based on what the compound is (or isn't) rather than from answer options. Detection: `SELECT q.id, q.question_text, q.correct_answer_letter, COUNT(a.id) as cnt FROM questions q LEFT JOIN answer_options a ON q.id=a.question_id GROUP BY q.id HAVING cnt=0;`
- **NEW PATTERN: Letter-only zero-option items (batch28).** Some matching items have `correct_answer_letter` stored but ZERO rows in `answer_options` — the option text was lost during extraction but the answer key letter survived. This differs from the classic zero-option case where both are missing. The stored letter is suspect when preceding items in the same matching set have wrong associations. Detection: `SELECT q.id, q.question_text, q.correct_answer_letter FROM questions q LEFT JOIN answer_options a ON q.id = a.question_id WHERE q.source_file_id = 2 AND q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != '' GROUP BY q.id HAVING COUNT(a.id) = 0;`
- **"Letter E" with only A–D options.** Many questions from the 2000Q Bank have `correct_answer_letter = "E"` but only 4 option rows (A–D). These function as "none of the above" or "all of the above." Some are valid (all listed statements are true/false), but in ~30% of cases the E answer is factually wrong and one of A–D is the textbook-correct answer (e.g., batch20: DABT-1195, 1217, 1218). Always cross-verify E-answer questions against reference texts — don't assume E is correct just because it's the stored answer.
- **Endocrine/reproductive batches (Domain IV) are also highly error-prone.** Batch17 (DABT-1019-1068) had a 28% error rate (14/50). Distinct failure modes not seen in other batches: (a) **fundamental physiology reversals** — dopamine agonist stored as antagonist, zona glomerulosa→glucocorticoids instead of aldosterone, pendrin→activin for iodide transport, adrenal cortex test→metanephrine instead of cortisol; (b) **species-difference reversal** — DB says humans lack TBG when rats actually do; (c) **epidemiology swap** — adrenal carcinoma stored as most common endocrine neoplasm instead of thyroid, RET mutations linked to adrenal cortex instead of medullary thyroid. Always verify endocrine questions against Casarett & Doull Ch.20, reproductive against Ch.21 before accepting the DB answer.
- **CYP450/Biotransformation batches (Domain II) from the 2000Q Bank — error-prone (batch34, DABT-1869-1918).** First CYP450 batch revealed systematic errors. Key failure modes: (a) **matching test scrambled across 13 items** — omeprazole stored as CYP1A2 inducer (should be CYP2C19/3A4 substrate), debrisoquin as CYP3A4 inhibitor (should be CYP2D6 substrate), bupropion as CYP3A4 inhibitor (should be CYP2B6 substrate), alprazolam as CYP2D6 inducer (should be CYP3A4 substrate), fluvoxamine as CYP2E1 inducer (should be CYP1A2/2C19/3A4 inhibitor), beta-naphthoflavone as CYP2E1 inducer (should be CYP1A1/1A2 inducer); (b) **factual identity errors** — CYP3A7 stored as rodent liver (should be fetal human liver); CYP450 enzyme in liver+small intestine stored as CYP1B1 (should be CYP3A4); (c) **Letter-E on 4-option items** — oxidative desulfuration stores E but parathion->paraoxon (A) is the textbook example per Casarett Ch.6; autoinduction question stores E but carbamazepine (C) is the classic autoinducer. Always verify CYP450 questions against Casarett Ch.6 before accepting DB answer. See `references/batch34-cyp450-errors.md` for item-by-item breakdown.
- **Air Pollution batches (Domain IV) from the 2000Q Bank appear clean.** Batch25 (DABT-1433-1468) is the first Air Pollution batch processed — **zero discrepancies found in 36 questions**. All 36 have full 4-option sets, no letter-E corruptions, no zero-option items, and 14 "all except" questions correctly identify false statements. This is highly unusual for source_file_id=2 and may reflect a cleaner sub-source within the 2000Q Bank. Air Pollution reference: Casarett & Doull Ch.27.

## Rules

- This skill is the entry point for ALL DABT sessions. Load it first, then dispatch to the appropriate mode skill.
- Never hardcode a project path, domain weight, or source list in any skill SKILL.md. Those live in the project config.
- If a skill needs to be patched with a new path or weight, update the project config instead. Patch the skill only if its *behavior* changes, not its *data*.
