# OCR Text to PDF Workflow

When the source is raw OCR `.txt` files (not markdown chapters), the pipeline differs from the chapter-based compilation workflow.

## OCR Noise Identification

**Frequency analysis** is the most reliable method to find repeated headers:

```python
# Collect all short lines (<70 chars) across all files
# Count frequencies — lines appearing 5+ times are candidates
```

Common OCR noise in scanned books:
- **Running headers**: book title or chapter name on every page (50-150+ occurrences)
- **Library stamps**: "UNIVERSITY OF MICHIGAN", "SCIENTIA", shelf numbers
- **Page numbers**: lone 1-4 digit numbers, "PAGE" markers
- **TOC fragments**: dotted leader lines (`....`), index entries (mostly digits+commas)
- **Printing boilerplate**: publisher name, date codes, copyright lines

## Header Removal

Use an **exact-match blacklist** for known headers. Supplement with **prefix matching** for OCR merge artifacts where the header fused with trailing text:

```python
# Exact match
if stripped in {"The Mantle of Caesar", "The Historical Personality", ...}:
    remove

# Prefix match (catches "The Magic NameT" where header merged with next line)
for header in RUNNING_HEADERS:
    if stripped.startswith(header) and len(stripped) - len(header) <= 3:
        remove
```

## Line-Break Joining

Raw OCR preserves **every physical line ending from the printed book** as `\n`. These must be joined into continuous text:

```python
# After removing noise lines and fixing hyphenation
text = re.sub(r'-\s*\n\s*', '', text)  # join hyphenated words
text = re.sub(r'\n+', ' ', text)        # all newlines → spaces
```

## Continuous Text Flow

**Do NOT split on file boundaries.** OCR files represent physical pages — paragraphs in the book span across pages. Joining with `\n\n` between files creates artificial paragraph breaks at page boundaries, producing short lines.

Instead, join all cleaned text with spaces: `" ".join(all_text)`.

## fpdf2 Rendering — Use `write()`, Not `multi_cell`

Three compounding fpdf2 bugs make `multi_cell` unsuitable for continuous OCR text >~50K characters. Use `write()` instead — it avoids all three:

```python
pdf.set_font("Liberation", size=11.5)
pdf.set_x(pdf.l_margin)
pdf.write(6.2, full_text)
```

1. **x-position drift**: `multi_cell` does not reset x to the left margin between calls. x accumulates until text vanishes off the page. Fix with `set_x` before each call — but this exposes bug #3.
2. **Long-string corruption**: A single `multi_cell` call with >50K chars corrupts fpdf2's internal state (text drifts to x=527). Fix with chunking — but this exposes bug #3.
3. **Chunk boundary artifacts**: Chunked `multi_cell` creates mid-sentence breaks at chunk boundaries (e.g., "...produced his" ends one chunk, "effect by means of..." starts the next). Fix: don't chunk — use `write()`.

`write()` is always left-aligned — correct for OCR text (see justification pitfall above).

Full details, symptoms, and verification commands: see `references/ocr-page-compilation.md` → "Critical fpdf2 Pitfalls".

## Style Settings (established)

- **Font**: 12pt Liberation Serif (11.5pt acceptable for OCR text)
- **Leading**: 6.2–6.5pt
- **Margins**: 25mm
- **Alignment**: left (not justified for OCR)
- **Headers**: running header on pages >1, centered italic 9pt
- **Footers**: centered page number
- **Title page**: separate, not included in body flow
