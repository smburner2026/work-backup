#!/bin/bash
# Double-fork daemon launcher for OCR, survives parent death
# Usage: ./launch_ocr_daemon.sh <volume_number>
set -e

VOL=$1
SCRIPT="/root/work/post-colonial-vietnam/sources/vstb/ocr_volume_detached.sh"
PIDFILE="/tmp/vstb_ocr_${VOL}.pid"
LOGFILE="/tmp/vstb_ocr_${VOL}.log"

# Check if already running
if [ -f "$PIDFILE" ]; then
    EXISTING_PID=$(cat "$PIDFILE")
    if kill -0 "$EXISTING_PID" 2>/dev/null; then
        echo "Already running with PID $EXISTING_PID"
        exit 0
    fi
    rm -f "$PIDFILE"
fi

# Double-fork daemon
(
    # First fork
    (
        # Second fork - fully detached
        exec setsid bash -c "
            exec > \"$LOGFILE\" 2>&1
            echo \"Daemon: starting OCR volume $VOL at \$(date)\"
            echo \$\$ > \"$PIDFILE\"
            exec bash \"$SCRIPT\" \"$VOL\"
        "
    ) &
    # Wait briefly to confirm startup
    sleep 1
) &

# Save the intermediate PID
DAEMON_PID=$!
echo "Daemon launcher PID: $DAEMON_PID"
sleep 2
if [ -f "$PIDFILE" ]; then
    echo "OCR daemon running with PID $(cat $PIDFILE)"
    echo "Tail log with: tail -f $LOGFILE"
else
    echo "PID file not found — may have failed. Check $LOGFILE"
    cat "$LOGFILE" 2>/dev/null | tail -5
fi
