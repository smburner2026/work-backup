# Hermes DB Secret Scrubbing — Incident Response

When an API key, token, or password is discovered in conversation history, it must be surgically removed from every Hermes internal database to prevent secondary exposure. One key pasted into chat spreads through 3+ data stores within minutes.

## Detection

Find leaked secrets across all surfaces:

```bash
# State DB (all session messages)
sqlite3 /root/.hermes/state.db "SELECT DISTINCT role, COUNT(*) FROM messages WHERE content LIKE '%sk-or-%' GROUP BY role;"

# LCM DB (compressed conversation history)
sqlite3 /root/.hermes/lcm.db "SELECT COUNT(*) FROM messages WHERE content LIKE '%sk-or-%';"

# LCM summary nodes (compressed summaries)
sqlite3 /root/.hermes/lcm.db "SELECT COUNT(*) FROM summary_nodes WHERE summary LIKE '%sk-or-%';"

# Kanban DB (task descriptions might reference keys)
sqlite3 /root/.hermes/kanban.db "SELECT COUNT(*) FROM tasks WHERE title LIKE '%sk-or-%' OR body LIKE '%sk-or-%';"

# State snapshots (pre-update backups of state.db)
find ~/.hermes/state-snapshots/ -name "state.db" -exec sqlite3 {} "SELECT COUNT(*) FROM messages WHERE content LIKE '%sk-or-%';" \;

# Cron output files
grep -rn 'sk-or\|sk-ant\|HETZNER_API_TOKEN\|BWS_ACCESS_TOKEN' ~/.hermes/cron/output/ 2>/dev/null

# Git repos (committed secrets — check backup diff commits)
cd /root/work && git log -p --all -S 'sk-or-' --not --glob='refs/remotes/*'
```

**Patterns to search for:**
- `sk-or-*` — OpenRouter keys (format: `sk-or-v1-<48hex>`)
- `sk-ant-*` — Anthropic keys
- `sk-proj-*` — OpenAI project keys
- `hf_*` — HuggingFace tokens
- `HETZNER*` / `BWS_ACCESS_TOKEN` / env-var names that carry secrets
- `Authorization: Bearer *`
- Any key-specific env var name

## Scrub Procedure

**Preferred approach: UPDATE + replace() over DELETE.** Deletion breaks auto-increment sequences, requires VACUUM to reclaim space, and destroys conversation structure. Replacing just the secret with `[REDACTED]` is faster, safer, and preserves everything except the compromised value.

### 1. Scrub from state.db

```bash
# Replace the leaked key with [REDACTED] — preserves message structure
sqlite3 /root/.hermes/state.db \
  "UPDATE messages SET content = replace(content, 'EXPOSED-KEY-VALUE', '[REDACTED]') WHERE content LIKE '%UNIQUE-FRAGMENT%';"

# Rebuild the FTS (full-text search) index so ghost hits don't surface
sqlite3 /root/.hermes/state.db "INSERT INTO messages_fts(messages_fts) VALUES('rebuild');"

# Verify zero remaining occurrences of the actual key
sqlite3 /root/.hermes/state.db "SELECT COUNT(*) FROM messages WHERE content LIKE '%UNIQUE-FRAGMENT%';"
# Returns 0 if successful

# Confirm FTS index no longer carries the key
sqlite3 /root/.hermes/state.db "SELECT COUNT(*) FROM messages_fts WHERE messages_fts MATCH '\"UNIQUE-FRAGMENT\"';"
# Returns 0 if FTS rebuild worked
```

**Why UPDATE over DELETE:**
- Keeps all message IDs intact — no broken foreign keys or sequence gaps
- Doesn't require VACUUM (no page-level reorganization)
- ziplist compression in LCM means most replacements are roughly same-length
- FTS rebuild is the only expensive step (~1-2 seconds per 100MB DB)

Use DELETE only if the entire message must be removed (e.g., it was a blob dump with no recoverable value):
```bash
sqlite3 /root/.hermes/state.db "DELETE FROM messages WHERE id IN (12345, 12346);"
sqlite3 /root/.hermes/state.db "INSERT INTO messages_fts(messages_fts) VALUES('rebuild');"
```

### 2. Scrub from lcm.db (compressed history)

```bash
# Replace (preferred)
sqlite3 /root/.hermes/lcm.db \
  "UPDATE messages SET content = replace(content, 'EXPOSED-KEY-VALUE', '[REDACTED]') WHERE content LIKE '%UNIQUE-FRAGMENT%';"

# Check summary nodes too — column is "summary", not "content"
sqlite3 /root/.hermes/lcm.db "SELECT COUNT(*) FROM summary_nodes WHERE summary LIKE '%UNIQUE-FRAGMENT%';"

# If found, scrub from summary_nodes
sqlite3 /root/.hermes/lcm.db "UPDATE summary_nodes SET summary = replace(summary, 'EXPOSED-KEY-VALUE', '[REDACTED]') WHERE summary LIKE '%UNIQUE-FRAGMENT%';"

# Rebuild both LCM FTS indexes
sqlite3 /root/.hermes/lcm.db "INSERT INTO messages_fts(messages_fts) VALUES('rebuild');"
sqlite3 /root/.hermes/lcm.db "INSERT INTO nodes_fts(nodes_fts) VALUES('rebuild');"

# Verify
sqlite3 /root/.hermes/lcm.db "SELECT COUNT(*) FROM messages WHERE content LIKE '%UNIQUE-FRAGMENT%';"
sqlite3 /root/.hermes/lcm.db "SELECT COUNT(*) FROM messages_fts WHERE messages_fts MATCH '\"UNIQUE-FRAGMENT\"';"
```

### 3. Check kanban.db

```bash
sqlite3 /root/.hermes/kanban.db "SELECT id, title, status FROM tasks WHERE title LIKE '%sk-or-%' OR body LIKE '%sk-or-%';"
# If found, delete or edit the task
```

### 4. Check state snapshots

Each snapshot under `~/.hermes/state-snapshots/` has its own `state.db`:

```bash
for snap in ~/.hermes/state-snapshots/*/; do
  db="$snap/state.db"
  [ -f "$db" ] && sqlite3 "$db" "DELETE FROM messages WHERE content LIKE '%sk-or-v1-XXXXX%'; DELETE FROM messages_fts WHERE content MATCH 'sk-or-';"
done
```

Also check for `auth.json` in snapshots — these can contain OAuth tokens:
```bash
find ~/.hermes/state-snapshots/ -name "auth.json" -exec grep -l 'id_token\|access_token' {} \;
# Delete any that contain live tokens — they are stale snapshots
```

### 5. Check git history for committed secrets

```bash
cd /root/work
git log -p --all -S 'sk-or-v1-XXXXX' --not --glob='refs/remotes/*'
```

If found and the commit is recent/unpushed:
- `git filter-branch` or `git rebase -i` to remove the commit
- Force-push if needed (⚠️ destructive)

If the secret was already redacted (e.g., `api_key: REDACTED` or truncated with `...`) — no action needed. The backup script does redaction before committing.

### 6. Lock file permissions

After scrubbing, ensure all DBs and config files are root-only:
```bash
chmod 600 ~/.hermes/state.db ~/.hermes/lcm.db ~/.hermes/kanban.db
chmod 600 ~/.hermes/config.yaml ~/.hermes/.env
chmod 600 ~/.hermes/logs/*.log
chmod 600 ~/.hermes/profiles/*/config.yaml
find ~/.hermes/state-snapshots/ -type f -exec chmod 600 {} \;
```

## Prevention

### Stop keys from entering conversation history
- **Prefer env vars** — `export NEW_KEY=sk-...` and `/reload` rather than pasting
- **File relay** — write key to `/tmp/key` (0600), use `read_file`, then delete. The key stays in the agent's context but redaction masks it from logs
- **BWS project** — store keys in Bitwarden Secrets Manager. Hermes auto-injects them on startup. No manual pasting needed

### Hermes redaction layer
`redact_secrets: true` in `config.yaml` masks secret-like patterns in ALL tool output. However, it does NOT mask user-pasted content in messages — that's conversation data that my redaction system doesn't filter. The DB scrub is the fallback.

### File deletion pattern
When delivering sensitive files to user: `deliver put <file>` → user downloads → nuke originals immediately. Never leave temp files with key data.

### Cron script auditing
Cron scripts that embed API keys in curl calls (e.g. `curl -H "Authorization: Bearer $KEY"`) can leak keys via process listing (`ps aux`), tool output, or git history. After rotating keys, scan all scripts:

```bash
grep -rn 'curl.*Authorization: Bearer\|curl.*api_key=' ~/.hermes/scripts/ 2>/dev/null
grep -rn 'api_key[=][^$]' ~/.hermes/scripts/*.sh 2>/dev/null
```
Replace hardcoded keys with env-var references sourced from `.env` or BWS. For no-agent watchdog scripts, pass the key via the cron job's environment rather than embedding it in the script body.

## Key files to monitor for secondary copies

| Path | Risk | Action if compromised |
|------|------|----------------------|
| `~/.hermes/state.db` | Session history with keys | Scrub messages + rebuild FTS |
| `~/.hermes/lcm.db` | Compressed conversation history | Scrub messages + summary_nodes + rebuild FTS |
| `~/.hermes/kanban.db` | Task descriptions referencing keys | Delete/modify task |
| `~/.hermes/config.yaml.bak` | Backup config with env-ref keys | Redact or delete (stale backups) |
| `~/.hermes/state-snapshots/*/` | Pre-update DB/cfg snapshots | Scrub each state.db, delete auth.json, check .env for actual keys |
| `~/.hermes/cron/output/*/` | Saved cron job reports | Check for key text, delete if found |
| `~/.hermes/logs/*.log` | Agent/gateway logs | `redact_secrets` mitigates; lock to 0600 |
| `~/.gbrain/brain.pglite.bak` | G-Brain PGLite backup | DB directory — impractical to scrub (PostgreSQL) |
| `~/.ssh/*` | SSH keys | Already protected (0600), rotate if exposed |
