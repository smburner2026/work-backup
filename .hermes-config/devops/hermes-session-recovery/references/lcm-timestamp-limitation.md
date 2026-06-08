# LCM Import Timestamp Limitation — 2026-06-08

## Discovery

Archive `.json.gz` session files only store `session_start` at the session level, NOT per-message timestamps. The import script assigns `session_start` to ALL messages in a session.

## Impact

- `session_search` by date range is **imprecise** for recovered sessions
- FTS5 topic/content search works correctly
- All messages in an imported session share the same timestamp

## What Works

- `session_search(query="topic")` — FTS5 text search ✓
- `session_search(query="WSL")` — finds recovered sessions ✓
- Date-range filtering — **UNRELIABLE** for recovered sessions ✗

## Source Data Format

Messages in archive `.json.gz` files do NOT have individual `timestamp` fields. The import assigned `session_start` to all messages.