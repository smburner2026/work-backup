#!/usr/bin/env python3
"""
Extract clean text from:
1. Untimely_Meditations_Hollingdale_Cambridge.pdf (use PyMuPDF)
2. Human_All_Too_Human_Hollingdale_Cambridge.epub (use zipfile+bs4)
3. Daybreak_Hollingdale_Cambridge.epub (use zipfile+bs4)

Save as .txt files in the same directory.
"""

import os
import re
import sys
import zipfile
from pathlib import Path

SRC = Path("/root/work/nietzsche-anthology/sources")

# ─────────────────────────────────────────────
# 1. EPUB extraction helpers
# ─────────────────────────────────────────────
def extract_epub_text(epub_path):
    """Extract text from an EPUB file (HTML inside ZIP)."""
    from bs4 import BeautifulSoup

    full_text = []
    with zipfile.ZipFile(epub_path) as z:
        # Find all xhtml/html files, sorted for reading order
        html_files = sorted(
            [f for f in z.namelist() if f.endswith(('.xhtml', '.html', '.htm'))]
        )
        for hf in html_files:
            raw = z.read(hf)
            soup = BeautifulSoup(raw, 'html.parser')
            # Kill scripts/styles
            for tag in soup(['script', 'style', 'nav']):
                tag.decompose()
            body = soup.find('body')
            if body:
                text = body.get_text(separator='\n')
            else:
                text = soup.get_text(separator='\n')
            full_text.append(text)
    return '\n'.join(full_text)


def clean_epub_text(raw_text):
    """Clean up EPUB-extracted text."""
    lines = raw_text.split('\n')
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        # Remove page numbers (isolated numbers or like "123")
        if re.match(r'^\d{1,4}$', s):
            continue
        # Remove common headers/footers like "Human, All Too Human" or "Daybreak" 
        # that appear on every page — we'll do content-based filtering below
        cleaned.append(s)
    return '\n'.join(cleaned)


# ─────────────────────────────────────────────
# 2. PDF extraction with PyMuPDF
# ─────────────────────────────────────────────
import fitz  # PyMuPDF

def extract_pdf_text(pdf_path):
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(str(pdf_path))
    all_text = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text('text')
        all_text.append(text)
    doc.close()
    return '\n'.join(all_text)


def clean_pdf_text(raw_text):
    """Clean PDF-extracted text: remove headers, footers, page numbers."""
    lines = raw_text.split('\n')
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        # Skip page numbers alone
        if re.match(r'^\d{1,4}$', s):
            continue
        # Skip header/footer lines that are very short and contain common patterns
        # like "Untimely Meditations" or "Human, All Too Human" at top of page
        if re.match(r'^(Untimely Meditations|Human, All Too Human|Daybreak)\s*$', s):
            continue
        # Skip Cambridge edition line
        if re.match(r'^Cambridge University Press$', s):
            continue
        # Skip "Translated by" lines that appear in headers
        if re.match(r'^Translated by R\.\s*J\.\s*Hollingdale$', s):
            continue
        # Skip lines with only dashes/dots
        if re.match(r'^[\s\-–—.·]+$', s):
            continue
        # Skip copyright page stuff
        if re.match(r'^© Cambridge University Press', s):
            continue
        if 'www.cambridge.org' in s.lower():
            continue
        # Skip ISBN-like lines
        if re.match(r'^ISBN', s):
            continue
        # Skip toc/chapter-number-only lines that are too short
        if re.match(r'^\d{1,2}\s*$', s) and len(s) <= 3:
            continue
        cleaned.append(s)
    return '\n'.join(cleaned)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    files = [
        {
            'name': 'Untimely_Meditations_Hollingdale_Cambridge',
            'type': 'pdf',
            'path': SRC / 'Untimely_Meditations_Hollingdale_Cambridge.pdf',
        },
        {
            'name': 'Human_All_Too_Human_Hollingdale_Cambridge',
            'type': 'epub',
            'path': SRC / 'Human_All_Too_Human_Hollingdale_Cambridge.epub',
        },
        {
            'name': 'Daybreak_Hollingdale_Cambridge',
            'type': 'epub',
            'path': SRC / 'Daybreak_Hollingdale_Cambridge.epub',
        },
    ]

    for f in files:
        print(f"\n{'='*60}")
        print(f"Processing: {f['name']} ({f['type']})")
        out_path = SRC / f"{f['name']}.txt"
        
        if not f['path'].exists():
            print(f"  ERROR: Source file not found: {f['path']}")
            continue
        
        try:
            if f['type'] == 'epub':
                print("  Extracting from EPUB...")
                raw = extract_epub_text(f['path'])
                print(f"  Raw text length: {len(raw)} chars")
                text = clean_epub_text(raw)
            else:
                print("  Extracting from PDF (PyMuPDF)...")
                raw = extract_pdf_text(f['path'])
                print(f"  Raw text length: {len(raw)} chars")
                text = clean_pdf_text(raw)
            
            # Write out
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.write(text)
            
            # Count lines
            line_count = text.count('\n') + 1
            word_count = len(text.split())
            print(f"  Saved: {out_path}")
            print(f"  Lines: {line_count:,}, Words: {word_count:,}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print("Done!")


if __name__ == '__main__':
    main()
