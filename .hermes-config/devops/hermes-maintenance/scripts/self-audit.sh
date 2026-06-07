#!/bin/bash
# self-audit.sh — Nightly check for updates & component health
# Silent when nothing to report (watchdog pattern — only outputs on changes)
set -euo pipefail

UPDATES=""
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
VENV_PYTHON="${VENV_PYTHON:-/usr/local/lib/hermes-agent/venv/bin/python3}"

# ── 1. Hermes base ──────────────────────────────────────────────────
CURRENT_SHA=$(git -C /usr/local/lib/hermes-agent rev-parse HEAD 2>/dev/null || echo "")
LATEST_SHA=$(curl -sf https://api.github.com/repos/NousResearch/hermes-agent/commits/main 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || echo "")
if [ -n "$CURRENT_SHA" ] && [ -n "$LATEST_SHA" ] && [ "$CURRENT_SHA" != "$LATEST_SHA" ]; then
    CURRENT_VER=$(git -C /usr/local/lib/hermes-agent describe --tags --abbrev=0 2>/dev/null || echo "unknown")
    BEHIND=$(git -C /usr/local/lib/hermes-agent rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
    if [ "$BEHIND" -gt 0 ]; then
        UPDATES+="• Hermes: $BEHIND commit(s) behind tag $CURRENT_VER — hermes update\n"
    fi
fi

# ── 2. hermes-lcm (git remote) ──────────────────────────────────────
LCM_DIR="/usr/local/lib/hermes-agent/plugins/context_engine/lcm"
if [ -d "$LCM_DIR/.git" ]; then
    cd "$LCM_DIR"
    OLD_HEAD=$(git rev-parse HEAD)
    git fetch origin 2>/dev/null || true
    NEW_HEAD=$(git rev-parse HEAD)
    BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
    if [ "$BEHIND" -gt 0 ]; then
        LCM_VER=$(git describe --tags --abbrev=0 2>/dev/null || echo "unknown")
        UPDATES+="• hermes-lcm: $BEHIND commit(s) behind ($LCM_VER) — cd $LCM_DIR && git pull\n"
    fi
fi

# ── 3. Mnemosyne (pip) ──────────────────────────────────────────────
INSTALLED_MNEMO=$($VENV_PYTHON -m pip show mnemosyne-memory 2>/dev/null | grep "^Version:" | cut -d' ' -f2 || echo "not_installed")
AVAIL_MNEMO=$($VENV_PYTHON -m pip index versions mnemosyne-memory 2>/dev/null | grep "^Available versions:" | head -1 | sed 's/.*: *//' | cut -d',' -f1 || echo "unknown")
if [ "$INSTALLED_MNEMO" != "$AVAIL_MNEMO" ] && [ "$AVAIL_MNEMO" != "unknown" ] && [ "$INSTALLED_MNEMO" != "not_installed" ]; then
    UPDATES+="• mnemosyne-memory: $INSTALLED_MNEMO → $AVAIL_MNEMO — pip install --upgrade mnemosyne-memory\n"
fi

# ── 4. DOGA (GitHub API) ────────────────────────────────────────────
DOGA_INSTALLED=$(grep -m1 "^version:" "$HERMES_HOME/plugins/doga/plugin.yaml" 2>/dev/null | sed 's/.*: *"//' | tr -d '"' || echo "unknown")
DOGA_LATEST=$(curl -sf https://api.github.com/repos/0z1-ghb/doga-hermes/releases/latest 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('tag_name','').lstrip('v'))" 2>/dev/null || echo "unknown")
if [ "$DOGA_INSTALLED" != "$DOGA_LATEST" ] && [ "$DOGA_LATEST" != "unknown" ] && [ -n "$DOGA_LATEST" ]; then
    UPDATES+="• DOGA: v$DOGA_INSTALLED → v$DOGA_LATEST — manual git clone + recopy\n"
fi

# ── 5. Hub skills ───────────────────────────────────────────────────
SKILL_OUTPUT=$(hermes skills update 2>&1 || true)
CLEAN_OUTPUT=$(echo "$SKILL_OUTPUT" | grep -v "Bitwarden\|applied\|Skipping\|No updates" || true)
if [ -n "$CLEAN_OUTPUT" ]; then
    UPDATES+="• Hub skills have available updates — hermes skills update\n"
fi

# ── 6. Cron jobs health ─────────────────────────────────────────────
FAILED_JOBS=$(hermes cron list 2>/dev/null | grep -c "last_status.*error\|last_status.*fail" || true)
if [ "$FAILED_JOBS" -gt 0 ]; then
    UPDATES+="• $FAILED_JOBS cron job(s) have errors — hermes cron list\n"
fi

# ── Report ──────────────────────────────────────────────────────────
if [ -n "$UPDATES" ]; then
    echo "=== Hermes Self-Audit: Updates Available ==="
    echo -e "$UPDATES"
    echo "=== Manifest: ~/.hermes/community-manifest.json ==="
else
    exit 0  # Silent — nothing to report
fi
