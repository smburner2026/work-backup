#!/usr/bin/env python3
"""Analyze Mini-ABT_1-11 exam files (.docx)"""
import docx
import os
import re
from collections import Counter

BASE = "/root/dabt-curated/Practice_Exams/Mini-ABT_1-11"

def extract_text(path):
    doc = docx.Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def count_questions(text):
    """Try to count questions by looking for numbered lists (1., 2., etc.) or question marks."""
    # Look for patterns like "1.", "1)", "1)" at start of lines
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
        if re.match(r'^[A-D][\.\)]', line):
            mc_indicators += 1
    
    return {
        'numbered_lines': numbered,
        'lines_with_question_marks': q_marked,
        'mc_option_lines': mc_indicators,
        'total_lines': len(lines)
    }

def extract_topics(text):
    """Extract topic-like content from text."""
    topics = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip().lower()
        # Look for section headers or topic indicators
        if any(kw in line for kw in ['toxicology', 'toxicity', 'carcinogen', 'mutagen', 
                                      'reproductive', 'developmental', 'neurotoxic',
                                      'dose', 'exposure', 'risk', 'safety', 'adverse',
                                      'pathology', 'pharmacokinetic', 'metabolism',
                                      'mechanism', 'organ', 'liver', 'kidney', 'blood',
                                      'cancer', 'genotoxic', 'ecotoxicology', 'environmental',
                                      'regulatory', 'guideline', 'oecd', 'epa', 'fda',
                                      'statistics', 'noael', 'loael', 'benchmark',
                                      'acute', 'chronic', 'subchronic', 'dermal',
                                      'inhalation', 'oral', 'intravenous',
                                      'study design', 'animal', 'rodent', 'rat', 'mouse',
                                      'in vitro', 'in vivo', 'cell', 'tissue']):
            topics.append(line[:100])
    return topics

def main():
    files = sorted(os.listdir(BASE))
    print(f"=== Mini-ABT_1-11: {len(files)} files ===")
    
    exam_files = [f for f in files if 'Answer Key' not in f and f.endswith('.docx')]
    key_files = [f for f in files if 'Answer Key' in f]
    
    print(f"\nExam files ({len(exam_files)}):")
    for f in sorted(exam_files):
        path = os.path.join(BASE, f)
        text = extract_text(path)
        stats = count_questions(text)
        print(f"\n--- {f} ---")
        print(f"  Lines: {stats['total_lines']}")
        print(f"  Numbered items: {stats['numbered_lines']}")
        print(f"  Lines with ?: {stats['lines_with_question_marks']}")
        print(f"  MC option lines (A-D): {stats['mc_option_lines']}")
        # Print first 500 chars to see format
        print(f"  Preview: {text[:500]}")
    
    print(f"\n\nAnswer Key files ({len(key_files)}):")
    for f in sorted(key_files):
        path = os.path.join(BASE, f)
        text = extract_text(path)
        print(f"\n--- {f} ---")
        print(f"  Lines: {len(text.split(chr(10)))}")
        print(f"  Content: {text[:800]}")

if __name__ == '__main__':
    main()
