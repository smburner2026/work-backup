#!/usr/bin/env python3
"""Quick OCR test on first 5 pages of a Mid-Amer topic summary."""
import pytesseract
from PIL import Image
import io
import fitz

path = "/root/dabt-curated/Mid-Amer_Tox_Course/Topic_Summaries/Principles of Tox.pdf"
doc = fitz.open(path)
print(f"Total pages: {len(doc)}")
print(f"Metadata: {doc.metadata}")

# OCR first 3 pages
for i in range(min(3, len(doc))):
    page = doc[i]
    pix = page.get_pixmap(dpi=200)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    text = pytesseract.image_to_string(img)
    print(f"\n===== PAGE {i+1} =====")
    print(text[:500])
doc.close()
