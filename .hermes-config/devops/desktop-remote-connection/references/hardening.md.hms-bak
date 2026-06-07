# Hardening the Dashboard for Remote Desktop Access

Session-specific detail, transcripts, and decision trees for tightening the `hermes dashboard` exposure when wiring up the **official** Desktop app to a VPS.

## TL;DR — If you just want the secure defaults

```bash
# 1. Add auth to .env
cat >> ~/.hermes/.env << 'EOF'
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=vps
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=***-phra**-phrase-here
HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(rand -base64 32)
EOF
chmod 600 ~/.hermes/.env

# 2. Update systemd unit — drop --insecure, bind to Tailscale IP, add EnvironmentFile
```

```ini
# ~/.config/systemd/user/hermes-dashboard.service
[Service]
EnvironmentFile=%h/.hermes/.env
ExecStart=/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main dashboard --no-open --host 100.113.2.25 --port 9119
```

```bash
systemctl --user daemon-reload
systemctl --user restart hermes-dashboard

# 3. Verify the gate is on
curl -s http://100.113.2.25:9119/api/status | jq '.auth_required, .auth_providers'
# → auth_required: true, auth_providers: ["basic"]
```

If you see anything else, the gate didn't engage. Don't ship it.

## Decision tree: auth provider choice

```
Where will the dashboard be reachable from?
│
├─ Same machine only (loopback) → no auth needed, default 127.0.0.1 binding
│
├─ Tailscale tailnet only → Basic auth (HERMES_DASHBOARD_BASIC_AUTH_*)
│   - Tailnet is the perimeter
│   - Defense in depth: bind to tailnet IP, not 0.0.0.0
│
├─ Trusted LAN (home/office) → Basic auth, bind to LAN IP
│
└─ Public internet → OAuth (Nous Portal) ONLY
    - Username/password is explicitly NOT safe for this per the official guide
    - Set up: hermes dashboard register → Portal /local-dashboards
    - Sign in via "Sign in with Nous Research" in the desktop app
```

## Why `--insecure` is a footgun

The `--insecure` flag was an older shortcut for "trusted network, skip the gate." In practice:

- **Reads `.env`** — exposes every API key, OAuth token, Bitwarden BWS token, Telegram bot token, Discord bot token
- **Runs agent commands** — can send messages as you on Telegram/Discord
- **Tailscale is a single point of failure** — if the VPS firewall flips off, the port is on `0.0.0.0` and the public internet can reach it
- **No audit trail** — no way to tell who connected

The 2 minutes it takes to set up basic auth + bind to the Tailscale IP is worth it. The official guide's stance is unambiguous:

> "never expose a password-protected dashboard directly to the open internet; put it behind a VPN. Tailscale is the clean option: bind to the machine's tailscale IP (`--host <tailscale-ip>`)"

## Password hash vs plaintext in .env

Both work, the .env is 0600 either way. Choose based on threat model:

| Approach | Pros | Cons |
|---|---|---|
| `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=...` | Simple, copy-paste from password manager | Anyone with read access to the file (or a backup) gets the password |
| `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH=...` | Even root can't recover the password from the file | Slightly slower; one extra command to generate |

Generate the hash:
```bash
python3 -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('your-password'))"
# → scrypt$...$...
```

**Set one or the other, not both.** If both are set the behavior is undefined per the official guide.

## The `_SECRET` trap

`HERMES_DASHBOARD_BASIC_AUTH_SECRET` is the token-signing key. Two failure modes:

1. **Missing entirely** — generated fresh per boot. Every restart invalidates every active session. You get logged out and have to sign in again.
2. **Set but changed on every boot** — same problem, just less obvious. If you generate the secret in the systemd unit (`EnvironmentFile` with a `$(rand ...)` line, or `ExecStartPre`), the secret rotates per restart. Bad.

**Fix:** set it once to a stable value and never rotate it unless you want to invalidate every session.

## The systemd `EnvironmentFile` trap

If you set `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=foo` in your shell, then start the dashboard with `hermes dashboard ... &` from the shell, the env var reaches the process. If you set the same env var in the shell and then start the dashboard via systemd (`systemctl --user start hermes-dashboard`), **the systemd-managed process does NOT see it.** Systemd runs services in a clean environment.

Two ways to fix:

**Option A — `EnvironmentFile` in the unit (recommended):**
```ini
[Service]
EnvironmentFile=%h/.hermes/.env
ExecStart=/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main dashboard --no-open --host 100.113.2.25 --port 9119
```

**Option B — `Environment=` lines in the unit:**
```ini
[Service]
Environment=HERMES_DASHBOARD_BASIC_AUTH_USERNAME=vps
Environment=HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=***
Environment=HERMES_DASHBOARD_BASIC_AUTH_SECRET=***
ExecStart=/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main dashboard --no-open --host 100.113.2.25 --port 9119
```

`EnvironmentFile` is cleaner because the creds live in one place.

## Diagnostic commands

**Is the dashboard running at all?**
```bash
systemctl --user status hermes-dashboard
ss -tlnp | grep :9119
# LISTEN ... 0.0.0.0:9119  users:(("hermes",pid=...))
# or
# LISTEN ... 100.113.2.25:9119  users:(("hermes",pid=...))
```

**Is the auth gate on?**
```bash
curl -s http://127.0.0.1:9119/api/status | jq '.auth_required, .auth_providers'
# auth_required: true, auth_providers: ["basic"]  ← good
# auth_required: false                                 ← bad
```

**Is the port reachable over Tailscale?**
```bash
# From a peer on the tailnet:
curl -s -o /dev/null -w "%{http_code}\n" http://<tailscale-ip>:9119/api/status
# 401 → good (gate is on, no creds provided)
# 200 → bad (gate is off, or you're hitting localhost)
# Connection refused → bad (bind address or firewall)
```

**Which env vars did the dashboard actually load?**
The dashboard logs to `~/.hermes/logs/`. Look for the auth provider activation at startup:
```bash
tail -50 ~/.hermes/logs/dashboard.log | grep -i "auth\|basic"
```

**Systemd EnvironmentFile actually loaded?**
```bash
systemctl --user show hermes-dashboard | grep -i "environmentfile\|execstart"
```

## Session transcript — Real `--insecure` → hardened migration

The user came in with this state on the VPS:

```bash
$ ps -fp $(pgrep -f 'hermes.*dashboard')
UID          PID    PPID  C STIME TTY          TIME CMD
root     2192183     838  0.1 02:09 ?        00:01:06 /usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main dashboard --port 9119 --host 0.0.0.0 --insecure

$ ss -tlnp | grep :9119
LISTEN 0  2048  0.0.0.0:9119  0.0.0.0:*  users:(("hermes",pid=2192183,fd=14))

$ grep "DASHBOARD" ~/.hermes/.env
HERMES_DASHBOARD_SESSION_TOKEN=***
```

Translation: bound to all interfaces, `--insecure`, no auth env vars, just a stale session token from the day it was set up. The session token doesn't enable auth — it's just a bearer token. Anyone hitting port 9119 over the public internet could have driven the agent.

Compare against the official guide's recommended state:

```ini
# systemd unit:
EnvironmentFile=%h/.hermes/.env
ExecStart=... dashboard --no-open --host 100.113.2.25 --port 9119

# .env additions:
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=***
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=*** (or _HASH)
HERMES_DASHBOARD_BASIC_AUTH_SECRET=***
```

**Diff in security posture:**

| Before | After |
|---|---|
| No authentication | Username + password required |
| Bound to `0.0.0.0` (whole internet) | Bound to Tailscale IP `100.113.2.25` (tailnet only) |
| Sessions die on every restart | Sessions persist (stable `_SECRET`) |
| `curl -u : http://IP:9119/api/status` → 200 | `curl -u : http://IP:9119/api/status` → 401 |

## Common migrations from older guides

**Old:** `--host 0.0.0.0 --insecure` (from `hermes-web-ui` skill, pre-2026)
**New:** `--host <tailscale-ip>` + basic auth in `.env`

**Old:** "just set `API_SERVER_HOST=0.0.0.0` for desktop access"
**New:** that was for the community app. Official app uses port 9119 dashboard, not 8642 API server.

**Old:** rely on Tailscale being the only perimeter
**New:** Tailscale + auth gate = defense in depth. If the firewall flips off, the gate is still there.

## Related gotchas

- **`hermes update` may overwrite the systemd unit** — re-check `ExecStart` and `EnvironmentFile` after updates
- **`.env` mode 0600 is non-negotiable** — it has API keys for every provider you've configured
- **The dashboard and the workspace (port 3000) restart together** — if you bounce one, bounce both, otherwise the workspace's session token goes stale and `/api/sessions` returns 401
- **OAuth registration is per-dashboard** — registering on one machine doesn't carry to others. Each VPS that exposes a dashboard to the public internet needs its own `hermes dashboard register`
