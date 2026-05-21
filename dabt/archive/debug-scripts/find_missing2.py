#!/usr/bin/env python3
"""Find answers - fixed logic."""
import os, re
from docx import Document

EXAM_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

def find_answers_in_file(fname, missing_qnums):
    fpath = os.path.join(EXAM_DIR, fname)
    doc = Document(fpath)
    
    print(f"\n{'='*70}")
    print(f"FILE: {fname}")
    
    prev_q = None
    prev_options = []
    current_q = None
    current_options = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        m = re.match(r'^(\d+)[\.\)]\s+', text)
        if m:
            # Save current as prev, process prev
            if current_q is not None:
                if current_q in missing_qnums:
                    found = None
                    for opt in current_options:
                        if re.search(r'\bCORRECT\b', opt['full'], re.IGNORECASE) and not re.search(r'\bINCORRECT\b', opt['full'], re.IGNORECASE):
                            found = opt['letter']
                            print(f"  Q{current_q}: {opt['letter']} (CORRECT marker)")
                            break
                    
                    if not found:
                        for opt in current_options:
                            if 'CORRECT' in opt['full'].upper() and 'INCORRECT' not in opt['full'].upper():
                                found = opt['letter']
                                print(f"  Q{current_q}: {opt['letter']} (CORRECT uppercase)")
                                break
                    
                    if not found and any('(OK)' in opt['full'] for opt in current_options):
                        for opt in current_options:
                            if '(OK)' in opt['full']:
                                found = opt['letter']
                                print(f"  Q{current_q}: {opt['letter']} (OK marker)")
                                break
                    
                    if not found:
                        print(f"\n  Q{current_q} - options (no answer found):")
                        for opt in current_options:
                            print(f"    {opt['letter']}) {opt['full'][:120]}")
            
            current_q = int(m.group(1))
            current_options = []
            continue
        
        if current_q is not None:
            m_opt = re.match(r'^([A-H])[\.\)]\s+(.*)', text)
            if m_opt:
                current_options.append({'letter': m_opt.group(1), 'full': m_opt.group(2)})
    
    # Process last question
    if current_q is not None and current_q in missing_qnums:
        found = None
        for opt in current_options:
            if re.search(r'\bCORRECT\b', opt['full'], re.IGNORECASE) and not re.search(r'\bINCORRECT\b', opt['full'], re.IGNORECASE):
                found = opt['letter']
                print(f"  Q{current_q}: {opt['letter']} (CORRECT marker)")
                break
        
        if not found:
            print(f"\n  Q{current_q} - options (no answer found):")
            for opt in current_options:
                print(f"    {opt['letter']}) {opt['full'][:120]}")

# Missing questions by file
find_answers_in_file("Mini-ABT exam with answers 05 May 2017.docx", {12, 14, 15, 26, 29, 30})
find_answers_in_file("Mini-ABT exam with answers for 11 August 2017.docx", {26, 27, 28, 29})
find_answers_in_file("Mini-ABT examination with answers 02 June 2017.docx", {25, 26, 27})
