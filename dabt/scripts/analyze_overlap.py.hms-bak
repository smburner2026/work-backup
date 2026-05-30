#!/usr/bin/env python3
"""Identify overlap between exam sets by comparing question content"""
import os
import docx
import re
from pdfminer.high_level import extract_text as pdf_extract
from collections import defaultdict

def extract_docx_text(path):
    doc = docx.Document(path)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_pdf_text(path):
    try:
        return pdf_extract(path)
    except:
        return ""

def get_question_stems(text, max_samples=20):
    """Extract question stems (first 80 chars of each numbered question)"""
    stems = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+[\.\)]\s', line):
            # Clean up the stem
            stem = re.sub(r'^\d+[\.\)]\s+', '', line)
            stem = stem.strip()[:80].lower()
            if stem and len(stem) > 10:
                stems.append(stem)
    return stems

# Mini-ABT_1-11 exams
mini11_exams = {}
BASE1 = "/root/dabt-curated/Practice_Exams/Mini-ABT_1-11"
for f in sorted(os.listdir(BASE1)):
    if f.endswith('.docx') and 'Answer Key' not in f:
        path = os.path.join(BASE1, f)
        text = extract_docx_text(path)
        stems = get_question_stems(text)
        mini11_exams[f] = stems

# Kristen exams (only those without embedded answers - use the standalone ones)
kristen_exams = {}
BASE2 = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

# Use exams without answers as primary source
for f in sorted(os.listdir(BASE2)):
    if f.endswith('.docx') and 'with answers' not in f.lower() and 'answers' not in f.lower():
        # Skip the "answers" standalone file
        if 'answers' in f.lower():
            continue
        path = os.path.join(BASE2, f)
        text = extract_docx_text(path)
        stems = get_question_stems(text)
        kristen_exams[f] = stems

# Also add the "with answers" for completeness
for f in sorted(os.listdir(BASE2)):
    if f.endswith('.docx') and 'with answers' in f.lower():
        path = os.path.join(BASE2, f)
        text = extract_docx_text(path)
        stems = get_question_stems(text)
        kristen_exams[f] = stems

# Past ABT Exams
past_exams = {}
BASE3 = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams"
# Use only unique PDFs
unique_pdfs = [
    "2012_complete_board_questions.pdf",
    "2013_Recert_Examination.pdf",
    "2015_Recert_Examination.pdf",
    "2017_Certification_Part_1_of_2.pdf",
    "2017_Certification_Part_1_of_2_day2.pdf",
    "2017_Certification_Part_2_of_2.pdf",
    "2017_Certification_Part_2_of_2_day2.pdf",
]
for fname in unique_pdfs:
    path = os.path.join(BASE3, fname)
    text = extract_pdf_text(path)
    stems = get_question_stems(text)
    past_exams[fname] = stems

# Now find overlap
print("=== OVERLAP ANALYSIS ===")

# Compare Mini-ABT_1-11 vs Kristen_Mini_Exams
print("\n--- Mini-ABT_1-11 vs Kristen_Mini_Exams ---")
overlap_count = 0
exam1_names = sorted(mini11_exams.keys())
exam2_names = sorted(kristen_exams.keys())

# Build sets of stems
mini11_all = set()
for stems in mini11_exams.values():
    mini11_all.update(stems)

kristen_all = set()
for stems in kristen_exams.values():
    kristen_all.update(stems)

common = mini11_all & kristen_all
print(f"Mini-ABT_1-11 unique stems: {len(mini11_all)}")
print(f"Kristen unique stems: {len(kristen_all)}")
print(f"Common stems: {len(common)}")
if common:
    print(f"  Examples: {list(common)[:5]}")

# Compare Mini-ABT_1-11 vs Past_ABT
print("\n--- Mini-ABT_1-11 vs Past_ABT_Exams ---")
past_all = set()
for stems in past_exams.values():
    past_all.update(stems)

common2 = mini11_all & past_all
print(f"Mini-ABT_1-11 unique stems: {len(mini11_all)}")
print(f"Past ABT unique stems: {len(past_all)}")
print(f"Common stems: {len(common2)}")
if common2:
    print(f"  Examples: {list(common2)[:5]}")

# Compare Kristen vs Past_ABT
print("\n--- Kristen vs Past_ABT_Exams ---")
common3 = kristen_all & past_all
print(f"Kristen unique stems: {len(kristen_all)}")
print(f"Past ABT unique stems: {len(past_all)}")
print(f"Common stems: {len(common3)}")
if common3:
    print(f"  Examples: {list(common3)[:5]}")

# Map which exams in Mini-ABT_1-11 correspond to which in Kristen
print("\n--- Detailed cross-mapping: Mini-ABT_1-11 exam content vs Kristen exams ---")
for e1_name, e1_stems in sorted(mini11_exams.items()):
    e1_set = set(e1_stems)
    best_match = ""
    max_overlap = 0
    for e2_name, e2_stems in sorted(kristen_exams.items()):
        e2_set = set(e2_stems)
        overlap = len(e1_set & e2_set)
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = e2_name
    if max_overlap > 0:
        print(f"  {e1_name} has {len(e1_stems)} Qs -> best match: {best_match} ({max_overlap}/{len(e1_stems)} Qs overlap)")
