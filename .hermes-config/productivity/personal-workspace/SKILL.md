---
name: personal-workspace
description: Organizing and maintaining a personal workspace for non-technical users running Hermes with mixed study, research, and custom agent workloads. Encodes simplicity-first principles and durable folder structures.
---

# Personal Workspace

## Core Principles
- Keep structure simple and flat where possible.
- Separate concerns clearly: study material, research, agents, scripts, and outputs.
- Prefer local-first testing before introducing VPS or new tools.
- Data ingestion (chat histories, external texts) goes into `archive/` first, then processed into relevant folders.
- **Never delete anything without explicit user approval** — when cleaning/organising, move files to a staging area (`~/recycle-bin/YYYY-MM-DD/`) preserving original path structure. Report what was moved. Let the user review and decide on deletion. This applies to both automated maintenance and manual cleanup sessions.
- **Services should live IN the work directory, not point at it.** When deploying a service (Hermes Workspace, file browser, etc.) that needs access to your files, set its `WorkingDirectory` directly to the work path. Avoid config-level indirection like `terminal.cwd` pointing at a separate directory — it adds a conceptual hop with no performance benefit and can cause confusing path-resolution issues.

## Recommended Top-Level Structure

work/
├── dabt/                    # Domain-specific study (DABT in this case)
│   ├── references/
│   ├── deep-dives/
│   ├── notes/
│   └── practice/
├── research/                # General research and scheduled digests
│   ├── sources/
│   └── digests/
├── agents/                  # Custom agent personalities and their knowledge
│   └── [agent-name]/
│       ├── persona/
│       ├── knowledge/
│       └── outputs/
├── scripts/                 # Reusable Python utilities and tools
├── output/                  # Final compiled artifacts (PDFs, exports)
├── archive/                 # Raw imports and inactive material (Grok histories, large dumps)
└── __pycache__/             # Ignored / cleaned periodically

## Data Ingestion Workflow
1. Dump raw material (Grok exports, Substack extracts, etc.) into `archive/`.
2. Process in small chunks.
3. Move summarized or extracted content into the appropriate folder (`dabt/`, `agents/[name]/knowledge/`, etc.).
4. Save high-value user patterns via the memory tool rather than keeping raw logs.

## Style & Interaction Rules
- Default to minimal, direct responses.
- Avoid unnecessary explanations or scaffolding unless requested.
- When user says "just some thoughts" or is exploring, stay in planning mode and do not execute file changes until explicitly told to proceed.
- Never introduce new tools or complexity unless the current setup demonstrably cannot handle the task.

## Cross-Machine Sync (rsync)

Keep the workspace in sync between local machine and remote VPS.

### Safe Pull (VPS → Local, Recommended Default)
```bash
rsync -avz root@<vps-ip>:/root/work/ /home/<user>/work/
```
No `--delete` — only adds/updates, never removes local-only content.

### Full Mirror Push (Local → VPS)
```bash
rsync -avz --delete /home/<user>/work/ root@<vps-ip>:/root/work/
```
Use when you want exact parity (VPS becomes authoritative).

**Pitfalls**: `--delete` on pull can silently remove local work — always pull without it unless VPS is confirmed source of truth. Use `-n` (dry-run) first: `rsync -avzn ...`. Always run from the local machine.

---

## Windows Host Cleanup (via WSL)

When the user wants to clean their Windows C: drive from WSL:

1. Start with top-level scan: `ls -la /mnt/c/`
2. Size suspicious folders with `du -sh` (ignore E-size artifacts on junction/OneDrive folders)
3. Check `/mnt/c/Users/<user>/` for Downloads, Games, old copies

### Safe Zero-Risk Deletes
- `/mnt/c/adobeTemp/*` — stale Adobe installer temp folders
- `/mnt/c/DumpStack.log.tmp`
- `/mnt/c/OneDriveTemp/*`
- `/mnt/c/ProgramFilesFolder` — empty
- `/mnt/c/Intel` — ExtremeGraphics 2020 remnants + empty GfxCPLBatchFiles
- `/mnt/c/WindowsInstallationAssistant` — post-update remnant
- `/mnt/c/Users/<user>/.openjfx` — JavaFX native DLL cache

### Conditional Deletes (research first)
- **ControlD**: check for active `ctrld.exe`
- **$SysReset / $GetCurrent**: verify no pending Windows reset
- **Dell**: remove only if not using Dell hardware
- **NordUpdater/NordVPN**: remove only if VPN uninstalled

### Never Touch
- `/mnt/c/Windows/` (especially `LastGood.Tmp` — recovery snapshot)
- `pagefile.sys`, `hiberfil.sys`, `swapfile.sys`, `$Recycle.Bin`, System Volume Information, Recovery, RUXIM

### Redundant Installs
- Cross-check Steam: primary is always `/mnt/c/Program Files (x86)/Steam`. `Games/Steam` (1.2 GB) is redundant.

**Mandatory rule**: Before recommending deletion of any non-obvious folder, run `web_search` on its name + "safe to delete".

### Verification
- After cleaning Program Files, optionally run DeleteEmptyFolders utility in review mode.
- `du` produces nonsense sizes on junction-heavy/OneDrive folders — rely on file presence instead.
- Recommend native Disk Cleanup for deep AppData caches (WSL has limited visibility).

See `references/wsl-c-drive-cleanup-findings.md` for the exact folder decisions from the initiating session.

---

## Workspace Tidy Workflow

When the workspace needs reorganising (scattered files, misplaced build artifacts, old temps), use this pattern:

### The Recycle-Bin Pattern
Never delete anything. Instead:
1. Create `~/recycle-bin/YYYY-MM-DD/` with a subdirectory mirroring the original relative path.
2. Move files there rather than deleting.
3. Report what was moved and why.
4. The user reviews the bin contents later and decides what to keep or discard.

### What to Look For
- Build artifacts in source directories (`.pyc`, `__pycache__` outside venvs, `node_modules/` duplicates)
- Temp files older than 7 days (`*.tmp`, `*.log`, scratch output)
- Files clearly in the wrong directory (e.g. download PDFs sitting in a code project root)
- Orphaned log files
- Stray export/output files that should live in a structured location

### What NOT to Touch
- Configuration files (`.env`, `config.yaml`, `*.json`, `*.toml`)
- Version control directories (`.git/`, `.svn/`)
- Virtual environments (`venv/`, `.venv/`, `.hermes/`)
- Anything starting with a dot in the home directory
- Recently modified files (<24h) — likely in active use

### After the Move
Report a structured summary to the user:
- Total items moved
- Items per directory of origin
- Rationale per item (aged temp / build artifact / misplaced)
- Size freed (optional)
- Location in recycle bin so they can browse

---

## Mobile Access (Phone as Node)

When the user needs to reach the VPS away from their computer, use **Tailscale + Termux + SSH** as the emergency back door.

The normal path (Phone → Telegram/Discord → Hermes → VPS) handles 99% of use. The SSH back door is for:
- Hermes crashes or becomes unresponsive
- Telegram/Discord is unreachable
- Raw config edits, disk checks, reboots
- Any maintenance the agent shouldn't do

See `references/mobile-phone-vps-access.md` for the complete setup guide.

## VPS Service Configuration

The Hermes Workspace (port 3000) and Dashboard (port 9119) are the primary web UIs. Key configuration quirks when deploying on a VPS:

### Dashboard reachability
The Dashboard binds to `127.0.0.1` by default. To reach it via Tailscale, add `--host 0.0.0.0 --insecure` to the service's `ExecStart`. The `--insecure` flag is required because the Dashboard exposes API keys; Tailscale is your auth layer on a private tailnet.

### Workspace file browser root — the `/root` block
The Workspace blocks `/root` as a system directory (same as `/etc`, `/usr`). If your work lives under `/root/work/`, every candidate root path fails the security filter silently. Fix by setting `HERMES_WORKSPACE_DIR=/root/work` in the service environment — this bypasses the blocked-path filter.

### Workspace service WorkingDirectory
Set `WorkingDirectory=/root/work` so the Workspace naturally lives in the work directory rather than pointing at it via config. Safe because the server finds its assets via `__dirname`.

### HTTP login & COOKIE_SECURE
On plain-HTTP deployments (Tailscale LAN), set `COOKIE_SECURE=0` so the browser doesn't silently drop login cookies.

### Workers & profile toolsets
Worker profiles need toolsets beyond `hermes-cli` (at minimum `terminal`, `file`, `web`) to be functional when the kanban dispatcher spawns them. See the `hermes-soul-design` skill's `references/profile-worker-configuration.md` for the full guide including model/auth checks and the Dashboard/Workspace config reference.

## Pitfalls to Avoid
- Do not scatter agent-related files across multiple top-level folders.
- Do not put raw large imports directly into active folders (`dabt/`, `agents/`).
- Resist the urge to create many narrow subfolders early; expand only when volume justifies it.
- Do not set `terminal.cwd` to a path under `/root` and expect the Workspace file browser to pick it up — the blocked-system-paths filter will silently reject it. Use `HERMES_WORKSPACE_DIR` instead.
- Do not proxy the Workspace or Dashboard through a separate working-directory config. Set the service's `WorkingDirectory` directly.

## Future Expansion
- When a VPS is added, mirror the same structure on the remote machine.
- Use `agents/` as the home for reusable personality definitions.
