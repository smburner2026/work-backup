#!/usr/bin/env python3
"""Quick OCR of first 2 pages of each Mid-Amer Topic Summary to identify content."""
import pytesseract
from PIL import Image
import io
import fitz
import os, json

base = "/root/dabt-curated/Mid-Amer_Tox_Course/Topic_Summaries"
results = []

for f in sorted(os.listdir(base)):
    if not f.endswith('.pdf'):
        continue
    fp = os.path.join(base, f)
    print(f"\n--- {f} ---")
    
    doc = fitz.open(fp)
    info = {
        "file": f,
        "pages": len(doc),
        "size_kb": round(os.path.getsize(fp)/1024, 1),
    }
    
    # OCR first 2 pages
    full_text = ""
    for i in range(min(2, len(doc))):
        page = doc[i]
        pix = page.get_pixmap(dpi=150)  # lower DPI for speed
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(img)
        full_text += f"\n--- Page {i+1} ---\n{text}"
    
    doc.close()
    
    # Extract key info from OCR text
    lines = [l.strip() for l in full_text.split('\n') if l.strip() and len(l.strip()) > 10]
    
    info["ocr_preview"] = lines[:15]
    
    # Determine if it includes practice questions
    has_q = any(kw in full_text.lower() for kw in ['questions', 'review', 'quiz', 'test', 'examination', 'multiple choice'])
    info["has_question_references"] = has_q
    
    results.append(info)
    print(f"  Pages: {info['pages']}, Content preview: {lines[:3] if lines else '(empty)'}")

with open("/root/midamer_ocr_summary.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to /root/midamer_ocr_summary.json")
