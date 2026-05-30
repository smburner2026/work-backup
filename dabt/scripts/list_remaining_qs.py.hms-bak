#!/usr/bin/env python3
"""
Match exam questions from PPTX files to DABT database IDs.
"""
import sqlite3
import json
import re

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all remaining source 7 questions with full text
cursor.execute("""
    SELECT id, question_text, correct_answer_letter
    FROM questions 
    WHERE source_file_id=7 
    AND (correct_answer_letter IS NULL OR correct_answer_letter = '')
    ORDER BY id
""")

all_qs = []
for row in cursor.fetchall():
    all_qs.append({
        'id': row[0],
        'text': row[1],
        'current_answer': row[2]
    })

print(f"Total remaining questions: {len(all_qs)}")

# Print questions to help match
print("\n=== FULL TEXT OF REMAINING QUESTIONS ===")
for q in all_qs:
    print(f"\n{q['id']}: {q['text'][:200]}")
    print(f"  {'='*40}")

conn.close()
