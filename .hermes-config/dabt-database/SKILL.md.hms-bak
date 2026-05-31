---
name: dabt-database
description: "Query the expanded DABT Practice Questions Database (3,796 main-table Qs, 1,048 quarantined, across 8 source banks — SQLite). Blueprint-weighted sampling, anti-clustering, dedup tracking. DB path from dabt-config.json. Legacy xlsx at reference/data/DABT_Practice_Questions_Database.xlsx."
category: education
---

# DABT Practice Questions Database

## Session Start
Load `dabt-project-workflow` first for config. DB path from `config['database']['primary']['path']` resolved against `config['project']['workdir']`. Domain weights from `config['drill_config']['target_distribution_per_10']`.

**Full recovery complete (2026-05-30):** The database now holds **5,368 questions** across 10 source banks with 5,362 domain-classified. Only **8 Qs still lack domain labels**, **670 Qs are legitimately flagged as no-answer-key** (401 from 2017 cert + 269 Past ABT PDFs), and only **2 items remain in quarantine**. Key recovery milestones: 626 Group A Qs recovered from corrupted answer keys, 273 Past ABT PDFs extracted, 466 domain-less Qs classified, 1,600 synthetic Domain I Qs and 600 synthetic Domain III Qs generated, 2015 recert exam imported. See `dabt-project-workflow` → `references/task-roadmap.md` for full tracking.

**Weekly truth audit:** Cron `DABT Weekly Truth Audit` (Sundays 05:00 UTC) — 5 merged checks: DB coverage, sample truth audit, new explanation quality, G-Brain health check, miss journal synthesis. Check latest output for new discrepancies. The last audit (t_07d66662) found 6 PASS, 2 PARTIAL FAIL, 2 FAIL — all follow-up tasks now complete.

## Schema (7 tables)
Core tables: `source_files`, `questions` (id TEXT PK, question_text, correct_answer_letter, explanation, source_file_id, bloom_level), `answer_options` (question_id, option_letter, option_text), `question_topics` (question_id, topic), `question_domains` (question_id, domain I-IV, sub_domain, task), `match_pairs` (term, match_answer), `state` (progress tracking). Full DDL in `references/schema.md`.

## Domain Distribution
DB is structurally skewed (56.4% Applied vs 38% exam weight for Risk Assessment). **DO NOT use raw DB proportions.** Use `config['drill_config']['target_distribution_per_10']` for sampling. 

**Current domain counts (as of 2026-05-30):**
- Domain I (Study Design | 36% exam weight): **1,125 Qs** (21.0%)
- Domain II (Mechanistic | 13% exam weight): **925 Qs** (17.2%)
- Domain III (Risk Assessment | 38% exam weight): **287 Qs** (5.3%) ⚠️ still critically underweight
- Domain IV (Applied | 13% exam weight): **3,025 Qs** (56.4%)
- Unclassified: **8 Qs**

Domain III (38% exam weight, 5.3% DB) has the worst ratio — conserve them during drilling. Domain IV is massively overweight and should be sampled sparingly to reflect exam proportion.

See `references/domain-distribution.md`.

## Core Query Patterns
All in `references/query-patterns.md`. Quick reference:

## DB Correction Script
A reusable Python script at `scripts/apply_batch_corrections.py` applies verified corrections from `batch{N}_done.json` back to the database. It:
- Parses batch files for items with `"DB-corrected"` markers and `"Correct answer: X"` patterns
- Gracefully skips quarantine-table items (E-answer corruptions, etc.)
- Backs up dabt.db before writing
- Updates both `correct_answer_letter` and `explanation`
- Verifies key items after the update

Load via `skill_view(name='dabt-database', file_path='scripts/apply_batch_corrections.py')` and run with `python3 apply_batch_corrections.py <batch_number>`. Requires terminal access — see the "Apply DB corrections" step in `dabt-project-workflow` for fallback paths.

```python
import sqlite3, json, random, os
# Config loaded at session start via dabt-project-workflow
WORKDIR = CONFIG['project']['workdir']
DB_PATH = os.path.join(WORKDIR, CONFIG['database']['primary']['path'])
conn = sqlite3.connect(DB_PATH)

# Blueprint-weighted sample (preferred)
TARGET = CONFIG['drill_config']['target_distribution_per_10']
# sample_by_exam_weight(n, asked_ids) → see references/query-patterns.md

# Direct domain query
def sample_from_domain(domain, n, asked_ids, exclude_sources=None):
    """Sample n unseen questions from a domain."""
    conn = sqlite3.connect(DB_PATH)
    placeholders = ','.join('?' * len(asked_ids)) if asked_ids else 'NULL'
    source_filter = ''
    if exclude_sources:
        source_filter = "AND q.source_file_id NOT IN (" + ','.join(map(str, exclude_sources)) + ")"
    query = f"""SELECT q.* FROM questions q JOIN question_domains d ON q.id = d.question_id
                WHERE d.domain = ? AND q.id NOT IN ({placeholders}) {source_filter} ORDER BY RANDOM() LIMIT ?"""
    return conn.execute(query, [domain] + list(asked_ids) + [n]).fetchall()
```

## Synthetic Question Generation — Protocol

When the user asks to generate synthetic DABT-style questions for underweight domains (Domain III or Domain I deficit):

### When to Use
- Domain III (Risk Assessment) has ~170 Qs for 38% exam weight — target 600 synthetic Qs
- Domain I (Conduct of Studies) has ~768 Qs for 36% exam weight — target 1,600 synthetic Qs
- Any topic where available DB questions are too few for effective drilling

### Ground Truth Sources
| Domain | Sources |
|--------|---------|
| Domain III | Casarett Ch.4 (190KB), Hayes Ch.3 (273KB) & Ch.10 (510KB), EPA Cancer Guidelines (359KB), Silver Book (1.4MB), IRIS docs |
| Domain I | Casarett Ch.5-7 (ADME/TK, 1.6MB), Ch.31-35 (analytical/regulatory), Hayes Ch.2/11/12/21-27, ICH (26 docs), OECD (13 docs), EPA GLP, RedBook, ABT Handbook task statements |

### Generation Rules
1. **Every question must cite its exact source** (chapter + page range). No citation → rejected.
2. **Use the exam blueprint's sub-domain weights**, not the DB's natural proportions.
3. **Format distribution targets** (deviations >5% need explicit justification in batch notes):
   - Standard MC: 55%
   - EXCEPT/NOT: 15%
   - Calculation (MOE, BMD, slope factor, ADD/LADD, HQ): 15%
   - Vignette (scenario-based with clinical/regulatory context): 15%
4. **Bloom's taxonomy targets** (deviations >5% need justification):
   - Recall (definitions, facts): 25%
   - Application (calculate, apply concept to new context): 50%
   - Analysis (compare, critique, determine implications): 25%
5. **4 plausible options** (A-D) — the correct answer is unambiguous when cross-referenced against the cited source. Distractors should be plausible but clearly wrong per the source material.
6. **Self-review**: the generating agent must confirm the correct answer matches the source before committing.
7. **10% post-audit**: spot-check a random sample against reference texts to catch drift.
8. **Flag as synthetic-2026** in the DB (synthetic_source = 'generated-2026') so synthetic and source-bank Qs are distinguishable.

### Generate–Validate–Tune Workflow
For batches of 50+ questions, use a programmatic pipeline rather than hand-crafting:

1. **Generate**: Write a Python script that constructs the full question batch as structured data — each question as a dict with all required fields (question_number, sub_domain, format, question_text, options, correct_answer, explanation, source, bloom_level). The script enforces structural rules (4 options A-D, correct answer in {A,B,C,D}) programmatically.

2. **Validate**: Run a validation pass over the generated JSON:
   - Question numbers form a contiguous sequence 1..N
   - All 4 options present (keys A-D)
   - correct_answer in {A,B,C,D}
   - bloom_level in {Recall, Application, Analysis}
   - format in {MC, EXCEPT/NOT, calculation, vignette}
   - explanation is substantive (>50 chars)
   - source contains chapter/page citation
   - sub_domain matches the target

3. **Count & Tune**: Count format and bloom distributions. If off-target:
   - Reclassify marginal questions (many "Recall" definitions are actually "Application" when the question tests applying the definition to a scenario)
   - Convert MC → EXCEPT/NOT by rephrasing the question stem and verifying the answer key becomes the FALSE statement
   - Convert MC → vignette when the question embeds a scenario (case study, regulatory context, epidemiological finding)
   - Re-run validation after each tuning pass

4. **Finalize**: One last validation after all tuning passes. Then deliver.

Pitfall: questions initially labeled "Recall" because they test a definition may actually be "Application" if the test-taker must determine which answer fits from distractors that misuse the definition. Classify by what the test-taker must DO, not by the surface topic.

Pitfall: calculation questions often get labeled "MC" by mistake. If the question provides numeric values and asks for a computed answer, label it "calculation".

Reference: `references/domain-iii-c-source-map.md` for a concrete example of source material mapping with key page ranges and numeric constants extracted from a 200-question Domain III-C generation session.

### Workflow
1. Sub-topic mapping → split target count across sub-domains proportionally
2. Pre-load reference chapter(s) for each sub-domain — extract key page ranges and numeric constants first (see `references/domain-iii-c-source-map.md` for a template)
3. Delegate parallel batches of 50 Qs to subagents, each with source chapter in context
4. Each batch writes: question, 4 options, correct answer, explanation (3-5 lines), source citation, bloom level, format
5. Validate within each batch (structural + distribution)
6. Post-generation audit (10% sample verified against reference)

### No-Answer-Key Question Type
For real exam PDFs without published answer keys (Past ABT PDFs, 2017 cert):
- Add to DB with correct_answer_letter = NULL
- Set synthetic_source = 'no-answer-key' for filtering
- Do NOT generate educated guesses automatically
- These become discussion prompts — when encountered during drilling they trigger review conversation rather than scoring

### Coverage Tracking via Curriculum Structure
The curriculum section in dabt-config.json (after absorption) provides:
- Prerequisite ordering — Domain I → Domain III. Checks whether the user has foundations before advanced topics.
- Topic checklists — e.g. 4/14 Domain IV topics covered, 5/11 organ systems drilled
- Cross-references progress/state.json by_topic against curriculum topic lists

After curriculum absorption into config, patch dabt-drill-mode to read topic lists from the config curriculum section for coverage reporting.

## Data Quality Policy
Issues → quarantine with documented label. Do NOT leave NULL/missing markers in main table. Main table must always produce valid questions with no quality filter. File path and absolute state path: `CONFIG['database']['primary']['path']` and `CONFIG['progress']['state_path']`.

**Current state:** All recovery work complete. 670 Qs legitimately flagged as no-answer-key (not a quality defect — these are real exam materials without published keys). 8 Qs need domain classification — prioritize next session.
