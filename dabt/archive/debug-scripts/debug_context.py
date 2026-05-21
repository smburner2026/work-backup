#!/usr/bin/env python3
"""Dump full context around unmatched questions to find non-bold answers."""
import os, re
from docx import Document

EXAM_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

def dump_question_context(fname, target_qnums):
    fpath = os.path.join(EXAM_DIR, fname)
    doc = Document(fpath)
    
    print(f"\n{'='*70}")
    print(f"FILE: {fname}")
    print(f"{'='*70}")
    
    capture = False
    lines_since_q = 999
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Check if this is a question line
        m = re.match(r'^(\d+)[\.\)]\s+', text)
        if m:
            qnum = int(m.group(1))
            if qnum in target_qnums:
                capture = True
                lines_since_q = 0
                print(f"\n--- Q{qnum} ---")
                print(f"  Q: {text[:120]}")
                # Check bold on question
                bold = [r.text for r in para.runs if r.bold]
                if bold:
                    print(f"  BOLD: {''.join(bold)[:80]}")
                continue
            elif capture and lines_since_q < 20:
                pass  # still capturing options for current target
            else:
                capture = False
                lines_since_q = 999
        
        if capture and lines_since_q < 20:
            lines_since_q += 1
            bold = [r.text for r in para.runs if r.bold]
            bold_mark = " [BOLD]" if bold else ""
            print(f"  {text[:120]}{bold_mark}")

# Check 05 May for Q14, Q15, Q26, Q29, Q30
dump_question_context("Mini-ABT exam with answers 05 May 2017.docx", {14, 15, 26, 29, 30})

# Check 11 August for Q16, Q26-Q29, Q36-Q40
dump_question_context("Mini-ABT exam with answers for 11 August 2017.docx", {16, 17, 18, 19, 20, 26, 27, 28, 29, 36, 37, 38, 39, 40})
