# DOCX Compilation from Chapter Files (python-docx)

Alternative to the PDF/fpdf2 path. Use when the user wants a Word document for review, editing, or track-changes workflow.

## Workflow

### 1. Establish Chapter Order

**Do NOT rely on filename sorting** — individual chapter files are often named inconsistently (German slugs, alphabetic sorting ≠ Roman numeral order). Always define an explicit ordered list of (filename, book_label, chapter_title) tuples at the top of the compiler script.

```python
# Explicit correct order, not alphabetical
CHAPTERS = [
    ('dedication.txt',         None,                None),
    ('00_intro.txt',           'INTRODUCTION',      None),
    ('01_chapter.txt',         'BOOK ONE — TITLE',  'I. CHAPTER TITLE'),
    ('02_chapter.txt',         None,                'II. NEXT CHAPTER'),
    # ...
]
```

Pattern:
- First entry in each book gets a `book_label` (triggers page break + H1 heading)
- Subsequent entries in the same book set `book_label=None` (just adds chapter as H2 with page break)
- Major sections (INTRODUCTION, CONCLUSION, CHRONOLOGY) use their name as `book_label`
- `chapter_title` is always set (or None for items like dedication/intro that use the label)

### 2. Handle Source File Heading Styles

Translation chapter files have **three inconsistent heading patterns**:

**Pattern A** (most common):
```
BOOK ONE — TITLE / I. SUBTITLE\n\nSUBTITLE\ntext...
```
→ Skip the first 3 lines (book heading, blank, redundant chapter title).

**Pattern B** (sub-section files):
```
BOOK FIVE — TITLE\n\nI. SECTION TITLE\ntext...
```
→ Skip the first 3 lines. The "I. SECTION TITLE" is redundant with chapter_title.

**Pattern C** (continuation files with no subtitle line):
```
BOOK TWO — TITLE / III. CHAPTER\ntext...
```
→ Skip only the first line (the book/chapter heading). Chapter title comes from the explicit definition.

Implementation: start reading at a calculated `start_idx` that skips:
1. Leading blank lines
2. First non-blank (always the heading line)
3. Following blank
4. Any known chapter title line (from a curated set like `{'ACTIVITY', 'CONFESSION', ...}`) — these duplicate info already in `chapter_title`)

### 3. Build the Compiler Script

Use `python-docx` (always available in Hermes venv). Key patterns:

```python
from docx import Document, shared
from docx.enum.text import WD_ALIGN_PARAGRAPH

def setup_styles(doc):
    s = doc.styles['Normal']
    s.font.name = 'Garamond'  # preferred for literary/classical works
    s.font.size = Pt(11)
    s.paragraph_format.line_spacing = 1.15
    for sec in doc.sections:
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin = Cm(2.5)
        sec.right_margin = Cm(2.5)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text.strip())
    r.bold = True
    r.font.size = Pt({1: 16, 2: 13}[level])
    if level == 1:
        r.font.small_caps = True  # book titles in small caps
```

### 4. Title Page & Dedication

Build manually with centered paragraphs and page breaks:
- 6 blank lines, NAPOLEON (28pt bold small caps), BY (12pt), author name (16pt small caps)
- Translation credits (10pt italic)
- Page break, then dedication centered vertically

### 5. Section Breaks

Use asterism (`⁂`) for internal section breaks — preserved as-is from source text. Display centered, 14pt.

## Common Pitfalls

- **Alphabetical sort trap**: `05_glauben_und_staat.txt` sorts before `05_gott.txt` — always use explicit ordering.
- **Duplicate headings**: Book heading + chapter title on same line in source file will produce the same text twice if both label and chapter_title are identical; set chapter_title=None in that case.
- **Known-chapter-title set**: Maintain a curated set of standalone title lines that appear in source files (e.g. `'ACTIVITY'`, `'CONFESSION'`, `'POETRY AND POLITICS'`) so the parser can skip them as redundant.
- **Body text alignment**: Use `WD_ALIGN_PARAGRAPH.JUSTIFY` for body text in literary works — ragged-left looks unprofessional.
- **Font choice**: Garamond is preferred for classical/literary works. If unavailable, fall back to Times New Roman or Georgia. Avoid sans-serif.

## Example: Vallentin Napoleon Translation

36 chapter files (.en.txt, 1.1M chars input) → single 410KB .docx (868 paragraphs, 42 headings). Full script in `build_docx_final.py` at the project work directory.
