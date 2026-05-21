---
name: document-pipelines
description: "Take source content in various formats (web articles, markdown chapters, OCR text, .docx) and produce formatted output documents (PDF, translated text, cleaned .docx). Covers RSS/web extraction, markdown book compilation, document format conversion, and large-document translation workflows."
category: software-development
tags: [document, pipeline, PDF, translation, RSS, markdown, OCR, docx, fpdf2]
trigger: |
  User needs to process source content into a formatted output document:
  - Web article URL → clean PDF
  - Markdown chapter files → compiled book PDF
  - .docx font/format adjustment or conversion
  - Large OCR document → translated, unified text
---

# Document Pipelines

## When to Use

- User provides a URL and wants article text as a PDF
- User provides RSS/Atom feed URLs or Substacks for batch extraction
- User provides markdown chapter files and wants a compiled book PDF
- User needs to modify font/size in a .docx or convert between formats
- User needs to translate a large book-length document (especially German Fraktur OCR)
- Any "take source X → produce output Y" document workflow

## Common Prerequisites

| Tool | Purpose |
|------|---------|
| `fpdf2` | PDF generation (pip install fpdf2) |
| `python-docx` | .docx reading/writing (pip install python-docx) |
| `libreoffice-writer` | docx→PDF conversion (apt-get) |
| `requests` | Fetching web content and RSS feeds |
| `html2text` | HTML→clean text conversion |
| `fonts-liberation2` | Serif font for PDFs (apt-get) |

---

## 1. Web Content → Clean Text → PDF

### Source Types
- **RSS/Atom feeds**: Most reliable — contain full HTML content in `<content:encoded>` CDATA.
- **Substack API**: Paginated endpoint `/api/v1/archive?sort=new&offset=N` for full archive.
- **Individual pages**: `window._preloads` JSON extraction for older Substack articles.
- **General web pages**: `web_extract` tool.

### RSS Feed URL Patterns

| Platform | Feed URL |
|----------|----------|
| Substack | `https://<pub>.substack.com/feed` |
| Medium | `https://medium.com/feed/@<username>` |
| WordPress | `https://<site>/feed/` or `/feed/atom/` |
| Blogspot | `https://<blog>.blogspot.com/feeds/posts/default` |

### Extraction Pipeline (RSS)

```python
import requests, xml.etree.ElementTree as ET, re, html, sqlite3

def fetch_rss(feed_url: str) -> list[dict]:
    resp = requests.get(feed_url, headers={"User-Agent": "Mozilla/5.0"})
    root = ET.fromstring(resp.content)
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    items = []
    for item in root.iter("item"):
        content_el = item.find("content:encoded", ns)
        items.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "pub_date": (item.findtext("pubDate") or "").strip(),
            "html_content": content_el.text if content_el is not None else "",
        })
    return items

def html_to_text(html_content: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_content)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

### Substack Full Archive (beyond RSS ~20-item limit)

```python
import json, time

def get_all_posts(pub_slug: str) -> list[dict]:
    all_posts = []
    for offset in range(0, 100, 20):
        url = f"https://{pub_slug}.substack.com/api/v1/archive?sort=new&offset={offset}"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(resp.text)
        if not isinstance(data, list) or len(data) == 0:
            break
        all_posts.extend(data)
        time.sleep(0.3)
    return all_posts
```

### HTML-to-Text for Substack

Two approaches:
1. **html2text** (recommended): `pip install html2text`, produces clean markdown.
2. **Regex-based** (fast, no deps): Strip captioned-image-container, figure, button-wrapper divs then HTML tags.

### PDF Generation with fpdf2

```python
from fpdf import FPDF

def article_to_pdf(text: str, title: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

    max_width = pdf.w - pdf.l_margin - pdf.r_margin
    def sanitize(line):
        for ch in '\u200b\u200c\u200d\u2060\ufeff':
            line = line.replace(ch, '')
        return line

    # Title
    pdf.set_font("DejaVu", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(5)

    # Body with word-wrap for long lines
    pdf.set_font("DejaVu", "", 10)
    for line in text.split('\n'):
        line = sanitize(line.strip())
        if not line:
            pdf.ln(3)
            continue
        words = line.split()
        buf = ""
        for word in words:
            test = (buf + " " + word).strip()
            if pdf.get_string_width(test) > max_width and buf:
                pdf.multi_cell(0, 5, buf)
                buf = word
            else:
                buf = test
        if buf:
            pdf.multi_cell(0, 5, buf)
    pdf.output(output_path)
```

**Pitfalls**: Unicode in PDFs needs DejaVu font (not Helvetica). Zero-width Unicode chars (U+200B etc.) crash fpdf2 — always strip. Single unbroken lines wider than page raise "Not enough horizontal space" — word-wrap manually. RSS pagination limited to ~20 items; use API for full archive.

See `references/substack-rss-pipeline.md` for complete Substack-specific extraction, window._preloads parsing, and example pipeline script.

---

## 2. Markdown Chapters → Compiled Book PDF

Compile a multi-chapter book from individual markdown files into a single bound volume PDF with fpdf2 and Liberation Serif font.

### Prerequisites

```bash
pip install fpdf2
sudo apt-get install -y fonts-liberation2
```

Font paths:
- `/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf`
- `/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf`
- `/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf`
- `/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf`

### Book Structure

Define a `BOOK_ORDER` list — the canonical order of every chapter/section slug. Use `CHAPTER_LABELS` dict to label special slugs (Preface, Introduction, etc.) and section-number dicts to map section slugs within each chapter.

### Title Extraction (Priority-Based)

Markdown sources have heterogeneous title formats. Priority extractor:
1. `# Hash heading` (multiline)
2. `**N. Bold numbered section**` (multiline)
3. `N. Plain numbered section` followed by blank line
4. `**Bold title**` (excludes Chapter-prefixed, Roman-numeral, and `[bracket]` notes)
5. `Chapter [Roman]: title`
6. `**IV Bold Roman-numeral chapter head**`
7. `X. N. Chapter.section number pattern`
8. First standalone capitalized line (15-150 chars)

### Body Rendering

- **Justified text**: Word-level line builder with variable inter-word spacing.
- **Overflow protection**: Words wider than available width fall back to `multi_cell()`.
- **Subsection headings**: `##` → centered bold, `###` → left-aligned bold.
- **Blockquotes**: Indented italic, gray.
- **Boilerplate stripping**: Italic preface notes, `Chapter X:` lines, bold Roman-numeral chapter heads, subscribe/FUNDRAISING lines removed.
- **Title dedup**: Extracted title stripped from body via regex so it doesn't appear twice.

### Table of Contents

Hierarchical: chapter headings (bold) with sections indented. Front matter (Preface, Introduction) top, back matter (Conclusion, Appendix) bottom.

### Page Layout

Font 12pt Liberation Serif, 25mm margins, title page with decorative rule, chapter title pages, running headers (8pt gray centered), page numbers in footer.

**Pitfalls**: `cell()` in fpdf2 does NOT wrap — always detect and fall back to `multi_cell()`. Title extraction fails silently — chain fallbacks. Liberation Serif italic missing newline glyph is cosmetic. Check for numbered titles without bold markers using numbered-line regex.

---

## 3. Document Format Conversion (.docx editing, docx↔PDF)

### Modify Font Size in .docx

```python
from docx import Document
from docx.shared import Pt

doc = Document("input.docx")

# 1. Update default style
style = doc.styles['Normal']
style.font.size = Pt(14)

# 2. Update explicit run-level sizes
for p in doc.paragraphs:
    for run in p.runs:
        if run.font.size and run.font.size.pt == 11:
            run.font.size = Pt(14)
        elif run.font.size and run.font.size.pt == 13:
            run.font.size = Pt(16)
        elif run.font.size and run.font.size.pt == 10:
            run.font.size = Pt(12)

doc.save("input.docx")
```

**Pitfalls**: Run-level sizes override style defaults — update both. Always scan current sizes first with a Counter pass before modifying:

```python
from collections import Counter
sizes = Counter()
for p in doc.paragraphs:
    for run in p.runs:
        if run.font.size:
            sizes[run.font.size.pt] += 1
print(dict(sizes.most_common(10)))
```

### Convert .docx → PDF

```bash
libreoffice --headless --convert-to pdf input.docx
```

Output is `input.pdf` in the same directory. Java warning is non-fatal.

### Delivery

Send the original format (.docx or .pdf) to the target platform, not text extraction. Tag with `MEDIA:/absolute/path/to/file`.

---

## 4. Large Document Translation Pipeline

Translate book-length documents (especially German Fraktur OCR) using parallel subagent dispatch with style-guide context, followed by multi-pass editorial unification.

### Phase 0: Source Extraction and Cleaning

For OCR'd Fraktur/German Gothic text:
1. **Extract**: PyMuPDF (`fitz`) for Google Books PDFs.
2. **Strip front matter**: Remove Google Books boilerplate, library stamps, call numbers, TOC pages.
3. **Fix hyphenation**: `re.sub(r'(\w)-\n(\w)', r'\1\2', text)`
4. **Fix missing spaces**: German Fraktur OCR drops word spaces. Regex for lowercase→UPPERCASE boundaries catches ~80%.
5. **Fix punctuation spacing**: Remove space before `,` `;` `:`.
6. **Fix word fragments**: German compounds broken at line ends produce artifacts like `Ge sichte` → `Geschichte`. Maintain a fix list.
7. **Greek cleanup**: Fraktur OCR garbles Greek (`Agɣetvños` → `ἀρχέτυπος`).

See `references/fraktur-ocr-cleaning.md` for the full artifact catalog and fix-list.

### Phase 1: Style Guide Preparation

Three documents:
1. **STYLE_GUIDE.md** — The register in one sentence. Cardinal rules (no calques, active verbs, restrained capitalization, American spelling).
2. **GLOSSARY.md** — Fixed English equivalents for recurring source terms.
3. **LORIMER_NOTES.md** — Observations on reference translation (sentence rhythm, capitalization, wit, archaisms).

### Phase 2: Parallel Subagent Translation

```python
delegate_task(tasks=[
    {goal: "Translate Book X", context: "STYLE.md + GLOSSARY.md + SAMPLE + source files", toolsets: ["terminal","file"]},
    {goal: "Translate Book Y", ...},
    {goal: "Translate Book Z", ...},
])
```

Each subagent needs: style guide (compressed), glossary, target-voice sample (2-3 paragraphs), cleaned source files, exact output filename convention.

### Phase 3: Editorial Passes

**Pass 1 — Mechanical** (automated): Em-dash normalization, American spelling sweep, Edwardian phrase strip (`not seldom→often`, `whilst→while`), double-space removal.

**Pass 2 — Content/register** (semi-automated): Scan for glossary violations, check capitalization, flag German calques (`conditionedness`, `history-writing`), flag Edwardian archaisms (`wherein`, `therein`, `whence`), check voice consistency across chapter boundaries.

### Phase 4: Assembly

Concatenate chapters with front matter. Strip leading ellipsis artifacts from continuation chapters.

**Pitfalls**: Subagent voice drift (always plan unification pass). Missing source alignment (chapter boundaries in OCR may not match book chapters). Over-aggressive cleanup (some archaisms are deliberate register choices). Context window limits on large German source files.

---

## References

See references/ for session-specific detail:
- `references/substack-rss-pipeline.md` — Substack extraction, window._preloads, full archive API, html2text patterns
- `references/fraktur-ocr-cleaning.md` — Full German Fraktur artifact catalog, word fragment fix list, Greek character table
- `references/curated-anthology-workflow.md` — Compiling a reference anthology of core texts: surveying competing translations/editions, establishing selection criteria tied to an intellectual inquiry, documenting trade-offs, and producing a mixed deliverable (PD full-texts + purchase references). Also covers multi-format text extraction (HTML, PDF, EPUB, OCR), thematic vs chronological organization, and mixed-source PDF compilation.
- `references/docx-bold-answer-extraction.md` — Extracting answer letters from MCQ docx files by detecting bold-formatted option text, with DB cross-reference patterns
- `references/text-extraction-quality-check.md` — Systematic QA checklist for verifying extracted text quality: OCR artifact detection, structural completeness, PDF cross-reference, front/back matter boundary checks, and contraction/apostrophe integrity. Run before feeding any extraction into downstream processing.
