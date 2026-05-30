#!/usr/bin/env python3
"""
Extract question fingerprints from 2000Q Question Bank docx files.
Output: /tmp/2000q_fingerprints.csv with columns: File, QuestionNumber, Fingerprint, FullText
v3 - Better detection of answer key sections embedded mid-paragraph
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

def contains_answer_key_header(text):
    """Check if text contains an answer key header like 'CHAPTER X ANSWERS'."""
    return bool(re.search(r'CHAPTER\s+\d+\s+ANSWERS', text.upper()))

def is_answer_entry(text):
    """
    Check if text is an answer entry like '1073. D (I)' or '1691. C (I)'.
    These have a number, period, then just a letter + optional roman numeral.
    """
    stripped = text.strip()
    m = re.match(r'^(\d+)\.\s+([A-Z])', stripped)
    if not m:
        return False
    rest = stripped[m.end():].strip()
    # If what follows is just optional roman numeral in parens and nothing else
    if rest == '':
        return True
    if re.match(r'^\([IVXLCDM]+\)\s*$', rest):
        return True
    return False

def is_question_start(text):
    """Check if a paragraph starts with a question number like '1.' or '552.'"""
    stripped = text.strip()
    m = re.match(r'^(\d+)\.\s', stripped)
    if m:
        num = int(m.group(1))
        if 1 <= num <= 1999:
            # Check if it's actually an answer entry (single letter after number)
            if is_answer_entry(stripped):
                return None
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
    max_qnum_seen = 0
    
    for para in doc.paragraphs:
        text = para.text
        stripped = text.strip()
        
        if not stripped:
            continue
        
        # Check for answer key section header embedded anywhere in text
        if contains_answer_key_header(stripped):
            in_answer_key = True
            # Flush current question
            if current_num is not None and current_text_lines:
                full_text = ' '.join(current_text_lines)
                questions.append((current_num, full_text))
                current_num = None
                current_text_lines = []
            # If there's question text before the answer header on this line,
            # try to extract it
            parts = re.split(r'CHAPTER\s+\d+\s+ANSWERS', stripped, maxsplit=1, flags=re.IGNORECASE)
            if len(parts) > 1 and parts[0].strip():
                # There might be a question in the first part
                before = parts[0].strip()
                qnum = is_question_start(before)
                if qnum is not None:
                    rest_text = re.sub(r'^\d+\.\s*', '', before, count=1)
                    questions.append((qnum, rest_text))
            break
        
        # Skip section headers
        if current_num is None and not current_text_lines and is_section_header(stripped):
            continue
        
        # Check if this paragraph starts a new question
        qnum = is_question_start(stripped)
        if qnum is not None:
            # If we see a question number lower than what we've already seen,
            # we might be in an answer key section
            if qnum < max_qnum_seen - 50:  # Allow some wiggle room for out-of-order
                in_answer_key = True
                if current_num is not None and current_text_lines:
                    full_text = ' '.join(current_text_lines)
                    questions.append((current_num, full_text))
                    current_num = None
                    current_text_lines = []
                break
            
            # Save previous question
            if current_num is not None and current_text_lines:
                full_text = ' '.join(current_text_lines)
                questions.append((current_num, full_text))
            
            # Start new question
            current_num = qnum
            max_qnum_seen = max(max_qnum_seen, qnum)
            rest_text = re.sub(r'^\d+\.\s*', '', stripped, count=1)
            current_text_lines = [rest_text]
        else:
            # Check if this paragraph starts with an answer entry pattern
            # (like just "D (I)") - if so, we're probably in answer key
            if re.match(r'^[A-Z]\s*\([IVXLCDM]+\)', stripped):
                in_answer_key = True
                if current_num is not None and current_text_lines:
                    full_text = ' '.join(current_text_lines)
                    questions.append((current_num, full_text))
                    current_num = None
                    current_text_lines = []
                break
            
            # Continuation of current question
            if not in_answer_key and current_num is not None:
                current_text_lines.append(stripped)
    
    # Flush last question
    if not in_answer_key and current_num is not None and current_text_lines:
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
            import traceback
            traceback.print_exc()
    
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
        
        # Check for within-file duplicates
        from collections import Counter
        seen_within = Counter((r[0], r[1]) for r in all_questions)
        multi = {k: v for k, v in seen_within.items() if v > 1}
        if multi:
            print(f"\nWithin-file duplicates: {len(multi)}")
            for (f, q), cnt in list(multi.items())[:10]:
                rows_for_q = [r for r in all_questions if r[0] == f and r[1] == q]
                for r in rows_for_q:
                    print(f'  Q{q} in {f}: [{r[2][:60]}...]')
        else:
            print("No within-file duplicates!")
        
        # Check for cross-file duplicates
        seen_fp = {}
        cross_dupes = 0
        for filename, qnum, fp, _ in all_questions:
            key = (qnum, fp)
            if key in seen_fp:
                prev_file = seen_fp[key]
                if prev_file != filename:
                    cross_dupes += 1
            seen_fp[key] = filename
        if cross_dupes:
            print(f"Cross-file duplicates: {cross_dupes}")
        else:
            print("No cross-file duplicates!")
        
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
