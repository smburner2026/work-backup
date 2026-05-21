#!/usr/bin/env python3
"""Find answers by checking ALL text, not just bold formatting."""
import os, re
from docx import Document

EXAM_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

def find_answers_in_file(fname, missing_qnums):
    """Search for any text-based answer indicators in a file."""
    fpath = os.path.join(EXAM_DIR, fname)
    doc = Document(fpath)
    
    print(f"\n{'='*70}")
    print(f"FILE: {fname}")
    print(f"Looking for Q: {missing_qnums}")
    
    current_q = None
    options = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Detect question
        m = re.match(r'^(\d+)[\.\)]\s+', text)
        if m:
            # Process previous question
            if current_q in missing_qnums and options:
                # Look for the correct answer in various ways
                found = None
                for opt in options:
                    # Check for (CORRECT), OK, textbook refs
                    if re.search(r'\bCORRECT\b', opt['full'], re.IGNORECASE) and not re.search(r'\bINCORRECT\b', opt['full'], re.IGNORECASE):
                        found = opt['letter']
                        print(f"  Q{current_q}: {opt['letter']} (via CORRECT marker)")
                        break
                
                if not found:
                    # Print all options for manual inspection
                    print(f"\n  Q{current_q} - NO ANSWER FOUND, options:")
                    for opt in options:
                        print(f"    {opt['letter']}) {opt['full'][:100]}")
            
            current_q = int(m.group(1))
            options = []
            continue
        
        if current_q is not None:
            m_opt = re.match(r'^([A-H])[\.\)]\s+(.*)', text)
            if m_opt:
                letter = m_opt.group(1)
                rest = m_opt.group(2).strip()
                options.append({'letter': letter, 'full': rest})
                continue
            
            # Also check for option in next paragraph
            m_opt2 = re.match(r'^([A-H])[\.\)]\s+(.*)', text)
            if m_opt2:
                options.append({'letter': m_opt2.group(1), 'full': m_opt2.group(2)})
    
    # Don't forget to process last question
    if current_q in missing_qnums and options:
        print(f"\n  Q{current_q} - at end, options:")
        for opt in options:
            print(f"    {opt['letter']}) {opt['full'][:100]}")


# 05 May missing: 12, 13, 14, 15, 26, 27, 28, 29, 30
find_answers_in_file("Mini-ABT exam with answers 05 May 2017.docx", {12, 13, 14, 15, 26, 27, 28, 29, 30})

# 11 August missing: 16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 36, 37, 38, 39, 40
find_answers_in_file("Mini-ABT exam with answers for 11 August 2017.docx", {16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 36, 37, 38, 39, 40})

# 02 June missing: 11, 12, 13, 25, 26, 27
find_answers_in_file("Mini-ABT examination with answers 02 June 2017.docx", {11, 12, 13, 25, 26, 27})

# 22 Sept missing: (none, has 50 answers for 50 texts)
# 21 July missing: Q1
find_answers_in_file("Mini-ABT exam with answers 21 July 2017.docx", {1})
