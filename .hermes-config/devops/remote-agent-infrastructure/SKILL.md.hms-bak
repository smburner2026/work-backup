---
name: remote-agent-infrastructure
description: Setting up mobile/remote access infrastructure for operating AI agents from anywhere. Covers Tailscale mesh networking, Termux mobile Linux environment, tmux session persistence, git as agent memory layer, and the script-everything discipline.
version: 1.1.0
---

# Remote Agent Infrastructure

## The 5-Point Foundation

A viral post from the agentic-coding community distilled the infrastructure that makes mobile agentic work viable. The insight: the first few steps of your setup matter more than any model or framework you pick later.

### 1. Tailscale — Mesh Network
Private mesh VPN across every machine you own. Laptop, desktop, rented VPS, all on one secure tailnet, reachable from anywhere. Nothing else works well until this does.

**Setup:**
```bash
# On VPS/server
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# On phone: install from Play Store, authenticate to same tailnet
# On laptop: same
```

All devices on the same tailnet can reach each other via Tailscale IPs or `tailscale ssh`.

### 2. Termux — Mobile Linux Node
**Termux** (not Termius — common confusion) is the open-source Android terminal emulator that gives you a full Linux userland on your phone. It makes the phone a **first-class compute node** on the mesh, not just an SSH client.

| Tool | What it is | Role in stack |
|------|-----------|---------------|
| **Termux** | Android Linux terminal emulator | Turns phone into a Linux node — run agents, git, scripts directly |
| **Termius** | Proprietary SSH client (cross-platform) | Thin client — phone is just a remote control |
| **SSH** | Standard protocol | Connection method over Tailscale |

**Setup:**
- Install from **F-Droid** (Play Store version is stale/unmaintained)
- `pkg update && pkg upgrade`
- `pkg install openssh tmux git`
- Connect: `tailscale ssh user@vps-ip` or SSH over Tailscale IP

**Adding a new device's SSH key to the VPS:**

When SSHing from a new device (laptop, phone Termux) and the VPS uses key-only auth, the device needs its public key in `~/.ssh/authorized_keys` on the VPS.

From the new device, generate a fresh key (NOT host keys — the user likely ran `ssh-keygen` without realizing it generated host keys instead of user keys; the distinction matters):

```bash
# Generate a user SSH key (NOT a host key)
ssh-keygen -t ed25519 -C "<device-name>"
# Accept defaults, no passphrase unless paranoid
cat ~/.ssh/id_ed25519.pub
```

The `-C` comment helps identify which device the key belongs to (`-C "phone"`, `-C "laptop"`, etc.). Copy the output—it starts with `ssh-ed25519 AAA...`.

Then add it to the VPS's authorized_keys (either paste into `~/.ssh/authorized_keys` on the VPS, or have the agent append it via terminal):

```bash
echo "ssh-ed25519 AAA... <comment>" >> ~/.ssh/authorized_keys
```

Verify immediately from the new device:

```bash
ssh root@<vps-tailscale-ip>
```

First connection asks to verify the host key fingerprint — type `yes` to accept and store it permanently. This only happens once per device per host. Subsequent connections are silent.

**File transfers from phone to VPS over Tailscale:**

Once SSH works, use SCP over the tailnet IP to move files:

```bash
scp /storage/emulated/0/Download/myfile.zip root@100.x.y.z:/root/
```

**Critical prerequisite:** Android restricts Termux's file access by default. Run once (grants storage permission):

```bash
termux-setup-storage
```

This symlinks `~/storage/downloads`, `~/storage/dcim`, etc. from `/storage/emulated/0/`. After permission is granted, the SCP command uses the tailnet IP (not the public IP) so traffic is peer-to-peer over the mesh — faster and never touches the public internet.

**Large file tip:** SCP over Tailscale is direct P2P once a direct connection is established. If the Tailscale connection is relayed (DERP), it may be slower than the public IP. `tailscale status` shows the connection path. SCP native encryption on top of WireGuard is redundant but harmless.

### 3. tmux — Session Persistence
Persistent terminal sessions. Disconnect, close the laptop, come back — every session exactly where you left it. Agentic work runs long (model downloads, batch processing, overnight experiments); your terminal has to survive network drops, device switches, and laptop closures.

**Basic workflow:**
```bash
tmux new-session -s agentwork   # Start a session
Ctrl+B D                        # Detach (leave running)
tmux attach -t agentwork        # Reattach from anywhere
```

### Auto-start tmux on boot (systemd)

For a VPS that should always have a persistent Hermes session ready, wrap the tmux session in a systemd service. This survives reboots without manual SSH intervention.

**Service file** (`/etc/systemd/system/tmux-workbench.service`):

```ini
[Unit]
Description=Persistent tmux workbench with Hermes
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
User=root
Environment=HOME=/root
Environment=PATH=/root/.hermes/node/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/usr/bin/tmux new-session -d -s workbench -n herm '/root/.hermes/node/bin/herm'
ExecStop=/usr/bin/tmux kill-session -t workbench

[Install]
WantedBy=multi-user.target
```

Key design choices:
- `Type=oneshot` + `RemainAfterExit=yes` — the ExecStart creates a detached tmux session and exits; systemd considers the service "active" because the session persists independently.
- `ExecStop` — kills the tmux session on `systemctl stop`.
- PATH must be explicit — tmux doesn't load non-interactive shell configs, so herm's Node.js shim and bun won't be found without it.

**Install and enable:**
```bash
systemctl daemon-reload
systemctl enable tmux-workbench.service
systemctl start tmux-workbench.service
```

**.bashrc auto-attach** — so SSH logins land directly in the workbench:

```bash
# Tmux auto-attach — if SSHing in and workbench session exists, attach
if [ -z "$TMUX" ] && [ -n "$SSH_TTY" ]; then
    if tmux has-session -t workbench 2>/dev/null; then
        tmux attach-session -t workbench
    fi
fi
```

The `[ -z "$TMUX" ]` guard prevents nesting inside an existing tmux. The `[ -n "$SSH_TTY" ]` guard skips local terminals and non-interactive sessions (scp, rsync, git-over-SSH).

**Verification:**
```bash
systemctl status tmux-workbench.service          # Should show active (exited)
tmux list-sessions                                # Should show 'workbench'
tmux capture-pane -t workbench -p | head -5       # Should show Hermes running
```

**tmux.conf basics** (placed at `~/.tmux.conf`):
```tmux
set -g mouse on                                   # Click to focus panes, drag to resize
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",*256col*:Tc"         # True colour support
set -g status-style "bg=#1a1b26,fg=#a9b1d6"      # Clean dark status bar
set -g status-left " #[fg=#7dcfff]#S #[default]"
set -g status-right "#[fg=#7dcfff] %H:%M #[default]"
bind -n M-Left select-pane -L                     # Alt+arrows switch panes
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D
set -g history-limit 50000                        # Large scrollback
set -sg escape-time 0                             # No Esc delay
set -g base-index 1                               # Window numbering starts at 1
```

**Pitfall — PATH in non-interactive shells:** The systemd service and tmux both run in non-interactive contexts. If `herm` or `herm --version` succeeds manually but fails when the service starts, the cause is almost always a missing PATH entry for bun or the Hermes node bin. Set PATH explicitly in the service file's `Environment=` — never rely on .bashrc or .profile.

### 4. Private Git Repo — Agent Memory Layer
The repo is the durable memory across all your agent sessions. Agents pull context, work, commit results, merge back. Context that would die in a chat window lives in the repo instead. Same principle as Hermes skills but at the infrastructure level.

Your existing workflow (pre-task pull → commit+push on completion) is exactly right.

### 5. Script Everything
SSH aliases for every node, setup scripts, boring boilerplate automated. If you'll do a thing more than twice, it's a script.

**The meta-habit:** Ask the AI itself for the config, the error, the fix. Let the agent do the lifting, then double-check what it hands you.

> Everything past these five is decorative. Know these cold.

## Implementation Order

1. **Tailscale first** — VPS + phone + laptop on the same tailnet. This unlocks everything else.
2. **Termux on phone** — F-Droid, not Play Store.
3. **SSH connection** — `tailscale ssh` or direct SSH over tailnet IP.
4. **tmux session** — start one on the VPS, detach, reattach from phone. Verify persistence by disconnecting and reconnecting.
5. **Git setup** — clone your work repo in Termux so you can pull/push from the phone.
6. **First script** — an alias that SSHs into the VPS and attaches the main tmux session in one command.

## Web UI Access via Tailscale

**User approach preference:** When deploying infrastructure on this VPS, always present a plan with options (including tradeoffs and risks) before executing anything. Check the simplest option first before building decision trees — if a `curl | bash` install script exists, read it and try it before designing a custom sequence. Do not SSH in and start running commands without a plan the user has seen and approved. The user prefers to execute commands themselves from their SSH terminal; run verification checks from the agent side after they report back.

Beyond SSH access, the tailnet enables **browser-based control planes** for your agent. Instead of SSHing in to check sessions or run commands, you run a web UI alongside the agent and access it as a bookmark.

**The pattern:**

```
Tailscale mesh (private, no internet exposure)
├── Phone (browser) ──▶ http://100.x.y.z:3000  ──▶ Hermes Workspace / WebUI
├── Laptop (browser) ──▶ http://100.x.y.z:3000  ──▶ Hermes Agent (:8642)
└── VPS (server)
      └── Web UI (:3000) ↔ Hermes Agent gateway/dashboard
```

**Three access methods, from best to worst:**

| Method | Daily use | Security | Setup cost |
|--------|-----------|----------|------------|
| **Tailscale mesh** (recommended) | Bookmark, open, done. No SSH, no tunnel, no passwords. | Only devices in your tailnet can reach it. Zero internet exposure. | Install Tailscale + auth once per node |
| **SSH tunnel** (fallback) | `ssh -L 3000:localhost:3000 user@vps` then open `localhost:3000` | Port-forward over SSH, safe but requires a terminal | Terminal open every session |
| **Direct exposure** (avoid) | `http://vps-ip:3000` with password auth | Port open to internet, bots can probe, must manage SSL + auth | Caddy/nginx + cert renewal + auth |

**Tailscale is the right choice for daily operation.** Once the VPS is on the tailnet, the workspace URL is just `http://<tailscale-ip>:<port>` — no ports open, no credentials to type, no tunnel to maintain. The same URL works from every device on the mesh.

### Deploying a Web UI (Hermes Workspace pattern)

The "attach to existing agent" path is the fastest for machines already running Hermes Agent:

```bash
git clone https://github.com/outsourc-e/hermes-workspace.git
cd hermes-workspace
cp .env.example .env
```

**Required `.env` values for VPS deployment:**

| Variable | Value | Why |
|----------|-------|-----|
| `HERMES_API_URL` | `http://127.0.0.1:8642` | Workspace talks to agent on same machine |
| `HERMES_API_TOKEN` | `<value from ~/.hermes/.env API_SERVER_KEY>` | Must match the agent's API key |
| `HOST` | `0.0.0.0` | Reachable via Tailscale from other devices |
| `HERMES_PASSWORD` | `<random strong string>` | Required by Workspace when binding to 0.0.0.0 |
| `COOKIE_SECURE` | `0` | Plain HTTP over Tailscale; browsers drop Secure cookies over http:// |

**Agent-side prerequisites (check `~/.hermes/.env`):**
- `API_SERVER_ENABLED=true`
- `API_SERVER_KEY=<some-secret>` (Workspace uses the same value as `HERMES_API_TOKEN`)
- `API_SERVER_HOST=127.0.0.1` is fine — Workspace connects locally

**Memory-constrained VPS pitfall (≤2GB RAM):** The production Vite build (`pnpm build`) gets OOM-killed on small VPS instances — 2600+ modules spike memory over 2GB during chunk rendering.

**❌ Dev mode is NOT a clean workaround.** Two blockers:
1. The npm script hardcodes `NODE_OPTIONS="--max-old-space-size=2048"` — overrides any env var you set.
2. Dev mode runs `concurrently "hermes gateway run" "vite dev"` — tries to spawn a second gateway at a binary path that doesn't exist on pip-based installs.

**✅ Fix: swap + gateway-pause sequence**
```bash
# Add swap (one-time)
dd if=/dev/zero of=/swapfile bs=1M count=1024
chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Stop gateway, build, restart
systemctl --user stop hermes-gateway
cd ~/hermes-workspace
npm run build               # or pnpm run build
systemctl --user start hermes-gateway
```

After the build, the workspace production server starts via:
```bash
export HOST=0.0.0.0
export HERMES_PASSWORD=<your-password>
cd ~/hermes-workspace
node server-entry.js
```

**⚠️ .env file is NOT auto-loaded.** The workspace's `server-entry.js` does NOT use dotenv. Values in `.env` have zero effect at runtime. The variables (`HOST`, `HERMES_PASSWORD`) must be in the environment at process start via:
- Systemd `Environment=` directives
- Shell `export` before launching
- Prepending: `HOST=0.0.0.0 HERMES_PASSWORD=<pw> node server-entry.js`
**Systemd service for production persistence:**

```ini
# Path: ~/.config/systemd/user/hermes-workspace.service  (multi-user VPS)
# Or:   /etc/systemd/system/hermes-workspace.service     (root-only VPS)
[Unit]
Description=Hermes Workspace — Web UI for Hermes Agent
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
ExecStart=/root/.hermes/node/bin/node /root/hermes-workspace/server-entry.js
WorkingDirectory=/root/hermes-workspace
Restart=on-failure
RestartSec=5
Environment=HOST=0.0.0.0
Environment=HERMES_PASSWORD=<your-password>
Environment=NODE_OPTIONS=--max-old-space-size=1024

[Install]
WantedBy=default.target
```
```bash
systemctl --user daemon-reload
systemctl --user enable hermes-workspace
systemctl --user start hermes-workspace
```

**PATH note:** `pnpm` may not be in SSH login PATH even after Hermes installs it (it lives at `/root/.hermes/node/bin/pnpm`). Fall back to `npm run build` if `pnpm` is not found.

### Tailscale Auth Flow (Common Issues)

Tailscale auth links expire and can give a `bad tailscale-authstate2 cookie` error if stale.

**Fix:** Regenerate the URL from the target machine:
```bash
# On the VPS/device that needs to authenticate
tailscale up
# This prints a fresh login URL
```

Open the new URL in a **regular browser** (not an in-app browser like Telegram/Discord), on any device. Authentication is OAuth-based — it doesn't need to happen on the same machine. Once authenticated, the device appears in the tailnet immediately with a `100.x.y.z` IP.

**After authentication**, `tailscale status` on any device shows the full mesh:

```
100.113.2.25     vps-hostname     user@  linux    -
100.102.166.100  laptop-name      user@  windows  -
100.65.99.106    phone-name       user@  android  -
```

All devices on the same tailnet can reach each other by these IPs. No ports need to be open to the internet.

**Always keep SSH as break-glass.** Tailscale can have hiccups. A workspace can crash. SSH is how you fix things when the web UI is down. The ratio shifts from "SSH to do anything" to "SSH only when something's on fire."

On Android, install **Termux from F-Droid** (not Play Store — Play version is stale) and `pkg install openssh`. Then SSH over the tailnet IP:

```bash
ssh root@100.113.2.25
```

This uses the same SSH key/password as your laptop, no additional config needed. Termux inherits the phone's Tailscale network — you don't need Tailscale inside Termux.

**Service persistence:** Wrap the web UI in systemd (or run via Docker with `restart: always`) so it survives VPS reboots without manual intervention. The user should never need to SSH in just to restart the workspace.

**Key pitfall:** Do not publish the workspace directly to the internet even with password auth. Tailscale mesh is the only layer that keeps bot traffic, credential stuffing, and zero-day exploits away from your agent's control plane. If you need to share access, add another device to the tailnet — don't open a port.

## VPS → Local Machine SSH Bridge (Reverse Direction)

Beyond connecting from mobile/laptop to the VPS, an equally important pattern is having the VPS connect back to local machines (WSL, desktop, dev laptop) so the always-on hub can push work to the compute node.

### Architecture

```
VPS (hub, always-on) ──[Tailscale mesh]──→ Local WSL (compute plane)
      │                                            │
      ├── Telegram/Discord gateway                 ├── Heavy compute (32GB RAM)
      ├── Cron jobs                                 ├── Code compilation
      └── File server                               └── Training/inference
```

The key requirement: **WSL needs its own Tailscale identity**, independent of the Windows host. The Windows host's Tailscale IP is not the WSL's — WSL runs inside a virtual network behind Windows NAT. Without its own Tailscale identity, the VPS cannot directly reach the WSL SSH server.

### Prerequisites

- Both machines on the same Tailscale tailnet
- SSH server installed and running on the target local machine
- Local machine has its own Tailscale identity (not just the host OS)

### Setup Steps

**Step 1 — Install Tailscale inside WSL (separate from Windows host)**

```bash
# Inside WSL terminal:
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Authenticate in browser when prompted. Verify:

```bash
tailscale ip -4
# → 100.x.y.z (WSL's own tailnet IP, NOT the Windows host's)
```

**Step 2 — Enable SSH server on WSL**

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable ssh --now
# Verify:
sudo systemctl status ssh --no-pager
```

If systemd is flaky on your WSL build (common on older installs):

```bash
sudo ssh-keygen -A     # generate host keys if missing
sudo /usr/sbin/sshd    # start manually
```

**Step 3 — Generate SSH key on the connecting machine (VPS)**

```bash
# On the machine that will initiate connections (e.g., VPS):
ssh-keygen -t ed25519 -C "vps-to-local-wsl" -N ""
cat ~/.ssh/id_ed25519.pub
```

Use a descriptive `-C` comment so you know which key belongs to which connection.

**Step 4 — Install public key on WSL**

```bash
# On WSL:
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo 'ssh-ed25519 AAA... <comment>' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Step 5 — Create SSH config entry on VPS**

```bash
# On VPS, add to ~/.ssh/config:
cat >> ~/.ssh/config << 'EOF'

Host wsl
    HostName <WSL_TAILSCALE_IP>
    User <wsl_username>
    IdentityFile ~/.ssh/id_ed25519_vps2local
EOF
```

**Step 6 — Test**

```bash
ssh wsl
# Should connect without password, landing in WSL shell
```

### Script Everything — Worked Example

Once the SSH bridge works, immediately create wrapper scripts that encode the connection, execution, and file-sync patterns. This is what "Script Everything" looks like in practice — you should never need to remember flags, paths, or hostnames.

**Trio of canonical wrappers for any VPS→local bridge:**

**1. `connect-local.sh`** — Drop-in SSH replacement. Run with no args for interactive shell; pass a command to execute non-interactively.

```bash
#!/bin/bash
# Connect to local WSL machine
# Usage: ./connect-local.sh [command]
ssh local-machine "$@"
```

**2. `run-local.sh`** — Explicit remote-execution script. Same as `connect-local.sh` but with a `--help` guard and stricter error handling — useful when an agent or cron script needs to invoke remote commands expectably.

```bash
#!/bin/bash
# Run a command on local WSL and return output
# Usage: ./run-local.sh <command>

if [ $# -eq 0 ]; then
  echo "Usage: $0 <command>"
  exit 1
fi

ssh -o ConnectTimeout=10 local-machine "$@"
```

**3. `sync-local.sh`** — Bidirectional rsync wrapper with pull/push direction control and optional single-volume mode. Prevents the common mistake (made in this session) of syncing the wrong direction and overwriting newer files with stale ones.

```bash
#!/bin/bash
# Usage: ./sync-local.sh [pull|push] [volume]
# pull — copies FROM local WSL TO VPS (overwrites VPS files)
# push — copies FROM VPS TO local WSL (overwrites WSL files)

ACTION=${1:-pull}
VOL=${2:-all}
LOCAL_DIR="/home/vthen/work/post-colonial-vietnam/sources/vstb/"
VPS_DIR="/root/work/post-colonial-vietnam/sources/vstb/"
PATTERN="viet-su-tan-bien-quyen-*.txt"

if [ "$VOL" != "all" ]; then
  PATTERN="viet-su-tan-bien-quyen-${VOL}.txt"
fi

if [ "$ACTION" = "push" ]; then
  echo "PUSH: VPS → local WSL"
  rsync -avz --include="$PATTERN" --exclude="*" "$VPS_DIR" "local-machine:${LOCAL_DIR}"
elif [ "$ACTION" = "pull" ]; then
  echo "PULL: local WSL → VPS"
  rsync -avz --include="$PATTERN" --exclude="*" "local-machine:${LOCAL_DIR}" "$VPS_DIR"
fi
```

**Common pitfalls with wrapper scripts:**

- **Path hardcoding is a feature, not a bug.** Scripts that hardcode `/root/work/...` work on the VPS but fail on WSL where the user is `vthen` and paths are `/home/vthen/work/...`. Fix by either:
  - **Symlink**: `sudo ln -sf /home/vthen/work /root/work` on WSL (requires sudo).
  - **Copy-and-modify**: `cp ocr_resumable.sh ocr_resumable_local.sh && sed -i 's|/root/work|/home/vthen/work|g' ocr_resumable_local.sh` — run the local variant on WSL.
- **SSH config deduplication.** Appending a duplicate `Host local-machine` block adds the keys from both blocks (SSH merges them) but creates a messy config. If you're programmatically adding a block when one already exists, remove the old one first or use `sed` to update in place. A config with duplicate Host stanzas works but is harder to debug.
- **rsync direction matters.** The agent's `sync-local.sh` started as a `pull`-only script. When used to sync from WSL→VPS after both sides had made progress, it overwrote the VPS's newer copies with WSL's stale ones. Explicit `pull`/`push` arguments prevent this. The two-letter mnemonic: you **push** from the machine you're on, you **pull** from the machine you're not on.

### Pitfalls

- **WSL needs its own Tailscale IP.** The Windows host's Tailscale IP (`tailscale status` from the VPS shows `desktop-b4lb6vl windows`) is NOT the WSL's IP. WSL runs on a virtual NAT behind Windows. Installing Tailscale inside WSL gives it a separate identity on the tailnet — only then can the VPS reach it directly. Without this, port forwarding on the Windows host is required.
- **WSL systemd can be unreliable.** `sudo systemctl enable ssh --now` may succeed without actually starting sshd. Always verify with `sudo systemctl status ssh --no-pager` — the output should show `Active: active (running)`. If systemd is broken, fall back to `sudo /usr/sbin/sshd`.
- **Typo traps when pasting commands:**
  - `https:tailscale.com/install.sh` → missing `//` → `curl: (3) URL rejected`
  - `https://tailscale.com/install.sk` → `.sk` instead of `.sh` → same error
  - `~/.ssh/authorized_keys~` → trailing tilde in filename → `chmod: cannot access`
- **Port 22 on Windows host is not WSL.** Even if Windows runs an SSH server, it serves the Windows filesystem, not WSL. WSL's SSH server listens inside its own network namespace. Tailscale inside WSL solves this cleanly.
- **Key file naming:** Use descriptive key names (`id_ed25519_vps2local` rather than bare `id_ed25519`) so you can manage multiple keys without confusion.
- **Host key verification on first connection:** First `ssh wsl` will prompt `The authenticity of host '<ip>' can't be established...` — type `yes` to accept. This only happens once.

## Architecture Note

This 5-point single-operator setup is the same architecture as a GKE cluster with self-hosted models, just at a different scale:

| | This setup | Cluster scale |
|---|---|---|
| **Network** | Tailscale mesh | VPC / service mesh |
| **Compute** | Phone + laptop + VPS | GPU node pool |
| **Session mgmt** | tmux | K8s pods / orchestration |
| **Memory** | Git repo | Object store / DB |
| **Automation** | Shell scripts | CI/CD, operators |

Both distribute access to compute across nodes. The cluster version buys you model multiplexing and autoscaling; the single-operator version buys you simplicity and zero DevOps overhead.

## Pitfalls

- **Termux ≠ Termius.** These get confused constantly. Termux is the open-source Android Linux terminal emulator (the phone becomes a compute node). Termius is a proprietary cross-platform SSH client (the phone is a thin remote). The 5-point foundation uses Termux because the phone is a first-class mesh participant.
- **Play Store Termux is stale** — the Android Play version hasn't been updated since a Google Play policy change forced Termux off the store. Install from **F-Droid** or GitHub releases.
- **Network drops kill raw SSH** — without tmux, a dropped connection kills your running agent mid-task. tmux is non-negotiable for agentic work.
- **Android may kill Termux in background** — use `termux-wake-lock` for long-running tasks. Check battery optimization settings.
- **Termux `Permission denied` when accessing phone files** — Termux starts without Android storage access. Run `termux-setup-storage` once to trigger the permission dialog and symlink `~/storage/` to `/storage/emulated/0/`. After that, use path `~/storage/downloads/filename` instead of `/storage/emulated/0/Download/filename`.
- **Git conflicts across devices** — if laptop and phone agents modify the same files, you'll hit merge conflicts. Establish a convention (e.g., phone is read-only for code, laptop is write-authoritative; or use branches per device).
- **Git repo Permission denied after cross-machine sync** — a git repo synced from one machine/user to another (e.g., WSL `vthen`/UID 1000 → VPS `root`/UID 0) preserves the original UID ownership in `.git/`. The clone works on the target machine only because root bypasses permissions, but the UID is orphan (nonexistent user). If a script or cron tries to access it as a non-root user, it crashes with `Permission denied`. Symptom: `ls -la /root/work/.git/` shows files owned by `1000:1000` and `getent passwd 1000` returns nothing. Fix: `chown -R root:root /root/work/.git/` on the VPS (authoritative machine), or clone separate per-machine working copies. See `references/git-cross-environment.md` for full diagnostic and repair guide.
- **Tailscale SSH vs tailscale serve** — `tailscale ssh` gives you SSH access to a machine over the mesh. `tailscale serve` exposes a local HTTP service on your tailnet. They solve different problems.
- **WSL Tailscale does NOT carry over to Windows** — Tailscale inside WSL is its own Linux network identity. Windows-native apps (including Hermes Desktop) can't reach tailnet IPs unless Windows itself has Tailscale installed. The reverse is also true: `ping 100.x.y.z` from Windows requires Windows Tailscale, not WSL Tailscale.
- **VPNs block Tailscale** — NordVPN, ExpressVPN, and similar can interfere with Tailscale's WireGuard connection. If ping fails over the tailnet and both sides show connected in `tailscale status`, try disconnecting the VPN as a diagnostic step.
- **Stale Tailscale auth URL** — if the user gets `bad tailscale-authstate2 cookie` when opening the auth link, the URL has expired. Run `tailscale up` on the target machine to regenerate it. Open in a regular browser (not in-app Telegram/Discord browser).
- **Web UI production build OOM on small VPS** — `pnpm build` spikes well over 2GB during chunk rendering on a 2600+ module codebase, getting OOM-killed on 2GB VPS. Dev mode is NOT a fix — the npm script hardcodes `--max-old-space-size=2048` and tries to spawn a second gateway process. The working fix: add 1GB swap, stop gateway, run `npm run build`, restart gateway. See "Memory-constrained VPS pitfall" section above for the exact sequence and systemd setup.
- **Node does not auto-load .env files** — workspace's `server-entry.js` does NOT use dotenv. Setting `HOST=0.0.0.0` and `HERMES_PASSWORD=<pw>` in `.env` has zero effect at runtime. These must be actual environment variables: systemd `Environment=` directives, shell `export`, or prepended to the command. Without explicit export, the server binds to `127.0.0.1` (unreachable via Tailscale) and/or refuses to start with "HERMES_PASSWORD is unset".
- **Gateway restarts kill tmux-hosed web UIs** — if the web UI runs in a tmux session on the same machine as the Hermes Agent, a gateway restart can kill the tmux process. Wrap the web UI in systemd for production persistence, not tmux.

## Verification

- [ ] Can you `tailscale ping <vps-hostname>` from your phone?
- [ ] Can you SSH into the VPS from Termux?
- [ ] Can you start a tmux session on VPS, detach, close Termux, reopen, and reattach?
- [ ] Can you `git pull` and `git push` from the phone?
- [ ] Does your one-command reconnect script work?

## Hermes Desktop Remote Gateway

The official Hermes Desktop (Nous Research Electron app) can connect to a VPS agent via the **dashboard** service on port 9119, not the API server on port 8642. See the dedicated reference for full setup.

**Quick start:**
```bash
# On the VPS — generate token, start dashboard
TOKEN=$(openssl rand -hex 32)
echo "HERMES_DASHBOARD_SESSION_TOKEN=$TOKEN" >> ~/.hermes/.env
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open --tui
```
Desktop app → Settings → Gateway → Remote gateway → URL `http://<tailscale-ip>:9119` + session token.

**After a failed connection attempt:** fully close the app (check system tray!), reopen, then re-enter URL + token. The app caches stale connection state.

**Dashboard does not survive reboots** without systemd wrapping — see `references/hermes-desktop-remote-gateway.md` for the service file.

### Common trap — port confusion
- Dashboard port **9119** with `HERMES_DASHBOARD_SESSION_TOKEN` → **Desktop app remote gateway**
- API server port **8642** with `API_SERVER_KEY` → **OpenAI-compatible API, Open WebUI, third-party tools**

They are different services. Giving the desktop app the API server URL + key will fail to connect.

## Related

- `personal-workspace` — workspace folder structure and rsync sync
- `hermes-agent` references/vps-hetzner-setup.md — VPS deployment workflow
- `remote-agent-infrastructure` references/hermes-desktop-remote-gateway.md — Hermes Desktop remote gateway setup with Tailscale (port 9119, dashboard session token, common pitfalls)
- `remote-agent-infrastructure` references/hermes-workspace-deployment.md — detailed Workspace deployment guide including dashboard setup, OOM build fix, and systemd persistence
- `remote-agent-infrastructure` references/git-cross-environment.md — diagnosing and fixing git repo Permission denied after syncing between environments (UID ownership mismatch, orphan UIDs, cross-machine git crashes)
- `remote-agent-infrastructure` references/secure-config-backup.md — backing up Hermes config (~/.hermes/config.yaml, SOUL.md, memories, skills) to a git repo without leaking secrets. Covers staged sync, sed redaction of tokens, .env exclusion, and GitHub secret alert recovery.
- `remote-agent-infrastructure` references/bitwarden-secrets-manager.md — Bitwarden Secrets Manager (BWS) for Hermes Agent: BWS vs vault distinction, setup steps, Hermes config integration, secret redaction bypass for export, and VPS→local migration workflow.
- `remote-agent-infrastructure` references/vps-security-hardening.md — four-layer VPS security model (network → OS → application → supply chain/resilience). Firewall setup, SSH lockdown, non-root user, file permissions, service audit, auto-updates, fail2ban, kernel hardening, token hygiene, skill audit, backup strategy, and a post-hardening verification checklist.
- `remote-agent-infrastructure` references/gateway-conflicts.md — diagnosing and resolving Telegram polling conflicts when running multiple Hermes instances with the same bot token. Covers symptom identification, root cause, resolution (stop secondary gateway), and prevention.
