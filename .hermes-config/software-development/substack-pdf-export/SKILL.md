---
name: substack-pdf-export
description: Export a Substack publication's articles to clean text files and text-only PDFs. Fetches all chapters via archive API, extracts full content from individual pages, and generates PDFs using fpdf2.
---

# Substack PDF Export Pipeline

Export a Substack publication's articles (e.g. a book translation) into clean text files and text-only PDFs, one per article.

## When to use

- User wants to archive a Substack publication locally
- User wants to convert a series of Substack articles/chapters into PDFs
- The publication is a book translation split across multiple posts
- All articles are free/public (no paywall)

## Prerequisites

```bash
pip3 install --break-system-packages trafilatura fpdf2
```
html2text is a fallback — only install if trafilatura is unavailable for your platform.

## Workflow

### 1. Get the list of all posts

The Substack archive API returns posts in reverse chronological order. Fetch multiple pages to get everything:

```bash
curl -s -H "User-Agent: Mozilla/5.0" "https://{pub}.substack.com/api/v1/archive?sort=new&offset=0" > /tmp/p1.json
curl -s -H "User-Agent: Mozilla/5.0" "https://{pub}.substack.com/api/v1/archive?sort=new&offset=20" > /tmp/p2.json
curl -s -H "User-Agent: Mozilla/5.0" "https://{pub}.substack.com/api/v1/archive?sort=new&offset=40" > /tmp/p3.json
curl -s -H "User-Agent: Mozilla/5.0" "https://{pub}.substack.com/api/v1/archive?sort=new&offset=60" > /tmp/p4.json
```

Each response is a JSON array of post objects (metadata only — `body_html` is empty in archive responses).

### 2. Identify target articles

Filter the posts you want by slug, title pattern, or exclude known non-target content. The archive gives you: `slug`, `title`, `id`, `post_date`, etc.

**Critical**: Manual slug curation is fragile — you will miss chapters. If the publication has a Table of Contents page, fetch it and extract all chapter links from the `body_html` to validate your slug set. At minimum, scan all archive pages for titles matching the publication's topic pattern rather than relying on a hardcoded list. See `references/chapter-validation.md` for the cross-referencing technique.

### 3. Extract full content from each page

Substack pages embed the full post data in a `window._preloads` JSON variable inside a `<script>` tag. Extract it:

```python
import re, codecs, json, urllib.request

def fetch_post_data(slug, publication):
    url = f"https://{publication}.substack.com/p/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=30)
    html = resp.read().decode('utf-8', errors='replace')
    
    match = re.search(r'window\._preloads\s*=\s*JSON\.parse\(\"(.*?)\"\)', html)
    if not match:
        return None
    
    escaped = match.group(1)
    unescaped = codecs.decode(escaped, 'unicode_escape')
    data = json.loads(unescaped)
    
    # Post data might be at data['post'] or data['preloads']['post']
    if 'post' in data:
        return data['post']
    return None
```

The returned post dict has `body_html` (full article HTML), `title`, `slug`, `post_date`, etc.

### 4. Convert HTML to clean text

**Preferred: trafilatura on `body_html` from `_preloads`.** Extract the article body from the page's `window._preloads` JSON first (step 3), then feed only `body_html` to trafilatura. Do NOT feed the full page HTML — that leaks reader comments and page chrome into the output.

```python
import trafilatura, re

def body_html_to_markdown(body_html):
    text = trafilatura.extract(body_html, output_format='markdown',
                               include_links=False, include_images=False,
                               include_formatting=True)
    if not text:
        return None
    # Strip Substack-specific boilerplate that trafilatura misses
    text = re.sub(r'^This below is.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^FUNDRAISING.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Click here to navigate.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Subscribe now\s*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()
```

trafilatura on `body_html` produces clean markdown: `#` headers, `**bold**`, `*italic*`, proper paragraph breaks. No reader comments, no page chrome.

**Preferred workflow: extract .md first, review, then convert to PDF.** The user will want to spot-check the markdown before PDF generation. Save intermediate `.md` files so corrections can be made without re-fetching.

**Fallback: html2text on `body_html`.** Only if trafilatura is unavailable. Be extremely careful with post-processing — the `re.sub(r'\n_+.*?$', ...)` pattern is lethal (see Pitfalls below and `references/truncation-bug.md`). Strip boilerplate by targeting exact strings, never patterns.

### 5. Generate PDF with fpdf2

Use DejaVu fonts (installed on Ubuntu at `/usr/share/fonts/truetype/dejavu/`). The key pitfall: `multi_cell(0, 5, line)` throws `FPDFException("Not enough horizontal space to render a single character")` when a line is wider than the page. Wrap long lines manually on word boundaries.

```python
from fpdf import FPDF

def sanitize_for_pdf(text):
    """Remove zero-width characters and replace Unicode punctuation."""
    for ch in '\u200b\u200c\u200d\u2060\ufeff\u200e\u200f':
        text = text.replace(ch, '')
    replacements = {
        '\u2013': '-', '\u2014': '--', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u00a0': ' ',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def write_line(pdf, max_width, ln, font_size=10, bold=False):
    """Write a line to PDF, wrapping on word boundaries if too wide."""
    style = "B" if bold else ""
    pdf.set_font("DejaVu", style, font_size)
    ln = sanitize_for_pdf(ln)
    if not ln.strip():
        pdf.ln(3)
        return
    
    try:
        lw = pdf.get_string_width(ln)
    except:
        lw = max_width + 1
    
    if lw <= max_width:
        try:
            pdf.multi_cell(0, 5, ln)
        except:
            pdf.ln(3)
        return
    
    # Word-wrap
    words = ln.split()
    buf = ""
    for word in words:
        test = (buf + " " + word).strip()
        try:
            tw = pdf.get_string_width(test)
        except:
            tw = max_width + 1
        if tw > max_width and buf:
            try:
                pdf.multi_cell(0, 5, buf)
            except:
                pdf.ln(3)
            buf = word
        else:
            buf = test
    if buf:
        try:
            pdf.multi_cell(0, 5, buf)
        except:
            pdf.ln(3)

pdf = FPDF()
pdf.add_page()
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
max_width = pdf.w - pdf.l_margin - pdf.r_margin
```

### 6. Pipeline script structure

A reusable script is available at `scripts/substack_pdf_export.py`. Edit the `PUBLICATION` and `CHAPTERS` variables at the top, then run it. The script:

1. Loads chapter list (hardcoded slugs or discovered from archive JSON)
2. For each chapter: checks cache → fetches if needed → converts to text → saves .txt → generates .pdf
3. Uses `time.sleep(0.3)` between fetches to be polite to the server
4. Strips boilerplate lines (Subscribe, FUNDRAISING, Click here) during PDF rendering
5. Handles word-wrapping for lines wider than the PDF page width

To bootstrap: fetch archive JSON files first (step 1), then scan for matching slugs. See `references/chapter-validation.md` for the cross-referencing technique to ensure no chapters are missed.

## Pitfalls

- **DO NOT strip boilerplate with `re.sub(r'\n_+.*?$', ...)`**: This is the most dangerous pattern you can add to `html_to_text`. html2text renders `<em>italic</em>` as `_italic_`, so `\n_+.*?$` with `re.DOTALL` matches from the first italic word to end-of-file, silently truncating the chapter. A 4,400-word chapter collapsed to 200 words before this was caught. Strip boilerplate at PDF rendering time instead (skip lines starting with `Subscribe`, `FUNDRAISING`, `Click here`, `Share`), or use trafilatura which handles it automatically.
- **html2text produces artifacts on Substack HTML**: Complex nested HTML (especially Substack's rich-text editor output) causes html2text to produce weird formatting — spurious underscores, broken paragraphs, embedded SVG fragments. Prefer trafilatura (see step 4) for Substack content. If you must use html2text, never add cleanup regexes without testing them on a chapter known to contain italic text.
- **Manual slug sets are incomplete**: Hardcoding a set of slugs (like `NOLTE_SLUGS = {...}`) almost always misses one or two chapters. Always cross-reference against the publication's TOC page or scan the archive for title patterns. The most common failure mode is missing a chapter that was published out of chronological order or has a non-obvious title.
- **Multi-page Substack posts**: Substack allows authors to split long posts into multiple pages. If a chapter feels too short (under ~5,000 chars), the original post may be paginated. Check for `post_page_count` in the `_preloads` data, or look for "Continue reading"/"Next page" links in the HTML. Multi-page posts require fetching each page separately (URLs follow the pattern `/p/{slug}?page=2`).
- **Slug-based API endpoint doesn't work**: `/api/v1/posts?slug=` searches globally across ALL substack posts, often returning wrong results. Use `window._preloads` from the individual page HTML instead.
- **Archive API pagination**: Only returns ~20-30 posts per page. Fetch offset=0,20,40,60 to get everything.
- **Body HTML empty in archive**: The archive list only has metadata. Full content requires fetching each individual page.
- **zero-width characters (U+200B)**: Substack HTML often contains these. They break fpdf2's `multi_cell()` with "Not enough horizontal space" error. Strip them before rendering.
- **DejaVu font**: Ensure DejaVu Sans is installed (`sudo apt-get install fonts-dejavu` on Ubuntu). Some Unicode chars (especially em-dashes and curly quotes) are wider than expected and trigger word-wrap issues.
- **Subscribe/boilerplate**: Article bodies include subscribe buttons, fundraising banners, and "Click here to navigate" text. These should be stripped at TWO stages: (a) during HTML→text conversion (regex removal of subscribe blocks), and (b) at PDF rendering time (skip lines starting with `Subscribe`, `FUNDRAISING`, `Click here`, `Share`). Doing it only at stage (a) leaves residual text; doing it only at stage (b) wastes PDF rendering on boilerplate lines. Both stages needed for clean output.
- **"This below is Chapter X Section Y" lines**: Some publications insert inter-chapter navigation lines that trafilatura preserves. Strip with `re.sub(r'^This below is.*?\n', '', text, flags=re.MULTILINE)`. These appear on ~95% of chapters in multi-chapter publications.
- **Short posts**: Some "chapters" may just be announcements, letters, or poems. Verify content length before PDF generation. A real book chapter typically has >15,000 chars of body text. Posts under 5,000 chars are almost certainly not full chapters — they're either paginated (see above) or auxiliary content.
- **body_html is null in older posts**: Some older Substack posts (pre-2022) serialize `body_html: null` in the `window._preloads` JSON and put content only in the rendered `<article>` HTML tag. When `body_html` extraction fails, fall back to: `re.search(r'<article[^>]*>(.*?)</article>', page_html, re.DOTALL)` and feed the result to trafilatura. This is common for the first few posts a publication ever made.
- **ToC page slug may change**: The URL of a publication's Table of Contents page is not stable. Always fetch the archive and search for it rather than hardcoding the URL. If a previously-working ToC URL returns 404, scan the archive for posts whose title contains the book name or "table of contents".

### 7. Compile chapters into a single book (bound volume)

When the user wants all chapters in one PDF with a Table of Contents and proper chapter ordering:

**Determine canonical chapter order**: The archive API returns posts in reverse chronological order (publication date), not book order. Get the correct order from the publication's dedicated Table of Contents page. Fetch the ToC page and extract links from `body_html` — each link's anchor text contains the chapter/section label (e.g. "Chapter 2 Section 3 here").

**ToC page discovery**: The ToC slug may not be obvious. If the first attempt returns 404, search for it by crawling the archive for posts whose title contains "civil war", "table of contents", or the book name. The correct slug may differ by a trailing number (e.g. `-917` vs `-1917`).

**When body_html is null**: Some older posts (especially the preface or early chapters) may have `body_html: null` in the page JSON. Fall back to extracting the `<article>` tag from the full page HTML and feeding that to trafilatura. The article tag pattern: `<article[^>]*>(.*?)</article>`.

**Book compilation script**: Use `scripts/compile_book.py`. Place all `.md` files in one directory, define the `BOOK_ORDER` list (slug order from the ToC), and the script generates a single PDF with:
- Title page (book title, subtitle, author credit)
- Table of Contents page (chapter/section labels)
- Each chapter starting on a fresh page with centered heading + decorative rule
- Running headers with chapter title on continuation pages
- Centered page numbers
- Liberation Serif (Times New Roman equivalent) -- `fonts-liberation2` package
- Justified text, preserved bold/italic, indented italic blockquotes
- Section labels for multi-section chapters (Chapter II, Section 5 etc.)
- Subsection headings (`##` / `###`) rendered as bold section titles
- **Long-word overflow handling**: single words wider than the page auto-fallback to `multi_cell()` instead of overflowing the margin (see `references/book-compilation.md`)
- **Title extraction**: 8-pattern priority chain handles bold titles, numbered sections, Chapter/X headings, and plain text titles with `re.MULTILINE` (see `references/book-compilation.md`)
- **Boilerplate stripping**: italic preface notes, Chapter heading lines, Roman-numeral chapter heads all removed from body text automatically
- **Updated font defaults**: 12pt body / 6.5pt leading for better readability (old: 11pt / 5.5pt)
- **Inline formatting**: `**bold**` markers within paragraphs render as italic (academic convention); `*italic*` as italic; `***bold italic***` as bold italic (see `references/book-compilation.md`)
- **Title casing**: All extracted titles run through `to_title_case()` — Chicago-style with proper noun awareness (see `references/book-compilation.md`)
- **Hierarchical TOC**: Front matter → Chapters with indented sections → Back matter, using `CHAPTER_FULL_NAMES` display names (see `references/book-compilation.md`)

**Fonts for book production**: Use Liberation Serif (`fonts-liberation2` package on Ubuntu) for a classic textbook look. Bold/Italic/BoldItalic variants are all included. Paths:
```
/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf
/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf
/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf
/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf
```

## Verification

See `references/truncation-bug.md` for the full forensics on the `\n_+.*?$` regex bug. See `references/comments-leakage.md` for the reader-comments leakage pitfall when feeding full page HTML to trafilatura. See `references/book-compilation.md` for the ToC extraction technique and chapter ordering methodology.

- Check that `.md` files end with proper chapter conclusions, not reader comments or informal text
- Verify PDFs render correctly by opening a few in a PDF viewer
- Compare slug count vs expected chapter list
- When compiling a book, cross-reference chapter order against the publication's official ToC page — do not rely on archive API order
