---
name: vstb-ocr-workflow
description: Canonical workflow for OCR'ing VSTB (Việt Sử Tân Biên) volumes using ocr_resumable.sh — one-page-at-a-time, PID-protected, auto-resume. Lessons learned from a painful first run.
---

# VSTB OCR Workflow

## Infrastructure

- **Primary compute**: User's local WSL (DESKTOP-B4LB6VL, 15GB RAM, 16 cores)
- **Fallback**: VPS at 178.156.199.37 (2GB RAM — avoid for batch OCR)
- **Connection**: `ssh local-machine` from VPS (key-based, config in ~/.ssh/config)

## Canonical script

Only one script matters: `ocr_resumable.sh`

Location: both VPS and WSL at:
```
<workdir>/sources/vstb/ocr_resumable.sh
```

Where `<workdir>` is `/root/work/post-colonial-vietnam/` on VPS or `/home/vthen/work/post-colonial-vietnam/` on WSL.

What it does:
- One page at a time at 150dpi (memory safe)
- PNG temp files (compressed, ~100KB/page vs 11MB for PPM)
- PID file lock prevents concurrent runs
- Auto-resumes from last completed page
- Cleans up temp files per-page (no OOM risk)
- `vie+fra` language for tesseract

Usage:
```bash
bash ocr_resumable.sh <volume_number>
```

## Bulk dispatch

Script: `ocr_all.sh [local|vps] [dpi]`

Defaults to local (WSL). Spawns one tmux session per incomplete volume:
```bash
bash <workdir>/sources/vstb/ocr_all.sh           # WSL, 150dpi
bash <workdir>/sources/vstb/ocr_all.sh vps 150    # VPS, 150dpi
```

## Quick connection scripts (VPS → WSL)

| Script | Purpose |
|--------|---------|
| `/root/connect-local.sh [cmd]` | Interactive SSH to WSL |
| `/root/run-local.sh <cmd>` | Run command on WSL, get output |
| `/root/sync-local.sh push\|pull [vol]` | Sync OCR outputs (push=VPS→WSL, pull=WSL→VPS) |

## Compute selection logic (for re-runs / recovery)

When dispatching OCR, decide compute target in this order:

1. **Try WSL first** — `ssh -o ConnectTimeout=5 local-machine exit` (or `./run-local.sh echo ok`). If it responds, use WSL (2s/page, 15GB RAM, 16 cores).
2. **Fall back to VPS** if local is unreachable. VPS is ~8s/page with 2GB RAM, but the resumable script handles this safely (one-at-a-time, 150dpi, PNG temp files). Check disk space first: `df -h /` needs >=5GB free for temp files + output.
3. **Never launch both simultaneously** — the output file will race. If switching compute mid-stream, ensure the target machine has the latest output file first (use `./sync-local.sh push` or `pull` as appropriate).

VPS fallback launcher:
```bash
# Ensure PID files are clean
rm -f /tmp/vstb_ocr_<N>.pid
# Launch in terminal background (notify_on_complete=true, timeout=7200)
bash ocr_resumable.sh <N>
```
Tesseract consumes ~90-170MB RAM per process on the VPS at 150dpi PNG. With 2GB total and nothing else memory-intensive running, two concurrent processes coexist safely. Monitor with `ps aux | grep tesseract | grep -v grep`.

## Critical Lessons (don't repeat these)

1. **Never `pull` from WSL unless WSL is the complete source of truth.** The sync overwrite mistake destroyed 3 completed files because the script defaulted to pull direction without checking which side had fresher data.

2. **Use WSL for batch OCR, not the VPS.** 2GB RAM on the VPS causes OOM with concurrent tesseract instances. The resumable script mitigates this (one-at-a-time) but it's still ~8s/page vs ~2s/page on WSL.

3. **One script, not five.** Earlier versions (ocr_volume.sh, v2, v3, detached, debug, v6_optimized, resume) are all deleted. Only `ocr_resumable.sh` survives. Don't create variants — adapt the canonical one.

4. **Verify the file, not the kanban status.** In this session I marked vols 6 and 7 as "done" on the kanban board, then later overwrote the files with stale copies and started re-running them — but never updated the kanban status. The board said "done" while the files were at 256/502 and 246/465. **Always grep the actual output file to confirm page count before marking things complete.** See `orchestration-workflow` skill Anti-Patterns table for the general version of this rule.

5. **Status checking** — grep the output file:
   ```bash
   grep -c "^=== PAGE" viet-su-tan-bien-quyen-<N>.txt
   ```
   Compare against total (run `pdfinfo <pdf>` for page count).

6. **Gap detection** — If resume scripts report "already complete" but the page count is short, check for gaps (pages present ≠ contiguous sequence):
   ```bash
   # Find gaps between present pages
   grep "^=== PAGE" file.txt | sed 's/=== PAGE //;s/ ===//' | sort -n | \
     awk 'NR>1{for(i=prev+1;i<$1;i++) print "GAP:", i} {prev=$1}'
   
   # Count unique pages (excludes duplicate markers from resume-overlap)
   grep "^=== PAGE" file.txt | sed 's/=== PAGE //;s/ ===//' | sort -n | uniq | wc -l
   ```
   
   **Gap repair procedure:** If gaps exist, truncate the file to keep all pages before the first gap, then run ocr_resumable.sh which will start fresh from the gap's first page:
   ```bash
   # Find the first page AFTER the gap, truncate there
   # E.g., gap at pages 50-113 → first page after gap is 114
   sed '/^=== PAGE 114 ===/,$d' viet-su-tan-bien-quyen-1.txt > /tmp/fixed.txt
   mv /tmp/fixed.txt viet-su-tan-bien-quyen-1.txt
   # Then run ocr_resumable.sh — it will start from page 50
   bash ocr_resumable.sh 1
   ```

7. **Cleanup procedure after OCR completes (all volumes):**
   ```bash
   # Remove temp files
   rm -rf /tmp/vstb_ocr_*
   
   # Clear at jobs (stale scheduled tasks)
   atq && atrm <job_nums>
   
   # Complete kanban tasks from the command line
   hermes kanban unblock <task_id> 2>/dev/null
   hermes kanban complete <task_id> --summary "OCR done"
   
   # Remove kanban workspace dirs
   rm -rf /root/.hermes/kanban/workspaces/t_<task_id>
   ```

8. **Don't trust a partial file.** If you overwrote a complete file with a stale copy, the `tail -1` resume detection may restart from the wrong page. Always verify unique page count matches the PDF total before declaring done.

9. **Scripts must live at persistent paths, not in kanban scratch workspaces.** The OCR script was originally created inside a kanban scratch workspace (`/root/.hermes/kanban/workspaces/t_*`). These directories get GC'd when the kanban task is archived — the script disappears silently with no warning. A recovery `at` job that references the deleted script will fail silently (no output, no error) because the path is gone. Always keep the canonical script in the project directory (`sources/vstb/ocr_resumable.sh`), never in a transient workspace. For background recovery runs on the VPS, use `nohup` with a PID file at a persistent temp path (`/tmp/vstb_ocr_*.pid`) rather than `at` jobs, since `at` binds to the script path at submission time and breaks if the path goes stale. Verify with `atq` or `ps aux | grep tesseract` before assuming a background job is still running.

10. **VPS OOM kills OCR silently — verify progress, don't trust completion.** On the 2GB VPS, an OCR run plus background services can trigger the OOM killer. It may kill a different process (system services) while OCR catches a cascading SIGTERM — the trap handler fires, PID file deleted, no useful log entry. Output simply stops growing. **Symptom:** `ps aux | grep -c tesseract` returns 0 but page count short of PDF total. **Recovery:** clean stale PID (`rm -f /tmp/vstb_ocr_*.pid`), re-launch via `terminal(background=true, notify_on_complete=true, timeout=7200)`. To prevent: stop competing services, run one volume at a time.

11. **Resume-detection blind spot (critical).** The `ocr_resumable.sh` script determines its resume point by reading the last `=== PAGE N ===` marker in the output file (line 38: `grep "^=== PAGE" "$OUT" | tail -1`). This is unreliable because the script writes the `=== PAGE N ===` marker **before** OCRing the page (line 70). The sequence for every page is:

    ```
    echo "=== PAGE $PAGE ===" >> "$OUT"    # ← marker written first
    tesseract ... >> "$OUT"                 # ← OCR text appended (may fail)
    ```

    This means: if all page markers exist but the OCR failed (producing `[IMAGE MISSING]` lines), the resume detection still sees the last page marker and declares the file complete — even though most pages are blank. The script exits with "Already complete" and does no work.

    **Verification must be a separate step before trusting the file. Never rely on the script's self-report of completeness.** The three checks:

    ```bash
    # 1. Count IMAGE MISSING pages — must be 0
    grep -c 'IMAGE MISSING' viet-su-tan-bien-quyen-6.txt

    # 2. Count unique page markers — must match PDF total
    pdfinfo viet-su-tan-bien-quyen-6.pdf | grep ^Pages: | awk '{print $2}'
    grep "^=== PAGE" viet-su-tan-bien-quyen-6.txt | sed 's/=== PAGE //;s/ ===//' | sort -n | uniq | wc -l

    # 3. Check for gaps in page sequence (duplicate markers from resume-overlap are OK)
    grep "^=== PAGE" viet-su-tan-bien-quyen-6.txt | sed 's/=== PAGE //;s/ ===//' | sort -n | \
      awk 'NR>1{for(i=prev+1;i<$1;i++) print "GAP:", i} {prev=$1}'
    ```

    If any IMAGE MISSING pages exist, the file needs truncation before the first gap:
    ```bash
    # Find first IMAGE MISSING page
    grep -n 'IMAGE MISSING' viet-su-tan-bien-quyen-6.txt | head -1
    # Extract the page number, truncate everything from that marker onward
    FIRST_MISSING=$(grep -B1 'IMAGE MISSING' viet-su-tan-bien-quyen-6.txt | grep '^=== PAGE' | head -1 | sed 's/=== PAGE //;s/ ===//')
    sed "/^=== PAGE ${FIRST_MISSING} ===/,\$d" viet-su-tan-bien-quyen-6.txt > /tmp/v6_fixed.txt
    mv /tmp/v6_fixed.txt viet-su-tan-bien-quyen-6.txt
    # Now run ocr_resumable.sh — it will resume from FIRST_MISSING
    bash ocr_resumable.sh 6
    ```

    This truncation technique is safe: it preserves all real OCR text from earlier pages and only removes the empty page markers forward. The script then re-OCR's all pages starting from the first gap.

## Cleanup Checklist (All Volumes Complete)

- [ ] All 7 output files have page counts >= PDF totals (use unique pages, not total markers)
- [ ] Zero `IMAGE MISSING` entries across all files: `grep -c 'IMAGE MISSING' *quyen-*.txt` returns 0 for each
- [ ] No gaps in page sequences: `grep "^=== PAGE" file.txt | sed ... | awk 'NR>1{for(i=prev+1;i<$1;i++) print "GAP:", i} {prev=$1}'` returns empty
- [ ] Temp files removed: `rm -rf /tmp/vstb_ocr_*`
- [ ] Stale at jobs cleared: `atq` then `atrm <ids>`
- [ ] Kanban tasks unblocked and completed
- [ ] Kanban workspace dirs removed: `rm -rf /root/.hermes/kanban/workspaces/t_*`
- [ ] Stale scripts removed (keeping only ocr_resumable.sh and ocr_all.sh)

## Output files

All 7 volumes complete (~3.5MB total text, vie+fra):
```
<workdir>/sources/vstb/viet-su-tan-bien-quyen-{1..7}.txt
```

PDFs live alongside them at:
```
<workdir>/sources/vstb/viet-su-tan-bien-quyen-{1..7}.pdf
```
