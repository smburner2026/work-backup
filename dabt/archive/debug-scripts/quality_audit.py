#!/usr/bin/env python3
"""Comprehensive DABT DB quality audit."""
import sqlite3

DB = '/root/work/dabt/dabt-tutor/reference/data/dabt.db'
conn = sqlite3.connect(DB)
cur = conn.cursor()

# Category 1: No answer letter
cur.execute('''
    SELECT s.bank_name, COUNT(*) 
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE q.correct_answer_letter IS NULL OR q.correct_answer_letter = ''
    GROUP BY s.id ORDER BY COUNT(*) DESC
''')
print('=== 1. NO ANSWER LETTER (275) ===')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')

# Category 2: No answer options at all
cur.execute('''
    SELECT s.bank_name, COUNT(*) 
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE NOT EXISTS (SELECT 1 FROM answer_options WHERE question_id = q.id)
    GROUP BY s.id ORDER BY COUNT(*) DESC
''')
print('\n=== 2. NO ANSWER OPTIONS (119) ===')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')

# Category 3: Answer letter doesn't match any option
cur.execute('''
    SELECT s.bank_name, COUNT(*) 
    FROM questions q
    JOIN source_files s ON q.source_file_id = s.id
    WHERE q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
    AND NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id AND ao.option_letter = q.correct_answer_letter)
    GROUP BY s.id ORDER BY COUNT(*) DESC
''')
print('\n=== 3. ANSWER LETTER DOESNT MATCH (343) ===')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')

# Category 4: Clean drill-ready
cur.execute('''
    SELECT COUNT(*) FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
    AND EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id AND ao.option_letter = q.correct_answer_letter)
    AND (SELECT COUNT(*) FROM answer_options WHERE question_id = q.id) >= 4
    AND (q.explanation IS NOT NULL AND q.explanation != '')
''')
print(f'\n=== 4. CLEAN: answer + matching options(4+) + explanation ===')
print(f'  {cur.fetchone()[0]} questions')

# Category 5: Usable but no explanation
cur.execute('''
    SELECT COUNT(*) FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
    AND EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id AND ao.option_letter = q.correct_answer_letter)
    AND (SELECT COUNT(*) FROM answer_options WHERE question_id = q.id) >= 4
    AND (q.explanation IS NULL OR q.explanation = '')
''')
print(f'\n=== 5. DRILLABLE NO EXPLANATION ===')
print(f'  {cur.fetchone()[0]} questions')

# Category 6: Non-standard option counts
cur.execute('''
    SELECT opt_count, COUNT(*) FROM (
        SELECT q.id, COUNT(ao.option_letter) as opt_count
        FROM questions q
        JOIN answer_options ao ON q.id = ao.question_id
        GROUP BY q.id
    )
    WHERE opt_count NOT IN (4,5)
    GROUP BY opt_count
    ORDER BY opt_count
''')
print('\n=== 6. NON-STANDARD OPTION COUNTS ===')
for row in cur.fetchall():
    print(f'  {row[0]} options: {row[1]} questions')

# Category 7: Odd answer letters (not A-H)
cur.execute('''
    SELECT q.correct_answer_letter, COUNT(*)
    FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND q.correct_answer_letter != ''
    AND q.correct_answer_letter NOT IN ('A','B','C','D','E','F','G','H')
    GROUP BY q.correct_answer_letter
    ORDER BY COUNT(*) DESC
''')
print('\n=== 7. NON-STANDARD ANSWER LETTERS ===')
for row in cur.fetchall():
    print(f'  \"{row[0]}\": {row[1]} questions')

# Category 8: Questions with options but options don't cover A-D (e.g. start at wrong letter)
cur.execute('''
    SELECT COUNT(*) FROM (
        SELECT q.id
        FROM questions q
        JOIN answer_options ao ON q.id = ao.question_id
        GROUP BY q.id
        HAVING COUNT(*) >= 4
        AND SUM(CASE WHEN ao.option_letter = 'A' THEN 1 ELSE 0 END) = 0
    )
''')
print(f'\n=== 8. 4+ OPTIONS BUT NONE START WITH A ===')
print(f'  {cur.fetchone()[0]} questions')

conn.close()
