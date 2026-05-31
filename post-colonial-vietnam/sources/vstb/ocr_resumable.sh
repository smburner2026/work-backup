#!/bin/bash
# Resumable OCR for VSTB — each page written atomically, resumes where left off
# Usage: ./ocr_resumable.sh <volume_number>
set -e

VOL=$1
PDF="/root/work/post-colonial-vietnam/sources/vstb/viet-su-tan-bien-quyen-${VOL}.pdf"
OUT="/root/work/post-colonial-vietnam/sources/vstb/viet-su-tan-bien-quyen-${VOL}.txt"
TMPDIR="/tmp/vstb_ocr_${VOL}"
PIDFILE="/tmp/vstb_ocr_${VOL}.pid"
LOGFILE="/tmp/vstb_ocr_${VOL}.log"

PREVENT_CONCURRENT_RUN () {
    if [ -f "$PIDFILE" ]; then
        if kill -0 $(cat "$PIDFILE") 2>/dev/null; then
            echo "[V$VOL] Already running (PID $(cat $PIDFILE)). Exiting."
            exit 0
        fi
        rm -f "$PIDFILE"
    fi
}

# Signal handler — clean up PID file so next run resumes cleanly
CLEANUP () {
    echo "[V$VOL] Received signal, cleaning up..."
    rm -f "$PIDFILE"
    rm -rf "$TMPDIR"
    exit 0
}
trap CLEANUP SIGTERM SIGINT SIGHUP

PREVENT_CONCURRENT_RUN
echo $$ > "$PIDFILE"

# Determine last processed page from output file
LAST_PAGE=0
if [ -f "$OUT" ]; then
    LAST_PAGE=$(grep "^=== PAGE" "$OUT" | tail -1 | sed 's/=== PAGE //;s/ ===//')
    [ -z "$LAST_PAGE" ] && LAST_PAGE=0
fi
START=$(( LAST_PAGE + 1 ))

TOTAL=$(pdfinfo "$PDF" | grep ^Pages: | awk '{print $2}')

if [ "$START" -gt "$TOTAL" ]; then
    echo "[V$VOL] Already complete ($TOTAL pages)." | tee -a "$LOGFILE"
    rm -f "$PIDFILE"
    exit 0
fi

echo "[V$VOL] Resuming from page $START of $TOTAL" | tee -a "$LOGFILE"
START_TIME=$(date +%s)

rm -rf "$TMPDIR"
mkdir -p "$TMPDIR"

# Process one page at a time to minimize memory per batch
for (( PAGE=START; PAGE<=TOTAL; PAGE++ )); do
    PAD=$(printf "%03d" "$PAGE")

    # Extract one page
    if ! pdftoppm -f "$PAGE" -l "$PAGE" -r 150 -png "$PDF" "$TMPDIR/p" >/dev/null 2>&1; then
        echo "[V$VOL] pdftoppm failed on page $PAGE, retrying..." >> "$LOGFILE"
        sleep 1
        pdftoppm -f "$PAGE" -l "$PAGE" -r 150 -png "$PDF" "$TMPDIR/p" >/dev/null 2>&1 || true
    fi

    IMG="$TMPDIR/p-${PAD}.png"

    echo "=== PAGE $PAGE ===" >> "$OUT"
    if [ -f "$IMG" ]; then
        tesseract "$IMG" stdout -l vie+fra --psm 1 2>/dev/null >> "$OUT" || echo "[OCR FAILED PAGE $PAGE]" >> "$OUT"
        rm -f "$IMG"
    else
        echo "[IMAGE MISSING PAGE $PAGE]" >> "$OUT"
    fi
    echo "" >> "$OUT"
    sync

    if (( PAGE % 20 == 0 )); then
        ELAPSED=$(( $(date +%s) - START_TIME ))
        DONE=$(( PAGE - START + 1 ))
        echo "[V$VOL] Progress: $PAGE/$TOTAL (+$DONE in ${ELAPSED}s)" | tee -a "$LOGFILE"
    fi
done

TOTAL_LINES=$(wc -l < "$OUT")
ELAPSED=$(( $(date +%s) - START_TIME ))
echo "[V$VOL] DONE. $TOTAL pages, $TOTAL_LINES lines -> $OUT (${ELAPSED}s)" | tee -a "$LOGFILE"

rm -f "$PIDFILE"
rm -rf "$TMPDIR"
