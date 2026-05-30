#!/usr/bin/env python3
"""
Extract question fingerprints from 2000Q Question Bank docx files.
Output: /tmp/2000q_fingerprints.csv with columns: File, QuestionNumber, Fingerprint, FullText
v2 - Better filtering of answer entries that look like "1073. D (I)"
"""

import os
import re
import csv
import glob

WORK_DIR = '/root/dabt-curated/2000Q_Question_Bank'
OUTPUT_CSV = '/tmp/2000q_fingerprints.csv'

def clean_text_for_fingerprint(text):
    """Clean: lowercase, strip punctuation, collapse whitespace, take first 80 chars."""
    t = text.lower()
    t = re.sub(r'[^\w\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:80]

def is_answer_key_section(text):
    """Check if a paragraph marks the start of answer key section."""
    text_upper = text.strip().upper()
    if re.match(r'^CHAPTER\s+\d+\s+ANSWERS', text_upper):
        return True
    if re.match(r'^CHAPTER\s+\d+\s+ANSWERS', text_upper):
        return True
    return False

def is_question_start(text):
    """Check if a paragraph starts with a question number like '1.' or '552.'"""
    stripped = text.strip()
    m = re.match(r'^(\d+)\.\s', stripped)
    if m:
        num = int(m.group(1))
        if 1 <= num <= 1999:
            # Check if this is actually an answer entry like "1073. D (I)" or "1073. A"
            # Answer entries have only a single letter/number after the period
            rest = stripped[m.end():].strip()
            # If the rest is very short (just 1-2 chars + optional parens), it's likely an answer
            # e.g. "D (I)", "A", "B (II)", "C (III)"
            rest_stripped = rest.replace(' ', '').replace('(', '').replace(')', '')
            if len(rest_stripped) <= 5 and re.match(r'^[A-Za-z0-9]+(?:\([A-Za-z0-9]+\))?$', rest.replace(' ', '')):
                # Could be an answer entry. But some short questions exist too like "44. antagonism"
                # Let's be more careful: if it's just a single letter with roman numeral, skip
                if re.match(r'^[A-Za-z]\s*(?:\([IVXLCDM]+\))?$', rest):
                    return None  # Skip answer entries like "D (I)"
            return num
    return None

def is_section_header(text):
    """Check if paragraph is a section header like '1  TOXICOLOGIC PRINCIPLES'"""
    stripped = text.strip()
    if re.match(r'^\d{1,2}\s{2,}[A-Z]', stripped):
        return True
    if re.match(r'^\d{1,2}\s+[A-Z]', stripped):
        return True
    return False

def extract_questions_from_docx(filepath):
    import docx
    doc = docx.Document(filepath)
    
    questions = []
    current_num = None
    current_text_lines = []
    in_answer_key = False
    
    for para in doc.paragraphs:
        text = para.text
        stripped = text.strip()
        
        if not stripped:
            continue
        
        # Check for answer key section
        if is_answer_key_section(stripped):
            in_answer_key = True
            if current_num is not None and current_text_lines:
                full_text = ' '.join(current_text_lines)
                questions.append((current_num, full_text))
                current_num = None
                current_text_lines = []
            break
        
        # Skip section headers
        if current_num is None and not current_text_lines and is_section_header(stripped):
            continue
        
        # Check if this paragraph starts a new question
        qnum = is_question_start(stripped)
        if qnum is not None:
            # Save previous question if exists
            if current_num is not None and current_text_lines:
                full_text = ' '.join(current_text_lines)
                questions.append((current_num, full_text))
            
            # Start new question
            current_num = qnum
            rest_text = re.sub(r'^\d+\.\s*', '', stripped, count=1)
            current_text_lines = [rest_text]
        else:
            # Continuation of current question
            if current_num is not None:
                current_text_lines.append(stripped)
            # If no current question, skip
    
    # Flush last question
    if current_num is not None and current_text_lines:
        full_text = ' '.join(current_text_lines)
        questions.append((current_num, full_text))
    
    return questions


def main():
    pattern = os.path.join(WORK_DIR, '2000Q*.docx')
    files = sorted(glob.glob(pattern))
    
    print(f"Found {len(files)} docx files to process")
    
    all_questions = []
    
    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"Processing: {filename}...", end=' ', flush=True)
        try:
            questions = extract_questions_from_docx(filepath)
            for qnum, full_text in questions:
                fp = clean_text_for_fingerprint(full_text)
                full_text_trunc = full_text[:200]
                all_questions.append((filename, qnum, fp, full_text_trunc))
            print(f"OK - {len(questions)} questions found")
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Sort by question number
    all_questions.sort(key=lambda x: x[1])
    
    # Write CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['File', 'QuestionNumber', 'Fingerprint', 'FullText'])
        for row in all_questions:
            writer.writerow(row)
    
    print(f"\nDone! Wrote {len(all_questions)} questions to {OUTPUT_CSV}")
    
    if all_questions:
        qnums = [r[1] for r in all_questions]
        print(f"Question number range: {min(qnums)} - {max(qnums)}")
        unique_qnums = len(set(qnums))
        print(f"Unique question numbers: {unique_qnums}")
        print(f"Total rows: {len(all_questions)}")
        
        # Check for cross-file duplicates (same fingerprint in different files)
        seen_fp = {}
        for filename, qnum, fp, _ in all_questions:
            key = (qnum, fp)
            if key in seen_fp:
                prev_file = seen_fp[key]
                if prev_file != filename:
                    print(f"  CROSS-FILE DUPE: Q{qnum} in {prev_file} and {filename}")
            seen_fp[key] = filename
        
        # Check for within-file duplicates
        from collections import Counter
        seen_within = Counter((r[0], r[1]) for r in all_questions)
        multi = {k: v for k, v in seen_within.items() if v > 1}
        if multi:
            print(f"Within-file duplicates: {len(multi)}")
            for (f, q), cnt in list(multi.items())[:5]:
                print(f"  Q{q} appears {cnt}x in {f}")
        
        # Check for gaps
        all_nums = sorted(set(qnums))
        gaps = []
        for i in range(len(all_nums) - 1):
            if all_nums[i+1] - all_nums[i] > 1:
                gaps.append((all_nums[i], all_nums[i+1]))
        if gaps:
            print(f"Gaps found: {len(gaps)}")
            for g in gaps[:10]:
                print(f"  Gap between Q{g[0]} and Q{g[1]}")
        else:
            print("No gaps in question numbers!")

if __name__ == '__main__':
    main()
