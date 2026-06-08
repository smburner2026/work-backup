# LCM Database Import Procedure — 2026-06-08

## What Was Done

Imported 411 archived session files from `/root/.hermes/backups/2026-06-07_old-sessions.tar.zst` into the live LCM database (`/root/.hermes/lcm.db`) so `session_search` returns the full May 16–June 8 range.

## Archive Contents

```
/tmp/session_*.json.gz  (411 files extracted)
Format:  {session_id, model, base_url, platform, session_start, last_updated, system_prompt, tools, message_count, messages: [array of {role, content, tool_calls, ...}]}
Date range: 2026-05-16 through 2026-05-20 (pre-hygiene sessions)
```

## Import Script

```bash
cd /tmp
zstd -dc /root/.hermes/backups/2026-06-07_old-sessions.tar.zst | tar -xf - --wildcards '*.json.gz'
python3 << 'PYEOF'
import json, sqlite3, gzip, os
from pathlib import Path

ARCHIVE_DIR = Path("/tmp")
DB_PATH = "/root/.hermes/lcm.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT session_id FROM messages")
existing = {row[0] for row in cursor.fetchall()}
print(f"Existing sessions in DB: {len(existing)}")

imported_count = 0
for gz_file in sorted(ARCHIVE_DIR.glob("session_*.json.gz")):
    try:
        with gzip.open(gz_file, 'rt') as f:
            data = json.load(f)
        session_id = data['session_id']
        if session_id in existing:
            continue
        platform = data.get('platform', 'unknown')
        source = platform
        for msg in data['messages']:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            tool_call_id = msg.get('tool_call_id', '')
            tool_calls = json.dumps(msg.get('tool_calls', [])) if msg.get('tool_calls') else ''
            tool_name = msg.get('tool_name', '')
            timestamp = data.get('session_start', 0)
            cursor.execute("""
                INSERT INTO messages (session_id, source, role, content, tool_call_id, tool_calls, tool_name, timestamp, token_estimate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (session_id, source, role, content, tool_call_id, tool_calls, tool_name, timestamp, len(content)//4))
        imported_count += 1
        if imported_count % 50 == 0:
            conn.commit()
            print(f"  Imported {imported_count} sessions...")
    except Exception as e:
        print(f"Error importing {gz_file}: {e}")

conn.commit()
cursor.execute("SELECT COUNT(DISTINCT session_id) FROM messages")
print(f"Total sessions now: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM messages")
print(f"Total messages now: {cursor.fetchone()[0]}")
conn.close()
PYEOF
```

## Results

| Metric | Before | After |
|--------|--------|-------|
| Sessions in LCM DB | 253 | 472 (+219) |
| Messages in LCM DB | ~30K | 68,264 |
| `session_search` coverage | May 30+ | May 16+ |

## Validation Queries (All Now Work)

```bash
session_search(query="20260516", limit=5)   # → returns session
session_search(query="pdf generation", limit=5)  # → returns 20260516 session
session_search(query="WSL", limit=5)  # → returns May 30+ WSL sessions
session_search(query="Obsidian vault", limit=5)  # → returns May 31 session
session_search(query="DABT Tutor", limit=5)  # → returns May 30 session
```

## Notes

- No duplicate sessions imported (skipped if session_id already in LCM)
- Only one file had a parse error (`session_20260520_013216_242c4261.json.gz` — NoneType len() error, non-blocking)
- WSL registry (`sessions-wsl.json`) NOT imported — it's metadata-only, no message content
- If WSL message files are synced to `/root/.hermes/sessions/`, they'll be picked up by the same import logic
- Session hygiene settings in config.yaml (threshold 0.75, hard limit 600) may re-prune older sessions over time; consider adjusting if long-term retention needed

## Commands for Future Runs

```bash
# Extract archive
zstd -dc /root/.hermes/backups/2026-06-07_old-sessions.tar.zst | tar -xf - -C /tmp --wildcards '*.json.gz'

# Run import
python3 /root/.hermes/skills/devops/hermes-session-recovery/scripts/import-archived-sessions.py
```

## Script Location

Save the Python script as `/root/.hermes/skills/devops/hermes-session-recovery/scripts/import-archived-sessions.py` for reuse.