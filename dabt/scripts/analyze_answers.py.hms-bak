#!/usr/bin/env python3
"""Extract actual answer choices from answer key files for matched questions."""

import os
import re
from docx import Document
from docx.document import Document as DocumentType

KRISTEN_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"
ORPHAN_FILE = os.path.join(KRISTEN_DIR, "Mini-ABT exam 21 July 2017.docx")

def extract_all_text(doc_path):
    doc = Document(doc_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return paragraphs

def extract_text_with_format(doc_path):
    """Extract text and detect bold formatting (often used for answers)."""
    doc = Document(doc_path)
    result = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        # Check if any run is bold
        has_bold = any(run.bold for run in p.runs if run.text.strip())
        result.append((text, has_bold))
    return result

# Q6 match: Mini-ABT exam answers 26 May 2017.docx - need to find which answer is correct
print("=" * 70)
print("EXAMINING MATCHED ANSWER KEY FILES FOR ACTUAL ANSWERS")
print("=" * 70)

# Q37, Q38, Q39, Q40 match: Mini-ABT examination with answers 02 June 2017.docx
print("\n--- Mini-ABT examination with answers 02 June 2017.docx (matched: Q37-40) ---")
ak_path = os.path.join(KRISTEN_DIR, "Mini-ABT examination with answers 02 June 2017.docx")
paras = extract_text_with_format(ak_path)
print(f"Total paragraphs with formatting info: {len(paras)}")

# Look for answer markers near questions 37-40
for i, (text, bold) in enumerate(paras):
    if any(text.startswith(f"{n}.") for n in range(37, 41)):
        print(f"  [{i}] {'[BOLD]' if bold else '      '} {text[:200]}")

# Q6 match: Mini-ABT exam answers 26 May 2017.docx
print("\n--- Mini-ABT exam answers 26 May 2017.docx (matched: Q6 -> their Q33) ---")
ak_path2 = os.path.join(KRISTEN_DIR, "Mini-ABT exam answers 26 May 2017.docx")
paras2 = extract_all_text(ak_path2)

# Find Q33 and look for answer indicator
for i, p in enumerate(paras2):
    if '33.' in p:
        print(f"  Found Q33 at line {i}")
        # Print context
        for j in range(max(0, i-2), min(len(paras2), i+20)):
            print(f"  [{j}] {paras2[j][:150]}")
        break

# Q26 match: Mini-ABT exam with answers 28 July 2017-PART B.docx Q10
print("\n--- Mini-ABT exam with answers 28 July 2017-PART B.docx (matched: Q26 -> their Q10) ---")
ak_path3 = os.path.join(KRISTEN_DIR, "Mini-ABT exam with answers 28 July 2017-PART B.docx")
paras3 = extract_all_text(ak_path3)

# Find Q10 and look for answer
for i, p in enumerate(paras3):
    if p.startswith('10.') or p == '10.':
        print(f"  Found Q10 at line {i}")
        for j in range(i, min(len(paras3), i+15)):
            print(f"  [{j}] {paras3[j][:150]}")
        break

# Also check what answers look like in 02 June 2017 - find explicit answer marks
print("\n--- Looking for explicit answer markers in 02 June 2017 ---")
for i, (text, bold) in enumerate(paras):
    # Look for patterns like "Answer:" or "Ans:" or asterisk
    if any(marker in text.lower() for marker in ['answer', 'ans:', 'correct answer']):
        print(f"  [{i}] {'[BOLD]' if bold else '      '} {text[:200]}")
    # Also check for asterisks which might mark answers
    if text.startswith('*') or text.startswith('* '):
        print(f"  [{i}] {'[BOLD]' if bold else '      '} {text[:200]}")
