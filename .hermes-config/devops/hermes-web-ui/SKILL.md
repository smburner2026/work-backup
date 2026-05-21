---
name: hermes-web-ui
description: "Configure and diagnose Hermes Workspace + Dashboard web UIs: remote access, profile toolset requirements for kanban workers, and the architecture distinction between the two interfaces."
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hermes, workspace, dashboard, web-ui, remote-access, tailscale, kanban, profiles]
    related_skills: [kanban-orchestrator, kanban-worker, hermes-agent]
---

# Hermes Web UI — Workspace & Dashboard

Hermes ships **two web UIs**, not one. Confusing them is the most common source of "Workspace is incomplete" frustration.

| | **Workspace** | **Dashboard** |
|---|---|---|
| Port | `:3000` (configurable via `PORT` env) | `:9119` (configurable via `--port`) |
| Engine | Node.js SPA | Python / `hermes dashboard` CLI |
| Purpose | Full web IDE — chat, file browser, sessions, skills, memory, kanban | Admin panel — session list, skills overview, profiles, status, config |
| Auth | Password (set via `HERMES_PASSWORD` in `.env`) | None by default — relies on bind address |
| Default bind | `HOST=0.0.0.0` (open, but needs password) | `127.0.0.1` (localhost only) |
| Remote access | Works out of box if password is set | Requires explicit `--host 0.0.0.0 --insecure` |

## Remote Access Setup

### Workspace (port 3000)

The Workspace binds to `0.0.0.0` by default when `HOST=0.0.0.0` is set in its `.env`. It requires `HERMES_PASSWORD` to be set before it starts on a non-loopback interface.

#### WorkingDirectory — the project root

The Workspace service file (`~/.config/systemd/user/hermes-workspace.service`) has a `WorkingDirectory=` directive. This determines where the file browser and terminal sessions start. **Set it to the user's actual project root, not the workspace install directory.**

```ini
# BAD: starts in the workspace's own directory
WorkingDirectory=/root/hermes-workspace

# GOOD: starts in the project root
WorkingDirectory=/root/work
```

After changing, reload and restart:
```bash
systemctl --user daemon-reload
systemctl --user restart hermes-workspace
```

This avoids a confusing layer of indirection where the workspace is installed in one place but configured to point elsewhere.

**Key config (in `hermes-workspace/.env`):**
```
HOST=0.0.0.0
HERMES_PASSWORD=<strong-secret>
COOKIE_SECURE=0                    # Needed for plain HTTP (no HTTPS)
```

If the login page loads but password is rejected on mobile:
- Check that `COOKIE_SECURE=0` is set — browsers silently drop Secure cookies over HTTP
- The password works via `curl -X POST http://localhost:3000/api/auth -d '{"password":"..."}'`

### Dashboard (port 9119)

The Dashboard binds to `127.0.0.1:9119` by default. To make it accessible over Tailscale or LAN:

1. **Edit the systemd service** (`~/.config/systemd/user/hermes-dashboard.service`):
   ```
   ExecStart=/usr/local/lib/hermes-agent/venv/bin/hermes dashboard --host 0.0.0.0 --insecure
   ```

2. **Reload and restart:**
   ```bash
   systemctl --user daemon-reload
   systemctl --user restart hermes-dashboard
   ```

3. **Verify:**
   ```bash
   curl -s http://<tailscale-ip>:9119/api/status
   ```

4. **Restart the workspace too** (it scrapes the dashboard's ephemeral session token on startup; a stale token produces 401s on `/api/sessions`):
   ```bash
   systemctl --user restart hermes-workspace
   ```

The `--insecure` flag is required because the Dashboard displays API keys and config in its UI. On a Tailscale tailnet this is acceptable — the tailnet is a private mesh.

> **Session reference:** `references/tailscale-fixes.md` documents a real-world diagnosis of Dashboard + Workspace remote access issues (Pixel 7a Android over Tailscale).

### Gateway API (port 8642)

The Hermes Agent gateway exposes an HTTP API at port 8642, but it also binds to `127.0.0.1` by default. To make it accessible:
```
# In ~/.hermes/.env:
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0    # Optional, defaults to 127.0.0.1
API_SERVER_KEY=<secret>     # Required when binding to 0.0.0.0
```

Then restart the gateway and set `HERMES_API_TOKEN=<secret>` in `hermes-workspace/.env`.

## Diagnosing "I don't have agents"

When a user says "the kanban system isn't doing anything" or "I don't have agents":

### Step 1 — Check profiles and their toolsets
```bash
hermes profile list
```
Look at the `toolsets` field for each non-default profile. A profile with only `hermes-cli` cannot:
- Run terminal commands (no `terminal` toolset)
- Read/write files (no `file` toolset)
- Search the web (no `web` toolset)

**A kanban worker needs at minimum:** `terminal`, `file`, and usually `web`.

### Step 2 — Fix the toolsets
```bash
# For an existing profile:
hermes -p <profile-name> config set toolsets "['hermes-cli', 'terminal', 'file', 'web']"

# Or edit ~/.hermes/profiles/<name>/config.yaml directly and add:
# toolsets:
#   - hermes-cli
#   - terminal
#   - file
#   - web
```

### Step 3 — Verify the dispatcher is running
```bash
# Check kanban dispatch config:
grep -A5 'kanban:' ~/.hermes/config.yaml
# Should have dispatch_in_gateway: true
```

### Step 4 — Create a test task
```bash
hermes kanban create "Test: list /tmp" --assignee <profile-name>
```
Watch the dispatcher pick it up (it polls every 60s or whatever `dispatch_interval_seconds` is set to).

## Profiles carry SOULs but need tool access

A profile's SOUL.md carries the persona (Layer 0-3 architecture), but the **config.yaml controls tool access**. A profile with a rich SOUL but `toolsets: [hermes-cli]` is a brain in a jar — it can think but can't touch files, run commands, or fetch web pages.

When a user says "the personality is there but it can't do anything" — this is always the toolsets issue.

### Profile model/provider configuration

Each profile runs its own model and provider, independent of the default. To change a profile's model:

```
# Option A: via hermes config (reliable)
hermes -p <profile-name> config set model.default <new-model>
hermes -p <profile-name> config set model.provider <new-provider>

# Option B: edit the profile config directly
# ~/.hermes/profiles/<name>/config.yaml
# model:
#   default: deepseek-v4-flash
#   provider: opencode-go
#   base_url: ''
```

Common scenario — switching a profile to match the default provider:
```
hermes -p euphy config set model.default deepseek-v4-flash
hermes -p euphy config set model.provider opencode-go
hermes -p euphy config set model.base_url ''
```

This is useful when the default provider supports a model the specialized provider doesn't, or when consolidating credentials.

## Key Paths

| Component | Path |
|---|---|
| Workspace root | Usually a sibling directory: `~/hermes-workspace/` |
| Workspace .env | `~/hermes-workspace/.env` |
| Dashboard service (user-level) | `~/.config/systemd/user/hermes-dashboard.service` |
| Workspace service (user-level) | `~/.config/systemd/user/hermes-workspace.service` |
| Dashboard service (system-level, root-only VPS) | `/etc/systemd/system/hermes-dashboard.service` |
| Workspace service (system-level, root-only VPS) | `/etc/systemd/system/hermes-workspace.service` |
| Workspace sessions file | `~/.hermes/workspace-sessions.json` |
| Profile configs | `~/.hermes/profiles/<name>/config.yaml` |
| Profile souls | `~/.hermes/profiles/<name>/SOUL.md` |
| Gateway API config | `~/.hermes/.env` (`API_SERVER_*` vars) |

## Pitfalls

- **Trying Dashboard at port 9119 and getting "connection refused"** — it's bound to 127.0.0.1 by default. Fix with `--host 0.0.0.0 --insecure`.
- **Workspace login works on desktop but not mobile** — check `COOKIE_SECURE=0` in workspace .env. The default `NODE_ENV=production` enables Secure cookies; browsers drop them over HTTP.
- **Workspace file browser shows the wrong directory** — the Workspace service's `WorkingDirectory=` in its systemd unit determines where the file browser and terminals start. Set it to the project root, not the workspace install directory.
- **Creating kanban tasks but nothing happens** — the dispatcher spawns workers on the assigned profile. If that profile has no terminal/file/web tools, the worker spawns, reads the task, and can't do anything. The spawn succeeds but the work never completes. Check the profile's toolsets.
- **Kanban dispatcher logs spawns but worker fails silently** — the worker started but lacks tool access. Turn on profile logging or check `~/.hermes/logs/gateway.log` for spawn events.
- **"I have four profiles but none of them work"** — check `hermes profile list` for toolsets. If all non-default profiles show `hermes-cli` only, none will function as workers until you add terminal/file/web.
- **Workspace went dark after restart** — if the workspace was restarted and no longer reachable over Tailscale, check the bind address: `ss -tlnp | grep 3000`. If it shows `127.0.0.1` instead of `0.0.0.0`, the `.env` file wasn't loaded (the server-entry.js does NOT use dotenv). Fix: restart with HOST=0.0.0.0 explicitly in the environment:
  ```
  # One-shot fix:
  systemctl stop hermes-workspace
  HOST=0.0.0.0 HERMES_PASSWORD=<pw> /root/.hermes/node/bin/node /root/hermes-workspace/server-entry.js
  ```
  Then update the systemd service file to have `Environment=HOST=0.0.0.0` in the [Service] section and `systemctl daemon-reload && systemctl restart hermes-workspace` for persistence.
- **`systemctl --user` commands fail on root-only VPS** — when running as root on a dedicated VPS, user-level systemd may not have a bus. Use system-level services at `/etc/systemd/system/` with plain `systemctl` (no `--user`). Service file syntax is identical; only the path and command differ.
