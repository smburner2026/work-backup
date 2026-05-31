---
name: hermes-multi-sync
description: "HMS — Hermes Multi-Sync: safe bidirectional sync between local (WSL) and VPS over Tailscale. Syncs skills, session DB, Mnemosyne memory, and work files with --update (never overwrite newer) + --backup (recovery copies). Config.yaml and .env are per-machine and never synced."
version: 1.3
author: Randoooos + Hermes
---

# Hermes Multi-Sync (HMS)

Safe bidirectional sync between a local Hermes instance (WSL) and a VPS Hermes instance over Tailscale. Replaces manual rsync commands with a single `hms` command.

## Architecture

- **Local (WSL)** drives sync — initiates all SSH connections to VPS. Script copies `~/.hermes/bin/hms` from VPS to local during setup.
- **VPS** is the always-on hub (Telegram gateway, scheduled jobs). Script also works locally on VPS for `hms cleanup`.
- **Transport** — Tailscale IPs (default: `root@100.113.2.25`), no public ports exposed.
- **Safety** — every rsync uses `--update` (skip newer destinations) + `--backup --suffix=.hms-bak` (recovery files).

## Commands

| Command | What it syncs | When to run |
|---|---|---|
| `hms push` | Everything: skills, work files, session DB, Mnemosyne, profiles (NOT config/.env) | End of local session |
| `hms pull` | Everything (reverse direction) — NOT config/.env | Start of local session |
| `hms auto` | Skills + work files only — NO databases, NO gateway stop | Cron every 30 min |
| `hms status` | Shows skill counts, DB sizes + mtimes, work file diffs, gateway status | Any time |
| `hms cleanup` | Removes `.hms-bak` debris from `~/.hermes/` + `~/work/` + reports VPS disk + top space hogs | When disk is low |

All sync commands run a **pre-flight disk-space check** — warns if VPS <500MB free, blocks if <100MB.

## Setup (one-time on local WSL)

### Prerequisites

- Tailscale installed and connected on both machines
- SSH key-based auth from local to VPS (already set up if you SSH into VPS)
- `~/.hermes/bin/` exists on local

### Commands

```bash
# 1. Copy script from VPS over Tailscale
scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms
chmod +x ~/.hermes/bin/hms

# 2. Add to PATH
echo 'export PATH="$PATH:$HOME/.hermes/bin"' >> ~/.bashrc
source ~/.bashrc

# 3. Test connectivity over Tailscale
hms status

# 4. First-time pull (grabs VPS state to local)
hms pull

# 5. Set up auto-sync cron (every 30 min while WSL is running)
crontab -e
# Add: */30 * * * * $HOME/.hermes/bin/hms auto >> $HOME/.hermes/logs/hms-cron.log 2>&1

# 6. Add boot-up auto-pull to .bashrc
echo 'hms pull 2>/dev/null' >> ~/.bashrc
```

Script updates: after editing the script on the VPS, re-copy to local:
```bash
scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms
```

## Daily Workflow

1. **Open WSL terminal** — `hms pull` fires from `.bashrc`. Latest skills, sessions, memory, and work files arrive from VPS.

2. **Work locally** — Cron runs `hms auto` every 30 minutes. Skills + work files sync bidirectionally. No gateway downtime.

3. **End session / switch machines** — Run `hms push`. Gateway pauses ~15s for clean DB handoff via `VACUUM INTO` snapshot, then restarts.

4. **If hms push/pull fails mid-way** — check VPS disk first (`hms cleanup`). If disk is full, free space and retry.

## Safety Guarantees

- **--update** — never overwrites a file if the destination side has a newer mtime. The newer version always wins regardless of push/pull direction.
- **--backup --suffix=.hms-bak** — any file that IS overwritten leaves a `.hms-bak` recovery copy.
- **Session DB is timestamp-gated** — compares mtime on both sides before syncing. Only syncs if source is actually newer.
- **No --delete** anywhere — files are never removed by sync, only added or updated.
- **VACUUM INTO** creates a consistent SQLite snapshot while the source DB is live — no corruption risk, no downtime on the source side.
- **Gateway stop on push** uses `systemctl --user stop/start hermes-gateway.service` via SSH with explicit `XDG_RUNTIME_DIR` set.
- **Pre-flight disk check** — every push/pull/auto checks VPS has ≥500MB free before starting.

> **⚠️ These guards only work when using `hms push`/`pull`/`auto`.**
> If you run a raw rsync outside HMS — especially without `--update` — all these guarantees are bypassed. The timestamp gate and backup flags only protect the files the HMS script touches. After any manual sync between instances, run the post-sync recovery audit (`references/post-sync-recovery-audit.md`) to verify nothing was overwritten in the wrong direction. The most common casualty is the LCM DB (session database), since it diverges naturally between the gateway VPS and the local CLI.

## Config via Environment Variables

Set these on the local machine. Script defaults are already correct for Tailscale:

| Var | Default | Description |
|---|---|---|
| `HMS_VPS_HOST` | `root@100.113.2.25` | SSH target for VPS |
| `HMS_VPS_HERMES` | `/root/.hermes` | `~/.hermes` path on VPS |

Override for non-default setups:
```bash
export HMS_VPS_HOST=user@custom-ip
export HMS_VPS_HERMES=/home/user/.hermes
```

## The Script

Located at `~/.hermes/bin/hms` on the VPS. Works from either machine:
- **From local (WSL):** SSHes to VPS, runs rsync in both directions, checks disk before starting.
- **From VPS:** `hms cleanup` detects it's local via hostname check, runs cleanup directly without SSH.

### Internal Design

**Safe rsync flags applied to all operations:**
- `--update` — skip destination file if it's newer than source
- `--backup --suffix=.hms-bak` — rename existing dest files before overwriting
- `--exclude=*.hms-bak*` — prevent infinite backup cascade (backup files are excluded from being backed up on the next cycle)
- `--no-o --no-g --no-t` — don't try to preserve owner/group/timestamps across machines
- NO `--delete` anywhere — files are never removed by sync

**Session DB sync is timestamp-gated:**
1. Compares mtime of local vs VPS `lcm.db`
2. Only syncs if source is actually newer
3. Uses `sqlite3 db "VACUUM INTO '/tmp/snap.db'"` to create a consistent snapshot without stopping the source Hermes
4. On push, briefly stops VPS gateway via `systemctl --user stop hermes-gateway.service`
5. After push, restarts gateway and verifies `systemctl --user is-active hermes-gateway.service`

**Skills and work files use bidirectional rsync:**
- Pull from VPS first, then push to VPS
- Each direction uses `--update` so newer version always wins
- Conflicting edits produce a `.hms-bak` of the older version

**Pre-flight disk check:**
- Runs at the top of `hms push`, `hms pull`, and `hms auto`
- Queries VPS via `df -k` over SSH
- Warns if <500MB free, dies if <100MB free
- References free space strategy in `references/low-disk-recovery.md`

## Pitfalls

- **Both machines must be on Tailscale** for default IPs to work. Fall back to VPS public IP via `export HMS_VPS_HOST=user@<public-ip>`.
- **WSL cron dies on Windows reboot.** Enable with `sudo service cron start` post-boot. Consider a Windows startup script or Task Scheduler trigger.
- **Disk full will hang a sync** — the rsync process hangs with data in the TCP send buffer (send-Q grows). Diagnose with `hms cleanup` or check `df -h` on VPS. See `references/low-disk-recovery.md`.
- **`.hms-bak cascade loop (CRITICAL)`** — the original `RSYNC_SAFE` used `--backup --suffix=.hms-bak` without excluding the backup files themselves. On every sync cycle, the `.hms-bak` copies from the previous run were picked up as new files and backed up again, creating an infinite cascade (`.hms-bak`, `.hms-bak.hms-bak`, `.hms-bak.hms-bak.hms-bak`...). This produced 15,714 backup files in one work directory within hours. **Fix:** add `--exclude=*.hms-bak*` to `RSYNC_SAFE`. If upgrading an existing HMS installation, apply this to `~/.hermes/bin/hms` on the VPS, then re-copy to local via `scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms`. Existing `.hms-bak*` debris must be cleaned separately via `hms cleanup` or `find ~/.hermes ~/work -name '*.hms-bak*' -type f -delete`.
- **Gateway stop on push** — if the VPS gateway fails to restart after push, SSH in and run `systemctl --user start hermes-gateway.service` (or `hermes gateway start` if the CLI is in PATH).
- **Per-machine config stays out** — `.env`, `auth.json`, and `config.yaml` are never synced. Each machine has its own provider setup, API key env var mappings, terminal backend config, and credential pools. **The HMS script was patched in May 2026** to remove config.yaml from push/pull after a VPS → local overwrite corrupted the local provider configuration (VPS's `nous` provider URL overwrote the local `opencode-go` setup, and the `api_key` mapping was left pointing to the wrong env var). Never add config.yaml or `.env` back to the sync set.
- **Large work files** — `node_modules/`, `venv/`, `__pycache__/` are excluded from sync. Don't expect these to transfer.
- **First pull is slow** — the initial `hms pull` transfers everything including large PDFs and CSVs. Subsequent syncs only transfer what changed.
- **SSH via systemctl** — gateway management over SSH needs `XDG_RUNTIME_DIR` set explicitly for `systemctl --user`. The script handles this with `XDG_RUNTIME_DIR=/run/user/$(id -u)`.
- **Mnemosyne DB corruption from WAL/sync overlap** — if the Mnemosyne provider has an open connection to the DB while HMS syncs it via rsync, the WAL file (`.db-wal`) and the main DB can desync, producing B-tree corruption (rowid out of order, missing index entries, malformed FTS5 inverted indexes). Symptoms: `mnemosyne_remember` / `mnemosyne_recall` tools fail with "database disk image is malformed" even though `PRAGMA integrity_check` may still pass for simple schemas. **Recovery:** stop the gateway (`kill -TERM <gateway-pid>`), rebuild the DB via SQLite `.dump` → rebuild in a new file, verify with `PRAGMA integrity_check`, then symlink the root `mnemosyne.db` to `data/mnemosyne.db` if the sync created a 0-byte split-brain file at the root level. Restart the gateway after the fix. See `references/mnemosyne-corruption-recovery.md`.

- **LCM DB diverges naturally** — the VPS gateway accumulates sessions from Discord/Telegram that the local CLI never sees. After a week, the VPS LCM DB can be 50-200 messages ahead even when both sides are healthy. The `--update` flag in `RSYNC_SAFE` handles this by only syncing when the source is actually newer. But after a raw/hard rsync that ignores timestamps, the wrong DB can overwrite the right one. Always verify message counts after a non-HMS sync: `sqlite3 lcm.db 'SELECT COUNT(*) FROM messages'` on both sides. See `references/post-sync-recovery-audit.md`.
- **Community manifest is not in the sync set** — `~/.hermes/community-manifest.json` is not synced by `hms push`/`pull`/`auto`. If you use it (the hermes-maintenance skill depends on it), copy it manually: `scp root@<vps>:.hermes/community-manifest.json ~/.hermes/` after each pull.
- **Cron jobs.json is not in the sync set** — `~/.hermes/cron/jobs.json` is not synced either. VPS cron metadata will drift from local. After `hms pull`, sync cron state manually if needed. The VPS is the canonical runner for recurring jobs.
- **RSYNC_SAFE duplicate exclude bug** — if the local `~/.hermes/bin/hms` has `--exclude=*.hms-bak*` appearing twice on the `RSYNC_SAFE` line, re-copy from VPS: `scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms`. The double exclusion is harmless (rsync deduplicates) but indicates the local copy was modified separately from the VPS canonical version.
- **Windows filesystem boundary** — HMS only operates on the Linux filesystem (`~/.hermes/`, `~/work/`). It never touches Windows files under `/mnt/c/`. Windows Terminal settings, fonts, Windows paths, and all Windows-side files are completely unaffected by any HMS operation. If a change to a Windows-side path (/mnt/c/Users/..., Windows Terminal settings.json, VS Code settings on Windows, etc.) appears to have reverted after an HMS run, HMS is not the cause — check whether Windows software (Terminal, VS Code, etc.) silently auto-corrected an invalid config value (e.g., a font face that doesn't exist on the system gets reverted to a safe default).
