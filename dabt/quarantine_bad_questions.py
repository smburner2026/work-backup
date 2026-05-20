#!/usr/bin/env python3
"""Move low-quality questions to quarantine tables."""
import sqlite3

DB = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'
conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = OFF")
cur = conn.cursor()

# Step 1: Create quarantine tables
cur.executescript("""
    CREATE TABLE IF NOT EXISTS quarantine (
        id TEXT PRIMARY KEY,
        question_text TEXT NOT NULL,
        correct_answer_letter TEXT,
        correct_answer_text TEXT,
        explanation TEXT,
        source_file_id INTEGER,
        question_number_in_source INTEGER,
        bloom_level TEXT,
        q_issue TEXT,
        FOREIGN KEY (source_file_id) REFERENCES source_files(id)
    );
    CREATE TABLE IF NOT EXISTS quarantine_answer_options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id TEXT NOT NULL,
        option_letter TEXT NOT NULL,
        option_text TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES quarantine(id)
    );
""")

# Step 2: Identify all problem questions with their issues
cur.execute("""
    SELECT q.id FROM questions q WHERE NOT EXISTS 
    (SELECT 1 FROM answer_options WHERE question_id = q.id)
""")
no_options = set(r[0] for r in cur.fetchall())

cur.execute("""
    SELECT q.id FROM questions q
    WHERE q.correct_answer_letter IS NULL OR q.correct_answer_letter = ''
""")
no_answer = set(r[0] for r in cur.fetchall())

cur.execute("""
    SELECT q.id FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
    AND NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id AND ao.option_letter = q.correct_answer_letter)
""")
mismatch = set(r[0] for r in cur.fetchall())

cur.execute("""
    SELECT q.id FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
    AND q.correct_answer_letter NOT IN ('A','B','C','D','E','F','G','H')
""")
bad_letter = set(r[0] for r in cur.fetchall())

cur.execute("""
    SELECT id FROM (
        SELECT q.id as id, COUNT(ao.option_letter) as opt_count
        FROM questions q
        JOIN answer_options ao ON q.id = ao.question_id
        GROUP BY q.id
    ) sub
    WHERE opt_count NOT IN (4,5)
""")
bad_options = set(r[0] for r in cur.fetchall())

# Step 3: Build the quarantine set with reasons
# Group A = broken: no_options + no_answer + mismatch + bad_letter
# Group B = non-standard formats: bad_options (not already in Group A)

group_a = no_options | no_answer | mismatch | bad_letter
group_b = bad_options - group_a

all_quarantine = group_a | group_b

print(f"Group A (broken): {len(group_a)} questions")
print(f"Group B (non-standard formats): {len(group_b)} questions")
print(f"Total to quarantine: {len(all_quarantine)} questions")

# Step 4: Assign issue labels for each question
issue_map = {}
for qid in all_quarantine:
    issues = []
    if qid in no_options: issues.append("no_answer_options")
    if qid in no_answer: issues.append("no_answer_letter")
    if qid in mismatch: issues.append("answer_mismatch")
    if qid in bad_letter: issues.append(f"bad_letter")
    if qid in bad_options: 
        cur.execute("SELECT COUNT(*) FROM answer_options WHERE question_id = ?", (qid,))
        cnt = cur.fetchone()[0]
        issues.append(f"nonstandard_options({cnt})")
    issue_map[qid] = ";".join(issues)

# Step 5: Move questions to quarantine
moved = 0
errors = []
for qid in all_quarantine:
    issue = issue_map[qid]
    # Copy question
    cur.execute("""
        INSERT OR IGNORE INTO quarantine (id, question_text, correct_answer_letter, correct_answer_text, 
                                           explanation, source_file_id, question_number_in_source, bloom_level, q_issue)
        SELECT id, question_text, correct_answer_letter, correct_answer_text,
               explanation, source_file_id, question_number_in_source, bloom_level, ?
        FROM questions WHERE id = ?
    """, (issue, qid))
    
    # Copy answer options
    cur.execute("""
        INSERT OR IGNORE INTO quarantine_answer_options (question_id, option_letter, option_text)
        SELECT question_id, option_letter, option_text FROM answer_options WHERE question_id = ?
    """, (qid,))
    
    if cur.rowcount > 0:
        moved += 1

print(f"\nMoved {moved} questions to quarantine")

# Step 6: Delete from main tables
# Delete answer_options first (FK dependency)
for qid in all_quarantine:
    cur.execute("DELETE FROM answer_options WHERE question_id = ?", (qid,))
    cur.execute("DELETE FROM questions WHERE id = ?", (qid,))

conn.commit()

# Step 7: Verify
cur.execute("SELECT COUNT(*) FROM questions")
remaining = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM quarantine")
q_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM answer_options")
ao_remaining = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM quarantine_answer_options")
qao_count = cur.fetchone()[0]

print(f"\n=== VERIFICATION ===")
print(f"Main questions table: {remaining}")
print(f"Quarantine table: {q_count}")
print(f"Main answer_options: {ao_remaining}")
print(f"Quarantine answer_options: {qao_count}")
print(f"Total accounted: {remaining + q_count} (should be 4841)")

# Step 8: Summary by issue
cur.execute("""
    SELECT q_issue, COUNT(*) FROM quarantine
    GROUP BY q_issue ORDER BY COUNT(*) DESC
""")
print(f"\n=== QUARANTINE BY ISSUE ===")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Step 9: Summary by source
cur.execute("""
    SELECT s.bank_name, COUNT(*) 
    FROM quarantine q
    JOIN source_files s ON q.source_file_id = s.id
    GROUP BY s.id ORDER BY COUNT(*) DESC
""")
print(f"\n=== QUARANTINE BY SOURCE ===")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
