#!/usr/bin/env python3
"""Phase 1: Extract answer letters from ALL explanations across all sources."""
import sqlite3
import re

DB = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'

conn = sqlite3.connect(DB)
cur = conn.cursor()

# ALL questions with explanation but no answer letter
cur.execute("""
    SELECT q.id, q.explanation, s.bank_name 
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE (q.correct_answer_letter IS NULL OR q.correct_answer_letter = '')
    AND (q.explanation IS NOT NULL AND q.explanation != '')
    ORDER BY s.id
""")

rows = cur.fetchall()
print(f'Total questions with explanation but no answer_letter: {len(rows)}')

# Multiple regex patterns to catch different answer formats
patterns = [
    # "answer is X" or "Answer is: X" or "answer is:A"  
    re.compile(r'(?:answer|Answer)\s*is\s*[:\.\-–\s]*([A-Z])\b'),
    # "X is the answer"  
    re.compile(r'([A-Z])\s+is\s+the\s+answer'),
    # "I chose X"
    re.compile(r'I\s+chose\s+([A-Z])\b'),
    # "Correct answer: X"
    re.compile(r'[Cc]orrect\s+answer\s*[:\-–]\s*([A-Z])\b'),
    # "The correct answer is X"
    re.compile(r'[Tt]he\s+correct\s+answer\s+is\s+([A-Z])\b'),
    # At start of explanation: "A)" or "A." or "A " (if it immediately states the answer)
    re.compile(r'^([A-F])\b[\.\)]?\s'),
]

by_source = {}
matched = 0
not_matched = 0
updates = []
no_match_samples = []

for qid, explanation, bank_name in rows:
    by_source.setdefault(bank_name, {'total': 0, 'matched': 0})
    by_source[bank_name]['total'] += 1
    
    matched_q = False
    for pat in patterns:
        m = pat.search(explanation)
        if m:
            letter = m.group(1).strip()
            if letter in 'ABCDEFGH':
                updates.append((letter, qid, bank_name))
                by_source[bank_name]['matched'] += 1
                matched += 1
                matched_q = True
                break
    if not matched_q:
        not_matched += 1
        if len(no_match_samples) < 10:
            no_match_samples.append((qid, bank_name, explanation[:200]))

print(f'\nMatched: {matched}')
print(f'No match: {not_matched}')

print('\n--- By source ---')
for src, counts in sorted(by_source.items()):
    print(f'  {src}: {counts["matched"]}/{counts["total"]}')

if no_match_samples:
    print('\n--- Samples that did not match ---')
    for qid, src, ex in no_match_samples:
        print(f'  {qid} ({src}): {ex}')
        print()

# Update DB
if updates:
    cur.executemany('UPDATE questions SET correct_answer_letter = ? WHERE id = ?', 
                    [(l, i) for l, i, _ in updates])
    conn.commit()
    print(f'\n✅ Updated {len(updates)} questions with correct_answer_letter')

conn.close()
