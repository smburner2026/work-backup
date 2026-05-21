# Cleaning OCR artifacts from Fraktur / historical German books (Google Books)

German Fraktur typeface creates consistent OCR artefacts when extracted via PyMuPDF or similar tools. The tightly-set Fraktur letterforms cause the OCR engine to drop inter-word spaces, producing run-together text that requires systematic cleanup.

## Common artefacts

| Type | Example (raw) | Desired | Detection |
|------|--------------|---------|-----------|
| Lowercase→uppercase merge | `dieGeschichteNapoleons` | `die Geschichte Napoleons` | `[a-zß][A-ZÄÖÜ]` — very reliable, ~3000 occurrences in a 550pp book |
| Uppercase→lowercase merge | `NOCHimmer` | `Noch immer` | `[A-ZÄÖÜ]{2,}[a-z]` — rarer, usually heading artefacts |
| Lowercase→lowercase merge | `Forschunghatum` | `Forschung hat um` | No simple regex; needs dictionary or language model |
| Hyphenated line-breaks | `neu-\nzeitlichen` | `neuzeitlichen` | `\w-\n\w` — rejoin, NOT split (German compounds are real) |
| Punctuation spacing | ` ,` / ` .` | `,` / `.` | `\s[.,;:]` → `[.,;:]` |
| Period-no-space | `Napoleons.Die` | `Napoleons. Die` | `\.(?=[A-ZÄÖÜ])` |
| Library stamps | Library shelfmarks, barcodes, ownership marks on early pages | Remove | Check first ~6 pages for `UNIVERSITYOF`, `BUHR`, `DC\s+\d+\s+V\d+`, `a\d+` |

## Cleanup strategy (iterative multi-pass)

Fraktur OCR cleaning is best done in **multiple passes**, each targeting a specific class of artifact. Attempting everything at once produces conflicts (e.g. prematurely inserting spaces that break later hyphenation repair).

### Pass 1: Strip front matter
Google Books PDFs always have 2 pages of license/terms text, then a title page, copyright page, and often a library-stamp page. Strip pages 1–6 entirely before extraction.

Look for these patterns in early pages:
- `UNIVERSITYOFMICHIGAN`, `BUHR`, `DC\s+\d+\s+V\d+`, `a\d+` — library stamps
- `This is a reproduction of a library book` — Google license
- `ERSTES BIS VIERTES TAUSEND` — edition notice
- `HODIERNO HEROI` — George-Kreis dedication (preserve as metadata!)

Remove the **entire** table-of-contents page(s) before starting content extraction, because the TOC duplicates all chapter headings and will confuse heading-detection logic. The cleanest way: locate SCHLUSSWORT in the TOC (its last entry), and drop everything before the content after it.

### Pass 2: Rejoin hyphenated compounds
German typesetting breaks words at syllable boundaries. The pattern is:
```
re.sub(r'(\w)-\n\s*', r'\1', text)
```
This catches genuine hyphenation while leaving intended hyphens (e.g. `menschlich-sozialen`) intact — those would have no `\n` after the hyphen.

**Important**: some Google Books OCR runs also break words WITHOUT hyphens (the word simply continues on the next line with a space inserted). These produce artifacts like `Ge schichte`, `We sens`, `Na poleon` — see Pass 5 for fixing these.

### Pass 3: Fix missing spaces (types 1, 2, 4)
Three regex patterns handle the bulk of cases:

```python
# Lowercase → uppercase (most productive)
re.sub(r'([a-zß])([A-ZÄÖÜ])', r'\1 \2', text)

# Period → sentence start 
re.sub(r'\.(?=[A-ZÄÖÜ])', r'. ', text)

# Punctuation spacing (Fraktur OCR adds space before commas)
re.sub(r' ,', ',', text)
```

Also fix space before semicolon, colon, and double-space:
```python
re.sub(r' ;', ';', text)
re.sub(r' :', ':', text)
re.sub(r'  +', ' ', text)
```

### Pass 4: Merge broken lines into paragraphs

Page-level OCR produces one logical line per physical line, with no paragraph awareness. Merge lines to reconstruct paragraphs:

```python
lines = text.split('\n')
merged = []
for line in lines:
    stripped = line.strip()
    if not stripped:
        merged.append('')
    elif merged and merged[-1]:
        merged[-1] = merged[-1] + ' ' + stripped
    else:
        merged.append(stripped)
text = '\n'.join(merged)
```

This step is essential before Pass 5, because word-fragment detection checks for spaces within suspect words.

### Pass 5: Fix word-fragment artifacts (lowercase→lowercase merges)

After merging into paragraphs, spaces appear between split word fragments (from unhyphenated line breaks). These are the hardest case because both sides are lowercase — no regex pattern distinguishes them.

Build a lookup table from known-fragment pairs found in the document:

```python
WORD_FRAGMENTS = {
    'Ge schichte': 'Geschichte',
    'We sens': 'Wesens', 
    'Na poleon': 'Napoleon',
    'Be deutung': 'Bedeutung',
    'Er scheinung': 'Erscheinung',
    'Dar stellung': 'Darstellung',
    'Vor stellung': 'Vorstellung',
    'Ent wicklung': 'Entwicklung',
    'Ver hältnis': 'Verhältnis',
    'Auf fassung': 'Auffassung',
    'Zu sammenhang': 'Zusammenhang',
    # ... 50-100+ more pairs, compiled from the document
}
for wrong, right in WORD_FRAGMENTS.items():
    text = text.replace(wrong, right)
```

**Pipeline order matters**: apply these fragments AFTER paragraph-merging (Pass 4), because `\n` between fragments prevents `str.replace` from matching.

### Pass 6: Structural chapter separation

For George-Kreis / early 20th C German academic books, the heading pattern is typically:
- `ERSTES BUCH`, `ZWEITES BUCH` … `SECHSTES BUCH` as `#` headings
- Section titles in full uppercase (40–60 chars) as `##` or `###`
- `EINLEITUNG`, `SCHLUSSWORT`, `ZEITTAFEL` as major divisions

**Warning**: heading detection by regex is fragile when a Table of Contents page precedes the content (it duplicates all headings). Two strategies:

**Strategy A — Regex heading detection** (use when no TOC pollution):
   Scan all lines for heading patterns. Works when the TOC was already stripped in Pass 1.

**Strategy B — File-number ranges** (use with UCAL page-level OCR):
   Map chapter boundaries by file-number ranges derived from the book's printed page numbers. More reliable when heading detection fails. Example:
   ```python
   CHAPTERS = [
       (13, 20, 'Einleitung', None),
       (21, 26, 'Erstes Buch', 'Aktivität'),
       (27, 29, 'Erstes Buch', 'Intensität'),
       # ... one entry per chapter, (start_file, end_file, book, chapter)
   ]
   ```
   UCAL files use the naming pattern `UCAL_B4569992_XXXXXXXX.txt` where the number maps to the printed page number. Read them in numeric order, concatenate within each range, clean, and output per-chapter.

### Pass 7: Post-cleanup quality check

```python
# Count remaining type-1 artefacts (should be near-zero)
remaining = len(re.findall(r'[a-zß][A-ZÄÖÜ]', cleaned_text))

# Check for suspiciously long words (>25 chars without known compound)
long_words = [w for w in cleaned_text.split() if len(w) > 25]
```

A "clean enough" pass for a Fraktur German book typically leaves <20 type-1 artefacts and <100 type-3 cases in 550 pages.

## Tools and dependencies

- **PyMuPDF** (`import fitz`): fast, no models, works on text-based PDFs
- **PyMuPDF4LLM**: markdown output helper (lightweight wrapper)
- **pyspellchecker**: optional, for dictionary-based type-3 splitting
- **German fraktur reference**: the [MATEO](https://mateo.uni-mannheim.de/) and [Deutsches Textarchiv](https://www.deutschestextarchiv.de/) projects have example-clean workflows

## Practical notes

- Always work on the full extracted text, not page-by-page — many artefacts only become visible when words straddle a page boundary.
- Google Books PDFs from the 2008–2012 digitisation wave are all text-based (not scans), so PyMuPDF extraction works; marker-pdf is not needed and would add ~3GB of models for no benefit.
- The `HODIERNO HEROI` dedication page in George-Kreis books is a dead giveaway for the Circle — preserve it as metadata.
- Salzwasser-Verlag / Archive.Org reprints often duplicate the Bondi originals and can be used as a second source to check garbled passages.
