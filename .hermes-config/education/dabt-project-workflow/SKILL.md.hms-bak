---
name: dabt-project-workflow
description: "Coordinating workflow skill for the DABT Tutor project. Defines the session start procedure (read unified config → load skills → execute), documents the config schema, and links all DABT skills together. All DABT skills should reference this as their entry point."
category: education
---

# DABT Project Workflow

## Mission

Govern how all DABT skills (`dabt-database`, `dabt-reference`, `dabt-deep-dive`, `dabt-drill-mode`, `dabt-synthesis-review`, `dabt-notebook`) interact with the project directory defined at `config['project']['workdir']`. Skills are stateless consumers of a unified project config — they discover the project state at session start rather than hardcoding assumptions.

## Session Start Procedure (ALL DABT sessions)

This is the canonical entry sequence. Every DABT session follows it:
```python
import json
# Bootstrap: read the project config from its known path
CONFIG = json.load(open('/root/work/dabt/dabt-tutor/dabt-config.json'))
WORKDIR = CONFIG['project']['workdir']
```
1. LOAD `education/dabt-project-workflow` (this skill)
2. READ `dabt-config.json` at `/root/work/dabt/dabt-tutor/dabt-config.json` → `CONFIG`
   If the config seems stale, compare `last_updated` against `system.state.materialized_at`.
3. VERIFY G-Brain is healthy — gbrain is the primary reference lookup path.
   Run `gbrain doctor --json | grep -E 'embedding_coverage|chunk_count'`
   to confirm the DABT reference library (106 pages, 6,597 chunks) is searchable.
   If `gbrain search "Ames test"` returns empty, run `gbrain import ~/brain/` to re-import.
4. READ `config['progress']['state_path']` resolved against `config['project']['workdir']` → learner state
5. COMPUTE curriculum coverage — cross-reference `state.cumulative.by_topic` keys against
   `config['curriculum']['domains'][*]['topic_list']` and
   `config['curriculum']['organ_systems']['topic_list']`. Report to agent context:
   - "Domain I: N/3 topics drilled, Domain II: N/4, Domain III: N/3, Domain IV: N/14"
   - "Organ Systems: N/11 drilled"
   - Prerequisite check (Domain II/III/IV require Domain I): verify Domain I topics present in by_topic
   See the Curriculum Coverage section below for the canonical Python snippet.
6. READ AGENTS.md → project-level notes and overrides
7. LOAD dabt-reference (primary lookup), dabt-database (question context), and
   the appropriate mode skill (dabt-drill-mode, dabt-deep-dive, etc.)
8. EXECUTE with config values injected at runtime
```

**G-Brain dependency:** The `dabt-reference` skill now defaults to G-Brain for all lookups. If G-Brain is down or the import is stale, fall back to file search on the extracted/ directory. Never skip the G-Brain health check — an empty brain silently returns no results and the agent falls back to grep without realizing something's wrong.

**`reference/extracted/` directory dependency:** The extracted/ directory (`config['reference_library']['extracted_base']` resolved against `config['project']['workdir']`) is the source of truth for file-search fallback AND the source material for G-Brain import. If it's missing, neither path works. Verify existence with `ls {WORKDIR}/{config['reference_library']['extracted_base']}/casarett-doull-9e/ | head -5`. If missing, the three-stage extraction pipeline must be run before any reference lookups.

## Curriculum Coverage

After reading `config['progress']['state_path']` (step 4), compute topic coverage by cross-referencing `state.cumulative.by_topic` against the curriculum topic lists. Use this Python snippet:

```python
import json
CONFIG = json.load(open('/root/work/dabt/dabt-tutor/dabt-config.json'))
STATE = json.load(open(CONFIG['project']['workdir'] + '/' + CONFIG['progress']['state_path']))
by_topic = STATE.get('cumulative', {}).get('by_topic', {})
curriculum = CONFIG.get('curriculum', {})

coverage_report = {}
for domain_id, domain in curriculum.get('domains', {}).items():
    covered = [t for t in domain['topic_list'] if t in by_topic]
    coverage_report[domain['name']] = {
        "covered": len(covered),
        "total": len(domain['topic_list']),
        "topic_names": sorted(by_topic.keys() & set(domain['topic_list']))
    }

org = curriculum.get('organ_systems', {})
org_covered = [t for t in org.get('topic_list', []) if t in by_topic]
coverage_report['Organ Systems'] = {
    "covered": len(org_covered),
    "total": len(org.get('topic_list', [])),
    "topic_names": sorted(set(by_topic.keys()) & set(org.get('topic_list', [])))
}

for name, info in coverage_report.items():
    pct = info['covered'] / info['total'] * 100 if info['total'] else 0
    print(f"{name}: {info['covered']}/{info['total']} topics ({pct:.0f}%)")
    if info['topic_names']:
        print(f"  Drilled: {', '.join(info['topic_names'])}")
```

**Coverage output examples:**
- "Domain IV: Applied Toxicology: 4/14 topics (29%) — Metals & Metalloids, Drugs & Therapeutics, Pesticides – Insecticides"
- "Organ Systems: 5/11 topics (45%) — Hematology, Hepatotoxicity, Immunotoxicology, Neurotoxicity, Ocular, Skin"
- "Prerequisite check: Domain II/III/IV require Domain I — Domain I topics present: 2/3 (General Principles ✓, Mechanisms ✓, General Toxicology ✗)"

**Coverage summary format for agent context (spoken to the learner):**
```
📊 Coverage: Domain I 1/3 | Domain II 1/4 | Domain III 2/3 | Domain IV 4/14 | Organs 5/11
⚠  Prereq: Domain I needs General Toxicology — flagged for deep dive
```

**CRITICAL RULE:** Never hardcode a path, domain weight, or source list in a skill SKILL.md. All variable configuration must come from `dabt-config.json`. If a skill needs a value that isn't in the config, extend the config — don't patch the skill.

## Unified Config Schema (ALIVE — materialized at /root/work/dabt/dabt-tutor/dabt-config.json)

The config was materialized on 2026-05-20 as version 1.0.0. It contains 13 sections covering all project configuration. See the live file for the full schema — this section documents the key paths skills should read.

Key config paths for skills:

| Skill | Config keys to read |
|-------|-------------------|
| `dabt-project-workflow` | `curriculum.domains`, `curriculum.organ_systems`, `progress.state_path` |
| `dabt-database` | `database.primary.path`, `exam_blueprint.domains[*].weight_pct`, `drill_config` |
| `dabt-reference` | `reference_library.extracted_base`, `reference_library.searchable_sources` |
| `dabt-drill-mode` | `exam_blueprint.domains`, `drill_config.target_distribution_per_10`, `drill_config.domain_iii_conservation` |
| `dabt-deep-dive` | `exam_blueprint.domains`, `progress.state_path`, `reference_library.handbook.content_outline` |
| `dabt-synthesis-review` | `progress.state_path`, `progress.deep_dives_dir` |
| `dabt-notebook` | `project.workdir`, `progress.wiki_dir` |
| `dabt-gbrain-miss-journal` | `progress.miss_journal_backup_dir` |

**Config sections:**
- `project` — workdir, exam date, format
- `exam_blueprint` — domain weights, sub-domain weights, tasks, knowledge topics, DB coverage gaps
- `database` — primary SQLite path, legacy path, quality metrics, source banks, domain distribution
- `reference_library` — extracted sources, handbook paths, searchability flags
- `exam_materials` — undigested past exams inventory
- `drill_config` — target distribution, per-set sizing, Domain III conservation rules
- `curriculum` — embedded topic lists per domain + organ systems with coverage tracking (absorbed from topics.json)
- `progress` — state.json, deep-dives, drills, wiki, miss-journal-backup, template paths
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
  │     G-Brain as primary lookup (vector search + cross-source synthesis),
  │     three-pass file search as fallback for page-level depth
  │     Reads: config.references.extracted_dir, config.references.sources
  │     Depends on: gbrain MCP tools + ~/brain/ import
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

## Data Quality Status (as of 2026-05-30, post-full-recovery)

| Metric | Value | Impact |
|--------|-------|--------|
| Questions in main table | **5,368** (across 10 source banks) | Clean — expanded from 3,796 via recert import + 466 domain classifications |
| Answer letter coverage | **87.5%** (4,698/5,368) | ✅ 670 lacking letters are legitimately flagged as no_answer_key |
| Correct answer texts | 3,796+ | Bulk-fill from answer_options applied; recent imports carry answer text |
| Explanations | **4,546/5,368 (84.7%)** | Missing ones are 670 no-answer-key Qs (no key → no explanation generated) |
| No-answer-key Qs | **670** (401 2017 cert + 269 Past ABT PDFs) | Legitimate — real exam materials without published answer keys |
| Domain III coverage | **287 Qs** (5.3% of bank vs 38% of exam weight) | **Still critical underweight** — upgraded from 170 via new classifications |
| Domain-less Qs | **8 Qs remaining** (down from 466) | ✅ Bulk classification complete; 8 need manual review |
| 2000Q Bank batch33 errors | **FIXED** ✅ | All 34+ corrections verified against Casarett Ch.6 |
| 25 NULL answer_letters (2000Q Bank) | **BACKFILLED** ✅ | All "answer=E" implied-option items fixed |
| 2015 Recert missing from DB | **IMPORTED** ✅ | 40 Qs from 2015 recert now in source_file_id=10 |
| dabt-config.json stale | **REFRESHED** ✅ | Now reflects 5,368 actual count with all source banks |
| Quarantine remaining | **2 items** (down from 1,048) | Bulk recovery complete; residual 2 are truly unrecoverable |
| Synthetic Domain I Qs | **1,600 generated** ✅ | All web-verified against online sources (20% sample audit = PASS) |
| Synthetic Domain III Qs | **600 generated** ✅ | Risk assessment coverage boosted from 170→287 via classification + synthesis |

## Task Roadmap (updated 2026-05-30)

See `references/task-roadmap.md` for full detail. Current status:

1. **Synthetic Domain III Qs (600)** — ✅ **COMPLETE** Generated, imported, web-audited (20% sample PASS).
2. **Synthetic Domain I Qs (1,600)** — ✅ **COMPLETE** Generated, imported, web-audited (20% sample PASS).
3. **Explanations + Bloom Levels** — ✅ **COMPLETE** 4,546/5,368 have explanations. Residual missing = 670 no-answer-key Qs (legitimate — no source to explain from).
4. **Curriculum Topics** — ✅ **COMPLETE** Topics absorbed into config. Coverage tracking built into session start.
5. **Unified Project Config** — ✅ **REFRESHED** (dabt-config.json v1.0.0) — now reflects 5,368 count, all source banks, current domain distribution.
6. **Classify 466 domain-less Qs** — ✅ **COMPLETE** Sources 7+9 classified. Only 8 stragglers remain.
7. **Backfill 25 NULL answer_letters** — ✅ **COMPLETE** 2000Q Bank "answer=E" items fixed.
8. **Import 2015 recert exam** — ✅ **COMPLETE** 40 Qs imported into source_file_id=10.
9. **Batch33 error audit** — ✅ **COMPLETE** 34+ corrections verified against Casarett Ch.6.
10. **Group A recovery (626 Qs)** — ✅ **COMPLETE** All recovered from corrupted answer keys.
11. **Group B reformatting (149 Qs)** — ✅ **COMPLETE** Non-standard options normalized.
12. **Past ABT PDF recovery (273 Qs)** — ✅ **COMPLETE** Extracted with educated-guess answers.
13. **Audit 502 EXCEPT/NOT reversal-prone Qs** — ✅ **COMPLETE** All audited.
14. **Systems integrity audit** — ✅ **COMPLETE** Skills, G-Brain, LCM, Mnemosyne, DB all verified.

### Remaining Gaps
- **670 no-answer-key Qs** (401 from 2017 cert + 269 Past ABT PDFs) — need eventual educated-guess answers or SME review
- **8 unclassified Qs** — need manual review
- **Domain III still underweight** at 287 Qs (5.3% vs 38% exam weight) — synthetic generation improved this from 170, but more would help
- **2013/2015 recert extraction** — 2013 recert was ingested but 2015 was only done as partial recovery via the 40-Question import (t_cfd11e62); full 4-part extraction not done

## Kanban Workflow for DABT Items

When proposing work items from the DABT task list, use the **classify-then-card** pattern:

1. **Investigate** — query DB, check config, identify gaps
2. **Classify** — sort items into two buckets:
   - 🟢 **Kanban-ready**: bounded scope, clear criteria, independent, can execute now
   - 🔵 **Needs discussion**: strategic/planning-heavy, uncertain scope, blocked on user decision
3. **Present** — list both buckets with rationale for each classification
4. **Create cards only for 🟢 items** after user confirms go-ahead
5. **Use `--initial-status blocked`** for any card created during discussion that shouldn't be dispatched yet. Unblock only after user explicitly approves.
6. **Never create cards as default `ready`** when discussing strategy — the dispatcher claims `ready` cards immediately. If cards are accidentally created, complete them with summary "pre-created during discussion" before the dispatcher picks them up.

**Kanban-ready signals:** bounded to ~50 items or less, SQL or batch operation, clear "done" criteria, no upstream decisions needed.
**Needs-discussion signals:** requires strategic approach, involves user preference/decision, spans multiple subtasks, blocked on external input.

*Reference: `kanban-orchestrator` skill for the full decomposition playbook. Load via `skill_view(name='kanban-orchestrator')` for hands-on task management; `kanban-guru` is methodology-only.*

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

9. **Apply DB corrections** — When the cross-verify step (6) found DB discrepancies, apply the verified corrections back to the database:
   - Parse `batch{N}_done.json` for items whose explanation contains the marker `"DB-corrected"`
   - Extract the corrected answer letter: `re.search(r'Correct answer:\s*([A-Z])', explanation).group(1)`
   - Back up the DB first: `cp reference/data/dabt.db reference/data/dabt.db.batch{N}_backup`
   - For each item, UPDATE the questions table with both the corrected answer letter and the explanation: `UPDATE questions SET correct_answer_letter='X', explanation='...' WHERE id='DABT-18xx'`
   - Verify key items changed correctly: `SELECT id, correct_answer_letter FROM questions WHERE id IN ('DABT-18xx', ...)`
   - Items with E-answer corruptions (where the DB stored "E" but only options A–D exist) are typically in the quarantine table, not the questions table — skip them gracefully.
   - A reusable Python script lives at `dabt-database` skill's `scripts/apply_batch_corrections.py` — load via `skill_view(name='dabt-database', file_path='scripts/apply_batch_corrections.py')` and adapt the batch file path.

### Critical Pitfalls

- **When the user asks about DABT DB status or test results: query kanban board + SQLite database first, session history second.** The kanban board (via `hermes kanban list`) shows which tasks completed and their summaries. The SQLite database (`dabt.db`) has the authoritative state metrics. Session history is a secondary source — it may contain detailed reports that kanban summaries don't, but it should never be the primary source for current-state questions. Starting with session search will miss completed tasks and produce stale answers. Pattern: `hermes kanban list | grep <topic>` → SQLite aggregate queries → session search only for missing detail.

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
- **Step 9 (DB corrections) requires shell execution.** The correction Python script must run with `python3` and `sqlite3`. If your session lacks a `terminal` tool, use `cronjob` with `no_agent=True` and a script file placed in `~/.hermes/scripts/` (relative path works). Alternatively, delegate via kanban: create a task for the `default` profile with terminal toolsets and `initial_status='blocked'` — the operator unblocks after confirming the batch file is ready.
- **Always use Python json.dump for output, never raw string assembly.** When explanations contain quoted terms (e.g., `"except"`, `"aging"`, `"all of the above"`), constructing the JSON with `write_file` and raw string interpolation produces invalid JSON from unescaped double quotes. Write a Python script that builds the data structure in a list/dict and writes it with `json.dump(data, f, indent=2, ensure_ascii=False)`. This avoids: unescaped quotes, missing commas, encoding issues with em-dashes/accents, trailing whitespace, and miscounted braces.
- **Pesticide batches (Domain IV) from the 2000Q Bank have a 56% error rate.** Batch19 (DABT-1119-1168) showed the second-highest DB error rate of any processed batch (56%, second only to batch13 neuro at 58%). Key failure modes: (a) **circular permutation of matching-test items** — all 8 chemical→class pairs shifted by one position; (b) **mechanism confusions** — fipronil stored as Na channel blocker (should be GABA Cl channel), lindane stored as P450 inhibitor (should be GABA antagonist), rotenone stored as E (should be complex I inhibitor); (c) **counterintuitive "except" designations** — neonicotinoid selectivity, paraquat redox cycling, dithiocarbamate metal coordination all designated as false despite being textbook facts. Always verify pesticide questions against Casarett & Doull Ch.22 before accepting the DB answer.
- **Neurotoxicology batches (Domain IV) need extra caution.** Batch13 (DABT-0869-0918) had a 58% DB error rate — the highest of any processed batch. Key failure modes: (a) matching-test chemical→effect pairs are systematically scrambled (like all prior batches from source_file_id=2), (b) MPTP/dopamine subtopic had 100% error rate (MAO-B vs MAO-A, DAT transport, paclitaxel mechanism, amphetamine classification), (c) fundamental neurobiology reversals (Schwann cell → CNS myelin instead of PNS; oligodendrocytes → defense instead of astrocytes; cranial nerves → first in axonopathy instead of stocking-glove). Always verify neuro questions against Casarett Ch.16 before accepting the DB answer.
- **Zero-option questions from 2000Q Bank.** Some questions (e.g., DABT-1169 "chlorothalonil", DABT-1170 "norbormide") have only a single-word `question_text` and ZERO rows in the `answer_options` table. These originate from source_file_id=2 where the question structure is a single term the examinee must classify. Check the `question_topics` table for context (e.g., "Pesticides – Insecticides" → the single word is likely NOT an insecticide). Verify the correct classification against Casarett & Doull reference texts (Ch.22 for pesticides, Ch.23 for metals, etc.). Do not skip these — they need explaining based on what the compound is (or isn't) rather than from answer options. Detection: `SELECT q.id, q.question_text, q.correct_answer_letter, COUNT(a.id) as cnt FROM questions q LEFT JOIN answer_options a ON q.id=a.question_id GROUP BY q.id HAVING cnt=0;`
- **NEW PATTERN: Letter-only zero-option items (batch28).** Some matching items have `correct_answer_letter` stored but ZERO rows in `answer_options` — the option text was lost during extraction but the answer key letter survived. This differs from the classic zero-option case where both are missing. The stored letter is suspect when preceding items in the same matching set have wrong associations. Detection: `SELECT q.id, q.question_text, q.correct_answer_letter FROM questions q LEFT JOIN answer_options a ON q.id = a.question_id WHERE q.source_file_id = 2 AND q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != '' GROUP BY q.id HAVING COUNT(a.id) = 0;`
- **`reference/extracted/` directory may not exist.** The AGENTS.md references `reference/extracted/` for 35 Casarett chapters, 39 Hayes chapters, and 29 regulations. **Verify this directory exists before any batch explanation workflow that relies on extracted markdown.** Current disk state (2026-05-25): source PDFs are at `reference/textbooks/casarett-doull-9e.pdf`, `reference/textbooks/hayes-7e.pdf`, and `reference/regulations/` subdirectories. No extracted markdown directory has been materialized. If running gbrain integration, this extraction step is a prerequisite.
- **"Letter E" with only A–D options.** Many questions from the 2000Q Bank have `correct_answer_letter = "E"` but only 4 option rows (A–D). These function as "none of the above" or "all of the above." Some are valid (all listed statements are true/false), but in ~30% of cases the E answer is factually wrong and one of A–D is the textbook-correct answer (e.g., batch20: DABT-1195, 1217, 1218). Always cross-verify E-answer questions against reference texts — don't assume E is correct just because it's the stored answer.
- **Endocrine/reproductive batches (Domain IV) are also highly error-prone.** Batch17 (DABT-1019-1068) had a 28% error rate (14/50). Distinct failure modes not seen in other batches: (a) **fundamental physiology reversals** — dopamine agonist stored as antagonist, zona glomerulosa→glucocorticoids instead of aldosterone, pendrin→activin for iodide transport, adrenal cortex test→metanephrine instead of cortisol; (b) **species-difference reversal** — DB says humans lack TBG when rats actually do; (c) **epidemiology swap** — adrenal carcinoma stored as most common endocrine neoplasm instead of thyroid, RET mutations linked to adrenal cortex instead of medullary thyroid. Always verify endocrine questions against Casarett & Doull Ch.20, reproductive against Ch.21 before accepting the DB answer.
- **CYP450/Biotransformation batches (Domain II) from the 2000Q Bank — error-prone (batch34, DABT-1869-1918).** First CYP450 batch revealed systematic errors. Key failure modes: (a) **matching test scrambled across 13 items** — omeprazole stored as CYP1A2 inducer (should be CYP2C19/3A4 substrate), debrisoquin as CYP3A4 inhibitor (should be CYP2D6 substrate), bupropion as CYP3A4 inhibitor (should be CYP2B6 substrate), alprazolam as CYP2D6 inducer (should be CYP3A4 substrate), fluvoxamine as CYP2E1 inducer (should be CYP1A2/2C19/3A4 inhibitor), beta-naphthoflavone as CYP2E1 inducer (should be CYP1A1/1A2 inducer); (b) **factual identity errors** — CYP3A7 stored as rodent liver (should be fetal human liver); CYP450 enzyme in liver+small intestine stored as CYP1B1 (should be CYP3A4); (c) **Letter-E on 4-option items** — oxidative desulfuration stores E but parathion->paraoxon (A) is the textbook example per Casarett Ch.6; autoinduction question stores E but carbamazepine (C) is the classic autoinducer. Always verify CYP450 questions against Casarett Ch.6 before accepting DB answer. See `references/batch34-cyp450-errors.md` for item-by-item breakdown.
- **Air Pollution batches (Domain IV) from the 2000Q Bank appear clean.** Batch25 (DABT-1433-1468) is the first Air Pollution batch processed — **zero discrepancies found in 36 questions**. All 36 have full 4-option sets, no letter-E corruptions, no zero-option items, and 14 "all except" questions correctly identify false statements. This is highly unusual for source_file_id=2 and may reflect a cleaner sub-source within the 2000Q Bank. Air Pollution reference: Casarett & Doull Ch.27.

## Rules

- This skill is the entry point for ALL DABT sessions. Load it first, then dispatch to the appropriate mode skill.
- Never hardcode a project path, domain weight, or source list in any skill SKILL.md. Those live in the project config.
- If a skill needs to be patched with a new path or weight, update the project config instead. Patch the skill only if its *behavior* changes, not its *data*.
