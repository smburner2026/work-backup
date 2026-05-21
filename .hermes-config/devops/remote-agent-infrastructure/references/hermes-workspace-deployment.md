# Hermes Workspace Deployment (VPS + Tailscale)

**Source:** Session where smburner2026 set up Hermes Workspace on a 2GB VPS with Tailscale mesh.

## Architecture

```
Browser (laptop/phone) ──▶ Workspace (:3000) on VPS ──▶ Hermes Agent gateway (:8642) + dashboard (:9119)
```

The Workspace runs alongside the existing Hermes Agent, connecting to it locally. No Docker, no fork, no reinstall.

## Agent-Side Prerequisites

In `~/.hermes/.env`:
```
API_SERVER_ENABLED=true
API_SERVER_KEY=<your-secret>          # Workspace needs this as HERMES_API_TOKEN
API_SERVER_HOST=127.0.0.1             # Fine — Workspace connects via localhost
API_SERVER_PORT=8642
```

## Workspace .env Configuration

File: `hermes-workspace/.env` (copy from `.env.example`)

```
HERMES_API_URL=http://127.0.0.1:8642
HERMES_API_TOKEN=<same as API_SERVER_KEY above>
HOST=0.0.0.0                           # Reachable via Tailscale from other devices
PORT=3000
HERMES_PASSWORD=<random-string>        # Required when HOST=0.0.0.0
COOKIE_SECURE=0                        # Plain HTTP over Tailscale (no HTTPS)
```

## Memory-Constrained Build (2GB VPS)

### The Problem
```
npm run build
vite v7.3.2 building...
✓ 2685 modules transformed.
rendering chunks...
Killed                                          ← exit code 137 = OOM
```

The Vite production build needs ~2GB+ during chunk rendering for a 2600+ module codebase. On a 2GB VPS with the Hermes gateway already using ~1.2GB peak, the OOM killer terminates it.

### Dev Mode Is NOT a Reliable Workaround

Dev mode (`pnpm dev` / `npm run dev`) has two blockers:

1. **The npm script hardcodes `NODE_OPTIONS="--max-old-space-size=2048"`** — any env var you set is overridden. 2GB heap on 2GB RAM still OOMs.
2. **The dev script runs `concurrently "hermes gateway run" "vite dev"`** — tries to spawn a second gateway at `/root/.hermes/hermes-agent/venv/bin/hermes`, which does not exist on pip-based installs.

### Working Fix: Swap + Gateway-Pause Sequence

**Step 1 — Add swap (one-time):**
```bash
dd if=/dev/zero of=/swapfile bs=1M count=1024
chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```
2GB VPS + 1GB swap = 3GB effective. The production build fits comfortably.

**Step 2 — Stop gateway, build, restart:**
```bash
systemctl --user stop hermes-gateway   # frees ~1.2GB
cd ~/hermes-workspace
npm run build                          # or pnpm run build (~35s)
systemctl --user start hermes-gateway
```
Total gateway downtime: ~2 minutes.

**Step 3 — Start workspace:**
```bash
export HOST=0.0.0.0
export HERMES_PASSWORD=<your-password>
cd ~/hermes-workspace
node server-entry.js
```

### PATH Note
`pnpm` may not be in SSH login PATH even after Hermes installs it (it lives at `/root/.hermes/node/bin/pnpm`). Fall back to `npm run build` if `pnpm` is not found.

### Build Script Limitation (install.sh)
The official install script (`curl -fsSL https://hermes-workspace.com/install.sh | bash`) does NOT run the production build. It clones the repo, installs deps, and sets up `.env` — stopping at `pnpm install`. You still need to run the build manually or start in dev mode.

## Systemd Service (Production Persistence)

Services can be deployed as either **user-level** (`~/.config/systemd/user/`) or **system-level** (`/etc/systemd/system/`). Which one depends on the VPS user model:

| Environment | Service path | Command | When to use |
|---|---|---|---|
| Multi-user VPS (sudo user) | `~/.config/systemd/user/` | `systemctl --user` | Default — Hermes Agent is installed under a non-root user with linger enabled |
| Root-only VPS (single root user) | `/etc/systemd/system/` | `systemctl` (no `--user`) | Dedicated VPS where everything runs as root; user systemd may lack a bus |

**Why user-level may fail on root-only VPS:** User systemd (`systemctl --user`) requires a user bus managed by `logind`. On a minimal VPS running everything as root with no desktop environment, the user bus may not start automatically. System-level services work unconditionally — systemd's PID 1 is always available.

Create the service file (system-level path for root-only VPS):

```ini
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
Environment=COOKIE_SECURE=0

[Install]
WantedBy=default.target
```

Enable and start:

```bash
# User-level service (multi-user VPS):
systemctl --user daemon-reload
systemctl --user enable hermes-workspace
systemctl --user start hermes-workspace

# System-level service (root-only VPS):
#   systemctl daemon-reload
#   systemctl enable hermes-workspace
#   systemctl start hermes-workspace
```

After this, the workspace survives VPS reboots and SSH logout.

### Critical: .env Is NOT Auto-Loaded

The workspace's `server-entry.js` reads `process.env.HOST` and `process.env.HERMES_PASSWORD` directly — it does NOT use dotenv. Setting values in `.env` is NOT sufficient. The variables must be actual environment variables at process start.

**Systemd:** Use `Environment=` directives in the service file (shown above).
**Shell:** `export HOST=0.0.0.0 HERMES_PASSWORD=<pw> && node server-entry.js`
**Prepend:** `HOST=0.0.0.0 HERMES_PASSWORD=<pw> node server-entry.js`

Without this, the server binds to `127.0.0.1` (unreachable over Tailscale) or refuses to start with "HERMES_PASSWORD is unset" and prints a security warning about exposing the control plane.

## Dashboard Requirement (Chat Won't Work Without It)

The workspace needs the Hermes Agent **dashboard API** (port 9119) for chat, sessions, skills, memory, and config. The gateway API (port 8642) alone is insufficient — it only exposes health, chat completions, models, and streaming.

Without the dashboard, the Workspace login succeeds (password auth works) but the chat panel appears broken — you can type but messages fail to send. Other panels (sessions, skills, memory, config) show "Not available." The workspace logs will show:

```
[model-info] falling back to gateway capabilities (source=gateway-capabilities mode=portable)
```

### Checking if Dashboard Is Running

```bash
curl -s http://127.0.0.1:9119/health   # Should respond if up
ss -tlnp | grep 9119                    # Should show listening process
hermes dashboard --status               # Shows running processes
```

### Starting the Dashboard

`hermes dashboard` starts the built-in dashboard on port 9119. Run it as a background process or systemd service for persistence:

```bash
hermes dashboard &
```

**Systemd service (recommended for production):**

```ini
# ~/.config/systemd/user/hermes-dashboard.service
[Unit]
Description=Hermes Agent Dashboard API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/lib/hermes-agent/venv/bin/hermes dashboard
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable hermes-dashboard
systemctl --user start hermes-dashboard
```

### Verifying Workspace Connection

After starting the dashboard, restart the workspace service. The workspace logs will show:

```
[gateway] gateway=http://127.0.0.1:8642 dashboard=http://127.0.0.1:9119 mode=zero-fork
core=[health, chatCompletions, models, streaming, dashboard]
enhanced=[sessions, skills, memory, config, jobs]
missing=[enhancedChat, mcp, mcpFallback]
```

"Enhanced" capabilities (sessions, skills, memory, config, jobs) appear only when the dashboard is reachable. The `missing` list varies by Hermes Agent version.

## Tailscale Auth Flow

The `tailscale up` link is single-use and can give `bad tailscale-authstate2 cookie` if stale.

### Correct sequence:
1. On VPS: `tailscale up` → prints auth URL
2. Open URL in **regular browser** (not in-app Telegram/Discord browser) on any device
3. Authenticate with Google/GitHub/Microsoft/email
4. VPS appears in tailnet immediately with `100.x.y.z` IP

**Check connection:** `tailscale status`

### Known devices in this setup:
```
100.113.2.25     ghjgh              smburner2026@  linux    (VPS)
100.102.166.100  desktop-b4lb6vl    smburner2026@  windows  (laptop)
100.65.99.106    pixel-7a           smburner2026@  android  (phone)
```

## Phone SSH (Break-Glass)

### Install Termux (NOT from Play Store):
1. Install F-Droid from f-droid.org
2. Search "Termux" in F-Droid, install
3. `pkg update && pkg upgrade -y && pkg install openssh`

### Connect:
```bash
ssh root@100.113.2.25
```

Use the same credentials as from laptop. Termux inherits phone's Tailscale network.

## Pitfalls Encountered

- **Stale Tailscale auth URL** → "bad tailscale-authstate2 cookie" error. Fix: run `tailscale up` again for a fresh URL.
- **Vite build OOM on small VPS** → do NOT use dev mode (it has its own blockers). The fix is: add 1GB swap file, stop the gateway, run `npm run build`, restart gateway. See "Memory-Constrained Build (2GB VPS)" section above for the exact sequence.
- **Gateway restarts kill tmux sessions** → the Workspace was running in a tmux session that died when the Hermes Agent went down (tandem gateway restart). Session persistence requires systemd, not just tmux.
- **Relying on `127.0.0.1` for agent API** → Workspace connects to Hermes Agent on localhost fine. Only the Workspace itself needs `HOST=0.0.0.0` for browser access.
- **Login succeeds but chat doesn't send** → the dashboard (port 9119) is not running. Start `hermes dashboard` and restart the workspace. The workspace needs both the gateway API and dashboard API to function fully.
- **`COOKIE_SECURE=0` required for plain HTTP** → without it, the browser silently drops Secure session cookies over `http://`, causing the login to appear to work but actually fail. The workspace's own startup warning catches this: it prints a plain-HTTP LAN deployment warning if `COOKIE_SECURE=0` is missing and `NODE_ENV=production`.
- **Environment variables not loaded from `.env`** → `server-entry.js` does NOT use dotenv. All config values (`HOST`, `HERMES_PASSWORD`, `COOKIE_SECURE`, `PORT`) must be actual OS environment variables. The `.env` file is purely documentation in this project.
- **Workspace reachable on localhost but not via Tailscale after restart** → the server bound to `127.0.0.1` instead of `0.0.0.0` because `HOST` was not in the environment at process start. Diagnostic: `ss -tlnp | grep 3000` shows `127.0.0.1:3000` instead of `0.0.0.0:3000`. Fix: stop the service, start with `HOST=0.0.0.0` explicitly set, verify with `curl -s -o /dev/null -w "%{http_code}" http://0.0.0.0:3000/`, then update the systemd service file to include `Environment=HOST=0.0.0.0` so it survives the next restart.
