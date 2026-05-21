# DOCX Bold-Text Answer Extraction

Extract answer letters from multiple-choice documents where the correct option is marked in **bold**.

## Core Technique

```python
from docx import Document
import re

def extract_bold_answers(docx_path):
    """Extract (question_number -> answer_letter) from bold-formatted docx."""
    doc = Document(docx_path)
    current_q = None
    answers = {}
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Detect question number (line starts with digit followed by . or ))
        q_match = re.match(r'^(\d+)[\.\)]\s', text)
        if q_match:
            current_q = int(q_match.group(1))
        
        # Check if any run in this paragraph is bold
        has_bold = any(
            run.bold and run.text.strip() 
            for run in para.runs
        )
        
        if has_bold and current_q is not None:
            # Extract option letter (A/B/C/D/E/F/G/H)
            opt_match = re.match(r'^([A-H])[\.\)]?\s*', text)
            if opt_match:
                answers[current_q] = opt_match.group(1)
    
    return answers
```

## Pitfalls

- **Sub-numbering**: If a question body contains numbered substeps (e.g., "1. factor A, 2. factor B"), the parser may treat them as new questions. Filter: track the maximum expected question count and ignore numbers that skip ahead too far.
- **Multi-paragraph questions**: The answer option may be on a different paragraph than the question number. Use `current_q` as state that persists until a new question number is encountered.
- **Mixed formatting**: Some documents use explicit "Answer: X" markers instead of bold text. Combine with regex fallback: `re.search(r'Answer\s*[:\-]\s*([A-H])', full_text)`.
- **Empty runs**: A run can exist with font metadata but zero visible text. Check `run.text.strip()` before checking `run.bold`.
- **Section breaks**: Chapter/section headings sometimes start with digits too. Filter by limiting to the expected question range for that document.

## Mapping Extracted Answers to a SQLite Database

```python
import sqlite3

def map_to_db(answers, db_path, source_file_id, q_num_start=1, q_num_end=100):
    """Map extracted {q_num: letter} to DB questions by question_number_in_source."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    updates = []
    for q_num, letter in answers.items():
        if q_num < q_num_start or q_num > q_num_end:
            continue
        cur.execute("""
            SELECT id FROM questions 
            WHERE source_file_id = ? 
            AND question_number_in_source = ?
        """, (source_file_id, q_num))
        row = cur.fetchone()
        if row:
            updates.append((letter, row[0]))
    
    cur.executemany(
        "UPDATE questions SET correct_answer_letter = ? WHERE id = ?", 
        updates
    )
    conn.commit()
    return len(updates)
```

## When to Use

- Textbook chapter question banks with answer keys in "with answers" editions
- Practice exam docx files where correct options are bolded
- Any structured MCQ document where formatting conveys the answer key
