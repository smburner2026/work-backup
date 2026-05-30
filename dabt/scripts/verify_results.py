#!/usr/bin/env python3
"""
Check which remaining questions can be answered from PPTX slides.
Focus on finding any missed matches.
"""
import sqlite3
import re

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all remaining source 7 questions with full text
cursor.execute("""
    SELECT id, question_text, correct_answer_letter
    FROM questions 
    WHERE source_file_id=7 
    AND (correct_answer_letter IS NULL OR correct_answer_letter = '')
    ORDER BY id
""")

remaining = []
for row in cursor.fetchall():
    text_clean = re.sub(r'\s+', ' ', row['question_text']).strip().lower()
    remaining.append({
        'id': row['id'],
        'text': text_clean,
        'raw': row['question_text']
    })

print(f"Remaining unanswered: {len(remaining)}")

# Additional patterns to try matching
more_patterns = [
    # More 2013 Part A Q9-16
    ('which of the patients is more likely to benefit from liver transplantation', '?'),  # Not in recert slides
    ('a 26-year-old nurse in her 18th week of pregnancy suffers a needle stick injury', '?'),  # Not in recert
    ('which of the following is indicated to further evaluate the etiology of his mild transaminitis', '?'),  # Not in recert
    ('patient denies excessive alcohol intake', '?'),  # Not in recert
    ('which of the following is not considered a part of the metabolic syndrome', '?'),  # Not in recert
    ('which of the following is not a feature of nash on liver biopsy', '?'),  # Not in recert
    ('what is the approximate prevalence of simple steatosis', '?'),  # Not in recert
    ('you recommend exercise and weight loss for your patient', '?'),  # Not in recert
    ('your patient asks you about the natural history of nafld', '?'),  # Not in recert
    ('reagents must be labeled with which of the following', '?'),  # Not in recert
    ('which of the following is not correct regarding ethanol in forensic toxicology laboratories', '?'),  # Not in recert
    
    # From 2013 Part C Q1 - the discussion mentions answer but without letter labels
    # The slide text lists options without A-E markers
  
    # Try "most critical factor in the site of deposition"
    ('most critical factor in the site of deposition within the respiratory tract', '?'),  # Not in recert slides
    
    # Clinical chemistry question from 2013 Part C Q1
    ('clinical chemistry profiles that show large increases in alanine aminotransferase', '?'),
]

# Check which DABT IDs are covered by our 45 matched answers
matched_ids = set()
if True:
    cursor.execute("""
        SELECT id FROM questions 
        WHERE source_file_id=7 
        AND correct_answer_letter IS NOT NULL AND correct_answer_letter != ''
    """)
    # Count total with answers now
    cursor.execute("""
        SELECT COUNT(*) FROM questions 
        WHERE source_file_id=7 
        AND correct_answer_letter IS NOT NULL AND correct_answer_letter != ''
    """)
    total_now = cursor.fetchone()[0]
    print(f"Total answered in source 7: {total_now}")
    
    cursor.execute("""
        SELECT COUNT(*) FROM questions 
        WHERE source_file_id=7 
        AND (correct_answer_letter IS NULL OR correct_answer_letter = '')
    """)
    still_missing = cursor.fetchone()[0]
    print(f"Still missing: {still_missing}")
    
    cursor.execute("""
        SELECT id FROM questions 
        WHERE source_file_id=7 
        AND correct_answer_letter IS NOT NULL AND correct_answer_letter != ''
    """)
    for row in cursor.fetchall():
        matched_ids.add(row['id'])

# Print the newly answered questions
print("\n=== Questions now answered (previously missing) ===")
cursor.execute("""
    SELECT id, correct_answer_letter, substr(question_text,1,80)
    FROM questions 
    WHERE source_file_id=7 
    AND correct_answer_letter IS NOT NULL AND correct_answer_letter != ''
    ORDER BY id
""")
for row in cursor.fetchall():
    print(f"  {row['id']}: {row['correct_answer_letter']} - {row[2][:60]}...")

conn.close()
