# Johnston Translation Text Cleaning (Nietzsche)

Ian Johnston's translations of Nietzsche (Birth of Tragedy, Beyond Good and Evil, Genealogy of Morals, Use and Abuse of History) are available as plain-text files from [johnstoniatexts.com](http://johnstoniatexts.com). They have a consistent structure but each work has unique cleaning requirements.

## Common Source Characteristics

- **Encoding**: UTF-8 with CRLF (`\r\n`) line endings
- **Non-breaking spaces**: Heavy use of `\xa0` (non-breaking space) in place of regular spaces, especially in header/boilerplate blocks
- **Footnote markers**: Inline `{1}` through `{85}` style markers (curly brackets with numbers)
- **Endnotes**: Work-specific endnotes sections with `(1)` through `(N)` references
- **Translator notes**: Inline `[square bracket annotations]` throughout
- **Copyright boilerplate**: Standard block at top of each file (translator credit, download links, RTF references, student/teacher distribution notice)
- **Section dividers**: BGE uses `============================================================` between its 9 parts

## Per-Work Cleaning Patterns

### Birth of Tragedy (`birth_of_tragedy_johnston.txt`)
- **Content start marker**: `THE BIRTH OF TRAGEDY` (all caps, appears after historical note)
- **Endnotes marker**: `ENDNOTES` (strip everything from here to end of file)
- **Sections**: Numbered sections 1-25 with "AN ATTEMPT AT SELF-CRITICISM" as preface
- **Structure**: One continuous text with no `=====` dividers

### Beyond Good and Evil (`bge_johnston_full.txt`)
- **Content start marker**: `PROLOGUE` (appears after title page)
- **Structure**: 21 sections separated by `=====` lines
  - Section 0: PROLOGUE content (4550 chars)
  - Section 1: Part heading ("Part 1: On the Prejudices of Philosophers", 41 chars)
  - Section 2: Part 1 content + boilerplate + NOTES (~50K chars)
  - Repeat pattern for remaining 9 parts
- **Part heading detection**: Short sections (<200 chars) after `=====` are part headings. Content sections contain boilerplate that must be stripped with line-by-line detection.
- **NOTES sections**: Each part has its own endnotes section starting with `NOTES` followed by `(1)`, `(2)` etc. Strip these after each part's content.
- **Repeated boilerplate**: The full copyright/translator block repeats at the start of every part's content section.

### Genealogy of Morals (`genealogy_johnston_full.txt`)
- **Content start marker**: Last standalone `Prologue` line (appears 3 times: filename header, link text, actual heading)
- **Structure**: Prologue + 3 Essays (First, Second, Third) with numbered sections
- **Endnotes**: ENDNOTES sections appear AFTER each essay (not just at the end), followed by copyright boilerplate blocks. There are 4 ENDNOTES blocks total — strip ALL of them, not just the trailing one.
- **Copyright boilerplate between essays**: After each essay's ENDNOTES, a block precedes the next essay containing:
  - `2014` (copyright year, standalone line)
  - `[Students, teachers...` (permission notice)
  - `Note that in the following text...` (translator note)
  - `If you would like to download...` (RTF download link)
  - `Nietzsche, Genealogy of Morals, Essay X` (header line)
- **Special**: Has `Nietzsche, Genealogy of Morals, Prologue` header line at very top

**Recommended approach** — split on essay boundaries, remove everything between each essay's ENDNOTES and the next essay heading:
```python
text = re.sub(r'\n\s*ENDNOTES\s*\n.*?(?=\nFirst\s+Essay|\nSecond\s+Essay|\nThird\s+Essay|\Z)', '\n', text, flags=re.DOTALL)
```
Then run `strip_boilerplate_block()` to remove residual copyright/download lines, followed by footnote marker stripping. This handles all 4 endnotes blocks in one pass.

### Use and Abuse of History (`use_abuse_history_johnston.txt`)
- **Content start marker**: `PREFACE` (NOT "Foreword" — there is no Foreword heading)
- **Structure**: PREFACE + 10 chapters, no explicit chapter headings in body text
- **Boilerplate stripping critical**: Has dense copyright block with split-line artifacts

## Cleaning Strategy

### Step 1: Locate Real Content Start

For each work, find the content start marker in the RAW text (before any stripping), then take `text[idx:]`:

```python
idx = text.find("PROLOGUE")      # BGE
idx = text.rfind("Prologue")     # Genealogy (last occurrence)
idx = text.find("PREFACE")       # Use and Abuse
idx = text.find("THE BIRTH OF TRAGEDY")  # Birth of Tragedy
```

### Step 2: Split on Structural Boundaries (BGE only)

BGE uses `=====` dividers between parts. Split BEFORE stripping boilerplate:

```python
sections = re.split(r'\n={5,}\n', text)
for sec in sections:
    if len(sec) < 200:
        # Part heading — create page break
    else:
        # Content section — strip boilerplate, NOTES, markers
        sec = strip_boilerplate_block(sec)
        sec = strip_endnotes_sections(sec)
        sec = strip_footnote_markers(sec)
```

### Step 3: Strip Boilerplate (all works)

Use line-by-line detection with these considerations:

1. **Strip `\\xa0` before matching**: `cleaned = line.replace('\\xa0', '')` — Python's `.strip()` doesn't remove `\\xa0`
2. **Use `in` not regex anchors**: Boilerplate can start mid-line after stripping. Check `'[RTF]' in line` not `r'^\\[RTF\\]'`
3. **Fragment prefixes**: Split lines like `'[Table '` / `'of Contents...'` need `'[Table' in line` checks AND a separate `'of Contents' in line` for the continuation
4. **Set vs pattern**: Use both a set of exact boilerplate strings AND regex patterns with `.search()` (not `.match()`)
5. **Genealogy-specific items to catch**: `2014` (copyright year), `If you ` (download link prefix), `Nietzsche, Genealogy` (essay header lines) — these appear between essays and must be stripped to avoid copyright boilerplate pages

### Step 4: Strip Editorial Apparatus

```python
text = re.sub(r'\\{[0-9]+\\}', '', text)           # {1}, {2} markers
text = re.sub(r'\\([0-9]+\\)', '', text)            # (1), (2) markers  
text = re.sub(r'\\[Back\\s+to\\s+Text\\]', '', text)  # endnote back-references
# BGE: strip NOTES blocks between ===== section dividers
text = re.sub(r'\\n\\s*NOTES\\s*\\n.*?(?=\\n={5,}\\n|\\Z)', '', text, flags=re.DOTALL)
# Genealogy: strip ALL endnotes blocks (embedded between essays, not just trailing).
# The Genealogy source has 4 ENDNOTES blocks — between Prologue/First Essay,
# First/Second, Second/Third, and at the end. Each is followed by copyright boilerplate.
text = re.sub(r'\\n\\s*ENDNOTES\\s*\\n.*?(?=\\nFirst\\s+Essay|\\nSecond\\s+Essay|\\nThird\\s+Essay|\\Z)', '\\n', text, flags=re.DOTALL)
```

### Step 5: Normalize

```python
text = text.replace('\\r\\n', '\\n').replace('\\r', '\\n')
# CRITICAL: Remove \\xa0 on otherwise-empty lines before collapsing newlines.
# Johnston sources use \\n\\xa0\\n (non-breaking space on a visually blank line)
# instead of \\n\\n. Without this fix, \\n\\n paragraph detection fails, collapsing
# entire sections into monster paragraphs. Combined with all-caps heading handling,
# this can silently discard thousands of characters of body text.
text = re.sub(r'\\n\\xa0\\n', '\\n\\n', text)
text = re.sub(r'\\n{4,}', '\\n\\n\\n', text)  # Collapse excess blank lines
```

## Boilerplate Fragments Known to Span Multiple Lines

From the BGE source, these artifacts appear across separate physical lines:

```
Line N:   '[Table '
Line N+1: 'of Contents for\xa0Beyond Good and Evil]'
```

Detect with `'[Table' in cleaned` to catch line N. Line N+1 (`'of Contents for\xa0...'`) needs its own catch — `'[Table'` alone misses it:
```python
if '[RTF]' in cleaned or '[Table' in cleaned or 'of Contents' in cleaned:
    return True
```

From the Genealogy source, the essay boilerplate header lines also span:
```
Line N:   'Nietzsche, Genealogy of Morals, Essay X'
Line N+1: '2014'
...
Line N+K: 'If you  would like to download...'
```

The `Nietzsche, Genealogy` header line and `2014` are single-line items best added to the boilerplate set or pattern list. `If you ` and `of Contents for` are prefix fragments that should use `startswith()` or `in` checks.

## Critical Compounding Bug: `\\xa0` + All-Caps Heading = Silent Content Loss

**This is the most destructive silent failure in the Johnston FPDF pipeline.** Two independent issues compound to discard thousands of characters with no error message:

1. **`\\xa0` on empty lines** (Step 5 above): Johnston sources use `\\n\\xa0\\n` instead of `\\n\\n`. When `clean_generic()` doesn't strip these before collapsing newlines, `write_body()`'s `text.split('\\n\\n')` sees the entire section as one continuous paragraph.

2. **All-caps heading handler** (in `write_body()`): When paragraph `[0]` after the failed split is the all-caps heading (e.g. `PART TWO`), the handler renders just the heading and `continue`s — **discarding all remaining lines** in the paragraph. With the `\\xa0` collapse, this means the entire Part 2 content (42K+ chars) is silently lost.

**Symptoms of this bug:**
- A build that should produce ~145 pages for BGE produces ~22 pages instead
- Part 2 through Part 9 each occupy 1 page (just the heading) instead of 8-12 pages of content
- No error, no warning — the PDF just ends suspiciously early
- PyMuPDF inspection shows the text blocks exist at the FPDF level but only contain heading lines

**Fix requires both parts:**

In `clean_generic()`:
```python
text = re.sub(r'\\n\\xa0\\n', '\\n\\n', text)  # Strip \\xa0 before collapsing
text = re.sub(r'\\n{4,}', '\\n\\n\\n', text)
```

In `write_body()` all-caps heading handler:
```python
if (first.isupper() and len(first) > 4 and len(first) < 100 and '[' not in first):
    self.multi_cell(0, 7, first, align="C")
    self.ln(3)
    # CRITICAL: render remaining lines as body text — don't just `continue`
    if len(lines) > 1:
        rest = ' '.join(l.strip() for l in lines[1:] if l.strip())
        if rest:
            self.write_paragraph(rest)
            self.ln(LEADING / 2)
    continue
```

**Verification after fix:** Page counts for BGE should be ~140-150 (not 22). Check with PyMuPDF that each Part section has multiple pages of body text, not just the heading page.

## Reference Script

The full build script is at `/root/work/scripts/build_johnston_pdfs.py`. It handles all 4 works with:
- Individual title pages
- Part-breaking pages (BGE 9 parts each on own page)
- Centered page numbers
- Running headers
- Liberation Serif 12pt, 25mm margins, leading 6.5
- Justified paragraphs with italic preserved
