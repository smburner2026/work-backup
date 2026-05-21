# Text Extraction Quality Check

A systematic methodology for verifying that extracted text (OCR, EPUB-parsed, PDF-to-text) is clean, complete, and structurally sound before feeding it into downstream processing (PDF compilation, translation, analysis).

## When to Use

Run this QA after any text extraction where fidelity matters:
- You extracted text from a PDF (via pymupdf, marker-pdf, or web_extract)
- You converted an EPUB/DJVU/DOCX to plain text
- You received an already-extracted text file from an unknown pipeline
- Before compiling the text into a PDF or sending it through a translation pipeline

## 1. Quick Sanity Check

```python
with open("extracted.txt", "r") as f:
    content = f.read()
lines = content.split("\n")

print(f"Lines: {len(lines)}")
print(f"Chars: {len(content)}")
print(f"Words: {len(content.split())}")
```

Single-chapter works: 5K–40K words; book-length works: 60K–200K words. Values far outside this can indicate truncation or double-extraction.

## 2. Structural Completeness

Verify every expected section exists in the text. Search for each structural element:

| Element | Example Search Pattern |
|---------|----------------------|
| Opening line | `"When Zarathustra was thirty"` |
| Part / Chapter headers | `"PART ONE"`, `"Chapter I"`, `"INTRODUCTION"` |
| Known canonical quotes | `"God is dead"`, `"I teach you the Superman"` |
| Final paragraph fragments | Last 50 chars of the source |
| Back matter | `"NOTES"`, `"APPENDIX"`, `"INDEX"` |

Key pattern: the exact opening phrase should appear **exactly once** in the main text. Multiple occurrences usually mean the text appears in both TOC and body — strip the TOC.

## 3. OCR Artifact Scan

Run these checks. A clean file should have zero hits on most:

```python
import re

# These should almost always be 0:
print("Pipe chars:", content.count("|"))
print("Stray slashes:", sum(1 for l in lines if l.strip() in ("/", "\\")))
print("Bracketed nums [N]:", len(re.findall(r"\[\d+\]", content)))
print("Replacement chars:", content.count("\ufffd"))
print("Long no-space lines:", sum(1 for l in lines if len(l) > 50 and " " not in l.strip()))
print("HTML tags:", len(re.findall(r"<[^>]+>", content)))

# Garbled characters
import unicodedata
garbled = set()
for ch in content:
    if not ch.isascii() and ch not in "äöüßÄÖÜéèêëàâîïôùûçÉÈÆæŒœ–—'"''""„«»":
        try:
            name = unicodedata.name(ch, "")
            if name and "LATIN" not in name:
                garbled.add(ch)
        except:
            garbled.add(ch)
print("Suspicious non-ASCII:", sorted(garbled)[:20])
```

**Expected non-ASCII**: German umlauts (ä ö ü ß), French accents (é è ê), typographic punctuation (— – ' ' " " « »). Everything else warrants inspection.

## 4. Paragraph Integrity

Texts with frequent short lines (verse, dialog, Nietzsche's Zarathustra style) will have many "lines starting lowercase after blank" — this is normal. For prose texts, the count should be near zero:

```python
lower_after_blank = 0
for i, line in enumerate(lines):
    prev = lines[i-1].strip() if i > 0 else ""
    curr = line.strip()
    if prev == "" and len(curr) > 3 and curr[0].islower():
        lower_after_blank += 1
print("Run-on indicators:", lower_after_blank)
```

For prose, flag >5 suspected run-ons. For poetry/verse, check the first few to confirm they're intentional line continuations.

## 5. Hyphenation Artifacts (Fraktur / historical German)

German Fraktur and some justified PDFs produce fake hyphenation across line breaks:

```python
# Find compound words broken across line ends
hyphen_joins = re.findall(r"\w+-\n\w+", content)
print("Hyphen continuations:", len(hyphen_joins))
# Each is either a genuine compound or a line-break artifact — spot-check
```

Fix known patterns:
```python
fixes = {
    r"(\w)- (\w)": r"\1\2",  # dropped space after hyphen
    r"Ge sichte": "Geschichte",  # known Fraktur fragment
    r"Ent wicklung": "Entwicklung",
}
```

## 6. Double-Space / Whitespace Issues

```python
double_spaces = sum(1 for l in lines if "  " in l)
print("Lines with double spaces:", double_spaces)
```

Zero is ideal. Occasional double spaces (~10-50 in a book) are acceptable. Hundreds suggest a formatting problem in the source.

## 7. Contraction Spacing Issues

OCR that drops apostrophes creates "don t" / "can t" patterns:

```python
bad_contractions = re.findall(r"\b(?:do|ca|wo|is|was|has|have|does|did|had|would|could|should)n t\b", content, re.IGNORECASE)
print("Broken contractions:", len(bad_contractions))
```

Zero expected. If found, the source had apostrophe corruption and needs regex repair.

## 8. PDF Cross-Reference

When the source is a PDF (and pdftotext is available), compare the extracted text against the rendered PDF at key boundaries:

```bash
# Extract the PDF's text and find structural markers
pdftotext source.pdf - 2>/dev/null | grep -n "PART ONE\|ZARATHUSTRA'S PROLOGUE\|CHAPTER I\|INTRODUCTION" | head -20

# Spot-check the opening of the main text
pdftotext source.pdf - 2>/dev/null | sed -n '27751,27810p'
```

**Known pdftotext quirks**: Drop caps ("W HEN" instead of "WHEN"), page numbers and running headers in the output, ligature stretching ("fi" → "ﬁ"). These are rendering artifacts in the text extraction, not problems in your source file.

## 9. Front/Back Matter Boundary Check

Confirm that TOC entries don't leak into the body and that back matter doesn't get truncated:

```python
# Check for repeated structural elements (present in both TOC and body)
for element in ["PART ONE", "ZARATHUSTRA'S PROLOGUE", "INTRODUCTION"]:
    count = content.count(element)
    if count > 1:
        print(f"WARNING: '{element}' appears {count} times — TOC / body duplication?")
```

## 10. End-of-File Integrity

The file should end cleanly, not mid-sentence or with a garbled fragment:

```python
tail = content[-200:]
print("Last 200 chars:")
print(repr(tail))
```

Expected: closing sentence, final punctuation, optional blank lines. Unexpected: mid-word cutoff, orphan references ("Page 28" without context), stray copyright lines.

## PDF Rendering Check

After generating the output PDF, do a final visual spot-check by running pdftotext on the output and comparing the first and last few paragraphs against your source text. This catches regressions in the PDF build pipeline (WeasyPrint, fpdf2) that the input QA missed.

## Checklist Summary

```
[ ] File opens cleanly (no encoding errors)
[ ] Expected word count range
[ ] All structural sections present
[ ] Opening line appears exactly once
[ ] Zero pipe chars, stray slashes, bracketed nums
[ ] Zero replacement characters (U+FFFD)
[ ] Suspicious non-ASCII: none
[ ] Broken contractions: none
[ ] Back matter intact (Notes, Appendices)
[ ] File ends cleanly
[ ] PDF cross-reference matches
[ ] PDF output pdftotext matches source
```
