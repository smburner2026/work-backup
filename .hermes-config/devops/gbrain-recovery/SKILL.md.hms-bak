---
name: gbrain-recovery
description: "Recover G-Brain from broken state — DB corruption, embedding failures, dream cycle hangs, PGLite lock contention with gateway auto-restart."
version: 1.0
author: Hermes Agent
tags: [gbrain, recovery, pglite, embedding, dream-cycle, mcp]
---

# G-Brain Recovery

Recover G-Brain from broken states. Common failures: 0% embedding coverage, dream cycle timeouts, PGLite lock contention, config mismatches.

## Diagnosis

```bash
gbrain stats 2>&1
gbrain doctor 2>&1 | head -20
```

Check: page count, embedded count, embed coverage, brain score, orphan count.

## Common Failures

### 1. 0% Embedding Coverage (Config Mismatch)

**Symptom:** `stats` shows 0 embedded, `embed --all` refuses with dimension mismatch.

**Cause:** DB was created with one vector dimension (e.g., 1024 for nvidia/nemotron) but config was changed to another (e.g., 1536 for text-embedding-3-small).

**Fix:**
```bash
export PATH="/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
source /root/.hermes/.env
export OPENROUTER_API_KEY

# Move old backup
mv /root/.gbrain/brain.pglite.bak /root/.gbrain/brain.pglite.bak.$(date +%Y%m%d%H%M) 2>/dev/null

# Reinit with correct dimensions
cd ~/gbrain
gbrain reinit-pglite --embedding-model openrouter:openai/text-embedding-3-small --embedding-dimensions 1536 --yes 2>&1

# Re-add source path
gbrain sources remove default --confirm-destructive 2>&1 || true
gbrain sources add default --path /root/brain 2>&1

# Import content
gbrain import /root/brain 2>&1  # May need multiple runs (159 files = ~2 passes)
```

### 2. Dream Cycle Timeout (PGLite Lock Contention)

**Symptom:** Cron output shows `propose_takes aborted (SIGTERM)` or `timed out after 900s`.

**Cause:** `gbrain dream` (CLI) and `gbrain serve` (MCP) both try to open PGLite. Gateway auto-restarts serve within seconds of being killed, so sleep-based approaches fail.

**Fix:** The dream cycle script uses a retry loop:
1. Kill MCP server
2. Immediately run dream (race the gateway's respawn)
3. If PGLite still locked, dream runs in filesystem-only mode (lint, backlinks, extract)
4. DB-dependent phases (sync, embed, propose_takes) are handled by MCP server during normal operation

**Key insight:** `gbrain dream` gracefully degrades — it runs filesystem-only phases when PGLite is locked and exits 0.

### 3. Stale MCP Connection (Corrupted Index)

**Symptom:** MCP tools return `index "idx_pages_type" contains corrupted page at block 0`.

**Cause:** MCP server has stale in-memory state after DB rebuild/reinit.

**Fix:**
```bash
kill -USR1 $(pgrep -f "gbrain serve")  # Forces MCP server to reload index
```

### 4. Cron Script Hangs (Self-Heal PGLite Check)

**Symptom:** Dream cycle script hangs for 900s during self-heal step.

**Cause:** Self-heal script tries to open PGLite directly for DB health check, but MCP server holds the lock.

**Fix:** Self-heal script skips DB health check when MCP server is running:
```bash
MCP_CHECK=$(pgrep -f "gbrain serve" 2>/dev/null || true)
if [ -n "$MCP_CHECK" ]; then
    log_ok "DB health check skipped — MCP server holds PGLite lock"
else
    # ... run DB health check
fi
```

## Verified Working Script (v2 — 2026-06-04)

Key fixes for 2GB VPS:
1. Stop gateway service before dream (frees ~825MB, prevents gbrain serve respawn)
2. Use `. /root/.hermes/.env` (POSIX-compatible, works in `/bin/sh` via `at`)
3. Explicitly export API keys (bare assignments in .env aren't exported to child processes)
4. 600s timeout (full cycle with propose_takes needs 5+ min)

```bash
#!/bin/bash
# gbrain-dream-cycle.sh — Nightly G-Brain maintenance
# Strategy: stop gateway service (frees memory + prevents gbrain serve respawn)
#           → run dream → restart gateway
set -uo pipefail

export HOME="/root"
. /root/.hermes/.env 2>/dev/null
# Export key vars for child processes (gbrain dream reads process.env)
export OPENROUTER_API_KEY DEEPSEEK_API_KEY ANTHROPIC_API_KEY OPENAI_API_KEY 2>/dev/null
export PATH="/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
export XDG_RUNTIME_DIR="/run/user/0"

MARKER_FILE="/root/.gbrain/.dream-last-run"
DREAM_TIMEOUT=600  # 10 minutes — full cycle with propose_takes

echo "=== GBRAIN DREAM CYCLE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
cd /root/gbrain

# Step 1: Stop gateway service (stops both gateway AND gbrain serve child)
echo "[1/4] Stopping gateway service..."
systemctl --user stop hermes-gateway.service 2>/dev/null
sleep 2

# Verify gbrain serve is dead
REMAINING=$(pgrep -f "gbrain serve" 2>/dev/null || true)
if [ -n "$REMAINING" ]; then
    echo "  Force-killing remaining gbrain serve processes..."
    pkill -9 -f "gbrain serve" 2>/dev/null || true
    sleep 1
fi

rm -f /root/.gbrain/brain.pglite/postmaster.pid 2>/dev/null

# Step 2: Verify memory is freed
FREE_MEM=$(free -m | awk '/^Mem:/{print $7}')
echo "[2/4] Available memory: ${FREE_MEM}MB"

# Step 3: Run dream cycle
echo "[3/4] Running gbrain dream (timeout ${DREAM_TIMEOUT}s)..."
DREAM_OUTPUT=$(timeout $DREAM_TIMEOUT gbrain dream --dir /root/brain 2>&1)
DREAM_OK=$?

echo "$DREAM_OUTPUT" | tail -10

# Step 4: Restart gateway
echo "[4/4] Restarting gateway service..."
systemctl --user start hermes-gateway.service 2>/dev/null

sleep 3
GW_STATUS=$(systemctl --user is-active hermes-gateway.service 2>/dev/null || echo "unknown")
echo "  Gateway status: $GW_STATUS"

if [ "$DREAM_OK" -eq 0 ]; then
    echo "DREAM CYCLE: completed successfully"
    date -u +%s > "$MARKER_FILE"
    echo "=== DREAM CYCLE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
    exit 0
else
    echo "DREAM CYCLE: failed/timeout with code $DREAM_OK"
    date -u +%s > "$MARKER_FILE"
    echo "=== DREAM CYCLE DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
    exit $DREAM_OK
fi
```

## Environment Requirements

- `OPENROUTER_API_KEY` in `/root/.hermes/.env` (for embedding model)
- `DEEPSEEK_API_KEY` in `/root/.hermes/.env` (for chat model)
- `.env` must use bare assignments (not `export`) — script handles export
- Gateway runs as systemd user service (`hermes-gateway.service`)
- G-Brain at `/root/gbrain/`
- Brain repo at `/root/brain/`
- **Critical:** Use `. /root/.hermes/.env` not `source` (POSIX compatibility for `at` jobs)

## Verification

After recovery, verify:
```bash
gbrain stats 2>&1  # Check embedded count
gbrain search "Ames test" --limit 2 2>&1  # Test search
```

MCP tools should also work:
```bash
# Via MCP (after gateway reconnects)
mcp_gbrain_get_stats
mcp_gbrain_search(query="Ames test", limit=2)
```
