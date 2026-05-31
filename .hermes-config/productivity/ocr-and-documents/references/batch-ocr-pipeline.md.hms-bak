# Batch OCR Pipeline — Scanned PDFs

## When to Use

Scanned PDFs (no selectable text) that need Tesseract OCR. Designed for multi-volume books on resource-constrained systems with limited disk.

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Per-page image | Single page at a time | Avoids 12GB+ temp file buildup from batch pdftoppm |
| DPI | 200 (not 300) | Reduces image size from 25MB to 12MB per page — still sufficient for Tesseract |
| Temp dir | `mktemp -d` | Unique path prevents collision between concurrent runs |
| Cleanup | `trap 'rm -rf \"$TMPDIR\"' EXIT` | Guarantees cleanup on crash, error, or SIGTERM |
| Error handling | `if pdftoppm ...; then` | `set -e` is dangerous — guards page loop against transient failures |
| Parallelism | Sequential volumes | Each volume needs 8-12GB temp space; parallel runs fill disk |

## Canonical Script Pattern — With Resume

```bash
#!/bin/bash
set -e

VOL=$1
DPI=${2:-200}
PDF=\"/path/to/volume-${VOL}.pdf\"
OUT=\"/path/to/volume-${VOL}.txt\"
TMPDIR=$(mktemp -d \"/tmp/ocr_${VOL}_XXXXXX\")
trap 'rm -rf \"$TMPDIR\"' EXIT

TOTAL=$(pdfinfo \"$PDF\" 2>/dev/null | grep -i 'pages:' | awk '{print $2}')

# Resume from last completed page — don't nuke partial progress on retry
LAST=0
if [ -f \"$OUT\" ]; then
    LAST=$(grep -oP '^=== PAGE \\K\\d+' \"$OUT\" 2>/dev/null | tail -1)
    LAST=${LAST:-0}
    echo \"[$VOL] Resuming from page $((LAST + 1)) ($LAST pages done previously)\"
fi

COUNT=$LAST

for ((P=LAST+1; P<=TOTAL; P++)); do
    PAGE=$(printf \"%03d\" $P)

    # Convert one page — skip on failure, don't kill the loop
    if pdftoppm -r \"$DPI\" -f \"$P\" -l \"$P\" \"$PDF\" \"$TMPDIR/p\" 2>/dev/null; then
        IMG=\"$TMPDIR/p-${PAGE}.ppm\"
        [ ! -f \"$IMG\" ] && IMG=\"$TMPDIR/p-${P}.ppm\"

        if [ -f \"$IMG\" ]; then
            echo \"=== PAGE $P === \" >> \"$OUT\"
            tesseract \"$IMG\" stdout -l vie+fra --psm 1 2>/dev/null >> \"$OUT\"
            echo \"\" >> \"$OUT\"
            rm -f \"$IMG\"
        else
            echo \"=== PAGE $P (IMAGE MISSING) === \" >> \"$OUT\"
        fi
    else
        echo \"=== PAGE $P (CONVERSION FAILED) === \" >> \"$OUT\"
    fi

    COUNT=$((COUNT + 1))
    [ $((COUNT % 50)) -eq 0 ] && echo \"[$VOL] Progress: $COUNT/$TOTAL pages\"
done

echo \"[$VOL] DONE. $COUNT pages -> $OUT\"
```

## Multi-Volume Kanban Integration

For multi-volume OCR projects, create one kanban card per volume so progress is visible and retries are trackable:

```bash
hermes kanban create "OCR Volume N: <title>" \
  --body "OCR volume N of <project>. Script: ocr_batch.sh" \
  --priority 2
hermes kanban assign t_<id> default
```

This also lets you add a synthesis card that depends on all volume cards completing, keeping the full pipeline visible on the board.

## Known Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "Could not write image to ... page-N.ppm" | Disk full during pdftoppm | Free space, reduce DPI, or run page-at-a-time (already doing it — reduce DPI to 200) |
| Tesseract returns garbled diacritics | Language model mismatch | Verify `tesseract --list-langs` has `vie` and `fra` installed |
| Repeated "(CONVERSION FAILED)" on consecutive pages | PDF has corrupt range | Check PDF integrity with `pdfinfo` — may need re-download |
| Output file truncated mid-page | Previous run cleared `> "$OUT"` (old script pattern) | Scripts now use resume-aware pattern — checks last completed page from existing file, starts from `LAST+1`. Ensure you're using the updated canonical script with the `LAST=$(grep ...)` logic. |
| Script exits with no output | `set -e` + pdftoppm failure on page 1 | Trap EXIT cleaned up. Check `df -h /` — likely ENOSPC |
| Resume exits immediately saying "already complete" but pages are missing | **Resume-by-last-page gap failure** — output has a gap in page numbers, but the last page marker equals `TOTAL`, so `LAST+1 > TOTAL` and the loop never executes. Happens when a previous run was interrupted mid-volume, then restarted from a later page (e.g., pages 1-49 done, then pages 114-509 done, but pages 50-113 never processed). | See "Resume-by-last-page failure with gaps" below. |
| Output has more `=== PAGE` markers than PDF pages | Duplicate page markers from overlapping runs | Check with `sort -n | uniq` vs raw count. If duplicates exist but all pages are present, the file is usable. The duplicates come from multiple resume runs overlapping the last few pages. Strip exact duplicates if needed. |

## Resume-by-last-page failure with gaps

### The problem

Both `ocr_resumable.sh` and the canonical script above determine where to resume by finding the **last page marker** in the output file:

```bash
LAST=$(grep -oP '^=== PAGE \K\d+' "$OUT" | tail -1)
START=$((LAST + 1))
```

This works perfectly when the output file is a contiguous sequence of pages 1..N. But if there's a **gap** — pages that were never processed — `tail -1` returns a page number near the end, making `START` greater than `TOTAL`. The script then exits immediately, claiming the volume is complete, while pages in the middle are missing forever.

### How gaps happen

Gaps appear when a script is interrupted mid-run, then manually restarted from a point *after* the interruption point. Common causes:

1. **OOM kill mid-volume** — Pages 1-350 done, process killed at page 351. Operator restarts from page 400 (to skip a known-bad section), then lets it run to completion. Result: pages 351-399 never processed.
2. **Partial re-run** — After a crash, a different script/approach is used that overlaps unevenly.
3. **Manual page skipping** — A corrupt PDF section is skipped, then the resumption doesn't go back to fill the skip.

### Detection

Before relying on resume, always check for gaps:

```bash
grep "^=== PAGE" "$OUT" | sed 's/=== PAGE //;s/ ===//' |
  sort -n | awk 'NR>1{for(i=prev+1;i<$1;i++) print "GAP:", i} {prev=$1}'
```

If this outputs any "GAP:" lines, the file has missing pages.

Also compare the count vs expected:

```bash
PDF_PAGES=$(pdfinfo "$PDF" | grep ^Pages | awk '{print $2}')
OCR_PAGES=$(grep "^=== PAGE" "$OUT" | wc -l)
UNIQ_PAGES=$(grep "^=== PAGE" "$OUT" | sed 's/=== PAGE //;s/ ===//' | sort -n | uniq | wc -l)
echo "PDF: $PDF_PAGES, OCR markers: $OCR_PAGES, Unique pages: $UNIQ_PAGES"
```

If `UNIQ_PAGES < OCR_PAGES`, there are duplicates. If `UNIQ_PAGES < PDF_PAGES`, there are gaps.

### Remediation — Truncate-and-resume

To fix a gap, truncate the output file at the **first missing page**, then re-run the resume script. This discards everything after the gap (which will be re-OCR'd) but preserves the pages before it:

```bash
# 1. Find the first gap
FIRST_GAP=$(grep "^=== PAGE" "$OUT" | sed 's/=== PAGE //;s/ ===//' |
  sort -n | awk 'NR>1{for(i=prev+1;i<$1;i++){print i; exit}} {prev=$1}')

# 2. Truncate the output file at that page
#    (removes everything from the first page >= FIRST_GAP onwards)
sed "/^=== PAGE ${FIRST_GAP}[^0-9]/,\$d" "$OUT" > /tmp/ocr_fixed.txt
mv /tmp/ocr_fixed.txt "$OUT"

# 3. Verify
echo "Pages kept: $(grep -c '^=== PAGE' "$OUT")"
echo "Last page: $(grep '^=== PAGE' "$OUT" | tail -1)"

# 4. Re-run the resume script — it will now start from FIRST_GAP
bash ocr_resumable.sh <volume>
```

**For `ocr_volume_v2.sh`** (which also uses `tail -1` resume), the same remediation applies.

**One-page gaps (99.8% complete):** If only 1 page is missing (e.g., 498/499 pages OCR'd), consider whether it's worth the time to re-process the entire remaining range. The gap-fill takes just as long as a full run from that point, because the script processes every page from `FIRST_GAP` to the end. If 498/499 pages are usable, a manual `pdftoppm + tesseract` for the single missing page is faster:

```bash
PAGE=54  # the missing page
pdftoppm -f $PAGE -l $PAGE -r 200 "$PDF" /tmp/missing
tesseract /tmp/missing-054.ppm stdout -l vie+fra --psm 1 >> "$OUT"
# Insert the marker if the resumable approach wasn't used
```

### Prevention

To prevent gaps in the first place:

- **Never manually skip pages.** If a page fails OCR, let the script log `(CONVERSION FAILED)` rather than skipping the page number in the output.
- **Use PID-file protected scripts** (like `ocr_resumable.sh`) that prevent concurrent runs from interleaving writes.
- **One process per volume.** Don't OCR the same volume from two terminals.
- **Atomic page markers.** The `=== PAGE N ===` marker and content must be written in the same script block — not split across append operations that could interleave.

## Persistent Background Execution

OCR of a multi-volume book (500+ pages/volume) takes 1-3 hours per volume. When running through Hermes, background processes can be killed when the session ends (SIGTERM on session close, timeout on `notify_on_complete=true`, etc.).

### Reliable patterns for long-running OCR

Choose based on what's available on the target machine:

| Pattern | Available via | Pros | Cons |
|---------|-------------|------|------|
| `at now` | Most Linux distros | Survives reboot up to queue retention, fully detached | Not available on WSL/macOS |
| tmux | Most Linux distros, WSL | Survives SSH disconnect, can reattach to monitor | Needs explicit cleanup of session |
| Hermes bg | Always | Integrated with Hermes lifecycle | Dies when session ends (hard 30-min limit) |

**Pattern 1 — `at now` (most reliable)**

Schedules the script in the system at-queue, fully independent of the Hermes session. Survives session closure, SSH disconnection, and reboots (up to the at-queue retention):

```bash
echo 'bash /path/to/ocr_resumable.sh <vol> >> /tmp/ocr_<vol>_cron.log 2>&1' | at now
```

Check status:

```bash
atq                           # List queued/running jobs
tail -f /tmp/ocr_<vol>_cron.log  # Follow progress
```

**Pattern 2 — tmux session (for machines without `at`, e.g. WSL)**

Creates a detached tmux session that continues running after SSH/Hermes disconnects:

```bash
tmux new-session -d -s ocr_vol<N> \
  'bash /path/to/ocr_resumable.sh <vol> 150 2>&1 | tee /tmp/ocr_<vol>.log'
```

Monitor:

```bash
tmux capture-pane -t ocr_vol<N> -p | tail -5
```

To kill the tmux session when done:

```bash
tmux kill-session -t ocr_vol<N>
```

**Pattern 3 — Hermes background (within-session only)**

Use `terminal(background=true)` without `notify_on_complete=true`. The process runs as long as the Hermes session is alive. Good for shorter runs or when you're actively monitoring.

**⚠ Watch out:** Hermes background processes have a hard ~30-min timeout regardless of the `timeout=` parameter. For runs longer than 30 min, prefer `at` or tmux.

### Running multiple volumes concurrently

On a 2GB RAM VPS, you can run **multiple volume OCRs concurrently** IF each uses:
- **Page-at-a-time processing** (not batch `pdftoppm`)
- **150 DPI** (lower image quality but ~3MB/page instead of 12MB)
- **PNG format** (compressed, vs PPM uncompressed) — use `pdftoppm -png`
- One-page-at-a-time deletion (`rm -f` after each tesseract call)

At 150dpi PNG, each tesseract process uses ~150-200MB RAM. Five concurrent processes fit in 2GB with headroom for the gateway and OS. The bottleneck is CPU (not memory) — expect ~3-5 pages/min per volume instead of ~8-10 pages/min when running solo.

### Cross-machine distribution

If you have a second machine with more resources (e.g. a local WSL machine with 15GB RAM), split the workload: run some volumes on the primary machine and some on the secondary. This requires:

1. **SSH key setup** so the primary machine can connect to the secondary:
   ```bash
   # On the primary machine, get the SSH public key
   cat ~/.ssh/id_ed25519.pub
   # Add it to ~/.ssh/authorized_keys on the secondary machine
   ```

2. **Path portability**: Scripts with hardcoded paths (e.g. `/root/work/...`) fail when run on a different machine as a different user. Fix by either:
   - **Symlink**: `sudo ln -sf /home/vthen/work /root/work`
   - **Copy-and-modify**: `sed -i 's|/root/work|/home/vthen/work|g' ocr_resumable_local.sh`

3. **Launch via tmux** on the remote machine (since `at` is usually unavailable on WSL):
   ```bash
   ssh remote-machine "tmux new-session -d -s ocr_vol<N> \\
     'bash /home/vthen/work/.../ocr_resumable_local.sh <vol> 150'"
   ```

## Quality Check

```bash
# Quick sample
head -80 /path/to/volume-1.txt | sed -n '2p'

# Page count
grep -c "^=== PAGE" /path/to/volume-1.txt

# Missing/conversion-failed count
grep -c "FAILED\|MISSING" /path/to/volume-1.txt

# Check for gaps (see "Resume-by-last-page failure with gaps" above)
grep "^=== PAGE" "$OUT" | sed 's/=== PAGE //;s/ ===//' |
  sort -n | awk 'NR>1{for(i=prev+1;i<$1;i++) print "GAP:", i} {prev=$1}'
```
