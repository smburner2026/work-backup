#!/usr/bin/env python3
"""Analyze Kristen_Mini_Exams files (.docx)"""
import docx
import os
import re

BASE = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

def extract_text(path):
    doc = docx.Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def analyze_exam(path, fname):
    text = extract_text(path)
    lines = text.split('\n')
    
    numbered = 0
    q_marked = 0
    mc_A = 0
    mc_B = 0
    mc_C = 0
    mc_D = 0
    mc_E = 0
    
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+[\.\)]', line):
            numbered += 1
        if '?' in line:
            q_marked += 1
        if re.match(r'^A[\.\)]', line):
            mc_A += 1
        if re.match(r'^B[\.\)]', line):
            mc_B += 1
        if re.match(r'^C[\.\)]', line):
            mc_C += 1
        if re.match(r'^D[\.\)]', line):
            mc_D += 1
        if re.match(r'^E[\.\)]', line):
            mc_E += 1
    
    return {
        'filename': fname,
        'total_lines': len(lines),
        'numbered_lines': numbered,
        'question_marks': q_marked,
        'mc_A_count': mc_A,
        'mc_B_count': mc_B,
        'mc_C_count': mc_C,
        'mc_D_count': mc_D,
        'mc_E_count': mc_E,
        'preview': text[:600]
    }

def main():
    files = sorted(os.listdir(BASE))
    print(f"=== Kristen_Mini_Exams: {len(files)} files ===")
    
    has_answers = [f for f in files if 'with answers' in f.lower()]
    no_answers = [f for f in files if 'with answers' not in f.lower()]
    
    print(f"Exams with answers embedded: {len(has_answers)}")
    print(f"Exams without/in separate answer keys: {len(no_answers)}")
    
    print("\n\n=== EXAMS WITHOUT EMBEDDED ANSWERS ===")
    for f in sorted(no_answers):
        path = os.path.join(BASE, f)
        result = analyze_exam(path, f)
        print(f"\n--- {result['filename']} ---")
        print(f"  Lines: {result['total_lines']}")
        print(f"  Numbered items (questions): {result['numbered_lines']}")
        print(f"  Lines with ?: {result['question_marks']}")
        print(f"  MC options - A:{result['mc_A_count']} B:{result['mc_B_count']} C:{result['mc_C_count']} D:{result['mc_D_count']} E:{result['mc_E_count']}")
        print(f"  Preview: {result['preview'][:400]}")
    
    print("\n\n=== EXAMS WITH EMBEDDED ANSWERS ===")
    for f in sorted(has_answers):
        path = os.path.join(BASE, f)
        result = analyze_exam(path, f)
        print(f"\n--- {result['filename']} ---")
        print(f"  Lines: {result['total_lines']}")
        print(f"  Numbered items (questions): {result['numbered_lines']}")
        print(f"  Lines with ?: {result['question_marks']}")
        print(f"  MC options - A:{result['mc_A_count']} B:{result['mc_B_count']} C:{result['mc_C_count']} D:{result['mc_D_count']} E:{result['mc_E_count']}")
        print(f"  Preview: {result['preview'][:500]}")

if __name__ == '__main__':
    main()
