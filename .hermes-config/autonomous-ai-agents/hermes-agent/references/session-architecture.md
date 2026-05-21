# Session Architecture

Hermes stores all session data in a single SQLite database at `~/.hermes/state.db` (or the profile-equivalent under `~/.hermes/profiles/<name>/`). Two FTS5 virtual tables provide full-text search. The design prioritises concurrent access from multiple processes (CLI, gateway, worktree agents) without corruption.

## Database

`hermes_state.py` — class `SessionDB`.

- **WAL journal mode** for concurrent readers + one writer. Falls back to `journal_mode=DELETE` on NFS/SMB/FUSE filesystems where WAL locking protocol doesn't work.
- **Write contention handling:** SQLite timeout set to 1s, then application-level retry with random jitter (20-150ms, up to 15 attempts). This avoids the convoy effect that SQLite's deterministic retry schedule produces under high contention from multiple Hermes processes.
- **Schema reconciliation:** columns are added declaratively — `SCHEMA_SQL` is the source of truth, `_reconcile_columns()` diffs live tables against it on startup and ADD COLUMN any that are missing. No more version-gated migration blocks for column additions.

### Key Tables

**`sessions`** — one row per session.
- `id` TEXT PRIMARY KEY (formatted as `YYYYMMDD_HHMMSS_<6hex>`)
- `source` — platform tag: `cli`, `telegram`, `discord`, etc. Third-party integrations use `"tool"` to self-hide.
- `parent_session_id` — links compression continuation/delegation/branch children to their parent. NULL for root sessions.
- `model`, `model_config`, `system_prompt` — model and config snapshot at session creation.
- `title` — user-assigned or auto-generated. On compression splits, auto-numbered (e.g. "Fix auth bug (2)").
- `started_at`, `ended_at`, `end_reason` — lifecycle. `end_reason='compression'` means context was compressed and a child session continues the conversation. `end_reason='branched'` means the child is an explicit /branch fork.
- `message_count`, `tool_call_count`, various `*_tokens` columns, `estimated_cost_usd` — usage tracking.

**`messages`** — one row per turn.
- Linked to sessions via `session_id` (FK).
- `role`: `user`, `assistant`, `tool`, `system`.
- `content`: the message text (nullable — tool calls may have NULL content).
- `tool_calls`: JSON array of tool call objects (assistant messages only).
- `tool_name`, `tool_call_id`: for tool result messages.
- `timestamp`: Unix epoch float.
- Various reasoning/codex-specific columns for chain-of-thought storage.

## FTS5 Full-Text Search

Two virtual tables, both auto-synced via INSERT/UPDATE/DELETE triggers on `messages`:

**`messages_fts`** — default unicode61 tokenizer. Supports standard FTS5 query syntax:
- Keywords: `docker deployment`
- Phrases: `"exact phrase"`
- Boolean: `docker OR kubernetes`, `python NOT java`
- Prefix: `deploy*`

**`messages_fts_trigram`** — trigram tokenizer. Handles CJK substring search where the unicode61 tokenizer fails (it splits CJK into individual characters, breaking phrase matching). Also handles any script's substring search.

Query routing in `SessionDB.search_messages()`:
- CJK queries with 3+ CJK characters per token → trigram FTS5 table
- CJK queries with <3 CJK chars → LIKE fallback (trigram needs >=3 CJK chars = 9 UTF-8 bytes to match)
- Non-CJK queries → standard `messages_fts` table

The `session_search` tool (Python agent's cross-session recall) wraps this and adds:
1. FTS5 query → ranked message matches (BM25 via SQLite's `rank`)
2. Walk parent_session_id chain to resolve child/delegation sessions to root
3. Group by resolved session, take top N (max 5)
4. Load conversation, truncate to ~100K chars centered on match positions
5. Summarize each session via auxiliary LLM with focus on query terms
6. Return structured summaries

Hidden sources (`source='tool'`) are excluded by default. Current session lineage is excluded.

## Compression Chains

When the conversation exceeds ~50% of the model's context window (configurable via `compression.threshold` in config.yaml), the `ContextCompressor` (`agent/context_compressor.py`) fires mid-conversation:

1. **Prune old tool results** (cheap, no LLM call) — replace long tool outputs with informative one-line summaries like `[terminal] ran 'npm test' -> exit 0, 47 lines output`.
2. **Protect head** (first N messages, default 3) — system prompt + first exchange.
3. **Protect tail** by token budget (~20K tokens default) — most recent turns that still contain the actual task context.
4. **Summarize middle** via auxiliary LLM — structured summary template with Resolved/Pending question tracking, "Remaining Work" section (not "Next Steps" — to avoid being read as active instructions).
5. **Split session**: end current session with `end_reason='compression'`, create child session linked via `parent_session_id`, propagate title with auto-numbering, reset flush cursor.

The chain looks like:
```
session_A -> (compression) -> session_B -> (compression) -> session_C
```
`/resume` automatically walks forward to find the tip session that has actual messages.

**Anti-thrashing:** if the last 2 compressions each saved <10%, compression is skipped with a warning suggesting `/new` or `/compress <topic>`.

**Compression count warning:** after 2+ compressions in one session chain, users see: "Session compressed N times — accuracy may degrade. Consider /new to start fresh."

## Pruning

Three tiers of cleanup:

**`hermes sessions prune --older-than N`** (CLI command)
- Deletes only *ended* sessions (`ended_at IS NOT NULL`) older than N days (default 90).
- Child sessions of pruned parents are orphaned (parent_session_id set to NULL), not cascade-deleted.
- Optional `--source` filter to target one platform.
- On-disk transcript files (.json/.jsonl/request_dump_*) also cleaned up.

**`prune_empty_ghost_sessions()`** (automatic)
- Removes TUI sessions with no messages, no title, and older than 24 hours.
- These are "crashes" — the TUI creates a session row on open but if closed before any conversation, it's a ghost.

**`finalize_orphaned_compression_sessions()`** (automatic)
- Marks compression children that were never properly finalized (api_call_count=0, stuck mid-compression) with `end_reason='orphaned_compression'` after 7 days.
- This makes them eligible for the next prune pass.

## Session Listing & Browsing

`list_sessions_rich()` is the main listing method used by `hermes sessions list` and `hermes sessions browse`.

- By default, hides child sessions (those with `parent_session_id`) UNLESS the child is a branch (`end_reason='branched'` AND `started_at >= parent.ended_at`).
- Hidden source `"tool"` excluded by default unless `--source` is explicitly provided.
- Compression chains are projected forward: the root session's metadata (title, last_active, message_count) reflects the live tip, so a compressed conversation appears as one entry.
- `order_by_last_active=True` uses a recursive CTE to compute effective last_active across compression chains at SQL level, so LIMIT/OFFSET still apply efficiently.

## Noise Management Summary

| Concern | Mechanism |
|---------|-----------|
| One-off questions with few messages | FTS5 ranking favours richer sessions; LIMIT 5 on search results |
| Crashed/aborted sessions | Ghost pruning after 24h; orphaned compression after 7d |
| Delegation/subagent sessions | Hidden from listing (have parent_session_id); resolved to root in search |
| Third-party tool sessions | Hidden (source='tool') from listing and search |
| Compression chain bloat | Long-lived chains can accumulate rows that can't be pruned while the tip is active. Workaround: end the chain deliberately and start fresh. |
| Current session noise in search | Current session lineage excluded from results |
