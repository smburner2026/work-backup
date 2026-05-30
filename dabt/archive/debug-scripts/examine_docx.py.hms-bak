#!/usr/bin/env python3
"""Examine the structure of a "with answers" docx file."""
import sys
from docx import Document

path = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams/Mini-ABT exam with answers 26 August 2017.docx"
doc = Document(path)

# Print all paragraphs with their style and runs info
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if not text:
        continue
    # Check for bold runs
    bold_runs = []
    for run in para.runs:
        if run.bold:
            bold_runs.append(run.text)
    
    if bold_runs:
        print(f"PARA {i}: {text[:120]}")
        print(f"  BOLD parts: {bold_runs}")
        print()
    
    # Also print question-like paragraphs (starting with number)
    if text and (text[0].isdigit() or text.startswith('Question') or text.startswith('Q.')):
        print(f"PARA {i}: {text[:120]}")
        if bold_runs:
            print(f"  BOLD parts: {bold_runs}")
        print()
