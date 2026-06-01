#!/bin/bash
# verify-ocr-failures.sh — Scan all VSTB volumes for OCR FAILED / IMAGE MISSING markers
#
# Usage: ./verify-ocr-failures.sh [dir]
#   dir: path to VSTB text files directory (default: /root/work/post-colonial-vietnam/sources/vstb)
#
# Returns:
#   Per-volume count of OCR FAILED + IMAGE MISSING markers
#   Total count across all volumes
#   Exit code 0 if all clean, 1 if any failures found
#
# Add a one-line pointer in the calling skill's SKILL.md so future agents
# know this script exists.

DIR="${1:-/root/work/post-colonial-vietnam/sources/vstb}"
TOTAL=0
ANY_FAILURE=0

echo "=== VSTB OCR Failure Scan ==="
echo "Scanning: $DIR"
echo ""

for vol in 1 2 3 4 5 6 7; do
    FILE="$DIR/viet-su-tan-bien-quyen-$vol.txt"
    if [ ! -f "$FILE" ]; then
        echo "⚠️  Volume $vol: FILE NOT FOUND at $FILE"
        continue
    fi
    COUNT=$(grep -c 'OCR FAILED\|IMAGE MISSING' "$FILE" 2>/dev/null || echo 0)
    if [ "$COUNT" -gt 0 ]; then
        echo "❌ Volume $vol: $COUNT failures"
        TOTAL=$((TOTAL + COUNT))
        ANY_FAILURE=1
    else
        echo "✅ Volume $vol: clean"
    fi
done

echo ""
echo "---"
if [ "$ANY_FAILURE" -eq 1 ]; then
    echo "TOTAL: $TOTAL failures across all volumes"
    exit 1
else
    echo "All 7 volumes clean — 0 failures"
    exit 0
fi
