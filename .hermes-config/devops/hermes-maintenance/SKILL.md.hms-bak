---
name: hermes-maintenance
description: "Long-term care of a Hermes Agent instance — tracking community additions via manifest, running self-audits for update availability, and discovering what's been bolted onto base Hermes."
version: 1.4
author: Hermes Agent
---

# Hermes Instance Maintenance

Governance patterns for managing a Hermes Agent instance over time — tracking what's been added beyond base Hermes, checking for updates, and auditing the full installation.

## Philosophy

Base Hermes is updated via `hermes update`. But community additions (plugins, pip packages, custom scripts, cloned repos, hub skills) have no unified update path. Left untracked, they drift stale silently. These patterns solve that.

## Community Additions Manifest

A single JSON file at `~/.hermes/community-manifest.json` that records every addition outside `hermes update`, with its source, version, and update command.

### Schema

```json
{
  "manifest_version": 1,
  "created": "2026-05-24",
  "entries": [
    {
      "name": "doga",
      "type": "plugin",
      "source": "https://github.com/0z1-ghb/doga-hermes",
      "install_date": "2026-05-24",
      "version": "1.1.0",
      "install_method": "git clone → cp to ~/.hermes/plugins/doga/",
      "update_command": "cd /tmp && git clone ... && cp ...",
      "post_update": "hermes plugins enable doga (if needed) + /reset",
      "status": "active"
    }
  ],
  "update_policies": {
    "plugins": "Manual per entry. No auto-update.",
    "pip_packages": "pip install --upgrade <name>.",
    "hub_skills": "hermes skills update — covers all at once.",
    "agent_skills": "Managed by hermes curator.",
    "base_hermes": "hermes update."
  }
}
```

### Rules

- **Add an entry** every time you install something outside `hermes update`
- **Type field** distinguishes: `plugin`, `pip_package`, `bash_script`, `external_tool`, `skill`, `cron_script`, `skills_group`
- **Status field**: `active` (currently installed), `known` (exists on another machine), `archived` (removed but documented)
- **Group hub skills** under one entry with a count — don't list 43 individually

## Self-Audit Watchdog

A no_agent cron job that checks every community component for updates nightly. Stays **silent when nothing to report** (watchdog pattern) — the user only gets a message when there's work to do.

### What it checks

| Component | Method |
|-----------|--------|
| Hermes base | `git rev-list --count HEAD..origin/main` in install dir |
| Plugins with git remotes | `git fetch origin` + `rev-list --count` |
| Pip packages | `pip show` vs `pip index versions` |
| Plugins without git | GitHub API: compare release tag vs installed version |
| Hub skills | `hermes skills update` — detect non-"No updates" output |
| Cron jobs | `hermes cron list` — count lines with errors |
| G-Brain embedding model | Curl `POST /v1/embeddings` to OpenRouter → check HTTP 200 + valid JSON embedding body |
| G-Brain dream cycle completion | Read `.gbrain/.dream-last-run` marker timestamp; warn if >36h stale or missing |
| G-Brain CLI/PGLite health | `timeout 10 gbrain providers list` — detect hung PGLite (lock contention with MCP server) |

### Script template

Place at `~/.hermes/scripts/self-audit.sh`. Guard with `set -euo pipefail`. Use `UPDATES` accumulator, only `echo` and `exit 0` when non-empty. Add `|| true` after any grep that may return 1 (no match causes `set -e` to abort).

### Cron job parameters

```python
cronjob(
    action='create',
    name='nightly-self-audit',
    schedule='0 8 * * *',      # 3 AM CT / 08:00 UTC
    no_agent=True,
    script='self-audit.sh',     # relative to ~/.hermes/scripts/
    deliver='origin',
)
```

## Discovery Audit Methodology

When asked to inventory a Hermes instance, check these locations systematically:

1. **User plugins** — `~/.hermes/plugins/*/` — check each for `plugin.yaml` + `.git` remote
2. **Bundled plugins with .git** — `find /usr/local/lib/hermes-agent/plugins -maxdepth 3 -name ".git" -type d` — community repos cloned into bundled dir
3. **Pip packages** — `pip list | grep` for known community packages (mnemosyne-memory, etc.)
4. **Skills** — `hermes skills list | grep "local"` — all user-installed skills
5. **Cron jobs** — `cronjob action='list'` — check for errors and stale entries. **Fallback when `cronjob` tool is unavailable** (e.g. in cron environments): read `~/.hermes/cron/jobs.json` directly — it contains all job definitions, schedules, statuses, and `next_run_at` timestamps. Validate that every job has a future `next_run_at` (no expired/dead jobs) and `last_status` is not `"error"`.
6. **Scripts** — `~/.hermes/scripts/` — custom shell scripts
7. **Binaries** — `~/.hermes/bin/` — check file type, look for non-Hermes entries
8. **Custom git repos** — `find /root -maxdepth 4 -name ".git" -type d` — exclude Hermes install, LCM, node_modules
9. **Config** — `~/.hermes/config.yaml` — look for non-default additions (personalities, custom toolsets)

### Skills validation (YAML frontmatter audit)

When auditing the skills library, don't just count them — validate every SKILL.md has parseable YAML frontmatter with required fields.

```bash
python3 -c "
import yaml, os

skills_root = os.path.expanduser('~/.hermes/skills')
errored = []
ok = []

for root, dirs, files in os.walk(skills_root):
    for f in files:
        if f == 'SKILL.md':
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    content = fh.read()
                parts = content.split('---', 2)
                if len(parts) < 3:
                    errored.append(path + ': no YAML frontmatter')
                    continue
                fm = yaml.safe_load(parts[1])
                if not isinstance(fm, dict):
                    errored.append(path + ': frontmatter not a dict')
                    continue
                missing = []
                if 'name' not in fm:
                    missing.append('name')
                if 'description' not in fm:
                    missing.append('description')
                if missing:
                    errored.append(path + ': missing required fields: ' + str(missing))
                    continue
                ok.append(path + ': OK')
            except Exception as e:
                errored.append(path + ': parse error: ' + str(e))

print('OK: ' + str(len(ok)))
print('ERRORS: ' + str(len(errored)))
for e in errored:
    print('  ' + e)
"
```

Expected result on a healthy install: 0 errors, all SKILL.md files reported OK. If errors exist, they need individual attention — frontmatter parse failures prevent skills from being loaded by new agent sessions.

**What to check in each frontmatter:**
- `name` field matches the directory basename (convention — helps with `skill_view` lookups)
- `description` is present and meaningful (at least 10 chars, not boilerplate)
- No trailing whitespace inside `---` delimiters (breaks the YAML parser)

**Pitfall — profile SOUL.md vs skill SKILL.md:** Profile SOUL.md files (`~/.hermes/profiles/<name>/SOUL.md`) use `---` as markdown section separators, NOT as YAML frontmatter. These will always fail if parsed with the same script. The script above scopes to `~/.hermes/skills/` only, so it won't hit profile SOUL.md files.

### Config path integrity check

After loading config.yaml, validate that all filesystem paths declared in the config still exist. Missing paths point to stale config entries, deleted state, or a broken migration.

```bash
python3 -c "
import yaml, os

cfg = yaml.safe_load(open(os.path.expanduser('~/.hermes/config.yaml')))

paths_to_check = []

# State paths
for k in ['path', 'data_dir', 'database']:
    v = cfg.get('state', {}).get(k)
    if isinstance(v, str):
        paths_to_check.append(os.path.expanduser(v))

# Browser
v = cfg.get('browser', {}).get('data_dir')
if isinstance(v, str):
    paths_to_check.append(os.path.expanduser(v))

# Checkpoints
v = cfg.get('checkpoints', {}).get('dir')
if isinstance(v, str):
    paths_to_check.append(os.path.expanduser(v))

# Compression
v = cfg.get('compression', {}).get('database')
if isinstance(v, str):
    paths_to_check.append(os.path.expanduser(v))

for p in paths_to_check:
    exists = os.path.exists(p)
    print(('EXISTS' if exists else 'MISSING') + ': ' + p)
"
```

**What MISSING paths mean:**

| Path | Implication |
|------|-------------|
| `state.db` | State DB not at expected location — file may have been moved or renamed. Check if `sessions.json` replaced it. |
| `memory/` | Old-style memory dir replaced by Mnemosyne at `~/.hermes/mnemosyne/`. Not necessarily a problem. |
| `sessions.db` | Sessions may be stored as JSON instead (`~/.hermes/sessions/sessions.json`). Depends on Hermes version. |
| `state-snapshots/` | Checkpoints pruned or path changed in config. |

**Pitfall:** Some config paths reference optional features (legacy memory, old session formats). A MISSING path is not always a bug — verify the feature is actually expected before flagging. If the path refers to a Mnemosyne-era deployment, the old `memory/` dir is expected to be absent.

### What NOT to track in the manifest

- Bundled plugins (ship with Hermes, covered by `hermes update`)
- Builtin skills (also shipped)
- Config values like personalities (not community additions)
- Environment-dependent failures (missing binaries, fresh-install errors)

## Cross-Instance Verification Audit

When two Hermes instances (e.g. local WSL + VPS gateway) share state via sync, you need a systematic approach to **detect divergence** after raw rsync, hard sync, or any sync not mediated by `--update` timestamp guards. The goal is to distinguish expected per-machine differences from actual data loss.

### When to run

- After any manual/raw rsync between instances ("did it break anything?")
- When investigating asymmetric behaviour between machines
- Before blowing away one side's state and replacing with the other's
- When cron jobs or session history appear stale on one side

### Methodology — compare in this order

| Step | What to compare | How | What it tells you |
|---|---|---|---|
| 1 | **config.yaml** | `md5sum` on both → `diff` if different | Core config divergence = someone edited one side |
| 2 | **Main .env** | `grep -v '^#' \| grep -v '^\s*$' \| grep '='` on both, diff the active vars | Machine-specific secrets (expected). Flag missing auth on the gateway side |
| 3 | **Profile configs** | `md5sum` each profile's `config.yaml` on both | Profile-level divergence |
| 4 | **Profile .env files** | Check existence + active vars per profile | Missing creds in a profile that needs them |
| 5 | **LCM DB** | Compare size, mtime, AND message count: `sqlite3 lcm.db 'SELECT COUNT(*) FROM messages'` | **Most critical.** Divergent counts = sessions only exist on one side. Gateway (VPS) naturally has more due to Discord/Telegram. Check direction — if local > VPS, local sessions may have been lost |
| 6 | **Mnemosyne DB** | `md5sum` the `mnemosyne.db` | Should match if last sync was clean. Divergence = memory drift |
| 7 | **Skills catalog** | Count skills: `ls ~/.hermes/skills/*/ \| wc -l` | Differing counts = skills added on one side not synced |
| 8 | **Cron jobs** | Compare job definitions via `cronjob action='list'` or diff `jobs.json` | VPS is the canonical runner. Local having stale/extra jobs = metadata not synced |
| 9 | **Community manifest** | Check `community-manifest.json` exists on both | Missing on one side = not in sync set |
| 10 | **Backup debris** | Count `.hms-bak` files: `find ~/.hermes ~/work -name '*.hms-bak*' -type f \| wc -l` | High count = aggressive overwrites. Check key config backups match current |
| 11 | **Config backups** | For each `config.yaml.hms-bak`, diff against current `config.yaml` | If different, sync replaced a config with a different version. Restore or accept |
| 12 | **Work dirs** | `ls ~/work/` on both, diff | Local-only dirs are normal. Missing shared project dirs are not |
| 13 | **SSH / gateway health** | `ssh -o ConnectTimeout=5 root@<vps> 'echo OK'` and `systemctl --user is-active hermes-gateway.service` | Can the sync channel still talk? Is the gateway alive? |
| 14 | **VPS disk** | `df -h /` on VPS | <500MB free = future syncs will hang |

### Distinguishing expected vs problematic differences

**Expected (machine-specific, not divergence):**
- `.env` vars: gateway has TELEGRAM/DISCORD/API_SERVER; local has SUDO_PASSWORD/TERMINAL_ENV
- `auth.json`: token files differ per machine
- LCM message count: VPS gateway naturally 50-200 messages ahead due to platform sessions
- Work dirs: local may have dev-only test projects
- Profile `.env` files: one side may have a template, the other none

**Problematic (needs attention):**
- `config.yaml` differs — someone edited one side without syncing
- `mnemosyne.db` hash differs — memory state diverged
- Local LCM message count > VPS — local sessions may have been overwritten
- Community manifest missing — tracking gap
- Cron job IDs differ — jobs created on one side not propagated
- Config backups differ from current — overwritten config with data loss

### Recovery commands

```bash
# Restore a config from backup
cp ~/.hermes/config.yaml.hms-bak ~/.hermes/config.yaml

# Copy community manifest from VPS
scp root@100.113.2.25:.hermes/community-manifest.json ~/.hermes/

# Sync cron state from VPS (careful — VPS is canonical runner)
scp root@100.113.2.25:.hermes/cron/jobs.json ~/.hermes/cron/jobs.json

# Verify HMS script is the correct version (re-copy from VPS)
scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms

# Clean up backup debris after verification
hms cleanup
# Or manually: find ~/.hermes ~/work -name '*.hms-bak*' -type f -delete
```

### Pitfalls

- **md5sum on live DBs** — `lcm.db` and `mnemosyne.db` change while Hermes is running (WAL mode). For clean comparison, stop at least the local TUI/gateway before hashing.
- **Count vs size for LCM DB** — SQLite page sizes can make equal-count DBs differ in file size. Always check message count, not just file size.
- **`auth.json` and `.env` diffs are always noisy** — machine-specific by design. Only flag them if an expected secret is outright missing on a machine that needs it.
- **Cron `jobs.json` mtime parity** — VPS `jobs.json` updates with every cron tick. A stale local copy (even 1 day old) is normal. Only worry if the VPS copy is missing jobs the local has.
- **First cross-instance audit on an existing setup** — some divergence is pre-existing debt, not damage from the last raw sync. Date-stamp each finding.

## Update Cheat Sheet

| Component | Command |
|-----------|---------|
| Base Hermes | `hermes update` |
| Hub skills | `hermes skills update` |
| Pip packages | `pip install --upgrade <name>` |
| Plugins with git remote | `cd <plugin_dir> && git pull` |
| Plugins without git | Manual recopy from source repo |
| Agent-created skills | `hermes curator run` (auto-managed) |

## Project Directory Convention

Use per-project temporary directories to avoid scattering intermediate files across the system. The user prefers:

> **Every project gets its own `temp/` dir** inside the project directory for intermediate work (build artifacts, extracted pages, test output, debug PDFs). Use `project/temp/` rather than `/tmp/project/` or bare project-root dumping.

### Rationale

- **Easy cleanup** — `rm -rf project/temp/` removes all intermediates at once without hunting for orphaned `/tmp/` dirs
- **Context locality** — intermediates stay with the project; `ls` shows what belongs to what
- **Sync-friendly** — `temp/` is trivially gitignored; `/tmp` files are lost on reboot and never sync
- **No cross-project pollution** — evidence/debug files from one project never clutter another's space

### When to apply

- Data-processing scripts that generate intermediate CSV/JSON/HTML
- PDF pipelines (WeasyPrint, fpdf2) that create per-chapter temp files
- Archive extraction steps before processing
- Any multi-step pipeline where intermediate files are generated

## Git Repository Maintenance

The Hermes agent's `.git` directory accumulates garbage over time from repeated `hermes update` (git fetch + git pull) operations that leave orphaned `tmp_pack_*` files in `.git/objects/pack/`.

### Warning signs

- Disk usage spikes after `hermes update` runs
- `du -sh /usr/local/lib/hermes-agent/.git` shows 5+ GB (should be ~1-2 GB for a healthy repo)
- Reports of "no space left on device" or Hermes gateway failing to start

### Detection procedure

```bash
cd /usr/local/lib/hermes-agent

# Check how much space .git is using
du -sh .git

# Count orphaned tmp_pack files
ls -la .git/objects/pack/tmp_* 2>/dev/null | wc -l

# Get full git object stats
git count-objects -vH
```

Key signals in `git count-objects -vH` output:

| Field | Healthy | Needs cleanup |
|-------|---------|---------------|
| `garbage` | < 10 | 100+ orphaned files |
| `size-garbage` | 0 MiB | 1+ GB |
| `packs` | 1-5 | 30+ pack files |
| `prune-packable` | 0 | > 0 stale objects |

### Cleanup procedure

1. **Remove orphaned tmp_pack files** — these are from failed/interrupted git operations, not referenced by any branch:

```bash
cd /usr/local/lib/hermes-agent
rm -f .git/objects/pack/tmp_*
```

2. **Run git gc** to repack valid objects and prune unreachable ones:

```bash
git gc --prune=now
```

3. **Verify**:

```bash
git count-objects -vH
du -sh .git
```

Expected result: `.git` drops from 16+ GB to ~1-2 GB. Garbage count goes to 0.

### Prevention

- Add `&& git gc --auto` after any manual `hermes update` in scripts
- The nightly self-audit script should check `.git` size: `du -sb .git | awk '$1 > 5000000000 {print "WARNING: .git directory is " $1 " bytes"}'`
- If `hermes update` crashes or is killed, check for tmp_pack files immediately afterward

### Pitfalls

- **Do NOT `rm -rf .git`** — the repo is the canonical Hermes install. You want to clean *inside* it, not delete it.
- **Disk space during gc** — `git gc` needs temporary space to repack. With 14+ GB of garbage, it may need 1-2 GB free to run. If disk is critically low (< 500 MB free), remove tmp_pack files first (they're safe to delete without gc) to free enough space for gc to run.
- **Post-gc verification** — After gc, run `git rev-list --count HEAD` to confirm the commit history is intact, then `hermes --version` to confirm the agent still starts.

## Disk Space Analysis

When disk usage is unexpectedly high, systematically map usage before deciding what to clean.

### Quick triage

```bash
df -h                                    # Overall usage
du -sh /usr/local/lib/hermes-agent/      # Hermes install (often the culprit)
du -sh ~/.hermes/                        # User config + data
du -sh /root/work/                       # Project work dirs
du -sh /root/.[!.]* 2>/dev/null | sort -rh | head -20  # Hidden dirs in home
```

### Top Hermes space consumers

| Location | Typical size | Growth pattern |
|----------|-------------|----------------|
| `.git/` inside install dir | 1-16 GB | Grows with each `hermes update` if garbage accumulates |
| `state-snapshots/` in `~/.hermes/` | 0.5-2 GB | Grows with Hermes checkpointing (configurable retention) |
| `mnemosyne/` in `~/.hermes/` | 0.3-1 GB | Grows with memory consolidation |
| `state.db` in `~/.hermes/` | 0.1-0.5 GB | SQLite session DB, auto-managed |
| `sessions/` in `~/.hermes/` | 0.1-0.5 GB | Past session transcripts |
| `venv/` in install dir | 1-2 GB | Python deps — fixed size after install |
| `node/` in `~/.hermes/` | 0.3-0.5 GB | Node.js runtime binary |

### Recovery candidates by expected savings

| Fix | Potential recovery | Risk |
|-----|-------------------|------|
| Clean git garbage (tmp_pack + gc) | 12-15 GB | None — orphaned files only |
| Prune old state-snapshots (keep last 3) | 0.5-1 GB | Low — oldest checkpoints lost |
| Compact Mnemosyne via `hermes mnemosyne sleep --all-sessions` | 0.1-0.3 GB | None — pure compaction |
| Clear session DB (via curator retention) | 0.1-0.3 GB | Low — old sessions unavailable for search |
| Clear `/tmp/` temp files | 0.1-2 GB | Low — only if user hasn't stored work there |

### Pitfalls

- **`du` counts multiple times for hard links** — snapshots doubled. Use `du -sh --apparent-size` for accurate single-reference sizes.
- **WAL journal files in SQLite** — `state.db` can appear 3-4× larger than actual data if the WAL journal hasn't been checkpointed. Before deleting a large DB file, run `sqlite3 <db> 'PRAGMA wal_checkpoint(TRUNCATE);'` and re-check size.
- **Snapshots with symlinks** — `state-snapshots/` may contain hardlinked copies of config files. Deleting the directory doesn't reclaim full space until all hardlinks are gone. Use `find <dir> -links +1 -ls` to identify shared blocks.

## Post-Session File Cleanup

After heavy translation, document-generation, or data-processing sessions, the filesystem accumulates temporary files (generated PDFs, extracted images, cleaned text, HTML intermediates, page-image caches) that are not needed across sessions. Clean these up at the user's request before syncing.

### What to clean

1. **Session-generated PDFs** — Anything under `/tmp/bay_vien_*`, `/tmp/caodai_*`, `/tmp/test_*`, `*.pdf` under `/root/.hermes/audio_cache/`, and stale outputs in `/tmp/` from multi-step document workflows. Keep DABT reference PDFs (`/root/work/dabt/`).

2. **Temp working directories** — Per-session extracted image dirs (`/tmp/caodai_images/`, `/tmp/caodai_pages*/`), per-chapter dirs (`/tmp/bay_vien_chapters/`, `/tmp/bay_vien_en/`), intermediate text files (`*_full.txt`, `*_clean.txt`, `*_english.txt`, `*_check.txt`).

3. **Hermes cache artifacts** — `/root/.hermes/cache/documents/` (document uploads), `/root/.hermes/media_cache/` (media uploads), `/root/.hermes/image_cache/`, `/root/.hermes/audio_cache/` (after extracting needed deliverables).

4. **Stale Hermes-internal empties** — These accumulate over time and are safe to remove when empty:
   - `/root/.hermes/hooks/`, `/root/.hermes/pairing/`, `/root/.hermes/digests/`
   - `/root/.hermes/sandboxes/singularity/`, `/root/.hermes/profiles/*/sandboxes/singularity/`
   - `/root/.hermes/profiles/*/bin/`, `/root/.hermes/profiles/*/audio_cache/`, `/root/.hermes/profiles/*/hooks/`
   - `/root/.hermes/profiles/*/pairing/`, `/root/.hermes/profiles/*/cron/output/`, `/root/.hermes/profiles/*/image_cache/`
   - `/root/.hermes/profiles/*/logs/curator/`, `/root/.hermes/profiles/*/memories/`, `/root/.hermes/profiles/*/sessions/`
   - Stale kanban workspaces: `/root/.hermes/kanban/workspaces/t_*/` (empty = no active board)

5. **Stale agent config dirs** — AI coding agent configs from tools no longer used accumulate under `/root/`. Canonical list of known agent config dirs (consolidated from multiple cleanup sessions):

   **VS Code / Cline-family agents:**
   `.claude/`, `.vscode/`, `.codeium/`, `.tabnine/`, `.zencoder/`, `.continue/`

   **AI coding agent tools (standalone):**
   `.openclaw/`, `.aider-desk/`, `.pi/`, `.rovodev/`, `.bob/`, `.neovate/`, `.roo/`
   `.qoden/`, `.qoder/`, `.qwen/`, `.kilocode/`, `.kiro/`, `.mux/`, `.trae/`, `.trae-cn/`
   `.mcpjam/`, `.kode/`, `.vibe/`, `.adal/`, `.junie/`, `.snowflake/`, `.openhands/`
   `.pochi/`, `.iflow/`

   **Cline-derived / Cline-companion configs:**
   `.agents/`, `.augment/`, `.forge/`, `.factory/`, `.codemaker/`, `.codestudio/`
   `.codeartsdoer/`, `.commandcode/`

   **Rules for deletion:**
   - Only delete these when the user explicitly authorizes cleanup — some may be actively used
   - When the user says "nuke all AI agent config dirs", delete the entire canonical list above
   - After deletion, always re-check with `ls -la /root/ | grep "^\."` to catch any new ones that appeared mid-session
   - Document any new directories found in a memory note so the canonical list can be updated

6. **Project-specific artifacts** — e.g. `/root/substack_exports/` article PDFs after extraction, `/root/work/nolte_book.pdf` after the Nolte compilation is complete. Confirm with the user before bulk-deleting project files.

### Cleanup discovery commands

```bash
# Find all PDFs (excluding system paths)
find /root /home /tmp -name "*.pdf" -not -path "*/venv/*" -not -path "*/__pycache__/*" -not -path "*/site-packages/*" -not -path "*/.local/share/*" 2>/dev/null | sort

# Find empty directories
find /root /home /tmp -type d -empty -not -path "*/venv/*" -not -path "*/__pycache__/*" -not -path "*/site-packages/*" -not -path "*/.cache/*" 2>/dev/null

# Find directories containing only subdirs (possible redundancy)
find /root /home /tmp -type d -not -path "*/venv/*" -not -path "*/__pycache__/*" 2>/dev/null | while read d; do
  contents=$(ls -A "$d" 2>/dev/null | wc -l)
  subdirs=$(find "$d" -maxdepth 1 -type d ! -path "$d" 2>/dev/null | wc -l)
  if [ "$contents" -eq "$subdirs" ] && [ "$contents" -gt 0 ] && [ "$contents" -le 3 ]; then
    echo "$d ($contents items, all subdirs)"
  fi
done
```

### PDF size constraints for platform delivery

When delivering generated PDFs to messaging platforms (Discord, Telegram), the file size MUST be under the platform's limit:
- **Discord (no boost):** 8MB — compress page images aggressively
- **Discord (boosted):** 25-100MB depending on level

For large PDFs with embedded page images:
- Extract source pages at 100dpi instead of 200dpi
- Compress JPEG quality to 50-60
- Target: 4-5MB for a 96-page document with photos
- If still over limit, split into parts or remove image backgrounds

```bash
# Example: compress page images at lower DPI + quality
pdftoppm -jpeg -r 100 source.pdf /tmp/pages/page
for f in /tmp/pages/page-*.jpg; do
  python3 -c "from PIL import Image; Image.open('$f').save('$f', 'JPEG', quality=50, optimize=True)"
done
```

### Post-cleanup sync

After cleanup on one machine, sync to the other(s) to avoid the cleaned state being overwritten by stale remote files:
- Use HMS: `sudo ~/.hermes/bin/hms pull` (remote → local) or `hms push` (local → remote)
- For bare rsync with deletion (mirror): add `--delete` flag
- Use Tailscale IPs for key-based auth (no password prompt)
- Run with `sudo` on the destination if the target is `/root/` on WSL

### What NOT to delete

- DABT reference PDFs under `/root/work/dabt/`
- Hermes skill template PDFs (conference paper formatting templates)
- Hermes system docs (e.g. `/usr/local/lib/hermes-agent/docs/hermes-kanban-v1-spec.pdf`)
- SSH keys in `~/.ssh/`
- HMS backup files (`*.hms-bak`)

## Hermes Venv Entry-Point Recovery

When `hermes` reports a "No such file or directory" error and the wrapper at `~/.local/bin/hermes` points to a missing `venv/bin/hermes`, but the Hermes repo checkout at `~/.hermes/hermes-agent/` is intact:

```bash
cd ~/.hermes/hermes-agent

# 1. Check if python3-venv is available (Ubuntu/Debian need it installed)
python3 -m venv --help >/dev/null 2>&1 || sudo apt install -y python3-venv

# 2. Rebuild the venv
rm -rf venv
python3 -m venv venv

# 3. Reinstall Hermes from the existing checkout
venv/bin/pip install -e .

# 4. Verify
hermes --version
```

### Trigger conditions

- `hermes` (or `hermes update`, `hermes uninstall`) errors with `No such file or directory` pointing to `venv/bin/hermes`
- The repo under `~/.hermes/hermes-agent/` still has all source files (not corrupted)
- Wrapper at `~/.local/bin/hermes` exists and is a 3-line Python stub pointing to `.../venv/bin/hermes`

### Common causes

- Partial upgrade interrupted mid-venv-creation
- `rm -rf ~/.hermes/hermes-agent/venv` during a cleanup attempt
- Linux distro shipped Python without `ensurepip` (Ubuntu WSL most common)

### Verification

After rebuild, confirm:
```bash
hermes --version         # Should show v0.X.Y
ls -la venv/bin/hermes   # Should exist and be executable
```

### What NOT to do

- Do NOT run `hermes update` first — it pulls the latest release but won't fix a missing venv entry point
- Do NOT reinstall from scratch (`curl install.sh | bash`) unless the checkout is also corrupted — rebuilding the venv preserves local data (session DB, config, skills)
- Do NOT symlink wrapper paths — the wrapper expects a real file at the venv path

## MCP Server Lifecycle & Memory Management

MCP servers consume significant RAM because each Hermes process spawns its own independent copies. A kanban worker spawned by the dispatcher reads the same config and starts fresh MCP server processes — creating duplicates that waste ~100MB+ per spawn.

### The duplicate MCP problem

When the gateway starts, it launches all configured MCP servers as subprocesses. When a kanban worker (or any child Hermes process) spawns, it reads the same `mcp_servers:` config and starts its OWN copies. The originals continue running under the gateway, so you end up with N× copies where N = number of active Hermes processes.

Detect duplicates:
```bash
# List running MCP processes — look for same-name processes with different PIDs
ps aux | grep -E "mcp|tradingview|wundertrading|gbrain" | grep -v grep

# Check Hermes MCP config
hermes mcp list
```

### Fix: remove unused MCP servers from config

If trading MCP servers (tradingview, wundertrading) are only needed during active trading sessions, remove them from config so they don't spawn on every Hermes process:

```bash
hermes mcp remove <name>     # Removes from config.yaml permanently
hermes mcp add <name>        # Re-adds later when needed (re-runs setup)
```

Alternatively, disable in config:
```yaml
mcp_servers:
  servername:
    ...
    enabled: false    # Hermes skips this server entirely
```

After removal, the change takes effect on next Hermes/gateway restart. The running gateway still has live MCP processes — kill them manually if immediate recovery is needed:
```bash
kill <pid_of_stale_mcp>
```

### Re-adding removed servers

```bash
hermes mcp add tradingview --command uvx --args "--from tradingview-mcp-server tradingview-mcp"
hermes mcp add wundertrading --command python3 --args "/root/work/trading/wundertrading_proxy_server.py"
```

### RAM optimization on constrained VPS (≤2GB)

These three adjustments have the highest impact on RAM-constrained Hermes instances:

**1. Reduce swappiness (immediate + persistent)**

Default is 60-80 on many distros. The kernel swaps running processes to disk eagerly even when file cache could be dropped instead. Lowering to 10-30 keeps Hermes/gateway processes in RAM:
```bash
sysctl vm.swappiness=10                    # immediate
echo "vm.swappiness=10" >> /etc/sysctl.conf # persistent
```

**2. Enable zswap (if compiled into kernel)**

Zswap intercepts swapped pages and compresses them in-RAM before writing to disk. Reduces effective swap footprint by ~50-70%. Check availability:
```bash
# Check if zswap is compiled in
cat /sys/module/zswap/parameters/enabled 2>/dev/null || echo "not compiled"
# Enable at runtime
echo 1 > /sys/module/zswap/parameters/enabled
# Make persistent via systemd-tmpfiles
echo 'w /sys/module/zswap/parameters/enabled - - - - Y' > /etc/tmpfiles.d/zswap.conf
```

**3. Profile Python RSS footprint**

On a 2GB server, Python processes easily consume 40-50% of RAM. Run `ps aux | sort -k4 -r | head -10` to identify the heaviest processes. The Hermes gateway alone can be 400+ MB. Know your baseline before making other changes.

### Typical recovery

| Fix | Savings | Risk |
|-----|---------|------|
| Remove trading MCP servers (not needed for non-trading sessions) | ~100-120MB per Hermes process | Low — re-add when needed |
| Reduce swappiness from 80 to 10 | ~300-500MB swap reduction | Low — can revert with `sysctl vm.swappiness=80` |
| Enable zswap | ~200-400MB effective on swap | Low — built-in kernel feature |

### Pitfalls

- `hermes mcp configure <name>` requires an interactive terminal and cannot be scripted. Use `hermes mcp remove` for non-interactive config changes.
- Removed MCP servers lose their tool availability for the current Hermes session (/reload-mcp after re-adding).
- Zswap compressor defaults to `lzo` — acceptable for most workloads. `zstd` gives better compression ratio if compiled in (`cat /sys/module/zswap/parameters/compressor`).
- `enabled: false` prevents server startup but the entry remains in `hermes mcp list` (shown as disabled).

## Routine Mnemosyne Health Check

Periodic maintenance to keep Mnemosyne's vector embeddings consolidated and catch early signs of DB corruption before they become crashes.

### Check frequency

- After any heavy session day (30+ messages)
- Weekly as part of the self-audit
- When Mnemosyne recall seems slower or less relevant than usual

### Procedure

```bash
# Step 1 — Diagnose
hermes mnemosyne diagnose

# Step 2 — Check the vector count
# Look for `episodic_vectors` in the diagnose output.
# If < 10 or 0 after a full day's work, consolidation is stale.

# Step 3 — Consolidate
hermes mnemosyne sleep --all-sessions
```

### What to look for in the output

| Metric | Healthy | Needs attention |
|---|---|---|
| `checks_failed` | 0 or 1 | ≥ 2 — investigate |
| `episodic_vectors` | ≥ 10 and growing | 0 — consolidation not running |
| `working_total` | Growing steadily | Flat = no new memories being formed |
| `episodic_total` | ≥ working_total × 0.05 | Very low = episodic summarizer inactive |

### Error patterns in consolidation output

- **`database disk image is malformed`** on specific session IDs — isolated session corruption, not DB-wide. Safe to ignore for old/stale sessions. If the count grows, run a full integrity check:
  ```bash
  sqlite3 ~/.hermes/mnemosyne/data/mnemosyne.db "PRAGMA integrity_check;"
  ```
  If that returns `ok`, the corruption is isolated to session FTS5 shadow tables — refer to `references/mnemosyne-recovery.md` for the full recovery procedure.

- **LLM-consolidation errors** — `llm_used: 0` is normal for the automatic (AAAK) consolidation path. `llm_used` only increments when the semantic summarizer (which requires an LLM) runs. If `summaries_created` is also 0 on a session with 50+ items, something is wrong.

- **Degraded consolidation** — `tier1_to_tier2` / `tier2_to_tier3` degradation shows memory tier compaction. Non-zero values are normal as older memories age out. Rapid degradation across many sessions in one cycle suggests an over-aggressive cleanup setting.

### Pitfalls

- **Don't run `mnemosyne sleep` while the gateway is handling a live conversation** — consolidation reads the entire working memory table and can cause temporary recall latency. Schedule for downtime.
- **`--all-sessions` is safe** — it only consolidates sessions that have new items since last consolidation. Idempotent.
- **Episodic vec_type** (`int8` vs `float32`) affects recall precision but not correctness. The default `int8` is fine for Hermes; don't change it without benchmarking.

When the Mnemosyne memory provider (`memory.provider: mnemosyne`) fails to initialize or recall, the root cause is most commonly orphaned FTS5/vec0 shadow tables in the SQLite database — virtual table entries got dropped (crash, interrupted migration) but their internal shadow tables persisted. This triggers:

```
fts5: error creating shadow table fts_episodes_data: table 'fts_episodes_data' already exists
```

And after fixing that, a secondary WAL-journal corruption may produce:

```
database disk image is malformed
```

Full recovery procedure — diagnosis scripts, shadow table cleanup, WAL checkpoint + VACUUM, and end-to-end verification — is documented in:

`references/mnemosyne-recovery.md`

Load this reference when a user reports Mnemosyne failing on import or recall, or when `hermes memory status` shows errors.

**Key distinction:** The `hermes-agent` skill's `references/mnemosyne-memory-provider.md` covers installation, activation, config pitfalls (duplicate YAML keys), and graceful degradation. This reference covers **recovery** after the DB is already corrupt and the provider won't initialize.

### Pitfalls

- **`grep -v` kills set -e** — `grep` returns exit 1 when no lines match. In scripts with `set -e`, wrap grep pipelines with `|| true` to prevent spurious exits.
- **`pip index versions` in cron** — requires network and the Hermes venv's Python. Hardcode `VENV_PYTHON=/usr/local/lib/hermes-agent/venv/bin/python3` if the default system Python doesn't have the package installed.
- **GitHub API rate limits** — unauthenticated requests are limited to 60/hour. The nightly self-audit makes 2 GitHub API calls (Hermes releases + DOGA releases), well within limit.
- **Tag vs HEAD mismatch** — `git describe --tags` may return the same tag as origin even when there are commits ahead. Use `rev-list --count` for accurate staleness, not tag comparison.
- **no_agent mode ignores prompt** — When `no_agent=True`, the LLM never runs. The script's stdout IS the message. Design the script to `exit 0` silently on no-changes and `echo` the report on changes.
- **Keep the manifest updated** — Add an entry every time you install something. A stale manifest is worse than no manifest (creates false confidence).
- **Dashboard process locks Mnemosyne DB** — If the dashboard (`hermes dashboard`) is running when the gateway starts, it holds an open handle on mnemosyne.db. If the gateway recreates the DB (fresh init, migration), the dashboard's file descriptors point to the deleted inode, preventing the gateway from acquiring a fresh lock. Mnemosyne init fails with "database is locked." **Fix:** kill the stale dashboard process (`kill <PID>`) and restart the gateway. Prevent by starting gateway before dashboard, or by restarting dashboard after any DB migration.
  - **Root cause — systemd auto-start:** The dashboard is often a systemd user service (`~/.config/systemd/user/hermes-dashboard.service`) that is **enabled** at login. It auto-starts after `hermes-gateway.service` and runs until logout. If you don't use the dashboard regularly, disable the auto-start: `systemctl --user disable hermes-dashboard.service`. Start it on-demand with `systemctl --user start hermes-dashboard.service` when needed.
