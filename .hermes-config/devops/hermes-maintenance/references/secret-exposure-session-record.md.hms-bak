# Secret Exposure Response — Worked Example

> Trigger: User asked "are my API keys vulnerable?"
> Real session with a production Hermes instance.

This is a concrete walkthrough of the Secret Exposure Audit procedure (main SKILL.md §Secret Exposure Audit). It shows the specific findings, commands that worked, and gotchas that fired during an actual audit.

---

## Phase 1 — Initial Permission Check

**Commands:**
```bash
ls -la /root/.hermes/config.yaml          # → 0600 ✅
ls -la /root/.hermes/state.db             # → 0644 ⚠️ world-readable
ls -la /root/.hermes/lcm.db               # → 0644 ⚠️ world-readable
ls -la /root/.hermes/kanban.db            # → 0644 ⚠️ world-readable
ls -la /root/.hermes/response_store.db    # → 0600 ✅
ls -la /root/.hermes/profiles/mike/config.yaml  # → 0644 ⚠️
ls -la /root/.hermes/.env                 # → 0600 ✅
ls -la /root/.hermes/logs/                # → 0644 on all .log files ⚠️
```

**Gotchas that fired:**
1. **DB owner UID mismatch** — `state.db`, `lcm.db`, `kanban.db` owned by UID 1000 (nonexistent user), running as root. The files were created in a different user context than where Hermes runs. `chmod 600` fixes access, but `chown root` may also be needed for clean ownership.
2. **DB files are NOT in `~/.hermes/` by default** — the check assumes default paths. If Hermes runs from `/usr/local/lib/hermes-agent/` with data at `~/.hermes/`, those are the paths to check. Don't scan the entire filesystem.
3. **The `.env` was a template, not actual keys** — its content started with comments ("Copy this file..."). This is safe. The actual keys are in environment variables.
4. **There was another user on the system** (`/home/vthen`) — world-readable files on a multi-user machine is a real risk, not theoretical.

**Remediation:**
```bash
chmod 600 /root/.hermes/state.db /root/.hermes/lcm.db /root/.hermes/kanban.db
chmod 600 /root/.hermes/logs/*.log
chmod 600 /root/.hermes/profiles/mike/config.yaml
```

---

## Phase 2 — Session DB Key Scan

**Search pattern:**
```bash
sqlite3 /root/.hermes/state.db "SELECT COUNT(*) FROM messages WHERE content LIKE '%sk-or-%';"
# → returned 1,071 (includes env var references and actual keys)
```

**Gotchas:**
1. **LIKE uses `%` not `*`** — common SQL pattern confusion. `%` is the wildcard in SQLite LIKE.
2. **`state.db` can be locked** — Hermes gateway holds a WAL-mode lock on `state.db`. If deletion hangs, kill the gateway/TUI processes first.
3. **`session_search` still finds deleted keys after SQL DELETE** — FTS5 shadow tables are NOT automatically synced when `messages` rows are deleted. You MUST rebuild the FTS index: `INSERT INTO messages_fts(messages_fts) VALUES('rebuild');`
4. **lcm.db `summary_nodes` has column `summary` not `content`** — a common trap. Check with `PRAGMA table_info(summary_nodes)` first.
5. **`hf_%` pattern catches HuggingFace tokens** — many real values start with `hf_`. Sample first before bulk-deleting (some matches may be legit env var names).

**Sample check (critical before bulk delete):**
```bash
sqlite3 ~/.hermes/state.db \
  "SELECT substr(content, 1, 200) FROM messages WHERE content LIKE '%sk-or-%' LIMIT 5;"
```

---

## Phase 2b — State-Snapshot Directory (Most Overlooked Risk)

This is the biggest gap in most audit procedures. **Hermes creates pre-update state snapshots** that contain copies of everything, including the session DB.

```bash
ls -la /root/.hermes/state-snapshots/
# → 20260530-004741-pre-update/
ls -la /root/.hermes/state-snapshots/20260530-004741-pre-update/
# Contains: config.yaml, .env, state.db, auth.json, channel_directory.json, ...
```

**Findings:**
- `auth.json` — contained an xAI OAuth `id_token` (live bearer token) **→ DELETE IMMEDIATELY**
- `state.db` (500MB) — had 34 messages with API key patterns that were already scrubbed from the live DB

**Remediation:**
```bash
# 1. Delete the bearer token file
rm /root/.hermes/state-snapshots/20260530-004741-pre-update/auth.json

# 2. Scrub keys from the snapshot DB (same procedure as live)
sqlite3 /root/.hermes/state-snapshots/20260530-004741-pre-update/state.db \
  "DELETE FROM messages WHERE content LIKE '%sk-or-%' OR content LIKE '%sk-ant-%' OR content LIKE '%HETZNER%';"
sqlite3 /root/.hermes/state-snapshots/20260530-004741-pre-update/state.db \
  "INSERT INTO messages_fts(messages_fts) VALUES('rebuild');"
```

> **Permanent fix:** Consider disabling pre-update snapshots if you don't use them for rollback. Or configure retention to keep only the last N.

---

## Phase 3 — Git History Scan

**Commands that worked:**
```bash
# Find repos
find /root -maxdepth 4 -name ".git" -type d | sed 's|/.git||'

# Check backup commits for config files
cd /root/work
git log --all --name-only -- '*.yaml' '*.yml' '*.env' '*.json' | grep -iE 'config|env|auth|key|token|secret'

# Check specific configs for actual key values
git show <commit-hash>:config.yaml | grep 'api_key'
```

**Gotchas:**
1. **Pre-commit redaction is better than post-hoc cleanup** — the `work-backup.sh` script in this setup had a sed command to replace `api_key: <value>` with `api_key: REDACTED` before committing. This is the right approach. If a backup commit has actual keys, rotate at source — git history rewrite is high-risk.
2. **Partial key prefixes in commit messages are low risk** — `sk-or-v1-ce5...` with literal `...` truncation isn't usable. The key prefix alone is 7 hex chars after `sk-or-v1-`, not enough to authenticate.
3. **`.env` and `auth.json` should be gitignored** — verify they aren't in the repo. If they are, treat as critical leak.

---

## Phase 4 — Post-Audit User Actions

After cleaning local storage, the user still needs to rotate keys at the source:

1. **OpenRouter key** — `https://openrouter.ai/settings/keys` → delete old, create new
2. **Hetzner API token** — `https://console.hetzner.cloud` → Project → Security → API Tokens → delete + generate
3. **BWS access token** — `https://vault.bitwarden.com` → Organization → Secrets Manager → Machine Accounts → revoke + create new

The session DB cleanup only prevents further exfiltration from local storage. If the keys were in a world-readable DB on a multi-user system, assume they were scraped and rotate immediately.

---

## Cleanup Aftermath

- `self-audit.sh` deleted (cron job was removed as redundant)
- `config.yaml.bak` deleted (was only env var refs, but stale)
- `bambam-vwap-bands.pine.bak` deleted (trading indicator backup)
- **857 `.hms-bak` files deleted** — these were Hermes auto-backup snapshots scattered across the filesystem. They didn't contain API keys but consumed space. Bulk-remove: `find /root -name "*.hms-bak" -type f -delete`
- **Cron job removed** — `nightly-self-audit` (08:00 daily, script-only watchdog) was redundant with the LLM-driven self-improvement job

---

## Prevention

1. **`redact_secrets: true`** in config.yaml masks keys in tool output. This catches new leaks before they reach logs/DB.
2. **Set all DBs to 0600** on first install — make it a checklist step.
3. **Never paste an API key into chat** — use a file relay (write to `/tmp/scratch.key`, have the agent read it, delete after) or set env var directly.
4. **Add a post-install cron** that checks file permissions weekly and alerts if any sensitive file drifts to 0644+.
