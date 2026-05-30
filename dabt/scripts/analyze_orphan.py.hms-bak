#!/usr/bin/env python3
"""Analyze the orphan Mini-ABT exam 21 July 2017 and compare with other exams."""

import os
from docx import Document

KRISTEN_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"
ORPHAN_FILE = os.path.join(KRISTEN_DIR, "Mini-ABT exam 21 July 2017.docx")

def extract_all_text(doc_path):
    """Extract all text from a docx file."""
    try:
        doc = Document(doc_path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        # Also extract from tables
        tables_text = []
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells]
                tables_text.append(' | '.join(row_text))
        return paragraphs, tables_text
    except Exception as e:
        return [f"ERROR: {e}"], []

def extract_questions(paragraphs):
    """Try to identify questions from paragraphs."""
    questions = []
    current_q = []
    for p in paragraphs:
        # Check if this looks like a question number
        stripped = p.strip()
        if stripped and (stripped[0].isdigit() or 
                        stripped.startswith('Q') or 
                        stripped.startswith('Question')):
            if current_q:
                questions.append(' '.join(current_q))
            current_q = [stripped]
        else:
            current_q.append(stripped)
    if current_q:
        questions.append(' '.join(current_q))
    return questions

def get_doc_text_set(doc_path):
    """Get a set of text lines from a document for comparison."""
    paragraphs, tables = extract_all_text(doc_path)
    return set(p for p in paragraphs if len(p) > 5)

# Step 1: Extract content from orphan file
print("=" * 70)
print("STEP 1: EXTRACTING ORPHAN FILE CONTENT")
print("=" * 70)
orphan_text, orphan_tables = extract_all_text(ORPHAN_FILE)
print(f"\nFile: Mini-ABT exam 21 July 2017.docx")
print(f"Number of paragraphs: {len(orphan_text)}")
print(f"Number of table rows: {len(orphan_tables)}")

print("\n--- All Paragraphs ---")
for i, p in enumerate(orphan_text):
    print(f"  [{i:3d}] {p[:200]}")

if orphan_tables:
    print("\n--- Table Content ---")
    for i, t in enumerate(orphan_tables):
        print(f"  [T{i:3d}] {t[:200]}")

# Step 2: Identify question format
print("\n" + "=" * 70)
print("STEP 2: IDENTIFY QUESTION FORMAT")
print("=" * 70)

# Look for multiple choice patterns (A., B., C., D.)
all_text = '\n'.join(orphan_text)
mcq_count = 0
short_answer_count = 0
lines = all_text.split('\n')
for line in lines:
    line = line.strip()
    if any(f"{letter}." in line or f"{letter})" in line for letter in ['A', 'B', 'C', 'D']):
        mcq_count += 1
    # Check for question numbers
    if any(line.startswith(f"{n}.") or line.startswith(f"{n})") for n in range(1, 101)):
        pass  # Just probing

print(f"\nTotal lines with MCQ options (A./B./C./D.): {mcq_count}")

# Try to identify questions
questions = extract_questions(orphan_text)
print(f"\nPotential questions identified: {len(questions)}")
for i, q in enumerate(questions):
    print(f"  Q{i+1}: {q[:150]}...")

# Step 3: Compare with other exam files that have answer keys
print("\n" + "=" * 70)
print("STEP 3: COMPARE WITH ANSWER-KEY EXAMS")
print("=" * 70)

answer_key_files = [
    "Mini-ABT exam with answers for 22 Sept. 2017 (corrected.ver.2).docx",
    "Mini-ABT exam with answers for 15 Sept. 2017.docx",
    "Mini-ABT exam with answers for 11 August 2017.docx",
    "Mini-ABT exam with answers 28 July 2017-PART A.docx",
    "Mini-ABT exam with answers 28 July 2017-PART B.docx",
    "Mini-ABT exam with answers 23 June 2017.docx",
    "Mini-ABT exam with answers 19 May 2017.docx",
    "Mini-ABT exam with answers 26 August 2017.docx",
    "Mini-ABT exam with answers 14 July 2017-B.docx",
    "Mini-ABT exam with answers 14 July 2017-A.docx",
    "Mini-ABT exam with answers 12 May 2017.docx",
    "Mini-ABT exam with answers 09 June 2017.docx",
    "Mini-ABT exam with answers 05 May 2017.docx",
    "Mini-ABT examination with answers 02 June 2017.docx",
    "Mini-ABT exam with answers 03 September 2017.docx",
    "Mini-ABT exam answers 26 May 2017.docx",
]

orphan_set = get_doc_text_set(ORPHAN_FILE)

# Also check the non-answer versions that have matching answer-key versions
exam_without_answers = [f for f in os.listdir(KRISTEN_DIR) if f.endswith('.docx') and 'answers' not in f.lower() and 'Answers' not in f]
print(f"\nExams without answers in filename: {exam_without_answers}")

# Check exam 02 June 2017 which has both versions
june2_no_ans = os.path.join(KRISTEN_DIR, "Mini-ABT examination 02 June 2017.docx")
june2_with_ans = os.path.join(KRISTEN_DIR, "Mini-ABT examination with answers 02 June 2017.docx")

if os.path.exists(june2_no_ans) and os.path.exists(june2_with_ans):
    set_no = get_doc_text_set(june2_no_ans)
    set_with = get_doc_text_set(june2_with_ans)
    overlap = set_no & set_with
    only_no = set_no - set_with
    only_with = set_with - set_no
    print(f"\n02 June 2017 comparison:")
    print(f"  Common lines: {len(overlap)}")
    print(f"  Only in no-answers version: {len(only_no)}")
    print(f"  Only in with-answers version: {len(only_with)}")
    if only_with:
        print(f"  Lines unique to answers version (likely answer key):")
        for l in list(only_with)[:20]:
            print(f"    - {l[:150]}")

# Compare orphan against ALL answer-key files
print(f"\nComparing orphan file against {len(answer_key_files)} answer-key files...")
best_match = None
best_overlap = 0

for akf in answer_key_files:
    ak_path = os.path.join(KRISTEN_DIR, akf)
    if not os.path.exists(ak_path):
        print(f"  SKIP (not found): {akf}")
        continue
    ak_set = get_doc_text_set(ak_path)
    overlap = len(orphan_set & ak_set)
    orphan_only = len(orphan_set - ak_set)
    ak_only = len(ak_set - orphan_set)
    total_orphan = len(orphan_set)
    total_ak = len(ak_set)
    
    pct = overlap / total_orphan * 100 if total_orphan > 0 else 0
    print(f"\n  Compared with: {akf}")
    print(f"    Orphan has {total_orphan} unique text lines")
    print(f"    Answer key has {total_ak} unique text lines")
    print(f"    Overlap: {overlap} lines ({pct:.1f}%)")
    print(f"    Orphan-only: {orphan_only} lines")
    print(f"    Answer-key-only: {ak_only} lines")
    
    if pct > best_overlap:
        best_overlap = pct
        best_match = akf
    
    if overlap > 0 and overlap / max(total_orphan, total_ak) > 0.5:
        print(f"  *** HIGH OVERLAP DETECTED ***")
        # Show the differing lines
        if orphan_only:
            print(f"  Lines in orphan but NOT in {akf}:")
            for l in sorted(list(orphan_only))[:15]:
                print(f"    - {l[:150]}")
        if ak_only:
            print(f"  Lines in {akf} but NOT in orphan:")
            for l in sorted(list(ak_only))[:15]:
                print(f"    - {l[:150]}")

if best_match:
    print(f"\n*** Best match: {best_match} with {best_overlap:.1f}% overlap ***")

# Step 4: Check if 21 July matches 14 July or other close dates
print("\n" + "=" * 70)
print("STEP 4: COMPARE WITH CLOSE DATE EXAMS")
print("=" * 70)

close_dates = [
    "Mini-ABT exam 14 July 2017-A.docx",
    "Mini-ABT exam 14 July 2017-B.docx",
    "Mini-ABT exam 28 July 2017-PART A.docx",
    "Mini-ABT exam 28 July 2017-PART B.docx",
    "Mini-ABT exam 23 June 2017.docx",
    "Mini-ABT exam 26 August 2017.docx",
]

for cd in close_dates:
    cd_path = os.path.join(KRISTEN_DIR, cd)
    if not os.path.exists(cd_path):
        continue
    cd_set = get_doc_text_set(cd_path)
    overlap = len(orphan_set & cd_set)
    total = len(orphan_set)
    pct = overlap / total * 100 if total > 0 else 0
    print(f"  Overlap with {cd}: {overlap}/{total} lines ({pct:.1f}%)")
    
    if pct > 5:
        cd_text, _ = extract_all_text(cd_path)
        print(f"  --- {cd} content preview ---")
        for p in cd_text[:20]:
            print(f"    {p[:200]}")

print("\nDone.")
