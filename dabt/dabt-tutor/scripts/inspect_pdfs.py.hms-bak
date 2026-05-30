"""Inspect PDF structure: page count, TOC, first/last pages."""
import fitz
import os, sys

REF = "/home/vthen/work/dabt-tutor/reference"

for name in ["casarett-doull-9e.pdf", "hayes-7e.pdf"]:
    path = f"{REF}/textbooks/{name}"
    doc = fitz.open(path)
    toc = doc.get_toc()
    
    print(f"=== {name} ===")
    print(f"  Pages: {len(doc)}")
    print(f"  TOC entries: {len(toc)}")
    
    if toc:
        print(f"  First 20 TOC entries:")
        for entry in toc[:20]:
            level, title, page = entry
            indent = "  " * (level - 1)
            print(f"    {indent}[lvl{level}] p{page}: {title[:120]}")
        if len(toc) > 20:
            print(f"    ... ({len(toc) - 20} more)")
        print(f"  Last 5 TOC entries:")
        for entry in toc[-5:]:
            level, title, page = entry
            indent = "  " * (level - 1)
            print(f"    {indent}[lvl{level}] p{page}: {title[:120]}")
    else:
        print("  No TOC — will need heading-based splitting")
    
    # Sample text from first content page (usually page 2-3, skip cover)
    for test_page in [2, 3]:
        text = doc[test_page].get_text()
        if len(text.strip()) > 100:
            print(f"  Sample text from page {test_page+1}:")
            print(f"    {text.strip()[:200]}...")
            break
    
    doc.close()
    print()
