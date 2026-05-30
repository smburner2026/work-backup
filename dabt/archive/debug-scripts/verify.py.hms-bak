#!/usr/bin/env python3
"""
Verify the match quality. Show DB IDs per exam and check for contiguous ranges.
"""

import os, re, json, sqlite3
from docx import Document

EXAM_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"
DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"

def normalize(t):
    t = re.sub(r'\s+', ' ', t).strip().lower()
    t = re.sub(r'[^\w\s]', '', t)
    return t

# Get DB questions
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("""
    SELECT id, question_number_in_source, question_text 
    FROM questions WHERE source_file_id=4 
    ORDER BY id
""")
db_qs = [dict(r) for r in cur.fetchall()]
conn.close()

print(f"DB has {len(db_qs)} questions\n")

# For each exam with answers, extract the question texts and try to find the exact DB ID range
exam_dir = EXAM_DIR
files_with_answers = [f for f in sorted(os.listdir(exam_dir)) if 'with answers' in f.lower() or 'examination with answers' in f.lower() or 'exam answers' in f.lower()]

# First, let's look at the 05 May 2017 exam specifically
for fname in files_with_answers:
    if '05 May' not in fname:
        continue
    
    print(f"=== {fname} ===")
    doc = Document(os.path.join(exam_dir, fname))
    
    # Extract question texts (without number prefix)
    qtexts = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        m = re.match(r'^(\d+)[\.\)]\s+(.*)', text)
        if m:
            qnum = int(m.group(1))
            qtext = m.group(2).strip()
            # Normalize: remove "(OK)" etc.
            qtext_clean = re.sub(r'\s*\(OK\)\s*$', '', qtext).strip()
            qtexts[qnum] = qtext_clean
    
    # Now for each question in this exam, find the BEST matching DB question
    for qnum in sorted(qtexts.keys())[:15]:
        exam_text = qtexts[qnum]
        exam_norm = normalize(exam_text)
        
        # Find best match among ALL DB questions
        best_match = None
        best_score = 0
        
        for db_q in db_qs:
            db_norm = normalize(db_q['question_text'])
            # Score: longest common prefix
            score = 0
            for i in range(min(len(exam_norm), len(db_norm))):
                if exam_norm[i] == db_norm[i]:
                    score += 1
                else:
                    break
            
            if score > best_score:
                best_score = score
                best_match = db_q
        
        if best_match:
            print(f"  Q{qnum:2d}: [{best_match['id']}] (score={best_score})")
            print(f"       Exam: {exam_text[:70]}")
            print(f"       DB:   {best_match['question_text'][:70]}")
            if best_score < 20:
                print(f"       *** LOW CONFIDENCE ***")
        print()

print("\n\n=== DB ID ORDER ===")
for q in db_qs:
    print(f"  [{q['id']}] Q{q['question_number_in_source']}: {q['question_text'][:60]}")
