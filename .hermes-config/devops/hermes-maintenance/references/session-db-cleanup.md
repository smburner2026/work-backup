# Session DB Cleanup — State.db Pruning Methodology

## Architecture

The session store lives at `~/.hermes/state.db` (SQLite). Key tables:
- `sessions` — one row per conversation (id, source, title, message_count, timestamps, tokens, costs)
- `messages` — all messages (content, tool_calls, reasoning, role, timestamps)
- `messages_fts` — FTS5 keyword/phrase index
- `messages_fts_trigram` — FTS5 trigram (3-char substring) index — **the bloat source**

JSONL files at `~/.hermes/sessions/*.jsonl` are secondary (17MB vs 550MB+ DB). Ignore them for pruning.

## Schema Reference

```sql
-- Key columns in sessions
id TEXT PRIMARY KEY,
source TEXT NOT NULL,          -- telegram, discord, cli, cron, tui, api_server
title TEXT,
message_count INTEGER DEFAULT 0,
started_at REAL NOT NULL,      -- Unix timestamp
ended_at REAL,

-- Key columns in messages
id INTEGER PRIMARY KEY,
session_id TEXT NOT NULL REFERENCES sessions(id),
role TEXT NOT NULL,
content TEXT,
tool_call_id TEXT,
tool_calls TEXT,
tool_name TEXT,
timestamp REAL NOT NULL,
token_count INTEGER,
finish_reason TEXT,
reasoning TEXT,
reasoning_content TEXT,
```

## Size Diagnosis

Before pruning, measure what's consuming space:

```sql
-- Overall size
SELECT COUNT(*) as sessions, SUM(message_count) as messages,
  ROUND(page_count * page_size / 1048576.0, 1) as db_size_mb
FROM sessions, pragma_page_count, pragma_page_size;

-- Breakdown by component
SELECT 'messages content' as comp, ROUND(SUM(LENGTH(content))/1048576.0, 1) as mb FROM messages;
SELECT 'messages tool_calls', ROUND(SUM(LENGTH(COALESCE(tool_calls,'')))/1048576.0, 1) FROM messages;
SELECT 'messages reasoning', ROUND(SUM(LENGTH(COALESCE(reasoning,''))+LENGTH(COALESCE(reasoning_content,'')))/1048576.0, 1) FROM messages;
SELECT 'system prompts', ROUND(SUM(LENGTH(COALESCE(system_prompt,'')))/1048576.0, 1) FROM sessions;

-- FTS index sizes (via dbstat or estimates)
-- messages_fts_trigram is typically 3-8x the actual data size
```

## Quality-Based Sorting

Sort sessions by message count to identify tiers:

```sql
SELECT
  source,
  CASE
    WHEN message_count < 3 THEN 'empty'
    WHEN message_count < 10 THEN 'short'
    WHEN message_count < 50 THEN 'medium'
    WHEN message_count < 200 THEN 'substantial'
    ELSE 'deep'
  END as quality,
  COUNT(*) as sessions,
  SUM(message_count) as total_msgs
FROM sessions
GROUP BY source, quality
ORDER BY source, total_msgs DESC;
```

## DABT Session Protection

When pruning sessions that contain project-critical work (DABT, trading, research), protect them explicitly:

```sql
-- Create protection list (search both title AND message content)
CREATE TEMPORARY TABLE protected AS
SELECT DISTINCT s.id
FROM sessions s
JOIN messages m ON m.session_id = s.id
WHERE (
  s.title LIKE '%dabt%' OR s.title LIKE '%DABT%'
  OR m.content LIKE '%dabt%' OR m.content LIKE '%DABT%'
  -- Add other project keywords as needed
)
AND m.role = 'user';
```

**Pitfall:** Title-only search misses most sessions. The title is often empty or auto-generated. Search message content for the actual topic.

## Pruning Strategy

### Tier 1: Safe deletes (low risk)
- Empty sessions (< 3 messages) — dead weight
- Cron sessions older than 7 days — ephemeral output
- Short cron (3-9 msgs) older than 7 days
- CLI/TUI sessions older than 14 days — work artifacts on disk

### Tier 2: Moderate deletes
- Medium cron (10-49 msgs) older than 7 days
- Short discord/telegram (3-9 msgs) older than 7 days, not project-related

### Tier 3: Aggressive deletes (VPS constraint)
- Everything older than 7 days — only viable on 2GB VPS

### Execution

```sql
-- 1. Protect critical sessions
CREATE TEMPORARY TABLE protected AS
SELECT DISTINCT s.id FROM sessions s
JOIN messages m ON m.session_id = s.id
WHERE (s.title LIKE '%dabt%' OR m.content LIKE '%dabt%')
AND m.role = 'user';

-- 2. Identify deletable sessions
CREATE TEMPORARY TABLE to_delete AS
SELECT id FROM sessions WHERE message_count < 3
AND id NOT IN (SELECT id FROM protected)
UNION ALL
SELECT id FROM sessions WHERE source='cron' AND julianday('now') - julianday(started_at, 'unixepoch') > 7
UNION ALL
-- ... add more tiers as needed

-- 3. Delete messages first (FK dependency)
DELETE FROM messages WHERE session_id IN (SELECT id FROM to_delete);

-- 4. Delete sessions
DELETE FROM sessions WHERE id IN (SELECT id FROM to_delete);

-- 5. Rebuild FTS + reclaim space
INSERT INTO messages_fts(messages_fts) VALUES('rebuild');
VACUUM;
```

**Critical:** Always DELETE messages before sessions (FK constraint). Always rebuild FTS after deleting (orphaned index entries). Always VACUUM after FTS rebuild.

## FTS Trigram Index Bloat

The `messages_fts_trigram` table indexes every 3-character substring for fuzzy/partial matching. On a 2GB VPS with ~55K messages, the trigram index consumed **490MB** (90% of the 549MB DB). Actual data was only 59MB.

### Impact
- DB appears 7-10x larger than actual content
- VACUUM helps marginally (FTS pages are not compacted by normal VACUUM)
- On constrained VPS, this steals RAM from the running process

### Dropping trigram
The trigram index can be dropped to save space. Tradeoff:
- **Kept:** Substring matching works ("dab" finds "DABT")
- **Dropped:** Only keyword/phrase search (must use full words)

### How to drop (if user approves)
```sql
-- Drop trigram table and its triggers
DROP TABLE IF EXISTS messages_fts_trigram;
DROP TRIGGER IF EXISTS messages_fts_trigram_insert;
DROP TRIGGER IF EXISTS messages_fts_trigram_delete;
DROP TRIGGER IF EXISTS messages_fts_trigram_update;

-- Rebuild regular FTS (still works)
INSERT INTO messages_fts(messages_fts) VALUES('rebuild');
VACUUM;
```

### Session search impact
Hermes's `session_search` tool uses both FTS tables. After dropping trigram:
- Exact word/phrase search still works
- Partial/substring search fails silently (returns no results instead of fuzzy matches)
- Most practical searches (project names, topics, keywords) are unaffected

### State snapshots
Old state-snapshots (`~/.hermes/state-snapshots/`) contain copies of the DB. If the live DB was cleaned but snapshots remain, the old bloat persists. Delete stale snapshots:
```bash
ls -la ~/.hermes/state-snapshots/
# Keep only the most recent snapshot, delete older ones
rm -rf ~/.hermes/state-snapshots/2026MMDD-*/
```

## Post-Cleanup Verification

```sql
-- Confirm remaining sessions
SELECT source, COUNT(*) as sessions, SUM(message_count) as msgs
FROM sessions GROUP BY source ORDER BY sessions DESC;

-- Confirm DB size
SELECT ROUND(page_count * page_size / 1048576.0, 1) as db_size_mb
FROM pragma_page_count, pragma_page_size;
```
