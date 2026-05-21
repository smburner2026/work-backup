#!/usr/bin/env python3
"""
Clean up extracted texts: remove IA notice, simplify structure markers,
collapse excessive whitespace.
"""
import re

SRC = "/root/work/nietzsche-anthology/extracted"

def clean_file(filename, remove_notice=True, simplify_markers=True):
    path = f"{SRC}/{filename}"
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove Internet Archive notice (everything between nav.xhtml and page_0.html)
    if remove_notice and "=== nav.xhtml ===" in text:
        text = re.sub(
            r'=== nav\.xhtml ===.*?=== page_0\.html ===',
            '',
            text,
            flags=re.DOTALL
        )
        # Also clean the nav/notice remnants
        text = re.sub(r'Nietzsche Unpublished Fragments and Writings\s*\n\s*\nNotice\s*\n', '', text)

    # Simplify page markers to just [Page N]
    if simplify_markers:
        text = re.sub(r'=== page_(\d+)\.html ===', r'[Page \1]', text)
        # Simplify other HTML file markers
        text = re.sub(r'=== (.*?)\.htm[l]? ===', r'--- \1 ---', text)

    # Collapse excessive blank lines (more than 2)
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Trim leading/trailing whitespace
    text = text.strip()

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

    lines = text.count('\n') + 1
    words = len(text.split())
    print(f"  Cleaned {filename}: {words} words, {lines} lines, {len(text):,} chars")
    return text

print("Cleaning up extracted files...")
clean_file("Nietzsche_Vol16_Spring1885-Spring1886.txt", remove_notice=True, simplify_markers=True)
clean_file("will_to_power_kaufmann.txt", remove_notice=False, simplify_markers=True)
clean_file("dithyrambs_hollingdale.txt", remove_notice=False, simplify_markers=True)
print("Done.")
