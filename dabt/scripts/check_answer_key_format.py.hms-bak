#!/usr/bin/env python3
"""Find explicit answer keys in the answer key files."""

import os
from docx import Document

KRISTEN_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

# Check a few specific files for answer key format
files_to_check = [
    "Mini-ABT examination with answers 02 June 2017.docx",
    "Mini-ABT exam answers 26 May 2017.docx",
    "Mini-ABT exam with answers 28 July 2017-PART B.docx",
    "Mini-ABT exam with answers 23 June 2017.docx",
    "Mini-ABT exam with answers 05 May 2017.docx",
]

for fname in files_to_check:
    fpath = os.path.join(KRISTEN_DIR, fname)
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fname}")
        continue
    
    doc = Document(fpath)
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    print(f"\n{'='*70}")
    print(f"FILE: {fname} ({len(paras)} paragraphs)")
    print(f"{'='*70}")
    
    # Look for answer key patterns
    key_patterns = ['Answer key', 'Answer Key', 'ANSWERS', 'answer:', 'Answers:']
    found_key = False
    for i, p in enumerate(paras):
        if any(kp in p for kp in key_patterns):
            print(f"  [{i}] {p[:200]}")
            found_key = True
            # Print next few lines
            for j in range(i+1, min(i+10, len(paras))):
                print(f"  [{j}] {paras[j][:200]}")
    
    if not found_key:
        print(f"  No explicit answer key section found.")
    
    # Check first 30 lines for structure
    print(f"\n  First 30 paragraphs:")
    for i, p in enumerate(paras[:30]):
        print(f"  [{i}] {p[:150]}")
    
    # Check last 30 lines for answer summary
    print(f"\n  Last 30 paragraphs:")
    for i, p in enumerate(paras[-30:]):
        print(f"  [{len(paras)-30+i}] {p[:150]}")
