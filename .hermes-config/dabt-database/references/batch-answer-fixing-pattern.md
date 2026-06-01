# Batch Null-Answer Fixing Pattern

For questions with `correct_answer_letter = NULL` and `no_answer_key = 1` (real exam materials without published answer keys), use this pattern to determine answers by cross-referencing reference textbooks via parallel subagents.

## When to Use

- Source files with `no_answer_key = 1` (flagged at import time)
- Questions have `answer_options` filled (A-D text) but no recorded correct answer
- Reference texts available for evidence-based determination

## Partition Strategy

Split questions into independent batches by exam part or natural grouping. Each batch goes to a `delegate_task` subagent with terminal+file toolsets.

**Example partition (Source 9, 2017 ABT Cert Exam):**
- Part A: questions with `question_number_in_source LIKE 'A_%'` (~100 Qs)
- Part B: `B_%` (~100 Qs)
- Part C: `C_%` (~100 Qs)
- Part D: `D_%` (~100 Qs)

Each part is an independent subagent — no cross-batch dependencies.

## Subagent Task Template

```
Goal: Determine correct answers for {exam/part} questions by searching reference texts.
       Apply answers directly to the database via sqlite3 UPDATE commands.

Context: 
  - Database: /root/work/dabt/dabt-tutor/reference/data/dabt.db (SQLite)
  - Source file ID: {N}
  - Question range: {ID range}
  - Reference texts:
    - Casarett & Doull chapters: .../casarett-doull-9e/ (36 .txt files)
    - Hayes chapters: .../hayes-7e/ (39 .txt files)
    - ABT handbook: .../extracted/abt-handbook/

Fetch questions with:
  SELECT q.id, q.question_number_in_source, q.question_text,
         group_concat(ao.option_letter || '||' || ao.option_text, '###') as options
  FROM questions q
  JOIN answer_options ao ON q.id = ao.question_id
  WHERE q.source_file_id = {N} AND q.question_number_in_source LIKE '{prefix}_%'
    AND q.correct_answer_letter IS NULL
  GROUP BY q.id ORDER BY q.question_number_in_source;

Apply answers DIRECTLY:
  sqlite3 /root/work/dabt/dabt-tutor/reference/data/dabt.db \
    "UPDATE questions SET correct_answer_letter = 'X' WHERE id = 'DABT-YYYY';"

For each question:
  1. grep the reference texts for keywords
  2. Determine answer from toxicology references
  3. Apply UPDATE

Skip any question you're uncertain about. Better to leave unanswered than answer wrong.
```

## Text Search Pattern

```bash
# Search reference texts for a topic
grep -l "topic keyword" /path/to/casarett-doull-9e/*.txt /path/to/hayes-7e/*.txt

# Read relevant sections
grep -A5 -B2 "keyword" /path/to/chapter.txt
```

## Applying Results

Subagents write UPDATE commands directly to the DB (not to files, since subagent files may not persist to the host filesystem). If a subagent hits max_iterations before applying, save the answers from its summary output and apply manually.

## Remaining Items

After batch processing, some questions may remain:
- **Figure-dependent**: Questions referencing figures/graphs not available as text
- **Calculation-heavy**: Multi-step calculations needing careful verification
- **Truncated options**: Questions where option text wasn't fully stored in DB

These need manual or targeted review — mark them in the task tracker.

## Numbers from 2026-05-31 campaign

- Source 9 (2017 ABT Cert Exam, 4 parts): 401 total → **396 answered** (5 remaining: figures/calculations)
- Source 7 (Past ABT PDFs, mixed clinical+tox): 351 total → **321 answered** (30 remaining: calculations/figures)
- Total: 670 → **35 remaining** (94.8% resolved)
