"""Extract all regulation PDFs into .txt files with index.json."""
import fitz
import os
import json
from pathlib import Path

REF = "/home/vthen/work/dabt-tutor/reference"
REG_DIR = os.path.join(REF, "regulations")
OUT_DIR = os.path.join(REF, "extracted", "regulations")

os.makedirs(OUT_DIR, exist_ok=True)

index_entries = []
total_bytes = 0

for root, dirs, files in os.walk(REG_DIR):
    for fname in sorted(files):
        if not fname.lower().endswith(".pdf"):
            continue
        
        pdf_path = os.path.join(root, fname)
        rel_dir = os.path.relpath(root, REG_DIR)
        category = rel_dir if rel_dir != "." else "other"
        
        # Clean output filename
        out_name = fname.lower().replace(" ", "-").replace("(", "").replace(")", "")
        out_name = out_name.replace(".pdf", ".txt")
        out_path = os.path.join(OUT_DIR, out_name)
        
        print(f"  [{category}] {fname[:70]}...", end="")
        
        doc = fitz.open(pdf_path)
        pages = len(doc)
        
        text_parts = []
        for pg in range(pages):
            page_text = doc[pg].get_text("text")
            if page_text.strip():
                text_parts.append(page_text.strip())
        
        if not text_parts:
            print(" ⚠️  NO TEXT (scanned/image PDF)")
            doc.close()
            continue
        
        full_text = "\n\n".join(text_parts)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {fname}\n")
            f.write(f"# Category: {category}\n")
            f.write(f"# Pages: {pages}\n\n")
            f.write(full_text)
        
        size_kb = os.path.getsize(out_path) / 1024
        total_bytes += os.path.getsize(out_path)
        
        print(f" {pages}p → {size_kb:.0f} KB")
        
        index_entries.append({
            "title": fname.replace(".pdf", ""),
            "category": category,
            "file": out_name,
            "pages": pages,
        })
        
        doc.close()

# Write index
index = {
    "source": "DABT Regulations",
    "total_documents": len(index_entries),
    "documents": index_entries,
}
with open(os.path.join(OUT_DIR, "index.json"), "w") as f:
    json.dump(index, f, indent=2)

print(f"\n✅ Done: {len(index_entries)} documents, {total_bytes/1024:.0f} KB total")
