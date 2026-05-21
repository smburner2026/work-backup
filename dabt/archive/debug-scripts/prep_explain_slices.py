#!/usr/bin/env python3
"""Dump questions needing explanations to JSON for parallel processing."""
import sqlite3
import json

DB = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
    SELECT q.id, s.bank_name, q.question_number_in_source,
           q.question_text, q.correct_answer_letter,
           q.correct_answer_text, q.bloom_level
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE (q.explanation IS NULL OR q.explanation = '')
    ORDER BY s.id, q.id
""")

questions = []
for row in cur.fetchall():
    q = {
        'id': row[0],
        'bank': row[1],
        'num': row[2],
        'text': row[3],
        'answer': row[4],
        'answer_text': row[5] or '',
        'bloom': row[6] or '',
        'options': []
    }
    # Get options
    opt_cur = conn.cursor()
    opt_cur.execute("SELECT option_letter, option_text FROM answer_options WHERE question_id = ? ORDER BY option_letter", (q['id'],))
    for opt in opt_cur.fetchall():
        q['options'].append({'letter': opt[0], 'text': opt[1]})
    questions.append(q)
    opt_cur.close()

conn.close()

# Split into slices
# Slice 1: Chapter Tests (576)
# Slice 2: Kristen Mini Exams (182) + Kristen Topic Tests (55) = 237
# Slice 3: Past ABT PDFs (82) + Past ABT 2008-2014 (6) = 88

slice1 = [q for q in questions if q['bank'] == 'Chapter Tests']
slice2 = [q for q in questions if q['bank'] in ('Kristen Mini Exams', 'Kristen Topic Tests')]
slice3 = [q for q in questions if q['bank'] in ('Past ABT Exams (PDFs)', 'Past ABT Exams (2008-2014)')]

print(f"Slice 1 (Chapter Tests): {len(slice1)}")
print(f"Slice 2 (Kristen): {len(slice2)}")
print(f"Slice 3 (Past ABT): {len(slice3)}")
print(f"Total: {len(slice1) + len(slice2) + len(slice3)}")

with open('/root/work/dabt/explain_slice1.json', 'w') as f:
    json.dump(slice1, f, indent=2)
with open('/root/work/dabt/explain_slice2.json', 'w') as f:
    json.dump(slice2, f, indent=2)
with open('/root/work/dabt/explain_slice3.json', 'w') as f:
    json.dump(slice3, f, indent=2)

print("\nSlices written to explain_slice{1,2,3}.json")
