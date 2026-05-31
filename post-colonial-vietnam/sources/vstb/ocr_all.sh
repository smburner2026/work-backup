#!/bin/bash
# Bulk OCR dispatch — run incomplete VSTB volumes on local machine
# Usage: ./ocr_all.sh [machine] [dpi]
#   machine: "local" (WSL) or "vps" (default: local)
#   dpi: 150 (default), 200, 300

MACHINE=${1:-local}
DPI=${2:-150}
BASE_DIR="/home/vthen/work/post-colonial-vietnam/sources/vstb"
SCRIPT="$BASE_DIR/ocr_resumable.sh"

if [ "$MACHINE" = "vps" ]; then
  BASE_DIR="/root/work/post-colonial-vietnam/sources/vstb"
  SCRIPT="$BASE_DIR/ocr_resumable.sh"
fi

echo "=== Bulk OCR Dispatch ==="
echo "Machine: $MACHINE"
echo "DPI: $DPI"
echo ""

# Find incomplete volumes
INCOMPLETE=""
for v in 1 2 3 4 5 6 7; do
  pdf="$BASE_DIR/viet-su-tan-bien-quyen-${v}.pdf"
  out="$BASE_DIR/viet-su-tan-bien-quyen-${v}.txt"

  if [ ! -f "$pdf" ]; then
    echo "Vol $v: PDF not found — skipping"
    continue
  fi

  target=$(pdfinfo "$pdf" 2>/dev/null | grep "^Pages" | awk '{print $2}' 2>/dev/null)
  [ -z "$target" ] && target=0

  if [ -f "$out" ]; then
    pages=$(grep -c "^=== PAGE" "$out" 2>/dev/null || echo 0)
  else
    pages=0
  fi

  if [ "$pages" -ge "$target" ] 2>/dev/null; then
    echo "Vol $v: ✅ $pages/$target — complete"
  else
    echo "Vol $v: ⏳ $pages/$target — needs processing"
    INCOMPLETE="$INCOMPLETE $v"
  fi
done

if [ -z "$INCOMPLETE" ]; then
  echo ""
  echo "All volumes complete. Nothing to do."
  exit 0
fi

echo ""
echo "Starting volumes:$INCOMPLETE"

if [ "$MACHINE" = "local" ]; then
  for v in $INCOMPLETE; do
    tmux new-session -d -s "ocr_v${v}" "bash $SCRIPT ${v} 2>&1 | tee /tmp/vstb_ocr_${v}.log"
    echo "  Vol $v — tmux ocr_v${v}"
  done
  echo ""
  echo "Monitor with:"
  for v in $INCOMPLETE; do
    echo "  tmux capture-pane -t ocr_v${v} -p | tail -3"
  done
else
  for v in $INCOMPLETE; do
    echo "bash $SCRIPT ${v} >> /tmp/vstb_ocr_${v}.log 2>&1" | at now 2>/dev/null
    echo "  Vol $v — at job scheduled"
  done
fi

echo ""
echo "Done."
