# Scanned PDF OCR Pipeline (Vietnamese + French)

## When to Use

Any scanned Vietnamese-language PDF (no selectable text, typically pre-1975 publications, colonial-era documents, or Vietnamese academic works). Uses Tesseract with `vie+fra` for bilingual OCR.

## Prerequisites

```bash
# One-time setup
apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-vie tesseract-ocr-fra
```

Available languages: `eng`, `vie`, `fra`, `osd`

## Pipeline Steps

### ⚠️ CRITICAL CONSTRAINT — Disk Space

This VPS has **38 GB total disk**. One volume at 300 DPI bulk conversion eats ~12 GB of temp space running 5 in parallel will crash the system. **Always OCR one volume at a time.**

Two scripts now exist for this:

| Script | Approach | DPI | Batch size | Best for |
|--------|----------|-----|-----------|----------|
| `ocr_volume.sh` | Batched PNG | 150 | 10 pages | Fast, balanced quality/speed |
| `ocr_volume_v2.sh` | Page-by-page PPM | 200 | 1 page | Reliable, easy to resume |

Both have: resume-aware (don't nuke partial progress), trap EXIT (temp cleanup on failure), and pdftoppm error skipping.

### Step 1: Check PDF

```bash
pdfinfo input.pdf
# Check: Pages, File size, PDF version
```

If PDF has selectable text (native digital), skip OCR. Use `pdftotext` directly:
```bash
pdftotext input.pdf output.txt
```

### Step 2: OCR One Volume (Sequential)

Use the dedicated scripts — they handle cleanup, resume, and the trap pattern automatically:

```bash
# Fast batch (10 pages at a time, 150 DPI)
bash /root/work/post-colonial-vietnam/sources/vstb/ocr_volume.sh 1

# Page-by-page (200 DPI, more reliable on corrupted pages)
bash /root/work/post-colonial-vietnam/sources/vstb/ocr_volume_v2.sh 1
```

**Never run multiple in parallel** on this VPS — each volume needs ~9 GB temp space.

### Kanban Integration

Create one kanban card per volume for visibility:
```bash
hermes kanban create "OCR Vol <N>: <title>" \
  --body "OCR volume <N> of <project>. Script: ocr_volume_v2.sh" \
  --priority 2
hermes kanban assign t_<id> default
```
Track progress via the board. Add a synthesis card gated on all volumes completing.

### Step 3: Monitor Progress

```bash
# Follow log output
tail -f /tmp/vstb_ocr_1/*.log 2>/dev/null

# Check resume point
grep -oP '^=== PAGE \K\d+' output.txt | tail -1

# Line growth
wc -l source.txt
```

### Step 4: Output Storage

```bash
/root/work/post-colonial-vietnam/sources/<source-name>/
├── source.pdf
└── source.txt          # OCR output with page markers
```

## Creating a New OCR Script for a Different Source

If you need to OCR a different scanned PDF (not VSTB), copy the v2 template:

```bash
cp /root/work/post-colonial-vietnam/sources/vstb/ocr_volume_v2.sh /path/to/ocr_source.sh
# Edit the PDF and OUT paths
```

The template already has: `set -e` safety with pdftoppm guard, mktemp unique dirs, trap EXIT cleanup, resume-aware page processing.
```

## Delegation Pattern (For Sub-agent Workers)

When distributing OCR across sub-agents:

```python
# Parent agent splits work by page ranges
VOLUME_PAGES = {"vstb-1": 509, "vstb-2": ..., ...}
PAGES_PER_WORKER = 50  # Adjust based on volume size

def split_page_ranges(total_pages, chunk_size=50):
    ranges = []
    for start in range(1, total_pages + 1, chunk_size):
        end = min(start + chunk_size - 1, total_pages)
        ranges.append((start, end))
    return ranges
```

Each worker sub-agent receives:
- **Input**: PDF path, page range (e.g. pages 1-50)
- **Task**: OCR those pages, return plaintext with page markers
- **Output**: `=== PAGE N ===` delimited text
- **Timeout**: ~30 seconds per page at 300 DPI

## OCR Tuning

| Parameter | Value | When to Change |
|-----------|-------|----------------|
| DPI | 300 | 400 for very small/faint text; 200 for speed |
| `--psm` | 1 (auto) | 6 if uniform block layout; 3 if multi-column |
| Language | `vie+fra` | Remove `fra` if no French; add `eng` if English |
| Output encoding | UTF-8 | Default; don't change |

## Error Handling

- **Empty OCR output** → Try higher DPI (400) or different PSM mode
- **Garbled Vietnamese diacritics** → Still acceptable for structure extraction; translation pass can clean up
- **Missing pages** → Check PDF page count vs output page markers
- **Disk full** → Check `df -h /` first. /tmp lives on the root partition here, not tmpfs — OCR temp files can fill it fast. Use `trap 'rm -rf "$TMPDIR"' EXIT` in all batch scripts to guarantee cleanup even on failure.
