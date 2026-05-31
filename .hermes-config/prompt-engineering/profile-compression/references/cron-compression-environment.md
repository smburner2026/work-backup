# Cron Environment — Compression Operational Pattern

When this skill is loaded by the `nightly-self-improvement` cron (06:00 UTC daily), the agent has **different tool availability** than in a user-facing session. This reference documents the fallback paths.

## Environment Constraints

| Tool | In cron | Fallback |
|------|---------|----------|
| `memory()` | ❌ Disabled | Write directly to `~/.hermes/memories/USER.md` and `~/.hermes/memories/MEMORY.md` |
| `clarify()` | ❌ Disabled | No user present — make autonomous decisions with stated assumptions |
| `delegate_task()` | ❌ Disabled | Execute all work in the same context |
| `terminal()`, `read_file()`, `patch()` | ✅ Available | Normal operation |
| `session_search()` | ❌ Disabled | Query `~/.hermes/state.db` via sqlite3 (FTS5 `messages` table) — see Phase 1 |

## Workflow

### Phase 1 — Session Review → Save Insights

1. Query `~/.hermes/state.db` via sqlite3 for recent sessions and user messages:

   ```bash
   # Sessions active in the last 24h, sorted by most recent
   sqlite3 ~/.hermes/state.db \
     \"SELECT session_id, datetime(MAX(timestamp),'unixepoch') as last_active,
             COUNT(*) as msgs
      FROM messages
      WHERE timestamp > $(($(date +%s) - 86400))
      GROUP BY session_id ORDER BY last_active DESC LIMIT 20;\"

   # User messages from the last 24h (exclude cron/worker sessions)
   sqlite3 ~/.hermes/state.db \
     \"SELECT datetime(timestamp,'unixepoch'), session_id, substr(content,1,300)
      FROM messages
      WHERE role='user'
        AND timestamp > $(($(date +%s) - 86400))
        AND session_id NOT LIKE 'cron_%'
        AND length(content) > 10
      ORDER BY timestamp DESC;\"

   # Full-text search across all messages (replaces session_search)
   # Uses FTS5 virtual table — MATCH supports standard FTS5 query syntax
   sqlite3 ~/.hermes/state.db \
     \"SELECT datetime(timestamp,'unixepoch'), session_id, role, substr(content,1,200)
      FROM messages_fts
      WHERE messages_fts MATCH 'searchterm'
      ORDER BY rank LIMIT 10;\"
   ```

2. Review results to extract: user corrections, new preferences, environment facts, workflow patterns.
3. **When memory tool is unavailable:** write directly to USER.md or MEMORY.md files instead:
   - **User-preference findings** → append to `~/.hermes/memories/USER.md` (compressed DSL, §-delimited)
   - **Operational/environment findings** → append to `~/.hermes/memories/MEMORY.md` (compressed DSL, §-delimited)
4. Still apply compression techniques (token packing, DSL encoding, semantic normalization) even when writing directly — don't write verbose prose and expect a future pass to compress it.
5. **Verify writes** by reading the file back after writing. Confirm the entry exists at the expected position.

### Phase 2 — Apply Compression to USER.md and MEMORY.md

1. Read both files in full.
2. Follow the same compression methodology as any other pass:
   - **Step 0 — Verify before compressing:** search sessions for operating principles, cross-reference against SOUL.md's Layer 0-2 (Operating Charter, Hermes Architecture, Karpathy Principles). Don't compress out identity to make room for activity.
   - **Structural compression** — group related facts under domain labels
   - **Token packing** — abbreviate: `→` for arrows, `|` for alternatives, `()` for qualifiers
   - **DSL encoding** — assignment-style syntax throughout
3. **Update stale entries** — don't just compress. Check whether facts have changed since they were written (e.g. a plugin that was "broken" may now be "fixed").

### Phase 3 — Audit

1. Run the self-audit script: `bash ~/.hermes/scripts/self-audit.sh`
2. Note the output but do NOT take action (user may want to control when updates happen)
3. If `hermes` CLI reports 34+ commits behind, note the exact count

## Pitfalls

- **Don't compress activity into identity.** The most common compression failure: removing "user's operating principle" to make room for "plugin version" or "specific tool path." The operating principle won't be discovered again; the version number can be found with `tool --version` or `session_search`. When in doubt, keep the principle and drop the version.
- **Don't write what you can't verify.** Without `memory()`, you can't atomically persist facts. Always write directly to the file and read it back to confirm. A write_file call that succeeds but produces garbage = fact lost silently.
- **Don't add noise.** If the session review found nothing new, don't add entries. Adding "nothing new" as a fact is worse than not adding — it wastes context and teaches the model that empty updates are normal.
- **USER.md has a ~1,375-char limit** (Hermes memory size). Don't exceed it. If compressing won't fit the new fact, drop activity-level entries (tool versions, platform details, transient project state) before identity-level ones (operating principles, voice rules, user preferences).
- **The self-audit exits 0 silently when nothing to report.** A blank audit isn't a failure — it means everything's up to date. Don't flag it as an error.

## Example: This cron run (2026-05-27)

**Findings saved to USER.md:**
- Speaking/writing insight added (identity-level user self-discovery)
- Pi entry compressed from multi-line version/path/auth → `Pi: default coding agent (one-shot|bg).`
- Domain line compressed: `Bioscience bench, Philosophy` → `Bio bench/Phil`

**Findings saved to MEMORY.md:**
- DOGA entry updated from "has NEVER loaded" (stale) to "FIXED 2026-05-26" with fix details

**Self-audit result:**
- Hermes 34 commits behind (v2026.5.16), hermes-lcm 4 behind (v0.12.0), mnemosyne 3.0.0→3.1.0
- All other checks passed
