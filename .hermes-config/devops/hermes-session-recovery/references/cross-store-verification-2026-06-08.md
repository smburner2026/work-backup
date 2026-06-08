# Cross-Store Verification Pattern (2026-06-08)

After any DB recovery or merge operation, verify all three stores are consistent and live.

## Quick Verification Checklist

```bash
# 1. LCM - session_search returns results from recovered period
session_search(query="<known topic from recovered period>", limit=5)
sqlite3 ~/.hermes/lcm.db "SELECT COUNT(DISTINCT session_id), COUNT(*) FROM messages;"

# 2. Mnemosyne - recall returns results from recovered period
mnemosyne_recall(query="<known fact from recovered period>", limit=5)
sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "SELECT COUNT(*) FROM working_memory;"

# 3. Git backup is current
cd /root/work && git log --oneline -3 && git status --short

# 4. Local backups exist
ls -lh ~/.hermes/backups/mnemosyne/ ~/.hermes/backups/lcm/ ~/.hermes/backups/dbs/
```

## Recovery Sources Reference

| Source | Location | Contains | Searchable via |
|--------|----------|----------|----------------|
| LCM DB | `~/.hermes/lcm.db` | 664 sessions, 90K+ messages | `session_search()` |
| Mnemosyne | `~/.hermes/mnemosyne/data/mnemosyne.db` | 5,240 working memories, 2,196 facts, 211 episodic | `mnemosyne_recall()` |
| Git backup | `/root/work` (GitHub) | Config/skills + session `.gz` archives | `git log`, file search |
| Local backups | `~/.hermes/backups/` | All DBs, daily/weekly snapshots | `ls`, `sqlite3` |

## What Was Recovered (2026-06-08)

- **192 sessions** from archive tar → imported into LCM (May 16-20 gap closed)
- **3,898 working memories** from corrupt DB → merged into Mnemosyne (May 18 - June 6 gap closed)
- **1,771 facts** from corrupt DB → merged into Mnemosyne
- **204 episodic memories** from corrupt DB → merged into Mnemosyne
- **125 memoria_instructions** from corrupt DB → merged into Mnemosyne

## Known Timestamp Issue

LCM timestamps for archived sessions use `session_start` for ALL messages (archive format doesn't store per-message timestamps). Use `SUBSTR(session_id,1,8)` for date grouping instead of timestamp.

## Backup Schedule

| Data | Local retention | Git | Cloud |
|------|----------------|-----|-------|
| Config/skills | Latest only | ∞ (git history) | Not yet (B2 planned) |
| Sessions .jsonl | 7 days live → .gz archive | ∞ (work-backup.sh) | Not yet |
| Mnemosyne DB | 7 daily snapshots | Weekly (Sundays) | Not yet |
| LCM DB | 4 weekly snapshots | Weekly (Sundays) | Not yet |
| Other DBs | 2 weekly snapshots | Weekly (Sundays) | Not yet |