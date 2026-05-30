#!/usr/bin/env python3
"""Quick check: PDF metadata and attempt OCR on a single Mid-Amer PDF."""
import os, json

try:
    import fitz
except:
    fitz = None

base = "/root/dabt-curated/Mid-Amer_Tox_Course/Topic_Summaries"

results = []

for f in sorted(os.listdir(base)):
    if not f.endswith('.pdf'):
        continue
    fp = os.path.join(base, f)
    size = os.path.getsize(fp)
    
    info = {"file": f, "size_bytes": size, "size_kb": round(size/1024, 1)}
    
    if fitz:
        doc = fitz.open(fp)
        info["pages"] = len(doc)
        info["metadata"] = doc.metadata
        # Try direct text extraction
        text = ""
        for page in doc:
            text += page.get_text()
        if text.strip():
            info["has_text"] = True
            info["text_preview"] = text[:200].strip()
        else:
            info["has_text"] = False
            info["text_preview"] = "(scanned/image-based)"
        doc.close()
    
    results.append(info)
    print(f"{f}: {info.get('pages','?')} pages, {info.get('size_kb','?')} KB, text={info.get('has_text','?')}")

with open(os.path.join(base, "..", "topic_summaries_info.json"), "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved to topic_summaries_info.json")
