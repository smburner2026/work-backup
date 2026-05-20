#!/usr/bin/env python3
"""Phase 1c: Aggressive extraction from all remaining explanations."""
import sqlite3
import re

DB = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ALL questions with explanation but no answer letter
cur.execute("""
    SELECT q.id, q.explanation, s.bank_name, s.id as src_id
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE (q.correct_answer_letter IS NULL OR q.correct_answer_letter = '')
    AND (q.explanation IS NOT NULL AND q.explanation != '')
    ORDER BY s.id
""")

rows = cur.fetchall()
print(f'Total remaining with explanation: {len(rows)}')

# All possible answer patterns, tried in order
# For each pattern, we check if the answer letter matches one of the valid options
# Options are A-H for most questions

patterns = [
    # "Answer is X" - with typos  
    (re.compile(r'(?:answer|Answer|anawer|Anawer|Answe?r)\s*(?:is)?\s*[:\.\-–\s=]*\s*([A-H])\b'), 'answer_is'),
    # "Correct response is X"
    (re.compile(r'[Cc]orrect\s+response\s+is\s+([A-H])\b'), 'correct_response'),
    # "X is the answer" 
    (re.compile(r'([A-H])\s+is\s+the\s+answer'), 'x_is_answer'),
    # "Correct answer: X" 
    (re.compile(r'[Cc]orrect\s+answer\s*[:\-–=]\s*([A-H])\b'), 'correct_answer_colon'),
    # "Correct Answer = ? X" 
    (re.compile(r'[Cc]orrect\s+[Aa]nswer\s*=\s*\?\s*([A-H])'), 'correct_answer_eq_q'),
    # "I chose X" 
    (re.compile(r'I\s+chose\s+([A-H])\b'), 'i_chose'),
    # "Probably X" at start of explanation
    (re.compile(r'^[Pp]robably\s+([A-H])\b'), 'probably_x'),
    # Explanation starts with "X" followed by explanation text (X being a single letter answer)
    (re.compile(r'^([A-H])\b[\.\)]?\s+(?:is|are|was|has|refers|involves|results|occurs|acts|works|causes|leads|produces|increases|decreases|affects|blocks|inhibits|stimulates|binds|forms|undergoes|does|can|will|may)'), 'first_word_answer'),
    # Answer letter embedded: "E)" in the text indicating the answer
    (re.compile(r'\b([A-H])\s*\)\s*(?:is|True|False|correct|incorrect)'), 'letter_paren_answer'),
    # Line starts with letter then dash
    (re.compile(r'^([A-H])\s*[:\-–]\s*(?:is|the)'), 'line_start_letter'),
    # "Answer = X" 
    (re.compile(r'[Aa]nswer\s*=\s*([A-H])\b'), 'answer_eq'),
    # "Answer: X" at beginning of paragraph
    (re.compile(r'[Aa]nswer\s*:\s*([A-H])\b'), 'answer_colon'),
]

# Also check question_text for embedded answer indicators (for source 6 style)
cur2 = conn.cursor()
cur2.execute("""
    SELECT q.id, q.question_text, s.bank_name
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE q.id IN ({})
""".format(','.join('?' for _ in [r[0] for r in rows])), [r[0] for r in rows])

qt_map = {qid: qt for qid, qt, _ in cur2.fetchall()}
gt_map = {qid: src_id for qid, _, _, src_id in rows}

# Pattern for question text: "NOT contribute to toxicity? E"
qt_patterns = [
    re.compile(r'\?\s*([A-H])\s*$'),
    re.compile(r'[?:]\s*([A-H])\s*$'),
    re.compile(r'[?]\s*([A-H])\b'),
]

updates = []
found_total = 0
not_found = 0
by_source = {}
no_match_samples = []

for qid, explanation, bank_name, src_id in rows:
    by_source.setdefault(bank_name, {'total': 0, 'found': 0})
    by_source[bank_name]['total'] += 1
    
    found = False
    
    # First try explanation patterns
    for pat, name in patterns:
        m = pat.search(explanation)
        if m:
            letter = m.group(1).strip()
            if letter in 'ABCDEFGH':
                updates.append((letter, qid))
                found = True
                found_total += 1
                by_source[bank_name]['found'] += 1
                break
    
    # If not found in explanation, try question text (for source 6 style: "NOT contribute? E")
    if not found and src_id == 6:
        qt = qt_map.get(qid, '')
        for pat in qt_patterns:
            m = pat.search(qt)
            if m:
                letter = m.group(1).strip()
                if letter in 'ABCDEFGH':
                    updates.append((letter, qid))
                    found = True
                    found_total += 1
                    by_source[bank_name]['found'] += 1
                    break
    
    if not found:
        not_found += 1
        if len(no_match_samples) < 10:
            no_match_samples.append((qid, bank_name, explanation[:200]))

print(f'\nTotal found: {found_total}')
print(f'Not found: {not_found}')

print('\n--- By source ---')
for src, counts in sorted(by_source.items()):
    print(f'  {src}: {counts["found"]}/{counts["total"]}')

if no_match_samples:
    print('\n--- Still unmatched ---')
    for qid, src, ex in no_match_samples:
        print(f'  {qid} ({src}): {ex}')
        print()

# Update
if updates:
    cur.executemany('UPDATE questions SET correct_answer_letter = ? WHERE id = ?', updates)
    conn.commit()
    print(f'\n✅ Updated {len(updates)} more questions')

conn.close()
