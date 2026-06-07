# PGLite Lock Contention — Gateway Auto-Restart Pattern

## The Problem

The Hermes gateway auto-restarts `gbrain serve` (MCP server) within seconds of it being killed. This creates a race condition:

1. Script kills `gbrain serve` to release PGLite lock
2. Gateway detects MCP server down, respawns it (~2-5s)
3. CLI command (`gbrain dream`, `gbrain import`, etc.) starts
4. CLI opens its own PGLite connection — **conflicts with respawned serve**
5. CLI hangs with "Timed out waiting for PGLite lock" or SIGTERM

**Symptom:** Dream cycle script hangs for 180s+ then gets SIGTERM'd, even though the dream itself only takes ~10s.

## Why `gbrain dream` (CLI) conflicts with `gbrain serve` (MCP)

Both open independent PGLite connections. PGLite only allows **one writer** at a time. When both run simultaneously:
- The CLI waits for the lock → times out after 180s
- Or the cron scheduler kills the process (SIGTERM) before it completes

## Why direct runs work but cron doesn't

When you run `gbrain dream` directly from a terminal:
- The MCP server may not have restarted yet (lucky timing)
- Or the dream completes fast enough (~10s) before the gateway respawns serve

When the cron scheduler runs the same script:
- The gateway respawns serve immediately (~2-5s)
- The dream's LLM phases (`propose_takes`) add latency
- Total time exceeds the lock timeout → hang → SIGTERM

## Solution: Graceful Degradation

**`gbrain dream` gracefully degrades when PGLite is locked.** It runs filesystem-only phases and skips DB-dependent phases:

| Phase | PGLite needed? | Runs when locked? |
|-------|---------------|-------------------|
| lint | No | ✅ Yes |
| backlinks | No | ✅ Yes |
| extract (FS links/timelines) | No | ✅ Yes |
| sync | Yes | ❌ Skipped |
| embed | Yes | ❌ Skipped |
| propose_takes | Yes | ❌ Skipped |
| grade_takes | Yes | ❌ Skipped |
| consolidate | Yes | ❌ Skipped |

The dream exits with code 0 even in degraded mode — it considers filesystem-only work a success.

## Cron Script Pattern

```bash
#!/bin/bash
# gbrain-dream-cycle.sh — Works whether or not PGLite is available
set -uo pipefail
source /root/.hermes/.env 2>/dev/null
export PATH="/root/.bun/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/root"

cd /root/gbrain

# Attempt to kill MCP — may or may not succeed (gateway respawns fast)
pkill -9 -f "gbrain serve" 2>/dev/null || true
rm -f /root/.gbrain/brain.pglite/postmaster.pid 2>/dev/null

# Run dream — degrades gracefully if PGLite is still locked
DREAM_OK=0
timeout 180 gbrain dream --dir /root/brain 2>&1 || DREAM_OK=$?

if [ "$DREAM_OK" -eq 0 ]; then
    echo "DREAM CYCLE: completed successfully"
else
    echo "DREAM CYCLE: completed with code $DREAM_OK"
fi
```

**Key insight:** Don't fight the gateway's auto-restart. Let the dream run in degraded mode — the filesystem-only phases (lint, backlinks, extract) still provide value. The DB-dependent phases (sync, embed) are handled by the MCP server during normal operation.

## When Full Dream Is Needed

If you need ALL phases (including sync, embed, propose_takes):

1. **Stop the gateway first** (not just kill gbrain serve):
   ```bash
   # Find and stop the gateway process
   pkill -f "hermes.*gateway" 2>/dev/null || true
   sleep 5
   # Now CLI commands have exclusive PGLite access
   gbrain dream --dir /root/brain
   # Gateway will restart on next Hermes interaction
   ```

2. **Or run during a maintenance window** when no Hermes sessions are active (gateway won't restart if nothing triggers it).

3. **Or use the MCP server's job queue** (if available):
   ```bash
   # Submit dream as a job through the MCP server
   # (avoids PGLite contention entirely)
   ```

## Prevention

- **Don't add longer sleeps** — the gateway respawns in ~2-5s, no sleep is long enough
- **Don't try to prevent auto-restart** — it's a feature, not a bug
- **Accept degraded mode** for cron — filesystem-only phases still run
- **Run full dream manually** when you need sync/embed — from an interactive session where you can stop the gateway
