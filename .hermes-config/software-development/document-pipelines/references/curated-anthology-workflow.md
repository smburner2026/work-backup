# Curated Anthology Workflow

When compiling a reference anthology of core texts for an intellectual inquiry — selecting between competing translations/editions, documenting rationale, and producing a mixed deliverable.

## When to Use

- User wants to build a "master PDF" or reference document collecting the best versions of a philosopher's works
- Multiple competing translations/editions exist with different strengths (style, fidelity, availability)
- Selection criteria are driven by a specific intellectual inquiry (e.g., "what does Nietzsche say about breeding and nobility" — not casual reading)
- Deliverable mixes public-domain full texts + purchase references for copyrighted editions

## Workflow

### 1. Establish the Inquiry Frame

Before evaluating sources, clarify what the texts are *for*:

- **Intellectual project**: What question is the user pursuing? (e.g., "what soil, blood, and breeding produced great civilizations")
- **Use case**: Will they be citing doctrinally (needs fidelity), reading for inspiration (needs style), or both?
- **Method vs. data**: Is this thinker a *lens* (Nietzsche as method) or the *subject* (Burckhardt as data)? Different sources serve different roles.

### 2. Survey Available Editions

For each core work, identify:

| Edition | Translator | Copyright | Available Formats | Key Trait |
|---------|-----------|-----------|------------------|-----------|
| Publisher X | Name | Public domain / Copyright | PDF, print, etc. | Strength (prose, fidelity, notes) |

**Where to check**: Wikipedia bibliography, publisher series pages, academic reviews (NDPR, JStor), Reddit threads (r/Nietzsche, r/askphilosophy — filter for translation discussions), Quora.

### 3. Establish Selection Criteria

Criteria should be *explicit* and *tied to the inquiry*, not generic. Common axes:

- **Doctrinal fidelity**: Does the translator editorialise (soften, domesticate, reframe) the author's radical claims? Check specific passages relevant to the user's inquiry.
- **Literary style**: Does the English *move*? Is the translator a writer or a scholar?
- **Textual basis**: Does it use the critical edition or an outdated one?
- **Apparatus**: Footnotes, introductions, endnotes — useful or noise?
- **Availability**: Public domain (compilable), print-only, in-print vs. out-of-print, cost

### 4. Document Trade-offs Explicitly

For each work, state what's gained and lost with each choice. Example:

> *BGE §257:* Johnston gives you the *claim* without editorial framing. Kaufmann gives you a more vivid sentence but surrounds it with qualifying context that blunts the aristocratic radicalism. For citation → Johnston. For inspiration → Kaufmann with guard up.

### 5. Structure the Deliverable

Two-tier approach:

**A. Available in public domain** — compile full text.
- Download source (RTF, HTML, plain text from translator's site or Wikisource)
- Convert to markdown
- Include in the PDF as a full chapter

**B. Copyright-protected** — provide a reference table.
- Work title, recommended edition, translator, publisher, ISBN
- Price range, where to buy
- One-line note on why this edition

### 6. Front Matter

Include a preface documenting:
- The intellectual inquiry that motivated the selection
- The criteria used
- The trade-offs made and why
- The structure of the document

## Multi-Format Text Extraction Pipeline

When the anthology requires actual text from various sources (not just edition recommendations), you need a multi-format extraction pipeline:

### HTML → Plain Text
Best for translators who publish freely online (e.g., Ian Johnston's site).

```python
import urllib.request, re, html

resp = urllib.request.urlopen(url, timeout=15)
raw = resp.read().decode('utf-8')
# Strip HTML tags
text = re.sub(r'<[^>]+>', ' ', raw)
# Clean whitespace
text = re.sub(r'\s+', ' ', text).strip()
# Unescape entities
text = html.unescape(text)
```

Pitfall: Some sites work with raw HTTP, others need HTTPS. Python `urllib.request` is more reliable than `curl` for sites with security scanners. Always check for and strip `<script>`, `<style>` blocks before main tag stripping.

### PDF → Plain Text (Born-Digital PDFs)
For PDFs with embedded selectable text (e.g., avalonlibrary.net copies of Penguin editions).

```bash
pdftotext input.pdf output.txt
```

This preserves paragraph structure well. For higher quality (preserving reading order) use PyMuPDF:

```python
import fitz
doc = fitz.open("input.pdf")
text = ""
for page in doc:
    text += page.get_text()
```

### PDF → Plain Text (Scanned / Image-Only PDFs)
For scanned books where text is not selectable (image-based PDFs). Requires OCR.

```bash
# Install tools
pip install ocrmypdf
apt-get install -y tesseract-ocr tesseract-ocr-eng

# OCR the PDF (adds a searchable text layer)
ocrmypdf --force-ocr input.pdf output_ocr.pdf

# Then extract text from the OCR'd PDF
pdftotext output_ocr.pdf output.txt
```

**Pitfalls:**
- OCR quality depends on scan resolution and font. Fraktur/Gothic fonts need `tesseract-ocr-deu` or `tesseract-ocr-frk`.
- `--force-ocr` replaces all original images with compressed versions. The resulting file can be large (2-3x original).
- `ghostscript` is recommended for compression but not required for basic OCR.
- Post-OCR cleaning is almost always needed: fix hyphenation breaks, running headers merged with body text, and punctuation spacing.
- For the first pass, expect ~80-90% accuracy from English tesseract on clean scans.
### EPUB → Plain Text

EPUB is a ZIP archive containing XHTML files. Extraction:

```python
import zipfile, xml.etree.ElementTree as ET
from pathlib import Path

# EPUB is a ZIP
with zipfile.ZipFile("book.epub") as z:
    # Find the OPF file (the package document)
    opf_path = None
    for name in z.namelist():
        if name.endswith('.opf'):
            opf_path = name
            break
    
    # Parse OPF
    opf_root = ET.fromstring(z.read(opf_path))
    ns = {'opf': 'http://www.idpf.org/2007/opf'}
    opf_dir = Path(opf_path).parent
    
    # Build manifest: id → href
    manifest = {}
    for item in opf_root.findall('.//opf:manifest/opf:item', ns):
        item_id = item.get('id')
        href = item.get('href')
        manifest[item_id] = href
    
    # Read spine order (CRITICAL: this defines reading order, not the manifest)
    spine_ids = []
    for itemref in opf_root.findall('.//opf:spine/opf:itemref', ns):
        idref = itemref.get('idref')
        spine_ids.append(idref)
    
    # Extract text in spine order
    all_text = ""
    for idref in spine_ids:
        if idref not in manifest:
            continue
        href = manifest[idref]
        if not href.endswith(('.xhtml', '.html', '.htm')):
            continue
        
        full_path = opf_dir / href
        content = z.read(str(full_path))
        # Use BeautifulSoup for better structure preservation
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        for tag in soup(['script', 'style', 'nav']):
            tag.decompose()
        body = soup.find('body')
        if body:
            text = body.get_text(separator='\\n')
            all_text += text + "\\n\\n"
```

**CRITICAL — spine vs manifest order:** EPUBs have both a `<manifest>` (list of ALL files) and a `<spine>` (the *reading order*). Iterating over manifest items produces content in random order (often pushing the Prologue after Part 4 or mixing preliminary pages with body text). Always use spine order via `<opf:spine>/<opf:itemref>` tags, not manifest `<opf:item>` tags.

**⚠️ Common mistake — alphabetical filename sorting:** A naive `sorted(z.namelist())` followed by `.endswith('.html')` filter sorts files alphabetically, which places `prologue.html` after `part4_chap_20.html`. The extracted text will have no Prologue or the Prologue buried at the end. This happened in the Nietzsche anthology — the Prologue was present in the EPUB but invisible in the output. Fix: always extract via spine order, never via filesystem or sorted manifest order.

**Pitfalls:**
- EPUB is a ZIP but may have a `.epub` extension. Always try `zipfile.is_zipfile()` first.
- OPF namespace varies. Check the actual namespace from the root element.
- Some EPUBs split content into many small files (50+). Always use spine order, never filesystem or manifest order.
- Some EPUBs have DRM that prevents extraction. These will decrypt only if the user has the key.
- For properly preserved structural markup, use BeautifulSoup `<body>` extraction instead of regex HTML stripping — it preserves paragraph boundaries, section breaks, and footnote markers.

### Project Gutenberg → Plain Text
Gutenberg offers multiple formats. For text, use the "Plain Text UTF-8" link.

```bash
wget -O output.txt "https://www.gutenberg.org/cache/epub/52263/pg52263.txt"
```

**Pitfall:** Gutenberg files include extensive boilerplate header/footer (license, production notes). Strip everything before "*** START OF THE PROJECT GUTENBERG EBOOK" and after "*** END OF THE PROJECT GUTENBERG EBOOK".

### LibGen/Anna's Archive → PDF/EPUB Download

When a user explicitly authorizes sourcing copyrighted translations for personal research compilation, the most reliable path is:

1. **Search by ISBN**: Most reliable identifier. Use `https://libgen.li/index.php?req=ISBN` or `https://libgen.is/search.php?req=ISBN`.
2. **Search by title+translator**: Secondary fallback when ISBN returns no results.
3. **Mirror availability**: `libgen.is` is often unavailable; `libgen.li` is more reliable. Anna's Archive can also be slow or blocked depending on network environment.
4. **Download**: Each LibGen result page has multiple download links (Cloudflare, IPFS, direct). Try several — some go dead.

**Pitfalls:**
- LibGen mirrors rotate; verify accessibility before building a workflow around one.
- AVALONLIBRARY.NET is a reliable source for public-domain-licensed translations (carries Hollingdale's Nietzsche PDFs as free downloads, explicitly attribution-only licensed).
- Internet Archive books are typically borrow-only or controlled digital lending, not downloadable unless public domain in the US.
- Some LibGen results are mislabeled — an EPUB may actually be an HTML file renamed. Always verify file integrity after download.

## Thematic vs. Chronological Organization

Anthologies can be organized two ways. Choose based on use case:

### Chronological (by work / by book order)
- **When to use**: Survey of a thinker's development, reading the corpus in order
- **Structure**: Each work gets its own chapter; passages appear in original sequence
- **Good for**: First-time readers, comprehensive reference

### Thematic (by concept / by inquiry)
- **When to use**: The user is pursuing a specific question (e.g., "what makes civilizations great") and needs Nietzsche's answer assembled from across the corpus
- **Structure**: Parts correspond to themes (Foundation of Rank, Breeding, Decadence, etc.); passages from different works sit side by side within each theme
- **Good for**: Writing projects, targeted research, argument assembly
- **Implementation**: After extraction, map each passage to a theme and order themes by logical progression (foundation → development → peak → decline)

### Hybrid (Recommended)
- Organize thematically for the user's inquiry
- Within each theme, sequence passages chronologically by work to preserve provenance
- Cross-reference passages that appear in multiple themes (e.g., BGE §257 anchors both "Foundation of Rank" and "Pathos of Distance")
- Include a work-by-work appendix for readers who want to find passages within their original context

## PDF Compilation from Mixed Sources

When the anthology draws from multiple extraction formats (HTML, PDF-text, OCR, EPUB), use a Python compilation script:

1. **Segment each source text** into individual passages (by aphorism/section number)
2. **Tag each passage** with metadata: work title, translator, section number
3. **Sort passage tags** into thematic buckets
4. **Render each bucket** as a chapter with passage-by-passage blockquotes
5. **Insert translator credits** as subheadings on each passage
6. **Generate front matter** (title page, table of contents, introduction)
7. **Compile to PDF** using fpdf2 (see `book-pdf-compilation` skill for fpdf2 patterns)

The Python script should be structured as a standalone `build_anthology.py` that reads from tagged source files and writes the anthology, so it can be re-run when sources change.

## Pitfalls

- **Copyright assumptions**: Public domain ≠ free to redistribute commercially. Check the translator's license (Johnston explicitly allows personal use and editing; commercial use needs permission).
- **Translator drift**: A translator good on one work may be wrong on another (e.g., Kaufmann's *Joyful Science* is better than his *Genealogy*). Evaluate per-work, not per-translator.
- **Missing works**: The only good translation may be copyrighted. Don't force-fit a bad PD translation — note it openly and recommend the purchase.
- **The user will disagree with your criteria**: The criteria must reflect *their* inquiry, not generic academic consensus. A scholar-recommended translation may be wrong for a project that needs *bite* over precision.
- **The inquiry can shift mid-project**: The user may start with style and pivot to fidelity once they start writing. Structure the anthology so it's modular — swap in different translations of individual works without rebuilding everything.
- **Subagent file isolation**: Subagents create files in their own sandbox. Files created by a subagent may not be accessible from the parent agent's file tools (read_file may return "File not found" even when search_files lists them). Use subagents for the *build* and verify file existence with a second subagent, not with parent tools.
- **Format detection**: An `.epub` file may actually be HTML masquerading. A `.pdf` may be an HTML search page. Always verify file integrity (check bytes, try to unzip EPUB, run `file` command) before building a pipeline around a downloaded file.
- **OCRed text quality**: Scanned PDFs OCR'd by tesseract reach ~90% accuracy for clean English text, lower for Fraktur or mixed-language sources. Budget for manual cleaning iterations. Always sample 5-8 pages of the final PDF before delivery.
