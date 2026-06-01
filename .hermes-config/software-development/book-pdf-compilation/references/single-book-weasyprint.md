# Single-Book WeasyPrint Compilation

## When to Use This

You have a single translated book (plain text, 30K–150K words) from a translation pipeline and need a bound PDF with proper book layout. The text has been segmented into parts and chapters during translation and is in a single plain text file.

This is lighter and simpler than the anthology pipeline — no multi-source merging, no EPUB spine ordering, no per-work build scripts. Just clean plain text → HTML → WeasyPrint.

## Workflow

### 1. Parse structure from the plain text

The translation output has section markers like `PART ONE`, `PART TWO`, chapter headings in Roman numerals:

```python
import re

with open('translation.txt') as f:
    text = f.read()

# Split into lines for structural detection
lines = text.split('\n')

# Detect part breaks
part_pattern = re.compile(
    r'^(PART (?:ONE|TWO|THREE|FOUR|FIVE|SIX)|THE DEATH OF|BA-PHUC|CAPTURE AND)',
    re.IGNORECASE
)

# Detect chapter headings (I —, II —, III. —, IV. — etc.)
chapter_pattern = re.compile(r'^[IVXL]+\s*[.—]\s*')
```

### 2. Split into logical blocks

Group lines sequentially into:
- **Title page** (first block — suppress running headers)
- **Table of contents** (second block — collect all part/chapter headings)
- **Content blocks** — each is either:
  - *Part break*: gets its own recto page with centered title
  - *Chapter heading*: inline heading before body text
  - *Body paragraphs*: justified text with first-line indent

### 3. Generate HTML with CSS book layout

```css
@page {
  size: 6in 9in;
  margin: 1in 1.25in 1in 1.25in;
  @top-center {
    content: "BOOK TITLE";
    font-family: "Liberation Serif", serif;
    font-size: 8pt;
    font-style: italic;
    color: #666;
  }
  @bottom-center {
    content: counter(page);
    font-family: "Liberation Serif", serif;
    font-size: 9pt;
    color: #333;
  }
}

@page :first {
  @top-center { content: none; }
  @bottom-center { content: none; }
}

body {
  font-family: "Liberation Serif", "DejaVu Serif", serif;
  font-size: 10.5pt;
  line-height: 1.6;
  color: #1a1a1a;
  overflow-wrap: break-word;
  word-wrap: break-word;
  widows: 2;
  orphans: 2;
}
```

**Critical:** `overflow-wrap: break-word` prevents WeasyPrint's default behaviour of letting long words overflow the text column. This is the most common single-book PDF failure.

### 4. Title page

```html
<div class="title-page" style="page-break-after: always; text-align: center; padding-top: 30%;">
  <div class="title-block">
    <div class="half-title" style="font-size: 22pt; font-weight: bold; letter-spacing: 0.05em; margin-bottom: 0.5em;">BOOK TITLE</div>
    <div class="byline" style="font-size: 12pt; font-variant: small-caps; letter-spacing: 0.15em; margin-bottom: 1.5em;">BY AUTHOR NAME</div>
    <div class="subtitle" style="font-size: 10pt; color: #555; font-style: italic; margin-bottom: 0.5em;">Translated from the French</div>
    <div class="year" style="font-size: 10pt; color: #555;">1933 / 2026</div>
  </div>
  <div class="imprint" style="margin-top: 4em; font-size: 8.5pt; color: #666; line-height: 1.4;">
    <p><em>Original Title</em> was first published in Paris by Les Éditions de France in 1933.<br>
    This English translation was produced in 2026.</p>
  </div>
</div>
```

### 5. Part break page

```html
<div class="part-break" style="page-break-before: always; padding-top: 25%; text-align: center;">
  <h1 style="font-size: 18pt; font-weight: bold; letter-spacing: 0.1em; line-height: 1.4;">
    PART ONE<br>
    <span style="font-size: 13pt; font-style: italic; letter-spacing: 0.05em;">BA-PHUC, OR THE ADOPTIVE FATHER</span>
  </h1>
</div>
```

### 6. Chapter heading

```css
h2.chapter-title {
  font-size: 11pt;
  font-weight: bold;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  font-variant: small-caps;
  letter-spacing: 0.05em;
}
```

### 7. RENDER

```python
import weasyprint

doc = weasyprint.HTML(string=full_html).render()
doc.write_pdf('output.pdf')
page_count = len(doc.pages)
print(f"PDF: output.pdf ({page_count} pages)")
```

### 8. Verify

```bash
pdfinfo output.pdf
pdftotext -l 4 output.pdf - | head -30
```

## Worked Example: Hoang-Tham, Pirate

| Metric | Value |
|--------|-------|
| Source text | 60K English words, 5 merged segments |
| Trim size | 6in × 9in |
| Body font | Liberation Serif 10.5pt |
| Line height | 1.6 |
| Pages | 274 |
| File size | 0.6 MB |
| Structure | Title page → TOC → 6 parts (each on recto) → End |

## Pitfalls

- **@page :first must suppress both top and bottom content** — otherwise running headers bleed onto the title page
- **WeasyPrint word overflow**: Always add `overflow-wrap: break-word; word-wrap: break-word;` — this is the #1 cause of visual defects
- **Text-indent vs first-paragraph**: Use `text-indent: 1.5em` on `p` and suppress for `h2 + p, h3 + p, .part-break p:first-of-type` via CSS adjacent sibling selectors
- **Part-break detection**: Chapter headings like `V. — A LANG-THUONG` start with Roman numerals but are chapters, not parts. Only the major `PART` headings get recto-page treatment
- **Font fallback**: Verify Liberation Serif is installed: `dpkg -l fonts-liberation` or `fc-list | grep Liberation`
- **OCR Roman numeral collisions**: `V. — NETTOYAGES` vs section references to footnotes. Require the heading to be a standalone line (first content in its section) not inline text
- **End-matter TOC from original book:** The original book's back-of-book Table of Contents may have been translated as body text. When building the compiled PDF's TOC from structure markers (PART ONE, II —, etc.), these duplicated entries get picked up and pollute the TOC. **Fix:** truncate the source text at the natural book ending (e.g. at "THE END" or the colophon) before feeding it to the compiler. Check with `pdftotext -l 4 output.pdf - | grep 'PART ONE'` — each part should appear exactly once.
- **Subtitle rendered twice in TOC:** When a part heading is immediately followed by a subtitle line (e.g. "PART ONE" then "BA-PHUC, OR THE ADOPTIVE FATHER"), the TOC builder may add the subtitle twice — once embedded in the part entry and once as a standalone sub-heading. **Fix:** track which part subtitles have already been rendered and skip duplicates. Use a `seen_subtitles` set keyed on `stripped.upper()`. Verify with `pdftotext -l 4 output.pdf - | grep 'ADOPTIVE FATHER'` — should be exactly 1.
- **Duplicate chapter headings from continued sections:** A long chapter may have a sub-break (e.g. "II — THE FACE LOST… AND REGAINED" followed later by "II — FACE LOST AND REGAINED (continued)"). Normalize chapter keys by stripping parenthetical suffixes like `(continued)`, `(suite)`, or truncate to the first 40 chars before comparing for dedup.
