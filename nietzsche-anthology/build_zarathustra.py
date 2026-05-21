#!/usr/bin/env python3
"""Build just the Zarathustra work as a standalone PDF (Hollingdale)."""
import sys, os, re, subprocess

SRC = "/root/work/nietzsche-anthology/sources"
OUTDIR = "/root/work/nietzsche-anthology"
TMPDIR = os.path.join(OUTDIR, "build_tmp")
os.makedirs(TMPDIR, exist_ok=True)

CSS = """<style>
@page { size: 6in 9in; margin: 1in 0.85in 0.9in 0.85in;
    @bottom-center { content: counter(page); font-family: 'Liberation Serif', Georgia, serif; font-size: 9pt; color: #666; } }
body { font-family: 'Liberation Serif', Georgia, serif; font-size: 10pt; line-height: 1.5; color: #1a1a1a; text-align: left; hyphens: auto; overflow-wrap: break-word; word-wrap: break-word; }
h1 { font-size: 16pt; font-weight: bold; margin-top: 1.5em; margin-bottom: 0.5em; }
h1.part { font-size: 16pt; font-weight: bold; text-align: center; margin-top: 2em; margin-bottom: 0.3em; }
h2 { font-size: 13pt; font-weight: bold; margin-top: 1.5em; margin-bottom: 0.5em; }
h3 { font-size: 11pt; font-weight: bold; margin-top: 1.2em; margin-bottom: 0.3em; }
.work-meta { text-align: center; font-size: 9pt; color: #666; margin-bottom: 1.5em; font-style: italic; }
p { margin: 0.5em 0; }
</style>"""

def markdown_to_html(text):
    text = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
    text = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    paragraphs = []
    for block in text.split('\n\n'):
        block = block.strip()
        if not block: continue
        if block.startswith('<h') or block.startswith('</'):
            paragraphs.append(block)
        elif block.startswith('> '):
            inner = block.replace('\n> ', '\n').lstrip('> ')
            paragraphs.append(f'<blockquote>{inner}</blockquote>')
        else:
            paragraphs.append(f'<p>{block}</p>')
    return '\n'.join(paragraphs)

# Build Zarathustra
filepath = os.path.join(SRC, 'hollingdale_zarathustra_full.txt')
print(f"Reading {filepath}...", flush=True)
with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
    body = f.read()

body = re.sub(r'  +', ' ', body)
body = re.sub(r'\n{3,}', '\n\n', body)
body = re.sub(r'^.*?(?=When Zarathustra was thirty)', '', body, flags=re.DOTALL)
body = re.sub(r'\n+Notes\n+.*$', '', body, flags=re.DOTALL)

html = '<h1 class="part">Part VI</h1>\n<h1>Thus Spoke Zarathustra</h1>\n<div class="work-meta">1883–1885 — Translated by R.J. Hollingdale</div>\n'
html += markdown_to_html(body)

full_html = f'<!DOCTYPE html><html><head><meta charset="utf-8"/>{CSS}</head><body>{html}</body></html>'
html_path = os.path.join(TMPDIR, '06_zarathustra.html')
pdf_path = os.path.join(TMPDIR, '06_zarathustra.pdf')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Converting to PDF with WeasyPrint...", flush=True)
result = subprocess.run(
    ['weasyprint', html_path, pdf_path],
    capture_output=True, text=True, timeout=120
)
if result.returncode == 0:
    kb = os.path.getsize(pdf_path) // 1024
    print(f'SUCCESS: {pdf_path} ({kb} KB)', flush=True)
else:
    print(f'FAILED: {result.stderr[:500]}', flush=True)
    sys.exit(1)
