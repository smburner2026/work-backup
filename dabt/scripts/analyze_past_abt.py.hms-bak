#!/usr/bin/env python3
"""Analyze Past_ABT_Exams files (.docx, .pdf, .pptx, .xlsx)"""
import os
import re
import docx
from pdfminer.high_level import extract_text as pdf_extract_text

BASE = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams"

def extract_docx(path):
    doc = docx.Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def extract_pdf(path):
    try:
        text = pdf_extract_text(path)
        return text
    except Exception as e:
        return f"[PDF extraction error: {e}]"

def analyze_text(text, fname):
    lines = text.split('\n')
    numbered = 0
    q_marked = 0
    mc_indicators = 0
    
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+[\.\)]', line):
            numbered += 1
        if '?' in line:
            q_marked += 1
        if re.match(r'^[A-E][\.\)]', line):
            mc_indicators += 1
    
    return {
        'filename': fname,
        'total_lines': len(lines),
        'numbered_lines': numbered,
        'question_marks': q_marked,
        'mc_option_lines': mc_indicators,
        'preview': text[:800]
    }

def main():
    # Get all files recursively
    all_files = []
    for root, dirs, files in os.walk(BASE):
        for f in files:
            full = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            all_files.append((full, f, ext))
    
    all_files.sort(key=lambda x: x[1])
    
    print(f"=== Past_ABT_Exams: {len(all_files)} files ===")
    
    docx_files = [x for x in all_files if x[2] == '.docx']
    pdf_files = [x for x in all_files if x[2] == '.pdf']
    pptx_files = [x for x in all_files if x[2] == '.pptx']
    xlsx_files = [x for x in all_files if x[2] == '.xlsx']
    
    print(f"DOCX: {len(docx_files)}, PDF: {len(pdf_files)}, PPTX: {len(pptx_files)}, XLSX: {len(xlsx_files)}")
    
    print("\n\n=== PDF FILES ===")
    for full, fname, ext in pdf_files:
        print(f"\n--- {fname} ---")
        text = extract_pdf(full)
        result = analyze_text(text, fname)
        print(f"  Lines: {result['total_lines']}")
        print(f"  Numbered items: {result['numbered_lines']}")
        print(f"  Question marks: {result['question_marks']}")
        print(f"  MC option lines (A-E): {result['mc_option_lines']}")
        print(f"  Preview: {result['preview'][:600]}")
    
    print("\n\n=== DOCX FILES ===")
    for full, fname, ext in docx_files:
        print(f"\n--- {fname} ---")
        text = extract_docx(full)
        result = analyze_text(text, fname)
        print(f"  Lines: {result['total_lines']}")
        print(f"  Numbered items: {result['numbered_lines']}")
        print(f"  Question marks: {result['question_marks']}")
        print(f"  MC option lines (A-E): {result['mc_option_lines']}")
        print(f"  Preview: {result['preview'][:600]}")
    
    print("\n\n=== PPTX FILES SUMMARY ===")
    for full, fname, ext in pptx_files:
        print(f"  {fname} (need python-pptx to analyze)")
    
    print("\n\n=== XLSX FILES SUMMARY ===")
    for full, fname, ext in xlsx_files:
        print(f"  {fname} (need openpyxl to analyze)")

if __name__ == '__main__':
    main()
