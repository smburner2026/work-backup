---
name: dabt-database
description: "Query the DABT Practice Questions Database (7,567 main-table Qs, 2 quarantined, 35 no-answer-key, across 17 source banks — SQLite). Blueprint-weighted sampling, anti-clustering, dedup tracking, synthetic generation with post-import verification. DB path from dabt-config.json."
category: education
---

# DABT Practice Questions Database

## Session Start
Load `dabt-project-workflow` first for config. DB path from `config['database']['primary']['path']` resolved against `config['project']['workdir']`. Domain weights from `config['drill_config']['target_distribution_per_10']`.

**Phantom completion incident RESOLVED (2026-06-02):** Synthetic generation tasks that were previously marked done without data landing are now fully imported. DB verified: 2,199 synthetic Qs across 7 source banks. Domain I: 2,728, Domain III: 887.

**Full recovery complete (2026-05-30, verified 2026-06-02):** The database holds **7,567 questions** across 17 source banks with **7,567 domain-classified** (100%). Only **35 Qs truly lack answer keys** (down from 670 after the 2026-06-01 audit cleared 635 stale `no_answer_key` flags). Only **2 items remain in quarantine**. Key recovery milestones: 626 Group A Qs recovered from corrupted answer keys, 273 Past ABT PDFs extracted, 466 domain-less Qs classified, 2015 recert exam imported. **Synthetic generation COMPLETE (2026-06-02):** 2,199 synthetic Qs across 7 source banks (IDs 11-17). Domain I: 1,600 Qs (was 1,125), Domain III: 599 Qs (was 287). All verified with answer options, explanations, domain classification.

**Weekly truth audit:** Cron `DABT Weekly Truth Audit` (Sun/Wed/Fri 05:00 UTC) — now script-based. The data gathering (DB coverage, sampling, **phantom completion detection**) runs via `~/.hermes/scripts/dabt-weekly-audit.py` as a `no_agent` script. Check 6 specifically flags if Domain I/III counts are at baseline despite claimed synthetic generation — catches the failure mode where kanban tasks are marked done but data never landed. The LLM only handles reference verification and report synthesis with a minimal prompt. Check latest output for new discrepancies.

## Schema (7 tables)
Core tables: `source_files`, `questions` (id TEXT PK, question_text, correct_answer_letter, explanation, source_file_id, bloom_level), `answer_options` (question_id, option_letter, option_text), `question_topics` (question_id, topic), `question_domains` (question_id, domain I-IV, sub_domain, task), `match_pairs` (term, match_answer), `quarantine` (rejected items). Full DDL in `references/schema.md`.

**⚠️ Domain is NOT in the `questions` table.** Join `question_domains` to get domain info:
```sql
SELECT q.*, qd.domain, qd.sub_domain 
FROM questions q 
JOIN question_domains qd ON q.id = qd.question_id 
WHERE qd.domain = 'Domain III';
```
Questions without a `question_domains` entry are unclassified. As of 2026-06-01, all 5,368 questions have domain classifications.

## Domain Distribution
DB is structurally skewed (56.4% Applied vs 38% exam weight for Risk Assessment). **DO NOT use raw DB proportions.** Use `config['drill_config']['target_distribution_per_10']` for sampling. 

**Current domain counts (as of 2026-06-02):**
- Domain I (Study Design | 36% exam weight): **2,728 Qs** (36.1%) ✅ at target
- Domain II (Mechanistic | 13% exam weight): **929 Qs** (12.3%) — near target
- Domain III (Risk Assessment | 38% exam weight): **887 Qs** (11.7%) — improved from 5.4% with 599 synthetic Qs
- Domain IV (Applied | 13% exam weight): **3,026 Qs** (40.0%) — still overweight
- Unclassified: **0 Qs** ✅

Synthetic Qs added 1,600 to Domain I and 599 to Domain III on 2026-06-02. Domain IV is still overweight and should be sampled sparingly to reflect exam proportion.

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
3. **Pre-register source banks** in `source_files` table before workers start — prevents duplicate/conflicting IDs. Assign source_file_id = MAX(id)+1 for each sub-domain.
4. Delegate parallel batches of 50 Qs to subagents, each with source chapter in context
5. Each batch writes: question, 4 options, correct answer, explanation (3-5 lines), source citation, bloom level, format
6. Validate within each batch (structural + distribution)
7. **Save batch JSON to disk** (e.g., `batches/synthetic_domain_i_batch_N.json`) — do NOT go directly to DB
8. **Verify JSON file**: count records, check structure, confirm expected format
9. Import verified JSON to DB (INSERT into questions + answer_options + question_domains + question_topics)
10. **Post-import verification** (MANDATORY — see `dabt-project-workflow` → Post-Import Verification Protocol):
    - `SELECT COUNT(*) FROM questions WHERE source_file_id = N` — must match expected
    - `SELECT domain, COUNT(*) ... WHERE source_file_id = N GROUP BY domain` — must match expected distribution
11. **Only after verification passes**: mark kanban task done, update skill description, update task-roadmap
12. Post-generation audit (10% sample verified against reference)

### Kanban Card Body Template (for synthetic generation cards)
Each card body should include:
- **Target count** (exact number of questions)
- **Source material** (chapters, page ranges, key constants)
- **Generation rules** (citation, format distribution, bloom targets)
- **Workflow steps** (file-based intermediate → verify → import → verify DB)
- **DONE CRITERIA** (explicit verification queries that must pass before marking done)

Example DONE CRITERIA block:
```
## DONE CRITERIA
1. All JSON batch files exist at batches/synthetic/domain_*_batch_*.json
2. Total records in JSON files = [TARGET]
3. Records imported to DB (SELECT COUNT confirms [TARGET])
4. Domain classification verified (question_domains shows correct domain)
5. Orchestrator confirms DB state matches task spec
```

### No-Answer-Key Question Type
For real exam PDFs without published answer keys (Past ABT PDFs, 2017 cert):
- Add to DB with `correct_answer_letter = NULL`
- Set `no_answer_key = 1` (column exists in the questions table — do NOT use `synthetic_source` which doesn't exist in the schema)
- These become discussion prompts — when encountered during drilling they trigger review conversation rather than scoring

### Coverage Tracking via Curriculum Structure
The curriculum section in dabt-config.json (after absorption) provides:
- Prerequisite ordering — Domain I → Domain III. Checks whether the user has foundations before advanced topics.
- Topic checklists — e.g. 4/14 Domain IV topics covered, 5/11 organ systems drilled
- Cross-references progress/state.json by_topic against curriculum topic lists

After curriculum absorption into config, patch dabt-drill-mode to read topic lists from the config curriculum section for coverage reporting.

## Data Quality Policy
Issues → quarantine with documented label. Do NOT leave NULL/missing markers in main table. Main table must always produce valid questions with no quality filter. File path and absolute state path: `CONFIG['database']['primary']['path']` and `CONFIG['progress']['state_path']`.

**Null-answer landscape (as of 2026-06-02):** 35 Qs across 3 sources with `no_answer_key=1` — Past ABT PDFs, 2017 Cert Exam, 2015 Recert Exam. Down from 670 after batch answer-fixing campaign and audit.

**Domain III explanation gap:** 95/287 Domain III questions (33%) lack explanations. These are mostly risk assessment topics (dose-response, hazard ID, risk characterization). Enrichment requires referencing Casarett & Doull Ch.4, Hayes Ch.3/10, and EPA guidelines. Best handled in batches during study sessions.

**Current state (2026-06-02):** All recovery work complete. 35 Qs legitimately lack answer keys (not a quality defect — real exam materials without published keys). All 7,567 questions have domain classifications. Bloom levels present on 7,050/7,567 (93.2%). Synthetic generation complete: 2,199 Qs added. Cron audit runs Sun/Wed/Fri.
