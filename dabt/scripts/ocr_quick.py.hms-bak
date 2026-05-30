#!/usr/bin/env python3
"""Quick OCR of key Mid-Amer Topic Summary PDFs for content characterization."""
import pytesseract
from PIL import Image
import io, fitz, os

targets = [
    "Principles of Tox.pdf",
    "Mech of Tox.pdf",
    "Disposition of Xenobiotics.pdf",
    "Genetic Toxicology.pdf",
    "Carcinogenesis.pdf",
    "Inhalation Toxicology.pdf",
    "Liver and Kidney Toxicity.pdf",
    "Neuro & Behavioral Tox.pdf",
    "Dermatotoxicity.pdf",
    "Immunotox.pdf",
    "Blood Toxicity.pdf",
    "Teratog and Repro.pdf",
    "Ocular & Visual Tox.pdf",
    "Metals.pdf",
    "Pesticides.pdf",
    "Solvents and Vapors.pdf",
    "Plant and Animal Toxins.pdf",
    "Reg.Tox. Risk Assess.pdf",
    "Table of Contents.pdf",
]

base = "/root/dabt-curated/Mid-Amer_Tox_Course/Topic_Summaries"

for fname in targets:
    fp = os.path.join(base, fname)
    if not os.path.exists(fp):
        print(f"\n--- {fname} NOT FOUND ---")
        continue
    
    doc = fitz.open(fp)
    print(f"\n--- {fname} ({len(doc)} pages) ---")
    
    full_text = ""
    for i in range(min(2, len(doc))):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(img)
        full_text += text
    
    doc.close()
    
    # Show first few meaningful lines
    lines = [l.strip() for l in full_text.split('\n') if l.strip() and len(l.strip()) > 15]
    for l in lines[:5]:
        print(f"  {l[:120]}")
    
    # Check for practice questions
    has_q = any(kw in full_text.lower() for kw in ['questions', 'review questions', 'quiz', 'test your', 'practice', 'multiple choice'])
    print(f"  Contains question references: {has_q}")
