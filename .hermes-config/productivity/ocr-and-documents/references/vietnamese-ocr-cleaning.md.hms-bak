# Vietnamese OCR Post-Processing Patterns

For scanned Vietnamese / French historical texts processed with `tesseract -l vie+fra+eng`.

## Common Artefacts

### 1. Missing/Corrupted Diacritics
Vietnamese uses 5 tone marks (sắc `´`, huyền `` ` ``, hỏi `?`, ngã `~`, nặng `.`) and 3 letter modifiers (ă, â, ê, ô, ơ, ư, đ). Tesseract may drop or misplace these, especially on old print with faded ink.

**Pattern:** `nguoi` → should be `người` (missing ơ + ˋ)
**Fix:** Context-aware — treat as a suggestion, not automatic replacement.
**Best approach:** Keep the raw OCR output. Apply diacritic restoration only when the corrected word is unambiguous from context.

### 2. Hyphenated Line Breaks
Scanned books have hyphenated words at line breaks. Tesseract preserves the hyphen but doesn't rejoin the word.

**Pattern:** `lịch-` + next line `sử` → `lịch-sử` (should be `lịch sử`)
**Fix:** Remove hyphens that occur at line ends and join the fragments. Use a dictionary (Hunspell vi_VN) for verification.

### 3. French Loanword Corruption
Vietnamese text often contains French terms (place names, ranks, institutions). The `vie` tesseract model may garble these because it expects Vietnamese phonetics.

**Pattern:** `Cochinchine` → `Cochinchine` (OK) or corrupted to `Coc hinc hine`
**Pattern:** `commissaire` → garbled
**Fix:** Keep a glossary of known French terms from the period. Flag ambiguous matches for manual review.

### 4. Mixed Script Issues
Historic texts may use Vietnamese romanization (quốc ngữ) alongside Chinese characters (for proper names in pre-20th century texts) and French. Tesseract with `vie+fra` handles these unevenly.

### 5. Period-Specific Spelling
Pre-1975 Vietnamese uses different conventions. E.g.:
- `Phạm Văn Sơn` (modern) vs older variants
- `Việt Nam` vs `Viêt-Nam` (French-influenced hyphenation)
- `Hà Nội` vs `Hanoi`

**Preserve original spelling** — do not modernize. Modernization is a separate translation step.

## Recommended Workflow

1. **Raw OCR** — `tesseract -l vie+fra+eng --psm 1` on each page
2. **Keep raw** — store the raw OCR output as-is in `extracted/page_NNN.txt`
3. **Post-process** — apply fixes in a separate cleaned version
4. **Separate files** — always have `raw/` and `clean/` directories

## Quick Quality Check

After OCR, run on first 3-5 pages:
```
# Count lines with Vietnamese diacritics (good sign)
grep -c '[ăâêôơưđ]' page_001.txt
# Count likely garbled sequences (bad sign)
grep -c '[A-Z]\{5,\}' page_001.txt
# Check if French terms survived
grep -i 'cochinchine\|commissaire\|protectorat\|indochine' page_001.txt
```

If garbled sequences dominate, try: lower resolution (200dpi instead of 300), different PSM mode (--psm 6 for uniform block, --psm 3 for default), or use the `eng` model only as a fallback.
