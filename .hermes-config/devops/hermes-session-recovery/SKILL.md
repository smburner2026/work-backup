---
name: hermes-session-recovery
description: Merge WSL/archived session history into the live Hermes session DB so session_search surfaces the full recovered range.
---

# Hermes Session Recovery & WSL Merge

Restore and merge Hermes session history from WSL registry and backup archives into the live session database.

## Problem

- Backup archives in `/root/.hermes/backups/` contain older sessions but do NOT auto-merge into `session_search`.
- WSL sessions live in `/root/.hermes/sessions/sessions-wsl.json` (registry) and are not part of the live DB.
- Aggressive compression/hygiene in `config.yaml` prunes older entries from the live DB.
  - threshold: 0.75
  - target_ratio: 0.2
  - hygiene_hard_message_limit: 600
  - protect_first_n: 3
  - protect_last_n: 20
- User expectation: recovering sessions via backup should make them searchable in `session_search`. This does NOT happen automatically.

## Recovery Sources

1. **Active session files** — `/root/.hermes/sessions/*.jsonl` (live session store)
2. **WSL registry** — `/root/.hermes/sessions/sessions-wsl.json` (851 lines, May 21+)
3. **Backup archives** — `/root/.hermes/backups/` (compressed old sessions, mnemosyne DBs)
4. **LCM database** — `/root/.hermes/lcm.db` (broader cross-session context)

## Findings from 2026-06-08

- `/root/.hermes/sessions/sessions-wsl.json` holds session metadata for WSL desktop + local-machine compute sessions.
- Key periods recovered by inspecting the file:
  - May 21–23: early Telegram/Discord threads
  - May 30: VPS inventory, WSL tailnet peer (`100.110.237.89`)
  - May 31: gbrain update to WSL, VSTB Vol 6 OCR, Hoang Tham OCR/cleanup
  - June 3: Hermes Desktop → VPS Tailscale troubleshooting
  - June 3: opendataloader-pdf install queued for WSL

## Procedure

### 1. Inspect WSL session registry

```bash
wc -l /root/.hermes/sessions/sessions-wsl.json
```

- >500 lines = WSL history exists and is substantial.

### 2. Verify backup archives exist

```bash
ls -lh /root/.hermes/backups/archive/old-sessions/
du -sh /root/.hermes/backups/archive/
```

- Old sessions compressed as `.json.gz` files.
- `sessions-archive/` may contain request dumps.

### 3. Compress / archive large backup collections

```bash
tar -c -I 'zstd -15' -f /root/.hermes/backups/YYYY-MM-DD_old-sessions.tar.zst -C /root/.hermes/backups/archive/old-sessions .
tar -c -I 'zstd -15' -f /root/.hermes/backups/YYYY-MM-DD_archive.tar.zst -C /root/.hermes/backups/archive .
rm -rf /root/.hermes/backups/archive/old-sessions /root/.hermes/backups/archive
```

### 4. Index WSL sessions for searchability

**4a. Verify whether each WSL registry session has a file-backed copy:**

```bash
python3 -c "import os,json; data=json.load(open('/root/.hermes/sessions/sessions-wsl.json')); ids={v['session_id'] for v in data.values()}; files=set(os.listdir('/root/.hermes/sessions')); print('missing=', sorted(ids-files))"
```

**4b. If file-backed copies exist under `/root/.hermes/sessions/`, index recovery is usually automatic.**

**4c. If registry entries have no file backing, document them in `references/wsl-session-inventory.md` so they remain recoverable from filesystem even when `session_search` does not surface them.**

### 5. Validate recovery

```bash
session_search(query="WSL", limit=10)
session_search(query="obsidian vault", limit=5)
```

- Supposed recovered content should match sessions referenced in `sessions-wsl.json`.
- If not present, the recovery preserved the files but did not populate the live search index.

### 4. Merge WSL/Archived Sessions into Live DB — Working Import Procedure

**Validated import method (2026-06-08):**

The backup archives at `/root/.hermes/backups/2026-06-07_old-sessions.tar.zst` contain 411 extracted `.json.gz` session files (May 16–20). These can be imported directly into the LCM database (`/root/.hermes/lcm.db`) which powers `session_search`.

```python
# Import script (run from /tmp after extracting archive)
import json, sqlite3, gzip, os
from pathlib import Path

ARCHIVE_DIR = Path("/tmp")  # extracted session_*.json.gz files
DB_PATH = "/root/.hermes/lcm.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT session_id FROM messages")
existing = {row[0] for row in cursor.fetchall()}

imported = 0
for gz_file in sorted(ARCHIVE_DIR.glob("session_*.json.gz")):
    with gzip.open(gz_file, 'rt') as f:
        data = json.load(f)
    session_id = data['session_id']
    if session_id in existing:
        continue
    platform = data.get('platform', 'unknown')
    for msg in data['messages']:
        cursor.execute("""
            INSERT INTO messages (session_id, source, role, content, tool_call_id, tool_calls, tool_name, timestamp, token_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, platform, msg.get('role'), msg.get('content', ''),
              msg.get('tool_call_id', ''), json.dumps(msg.get('tool_calls', [])),
              msg.get('tool_name', ''), data.get('session_start', 0), len(msg.get('content', ''))//4))
    imported += 1
conn.commit()
print(f"Imported {imported} new sessions")
```

**Results:** 410 sessions imported, 472 total sessions, 68,264 messages. `session_search` now returns May 16–20 sessions (e.g., "pdf generation", "WSL", "Obsidian vault", "DABT Tutor" queries all hit).

### 4a. WSL Registry Merge

The WSL registry (`/root/.hermes/sessions/sessions-wsl.json`, 851 lines) is a metadata index only — it does not contain message content. It cannot be directly imported into `session_search`. If WSL session message files exist on the WSL machine, they must be synced via `hermes-multi-sync` or copied manually to `/root/.hermes/sessions/` as `.jsonl` files, then the LCM import will pick them up if not already present.

**Action sequencing rule:** When the user requests recovery/merge, execute the LCM import before pivoting to unrelated diagnostics. Validate with `session_search` queries immediately after.

### 4b. Recommended Three-Path Search Plan (confirmed session-review pattern)
1. Quick semantic path — FTS fallback.
2. Strict path when exact IDs are known — `session_id=<id>` keyword search.
3. Profile-scoped lookup when cross-profile separation may be hiding matches.

Use this ordering when users say session history is missing; it is not just file presence but whether search indexes those IDs.
- Old sessions may contain copy-paste degradation from prior compaction.
- Session hygiene settings may delete older entries again unless adjusted.
 
## LCM Timestamp Limitation (2026-06-08)

Archive `.json.gz` session files only store `session_start` at the session level — NOT per-message timestamps. The import script assigns `session_start` to ALL messages in a session. This means:
- `session_search` by date range is **imprecise** for recovered sessions (all messages in a session share the same timestamp)
- FTS5 topic/content search works correctly
- For details, see `references/lcm-timestamp-limitation.md`

## Cross-Store Verification (2026-06-08)

After any recovery operation, verify both LCM and Mnemosyne show continuous, overlapping coverage to ensure no gaps in the historical record. This prevents situations where sessions are imported but memories are missing (or vice versa), which creates the illusion of recovery while losing verifiable knowledge.

**Verification procedure:**
```bash
# 1. Check LCM session coverage (should be continuous after import)
sqlite3 ~/.hermes/lcm.db "SELECT 
    SUBSTR(session_id,1,8) as day, 
    COUNT(DISTINCT session_id) as sessions 
    FROM messages 
    WHERE session_id GLOB '2026*' 
    GROUP BY day 
    ORDER BY day;"

# 2. Check Mnemosyne memory coverage (should show continuous daily accumulation)
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "SELECT 
    DATE(timestamp) as day, 
    COUNT(*) as memories 
    FROM working_memory 
    WHERE timestamp >= '2026-05-18' 
    GROUP BY day 
    ORDER BY day;"

# 3. Verify overlap exists (both stores should have data for same dates)
# Expected: LCM may have earlier sessions (pre-Mnemosyne install), 
# but post-install dates should show overlap in both stores

# 4. Spot-check known recovered content
session_search(query=\"Obsidian vault\", limit=3)
mnemosyne_recall(query=\"Obsidian vault\", limit=3)
```

**Expected results:**
- LCM: Sessions from May 16 onward (includes pre-Mnemosyne WSL sessions)
- Mnemosyne: Memories from May 18 onward (install date) 
- Overlap: May 18 onward should appear in both stores
- Gaps: May 16-17 may appear in LCM only (expected - pre-Mnemosyne)
- Continuity: No major gaps in daily counts within each store

**Key insight:** True recovery requires both stores to be healthy. Recovering only LCM sessions makes history "findable" but not "usable" for Mnemosyne-powered features like contextual recall and semantic search.
 
## User Preference

- "Recovered sessions should be immediately searchable" — any recovery action must include validation via `session_search`, not just file restoration.
- Disk hygiene: prefer bundled archive format, remove loose file collections after archiving.
- Direct action: "just run them" — no analysis menus, no confirmation loops.
- Frustration signals: empty responses, cut-offs, re-proposing completed work.
- **Cross-store verification**: After any recovery, verify both LCM and Mnemosyne show continuous, overlapping coverage to ensure no gaps in historical record.
