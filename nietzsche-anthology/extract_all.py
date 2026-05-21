#!/usr/bin/env python3
"""
Extract clean text from Nietzsche Vol.16, Will to Power, and Dithyrambs.
Prefers EPUB (ZIP+HTML) extraction; uses PyMuPDF for PDF-only sources.
"""

import zipfile
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SRC = Path("/root/work/nietzsche-anthology/sources")
OUT = Path("/root/work/nietzsche-anthology/extracted")
OUT.mkdir(parents=True, exist_ok=True)


class TextExtractor(HTMLParser):
    """Strip HTML tags, keep text with paragraph breaks."""
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_tag = False
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        # Skip script, style, head, etc.
        if tag_lower in ('script', 'style', 'head', 'meta', 'link', 'title'):
            self.skip_tag = True
            self.skip_depth += 1
        if tag_lower in ('p', 'div', 'br', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in ('script', 'style', 'head', 'meta', 'link', 'title'):
            self.skip_depth -= 1
            if self.skip_depth <= 0:
                self.skip_tag = False
                self.skip_depth = 0
        if tag_lower in ('p', 'div', 'br', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'):
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip_tag:
            self.parts.append(data)

    def get_text(self):
        raw = ''.join(self.parts)
        # Collapse multiple newlines to at most 2
        raw = re.sub(r'\n{3,}', '\n\n', raw)
        # Strip leading/trailing whitespace on each line
        lines = [line.strip() for line in raw.split('\n')]
        # Remove empty lines at start and end
        while lines and lines[0] == '':
            lines.pop(0)
        while lines and lines[-1] == '':
            lines.pop()
        return '\n'.join(lines)


def extract_epub_text(epub_path, output_path, file_glob='*.htm*', use_ncx_order=True):
    """Extract text from an EPUB file (ZIP containing HTML)."""
    print(f"  Extracting EPUB: {epub_path.name}")
    all_text_parts = []

    with zipfile.ZipFile(epub_path, 'r') as z:
        # Get list of HTML/XHTML files
        html_files = sorted([f for f in z.namelist() if f.endswith(('.htm', '.html', '.xhtml'))])

        # Try to use NCX for ordering, but also just process all HTML files
        for fname in html_files:
            try:
                content = z.read(fname).decode('utf-8', errors='replace')
            except Exception:
                try:
                    content = z.read(fname).decode('latin-1', errors='replace')
                except Exception:
                    continue

            # Extract file-specific headers
            header = f"\n\n=== {os.path.basename(fname)} ===\n\n"

            extractor = TextExtractor()
            extractor.feed(content)
            text = extractor.get_text()
            if text.strip():
                all_text_parts.append(header + text)

    result = '\n\n'.join(all_text_parts)
    # Remove excessive blank lines
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    word_count = len(result.split())
    print(f"  -> Saved: {output_path.name} ({word_count} words, {len(result):,} chars)")
    return result


def extract_pdf_text(pdf_path, output_path):
    """Extract text from PDF using PyMuPDF."""
    print(f"  Extracting PDF: {pdf_path.name}")
    try:
        import fitz
        doc = fitz.open(pdf_path)
        all_text = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                all_text.append(f"\n\n[Page {page_num+1}]\n\n{text}")

        result = ''.join(all_text)
        # Clean: remove page number lines (often standalone numbers)
        result = re.sub(r'\n\s*\d+\s*\n', '\n', result)
        result = re.sub(r'\n{4,}', '\n\n\n', result)

        doc.close()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)

        word_count = len(result.split())
        print(f"  -> Saved: {output_path.name} ({word_count} words, {len(result):,} chars)")
        return result
    except ImportError:
        print("  ! fitz not available, trying pdftotext...")
        import subprocess
        subprocess.run(['pdftotext', '-layout', str(pdf_path), str(output_path)], check=True)
        word_count = len(open(output_path).read().split())
        print(f"  -> Saved: {output_path.name} ({word_count} words)")
        return open(output_path).read()


# ========== 1. Nietzsche Vol. 16 (EPUB) ==========
print("\n=== 1. Nietzsche Vol.16 Spring 1885-Spring 1886 (Del Caro) ===")
epub_v16 = SRC / "Nietzsche_Vol16_Spring1885-Spring1886.epub"
out_v16 = OUT / "Nietzsche_Vol16_Spring1885-Spring1886.txt"
extract_epub_text(epub_v16, out_v16)

# ========== 2. Will to Power (Kaufmann) - EPUB ==========
print("\n=== 2. Will to Power (Kaufmann/Hollingdale) ===")
epub_wtp = SRC / "will_to_power_kaufmann.epub"
out_wtp = OUT / "will_to_power_kaufmann.txt"
extract_epub_text(epub_wtp, out_wtp)

# ========== 3. Dithyrambs (Hollingdale) - PDF only ==========
print("\n=== 3. Dithyrambs (Hollingdale) ===")
pdf_dith = SRC / "dithyrambs_hollingdale.pdf"
out_dith = OUT / "dithyrambs_hollingdale.txt"
extract_pdf_text(pdf_dith, out_dith)

print("\n=== DONE ===")
for f in sorted(OUT.glob("*.txt")):
    size = f.stat().st_size
    print(f"  {f.name}: {size:,} bytes")
