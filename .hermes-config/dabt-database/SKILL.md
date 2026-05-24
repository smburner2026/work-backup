---
name: dabt-database
description: "Query the expanded DABT Practice Questions Database (4,841+ questions across 8 source banks — replaces the old 446-Q xlsx with a SQLite relational db). SQLite-based selection with domain/topic/source indexing, blueprint-weighted sampling, anti-clustering, dedup tracking. Legacy xlsx still available at reference/data/DABT_Practice_Questions_Database.xlsx."
category: education
---

# DABT Practice Questions Database (SQLite)

## Session Start

Before any query, load `education/dabt-project-workflow` and read the project config (`dabt-config.json`). The DB path and exam weight distribution MUST come from the config — the unified config is alive (materialized 2026-05-20). No fallback needed.

**✅ Quarantine complete (2026-05-20):** 1,048 low-quality/broken questions moved to `quarantine` and `quarantine_answer_options` tables. Main table is now 100% clean: all 3,793 questions have valid answer letters matching existing 4–5 options. See `references/answer-recovery-campaign.md#quarantine` for the full breakdown.

Three quarantine categories:
- **Group A (broken, 626):** No answer letter, no answer options, answer letter doesn't match options, or non-standard answer letters (I–Q). Cannot be drilled.
- **Group B (non-standard formats, 422):** Option counts not 4–5. May be salvageable but not compatible with standard drill pipeline.
- **Past ABT PDFs (273):** Real exam questions without published answer keys — placed in quarantine rather than left as NULL in main table. Requires SME review for recovery.

The quarantine tables preserve all original data (question text, options, explanations) with a `q_issue` column documenting the specific defect. To restore any question: `INSERT INTO questions SELECT * FROM quarantine WHERE id = ?` and migrate its options.

**🔄 Automated truth audit:** A weekly cron job (`DABT Weekly Truth Audit`, job_id: `2a16ef8310c5`) runs every Sunday at 5:00 AM UTC. It compares DB quality metrics against `dabt-config.json` baselines, samples 5 questions for reference-text cross-verification, and flags new content issues. The cron loads `dabt-database` + `dabt-reference` + `batch-data-enrichment` skills and delivers compact deltas-only reports to origin. The inaugural audit report is at `references/truth-audit-2026-05-19.md`; the cron definition is snapshotted in the work repo at `.hermes-snapshots/cron/dabt-weekly-truth-audit.md`. When running any DB query this session, first check the cron's latest output if available — it may have flagged new discrepancies since the last skill patch.

**⚠️ Data quality policy:** When data quality issues are found (answer mismatches, broken formats, missing fields), **quarantine physically** — move to quarantine tables with a documented issue label. Do NOT leave NULL/missing markers in the main table that could silently corrupt drills. The main table must always be clean enough that a drill query with no quality filter produces valid questions. This policy was established by user directive on 2026-05-20.

## Database Location

### Primary (new, expanded)

The canonical database path is defined in `/root/work/dabt/dabt-tutor/dabt-config.json`:

```python
import json, sqlite3

with open('/root/work/dabt/dabt-tutor/dabt-config.json') as f:
    CONFIG = json.load(f)

DB_PATH = CONFIG['database']['primary']['path']  # Resolves relative to workdir
# Absolute: /root/work/dabt/dabt-tutor/reference/data/dabt.db
conn = sqlite3.connect(f"{CONFIG['project']['workdir']}/{DB_PATH}")
```

Relational schema with **4,841 questions** (see `dabt-config.json` → `database.primary.total_questions`) from 7 source banks (see `dabt-config.json` → `database.primary.source_banks`):

- **Mini-ABT 1-11** (446 Qs) — original, from the legacy xlsx
- **2000Q Question Bank** (~1,801 Qs) — chapter-based general tox
- **Chapter Tests** (~1,119 Qs) — C&D organ system tests
- **Kristen Mini Exams** (~208 Qs, deduped) — comprehensive practice
- **Kristen Topic Tests** (~145 Qs, deduped) — topic-specific
- **Past ABT Exams 2008-2014** (~767 Qs) — compiled recert questions
- **Past ABT Exam PDFs** (~355 Qs) — 2012-2017 real exams

**Domain distribution of the DB is structurally skewed** — see `dabt-config.json` → `exam_blueprint.domains` for the authoritative exam weights vs DB distribution. Always use the config's `drill_config.target_distribution_per_10` for question sampling, not the DB's natural proportions.

### Legacy (backward compat)

```python
DB_PATH_LEGACY = '/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx'
df = pd.read_excel(DB_PATH_LEGACY, sheet_name='Questions')  # 446 Qs only
```

## SQLite Schema

```sql
-- Source files (banks)
CREATE TABLE source_files (
    id INTEGER PRIMARY KEY,
    bank_name TEXT NOT NULL,
    filename TEXT,
    format_type TEXT,       -- "chapter-based", "topic-based", "comprehensive", "real-exam"
    year TEXT,
    description TEXT
);

-- Questions
CREATE TABLE questions (
    id TEXT PRIMARY KEY,              -- DABT-0001 to DABT-XXXX
    question_text TEXT NOT NULL,
    correct_answer_letter TEXT,
    correct_answer_text TEXT,
    explanation TEXT,
    source_file_id INTEGER,
    question_number_in_source INTEGER,
    bloom_level TEXT,
    FOREIGN KEY (source_file_id) REFERENCES source_files(id)
);

-- Answer options (1:M)
CREATE TABLE answer_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    option_letter TEXT NOT NULL,
    option_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Topic tags (M:M)
CREATE TABLE question_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Domain classification
CREATE TABLE question_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    domain TEXT NOT NULL,         -- "Domain I" through "Domain IV"
    sub_domain TEXT,
    task TEXT,
    confidence TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Matching test pairs
CREATE TABLE match_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    term TEXT NOT NULL,
    match_answer TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE INDEX idx_q_domain ON question_domains(domain);
CREATE INDEX idx_q_topic ON question_topics(topic);
CREATE INDEX idx_q_source ON questions(source_file_id);
```

## Query Patterns

### Load the Database

```python
import sqlite3, pandas as pd

conn = sqlite3.connect('/root/work/dabt/dabt-tutor/reference/data/dabt.db')

# Load all questions with their topics and domains
df = pd.read_sql("""
    SELECT q.*, t.topic, d.domain, d.sub_domain, d.task
    FROM questions q
    LEFT JOIN question_topics t ON q.id = t.question_id
    LEFT JOIN question_domains d ON q.id = d.question_id
""", conn)

# Or load as a flat table with options
df_full = pd.read_sql("""
    SELECT q.id, q.question_text, q.correct_answer_letter,
           a.option_letter, a.option_text
    FROM questions q
    JOIN answer_options a ON q.id = a.question_id
""", conn)
```

### Filter by Topic

```python
topic_df = pd.read_sql("""
    SELECT q.* FROM questions q
    JOIN question_topics t ON q.id = t.question_id
    WHERE t.topic = 'Metals & Metalloids'
""", conn)
```

### Blueprint-Weighted Sampling with Anti-Clustering

**IMPORTANT — domain weight correction:** DB distribution does NOT match exam weights. All authoritative values live in `dabt-config.json`:
- Exam blueprint weights → `config['exam_blueprint']['domains']`
- Drill target distribution → `config['drill_config']['target_distribution_per_10']`
- Domain III depletion warning → `config['drill_config']['domain_iii_conservation']['warning_threshold']`

```python
import json, sqlite3, random

with open('/root/work/dabt/dabt-tutor/dabt-config.json') as f:
    CONFIG = json.load(f)

WORKDIR = CONFIG['project']['workdir']
DB_PATH = f"{WORKDIR}/{CONFIG['database']['primary']['path']}"
conn = sqlite3.connect(DB_PATH)

# Load target distribution from config
TARGET = CONFIG['drill_config']['target_distribution_per_10']
# Result: {'Domain III': 4, 'Domain I': 4, 'Domain II': 1, 'Domain IV': 1}

state = json.load(open(f"{WORKDIR}/{CONFIG['progress']['state_path']}"))
asked = set(state.get('asked_question_ids', []))

def sample_by_exam_weight(n=5, asked_ids=set()):
    """Sample questions weighted by exam domain proportion from dabt-config.json."""
    # Scale target distribution to requested set size
    if n <= 5:
        weights = {'Domain III': 2, 'Domain I': 2, 'Domain II': 1, 'Domain IV': 0}
    else:
        weights = {'Domain III': max(1, int(n * 0.38)),
                   'Domain I': max(1, int(n * 0.36)),
                   'Domain II': max(0, int(n * 0.13)),
                   'Domain IV': max(0, int(n * 0.13))}

    result = []
    for domain, count in weights.items():
        if count == 0:
            continue
        placeholders = ','.join('?' * len(asked_ids)) if asked_ids else 'NULL'
        query = f"""
            SELECT q.*, COALESCE(d.sub_domain, ''), COALESCE(d.task, '')
            FROM questions q
            JOIN question_domains d ON q.id = d.question_id
            WHERE d.domain = ?
            AND q.id NOT IN ({placeholders})
            ORDER BY RANDOM() LIMIT ?
        """
        params = [domain] + list(asked_ids) + [count]
        rows = conn.execute(query, params).fetchall()
        result.extend(rows)
    return result


def sample_from_domain(domain, n, asked_ids, exclude_sources=None):
    """Sample n questions from a specific domain, excluding already-asked IDs."""
    placeholders = ','.join('?' * len(asked_ids)) if asked_ids else 'NULL'
    source_filter = ""
    if exclude_sources:
        source_filter = "AND q.source_file_id NOT IN ({})".format(
            ','.join(map(str, exclude_sources))
        )
    query = f"""
        SELECT q.* FROM questions q
        JOIN question_domains d ON q.id = d.question_id
        WHERE d.domain = ?
        AND q.id NOT IN ({placeholders})
        {source_filter}
        ORDER BY RANDOM() LIMIT ?
    """
    params = [domain] + list(asked_ids) + [n]
    return conn.execute(query, params).fetchall()


def domain_iii_depletion_check():
    """Check remaining Domain III questions against config threshold."""
    threshold = CONFIG['drill_config']['domain_iii_conservation']['warning_threshold']
    state = json.load(open(f"{WORKDIR}/{CONFIG['progress']['state_path']}"))
    asked = set(state.get('asked_question_ids', []))
    placeholders = ','.join('?' * len(asked)) if asked else 'NULL'
    remaining = conn.execute(f"""
        SELECT COUNT(*) FROM questions q
        JOIN question_domains d ON q.id = d.question_id
        WHERE d.domain = 'Domain III'
        AND q.id NOT IN ({placeholders})
    """, list(asked) if asked else []).fetchone()[0]
    if remaining <= threshold:
        return {'depleted': True, 'remaining': remaining, 'threshold': threshold,
                'supplemental': CONFIG['drill_config']['domain_iii_conservation']['supplemental_textbooks']}
    return {'depleted': False, 'remaining': remaining}
```

### Match Pairs (for matching test questions)

```python
# Get matching pairs for a question
pairs = pd.read_sql("""
    SELECT term, match_answer FROM match_pairs
    WHERE question_id = 'DABT-XXXX'
    ORDER BY id
""", conn)
```

## Explanation Generation

Two protocols exist depending on scale:

### Small batches (<100 questions)
Use `references/batch-explanation-workflow.md` for the original repeatable pipeline. Covers: fetching question data from the DB, crafting 2-4 sentence explanations with mechanism, distractor traps, and source citations, saving structured JSON, and self-review verification.

### Full-database pass (100–901 questions)
Use `references/explanation-generation-protocol.md` for the parallel subagent approach. Strategy:
- Pre-export all questions needing explanations into source-based JSON slices
- Dispatch each slice as a `delegate_task` subagent with the approved template in context
- Subagents process batches of 20-30, write UPDATE queries directly to the DB
- Verify coverage post-generation; fix corrupt placeholders (single letters, page refs)

**User-approved explanation template (2026-05-20):**
```
**Answer: X** — [1 sentence: mechanism/rationale]
**Why not the others:** [1-2 sentences on the most seductive distractor]
**Exam tip:** [Optional — 1 sentence: memory hook or exam trick]
**Source:** [Textbook reference]
```

Template rules: 3-4 lines max, mechanism-anchored (WHY not WHAT), distractor trap explains the reasoning error, exam tip only when there's a genuine hook, source references use standard abbreviations (C&D, Hayes, EPA, ICH, OECD, Goldfrank's).

### Structural Quirk: Matching-Type Single-Option Questions

Some questions from the 2000Q Bank (source_file_id=2) have only **one entry** in the `answer_options` table — just the correct answer letter and its text. These originated from matching-test format (column A = chemical/term, column B = effect/association). **Do NOT assume the stored pairing is correct.** Across all batches examined, >90% of these single-option matching items have the wrong association stored. Always reconstruct the correct association from Casarett & Doull reference texts.

Detection query:
```sql
SELECT q.id, q.question_text, q.correct_answer_letter, a.option_text
FROM questions q
JOIN answer_options a ON q.id = a.question_id
WHERE q.source_file_id = 2
GROUP BY q.id
HAVING COUNT(a.id) = 1;
```

When writing explanations for these, format the explanation as: "The DB-stated match is X → Y (a likely data error in the database). **Correct association: X → Z**..."

**Circular permutation pattern found in batch19 (DABT-1159–1166):** All 8 matching-test chemicals from the 2000Q Bank's pesticide classification matching set are mispaired such that each chemical's stored match is the correct class of ANOTHER chemical in the set (a +1 or -1 shift during extraction). For example, carbofuran (correct: carbamate) is stored as "pyrethroid" — which is the correct class of fenvalerate, while fenvalerate is stored as "chlorphenoxy" — the correct class of 2,4,5-T. This pattern repeats through all 8 items. **Recommendation:** When you encounter a batch of single-option matching questions from source_file_id=2 that all concern the same topic (e.g., all pesticides), check for circular permutation before treating individual pairs as independent errors. If the permuted pairings form a closed loop, the entire matching set was shifted by one position during import and no individual DB answer among them is reliable.

**NEW sub-pattern: Multi-position Column Shift (batch29, DABT-1657-1665):** 9 food/microbial toxin matching items from source_file_id=2 follow a different corruption pattern than prior batches:
- Unlike batch19 (circular permutation, every chemical's stored match is another's correct class), batch29 shows **neither circular permutation nor random assignment**
- The correct matches for items like ciguatera→dinoflagellates, rennet→enzyme, patulin→apple products, and scombroid→mahimahi **all exist as option_text values in the database** but are assigned to the wrong question IDs entirely
- For example, DABT-1660 (emetic toxin → "enzyme") — emetic toxin (cereulide) is NOT an enzyme, but rennet IS an enzyme. DABT-1664 (rennet → "dinoflagellates") — rennet is NOT dinoflagellate-related, but ciguatera IS caused by dinoflagellates. This suggests a **multi-position offset** during extraction rather than the +1 shift seen in batch19.
- Only 1/9 stored associations is correct (DABT-1659: endotoxin → gram-negative bacterial toxin)
- Unlike batch28 (letter-only, zero option text), all 9 batch29 matching items have both letter and text stored — just the wrong text.

**THIRD sub-pattern: Non-uniform Offset within a Bounded Range (batch30, DABT-1691-1697):** 7 analytical technique matching items from source_file_id=2 follow a different corruption pattern:
- Unlike batch19 (circular permutation), batch29 (multi-position offset), or batch28 (random misassignment), batch30's pattern has the **end items correct** and the **middle 5 systematically wrong**
- Spot test (DABT-1691, position 1/7) → correctly stored as "nonquantitative screening" ✓
- Spectrochemical (DABT-1697, position 7/7) → correctly stored as "detector adds/removes protons" ✓
- DABT-1692 through DABT-1696: all wrong, but with inconsistent letter offsets (-2, -4, -2, +3) — suggesting a manual data-entry error affecting those specific rows rather than a systematic extraction shift.
- This is the **first documented pattern where some items in a matching set are correct** — earlier patterns had 0/7 to 1/9 correct
**Consolidated pattern summary:**

| Batch | Pattern | Correct Ratio | Sub-type |
|-------|---------|---------------|----------|
| batch7 (antidotes) | correct_answer_text wrong, letter right | 0/17 text | Column B text from display line, not answer key |
| batch19 (pesticides) | Circular permutation (+1 shift) | 0/8 | Every chemical's stored class is the next chemical's true class |
| batch28 (neuropharm) | Random misassignment + letter-only | 0/7 text, 8/8 text-zero | Both text and letter scrambled; 8 items with letter only, zero option text |
| batch29 (food toxins) | Multi-position column shift | 1/9 | Correct matches exist in DB but assigned to wrong IDs; text retained but displaced |
| **batch30 (analytical tox)** | **Non-uniform offset (middle 5 of 7)** | **2/7** | **End items (spot test, spectrochemical) correct; 5 middle items systematically wrong with inconsistent offsets — NOT a circular permutation. See `references/batch30-analytical-tox-errors.md`.** |
| **batch31 (industrial gases)** | **Correct letter, wrong display-line text (same pattern as batch7 antidotes)** | **7/7 text wrong** | **Column B text from display line, not the definition of the correct answer letter. Gas matching test from 2000Q Ch33 Occupational Toxicology docx. See `references/batch-explanation-workflow.md` for the full letter-to-definition mapping.** |
- The letter MAY be the correct answer (if the answer-key parsing partially succeeded)
- But the letter is UNVERIFIABLE without option text
- In batch28, the 7 preceding items (DABT-1593-1599) all had WORNG stored associations from the same test → these 8 are also suspect
- **Write explanations describing the term's ACTUAL pharmacological mechanism**, ignoring the stored letter entirely. Reference standard pharmacology (Goodman & Gilman or Casarett Ch.9). Example: "Tecadenoson is a selective A1 adenosine receptor agonist used for PSVT."

Detection query:
```sql
-- Find items with correct_answer_letter but zero option rows
SELECT q.id, q.question_text, q.correct_answer_letter
FROM questions q
LEFT JOIN answer_options a ON q.id = a.question_id
WHERE q.source_file_id = 2
  AND q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
GROUP BY q.id
HAVING COUNT(a.id) = 0;
```

## Adding User-Contributed Questions

TempMoon/Mike regularly contributes questions from study sessions. When asked "add this question":

### Workflow

1. **Verify the answer** against reference texts (Casarett & Doull, Hayes) before inserting. Use `dabt-reference` three-pass search. Do NOT trust the user's claimed answer if it contradicts reference — flag the discrepancy and let the user judge.
2. **Assign the next ID**: `SELECT MAX(CAST(SUBSTR(id,6) AS INTEGER)) FROM questions;` then increment (e.g., DABT-4628 → DABT-4629).
3. **Find the next answer_options autoincrement**: `SELECT MAX(id) FROM answer_options;` — insert options starting at MAX+1.
4. **Insert into 4 tables**:

```sql
-- Questions (source_file_id=8 for User-Contributed)
INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, bloom_level)
VALUES ('DABT-XXXX', 'question text', 'A', 'full answer text', 'explanation with source citation', 8, 'Remember/Understand');

-- Answer options (4-5 standard)
INSERT INTO answer_options (id, question_id, option_letter, option_text) VALUES
  (N,   'DABT-XXXX', 'A', 'option A text'),
  (N+1, 'DABT-XXXX', 'B', 'option B text'),
  (N+2, 'DABT-XXXX', 'C', 'option C text'),
  (N+3, 'DABT-XXXX', 'D', 'option D text');

-- Topics (1-2 relevant topic tags)
INSERT INTO question_topics (question_id, topic) VALUES
  ('DABT-XXXX', 'Relevant Topic'),
  ('DABT-XXXX', 'Second Topic');

-- Domain classification
INSERT INTO question_domains (question_id, domain, confidence) VALUES
  ('DABT-XXXX', 'Domain II', 'tool');
```

### Domain Assignment Guide

| Topic area | Domain | Typical topics |
|-----------|--------|----------------|
| Carcinogenesis, mutagenesis, genotoxicity | Domain II | Carcinogenesis & Mutagenesis, Genotoxicity / DNA Damage |
| ADME, biotransformation, toxicokinetics | Domain I or II | Biotransformation, ADME |
| Organ system toxicity (liver, kidney, neuro) | Domain IV | Hepatotoxicity, Nephrotoxicity, Neurotoxicology |
| Risk assessment, dose-response | Domain III | Risk Assessment, Dose-Response |
| Clinical toxicology, overdose management | Domain IV | Clinical Toxicology / Overdose Management |
| Study design, statistics, regulatory | Domain I | Study Design, Regulatory Toxicology |

### Pitfalls

- The `explanation` field must escape single quotes with two single quotes (`''`) in SQL.
- The topic tags come from existing vocabulary in `question_topics.topic` — use `SELECT DISTINCT topic FROM question_topics ORDER BY topic;` to check available tags.
- The bloom_level is typically `'Remember/Understand'` for new user-contributed questions unless the question explicitly tests higher-order reasoning (apply/analyze).
- After inserting, verify all 4 tables with SELECT queries before confirming completion.

## Known DB Error Patterns Per Organ System

The 2000Q Bank (source_file_id=2) has systematic answer key extraction errors that vary by organ system. Before writing explanations for any new batch, check the relevant reference file:

| Organ System | Reference File | Key Issues |
|-------------|---------------|------------|
| General tox / Chapter 1 | `references/batch-explanation-workflow.md` (DB Verification section) | 21+ known errors; docx cross-reference required |
| Antidotes Matching | `references/batch-explanation-workflow.md` (Antidotes Matching section) | correct_answer_text is WRONG for all items |
| General Principles Matching | `references/batch-explanation-workflow.md` (General-Principles section) | Letter-to-definition mapping scrambled for 10 items |
| Hematology | `references/batch-explanation-workflow.md` (Hematology section) | 3 confirmed errors in DB answer keys |
| Immunotoxicology | `references/batch-explanation-workflow.md` (Immunotoxicology pitfall) | "EXCEPT" questions reversed; letter E errors |
| Liver/Hepatotoxicity | `references/batch-explanation-workflow.md` (Liver zonation pitfall) | Zone assignments systematically shifted by 1 zone |
| **Renal** | **`references/batch11-renal-errors.md`** | **8+ DB errors in renal physiology; 6 E answers; 2 data quality issues** |
| **Lung / Pulmonary (Domain IV)** | **`references/batch12-lung-errors.md`** | **24 DB errors in 50 questions (48%); 9 E answers; 15 wrong-standard-answer; 5 scrambled matching items** |
| **Neurotoxicology (Domain IV)** | **`references/batch13-neuro-errors.md`** | **29 DB errors in 50 questions (58%); 8 E answers (6 valid, 2 invalid); 21 wrong-standard-answer; 3 scrambled matching items; 100% error on MPTP/dopamine subtopic** |
| **Ocular Toxicity (Domain IV)** | **`references/batch14-ocular-skin-errors.md`** | **6 DB errors in 27 questions (22%)** — surfactant damage order reversed, lens anatomy false statement misattributed, ethambutol/isoniazid swap, fluorescein replaced by hypertonic saline, occipital/temporal lobe swap for vision, strong acids instead of strong bases as most cornea-damaging; also 4 matching items with correct pairings but single-option-only DB storage; 1 question with zero stored options (DABT-0962) |
| **Skin / Dermatotoxicity (Domain IV)** | **`references/batch14-ocular-skin-errors.md`** + **`references/batch16-reproductive-skin-errors.md`** | **14 DB errors across 32 questions (44%)** — batch14: 1 error (high-MW hydrophobic as best penetrant vs 500 Da rule). batch16: 13 errors in 26 questions (50%): 2 letter-E corruptions, 6 wrong-standard-answers, 4 scrambled matching items, 1 text corruption. All 4 matching items (DABT-0991-0994) are toxicologically wrong. |
| **Reproductive & Developmental Toxicity (Domain IV)** | **`references/batch16-reproductive-skin-errors.md`** | **11 DB errors in 24 questions (46%)** — 5 letter-E corruptions (DABT-0995, 1011, 1012, 1013, 1015), 6 wrong-standard-answers (puberty staging → cortisol, TCDD classified as non-EDC, uterine weight cycle-variation called false, linuron labeled estrogen antagonist, p,p'-DDE excluded from antiandrogens, NSAIDs as ED cause instead of autonomic drugs). |
| **Endocrine + Reproductive (Domain IV, batch17)** | **`references/batch17-endocrine-reproductive-errors.md`** | **14 DB errors in 50 questions (28%)** — 6 letter-E corruptions (DABT-1025, 1033, 1034, 1041, 1053, 1064), 13 wrong-standard-answers including fundamental physiology reversals (dopamine agonist→antagonist, zona glomerulosa→glucocorticoids, pendrin→activin), species differences reversal (humans said to lack TBG when rats actually lack it), neoplasm epidemiology swapped (adrenal→thyroid as most common, RET→adrenal cortex instead of medullary thyroid). See batch17 file for full table with rationale. |
| **Endocrine Toxicology (Domain IV)** | **`references/batch18-endocrine-pesticide-errors.md`** | **3 confirmed wrong-standard-answers in 24 questions (12.5%)** — DABT-1081 (adrenal adenoma vs pheochromocytoma), DABT-1078 (4 true statements all correct, E as only answer), DABT-1086 (androgen vs estrogen role in thyroid cancer). 1 parsing issue (DABT-1070: all 4 options crammed into option A). 1 zero-options question (DABT-1092). 5 E-answers with only A-D options (mostly plausible as "none of the above"). |
| **Pesticides – Insecticides (Domain IV)** | **`references/batch18-endocrine-pesticide-errors.md`** | **3 confirmed wrong-standard-answers in 26 questions (11.5%)** — DABT-1100 (status epilepticus vs respiratory failure as OP cause of death), DABT-1107 (G6PD vs aconitase for fluoroacetate), DABT-1095 (rotenone vs anticoagulants as most common rodenticide). 5 E-answers with only A-D options. Reference chapter: Casarett & Doull Ch.22. |
| **Pesticides – Insecticides (Domain IV, batch19)** | **`references/batch19-pesticide-errors.md`** | **~28 source discrepancies in 50 questions (56%)** — 11 wrong-standard-answers (Bt toxin→ciguatoxin, intermediate→nicotine syndrome, α-cyano→imidazole for type II pyrethroids, PBO→formamidines, fipronil→Na channel, captan/folpet→urea, fluoroacetate→not rodenticide), **8 matching-test items with circular permutation** (every chemical misclassified with the class of another in the set — sarin as rodenticide, fenvalerate as chlorphenoxy, 2,4,5-T as bipyridyl, acetochlor as carbamate, carbofuran as pyrethroid, propazine as organochlorine, endrin as dithiocarbamate, thiram as neonicotinoid). 14 E-answers with only A-D options. 5 counterintuitive "except" designations. 2 zero-option questions (nithiazine, benomyl). |
| **Metals & Metalloids (Domain IV)** | **`references/batch20-metals-errors.md`** | **~10 source discrepancies in 50 questions (20%)** — 7 wrong-standard-answers (acrodynia→arsenic vs mercury, fluorosis→liver/kidney vs teeth/bones, selenium→peripheral neuropathy vs cardiomyopathy, bromine→metalloid vs halogen, etc.), 7 E-answers with only A-D options (3 invalid — DABT-1195, 1217, 1218), 2 zero-option questions (DABT-1169, 1170 — single-word from 2000Q Bank). Notable patterns: source key contradicts same-reference-chapter on basic facts (acrodynia in Ch.23 says mercury, answer key says arsenic). |
| **Solvents & Hydrocarbons (Domain IV), batch21** | **`references/batch21-solvents-errors.md`** | **5 wrong-standard-answers in 15 questions (33%)** — CYP2E1 inducer error (acetone DENIED as inducer, DABT-1254), TCE cancer endpoint swap (astrocytoma → should be renal cell carcinoma, DABT-1257), methylene chloride metabolic feature reversed (auto-inducing → CO production, DABT-1258), jet fuel composition error (ethers → hydrocarbon mixtures, DABT-1261), ambiguous CS₂/disulfiram direction (DABT-1262). 4 letter-E corruptions (DABT-1256, 1259, 1260, 1262) — mostly fixable as option B/D. Reference chapter: Casarett & Doull Ch. 24. |
| **Solvents & Hydrocarbons (Domain IV), batch22** | **`references/batch22-solvents-errors.md`** | **7 wrong-standard-answers in 50 questions (14%)** — toluene target organ (lung→CNS), benzene cancer (RCC→AML), cyclic ether (dioxin→dioxane), xylene/toluene dermal abs (B→A), acrylamide effects inverted, p-aminophenol biomarker (toluene→aniline), VOC in water (CCl₄→CHCl₃). 6 letter-E corruptions (DABT-1271, 1274, 1278, 1299, 1305, 1312). 1 scrambled matching item (benzidine→inorganic lung carcinogen). Plus 2 additional wrong-answers found during detailed review (chloroform metabolite, vinyl chloride effects). Reference chapter: Casarett & Doull Ch. 24. |
| **Solvents Matching / Radiation / Plant Toxins (batch23)** | **`references/batch23-solvents-radiation-plant-errors.md`** | **~23 errors in 50 questions (~46%)** — 6 matching-item circular permutation (100% wrong in DB), 7+ radiation errors (stable isotope called gamma emitter, visible-range beta wavelength, non-radioactive elements as terrestrial sources), 10+ plant toxin errors (ricin MOA, poison ivy allergen, mad honey toxin, cascara use, locoweed toxin swapped with domoic acid, Datura mechanism opposite — all fundamental). **Plant Toxins has the highest error rate of any reviewed organ system at 50%.** |
| **Plant Toxins (Domain IV), batch24** | **`references/batch24-plant-toxins-errors.md`** | **~13 wrong-standard-answers in 50 questions (26%)** — fundamental plant tox facts reversed (ricin→lily of valley vs castor bean, solanine denied in Solanaceae, aconitine cardiotoxicity denied, aflatoxin→pneumonia vs hepatocarcinogen, bracken fern denied as carcinogen, ergotism→false morels vs Claviceps). **9 letter-E corruptions** (5 demonstrably wrong — linamarin, oxalate, mushroom genera, carcinogens, alkaloid definition). **3 foundational classification Qs (alkaloids, terpenes, glycosides definitions): 2/3 wrong.** All "except" questions designate TRUE statements as exception (batch9 pattern). All verifiable against single source: Casarett & Doull Ch.26. |
| **Plant Toxins (Domain IV), batch25** | **`references/batch25-air-pollution-errors.md`** (Plant Toxins section) | **8 of 9 matching-test items have wrong stored associations** (DABT-1424-1431) — same single-option storage pattern as prior batch matching items. NOT a circular permutation (unlike batch19); appears to be random column misalignment during extraction. DABT-1432 (rhubarb) had **null correct_answer_text** — filled from toxicology as "soluble oxalate." The 5 standard MCQs (DABT-1419-1423) are correct. |
| **Air Pollution & Particulates (Domain IV, batch25)** | **`references/batch25-air-pollution-errors.md`** (Air Pollution section) | **FIRST Air Pollution batch processed. Zero discrepancies found (0/36).** Unusual for source_file_id=2: all 36 Qs have full 4-option sets, no letter-E corruptions, no zero-option questions. 14 "all except" questions all correctly identify the false statement. This may indicate Air Pollution questions were extracted from a cleaner sub-source within the 2000Q Bank. |
| **Neuropharmacology / Drug Mechanism Matching (Domain II, batch28)** | **`references/batch28-neuropharm-food-errors.md`** | **7/7 matching-item stored associations are wrong (100%)** — muscimol→serotonin agonist (should be GABA-A), clonidine→NET inhibitor (should be α₂ agonist), baclofen→nicotine antagonist (should be GABA-B agonist), bicuculline→dopamine agonist (should be GABA-A antagonist), theophylline→serotonin antagonist (should be PDE inhibitor), nicotine→GABA-A agonist (should be nAChR agonist), clozapine→GABA-A agonist (should be D₄/5-HT₂A antagonist). **NEW sub-pattern: 8 items with correct_answer_letter but ZERO stored option text** (DABT-1600-1607). Unlike circular permutation (batch19), these seem randomly misassigned. |
| **Food Safety (Domain IV, batch28)** | **`references/batch28-neuropharm-food-errors.md`** (Food Safety section) | **SECOND clean sub-source from source_file_id=2 (0/11 discrepancies).** All 11 Qs have full 4-option sets, correct answer letters, and no parsing issues. Topics: food contamination, GRAS, color additives, preservatives, sweeteners, antimicrobials. Consistent with Air Pollution (batch25) as likely separately-extracted with better QC. |
| **Cell Death & Toxicity Mechanisms (Domain II, batch28)** | **`references/batch28-neuropharm-food-errors.md`** | **~8% error rate (2/24 ambiguous).** DABT-1570: letter-E import corruption (4 options A-D, answer letter E). DABT-1580: "act locally" vs "specialized organs" ambiguity for cytokines. DABT-1590: ADH blocking stored as mercury mechanism (should be cystine-mimicry uptake). Remaining 21 Qs are correct (necrosis, apoptosis, signaling, fibrogenesis, cellular stress, Fenton chemistry). |
| **Mechanistic Toxicology (Domain II, batch27)** | **`references/batch27-mechanistic-tox-errors.md`** | **~12% error rate (6/50).** 4 wrong-standard-answers (DABT-1528 receptor agonist pair reversal, DABT-1529 merged-option parsing error, DABT-1559 HMG-CoA reductase→thioredoxin reductase, DABT-1568 glutathione false-statement ambiguity). 5 E-answer corruptions. 1 parsing issue (merged options). Generally higher quality than Domain IV organ-system batches from same source. Reference: Casarett & Doull Ch.3. |
| **Food Safety / Applied Toxicology (Domain IV, batch29)** | **`references/batch29-food-errors.md`** |\n| **Analytical Toxicology / Occupational Exposure (Domain I, batch30)** | **`references/batch30-analytical-tox-errors.md`** | **10% error rate (5/50)** — 5 matching item wrong associations in analytical techniques matching set (DABT-1692–1696). Non-uniform offset pattern: end items correct (spot test, spectrochemical), middle 5 systematically wrong with inconsistent offsets (NOT circular permutation). All 43 standard MCQs are correct. Reference: Casarett & Doull Ch.31 (Analytic/Forensic Toxicology). |
| **ADME/Toxicokinetics (Domain I, batch32)** | **`references/batch32-adme-biotransformation-errors.md`** | **~30% error rate (15/50)** — 7 physiological reversals (DES vs warfarin, enterohepatic cycling vs well-stirred effect, bile:plasma ratio, cardiac output distribution, TCDD excretion route, plasma protein binding, phenobarbital species). 3 transporter/classification errors. 5 wrong-mechanism. 12 letter-E corruptions. First systematic documentation of Domain I errors from 2000Q Bank. |
| **ADME/Toxicokinetics (Domain I, batch31)** | **See text below** | **22/32 (69%) — HIGHEST error rate found** — Ion trapping direction reversed, kernicterus mechanism wrong, colonic absorption, bone storage, placental transfer (IgG vs heparin), MeHg/methionine mimic, facilitated diffusion exception, P-gp classification/substrates, Fick's law, membrane fluidity, aqueous pores, octanol/water partition (TCDD vs acetic acid), fetal nutrient/toxin transport, BBB transporter energy, neonatal methemoglobinemia. All verified against 2000Q Ch5 ADE docx answer key. |
| **Industrial Gas Matching (Domain I, batch31)** | **See text below** | **7/7 wrong stored text (same batch7 pattern)** — Display-line text stored instead of letter-matched definition. Correct matches: chlorine→water treatment, phosgene→pesticide/welding, ozone→arc welders, EtO→gas sterilization, formaldehyde→furniture, NO₂→agricultural workers, arsine→microelectronics. Verified against 2000Q Ch33 Occupational Toxicology docx answer key. |
| **Biotransformation (Domain II, batch32)** | **`references/batch32-adme-biotransformation-errors.md`** | **~25% error rate (12/50)** — Phase 1 vs 2 reversal, terfenadine/ketoconazole DDI pair, UDPGA/PAPS depletor, nitroreductase location, sulfoxide reduction example, ethanol oxidation pathway. Overlaps with batch27 Mechanistic Toxicology at the margins but focuses on enzyme systems (CYPs, UGTs, SULTs, EH) rather than general cell-death/signaling pathways. |
| **Biotransformation (Domain II, batch33)** | **`references/batch33-biotransformation-errors.md`** | **~82% error rate (41/50) — WORST Domain II batch.** DABT-1800+ range shows a data-quality cliff. 14 "EXCEPT" questions with TRUE statement marked as exception. ALDH2 location, CYP450 location, GST compartment all reversed. CYP450 epoxidation substrates wrong. Enzyme cofactors (molybdenum, UGT count) wrong. E-answer corruptions (6). CYP probe drugs swapped (chlorzoxazone→erythromycin). Quinidine→rifampin swap for CYP2D6 inhibitor. M6G > morphine denied. CYP3A4 cooperativity denied. Check EVERY answer against C&D Ch.6 — do NOT trust DB stored letters in the DABT-1800+ range. |
| **Cardiovascular Toxicity (Domain IV, batch35)** | **`references/batch35-cardiovascular-errors.md`** | **~20% error rate (10/50)** — 7 definite + 3 probable. Key failures: (a) **Antiarrhythmic classification** — Class III stored as Cl⁻ channel blockers (should be K⁺ channel blockers per Vaughan Williams). (b) **Cardiac biomarker confusion** — CK-MM called inflammatory marker (should be CRP), AST called most sensitive for MI (should be troponin). (c) **Hypertrophy/failure distinction blurred** — dilation stored as hypertrophy marker (marks transition to failure). (d) **4 matching-test items with wrong stored associations** (multi-position offset pattern, same as batch29) — homocysteine→hemangiosarcoma, β-amyloid→abortion, CS₂→portal hypertension are all toxicologically incorrect. (e) **Alcoholic cardiomyopathy duration dependency reversed** — DB says unrelated to exposure duration (should be dose- and duration-dependent). |
| **Drug Abuse & Forensic Toxicology (Domain IV, batch36+batch37)** | **`references/batch37-drugs-of-abuse-errors.md`** | **0% error rate (0/96)** — the LARGEST clean 2000Q Bank sub-source. 46 Qs in batch36 (DABT-1973–2018) + 50 Qs in batch37 (DABT-2019–2068) all have correct DB answers: full 4-option sets, correct letters, no E-corruptions, no EXCEPT reversals, no parsing errors. Topics: opioid metabolism (codeine→morphine via CYP2D6, 6-AM as heroin biomarker, normeperidine neurotoxicity, norpropoxyphene cardiotoxicity, methadone→EDDP), cocaine toxicology (cocaethylene, pyrolysis products, esterase metabolism, postmortem redistribution), methamphetamine (pH-dependent excretion, l-isomer in Vicks), methylphenidate (ritalinic acid), GHB (postmortem artifact, date-rape use), benzodiazepines (eszopiclone as non-BZD, oxazepam prodrugs), dissociative anesthetics (PCP NMDA antagonism, ketamine pressor effect), hallucinogens, ethanol, cannabinoids, anabolic steroids. Primary references: C&D Ch.32 (Analytical & Forensic Toxicology), C&D Ch.33 (Clinical Toxicology). |
| **Clinical Toxicology / Overdose Management (Domain IV, batch38)** | **`references/batch38-overdose-management-notes.md`** | **First clinical toxicology batch processed. ~0% apparent error rate (0/50).** Covers: chloroquine/cocaine antidotal mechanisms, APAP/salicylate/NSAID overdose, iron toxicity, vitamin A/D/B6/C toxicity, diabetes drug overdose, antibiotic ADRs, anticoagulant rodenticides, thyroid hormone overdose, antihistamine/decongestant/triptan overdose, topiramate acidosis, CCB overdose. Answers appeared consistent with clinical toxicology knowledge (Goldfrank's Toxicologic Emergencies). **Limitation:** Goldfrank's is NOT present in the extracted reference library — full text-based cross-verification was not possible. All source citations in explanations use Goldfrank's (clinical standard) rather than Casarett & Doull. This is a distinct reference-gap issue: clinical toxicology/overdose management questions are best verified against Goldfrank's, Casarett Ch.33 (Clinical Toxicology), or Casarett Ch.30 (Therapy). |
| **Drugs of Abuse / Forensic Toxicology (Domain IV, batch37)** | **`references/batch37-drugs-of-abuse-errors.md`** | **0% error rate (0/50) — third clean 2000Q Bank sub-source.** All 50 Qs have correct DB answers: no letter-E corruptions, no EXCEPT reversals, no matching-test scrambling, no zero-option questions. Covers opioids, hallucinogens, cannabinoids, stimulants, ethanol, GHB, Kratom, Salvia, anabolic steroids. Reference: C&D Ch.33 (Clinical Toxicology). |

New batches targeting an unlisted organ system should be treated with high suspicion — check the extracted answer keys against the original docx (if available) or against Casarett & Doull reference texts. **Exceptions — four clean 2000Q Bank sub-sources identified so far:** Air Pollution (batch25, 0/36 errors), Food Safety (batch28, 0/11 errors), Drugs of Abuse / Forensic Toxicology (batch36+batch37, 0/96 errors — the largest clean sub-source), **Clinical Toxicology / Overdose Management (batch38, 0/50 errors)**. See `references/batch14-ocular-skin-errors.md` for the full batch 14 findings including verified matching items and format issues.
