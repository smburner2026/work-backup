# French Colonial Text Translation Workflow

## When to Use This

A French colonial-era book (1920s-1940s) about Vietnam has been downloaded from Gallica as page images (JPEGs from IIIF) or as a scanned PDF. You need to OCR it, clean it, and translate it to English.

## Phase 1: OCR — French (`fra`)

French OCR is **fast** on the VPS (~0.84s/page at 150dpi) because French has fewer diacritics than Vietnamese and uses standard Latin characters. No need for WSL for batches under 300 pages.

### Tesseract parameters

```bash
tesseract page.jpg stdout -l fra --psm 6
```

Only `fra` is needed — no mixed-language mode like Vietnamese. Tesseract's French model handles accents (é, è, ê, ô, œ, etc.) well.

### Resumable script pattern (generalized)

```bash
#!/usr/bin/env bash
PAGE_DIR="/path/to/page-images"
OUTPUT="/path/to/output-filename.txt"
TOTAL=279

for i in $(seq 1 $TOTAL); do
    PAGE_FILE=$(printf "p%04d.jpg" "$i")
    PAGE_PATH="$PAGE_DIR/$PAGE_FILE"
    if grep -q "^=== PAGE $i ===" "$OUTPUT" 2>/dev/null; then
        echo "  [$i/$TOTAL] — already done, skipping"; continue
    fi
    echo "=== PAGE $i ===" >> "$OUTPUT"
    tesseract "$PAGE_PATH" stdout -l fra --psm 6 2>/dev/null >> "$OUTPUT"
    echo "" >> "$OUTPUT"
done
```

### Compute selection

| Language | VPS speed | WSL speed | Recommendation |
|----------|-----------|-----------|----------------|
| French (fra) | ~1s/page | ~0.3s/page | VPS fine for ≤300 pages |
| Vietnamese (vie) | ~8s/page | ~2s/page | WSL preferred |
| Mixed (vie+fra) | ~10-12s/page | ~3s/page | WSL preferred |

## Phase 2: Cleaning — French-specific Patterns

French OCR errors differ from Vietnamese:

| Pattern | Fix | Examples |
|---------|-----|----------|
| Hyphenated line breaks | Join word halves | `pro-\nduction` → `production` |
| Running headers | Strip | `PAUL. CHACK` headers common |
| Old typography (long s) | Usually fine in 1930s | May appear as stray `f` |
| Ligatures | Normalize | `oe` → `œ` where appropriate |
| Stray pipes `\|` | Remove | From decorative page borders |
| Accent drops on caps | Usually fine | Tesseract handles E→É reasonably |
| Stray dots/colons | Remove line-leading punctuation | From typesetting artifacts |

### Python cleaning script template

```python
import re

with open('ocr-raw.txt') as f:
    text = f.read()

# 1. Join hyphenated line breaks
text = re.sub(r'(\w)-\n(\w)', lambda m: m.group(1) + m.group(2).lower(), text)

# 2. Strip running headers
text = re.sub(r'^AUTHOR\.?\s*SURNAME\s*\n', '', text, flags=re.MULTILINE)

# 3. Remove decorative artifacts (pipes, underscores)
text = re.sub(r'[\|_]', '', text)

# 4. Normalize spacing
text = re.sub(r'  +', ' ', text)
text = re.sub(r'\n{3,}', '\n\n', text)

# 5. Fix common French OCR substitutions
fixes = [
    (r'\btres\b', 'très'),
    (r'\ba\s+(?=[a-zéèê])', 'à '),  # "a Paris" → "à Paris"
]
for pattern, repl in fixes:
    text = re.sub(pattern, repl, text)
```

## Phase 3: Register Selection

For the post-colonial Vietnam project, two translation registers are established:

| Register | Source type | Voice | Model | When to use |
|----------|-------------|-------|-------|-------------|
| **Burckhardtian Scholarly** | Vietnamese historical texts (Phạm Văn Sơn, VSTB) | Cultured, measured, carries author's partisan energy. Think Burckhardt's *Civilization of the Renaissance in Italy*. | Primary model | Vietnamese scholarly histories |
| **Conrad-Kipling Adventure** | French colonial narratives (Paul Chack, colonial adventure) | Weighted, vivid, slightly formal early-20th-century adventure prose. Sensory landscapes, plain violence, colonial "our/we" perspective. Think Conrad stripped of the philosophy, or a French Kipling. | Primary model | French colonial adventure/history |

### Conrad-Kipling register — detailed rules

- **Slightly formal, literary sentence rhythms** — not stiff, not modern conversational
- **Sensory, bodily landscape descriptions** — "the forest had devoured the ancient roads", "tangled like the hair of the sick"
- **Violence lands plainly** — without hand-wringing or moral commentary
- **Colonial "our"/"we" perspective preserved** — this is a French colonial officer's account
- **Vietnamese proper names NEVER translated** — Đề Thám, Phủ Lạng Thương, etc.
- **French titles** — translate on first use with original in parentheses, then English (e.g. "the résident (résident)")
- **Dialogue** — natural spoken register, raw when characters speak
- **NO translator footnotes, NO commentary, NO interpretation**
- **Page markers removed** from output
- **Plain text**, not markdown
- **OCR garbles** — reconstruct from context where possible, note where impossible

## Phase 4: Kanban Batching Pattern

Books are too large for a single translation pass. Split into segments by part/chapter boundaries:

### Splitting

```bash
# From cleaned OCR, extract page ranges:
# Part 1: pages 7-79, Part 2: pages 80-113, etc.
python3 -c "
import re
with open('hoang-tham-cleaned.txt') as f:
    text = f.read()
sections = re.split(r'(=== PAGE \d+ ===)', text)
# ... extract by page range ...
"
```

### Kanban card creation

```bash
hermes kanban boards create <project-slug> --name "Project Name"
hermes kanban boards switch <project-slug>
hermes kanban create \
  --body "Translate Part One — pages X-Y, ~N words. Source: /path/to/source.txt Voice ref: /path/to/voice-ref.txt. Register: Conrad-Kipling. Output: /path/to/output.txt" \
  --priority 1 \
  "Translate: Part One — Description"
# Repeat for each segment
```

### Parallel dispatch via delegate_task

Use delegate_task with `tasks` array for parallel segments (max 3 concurrent):

```python
delegate_task(
    tasks=[
        {"goal": "Translate Part 1...", "context": "...", "toolsets": ["file", "terminal"]},
        {"goal": "Translate Part 2...", "context": "...", "toolsets": ["file", "terminal"]},
        {"goal": "Translate Part 3...", "context": "...", "toolsets": ["file", "terminal"]},
    ],
    toolsets=["file", "terminal"]
)
```

Each subagent:
1. Reads the source text (French)
2. Reads the voice reference file
3. Translates the entire segment in the prescribed register
4. Writes output to the specified path
5. Reports verbatim — verify file sizes after return

### Verification

```bash
# Check all outputs exist
ls -lh translations/part{1,2,3,4a,4b}-translated.txt
# Mark cards complete
hermes kanban complete <task_id>
```

### Consolidation

```bash
{
  echo "TITLE"
  echo "by Author (Year)"
  echo "Translated from the French"
  echo "=============================="
  echo ""
} > /path/to/full-translation.txt
for part in part1 part2 part3 part4a part4b; do
  cat "translations/${part}-translated.txt" >> full-translation.txt
  echo "" >> full-translation.txt
done
```

## Worked Example: Hoang-Tham, pirate (Paul Chack, 1933)

| Step | Detail |
|------|--------|
| Source | Gallica PDF (279 pages, French, image-based) |
| OCR | Sequential tesseract `-l fra`, 279 pages, ~4 min |
| Cleaning | Python script: hyphen joins, header strip, pipe removal |
| Register | Conrad-Kipling adventure narrative |
| Segments | 5 (Part 1-3 + Part 4a/4b) |
| Dispatch | 2 batches of parallel subagents (3+2) |
| Output | ~60K English words in ~7 min |
| Kanban board | `hoang-tham` |
| File location | `/root/work/post-colonial-vietnam/sources/chack/` |
