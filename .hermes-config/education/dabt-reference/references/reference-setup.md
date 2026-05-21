# Reference Library Setup

How the DABT reference library was built and how to maintain it.

## Source PDFs

```
reference/
├── textbooks/
│   ├── casarett-doull-9e.pdf       (54 MB, 1639 pages)
│   └── hayes-7e.pdf                (121 MB, 2143 pages)
├── regulations/
│   ├── epa/                        (2 PDFs: cancer guidelines, Silverbook)
│   ├── fda/                        (3 PDFs: Redbook, drug metabolites, least burdensome)
│   ├── ich/M/                       (2 PDFs: M7(R2), M3(R2))
│   ├── ich/S/                       (9 PDFs: S1-S9 safety guidelines)
│   └── oecd/                       (13 PDFs: TG407-TG497)
├── exam-materials/
│   ├── ABT-Candidate-Handbook-2026.pdf
│   └── practice-exams/
│       ├── abt-2013-recert/
│       ├── abt-2015-recert/
│       ├── abt-2017-cert/
│       ├── abt-2008-2014-compiled/
│       ├── tox-2000-notecards/
│       └── mini-abt-01/ through mini-abt-11/
├── data/
│   ├── question_classifications.csv
│   └── question_classifications.json
└── extracted/                      ← searchable text output (25 MB)
```

## Extraction Pipeline

All scripts live at `/root/work/dabt/dabt-tutor/scripts/`:

### 1. `inspect_pdfs.py`
Inspects PDF structure: page count, TOC depth, sample text. Run before extraction to understand what you're dealing with.

### 2. `extract_textbooks.py`
Extracts Casarett and Hayes into chapter-level .txt files using PyMuPDF TOC.
- C&D: TOC level 2 = chapters (35 chapters, 77 TOC entries total)
- Hayes: TOC level 3 = chapters (39 chapters, 2415 TOC entries total)
- Filter: front matter + index entries skipped via regex patterns
- Output: one .txt per chapter + index.json

### 3. `extract_regulations.py`
Extracts all regulation PDFs into individual .txt files.
- Simple: one PDF → one .txt, no TOC splitting
- Output: .txt files + index.json grouped by category (epa, fda, ich, oecd)

## Extraction Quirks

### Skip Filter Bug (fixed)
Original script used substring matching for front-matter filtering. Words like "history" matched inside "historical", "foreword" inside legitimate text. Fixed by switching to regex word-boundary matching (`^cover$`, `^preface`, etc.).

### MuPDF Warnings
ICH S3A and S3B guidelines produce "No default Layer config" warnings during extraction. Text extracts fine — these are non-fatal.

### Hayes TOC Depth
Hayes 7e has 2415 TOC entries (5 levels deep). Chapter level is 3. Section titles at level 2 are filtered out via `^section I:` pattern.

### Page Numbering
PDF page numbers are 1-indexed PDF-internal numbers. Casarett's printed page numbers roughly match (offset of ~1 in early chapters due to roman-numeral front matter). Hayes uses a different numbering scheme — the chapter headers in extracted .txt files use PDF page numbers.

## Adding New References

1. Place PDF in `reference/textbooks/` or `reference/regulations/<category>/`
2. For textbooks with TOC: add to `extract_textbooks.py` with appropriate chapter_level
3. For regulations: they'll be picked up automatically by `extract_regulations.py`
4. Re-run extraction — existing files are overwritten, not duplicated

## Re-extraction

If PDFs are updated or extraction failed:
```bash
cd /root/work/dabt/dabt-tutor
python3 scripts/extract_textbooks.py
python3 scripts/extract_regulations.py
```
Total runtime: ~60-90 seconds for all sources.
