#!/bin/bash
# OCR one volume of a scanned PDF — page-by-page, resume-aware, trap EXIT cleanup
# Usage: ./ocr-volume.sh <volume_number> [dpi]
# Copy this file, edit the PDF and OUT paths, then run.
set -e

VOL=$1
DPI=${2:-200}
PDF="/path/to/volume-${VOL}.pdf"
OUT="/path/to/volume-${VOL}.txt"
TMPDIR=$(mktemp -d "/tmp/ocr_${VOL}_XXXXXX")
trap 'echo "[$VOL] Cleaning up..."; rm -rf "$TMPDIR"' EXIT

echo "[$VOL] Starting OCR at ${DPI}dpi"

TOTAL=$(pdfinfo "$PDF" 2>/dev/null | grep -i 'pages:' | awk '{print $2}')
echo "[$VOL] Total pages: $TOTAL"

# Resume from last completed page
LAST=0
if [ -f "$OUT" ]; then
    LAST=$(grep -oP '^=== PAGE \K\d+' "$OUT" 2>/dev/null | tail -1)
    LAST=${LAST:-0}
    echo "[$VOL] Resuming from page $((LAST + 1)) ($LAST pages done previously)"
fi

COUNT=$LAST

for ((P=LAST+1; P<=TOTAL; P++)); do
    PAGE=$(printf "%03d" $P)

    # Convert one page — skip on failure, don't kill the loop
    if pdftoppm -r "$DPI" -f "$P" -l "$P" "$PDF" "$TMPDIR/p" 2>/dev/null; then
        IMG="$TMPDIR/p-${PAGE}.ppm"
        [ ! -f "$IMG" ] && IMG="$TMPDIR/p-${P}.ppm"

        if [ -f "$IMG" ]; then
            echo "=== PAGE $P === " >> "$OUT"
            tesseract "$IMG" stdout -l vie+fra --psm 1 2>/dev/null >> "$OUT"
            echo "" >> "$OUT"
            rm -f "$IMG"
        else
            echo "=== PAGE $P (IMAGE MISSING) === " >> "$OUT"
        fi
    else
        echo "=== PAGE $P (CONVERSION FAILED) === " >> "$OUT"
    fi

    COUNT=$((COUNT + 1))
    [ $((COUNT % 50)) -eq 0 ] && echo "[$VOL] Progress: $COUNT/$TOTAL pages"
done

echo "[$VOL] DONE. $COUNT pages -> $OUT"
