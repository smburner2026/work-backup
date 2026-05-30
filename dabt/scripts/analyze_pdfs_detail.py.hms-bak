#!/usr/bin/env python3
"""Detailed PDF analysis for Past_ABT_Exams"""
import os
from pdfminer.high_level import extract_text as pdf_extract

BASE = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams"
# Only analyze unique PDFs (deduplicated)
unique_pdfs = [
    "2012_complete_board_questions.pdf",
    "2013_Recert_Examination.pdf",
    "2015_Recert_Examination.pdf",
    "2017_Certification_Part_1_of_2.pdf",
    "2017_Certification_Part_1_of_2_day2.pdf",
    "2017_Certification_Part_2_of_2.pdf",
    "2017_Certification_Part_2_of_2_day2.pdf",
]

def extract_pdf(path):
    try:
        text = pdf_extract(path)
        return text
    except Exception as e:
        return f"[Error: {e}]"

for fname in unique_pdfs:
    path = os.path.join(BASE, fname)
    print(f"\n{'='*60}")
    print(f"=== {fname} ===")
    print('='*60)
    text = extract_pdf(path)
    lines = text.split('\n')
    # Get topics by looking at question stems
    questions = []
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() and '. ' in line[:5]):
            q_num = line.split('.')[0].strip()
            if q_num.isdigit():
                questions.append(line)
    
    print(f"Total lines: {len(lines)}")
    print(f"Detected questions (numbered starts): {len(questions)}")
    print(f"\nFirst 10 questions:")
    for q in questions[:10]:
        print(f"  {q[:120]}")
    print(f"\nLast 3 questions:")
    for q in questions[-3:]:
        print(f"  {q[:120]}")
    
    # Check for answer key sections
    lower_text = text.lower()
    has_answers = any(kw in lower_text for kw in ['answer key', 'answer:', 'answer ', 'correct answer', 'key'])
    print(f"\nContains answer markings: {has_answers}")
    
    # Look for topic distribution
    topic_kw = {
        'Pesticides': ['pesticide', 'insecticide', 'herbicide', 'organophosphate', 'organochlorine', 'ddt', 'chlorpyrifos'],
        'Metals/Heavy Metals': ['mercury', 'lead', 'arsenic', 'cadmium', 'selenium', 'metal'],
        'Solvents': ['solvent', 'benzene', 'toluene', 'xylene', 'methanol', 'ethanol'],
        'Pharmacokinetics/ADME': ['absorption', 'distribution', 'metabolism', 'excretion', 'pharmacokinetic', 'adme'],
        'Carcinogenesis': ['carcinogen', 'cancer', 'tumor', 'mutagen', 'genotoxic', 'initiation', 'promotion'],
        'Reproductive/Developmental': ['reproductive', 'developmental', 'teratogen', 'fertility', 'fetal'],
        'Neurotoxicity': ['neurotox', 'neuropathy', 'nerve', 'brain', 'cns', 'peripheral'],
        'Risk Assessment': ['risk', 'hazard', 'safety assessment', 'exposure assessment', 'dose-response'],
        'Regulatory': ['regulatory', 'oecd', 'epa', 'fda', 'glp', 'guideline'],
        'Statistics/Biostatistics': ['statistical', 'noael', 'loael', 'benchmark', 'dose', 'significant'],
        'Target Organ Toxicity': ['hepatotox', 'nephrotox', 'cardiotox', 'pulmonary', 'dermal', 'liver', 'kidney'],
        'Ecotoxicology': ['ecotox', 'environmental', 'fish', 'aquatic', 'wildlife'],
    }
    
    print("\nTopic keyword frequency:")
    for topic, kws in sorted(topic_kw.items()):
        count = sum(lower_text.count(kw) for kw in kws)
        if count > 0:
            print(f"  {topic}: {count} mentions")
