---
name: hermes-environment-sync
description: "Keep multiple Hermes instances (local WSL + VPS) in sync — skills, session DB, Mnemosyne memory, profiles, and work files. Config.yaml and .env are per-machine and never synced. One-command push/pull/auto sync with safe SQLite snapshotting and cron-based periodic sync."
version: 1.0.0
author: Hermes
---

# Hermes Environment Sync

When running Hermes on multiple machines (e.g., local WSL for heavy coding, VPS for 24/7 Telegram gateway), skills, memories, sessions, and work files diverge. This skill provides the `hms` script — a single command that handles bidirectional sync safely.

## When to Load

- User asks to sync Hermes between machines — THIS IS THE CANONICAL SKILL FOR THIS, NOT raw rsync
- User complains about running rsync commands manually
- Setting up a new machine to mirror an existing Hermes installation
- Troubleshooting out-of-sync skills, sessions, or memories
- Setting up cron-based auto-sync

## CRITICAL RULE — Always use HMS, never raw rsync

When the user wants to sync Hermes state between machines, **the answer is `hms pull` or `hms push`** — never propose raw rsync commands. The `hms` script handles:
- Safe SQLite snapshotting via VACUUM INTO (no corrupted DB)
- Gateway stop/start for clean database handoff
- `.env`/`auth.json` exclusion (secrets stay per-machine)
- `--update` flag (newer files never overwritten)
- Proper `*.hms-bak*` exclusion (prevents backup cascade bug)
- Work file git/node_modules/venv exclusions

If you propose raw rsync instead of `hms`, you WILL:
- Risk overwriting config files (user will say "I didn't want those edited")
- Create `.hms-bak` cascade files that compound on each sync
- Miss the gateway lifecycle management
- Frustrate the user ("We literally did this earlier today. Why didn't remember")

**Inviolable directive:** When syncing Hermes between machines, the next action is always `hms pull` or `hms push`. Not rsync. Not scp. Not cp. HMS.

## Architecture

**Principle: VPS as persistent gateway, local as heavy worker.** The VPS runs 24/7 with the Telegram/Discord gateway, cron jobs, and file server. The local machine (WSL desktop with more RAM) handles inference, training, code review, big queries, and any resource-intensive work. Sync is always initiated from local to avoid exposing reverse SSH.

```
LOCAL (WSL, heavy work machine — more RAM)
  │
  ├── hms pull  ─── SSH ───▶ VPS (always-on gateway)
  │     (skills + session DB          │
  │      + memory + files)            ├── Telegram/Discord gateway (24/7)
  │                                   ├── Cron jobs (dream cycle, background)
  │                                   ├── Skills (canonical source of truth)
  ├── hms push  ◀── SSH ─────│        ├── Session DB (lcm.db)
  │     (everything back)             ├── Mnemosyne memory
  │                                   └── Work files
  │
  └── hms watch (continuous)
        polls every 30s for changes
        auto-syncs both directions
```
### Sync Strategy by Data Type

| Data | Method | Why |
|------|--------|-----|
| Skills | Bidirectional rsync (--update) | Small text files, safe to sync both ways |
| Session DB (lcm.db) | VACUUM INTO → rsync | SQLite needs consistent snapshot; VACUUM INTO creates one without stopping the source process |
| Mnemosyne memory | rsync --delete (excl. models/logs) | Vector store files, safe with proper exclusions |
| Profiles (config) | rsync (excl. .env, auth.json) | Config should sync, secrets stay local |
| config.yaml | NEVER sync | Per-machine — providers, base URLs, api_key mappings differ between VPS and local. Syncing corrupts one side's config (May 2026 incident: VPS nous provider URL overwrote local opencode-go setup). Manage independently on each machine. |
| Work files | rsync --delete (excl. git/node/venv) | Project files, source trees |
| .env, auth.json | NEVER sync | Different API key pools per machine |

## Setup

### VPS Side (one-time)

The `hms` script lives at `~/.hermes/bin/hms` on the VPS. It's included as a linked file in this skill (`scripts/hms.sh`).

```bash
# Ensure the script is executable
chmod +x ~/.hermes/bin/hms

# Verify gateway is running as a systemd user service
systemctl --user status hermes-gateway.service
```

### Local Side (WSL)

**Step 1 — Copy the script from VPS:**
```bash
scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms
chmod +x ~/.hermes/bin/hms
```
Replace the IP with your VPS Tailscale IP or SSH hostname.

**Step 2 — Run setup (mirrors VPS structure to local):**
```bash
hms setup
```
This runs cmd_pull (copies skills, plugins, scripts, bin, cron, profiles, work files, databases) and prints guidance for PATH, cron, and boot-up auto-pull.

**Step 3 — Test connectivity:**
```bash
hms status
```
Shows skill counts, DB sizes, profile counts, work file diffs, and VPS gateway status.

**Step 4 — Start continuous sync (optional):**
```bash
hms watch
```
Background daemon polls both sides every 30 seconds, auto-syncs changes.

## Commands

### `hms push` — Local → VPS (end of local session)

Full sync including session DB. Briefly stops the VPS gateway (~15s) for clean DB handoff. Run when you finish working on the local machine.

**What it syncs:**
- skills/, plugins/, scripts/, bin/, cron/ -- full directory structure
- profiles/ (excludes .env, auth.json, *.lock)
- Session DB (lcm.db) -- timestamp-gated, VACUUM INTO snapshot
- Mnemosyne memory (excludes models/, cache/)
- Legacy memories/
- Work files (~/work -- excludes .git, node_modules, venv, __pycache__)
- HMS script itself (self-syncs the binary)
- Does NOT sync: config.yaml, .env, auth.json (per-machine)

### `hms pull` — VPS → Local (start of local session)

Full sync from VPS to local. VPS gateway stays running -- VACUUM INTO works on a live DB. Run when you sit down at the local machine.

Same scope as push but in reverse. Also syncs the HMS script itself from VPS so local always has the latest version.

### `hms auto` — Skills + files only (for cron)

Lightweight sync for cron. No database touching, no gateway downtime. Syncs skills and work files both ways using --update (never overwrite newer).

Suitable for */30 * * * * cron jobs.

### `hms status` — Sync differences

Shows skill counts, DB sizes, work file diffs (both directions), and VPS gateway status. Also shows whether the HMS watch daemon is running.

### `hms watch` — Continuous bidirectional sync daemon

Starts a background daemon that polls both VPS and local every 30 seconds for file changes. On detecting changes, runs push + pull automatically.

Polls for changes by checking files modified within the last minute (via find -mmin -1). Runs cmd_pull then cmd_push when changes are detected on either side.

Logs to ~/.hermes/hms/watch.log. PID file at ~/.hermes/hms/watch.pid.

```
hms watch       # Start daemon
hms stop        # Stop daemon
hms status      # Shows daemon status + recent log tail
```

### `hms setup` — Initialize local Hermes from VPS (first-time)

One-time setup that mirrors the entire VPS Hermes structure to the local machine. Runs cmd_pull, then prints guidance for:
- Adding ~/.hermes/bin to PATH
- Setting up cron for auto-sync every 30 minutes
- Setting up boot-up auto-pull in ~/.bashrc

### `hms merge-db` — Smart session DB merge

When both VPS and local have accumulated sessions independently (VPS from gateway, local from CLI), this determines which DB is newer and syncs the newer one to the other side. Pulls the older side's DB as a backup first, then pushes the newer.

### `hms cleanup` — Remove .hms-bak debris, check disk

Removes stale .hms-bak backup files created by rsync --backup. Reports disk usage and top space hogs. Works both from local (via SSH) and directly on VPS.

## Cron Auto-Sync Setup

Set up on the local machine (WSL). Ensure cron is running:

```bash
sudo service cron status || sudo service cron start
```

Add to crontab (`crontab -e`):

```cron
# HMS auto-sync every 30 minutes (skills + work files)
*/30 * * * * $HOME/.hermes/bin/hms auto >> $HOME/.hermes/logs/hms-cron.log 2>&1
```

On WSL, cron doesn't start automatically. Add to your `~/.bashrc`:

```bash
# Start cron if not running (for hms auto-sync)
sudo service cron status &>/dev/null || sudo service cron start >/dev/null 2>&1
```

## Daily Workflow

| When | Run | What happens |
|------|-----|-------------|
| Sit down at local machine | `hms pull` | Skills, sessions, memory, files, profiles ← VPS |
| Work locally (heavy tasks) | `hms watch` or cron `hms auto` | Continuous or every 30min background sync |
| Need a file from VPS | agent uses `deliver put` | File server on Tailscale IP → download from browser |
| Leave local machine | `hms push` | Everything back to VPS. Gateway down ~15s for DB sync |
| Access via Telegram on VPS | nothing | VPS has latest state from push + watch cycles |

## File Delivery to Local (Supplement to HMS)

HMS handles bidirectional sync of Hermes state (skills, DBs, memory, profiles, work files). For **one-off file delivery** (large PDFs, media, downloaded books), use the Tailscale-bound file server instead.

See `references/vps-file-server.md` for full setup and commands.

Quick workflow:
1. Agent runs `deliver put /path/to/file` (copies to ~/deliver/)
2. User opens `http://100.113.2.25:8080` in local browser
3. Downloads, then tells agent "nuke them"
4. Agent runs `deliver cleanup`

The file server is stopped when not in use to minimize surface area.

## Database Sync: How VACUUM INTO Works

The session DB (`lcm.db`) is a SQLite database using WAL mode. It's always open when Hermes is running. Standard `cp` or `rsync` can produce inconsistent copies because of the WAL.

**Solution:** `sqlite3 lcm.db "VACUUM INTO '/tmp/snap.db'"` creates a point-in-time consistent snapshot while the source DB is still being written to. This is built into SQLite 3.27+ (2019) and is fully atomic.

**In `hms push`** — the VPS gateway is stopped before transferring the snapshot (needed because the running gateway holds the old inode; replacing the file doesn't take effect until the process reopens it).

**In `hms pull`** — the VPS stays running. The snapshot is created on VPS (while live), transferred to local, and local's stale WAL files are cleaned up.

**WAL files to clean:**
```bash
rm -f lcm.db-wal lcm.db-shm
```

## Gateway Management via SSH

The script manages the VPS gateway using `systemctl --user` via SSH:

```bash
# Stop (for clean DB handoff during push)
XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user stop hermes-gateway.service

# Start (after sync)
XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user start hermes-gateway.service

# Status check
XDG_RUNTIME_DIR=/run/user/$(id -u) systemctl --user is-active hermes-gateway.service
```

**`XDG_RUNTIME_DIR` is required** because non-interactive SSH sessions don't set it automatically. Without it, `systemctl --user` fails with "Failed to connect to bus."

## The hms Script

The script is included as a linked file: `scripts/hms.sh`

Deploy from the skill:
```bash
# Copy to ~/.hermes/bin/
cp <skill_path>/scripts/hms.sh ~/.hermes/bin/hms
chmod +x ~/.hermes/bin/hms
```

Or scp from the VPS to local as described above.

## Pitfalls

- **SSH PATH for `hermes` command:** Non-interactive SSH doesn't source .bashrc. The `hermes` binary is in a venv (`/usr/local/lib/hermes-agent/venv/bin/hermes`), which may not be in SSH's PATH. The script uses `systemctl --user` directly (with XDG_RUNTIME_DIR) instead of the `hermes gateway stop/start` CLI to avoid this. If you need the hermes CLI, use the full path.
- **Gateway downtime:** `hms push` stops the VPS gateway for ~15 seconds. Telegram delivery is interrupted during this window. Plan pushes between expected messages, not during active conversations.
- **WAL files:** After replacing `lcm.db`, stale `lcm.db-wal` and `lcm.db-shm` files cause Hermes to see a corrupt database. Always clean these after a DB sync.
- **.env/.auth.json are NOT synced:** API keys, OAuth tokens, and credential pools differ per machine. The script explicitly excludes them. After initial setup, run `hermes auth list` on each machine to verify provider credentials.
- **Mnemosyne models/ directory:** The vector embedding models are large (hundreds of MB) and identical across machines. The script excludes `models/`, `logs/`, and `.cache/` from Mnemosyne sync to save bandwidth.
- **Work file rsync excludes:** Git repos, node_modules, venvs, __pycache__ — these are either machine-specific or better rebuilt locally. Excluded by default.
- **Cron on WSL:** WSL doesn't start cron on boot. Add the `sudo service cron start` check to `~/.bashrc`. Without this, `hms auto` doesn't fire automatically.
- **Backup cascade bug (`*.hms-bak*`):** The `rsync --backup --suffix=.hms-bak` flag creates backup files that look like new files to the next sync run, creating infinite `.hms-bak.hms-bak.hms-bak` nesting. Killed 15,714 garbage files from one VPS. FIXED by adding `--exclude=*.hms-bak*` to every rsync call in the `hms` script. THIS EXCLUDE MUST BE PRESENT in all rsync commands. If you find a raw rsync command that lacks it, add it. This applies to the HMS script (`~/.hermes/bin/hms`) on BOTH VPS and local — the script is not self-syncing, so both sides need independent patching.
- **First pull after fresh Hermes install:** If local Hermes has never been used and the VPS has a large session DB (tens of MB), `hms pull` transfers the full DB. This is expected for the initial sync.
- **Disk space on small VPS:** Session DB can grow to 50-100MB over months. Mnemosyne models add ~300MB. Before syncing large files, verify disk space: `df -h`.

## Post-Sync Config Integrity Check

HMS syncs `config.yaml` between machines. If the two machines have **different provider setups** (e.g., VPS uses `custom/nous` while local uses `opencode-go`), a push from VPS overwrites the local config with the wrong provider. The fix is partial if only `provider` and `base_url` are corrected but `api_key` is missed.

### The Triad Check — always verify these three after a sync

After any `hms pull` or `hms push`, run:

```bash
grep -A5 '^model:' ~/.hermes/config.yaml
```

You must confirm all three match expectations:

```
model:
  default: <expected-model>
  provider: <expected-provider>       # ✓ Check 1
  base_url: <expected-endpoint>       # ✓ Check 2
  api_mode: chat_completions
  api_key: ${EXPECTED_ENV_VAR}        # ✓ Check 3 — NOT a different provider's key
```

**Check 1 — provider:** Must match the intended backend (`opencode-go`, `custom`, `openrouter`, etc.)

**Check 2 — base_url:** Must point to the right API endpoint. Common mismatch: VPS's `inference-api.nousresearch.com` vs local's `opencode.ai/zen/go/v1`.

**Check 3 — api_key:** The most commonly missed fix. If the provider changed, the `api_key` env var must change with it. A VPS using `custom/nous` leaves `api_key: ${NOUS_API_KEY}` — if you fix provider back to `opencode-go` but miss the api_key, Hermes sends the wrong credentials to the correct endpoint, causing silent auth failures. The VPS key stays mapped even after the provider is corrected.

### Config backup trap — stale `config.yaml.hms-bak`

The `hms` script creates `config.yaml.hms-bak` as a backup BEFORE overwriting. If a VPS push replaced your local config with the wrong provider config, **that same hms-bak now contains the stale VPS config**. A subsequent `hms push` from the same VPS will re-corrupt because the source config hasn't changed.

**Fix:** After correcting the local config, also update the VPS config to match:

```bash
# From local, push corrected config to VPS:
scp ~/.hermes/config.yaml root@<vps-host>:.hermes/config.yaml
# Or SSH in and edit directly
```

Then verify the next HMS sync won't re-overwrite.

### .env cosmetic corruption

HMS sync can merge adjacent comment lines in `.env` files. Symptom: two unrelated configuration comments appear on one line (e.g., `# OPENCODE_GO_API_KEY=*** # Get your token at: https://huggingface.co/settings/tokens`). This is cosmetic — commented lines have no runtime effect — but indicates the sync had a line-boundary collision. Fix by splitting the merged line at the natural break point.

### Post-sync config recovery procedure

If a sync broke your model config:

1. Identify the corruption: `grep -A5 '^model:' config.yaml`
2. Check what the hms-bak has: `diff config.yaml config.yaml.hms-bak` — confirms the overwrite direction
3. Fix all three: `provider`, `base_url`, `api_key`
4. Also fix the source machine's config so next sync doesn't re-corrupt
5. Clean up `.env` comment merges if present
6. Verify against Bitwarden BWS if secrets are involved: `bws secret list <project_id>`

See `references/config-corruption-recovery.md` for a full reproduction transcript from a real incident.

## Verification

After setup, verify end-to-end:

```bash
# On local machine:
hms status                # Shows sync state
hms pull                  # Pull from VPS
# ... work locally ...
hms push                  # Push back to VPS

# On VPS (via SSH):
systemctl --user is-active hermes-gateway.service  # Should show "active"
sqlite3 ~/.hermes/lcm.db "SELECT count(*) FROM sessions;"  # Sessions intact
ls ~/.hermes/skills/ | wc -l  # Skills present

# Config integrity after sync:
grep -A5 '^model:' ~/.hermes/config.yaml    # Check provider/base_url/api_key triad
diff ~/.hermes/config.yaml ~/.hermes/config.yaml.hms-bak  # Verify no stale overwrite
```

## Related

- `remote-agent-infrastructure` — Tailscale mesh, Termux, tmux, git-as-memory for remote Hermes access (overlapping infra; this skill handles the sync layer)
- `git-memory-layer` — Git as persistent agent working memory for project artifacts (different scope: project repos vs Hermes infra sync)
- `background-agents` — Cron for background autonomous agent sessions (different scope: task execution vs infra sync)
- `hermes-agent` — General Hermes CLI reference (CLI commands, paths, profiles)
