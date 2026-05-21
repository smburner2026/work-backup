# WeasyPrint PDF Workflow (Alternative to fpdf2)

Use this path when the user needs **typographic quality** — CSS-controlled layout, proper justification with hyphenation, font variety, and precise page geometry. WeasyPrint renders HTML+CSS to PDF via WebKit, producing book-quality output at the cost of higher memory usage.

## When to Use

- User specifies a font that isn't Liberation Serif (DejaVu Serif, EB Garamond, etc.)
- User wants body text at 14pt or above (fpdf2's cell/multi_cell system gets unwieldy at large sizes)
- Full CSS control needed (page margins, headers/footers, page numbers, tables)
- Input is markdown that converts naturally to HTML
- The book has complex layout requirements (pull quotes, side notes, multiple columns)

## When NOT to Use (use fpdf2 instead)

- Input is OCR text with unpredictable line breaks
- The server has less than 512MB available RAM (WeasyPrint builds a full DOM)
- The source text is over 5MB (WeasyPrint DOM+rendering uses ~200MB+ per MB of text)
- The output is an academic manuscript with Liberation Serif 12pt (fpdf2 is faster)

## Memory-Constrained Server Strategy

When the server has limited RAM (<2GB) and the corpus is large (>5MB text):

1. **Split by work** — build each work/part as its own small PDF
2. **Use `pdfunite` (poppler-utils)** to merge them into one final volume
3. Never let a single WeasyPrint call exceed ~3MB of text (~200MB peak memory)

### Per-Work Build Pattern

```python
import subprocess

pdfs = []
for work_name, html_body in works:
    path = f\"build_tmp/{work_name}.pdf\"
    build_small_pdf(html_body, path)  # One WeasyPrint call per work
    pdfs.append(path)

# Merge with pdfunite
subprocess.run([\"pdfunite\"] + pdfs + [\"final_output.pdf\"])
```

**Sub-split pattern for oversized works:** Even with per-work splitting, some individual works may be too large for a single WeasyPrint call on a memory-constrained server (~2GB RAM). A single 1.6MB source text can produce a WeasyPrint process that uses 300-500MB+ peak memory. If a build times out or crashes, split that single work into two halves at a natural paragraph boundary:

```python
# Split in half at a double-newline near the midpoint
mid = len(body) // 2
split_point = body.find('\n\n', mid)
if split_point == -1:
    split_point = mid
part1, part2 = body[:split_point], body[split_point:]

# Build each half as a separate PDF, then pdfunite merges them
build_part(part1, f\"{name}_p1\")
build_part(part2, f\"{name}_p2\")
```

This was required for Kaufmann's Will to Power (~1.6MB source text) — building as a single PDF consumed 550MB+ RAM and timed out on a 2GB VPS. Splitting into two halves (565KB + 550KB PDFs) fixed it.

Each work PDF builds with WeasyPrint in isolation. Memory is freed between builds. The merge is a trivial PDF operation.

## Source Text Cleaning (Required Preprocessing)

Before feeding any text into the markdown-to-HTML pipeline, always run a `cleanup_text()` pass. Source texts from Project Gutenberg, OCR, Anna's Archive, and similar sources accumulate artifacts that break layout engines:

```python
def cleanup_text(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)       # Collapse excess blank lines
    text = re.sub(r'  +', ' ', text)              # Collapse double spaces (CRITICAL — OCR/digitised texts frequently have variable inter-word spacing)
    text = re.sub(r'(\w)_(\w)', r'\1 \2', text)  # Fix underscore artifacts from OCR
    text = text.replace('`', '')                   # Remove backticks (trigger monospace font in WeasyPrint)
    # --- OCR one-word-per-line reflow ---
    # Some source texts (especially from PDF text extraction) have every word on its own line.
    # This pass joins consecutive short lines into proper paragraphs.
    import re as _re
    lines = text.split('\n')
    reflowed = []
    buffer = []
    standalone_punct = {'.', '..', '...', '. . .', '. .', ':', ';', ',', '!', '?'}
    heading_starts = {'chapter', 'part', 'book', 'section', 'preface', 'introduction',
                      'note', 'appendix', 'index', 'volume',
                      'book first', 'book second', 'book third', 'book fourth', 'book fifth',
                      'first part', 'second part', 'third part', 'fourth part'}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                reflowed.append(' '.join(buffer))
                buffer = []
            reflowed.append('')
            continue
        if stripped in standalone_punct:
            if buffer:
                buffer[-1] = buffer[-1] + stripped
            continue
        word_count = len(stripped.split())
        is_heading_like = (stripped.startswith(('#', '*')) 
                          or stripped.isupper() and len(stripped) > 2
                          or any(stripped.lower().startswith(h) for h in heading_starts))
        if word_count <= 5 and not is_heading_like:
            buffer.append(stripped)
            continue
        if buffer:
            reflowed.append(' '.join(buffer))
            buffer = []
        reflowed.append(stripped)
    if buffer:
        reflowed.append(' '.join(buffer))
    text = '\n'.join(reflowed)
    # Break unreasonably long lines (2000+ char paragraphs defeat WeasyPrint's overflow-wrap)
    lines = []
    for line in text.split('\n'):
        while len(line) > 300:
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
```

**Why each step matters:**
- **Double spaces** — OCR text often has 2-3 spaces between words from justified source PDFs. WeasyPrint's HTML renderer may not collapse these consistently, causing words to break onto individual lines or text to render with irregular spacing.
- **Backticks** — Stanford critical edition volumes use backtick markers for citations. Without stripping, WeasyPrint renders them as `<code>` → DejaVu Sans Mono, creating a jarring font switch mid-page.
- **Underscore artifacts** — OCR occasionally produces mid-word underscores as noise (`desire_` → `desire`).

## CSS Template for Book-Quality PDF

```css
@page {
    size: 6in 9in;              /* Standard trade paperback */
    margin: 1.2in 1in 1in 1in;
    @bottom-center {
        content: counter(page);
        font-family: 'Liberation Serif', Georgia, serif;
        font-size: 9pt;
        color: #666;
    }
}
body {
    font-family: 'Liberation Serif', Georgia, serif;  /* User's preferred font (same family as fpdf2 path) */
    font-size: 11pt;            /* 11pt for anthologies/collections; 12pt for standard books; 14pt for short standalone */
    line-height: 1.55;
    text-align: left;           /* Left-align for OCR/spaced text; use 'justify' only for clean markdown source */
    hyphens: auto;
    color: #1a1a1a;
    overflow-wrap: break-word;  /* CRITICAL: prevents long words running off the page */
    word-wrap: break-word;      /* Legacy fallback */
    word-break: break-word;     /* Third layer — still needed for extreme cases (2000+ char Kaufmann WtP paragraphs) */
}
p {
    margin: 0.5em 0;
    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;     /* Per-paragraph repeat — fails without this on ultra-dense source text */
    hyphens: auto;
    max-width: 100%;
}
```

### Book-Style Typesetting (User Preference)

After multiple build iterations with explicit feedback, the user's standard for "feels like a real book" is:

```css
@page { size: 6in 9in; margin: 0.7in 0.65in 0.75in 0.65in; }
body {
    font-family: 'Liberation Serif', Georgia, serif;
    font-size: 10pt;
    line-height: 1.3;
    orphans: 3; widows: 3;
    hyphens: auto;
    text-align: left;
}
p {
    margin: 0;
    text-indent: 1.2em;
}
/* Book convention: no indent on first paragraph after heading */
h1 + p, h2 + p, h3 + p, h1.part + p { text-indent: 0; }
/* Metadata, lists, blockquotes — no indent */
p.work-meta, li, blockquote p { text-indent: 0; }
```

Key differences from standard WeasyPrint CSS:
- **Tighter margins** (0.7in/0.65in vs 1in/0.85in) — gives more text per page
- **Line-height 1.3** (vs 1.5) — book-like density, not manuscript spacing
- **Paragraph indent, not paragraph spacing** — `margin: 0; text-indent: 1.2em` instead of `margin: 0.5em 0`
- **No indent after headings** — `h1 + p, h2 + p { text-indent: 0; }`
- **Orphans/widows control** — prevents single lines at page breaks
- **Left-align, not justify** — the user values consistency over justification

This was iterated over 4+ builds. Each build dimension comes from a specific user complaint: "margins are too big", "line spacing is too loose", "footnote numbers need to be removed", "doesn't feel like a put together book". Apply ALL at once — don't ship incrementally and let them test each one.

### Text Alignment Decision

| Source quality | Alignment | Reason |
|---|---|---|
| Clean markdown | `justify` | WeasyPrint justification works well |
| Plain text, spaced (OCR artifacts, double spaces) | `left` | Justified text exaggerates spacing artifacts; words break onto individual lines. This is the same principle as `align='L'` for fpdf2 OCR text. |
| Mixed (some works clean, some digitised) | `left` | Consistent ragged-right avoids the problem entirely |

### Font Sizing by Book Type

| Book type | Body pt | h1 | h2 | h3 | Margin in |
|-----------|---------|----|----|----|-----------|
| Anthology (2000+ pages) | 11pt | 18pt | 14pt | 12pt | 0.85in |
| Standard book (300-1500p) | 12pt | 20pt | 16pt | 13pt | 1in |
| Short work / standalone | 14pt | 22pt | 17pt | 14pt | 1in |

### Scaled Headings (relative to 11pt body)

| Element | Size | Ratio |
|---------|------|-------|
| Body | 14pt | 1× |
| h3 | 14pt | 1× |
| h2 | 17pt | 1.21× |
| h1 | 22pt | 1.57× |
| Title page title | 28pt | 2× |
| Blockquote | 13pt | 0.93× |
| Meta/credits | 11pt | 0.79× |
| Page number | 9pt | 0.64× |

If user requests a different body font size (e.g. 12pt, 16pt), scale all heading sizes proportionally.

## Markdown to PDF Pipeline

1. Assemble all source texts into one markdown file with `#` headings per work
2. Convert markdown to HTML (simple regex-based conversion for headings, paragraphs, bold/italic, blockquotes)
3. Wrap with CSS + doctype
4. Write to temp `.html` file
5. `HTML(filename=html_path).write_pdf(output_path)` via WeasyPrint
6. Delete temp `.html`

### HTML Construction (for per-work builds)

```python
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">{CSS}</head>
<body>
<h1 class="part">{part_label}</h1>
<h1>{work_title}</h1>
<div class="work-meta">{year} — Translated by {translator}</div>
{markdown_to_html(body_text)}
</body></html>'''
```

## Long Build Strategy (Background)

When the full build takes more than a minute (common for 10+ works, 5+ MB text):

1. Write the build script that does per-work → merge
2. Fire as a background terminal process:

```python
terminal(command='cd /project && python3 build_book.py', 
         background=True, notify_on_complete=True, timeout=600)
```

3. The system auto-notifies when done — keep working on other tasks
4. Verify the output PDF page count and file size before delivering

## Pitfalls

- **[CRITICAL] Words overflow the page by default** — WeasyPrint does NOT break long words. Every CSS stylesheet MUST include `overflow-wrap: break-word; word-wrap: break-word;` on the body rule. Without it, any word wider than the text column (German compounds, chemical names, Greek terms, URL-like strings in serif fonts) will bleed into the margin or off the page. This is the single most consistent failure across all PDF build projects — check for it every time.\n- **EVEN WITH overflow-wrap, single-line paragraphs >300 chars overflow** — source texts with 2000+ character lines (e.g. Kaufmann's Will to Power) defeat `overflow-wrap` alone. Three fixes required: (1) add `word-break: break-word;` to body AND p CSS rules, (2) add text-level line breaking in cleanup_text() that splits lines at 300 chars on word boundaries, (3) add per-paragraph overflow-wrap to `<p>` elements. All three layers together are what finally stopped the running-off-page bug.\n- **Font size vs page width** — DejaVu Serif at 14pt on a 6×9 page with 1in margins leaves only ~4in text width. Long words WILL overflow at this size. For anthologies and collections, use 11pt body. See the sizing table above.
- **WeasyPrint leaks memory on large documents** — never feed it more than ~3MB of text at once. Split the work.
- **`hyphens: auto` requires a CSS hyphenation dictionary** — DejaVu Serif has built-in hyphenation in WeasyPrint, but custom fonts may need `lang="en"` attribute on `<html>`.
- **WeasyPrint 68+ (current)** handles most CSS3 but does NOT support `column-count` with `@page` breaks reliably.
- **The HTML intermediate can be larger than the final PDF** — 8.9MB of markdown → 35MB of HTML temp → 15MB PDF. Budget disk space.
- **`pdfunite` preserves each page's layout** — if works have different margins or styles between PDFs, the final merged PDF will have inconsistent page styling. Define ONE CSS for all works.
- **DejaVu Serif is always available on Ubuntu/Debian** (packaged in `fonts-dejavu-core`). It renders bold weights and italic with full character coverage including Greek and Cyrillic.
