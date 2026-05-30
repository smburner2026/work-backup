# Dream Cycle Memory Optimization

## The Problem

`gbrain dream` runs inside a **Bun + PGLite WASM** process that can consume **1.2GB+ RSS** on a full brain (1000+ pages, 6000+ chunks). The WASM runtime pre-allocates a contiguous virtual address space (~74GB virtual), and PGLite loads the entire database into memory. On machines with ≤2GB RAM, this causes OOM kills.

### Observed OOM Profile (1.9GB RAM machine, May 28 2026)

```
OOM-kill: task=bun, pid=1118120
total-vm:74406896kB  anon-rss:1182532kB  (74GB virtual, 1.18GB physical)
System: MemTotal 1.9GB, available ~1.0GB
```

The OOM hit during `backlinks.scan` phase, which loads all brain pages into memory to scan for wikilinks.

### Baseline Memory (before dream)

| Component | RSS | Notes |
|-----------|-----|-------|
| Hermes gateway | ~320MB | Python process |
| tradingview-mcp | ~60MB | Python (uvx) |
| gbrain MCP server | ~320MB | bun + PGLite WASM |
| wundertrading proxy | ~60MB | Python |
| System services | ~200MB | systemd, journald, tailscaled, etc. |
| **Total baseline** | **~960MB** | Before dream starts |

After killing gbrain MCP server: frees ~320MB → baseline drops to ~640MB.

Available RAM for dream: 1.9GB - 640MB = ~1.26GB. Dream needs ~1.2GB. **Right at the edge.**

## Mitigation Techniques

### 1. Kill ALL MCP Servers (not just gbrain)

The dream cycle script already kills `gbrain serve` to free the PGLite lock. Also kill tradingview-mcp and wundertrading to reclaim another ~120MB:

```bash
pkill -f "gbrain serve" 2>/dev/null
pkill -f "tradingview-mcp" 2>/dev/null
pkill -f "wundertrading" 2>/dev/null
sleep 3  # Let kernel reclaim pages
```

Hermes auto-restarts all MCP servers on the next tool call that needs them.

**Impact:** Frees ~120MB. Low effort, high ROI.

### 2. Run Dream Phases Individually

Instead of `gbrain dream --json` (runs all 9 phases in one bun process), run each phase separately:

```bash
gbrain dream --phase lint 2>&1          # filesystem-only, ~5s
gbrain dream --phase backlinks 2>&1     # filesystem-only, memory-heavy
gbrain sync --repo ~/brain/ 2>&1        # import from brain repo
gbrain dream --phase embed --stale 2>&1 # vector embeddings (API)
gbrain dream --phase extract 2>&1       # link/timeline extraction
gbrain dream --phase orphans 2>&1       # report only
```

Each `gbrain dream --phase X` starts a fresh bun process, runs one phase, and exits. Memory is fully reclaimed between phases. Peak RSS per phase is typically 300-600MB instead of 1.2GB.

**Available phases (from `src/core/cycle.ts`):**
`lint`, `backlinks`, `sync`, `synthesize`, `extract`, `extract_facts`, `resolve_symbol_edges`, `patterns`, `recompute_emotional_weight`, `consolidate`, `propose_takes`, `grade_takes`, `calibration_profile`, `embed`, `orphans`, `purge`, `schema-suggest`

Note: `sync` is a separate CLI command (`gbrain sync --repo ~/brain/`), not a dream `--phase`.

**Impact:** Reduces peak memory 40-60%. Adds ~5s overhead for process restarts.

### 3. Increase Swap

1GB swap is insufficient for a 1.2GB RSS process. Adding 3GB+ swap lets the kernel page out less-frequently-used memory from other processes:

```bash
fallocate -l 3G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo "/swapfile none swap sw 0 0" >> /etc/fstab
```

**Impact:** Cheap OOM buffer. If disk is slow (HDD), dream may take longer but won't crash.

### 4. Set `vm.swappiness = 100`

Makes the kernel swap more aggressively, keeping RAM free. Trade-off: other processes get slower when paged out:

```bash
sysctl vm.swappiness=100
echo "vm.swappiness=100" >> /etc/sysctl.conf
```

### 5. Eliminate Redundant Pre-Dream Steps

The original script ran:
1. `gbrain sync --repo ~/brain/` → imports markdown → bun+PGLite starts, works, exits
2. `gbrain embed --stale` → embeds stale → another bun+PGLite
3. `gbrain extract links --source db` → another bun+PGLite
4. `gbrain extract timeline --source db` → another bun+PGLite
5. `gbrain dream --dir ~/brain/ --json` → runs sync/embed/extract AGAIN internally

Save 3 unnecessary bun+PGLite cycles by dropping steps 2-4. The dream cycle's `sync` phase does git pull + import, its `embed` phase does stale embedding, and its `extract` phase does link+timeline extraction.

**Impact:** Reduces total PGLite invocations from 5 to 1, eliminating potential lock contention.

### 6. Skip the Backlinks Phase (most memory-heavy)

If OOM consistently hits during `backlinks.scan`, skip that phase specifically:

```bash
gbrain dream --phase lint 2>&1
gbrain sync --repo ~/brain/ 2>&1
gbrain dream --phase embed --stale 2>&1
gbrain dream --phase orphans 2>&1
# skip backlinks
```

Backlinks are important for the knowledge graph, but not critical for basic search functionality. They can be run separately on a less-loaded schedule.

### 7. Switch to Remote Postgres (the actual fix)

PGLite WASM is the root cause — its in-process Postgres engine pre-allocates huge amounts of memory. Switching to a real Postgres instance (Neon free tier, Supabase, or local `pg`) eliminates WASM entirely:

```bash
# After setting up Postgres, migrate:
gbrain migrate --to supabase --connection-url postgres://...
```

Local Postgres typically uses 50-150MB for the same workload. The gbrain CLI process drops to <200MB RSS.

**Impact:** Frees ~800MB+ per dream cycle. The most effective option but requires infrastructure setup.

## Swap Sizing Guide

| RAM | Recommended swap | Dream cycle behavior |
|-----|-----------------|---------------------|
| 1GB | 4GB+ | Marginal — frequent OOM risk |
| 2GB | 4GB | Manageable with mitigations 1-4 |
| 4GB | 2GB | Comfortable with mitigations |
| 8GB+ | 1GB | No issues |

## Quick Recipe for 2GB RAM Machine

```bash
# 1. Add swap
fallocate -l 3G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile

# 2. Replace dream cycle script with phase-by-phase pattern:
cat > ~/.hermes/scripts/gbrain-dream-cycle.sh << 'SCRIPT'
#!/bin/bash
set -uo pipefail
set -a; source /root/.hermes/.env 2>/dev/null; set +a
export PATH="$HOME/.bun/bin:/usr/local/bin:/usr/bin:/bin"
cd ~/gbrain

echo "=== GBRAIN DREAM CYCLE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

# Kill ALL MCP servers
pkill -f "gbrain serve" 2>/dev/null; pkill -f "tradingview-mcp" 2>/dev/null
pkill -f "wundertrading" 2>/dev/null
sleep 3
rm -f /root/.gbrain/brain.pglite/postmaster.pid

# Run phases individually — lower peak memory
OK=0
gbrain dream --phase lint 2>&1 || OK=1
gbrain dream --phase backlinks 2>&1 || OK=1
gbrain sync --repo ~/brain/ 2>&1 || OK=1
gbrain dream --phase embed --stale 2>&1 || OK=1
gbrain dream --phase orphans 2>&1 || OK=1

date -u +%s > ~/.gbrain/.dream-last-run
echo "DREAM CYCLE: $( [ $OK -eq 0 ] && echo ok || echo partial )"
echo "=== DONE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
SCRIPT
```

## References

- `https://github.com/garrytan/gbrain/blob/main/src/core/cycle.ts` — phase definitions
- `https://hermes-agent.nousresearch.com/docs/developer-guide/cron-internals` — cron script timeout config
- `pglite-database-recovery.md` — corruption recovery after OOM
