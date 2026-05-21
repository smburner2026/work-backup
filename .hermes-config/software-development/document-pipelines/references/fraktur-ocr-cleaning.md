# Fraktur OCR Cleaning Reference

Common artifacts when extracting text from German Fraktur-type books (pre-1945),
especially Google Books PDFs and UCAL page-level OCR.

## Missing spaces between words

Fraktur's tight letter spacing causes OCR to drop inter-word spaces. Three types:

| Type | Example | Fix | Method |
|------|---------|-----|--------|
| lowercase→UPPERCASE | `dieGeschichte` → `die Geschichte` | Insert space | `re.sub(r'([a-zß])([A-ZÄÖÜ])', r'\1 \2', text)` |
| UPPERCASE→lowercase (within "word") | `NOCHimmer` → `NOCH immer` | Insert space at case transition | More complex; check for all-caps prefix |
| lowercase→lowercase | `Forschunghatum` → `Forschung hat um` | Hard — needs dictionary | Build a word-splitting fix list of common compounds |

The lowercase→UPPERCASE pattern catches ~80% of cases. The remaining 20% need
manual fixes by maintaining a `WORD_FIXES` dictionary.

## Word fragments from line breaks

German Fraktur often breaks compounds at line ends. The hyphen may or may not
be present in the OCR output.

**With hyphen** (caught by pattern):
`re.sub(r'(\w)-\n(\w)', r'\1\2', text)`

**Without hyphen** (produces spaces mid-word):
Common fragments seen in Vallentin, *Napoleon*:

| Fragment | Fix |
|----------|-----|
| `Ge sichte` | `Geschichte` |
| `Ge sichtspunkte` | `Gesichtspunkte` |
| `We sens` | `Wesens` |
| `Na poleon` | `Napoleon` |
| `Na poleons` | `Napoleons` |
| `Be deutung` | `Bedeutung` |
| `Be ziehungen` | `Beziehungen` |
| `Er kenntnis` | `Erkenntnis` |
| `Er scheinung` | `Erscheinung` |
| `An schauung` | `Anschauung` |
| `Aus druck` | `Ausdruck` |
| `Dar stellung` | `Darstellung` |
| `Ent wicklung` | `Entwicklung` |
| `Ge gebenheit` | `Gegebenheit` |
| `Ge genstand` | `Gegenstand` |
| `Ge genwart` | `Gegenwart` |
| `Ge halt` | `Gehalt` |
| `Vor stellung` | `Vorstellung` |
| `Vor aussetzung` | `Voraussetzung` |
| `Zu sammenhang` | `Zusammenhang` |
| `Jahrhun derte` | `Jahrhunderte` |
| `Andeu tung` | `Andeutung` |
| `Über einstimmung` | `Übereinstimmung` |
| `Ent scheidung` | `Entscheidung` |
| `Ver gangenheit` | `Vergangenheit` |

Most follow the pattern of a German prefix (Ge-, Be-, Er-, Ver-, Vor-, Zu-, Ent-,
Aus-, Dar-) separated by a space from the root. Build a fix list iteratively:
run → find artifacts → add to list → re-run.

## Punctuation spacing

Fraktur OCR consistently adds spaces before punctuation:

```python
re.sub(r' ,', ',', text)
re.sub(r' ;', ';', text)
re.sub(r' :', ':', text)
```

## Greek character rendering

Fraktur OCR garbles Greek letters into Latin approximations:

| Garbled | Correct |
|---------|---------|
| `Agɣetvνoς` or `Agɣetvños` | `ἀρχέτυπος` |
| Various `φ`, `θ`, `χ` substitutions | Check original PDF |

Fix with direct string replacement after the regex passes.

## Running headers and page numbers

German books from this period have running headers (author + short title) on
every page. Also isolated page numbers (Arabic and Roman numerals):

```python
re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)       # Arabic page numbers
re.sub(r'^[IVXLCDM]+\s*$', '', text, flags=re.MULTILINE) # Roman numerals
re.sub(r'^Vallentin, Napoleon\s*\n', '', text, flags=re.MULTILINE)  # Running header
```

## Workflow for cleaning a full book

1. **Scan**: Count lowercase→UPPERCASE transitions per page to gauge severity.
2. **Fix mechanics**: Hyphenation, punctuation, running headers first.
3. **Fix missing spaces**: Regex for lowercase→UPPERCASE, then iterative fix-list.
4. **Split into chapters**: Use known page ranges (from TOC or visual inspection).
5. **Post-clean each chapter**: Run the same pipeline on each chapter file.
6. **Verify**: Spot-check the first paragraph of each chapter for remaining artifacts.
