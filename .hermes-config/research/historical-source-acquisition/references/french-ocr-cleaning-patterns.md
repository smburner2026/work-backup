# French OCR Cleaning Patterns (Colonial-era Books)

## Overview

French colonial-era books (1900–1945) scanned from Gallica IIIF images and OCR'd with Tesseract (`-l fra`) produce systematic errors. This reference covers the cleaning pipeline developed for Paul Chack's "Hoang-Tham, pirate" (1933, 279 pp) and generalizes to other French texts of the period.

## Phase 1: Hyphenated Line Break Joining

French typography hyphenates multi-syllable words at line breaks more aggressively than English. Tesseract preserves the hyphens.

**Regex pattern:**
```
re.sub(r'(\w)-\n(\w)', lambda m: m.group(1) + m.group(2), text)
```

**Examples:**
| OCR output | Correct |
|------------|---------|
| `pro-\nduction` | `production` |
| `gouver-\nnement` | `gouvernement` |
| `révolu-\ntion` | `révolution` |
| `particu-\nlièrement` | `particulièrement` |

**Edge cases:** Don't join across blank lines (paragraph boundary). Only join when the broken segment is on immediately consecutive lines.

## Phase 2: Running Header Removal

Colonial-era books typically repeat the author's surname at the top of each page (recto pages). For Paul Chack's books, every page starts with "PAUL. CHACK" or "PAUL CHACK".

**Regex pattern:**
```
text = re.sub(r'^PAUL\.?\s*CHACK\s*\n', '', text, flags=re.MULTILINE)
```

**Variant headers to check per book:**
- Author full name: `Paul Chack`, `PAUL CHACK`
- Author surname only: `CHACK`
- Chapter title repeats
- Page numbers inline with header

Before stripping, scan the first 50 pages to identify the recurring header pattern.

## Phase 3: Accent Restoration

Tesseract drops acute/grave accents on page edges and in poorly-scanned regions.

**Common substitutions:**
| OCR | Correct | Context |
|-----|---------|---------|
| `a` (before verb/place) | `à` | `a Paris` → `à Paris`, `a la` → `à la` |
| `e` | `é/è/ê` | `tres` → `très`, `etait` → `était`, `general` → `général` |
| `o` | `ô` | `cote` → `côte`, `hopital` → `hôpital` |
| `u` | `û` | `sur` (context: "sûr" = certain) |

**Approach:** Context-dependent regex replacements for high-confidence cases. Don't blindly replace — many `a`/`e`/`o`/`u` are correct as-is.

## Phase 4: Ligature Handling

Old French typography uses `œ` and `æ` ligatures. Tesseract sometimes splits them.

| OCR | Correct | Example |
|-----|---------|---------|
| `oe` | `œ` | `coeur` → `cœur`, `soeur` → `sœur`, `oeuvre` → `œuvre` |
| `ae` | `æ` | Rare in colonial-era books, `taenia` → `tænia` |

Apply only to known words (list of ~20 common French œ/æ words).

## Phase 5: Paragraph Reconstruction

Tesseract breaks lines at image width, not at paragraph boundaries. Rejoin lines that are clearly same-paragraph:

**Heuristic:** If line N ends with `[a-z0-9,)';:]` AND line N+1 starts with `[a-z]` (lowercase), they're same paragraph. Join with space.

**When NOT to join:**
- Line N ends with `.` followed by uppercase (sentence boundary)
- Line N+1 is a page marker (`=== PAGE N ===`)
- Line N+1 is a running header
- Line N+1 is a chapter/section heading (all caps or numbered)

## Phase 6: Stray Symbol Removal

Image borders and fold shadows produce stray characters:

| Symbol | Source | Action |
|--------|--------|--------|
| `<`, `>` | Shadow artifacts | Remove if at line start/end, not in math context |
| `[`, `]`, `{`, `}` | Border noise | Remove if isolated, not in citation context |
| `*`, `@`, `#`, `$`, `%`, `^` | Optical noise | Remove if not in footnote context |
| Stray `·` (middle dot) | Page edge | Remove |

Use regex with context awareness: `re.sub(r'^[<>\[\]{}*@#\$%\^·]+', '', line)` for line starts, same for ends.

## Phase 7: Number Normalization

Old French page numbers and dates can be mangled:

| OCR | Correct | Pattern |
|-----|---------|---------|
| `1781884` | `17-8-1884` | Date digits concatenated |
| `l` as `1` | varies | French Roman numerals: `V` vs `l` confusion |
| `O` as `0` | varies | Letters in numbers |

---

## Complete Cleaning Script Pattern

```python
#!/usr/bin/env python3
"""Clean French OCR output for colonial-era books."""
import re

def clean_french_ocr(text: str) -> str:
    # 1. Join hyphenated line breaks
    text = re.sub(r'(\w)-\n(\w)', lambda m: m.group(1) + m.group(2).lower() if m.group(2).islower() else m.group(1) + m.group(2), text)
    
    # 2. Strip known running headers (customize per book)
    text = re.sub(r'^PAUL\.?\s*CHACK\s*\n', '', text, flags=re.MULTILINE)
    
    # 3. Paragraph reconstruction
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('=== PAGE') or line.strip() == '':
            out.append(line)
            i += 1
            continue
        merged = line
        while i + 1 < len(lines):
            nxt = lines[i + 1]
            if nxt.startswith('=== PAGE') or nxt.strip() == '':
                break
            if merged and merged[-1].isalpha() and nxt and nxt[0].islower():
                merged += ' ' + nxt
                i += 1
            else:
                break
        out.append(merged)
        i += 1
    text = '\n'.join(out)
    
    # 4. High-confidence accent fixes
    text = re.sub(r'\btres\b', 'très', text)
    text = re.sub(r'\bvoila\b', 'voilà', text)
    text = re.sub(r'\bapres\b', 'après', text)
    text = re.sub(r'\bpres\b', 'près', text)
    
    # 5. Ligatures
    replacements = {
        'coeur': 'cœur', 'soeur': 'sœur', 'choeur': 'chœur',
        'oeuvre': 'œuvre', 'oeil': 'œil', 'foetus': 'fœtus',
        'noeud': 'nœud', 'voeu': 'vœu', 'oeuf': 'œuf',
        'moeurs': 'mœurs', 'boeuf': 'bœuf', 'poeme': 'poème',
    }
    for wrong, correct in replacements.items():
        # word-boundary-aware
        text = re.sub(r'\b' + wrong + r'\b', correct, text)
    
    # 6. Stray symbol cleanup
    text = re.sub(r'^[<>\[\]{}*@#\$%\^·]+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[<>\[\]{}*@#\$%\^·]+$', '', text, flags=re.MULTILINE)
    
    # 7. Normalize whitespace
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text
```

## Source-Specific Quirks

For each book, scan the first 20 raw OCR pages to identify:

1. **Running header pattern** — often varies between recto/verso
2. **Chapter heading format** — all-caps, mixed case, numbered?
3. **Footnote style** — inline `[1]` or bottom-of-page? Preserve markers.
4. **Foreign phrases** — Latin, English, Vietnamese inline quotations
5. **Italics handling** — Tesseract usually gets italic text right, but sometimes italic `a` reads as `o`

Document these in a per-book companion note (e.g. `chack-hoang-tham-cleaning-notes.md`).
