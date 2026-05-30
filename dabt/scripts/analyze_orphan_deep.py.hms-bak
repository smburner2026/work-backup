#!/usr/bin/env python3
"""Deep comparison: match orphan questions to answer-key file answers."""

import os
import re
from docx import Document

KRISTEN_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"
ORPHAN_FILE = os.path.join(KRISTEN_DIR, "Mini-ABT exam 21 July 2017.docx")

def extract_all_text(doc_path):
    doc = Document(doc_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return paragraphs

def extract_questions_with_options(paragraphs):
    """Extract questions as list of (q_num, q_text, options_list)."""
    questions = []
    i = 0
    while i < len(paragraphs):
        p = paragraphs[i]
        # Check if this starts with a number followed by period or paren
        m = re.match(r'^(\d+)\.\s+(.*)', p)
        if m:
            q_num = int(m.group(1))
            q_text = m.group(2)
            options = []
            i += 1
            # Collect options (A., B., C., D., etc.)
            while i < len(paragraphs):
                opt = paragraphs[i]
                if re.match(r'^[A-Z][\.\)]\s', opt) or re.match(r'^[A-Z]\.\s', opt):
                    options.append(opt)
                    i += 1
                elif re.match(r'^\d+\.\s', opt):
                    # Next question starts
                    break
                elif opt.startswith('E.') or opt.startswith('F.') or opt.startswith('G.') or \
                     opt.startswith('H.') or opt.startswith('I.') or opt.startswith('J.'):
                    options.append(opt)
                    i += 1
                else:
                    # Could be continuation of last option or something else
                    if options and len(opt) > 3:
                        options[-1] = options[-1] + ' ' + opt
                    i += 1
            questions.append((q_num, q_text, options))
        else:
            i += 1
    return questions

def extract_questions_loose(paragraphs):
    """Extract questions using a more lenient approach."""
    questions = {}
    current_num = None
    current_lines = []
    
    for p in paragraphs:
        m = re.match(r'^(\d+)\.\s+(.*)', p)
        if m:
            if current_num is not None:
                questions[current_num] = ' '.join(current_lines)
            current_num = int(m.group(1))
            current_lines = [p]
        elif current_num is not None:
            current_lines.append(p)
    
    if current_num is not None:
        questions[current_num] = ' '.join(current_lines)
    
    return questions

# Load orphan
orphan_text = extract_all_text(ORPHAN_FILE)
orphan_qs = extract_questions_loose(orphan_text)

print("=" * 70)
print("ORPHAN EXAM QUESTIONS (21 July 2017)")
print("=" * 70)
for qnum in sorted(orphan_qs.keys()):
    text = orphan_qs[qnum]
    print(f"\nQ{qnum}: {text[:200]}")

# Now search for these question texts in ALL answer-key files
print("\n" + "=" * 70)
print("SEARCHING FOR MATCHING QUESTIONS IN ANSWER-KEY FILES")
print("=" * 70)

answer_key_files = [f for f in os.listdir(KRISTEN_DIR) 
                    if f.endswith('.docx') and ('answers' in f.lower() or 'Answers' in f)]
answer_key_files.sort()

# Build question bank from all answer key files
all_ak_questions = {}  # question_text -> (file, full_text)

for akf in answer_key_files:
    ak_path = os.path.join(KRISTEN_DIR, akf)
    ak_text = extract_all_text(ak_path)
    ak_qs = extract_questions_loose(ak_text)
    for qnum, qtext in ak_qs.items():
        # Truncate to first 100 chars as key for matching
        key = qtext[:100].strip().lower()
        if key not in all_ak_questions:
            all_ak_questions[key] = []
        all_ak_questions[key].append((akf, qnum, qtext))

# For each orphan question, try to find the same question in any answer key
found_answers = {}
unmatched = []

for qnum in sorted(orphan_qs.keys()):
    qtext = orphan_qs[qnum]
    key = qtext[:100].strip().lower()
    
    matches = []
    for ak_key, entries in all_ak_questions.items():
        # Check if question stems match (first 60 chars)
        qstem = qtext[:80].strip().lower()
        for ak_file, ak_qnum, ak_fulltext in entries:
            ak_stem = ak_fulltext[:80].strip().lower()
            # Simple overlap score
            overlap = len(set(qstem.split()) & set(ak_stem.split()))
            union = len(set(qstem.split()) | set(ak_stem.split()))
            score = overlap / union if union > 0 else 0
            if score > 0.5:
                matches.append((score, ak_file, ak_qnum, ak_fulltext))
    
    matches.sort(reverse=True)
    if matches:
        best_score, best_file, best_qnum, best_fulltext = matches[0]
        found_answers[qnum] = (best_score, best_file, best_qnum, best_fulltext)
        print(f"\nQ{qnum}: MATCH FOUND (score={best_score:.2f}) in {best_file} Q{best_qnum}")
        print(f"  Orphan: {qtext[:120]}...")
        print(f"  Match:  {best_fulltext[:120]}...")
    else:
        unmatched.append(qnum)
        print(f"\nQ{qnum}: NO MATCH found in any answer key file")
        print(f"  Text: {qtext[:120]}...")

print("\n" + "=" * 70)
print(f"MATCHED: {len(found_answers)} questions")
print(f"UNMATCHED: {len(unmatched)} questions")
print(f"Unmatched question numbers: {unmatched}")

# Now try to extract answer text from the matched files
print("\n" + "=" * 70)
print("EXTRACTING ANSWERS FROM MATCHED FILES")
print("=" * 70)

for qnum in sorted(found_answers.keys()):
    score, ak_file, ak_qnum, ak_text = found_answers[qnum]
    ak_path = os.path.join(KRISTEN_DIR, ak_file)
    
    # Read the full file to find answers near the matched question
    full_text = extract_all_text(ak_path)
    
    # Find the position of the question
    q_idx = -1
    for idx, p in enumerate(full_text):
        if p.strip().startswith(f"{ak_qnum}.") or p.strip().startswith(f"{ak_qnum})"):
            q_idx = idx
            break
    
    if q_idx >= 0:
        # Look for answer markers in the subsequent text
        print(f"\nQ{qnum}: Context from {ak_file} (starting at line {q_idx}):")
        for j in range(q_idx, min(q_idx + 15, len(full_text))):
            print(f"  [{j}] {full_text[j][:150]}")
    else:
        print(f"\nQ{qnum}: Could not find exact position in {ak_file}")
        # Show the matched text snippet
        print(f"  Matched text: {ak_text[:200]}")
