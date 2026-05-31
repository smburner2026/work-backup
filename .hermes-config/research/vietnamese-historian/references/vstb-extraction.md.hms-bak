# VSTB Extraction Pipeline — Việt Sử Tân Biên

## The Source

**Việt Sử Tân Biên** (Phạm Văn Sơn) — 7 volumes, definitive Vietnamese history.
- Location: `/root/work/post-colonial-vietnam/sources/vstb/`
- Format: Scanned PDFs (291 MB total, ~3,500 pages)
- OCR: Tesseract with `vie+fra` (Vietnamese + French)
- Extracted text will be saved as `.txt` alongside each `.pdf`

## Pipeline Architecture

```
PHASE 1                    PHASE 2                  PHASE 3                  PHASE 4
══════════════             ══════════════            ══════════════            ══════════════
Batch OCR                  Structure Extract        Period Map               G-Brain Ingest
│                          │                         │                        │
├── Vol 1 (509p) ──────►  ├── TOC parse ──────────► ├── Period tags ───────► ├── Page create
├── Vol 2 ────────────►   ├── Chapter detect        │  (P1-P7)               │  per period
├── Vol 3 (Nam Bắc) ──►   ├── Figure extraction     ├── Figure map           ├── Cross-link
├── Vol 4 ────────────►   │  (names, dates, roles)  │  per period            │  per figure
├── Vol 5 ────────────►   ├── Event extraction      ├── Timeline             └── Final QC
├── Vol 6 ────────────►   └── Quality flags          │  building
└── Vol 7 ────────────►                              └── Gap analysis
```

## Phase 1: OCR

### Disk & Memory Strategy

This VPS has **38 GB total disk** and **2 GB RAM**. The original approach was sequential-only at 300 DPI PPM, which requires ~25 MB/page temp space and fills disk fast. The refined approach uses **150 DPI PNG** (compressed, ~3 MB/page) and processes page-at-a-time with immediate deletion — this allows multiple concurrent volumes safely.

**Rule of thumb:** At 150 DPI PNG with page-at-a-time processing and per-page cleanup, each tesseract instance uses ~150-200 MB RAM. 5 concurrent volumes fit in 2 GB with headroom. The bottleneck is CPU, not memory or disk.

### Strategy
Use the existing scripts — they handle cleanup, resume, and disk pressure:

| Script | Method | DPI | Batch | Speed | Notes |
|--------|--------|-----|-------|-------|-------|
| `ocr_volume.sh` | Batched PNG | 150 | 10 pgs | Fast | Best for clean PDFs |
| `ocr_volume_v2.sh` | Page-by-page PPM | 200 | 1 pg | Reliable | Survives bad pages |

Both scripts have:
- **Resume-aware**: scan existing output for last `=== PAGE N ===` marker, start from N+1
- **Trap EXIT**: `rm -rf "$TMPDIR"` fires on success, crash, or kill — no orphaned temp files
- **Pdftoppm error skipping**: `set -e` doesn't kill the loop on a bad page — skips and logs
- **Mktemp unique dirs**: no collisions between retries

### Execution

```bash
# Launch one volume (VPS, within-session)
bash ocr_volume.sh $VOL_NUM 150

# Or the v2 variant
bash ocr_volume_v2.sh $VOL_NUM 200

# For long-running volumes that must survive session end, use at or tmux:
echo "bash /root/work/post-colonial-vietnam/sources/vstb/ocr_resumable.sh $VOL_NUM >> /tmp/vstb_ocr_${VOL_NUM}.log 2>&1" | at now
# OR
tmux new-session -d -s ocr_v${VOL_NUM} "bash /root/work/post-colonial-vietnam/sources/vstb/ocr_resumable.sh ${VOL_NUM} 150 2>&1 | tee /tmp/vstb_ocr_${VOL_NUM}.log"

# Monitor
tail -f /tmp/vstb_ocr_${VOL_NUM}*.log 2>/dev/null
grep -oP '^=== PAGE \K\d+' viet-su-tan-bien-quyen-${VOL_NUM}.txt | tail -1
tmux capture-pane -t ocr_v${VOL_NUM} -p | tail -3  # if using tmux
```

You can run **multiple volumes concurrently** as long as each uses 150 DPI PNG and page-at-a-time processing. The VPS (2 GB RAM) handles 4-5 concurrent volumes at ~3-5 pages/min each. For faster results, distribute volumes across machines (see below).

### Cross-Machine Distribution

The local WSL machine has **15 GB RAM** and **940 GB free disk** — ideal for heavy OCR. The VPS scripts hardcode `/root/work/...` paths, so on the local machine you either:
- Symlink: `sudo ln -sf /home/vthen/work /root/work` (needs sudo)
- Copy and modify paths: `sed -i 's|/root/work|/home/vthen/work|g' ocr_resumable_local.sh`

Launch on the local machine via SSH + tmux:
```bash
ssh local-machine "tmux new-session -d -s ocr_v${VOL_NUM} \
  'bash /home/vthen/work/post-colonial-vietnam/sources/vstb/ocr_resumable_local.sh ${VOL_NUM} 150'"
```

Check progress remotely:
```bash
ssh local-machine "grep -c '^=== PAGE' /home/vthen/work/post-colonial-vietnam/sources/vstb/viet-su-tan-bien-quyen-${VOL_NUM}.txt"
ssh local-machine "tmux capture-pane -t ocr_v${VOL_NUM} -p | tail -3"
```

### Gap Handling

The resume scripts detect the **last page** in the output file and start from there. **This fails when the output has gaps** — pages missing in the middle but a later page marker exists. The script thinks the volume is complete.

**Always check for gaps after a partial run:**
```bash
grep "^=== PAGE" "viet-su-tan-bien-quyen-${VOL_NUM}.txt" |
  sed 's/=== PAGE //;s/ ===//' | sort -n |
  awk 'NR>1{for(i=prev+1;i<$1;i++) print "GAP:", i} {prev=$1}'
```

**Fix: Truncate at the first gap, then resume:**
```bash
FIRST_GAP=$(grep "^=== PAGE" "viet-su-tan-bien-quyen-${VOL_NUM}.txt" |
  sed 's/=== PAGE //;s/ ===//' | sort -n |
  awk 'NR>1{for(i=prev+1;i<$1;i++){print i; exit}} {prev=$1}')
sed "/^=== PAGE ${FIRST_GAP}[^0-9]/,\$d" "viet-su-tan-bien-quyen-${VOL_NUM}.txt" > /tmp/fixed.txt
mv /tmp/fixed.txt "viet-su-tan-bien-quyen-${VOL_NUM}.txt"
# Then re-run the resume script
```

### Kanban Integration

Each volume should be a kanban card so progress is visible:
```bash
hermes kanban create "VSTB Vol $N: OCR Việt Sử Tân Biên Quyển $N" \
  --body "OCR volume $N of Việt Sử Tân Biên (vie+fra). Script: ocr_volume.sh or ocr_volume_v2.sh" \
  --priority 2
hermes kanban assign t_<id> default
```

For long-running volumes, also create a card for the Synthesis phase that depends on all 7 volume cards completing.

### Progress Tracking

| Metric | How to check |
|--------|-------------|
| Pages done | `grep -oP '^=== PAGE \K\d+' output.txt \| tail -1` |
| Lines extracted | `wc -l output.txt` |
| Actual text vs noise | Sample pages: `sed -n '/=== PAGE 10 ===/,/=== PAGE 11 ===/p' output.txt` |

### Expected Output

```
sources/vstb/
├── viet-su-tan-bien-quyen-1.pdf      (52 MB, 509 pages)
├── viet-su-tan-bien-quyen-1.txt       (~1-3 MB OCR output)
├── viet-su-tan-bien-quyen-2.pdf      (55 MB)
├── viet-su-tan-bien-quyen-2.txt       (~1-3 MB)
├── viet-su-tan-bien-quyen-3.pdf      (29 MB)
├── viet-su-tan-bien-quyen-3.txt       (~0.5-2 MB)
├── viet-su-tan-bien-quyen-4.pdf      (35 MB)
├── viet-su-tan-bien-quyen-4.txt       (~0.5-2 MB)
├── viet-su-tan-bien-quyen-5.pdf      (38 MB)
├── viet-su-tan-bien-quyen-5.txt       (~0.5-2 MB)
├── viet-su-tan-bien-quyen-6.pdf      (54 MB)
├── viet-su-tan-bien-quyen-6.txt       (~1-3 MB)
└── viet-su-tan-bien-quyen-7.pdf      (31 MB)
    viet-su-tan-bien-quyen-7.txt       (~0.5-2 MB)
```

## Phase 2: Structure Extraction (Per volume, sequential)

### What to Extract

For each volume, produce a `sources/vstb/vstb-vol-{N}-structure.json` with:

```json
{
  "volume": 1,
  "title": "Việt Sử Tân Biên — Quyển I",
  "subtitle": "Thượng Cổ và Trung Cổ Thời Đại",
  "total_pages": 509,
  "total_lines": 12500,
  "author": "Phạm Văn Sơn",
  "preface_pages": [1, 15],
  "table_of_contents": {
    "found_on_pages": [16, 20],
    "sections": [
      {"title": "Phần Thứ Nhất: ...", "start_page": 21, "end_page": 200},
      {"title": "Chương I: ...", "start_page": 21, "end_page": 80},
      ...
    ]
  },
  "periods_covered": ["P1 (Nguyen Dynasty)", "earlier"],
  "key_figures": [
    {"name": "Hùng Vương", "pages": [30, 45], "role": "founder"},
    {"name": "Trần Hưng Đạo", "pages": [200, 250], "role": "military leader"}
  ],
  "french_references": [
    {"author": "Jean Chesneaux", "work": "Contribution à l'histoire...", "page": 10}
  ],
  "quality_flags": [
    {"page": 50, "issue": "faint print", "severity": "minor"},
    {"page": 200, "issue": "water damage", "severity": "moderate"}
  ]
}
```

### TOC Detection Heuristics

Vietnamese historical texts use consistent chapter markers:
- **Phần thứ [N]:** Part number
- **Chương [N]:** Chapter number
- **Mục [N]:** Section number
- **Thế-kỷ thứ [N]:** Century markers
- Dates like **(1802–1887)** or **(1945–1954)**
- Emperor names: **nhà Nguyễn**, **nhà Trần**, **nhà Lê**, **nhà Mạc**
- War/event names: **kháng chiến**, **cách mạng**, **phân tranh**, **chiến tranh**

### OCR-Noise Cleanup

Apply these regex patterns to clean Vietnamese OCR output before parsing:

| Pattern | Replace | Reason |
|---------|---------|--------|
| `[—–-]{2,}` | ` — ` | long dashes |
| `[®©™]` | `` | copyright symbols |
| `\s{2,}` | ` ` | collapsed whitespace |
| `(?<![a-zA-Z])\d{10,}(?![a-zA-Z])` | `` | page numbers / artifact digits |
| `[|¦]` | `` | broken characters |

## Phase 3: Period Mapping

Map each extracted volume's content to the project's 7-period framework.

### Period Definitions

```
P1 — Nguyen Dynasty (1802–1887)
P2 — French Colonial Period (1887–1940)
P3 — Resistance Leaders (1930–1945)
P4 — Japanese Occupation (1945)
P5 — First Indochina War (1946–1954)
P6 — Rise and Fall of Diem (1954–1963)
P7 — Covert Build-Up (1963–1965)
```

Note: VSTB covers Vietnamese history from ancient times. Only chapters within ~1800–1965 are relevant to this project's scope. Earlier content is background context.

### Mapping Rules

- **Pre-1800 content** → flag as "background context" (useful but outside core scope)
- **1802–1887 content** → P1 (Nguyen Dynasty)
- **1887–1940 content** → P2 (French Colonial)
- **1945 content** → P4 (Japanese Occupation)
- **Pre-1887 but relevant to later periods** (land reform, class structures, etc.) → flag for cross-reference
- **No post-1965 extraction needed** (user scope ends at pre-US direct intervention)

### Output

```
sources/vstb/period-map.json
{
  "P1": {"volumes": [1, 2], "pages": "V1:200-350, V2:1-150", "files": [...]},
  "P2": {"volumes": [4, 5], "pages": "...", "files": [...]},
  ...
}
```

## Phase 4: G-Brain Ingest

For each period, create a G-Brain page:

```
slug: sources/vstb-quyen-1
content: |
  ---
  type: book
  source: vstb
  ---
  # Việt Sử Tân Biên — Quyển I

  **Author:** Phạm Văn Sơn
  **Period covered:** [period name]
  **Pages:** [range]
  **Full text:** sources/vstb/viet-su-tan-bien-quyen-1.txt

  ## Table of Contents
  ...

  ## Key Figures
  ...

  ## Key Events
  ...

  ## Notes for Project
  ...
```

## Delegation Architecture

```
                  ┌──────────────────────────┐
                  │  Parent Orchestrator      │
                  │  (This persona)           │
                  └────────────┬─────────────┘
                               │
              ┌────────────────┼────────────────┬────────────────┐
              ▼                ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Worker: Vol 1 │  │ Worker: Vol 2 │  │ Worker: Vol 3 │  │ Worker: Vol N │
    │ OCR + save   │  │ OCR + save   │  │ OCR + save   │  │ OCR + save   │
    └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
              │                │                │                │
              └────────────────┴────────────────┴────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │  Synthesis Worker   │
                    │  Structure extract  │
                    │  Period map         │
                    │  QC                 │
                    └────────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │  G-Brain Ingest     │
                    │  Page creation      │
                    │  Cross-linking      │
                    └────────────────────┘
```

## Verification Gates

| Gate | Check | Who |
|------|-------|-----|
| G1 | All 7 PDFs present | Parent |
| G2 | OCR text files exist, non-zero size | Parent |
| G3 | Sample 5 pages per vol — readable Vietnamese | Parent |
| G4 | Structure JSON valid, TOC parsed | Synthesis |
| G5 | Period map covers all 7 periods | Parent |
| G6 | G-Brain pages created, cross-linked | Parent |
