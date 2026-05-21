#!/usr/bin/env python3
"""
Build Nietzsche Complete Works PDF — per-work approach to avoid memory issues.
Each work builds as a small PDF, then pdfunite merges them.
"""
import os
import re
import subprocess
import sys

SRC = "/root/work/nietzsche-anthology/sources"
OUTDIR = "/root/work/nietzsche-anthology"
TMPDIR = os.path.join(OUTDIR, "build_tmp")
FINAL_PDF = os.path.join(OUTDIR, "Nietzsche_Complete_Works.pdf")

os.makedirs(TMPDIR, exist_ok=True)

def read_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def strip_editorial_apparatus(text, filename):
    """Strip editorial footnotes, COMMENT blocks, and front matter from source files."""
    import re as _re
    
    # Will to Power: special handling for Kaufmann's extensive apparatus
    if 'will_to_power' in filename:
        # Strip everything before the first numbered section (the actual Nietzsche content)
        first_section = _re.search(r'^[0-9]+\s+\(', text, _re.MULTILINE)
        if first_section:
            text = text[first_section.start():]
        # Remove COMMENT blocks (Kaufmann's editorial interjections)
        text = _re.sub(r'\n\nCOMMENT\n\n.*?(?=\n\n[0-9]+\s+\()', '', text, flags=_re.DOTALL)
        # Remove standalone footnote lines: "1 " followed by editorial text at line start
        text = _re.sub(r'\n[0-9]+\s+[A-Z][a-z].*?(?=\n\n)', '', text)
        # Remove remaining footer references at end of sections
        text = _re.sub(r'\n\n[0-9]+\s+[A-Z][a-z].*?(?=\n\n---|\Z)', '', text, flags=_re.DOTALL)
        # Remove trailing publisher/translator matter
        text = _re.sub(r'\n\n.*?About the Author.*?(?=\n\n[0-9]+\s+\()', '', text, flags=_re.DOTALL)
    
    # ALL works: aggressively strip inline footnote numbers attached to words
    # Remove digit sequences stuck to lowercase words like "bêtise111" → "bêtise"
    text = _re.sub(r'([a-z])[0-9]+([,.;:!?)\s\])]*)', r'\1\2', text)
    # Remove digit sequences stuck to closing parens like "note112)" → "note)"
    text = _re.sub(r'([a-zA-Z])([0-9]+)([)\]})]*)', r'\1\3', text)
    # Remove standalone footnote lines in Hollingdale/Cambridge style:
    # "1879. While at Basle..." (period after year = footnote)
    # "3. Up to this point..." (numbered footnote start)
    text = _re.sub(r'\n[0-9]+\.[\s]+[A-Z].*?(?=\n\n)', '', text)
    text = _re.sub(r'\n[0-9]+\.[\s]+[A-Z].*?(?=\n[A-Z])', '', text)
    
    # General: strip EPUB artifacts and publisher cruft
    text = _re.sub(r'\n---.*?---\n', '\n\n', text)
    
    return text

def cleanup_text(text, source=""):
    text = strip_editorial_apparatus(text, source)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple spaces (OCR artifacts)
    text = re.sub(r'  +', ' ', text)
    # Fix underscore artifacts (OCR leftovers)
    text = re.sub(r'(\w)_(\w)', r'\1 \2', text)
    # Remove backticks (monospace triggers)
    text = text.replace('`', '')
    # Reflow text broken into one-word-per-line (OCR artifact)
    # Joins consecutive short lines into sentences
    import re as _re
    lines = text.split('\n')
    reflowed = []
    buffer = []
    standalone_punct = {'.', '..', '...', '. . .', '. .', ':', ';', ',', '!', '?'}
    heading_starts = {'chapter', 'part', 'book', 'section', 'preface', 'introduction',
                      'note', 'appendix', 'index', 'volume', 'book first',
                      'book second', 'book third', 'book fourth', 'book fifth',
                      'first part', 'second part', 'third part', 'fourth part'}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                reflowed.append(' '.join(buffer))
                buffer = []
            reflowed.append('')
            continue
        # Standalone punctuation — append to previous line
        if stripped in standalone_punct:
            if buffer:
                buffer[-1] = buffer[-1] + stripped
            continue
        word_count = len(stripped.split())
        is_heading_like = (stripped.startswith(('#', '*')) 
                          or stripped.isupper() and len(stripped) > 2
                          or any(stripped.lower().startswith(h) for h in heading_starts))
        # Reflow: if this is a short non-heading line, join into buffer
        if word_count <= 5 and not is_heading_like:
            buffer.append(stripped)
            continue
        # Longer line or heading — flush buffer then add this line directly
        if buffer:
            reflowed.append(' '.join(buffer))
            buffer = []
        reflowed.append(stripped)
    if buffer:
        reflowed.append(' '.join(buffer))
    text = '\n'.join(reflowed)
    # (WeasyPrint's overflow-wrap can't handle 2000+ char paragraphs)
    lines = []
    for line in text.split('\n'):
        while len(line) > 300:
            # Find last space before 300 to break cleanly
            break_at = line.rfind(' ', 0, 300)
            if break_at < 200:
                break_at = line.find(' ', 200)
            if break_at == -1:
                break_at = 250
            lines.append(line[:break_at].strip())
            line = line[break_at:].strip()
        if line:
            lines.append(line)
    text = '\n'.join(lines)
    return text.strip()

# ============================================================
# CSS (same throughout)
# ============================================================
CSS = """<style>
@page { size: 6in 9in; margin: 0.7in 0.65in 0.75in 0.65in;
    @bottom-center { content: counter(page); font-family: 'Liberation Serif', Georgia, serif; font-size: 9pt; color: #666; } }
body { font-family: 'Liberation Serif', Georgia, serif; font-size: 10pt; line-height: 1.3; color: #1a1a1a; text-align: left; hyphens: auto; orphans: 3; widows: 3; }
p { margin: 0; text-indent: 1.2em; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; max-width: 100%; }
/* Book-style: no indent on first paragraph after heading */
h1 + p, h2 + p, h3 + p, h1.part + p, .section-break + p { text-indent: 0; }
p.work-meta, p.works-intro, p.nachlass-note, li, blockquote p { text-indent: 0; }
pre, code { white-space: pre-wrap; word-break: break-all; font-size: 9pt; }
h1 { font-size: 16pt; font-weight: bold; margin-top: 1.8em; margin-bottom: 0.3em; }
h1.part { font-size: 16pt; font-weight: bold; text-align: center; margin-top: 0.5em; margin-bottom: 0.3em; }
h2 { font-size: 13pt; font-weight: bold; margin-top: 1.5em; margin-bottom: 0.3em; }
h3 { font-size: 11pt; font-weight: bold; margin-top: 1.2em; margin-bottom: 0.3em; }
.work-meta { text-align: center; font-size: 9pt; color: #666; margin-bottom: 1.5em; font-style: italic; }
.works-intro { text-align: center; font-style: italic; color: #555; padding: 1em 0; }
.nachlass-note { font-size: 9pt; font-style: italic; color: #666; text-align: center; margin: 1em 0; padding: 1em; border-top: 1px solid #ccc; border-bottom: 1px solid #ccc; }
.section-break { page-break-before: always; margin-top: 1.5em; }
.section-break p:first-child { font-weight: bold; font-size: 11pt; color: #444; }
blockquote { margin: 0.8em 0 0.8em 1.5em; padding-left: 1em; border-left: 3px solid #ccc; font-size: 9.5pt; line-height: 1.5; color: #333; }
</style>"""

def markdown_to_html(text):
    """Simple markdown-to-HTML conversion."""
    # Section breaks: numbered entries like "2 (Spring-Fall 1887)" get a page break
    text = re.sub(r'^([0-9]+\s+\([A-Z].*?\))$', r'<div class="section-break"><p>\1</p></div>', text, flags=re.MULTILINE)
    # Headings
    text = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
    text = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    # Bold/italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Paragraphs
    paragraphs = []
    for block in text.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        if block.startswith('<h') or block.startswith('<div') or block.startswith('<table') or block.startswith('</'):
            paragraphs.append(block)
        elif block.startswith('> '):
            inner = block.replace('\n> ', '\n')
            inner = re.sub(r'^> ', '', inner, count=1)
            paragraphs.append(f'<blockquote>{inner}</blockquote>')
        else:
            lines = block.split('\n')
            if all(l.strip().startswith('- ') or l.strip().startswith('* ') for l in lines if l.strip()):
                items = ''.join(f'<li>{l.strip()[2:]}</li>' for l in lines if l.strip())
                paragraphs.append(f'<ul>{items}</ul>')
            else:
                paragraphs.append(f'<p>{block}</p>')
    return '\n'.join(paragraphs)

def build_small_pdf(html_body, output_path):
    """Build a PDF from HTML body using WeasyPrint."""
    html = f'<!DOCTYPE html><html><head><meta charset="utf-8">{CSS}</head><body>{html_body}</body></html>'
    # Write to temp file
    with open(output_path.replace('.pdf', '.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    from weasyprint import HTML
    HTML(filename=output_path.replace('.pdf', '.html')).write_pdf(output_path)
    os.remove(output_path.replace('.pdf', '.html'))

# ============================================================
# Build each part
# ============================================================
pdfs = []

def build_part(html_body, name):
    path = os.path.join(TMPDIR, f"{name}.pdf")
    print(f"  Building {name}.pdf...", flush=True)
    build_small_pdf(html_body, path)
    pdfs.append(path)
    print(f"    Done: {os.path.getsize(path) // 1024} KB", flush=True)

# --- FRONT MATTER ---
print("Phase 1: Front matter...", flush=True)

front_html = """
<div style="text-align:center; padding-top:2in;">
<h1 style="font-size:28pt;">THE COMPLETE WORKS<br>OF<br>FRIEDRICH NIETZSCHE</h1>
<p style="font-size:16pt; font-style:italic; color:#444; margin-bottom:1.5em;">A Compilation of Translations</p>
<p style="font-size:12pt; color:#666;">Translations by Ian Johnston, R.J. Hollingdale, Graham Parkes,<br>
Adrian Del Caro, Josefine Nauckhoff, Paul S. Loeb, David F. Tinsley,<br>
Walter Kaufmann, and George H. Leiner</p>
<p style="font-size:12pt; color:#666; margin-top:2em;">Compiled by Costin · 2026</p>
</div>
"""
build_part(front_html, "00_title")

toc_html = """
<h1 style="text-align:center;">TABLE OF CONTENTS</h1>
<div style="font-size:13pt; line-height:2.2;">
<p><b>PUBLISHED WORKS</b></p>
<p>Part I &nbsp; The Birth of Tragedy</p>
<p>Part II &nbsp; Untimely Meditations</p>
<p>Part III &nbsp; Human, All Too Human</p>
<p>Part IV &nbsp; Daybreak</p>
<p>Part V &nbsp; The Gay Science</p>
<p>Part VI &nbsp; Thus Spoke Zarathustra</p>
<p>Part VII &nbsp; Beyond Good and Evil</p>
<p>Part VIII &nbsp; On the Genealogy of Morals</p>
<p>Part IX &nbsp; Twilight of the Idols / The Antichrist</p>
<p>Part X &nbsp; Ecce Homo</p>
<p>Part XI &nbsp; Dithyrambs of Dionysus</p>
<p style="margin-top:1em;"><b>NACHLASS</b></p>
<p>App. A &nbsp; Nachlass Vol.14 (1882–1884)</p>
<p>App. B &nbsp; Nachlass Vol.16 (1885–1886)</p>
<p>App. C &nbsp; The Will to Power</p>
</div>
"""
build_part(toc_html, "00_toc")

intro_html = """
<h1>INTRODUCTION</h1>
<p>This volume collects Friedrich Nietzsche's published works and a selection of his posthumous fragments (the <em>Nachlass</em>) in English translation. The translations have been chosen for their fidelity to Nietzsche's voice — his bite, his physiological concreteness, his aristocratic radicalism — rather than for scholarly consensus or editorial safety.</p>
<p>The published works are presented in chronological order, from <em>The Birth of Tragedy</em> (1872) through the <em>Dithyrambs of Dionysus</em> (1888), the last thing Nietzsche wrote before his collapse. Each work is credited to its translator.</p>
<p>The Nachlass presents a harder question. Nietzsche abandoned his plan for a magnum opus called <em>The Will to Power</em> in 1888, and the posthumous compilation bearing that title — assembled by his sister and later re-edited by Walter Kaufmann — is a construction, not a book Nietzsche authorised. For the late notebooks (1885–1888), Kaufmann's <em>Will to Power</em> is included here as a provisional map of the terrain, with the recognition that the Stanford critical edition will eventually supersede it. The Stanford volumes that were available at the time of compilation (vols. 14 and 16) appear in full.</p>
<p>Three notes on the translations:</p>
<p><b>Ian Johnston</b> — the doctrinal core (Birth of Tragedy, Beyond Good and Evil, Genealogy of Morals). His public-domain translations are chosen for fidelity, not polish. They do not flinch.</p>
<p><b>R.J. Hollingdale</b> — the middle and late periods (Untimely Meditations, Human All Too Human, Daybreak, Twilight, Antichrist, Ecce Homo, Dithyrambs). Hollingdale's Nietzsche has bite without editorial softening. He is the translator who lets Nietzsche's spite stay in the room.</p>
<p><b>R.J. Hollingdale</b> — Thus Spoke Zarathustra. Lean, direct, and unflinching. His Zarathustra strikes like a hammer — no poetic softening, no academic hedging. The Übermensch is "the Superman" and "down-going" is the path, not "going-under."</p>
"""
build_part(intro_html, "00_intro")

# --- PUBLISHED WORKS ---
print("Phase 2: Published works...", flush=True)

published = [
    ("01_birth_tragedy", "Part I", "The Birth of Tragedy", "1872", "Ian Johnston", "birth_of_tragedy_johnston.txt", False),
    ("02_untimely", "Part II", "Untimely Meditations", "1873–1876", "R.J. Hollingdale", "Untimely_Meditations_Hollingdale_Cambridge.txt", False),
    ("03_human", "Part III", "Human, All Too Human", "1878–1880", "R.J. Hollingdale", "Human_All_Too_Human_Hollingdale_Cambridge.txt", False),
    ("04_daybreak", "Part IV", "Daybreak: Thoughts on the Prejudices of Morality", "1881", "R.J. Hollingdale", "Daybreak_Hollingdale_Cambridge.txt", False),
    ("05_gay_science", "Part V", "The Gay Science", "1882/1887", "Adrian Del Caro / Josefine Nauckhoff", "gay_science_delcaro.txt", False),
    ("06_zarathustra", "Part VI", "Thus Spoke Zarathustra", "1883–1885", "R.J. Hollingdale", "hollingdale_zarathustra_full.txt", False),
    ("07_bge", "Part VII", "Beyond Good and Evil", "1886", "Ian Johnston", "bge_johnston_full.txt", False),
    ("08_genealogy", "Part VIII", "On the Genealogy of Morals", "1887", "Ian Johnston", "genealogy_johnston_full.txt", False),
]

for name, part, title, year, translator, filename, strip_front in published:
    filepath = os.path.join(SRC, filename)
    if not os.path.exists(filepath):
        print(f"  WARNING: {filename} not found, skipping {title}", flush=True)
        continue
    
    body = read_file(filepath)
    body = cleanup_text(body, filename)
    # Strip front matter for specific works
    if title == "The Birth of Tragedy":
        body = re.sub(r'^.*?(?=THE BIRTH OF TRAGEDY)', '', body, flags=re.DOTALL)
    elif title == "Thus Spoke Zarathustra":
        body = re.sub(r'^.*?(?=When Zarathustra was thirty)', '', body, flags=re.DOTALL)
        # Strip EPUB back-matter cruft after the last chapter
        body = re.sub(r'\n+Notes\n+.*$', '', body, flags=re.DOTALL)
    
    # Add page break before, part header, work header, translator credit
    html = f'<h1 class="part">{part}</h1>\n<h1>{title}</h1>\n<div class="work-meta">{year} — Translated by {translator}</div>\n'
    html += markdown_to_html(body)
    build_part(html, name)

# --- TWILIGHT + ANTICHRIST (same file) ---
print("  Building 09_twilight_antichrist.pdf...", flush=True)
twilight_file = os.path.join(SRC, "twilight_antichrist_hollingdale.txt")
if os.path.exists(twilight_file):
    body = read_file(twilight_file)
    body = cleanup_text(body, "twilight_antichrist_hollingdale.txt")
    # Split at Antichrist marker
    ac_marker = "THE ANTI-CHRIST"
    ac_pos = body.find(ac_marker, 100)
    if ac_pos != -1:
        twilight = body[:ac_pos]
        antichrist = body[ac_pos:]
    else:
        twilight = body
        antichrist = ""
    
    html = '<h1 class="part">Part IX</h1>\n<h1>Twilight of the Idols</h1>\n<div class="work-meta">1888 — Translated by R.J. Hollingdale</div>\n'
    html += markdown_to_html(twilight)
    html += '<div style="page-break-before: always;"></div>\n<h1 class="part">Part IX (continued)</h1>\n<h1>The Antichrist</h1>\n<div class="work-meta">1888 — Translated by R.J. Hollingdale</div>\n'
    html += markdown_to_html(antichrist)
    build_part(html, "09_twilight_antichrist")

# --- ECCE HOMO ---
print("  Building 10_ecce_homo.pdf...", flush=True)
ecce_file = os.path.join(SRC, "ecce_homo_hollingdale.txt")
if os.path.exists(ecce_file):
    body = read_file(ecce_file)
    body = cleanup_text(body, "ecce_homo_hollingdale.txt")
    body = re.sub(r'^.*?(?=ECCE HOMO)', '', body, flags=re.DOTALL)
    html = f'<h1 class="part">Part X</h1>\n<h1>Ecce Homo</h1>\n<div class="work-meta">1888 — Translated by R.J. Hollingdale</div>\n'
    html += markdown_to_html(body)
    build_part(html, "10_ecce_homo")

# --- DITHYRAMBS ---
print("  Building 11_dithyrambs.pdf...", flush=True)
dith_file = os.path.join(SRC, "dithyrambs_hollingdale.txt")
if os.path.exists(dith_file):
    body = read_file(dith_file)
    body = cleanup_text(body, "dithyrambs_hollingdale.txt")
    html = f'<h1 class="part">Part XI</h1>\n<h1>Dithyrambs of Dionysus</h1>\n<div class="work-meta">1888 — Translated by R.J. Hollingdale</div>\n'
    html += markdown_to_html(body)
    build_part(html, "11_dithyrambs")

# --- NACHLASS ---
print("Phase 3: Nachlass...", flush=True)

nachlass_intro = """
<div class="nachlass-note">
The following sections contain Nietzsche's unpublished notebook fragments, presented in 
chronological order as they appear in the Stanford Complete Works critical edition. 
These are not finished works but working notes, drafts, and abandoned projects — they 
show Nietzsche thinking on the page. The reader should treat them as a workshop, not a gallery.
</div>
"""

nachlass_works = [
    (name, appendix, title, translator, filename)
    for name, appendix, title, translator, filename in [
        ("12_nachlass14", "Appendix A", "Nachlass Volume 14: Unpublished Fragments from the Period of Thus Spoke Zarathustra (Summer 1882 – Winter 1883/84)", "Paul S. Loeb & David F. Tinsley", "Nietzsche_Vol14_Summer1882-Winter1883.txt"),
        ("13_nachlass16", "Appendix B", "Nachlass Volume 16: Unpublished Fragments (Spring 1885 – Spring 1886)", "Adrian Del Caro", "Nietzsche_Vol16_Spring1885-Spring1886.txt"),
    ]
]

for i, (name, appendix, title, translator, filename) in enumerate(nachlass_works):
    filepath = os.path.join(SRC, filename)
    if not os.path.exists(filepath):
        print(f"  WARNING: {filename} not found, skipping {title}", flush=True)
        continue
    body = read_file(filepath)
    body = cleanup_text(body, filename)
    nachlass_html = nachlass_intro if i == 0 else ""
    nachlass_html += f'<h1 class="part">{appendix}</h1>\n<h1>{title}</h1>\n<div class="work-meta">Translated by {translator}</div>\n'
    nachlass_html += markdown_to_html(body)
    build_part(nachlass_html, name)

# Will to Power is too large for a single PDF on 2GB RAM — split into halves
print("  Building 14_will_to_power (split into two parts)...", flush=True)
wtp_file = os.path.join(SRC, "will_to_power_kaufmann.txt")
if os.path.exists(wtp_file):
    body = read_file(wtp_file)
    body = cleanup_text(body, "will_to_power_kaufmann.txt")
    # Split in half at a natural boundary
    mid = len(body) // 2
    # Find nearest double-newline to mid
    split_point = body.find('\n\n', mid)
    if split_point == -1:
        split_point = mid
    part1_text, part2_text = body[:split_point], body[split_point:]
    
    wtp_intro = f'<h1 class="part">Appendix C</h1>\n<h1>The Will to Power</h1>\n<div class="work-meta">Translated by Walter Kaufmann & R.J. Hollingdale</div>\n'
    
    html1 = wtp_intro + '<h2>Book One — Two: (Part 1)</h2>\n' + markdown_to_html(part1_text)
    build_part(html1, "14a_will_to_power_p1")
    
    html2 = '<div style="page-break-before: always;"></div>\n' + wtp_intro + '<h2>Book Three — Four: (Part 2)</h2>\n' + markdown_to_html(part2_text)
    build_part(html2, "14b_will_to_power_p2")

# --- MERGE ---
print("Phase 4: Merging PDFs...", flush=True)
if pdfs:
    merge_cmd = ["pdfunite"] + pdfs + [FINAL_PDF]
    result = subprocess.run(merge_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(FINAL_PDF) // 1024
        print(f"\nSUCCESS: {FINAL_PDF} ({size} KB)", flush=True)
    else:
        print(f"Merge failed: {result.stderr}", flush=True)
        
    # Clean up temp files
    for p in pdfs:
        os.remove(p)
    os.rmdir(TMPDIR)
    print("Temp files cleaned up.", flush=True)
else:
    print("ERROR: No PDFs were built!", flush=True)
