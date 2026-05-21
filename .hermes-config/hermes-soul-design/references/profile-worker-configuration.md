# Profile Worker Configuration — Toolsets & Runtime Setup

## The Problem

When you create a Hermes profile via `hermes profile create <name>`, the profile's `config.yaml` defaults to:

```yaml
toolsets:
  - hermes-cli
```

The `hermes-cli` toolset is the minimal chat management set — slash commands (`/retry`, `/undo`, `/title`, etc.) and session control. It provides **no terminal access, no file system, no web search, no code execution, no delegation**.

A profile with a SOUL.md (persona) but `toolsets: [hermes-cli]` can think and talk, but cannot read a file, run a command, or fetch a web page. If the kanban dispatcher spawns it as a worker, the worker will start, load its soul, greet the void, and be unable to execute any concrete task.

## Diagnosis

Check a profile's configured toolsets:

```bash
hermes -p <profile-name> config get toolsets
# or
grep -A2 'toolsets:' ~/.hermes/profiles/<profile-name>/config.yaml
```

If the output shows only `hermes-cli`, the profile is not worker-capable.

## The Fix

### Via CLI (within profile context)

```bash
hermes -p <profile-name> config set toolsets "['hermes-cli', 'terminal', 'file', 'web']"
```

### Via direct config edit

Edit `~/.hermes/profiles/<profile-name>/config.yaml` and change the `toolsets:` list.

## What Toolsets a Worker Needs

| Toolset | Why | Required? |
|---------|-----|-----------|
| `hermes-cli` | Session control, kanban tools | ✅ Always |
| `terminal` | Shell commands (git, pip, build, run) | ✅ Always |
| `file` | Read/write/search/patch files | ✅ Always |
| `web` | Internet access for research | ⬜ If the task involves external info |
| `code_execution` | Sandboxed Python | ⬜ If the task involves data processing |
| `skills` | Load skill context | ⬜ If the task needs specific skills |
| `memory` | Cross-session memory | ⬜ If the profile should accumulate experience |
| `delegation` | Spawn subagents | ⬜ If the profile should decompose work |
| `session_search` | Search past sessions | ⬜ If the profile needs historical context |

## Verification

After fixing toolsets, verify the profile is worker-ready:

```bash
# 1. Profile can start
hermes -p <profile-name> chat -q "what tools do you have available" --quiet 2>&1 | head -10

# 2. config shows correct toolsets
hermes -p <profile-name> config get toolsets

# 3. kanban dispatcher can see the profile
hermes profile list
# → profile should appear with a model set and gateway status (may be stopped — that's fine)
```

## Pitfalls

### Model not set
A profile with toolsets but no model is a brain in a jar. Verify with `hermes -p <profile-name> model` or check `model.default` in config.yaml.

### Auth not configured
Profiles created with `--clone` or `--clone-from` may symlink `.env` and `auth.json` from the source profile. Profiles created from scratch have no auth at all. Check:
```bash
ls -la ~/.hermes/profiles/<profile-name>/.env
ls -la ~/.hermes/profiles/<profile-name>/auth.json
```
If missing, the worker won't authenticate with its provider.

### SOUL.md without tools
A SOUL.md makes the profile *talk right* but doesn't make it *act right*. The soul file only governs persona, voice, and behavior — not runtime capabilities. Always check `toolsets` as a separate dimension.

### Dispatcher silently fails
If the dispatcher tries to spawn a worker for a profile that exists on disk but has no model or wrong toolsets, the spawn may succeed (process starts) but the worker immediately can't do anything. The kanban board shows a `running` state that never completes. Always verify with a one-shot `hermes -p <profile-name> chat -q "hello"` before relying on the dispatcher.

## Dashboard & Workspace — Two Web UIs

Two separate Hermes web interfaces exist on a standard VPS deployment:

| | Workspace | Dashboard |
|---|---|---|
| Port | `:3000` | `:9119` |
| Engine | Node.js SPA | Python / `hermes dashboard` |
| Auth | Password (`HERMES_PASSWORD`) | None (bind protection; Tailscale is auth) |
| What it does | Full web IDE — chat with Hermes, file browser (drag-drop), session list, skills, memory viewer, kanban | Admin panel — session history, skills overview, profiles, cron jobs, kanban board, status |
| File browser | ✅ Yes — browse/edit/upload/download files | ❌ No |
| Access via | `http://<vps-ip>:3000` | `http://<vps-ip>:9119` |

Use the **Workspace** for day-to-day agent interaction with a visual file browser. Use the **Dashboard** to inspect state (sessions, skills, profiles, kanban, cron) without asking the agent.

### Binding default: Dashboard is localhost-only

⚠️ The Dashboard binds to `127.0.0.1` by default. If you're on a Tailscale/LAN, `http://<vps-ip>:9119` shows "Connection refused." To make it reachable:

```bash
# Edit the systemd service file (/root/.config/systemd/user/hermes-dashboard.service):
ExecStart=.../hermes dashboard --host 0.0.0.0 --insecure
# Then:
systemctl --user daemon-reload && systemctl --user restart hermes-dashboard
```

`--insecure` is required because the Dashboard exposes API keys. On a private tailnet this is fine — Tailscale is your auth layer.

### Workspace directory root — the blocked `/root` problem

The Workspace's file browser uses a root-path resolution chain. It checks these in order and uses the first that exists and passes security filters:

1. `$HERMES_WORKSPACE_DIR` env var ← bypasses blocked-path filter
2. `$CLAUDE_WORKSPACE_DIR` env var
3. `config.workspace` in Hermes config
4. `config.default_workspace` in Hermes config
5. `config.terminal.cwd` in Hermes config
6. `~/workspace` (`/root/workspace`)
7. `~/work` (`/root/work`)
8. Create `~/workspace` as fallback

**Critical:** The Workspace maintains a blocked-system-paths list that includes `/root`, `/etc`, `/usr`, `/bin`, `/sbin`, etc. If your candidate workspace path is *anywhere under `/root/*`*, it is silently rejected by `firstValidDirectory()`. This means `terminal.cwd: /root/work`, `~/work`, and `~/workspace` all fail on a VPS where the user's home is `/root`.

**Fix:** Set the `HERMES_WORKSPACE_DIR` env var in the workspace service file. This variable is checked **before** the blocked-path filter and takes precedence:

```ini
# In /root/.config/systemd/user/hermes-workspace.service:
Environment=HERMES_WORKSPACE_DIR=/root/work
```

After adding it:

```bash
systemctl --user daemon-reload && systemctl --user restart hermes-workspace
```

### Workspace service should run FROM the work directory

Instead of having the Workspace point at the work directory via config (an extra hop), change its `WorkingDirectory` to the actual work path so terminals, file browser, and swarm subsystems naturally start there:

```ini
# In hermes-workspace.service:
WorkingDirectory=/root/work
```

This eliminates the indirection. The workspace server finds its assets via `__dirname` (its install location), so changing WorkingDirectory is safe — it doesn't break asset resolution.

### HTTP login on mobile: COOKIE_SECURE=0

If accessing the Workspace over plain HTTP (no HTTPS — common on Tailscale LAN), the browser silently drops Secure cookies, causing the login to appear successful but immediately log out:

```ini
# In hermes-workspace.service:
Environment=COOKIE_SECURE=0
```

This must be set alongside `HOST=0.0.0.0` on any deployment that serves HTTP without TLS.

### Workspace login password reference

The password is stored in `~/.hermes/.env` as `HERMES_PASSWORD` (legacy: `CLAUDE_PASSWORD`) and passed to the service via `Environment=HERMES_PASSWORD=<value>`. Find the current value with `grep HERMES_PASSWORD /root/hermes-workspace/.env`.
