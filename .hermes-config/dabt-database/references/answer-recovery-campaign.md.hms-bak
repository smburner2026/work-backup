# Answer Letter Recovery Campaign (2026-05-20)

Brought the DABT database from 64% (3,092/4,841) to **94.3% (4,566/4,841)** answer letter coverage.

## Original Gap: 1,749 questions missing correct_answer_letter

| Source | Missing | Recovered | Remaining | Method |
|--------|---------|-----------|-----------|--------|
| Chapter Tests | 774 | 773 | 1* | Bold-text extraction from docx |
| Past ABT Exams (PDFs) | 355 | 82 | 273 | PPTX study-group slide extraction |
| Past ABT 2008-2014 | 320 | 319 | 1* | XLSX column parsing + regex from explanations |
| Kristen Mini Exams | 208 | 208 | 0 | Bold-text extraction from docx |
| Kristen Topic Tests | 92 | 92 | 0 | Bold-text extraction from docx |
| Regex from explanations | — | 162 | — | Pattern matching existing DB explanations |
| **Total** | **1,749** | **1,474** | **275** | |

*2 statement-type entries with no answer options (DABT-3020, DABT-3934). Not valid MCQs.

## Extraction Techniques Per Format

### DOCX — Bold Text Detection (Chapter Tests, Kristen materials)

The most productive technique. Source files at `/root/dabt-curated/` have "with answers" versions where the correct option is bolded.

```python
from docx import Document
from docx.shared import RGBColor

def extract_bold_answers(docx_path):
    """Extract answer letters from docx where correct options are bolded."""
    doc = Document(docx_path)
    current_q_num = None
    answers = {}
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        # Detect question number
        import re
        qm = re.match(r'^(\d+)[\.\)]\s*', text)
        if qm:
            current_q_num = int(qm.group(1))
        
        # Check for bold runs (answer marking)
        has_bold = any(run.bold for run in para.runs if run.text.strip())
        if has_bold and current_q_num:
            # Extract the option letter (A, B, C, D, etc.)
            lm = re.match(r'^([A-H])[\.\)]?\s*', text)
            if lm:
                answers[current_q_num] = lm.group(1)
    
    return answers
```

**Pitfalls:**
- Sub-numbering within questions (e.g. Q29 having "1.", "2." inside) can cause off-by-one errors. Filter: only accept numbered lines where the number is the current question (not increasing above the max expected).
- Merged chapters (e.g., 12A+12B into one DB chapter) need manual mapping.
- Some docx files use explicit "Answer: X" markers instead of bold text — add regex fallback.

### XLSX — Column Parsing (2008-2014 Past ABT)

The compiled recert exams xlsx had answer explanations in column B. Answer letter was the first token after "Answer is" / "answer is" / "Answer:" in the explanation text.

```python
import openpyxl
wb = openpyxl.load_workbook('file.xlsx')
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    q_num, explanation = row[0], row[1]
    if explanation:
        m = re.search(r'(?:answer|Answer)\s*is\s*[:\.\-–\s]*([A-H])', str(explanation))
        if m:
            answer_letter = m.group(1)
```

### PPTX — Slide Text Extraction (Past ABT Exam Study Groups)

Study group discussion slides had explicit "Answer: X" markers on some slides. Extract all text and search for patterns.

```python
from pptx import Presentation
prs = Presentation('file.pptx')
all_text = []
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            all_text.append(shape.text)
full = '\n'.join(all_text)
# Then regex for answer markers
```

**Pitfalls:**
- Not all slides have explicit answer markers — many are discussion-only.
- Question text in slides may be abbreviated or reformatted vs the DB, making cross-referencing by text matching inexact.
- 2017 Certification Exam has no study group PPTX files at all.

### Regex from DB Explanations

For questions where `explanation` IS set but `correct_answer_letter` is NULL, the answer letter may be embedded in the explanation text. Most common patterns:

```
Answer is X
Answer: X
Correct answer: X
Correct response is X
I chose X
```

Aggressive extraction (try multiple patterns, longest match first) recovered ~162 answers this way.

## Cross-Referencing with Database

Two strategies for matching extracted answers to DB records:

1. **By question_number_in_source:** When source file numbering is sequential and clean (e.g., Kristen exams numbered 1-40 per file). Requires knowing offset ranges — query `SELECT id, question_number_in_source FROM questions WHERE source_file_id=N ORDER BY question_number_in_source`.

2. **By text matching:** When question_number_in_source is unreliable or NULL. Match the first ~80 chars of question_text from the source against the DB. Use substring matching with normalization (strip whitespace, lowercase).

```python
def match_by_text(db_cursor, source_text, source_file_id):
    """Match a source question to DB by text prefix."""
    stub = source_text[:80].strip().lower()
    db_cursor.execute("""
        SELECT id FROM questions 
        WHERE source_file_id = ? 
        AND LOWER(SUBSTR(question_text, 1, ?)) = ?
    """, (source_file_id, len(stub), stub))
    row = db_cursor.fetchone()
    return row[0] if row else None
```

## Quarantine (2026-05-20)

After recovering answer letters, a comprehensive quality audit revealed that 1,048 questions across all sources still had fatal defects — broken formatting, non-standard option counts, or unresolvable answer mismatches. Per user directive, these were **physically moved** to `quarantine` / `quarantine_answer_options` tables rather than leaving NULL markers that could corrupt drill pipelines.

### Quarantine by Issue

| Issue | Questions | Impact |
|-------|-----------|--------|
| No answer letter (273 Past ABT PDFs + 1 Chapter statement) | 274 | Cannot determine correct answer |
| No answer options (94 2000Q + 23 Kristen Topic + 1 Chapter + 1 2008-14) | 119 | No MCQ structure to drill |
| Answer letter doesn't match options (312 2000Q + rest) | 343 | Would present wrong answer |
| Non-standard letters (I, J, O, M, Q, etc.) | 27 | Not valid MCQ letters |
| Non-standard option counts (1-3 or 6-8 options) | 422 | Incompatible with 4-5 option drill format |

### Quarantine by Source

| Source | Main Table | Quarantine | Quarantine Reason |
|--------|-----------|------------|-------------------|
| 2000Q Bank | 1,351 | 450 | Answer mismatch, non-standard letters, missing options |
| Chapter Tests | 904 | 215 | Non-standard option counts (matching tests with 1 option) |
| Past ABT 2008-2014 | 763 | 4 | 3 mismatch + 1 statement entry |
| Mini-ABT 1-11 | 399 | 47 | Non-standard option counts |
| Kristen Topic Tests | 112 | 33 | No options (matching tests) |
| Kristen Mini Exams | 182 | 26 | Non-standard option counts |
| Past ABT PDFs | 82 | 273 | No answer keys published |

### Current State

- **Main table:** 3,793 questions, 100% with answer letter matching valid 4-5 options
- **Quarantine:** 1,048 questions preserved intact with documented issue labels
- **Total:** 4,841

### Restoration Policy

If a quarantine source is later resolved (e.g., SME provides answer keys for Past ABT PDFs), restore with:

```sql
INSERT INTO questions SELECT * FROM quarantine WHERE source_file_id = 7;
INSERT INTO answer_options SELECT * FROM quarantine_answer_options WHERE question_id IN (SELECT id FROM quarantine WHERE source_file_id = 7);
DELETE FROM quarantine WHERE source_file_id = 7;
```

## Remaining Unresolved Questions (273 in quarantine)

All from source_file_id=7 (Past ABT PDFs). These are real ABT certification/recertification exam questions from 2013 (Part B), 2017 (Parts A-D), and clinical vignettes. No answer keys were published with these exams, and no study group PPTX files exist for the 2017 exam. These require SME review — a domain expert needs to answer each question independently and provide the answer key.

To export the remaining questions for SME review:

```sql
SELECT q.id, q.question_text, 
       GROUP_CONCAT(a.option_letter || '. ' || a.option_text, ' | ') as options
FROM questions q
JOIN answer_options a ON q.id = a.question_id
WHERE q.source_file_id = 7 
AND (q.correct_answer_letter IS NULL OR q.correct_answer_letter = '')
GROUP BY q.id
ORDER BY q.id;
```

## Source Directory Structure

The `/root/dabt-curated/` directory is the authoritative source of raw materials, richer than the reference/materials directory:

```
/root/dabt-curated/
├── Chapter_Tests/
│   ├── Tests_with_Answers/     ← 25 docx files with answers in bold
│   └── Tests/                   ← Question-only versions
├── Practice_Exams/
│   ├── Kristen_Mini_Exams/      ← 17 "with answers" docx files
│   ├── _DUPLICATE_Mini-ABT_1-11/
│   └── Past_ABT_Exams/
│       └── Recert_Discussion_Slides/  ← PPTX files (2013, 2015 Part A/B/C)
├── Practice_Tests_by_Topic/
│   └── Kristen_Topic_Tests/     ← 4 topic test "with answers" docx files
├── 2000Q_Question_Bank/
└── Mid-Amer_Tox_Course/
```
