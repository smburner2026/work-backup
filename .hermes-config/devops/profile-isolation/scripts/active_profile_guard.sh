#!/bin/bash
# Guard: ensure active_profile doesn't silently drift from default.
# If active_profile file exists and is NOT "default", log a warning and reset.
# This prevents the terminal/TUI from booting into the wrong profile after restarts.
#
# Usage: schedule as a cron job (every 30 min recommended)
#   cronjob create: "bash ~/.hermes/skills/devops/profile-isolation/scripts/active_profile_guard.sh" every 30m

ACTIVE_PROFILE_FILE="$HOME/.hermes/active_profile"
LOG_FILE="$HOME/.hermes/logs/active_profile_guard.log"

mkdir -p "$(dirname "$LOG_FILE")"

if [ -f "$ACTIVE_PROFILE_FILE" ]; then
    CONTENT=$(cat "$ACTIVE_PROFILE_FILE" 2>/dev/null | tr -d '[:space:]')
    if [ -n "$CONTENT" ] && [ "$CONTENT" != "default" ]; then
        echo "$(date -Iseconds) WARNING: active_profile was '$CONTENT', resetting to default" >> "$LOG_FILE"
        rm -f "$ACTIVE_PROFILE_FILE"
        echo "$(date -Iseconds) Reset: active_profile file removed (now default)" >> "$LOG_FILE"
    fi
fi
