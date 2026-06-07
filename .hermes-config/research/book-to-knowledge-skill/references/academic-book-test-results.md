# Book-to-Skill Test Results — Academic Books

Tested with: **Aion: Researches into the Phenomenology of the Self** by C.G. Jung (Collected Works Vol. 9ii, 374 pages, 132K words)

## Extraction Results
- **Method**: pdftotext (poppler-utils) — clean, fast
- **Output**: 132,757 words, ~177K tokens
- **Quality**: Good — text extraction itself works well for this format

## Generation Results (v2 — after Roman numeral fix)

### Chapter Detection — FIXED (v2)
- **Expected**: 15 chapters (I–XV)
- **Actual**: 15 detected + 1 false positive (appendix entry)
- **Strategy used**: ToC-based detection — parsed Roman numeral entries from lines 205–229, found first occurrence of each title in body text
- **False positive**: `II. of Psychology and Alchemy` — a List of Plates entry that shares the `II.` prefix with Chapter II (The Shadow). The ToC parser picks up both.
- **Remaining gap**: Chapter IX ("The Ambivalence of the Fish Symbol") has a malformed page number (`1 1` with space) — title cleanup regex `r"\s+\d[\d\s]*$"` strips it correctly

### Chapter Filenames — FIXED (v2)
- **Before**: `ch01-the-medusa-126-2-the-fish-137-3-the-fish.md` (garbage from false positives)
- **After**: `chI-the-ego.md`, `chII-the-shadow.md`, `chIX-the-ambivalence-of-the-fish-symbol.md`
- Roman numerals used as-is, no leading zeros

### Glossary — STILL GARBAGE
- Regex pulls random fragments containing em-dashes or bold text
- Examples of bad entries: "Deluge!", publication dates, partial sentences
- **Root cause**: Academic text doesn't follow `Term — definition` format consistently
- **Fix needed**: LLM-based glossary extraction, or manual curation

### Patterns — STILL EMPTY
- Only detects `### How to apply:` sections
- Academic books don't use this format
- **Fix needed**: Detect named methods, step-by-step procedures, analytical frameworks

### Core Frameworks — STILL PLACEHOLDER
- Generator doesn't populate this section
- Must be written manually after reading the text
- This is the most important section — the 1500-2500 token core

## Fixes Applied to hermes_skill_gen.py (2026-06-02)

### detect_chapters() — 3 strategies
1. **Standard patterns**: `Chapter N`, `Part X` (removed the false-positive-prone `N. Title`)
2. **ToC-based**: Parse `I. Title`, `II. Title` Roman numeral entries, find first body occurrence
3. **Centered uppercase headings**: After form feeds (academic book format)

### chapter_num_format() — new helper
- Roman numerals: as-is (`chI-`, `chII-`)
- Arabic numbers: zero-padded (`ch01-`, `ch02-`)

### Title cleanup
- `re.sub(r"\s+\d[\d\s]*$", "", title)` strips trailing page numbers with spaces

### Old file cleanup
- Before generating, all `ch*.md` files in chapters/ are deleted to prevent stale artifacts

## Chapter Structure (Aion)
Lines 205–229 of extracted text contain the ToC:
- I. The Ego (p.3)
- II. The Shadow (p.8)
- III. The Syzygy: Anima and Animus (p.15)
- IV. The Self (p.23)
- V. Christ, a Symbol of the Self (p.36)
- VI. The Sign of the Fishes (p.72)
- VII. The Prophecies of Nostradamus (p.95)
- VIII. The Historical Significance of the Fish (p.103)
- IX. The Ambivalence of the Fish Symbol (p.111)
- X. The Fish in Alchemy (p.126)
- XI. The Alchemical Interpretation of the Fish (p.154)
- XII. Background to the Psychology of Christian Alchemical Symbolism (p.173)
- XIII. Gnostic Symbols of the Self (p.184)
- XIV. The Structure and Dynamics of the Self (p.222)
- XV. Conclusion (p.266)
