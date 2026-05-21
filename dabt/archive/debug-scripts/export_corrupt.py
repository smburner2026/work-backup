#!/usr/bin/env python3
"""Export 68 corrupt source-6 questions to JSON for processing."""
import sqlite3
import json

DB = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
    SELECT q.id, q.question_text, q.correct_answer_letter, s.bank_name
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE s.id = 6
    AND length(q.explanation) < 10
    AND q.explanation != ''
    ORDER BY q.id
""")

questions = []
for row in cur.fetchall():
    q = {'id': row[0], 'text': row[3], 'answer': row[2], 'bank': row[3], 'options': []}
    opt_cur = conn.cursor()
    opt_cur.execute("SELECT option_letter, option_text FROM answer_options WHERE question_id = ? ORDER BY option_letter", (q['id'],))
    for o in opt_cur.fetchall():
        q['options'].append({'letter': o[0], 'text': o[1]})
    opt_cur.close()
    questions.append(q)

print(f"{len(questions)} corrupt questions")

with open('/root/work/dabt/fix_explain_batch.json', 'w') as f:
    json.dump(questions, f, indent=2)

conn.close()
