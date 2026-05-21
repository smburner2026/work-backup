# OCR Page Compilation Patterns (HathiTrust / University of Michigan dumps)

This reference captures the cleaning techniques that produced usable results from raw numbered `.txt` OCR files through multiple iterative passes.

## Step 1: Frequency-Analyze to Discover Headers

Before guessing what to remove, sample across the full file set and count short lines. Lines appearing 5+ times are almost certainly running headers or page artifacts.

```python
import os, re, collections

OCR_DIR = "/path/to/ocr/files"
files = sorted([f for f in os.listdir(OCR_DIR) if f.endswith('.txt')],
               key=lambda x: int(re.search(r'(\d+)', x).group(1)))

line_counts = collections.Counter()
for fname in files:
    path = os.path.join(OCR_DIR, fname)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    for line in raw.split('\n'):
        stripped = line.strip()
        # Focus on short lines that could be headers
        if 3 < len(stripped) < 70:
            line_counts[stripped] += 1

# Show lines appearing 5+ times — these are the blacklist candidates
for line, count in line_counts.most_common(80):
    if count >= 5:
        print(f'{count:4d} | {line[:120]}')
```

The output from a 328-page University of Michigan scan:
- `The Mantle of Caesar` — 145 occurrences (running title header)
- `The Historical Personality` — 97 occurrences (running chapter header)
- `The Mythical Figure` — 25 occurrences (running chapter header)
- `The Magic Name` — 23 occurrences (running chapter header)
- `Index` — 16 occurrences (index page header)

## Step 2: Also Check Uppercase Lines

Some artifacts only appear once or twice but are still junk (library stamps, copyright pages):

```python
for fname in files:
    path = os.path.join(OCR_DIR, fname)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    for line in raw.split('\n'):
        stripped = line.strip()
        if 5 < len(stripped) < 60 and stripped == stripped.upper():
            # Manually review these — they include library stamps, TOC fragments, etc.
```

## Step 3: The Production Cleaning Function

Built from the frequency analysis above. Uses exact-match blacklist + prefix-match for OCR merge artifacts.

```python
EXACT_REMOVE = {
    # Running headers (discovered via frequency analysis)
    "The Mantle of Caesar",
    "The Historical Personality",
    "The Mythical Figure",
    "The Magic Name",
    "Index",
    "INDEX",
    # Title page / frontmatter
    "THE MANTLE OF CAESAR",
    "MANTLE",
    "OF CAESAR",
    "FRIEDRICH GUNDOLF",
    "THE MYTHICAL FIGURE",
    "I. THE MYTHICAL FIGURE",
    "II. THE MAGIC NAME",
    "III. THE HISTORICAL PERSONALITY",
    "III. THE HISTORICAL",
    "PERSONALITY",
    "TABLE OF CONTENTS",
    "CHAPTER",
    "THE END",
    # Library stamp fragments
    "UNIVERSITY OF MICHIGAN",
    "THE UNIVERSITY OF MICHIGAN",
    "SCIENTIA", "LIBRARY", "VERITAS", "OF THE",
    "TUEBOR", "QUERIS PENINSULAM ANG NAM", "CIRCUMSPICE",
    "648992",
    # Printing info
    "GRANT RICHARDS AND HUMPHREY TOULMIN",
    "AT THE CAYME PRESS LIMITED",
    "LONDON, W. 1",
    "PRINTED IN U.S.A.",
    "4-25-30",
    "JAN 5.1995",
    "DATE DUE",
    # Page markers
    "PAGE",
    "B",
}

# Running headers that may have trailing OCR artifacts
RUNNING_HEADERS = [
    "The Mantle of Caesar",
    "The Historical Personality",
    "The Mythical Figure",
    "The Magic Name",
]


def is_noise_line(line):
    stripped = line.strip()

    # Exact blacklist match
    if stripped in EXACT_REMOVE:
        return True

    # Prefix match for running headers (catches OCR merge artifacts
    # like "The Magic NameT" where header fused with next line)
    for header in RUNNING_HEADERS:
        if stripped.startswith(header) and stripped != header:
            remainder = stripped[len(header):]
            if len(remainder) <= 3:
                return True

    # Empty or too short
    if len(stripped) < 3:
        return True

    # Lone page number (1-4 digit number on its own line)
    if re.match(r'^\s*\d{1,4}\s*$', stripped):
        return True

    # Shelf number (5+ digits)
    if re.match(r'^\s*\d{5,}\s*$', stripped):
        return True

    # Index-like line: mostly numbers and commas, short
    if len(stripped) < 80:
        digit_comma_space = sum(1 for c in stripped if c.isdigit() or c in ', ')
        if digit_comma_space / max(len(stripped), 1) > 0.4:
            return True

    # Dotted TOC leader lines (e.g. "Introduction .......... 9")
    if '....' in stripped:
        return True

    # Roman numeral chapter prefix on its own
    if re.match(r'^[IVX]+\.\s*$', stripped):
        return True

    return False


def clean_ocr_text(text):
    """Apply all cleaning passes — returns text with paragraph breaks preserved
    where detectable. Physical line endings are joined; inferred paragraph
    boundaries become \\n\\n for downstream rendering."""

    lines = text.split('\n')

    # Pass 1: remove noise lines
    lines = [l for l in lines if not is_noise_line(l)]

    if not lines:
        return ""

    # Pass 1.5: detect paragraph breaks before joining.
    # Heuristic: a line that is short (< 65% of average length in this file),
    # ends with a sentence-terminal punctuation mark, and is followed by a line
    # starting with an uppercase letter is likely a paragraph end.
    stripped_lines = [l.strip() for l in lines]
    lengths = [len(s) for s in stripped_lines if len(s) > 10]
    avg_len = sum(lengths) / max(len(lengths), 1) if lengths else 60
    threshold = avg_len * 0.65

    result_parts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        result_parts.append(stripped)

        # Decide what separator follows this line
        if i < len(lines) - 1:
            next_stripped = lines[i + 1].strip()
            if (len(stripped) < threshold
                    and stripped[-1] in '.!?:)'
                    and next_stripped
                    and next_stripped[0].isupper()):
                result_parts.append('\n\n')  # paragraph break
            else:
                result_parts.append(' ')     # within-paragraph space

    # Join everything
    text = ''.join(result_parts)

    # Pass 2: fix hyphenated word breaks (now spanning spaces)
    text = re.sub(r'-\s+', '', text)

    # Pass 3: normalize whitespace (preserve \n\n paragraph separators)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' *\n\n *', '\n\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
```

## Step 4: PDF Generation — Use `write()`, Not `multi_cell`

**Use `write()` for continuous OCR text — never `multi_cell`.**

`write(h, text)` flows text continuously from the current position, wrapping at the right margin. It avoids three compounding fpdf2 bugs that plague `multi_cell` on long strings (see Pitfalls below for full details):

1. **x-position drift** across `multi_cell` calls
2. **Long-string state corruption** (>50K chars in a single call)
3. **Chunk boundary artifacts** (mid-sentence breaks at chunk edges)

```python
# Join ALL cleaned text into ONE continuous flow.
# Do NOT split at file boundaries — OCR files represent physical pages,
# not paragraphs. Paragraphs in the book span across pages.
full_text = " ".join(all_cleaned_pages)
full_text = re.sub(r'[ \t]+', ' ', full_text).strip()

# Render as one continuous flow with write()
pdf.set_font("Liberation", size=11.5)
pdf.set_x(pdf.l_margin)
pdf.write(6.2, full_text)
```

**Never use `align='J'` (justified) for OCR text.** fpdf2's justification engine stretches inter-word spacing to fill the line width, but without a hyphenation engine, long paragraphs produce lines with too few words to stretch across the full width. The engine breaks early, creating the same mid-sentence hard breaks you just fixed. `write()` is always left-aligned, which is correct for OCR-sourced books.

## Step 5: Inspect Before Delivering

After generation, always extract and review pages before telling the user:

```python
import fitz
doc = fitz.open("output.pdf")
for i in [0,1,2,3,5,10,20,50,100,150,200,250,-1]:
    if i < len(doc):
        text = doc[i].get_text()
        print(f"=== PAGE {i+1} ===")
        print(text[:600])
```

Also run a residual noise scan:
```python
patterns = ["header1", "header2", "648992", "SCIENTIA", ...]
for i in range(len(doc)):
    text = doc[i].get_text()
    for pattern in patterns:
        if pattern.lower() in text.lower():
            # Skip intentional running header
            if pattern in text and text.strip().startswith("The Mantle of Caesar —"):
                continue
            print(f"Page {i+1}: RESIDUAL [{pattern}]")
```

If any residuals found, add them to the blacklist and regenerate. Budget for at least 2–3 iterations — the first pass almost always misses noise patterns that only become visible in the cleaned output.

## Pitfalls Learned

- **Hard line breaks are NOT paragraph breaks** — OCR from printed books preserves every physical line ending as `\n`. If you only collapse `\n{3,}` (blank lines) but leave single `\n` intact, your PDF will show mid-sentence line breaks exactly where the original book pages wrapped. The fix: replace ALL `\n` with spaces after noise-line removal (`re.sub(r'\n+', ' ', text)`), treating each page as continuous flowing text.

- **Paragraph boundary reconstruction** — the user prefers preserving the original book's paragraph structure where detectable. The heuristic: a line shorter than 65% of the average line length in its file, ending with `. ! ? : )`, followed by a line starting with an uppercase letter, is inferred to be a paragraph break and replaced with `\n\n`. This is approximate (some paragraph boundaries are invisible when the last line fills the full width, and some sentence endings within paragraphs happen to fall on shorter lines), but it recovers ~80% of the original structure. The `\n\n` separators survive into the final `full_text` and are respected by `write()` as paragraph breaks.

- **Do NOT split at file boundaries** — OCR files represent physical pages, not paragraphs. Joining files with `\n\n` and splitting into paragraph blocks creates artificial hard breaks at page transitions where the last line of a page ends mid-sentence. The fix: join ALL cleaned text with spaces into one continuous flow. `write()` handles all wrapping.

- **Do NOT use `align='J'` for OCR text** — fpdf2's justification engine stretches inter-word spacing to fill the line width, but without hyphenation, long paragraphs produce lines with too few words to stretch across the full width. The engine breaks early, creating mid-sentence hard breaks. Use `write()` (always left-aligned) for all OCR-sourced text. Justified alignment is only safe with structured markdown chapters that have author-provided line breaks.

- **OCR merge artifacts** — running headers sometimes fuse with the next text line (e.g. "The Magic NameT"). Exact-match blacklisting misses these. Prefix matching with a ≤3 char trailing tolerance catches them.

- **Variable running headers** — multi-chapter books have different running headers per chapter. The frequency analysis catches all of them because each appears on every page of its chapter.

- **Index pages** — the last ~30 pages of academic scans are dense index entries (short lines of "Name, description, page_numbers"). These survive cleaning as legitimate content, which is correct. Don't try to strip them — they're part of the book.

- **"PAGE" false positive risk** — the word "page" appears in legitimate text ("pageants", "pages of admiring comment"). Exact-match on the lone word "PAGE" is safe, but never regex-substring match it.

- **Don't deliver until inspected** — a PDF that looks clean in the raw OCR files will still carry noise artifacts. Always extract page samples and scan before telling the user the file is ready.

## Critical fpdf2 Pitfalls (multi_cell → write migration)

Three compounding fpdf2 bugs emerge when rendering 100K+ character continuous text via `multi_cell`. All three are avoided by using `write()` instead.

### 1. x-position drift across multi_cell calls

`multi_cell` does NOT reset x to the left margin between calls. After a call that fills the full width, x is left at `l_margin + usable_width` (the right edge). The next call starts from that x, not from the left margin. x accumulates: 25 → 185 → 345 → 505 → 665 → ... until text is placed past the page edge and becomes invisible.

**Symptom:** `fitz` extraction shows body text at x=527+ (past the 25mm right margin). Later pages have zero visible body text.

**Fix:** `write()` — single call, single state, no drift.

### 2. Long-string internal state corruption

A single `multi_cell` call with a 664K-character string corrupts fpdf2's internal layout state. Text drifts to x=527 after a few pages even with no chunking. The corruption appears to be in `multi_cell`'s page-break handling — when a page break occurs during the call, resumed text on the new page starts from a wrong x position.

**Symptom:** Same as #1 — text at x=527, later pages empty. Occurs even with a single `multi_cell` call.

**Fix:** `write()` handles the full string incrementally without state corruption.

### 3. Chunk boundary artifacts

When `multi_cell` is called with chunked text and `set_x` before each call, the transition between chunks creates an artificial mid-sentence break. Chunk N's last line might end with "...produced his" and chunk N+1 starts with "effect by means of..." — the sentence is broken across chunks.

**Symptom:** Very short lines (59–168 pts) in body text, always at ~8K character intervals.

**Fix:** `write()` — no chunking, no boundaries, one continuous flow.

### Verification After write()-Based Generation

```python
import fitz
doc = fitz.open(output_pdf)
# Body text must start at x ≈ l_margin (74 points for 25mm margins)
# No non-last-line should be under 200 points wide
for p in range(len(doc)):
    page = doc[p]
    blocks = page.get_text('dict')['blocks']
    for block in blocks:
        if 'lines' in block:
            for line in block['lines']:
                x0 = line['spans'][0]['bbox'][0]
                x1 = line['spans'][-1]['bbox'][2]
                w = x1 - x0
                if x0 < 100 and w < 200 and len(line['spans'][0]['text'].strip()) > 10:
                    print(f"Page {p+1}: SHORT w={w:.0f} — possible residual artifact")
```
