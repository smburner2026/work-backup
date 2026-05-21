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
- **Endnotes marker**: Trailing `Notes` section at end of each essay
- **Structure**: Prologue + 3 Essays with numbered sections
- **Special**: Has `Nietzsche, Genealogy of Morals, Prologue` header line at very top

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

1. **Strip `\xa0` before matching**: `cleaned = line.replace('\xa0', '')` — Python's `.strip()` doesn't remove `\xa0`
2. **Use `in` not regex anchors**: Boilerplate can start mid-line after stripping. Check `'[RTF]' in line` not `r'^\[RTF\]'`
3. **Fragment prefixes**: Split lines like `'[Table '` / `'of Contents...'` need `'[Table' in line` checks
4. **Set vs pattern**: Use both a set of exact boilerplate strings AND regex patterns with `.search()` (not `.match()`)

### Step 4: Strip Editorial Apparatus

```python
text = re.sub(r'\{[0-9]+\}', '', text)           # {1}, {2} markers
text = re.sub(r'\([0-9]+\)', '', text)            # (1), (2) markers  
text = re.sub(r'\[Back\s+to\s+Text\]', '', text)  # endnote back-references
text = re.sub(r'\n\s*NOTES\s*\n.*?(?=\n={5,}\n|\Z)', '', text, flags=re.DOTALL)  # NOTES blocks
```

### Step 5: Normalize

```python
text = text.replace('\r\n', '\n').replace('\r', '\n')
text = re.sub(r'\n{4,}', '\n\n\n', text)  # Collapse excess blank lines
```

## Boilerplate Fragments Known to Span Multiple Lines

From the BGE source, these artifacts appear across separate physical lines:

```
Line N:   '[Table '
Line N+1: 'of Contents for\xa0Beyond Good and Evil]'
```

Detect with `'[Table' in cleaned` rather than requiring the full `'[Table of Contents'` string.

## Reference Script

The full build script is at `/root/work/scripts/build_johnston_pdfs.py`. It handles all 4 works with:
- Individual title pages
- Part-breaking pages (BGE 9 parts each on own page)
- Centered page numbers
- Running headers
- Liberation Serif 12pt, 25mm margins, leading 6.5
- Justified paragraphs with italic preserved
