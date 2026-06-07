---
name: desktop-remote-connection
description: "Connect Hermes Desktop app (official Nous Research client) to a remote Hermes instance running on a VPS via the dashboard backend (port 9119). Covers auth setup, Tailscale binding, systemd, and the OAuth vs basic-auth decision."
version: 2.0.0
author: hermes-agent
tags: [hermes, desktop, remote, vps, dashboard, auth, tailscale, systemd]
triggers:
  - "connect desktop to vps"
  - "hermes desktop remote"
  - "desktop app remote backend"
  - "desktop can't reach vps"
  - "remote gateway settings"
  - "hermes dashboard remote access"
  - "Sign in with Nous Research"
related_skills:
  - hermes-web-ui
  - tailscale-client
  - secrets-management
  - hermes-environment-sync
---

# Desktop ↔ Remote VPS Connection

The **official Hermes Desktop app** (Nous Research, Electron+React) is a GUI frontend for the Hermes agent. It talks to a remote instance through the **dashboard backend** (`hermes dashboard`, port 9119) — not the API server adapter (port 8642, which is for the community app and third-party integrations).

```
Desktop App  ──HTTP/WebSocket──▶  hermes dashboard (port 9119)  ──▶  Hermes Agent
                                   on VPS, behind auth gate
```

The auth gate is **mandatory** whenever the dashboard is bound to a non-loopback address. There is no "trusted LAN, no auth" mode for production use.

## Two App Variants — Pick the Right Backend

| App | Backend | Port | Auth | Entry in app |
|---|---|---|---|---|
| **Official** (Nous Research, `hermes-agent.nousresearch.com/desktop`) | `hermes dashboard` | **9119** | Basic auth **or** OAuth (Nous Portal) | Settings → Gateway → Remote gateway |
| **Community** (`fathah/hermes-desktop`) | API server adapter | 8642 | `API_SERVER_KEY` | First-launch wizard → Remote mode |

**If you downloaded the official app, follow this guide. If you have the community app, see the API server section at the bottom.**

## Architecture (Official App)

```
┌──────────────────┐                              ┌─────────────────────┐
│  Desktop App     │   HTTP + WebSocket           │  VPS                │
│  (Electron+React)│ ───────────────────────────▶ │  hermes dashboard   │
│                  │   http://<host>:9119         │  (auth gate ON)     │
│  Settings →      │   + Basic or OAuth header    │                     │
│  Gateway →       │                              │  → Hermes Agent     │
│  Remote gateway  │                              │  → Tools / Sessions │
└──────────────────┘                              └─────────────────────┘
```

The dashboard reads `.env` (API keys, secrets) and can run agent commands. **It must be behind a working auth gate whenever it's reachable beyond loopback.**

## Setup — Backend on the VPS

### 1. Add auth credentials to `~/.hermes/.env`

The dashboard reads three env vars. **All three are required** for a clean setup:

```bash
# 0600 mode is mandatory — .env contains API keys
cat >> ~/.hermes/.env << 'EOF'
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=*** a username***
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=*** a strong password***
# Stable secret so sessions survive restarts. Without it the token-signing
# key regenerates per boot and you get logged out on every restart.
HERMES_DASHBOARD_BASIC_AUTH_SECRET=*** -base64 32)
EOF
chmod 600 ~/.hermes/.env
```

**Password hash option** (no plaintext at rest, even in 0600 file):
```bash
python3 -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('your-password'))"
# → scrypt hash. Set HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH=*** (do NOT set both PASSWORD and PASSWORD_HASH)
```

### 2. Pick a bind strategy

| Deployment | Bind to | Auth | Use case |
|---|---|---|---|
| **Tailscale-only** (default) | `--host <tailscale-ip>` | Basic auth | Tailnet is the only network that can reach the port — defense in depth |
| **Trusted LAN** | `--host <lan-ip>` | Basic auth | Home network, no VPN |
| **Public internet** | `--host 0.0.0.0` | **OAuth (Nous Portal) only** | Username/password is **not safe** for internet exposure per the official guide |
| **Local-only testing** | `--host 127.0.0.1` | None (loopback bypasses gate) | Just for SSH tunnel / dev |

**Recommendation:** Tailscale-only is the clean default. Bind explicitly to the tailnet IP, not `0.0.0.0`, so a future firewall misconfiguration can't accidentally expose the port.

### 3. Start the dashboard as a systemd service

`~/.config/systemd/user/hermes-dashboard.service`:

```ini
[Unit]
Description=Hermes Agent Dashboard
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=%h/.hermes/.env
# Bind to Tailscale IP. Replace with your actual tailnet IP.
ExecStart=/usr/local/lib/hermes-agent/venv/bin/python -m hermes_cli.main dashboard --no-open --host 100.113.2.25 --port 9119
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable hermes-dashboard
systemctl --user restart hermes-dashboard
systemctl --user status hermes-dashboard
```

If you run as root on a dedicated VPS and `systemctl --user` doesn't have a bus, copy the unit to `/etc/systemd/system/` and use plain `systemctl`.

### 4. Verify the auth gate is engaged

```bash
curl -s http://<tailscale-ip>:9119/api/status | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('auth_required:', d.get('auth_required'))
print('auth_providers:', d.get('auth_providers'))
"
```

**Expected output:**
```
auth_required: True
auth_providers: ['basic']
```

If `auth_required: False` → the gate is off, either the dashboard is on loopback or `--insecure` is set. **Do not proceed until `True`.**

## Setup — Desktop App

### Via the UI (recommended)

1. Open Desktop app → **Settings** (sidebar) → **Gateway** → **Remote gateway**
2. **Remote URL:** `http://100.113.2.25:9119` (your VPS Tailscale IP)
3. The app detects which provider the backend advertises and shows the right button:
   - Basic auth backend → "Sign in" button → enter username + password
   - OAuth backend → "Sign in with Nous Research" → browser flow
4. **Save and reconnect** — switches the shell onto the remote backend. Sessions persist across restarts when `HERMES_DASHBOARD_BASIC_AUTH_SECRET` is set.

### Via env var (skip the UI)

```bash
# Set before launching the desktop app:
export HERMES_DESKTOP_REMOTE_URL=http://100.113.2.25:9119
hermes desktop
```

You still need to sign in from the Gateway settings panel once.

## OAuth (Nous Portal) — For Public-Internet Exposure

If you must expose the dashboard to the public internet (no Tailscale), the username/password setup is **explicitly not safe** for that — the official guide says so directly. Use OAuth instead.

OAuth verifies logins against your Nous account, so the credential model is identity-provider-backed rather than a single shared password. A self-hosted OIDC provider works the same way.

### Mental model: "Sign in with Nous Research" ≠ "Sign in with GitHub"

When the desktop app shows **"Sign in with Nous Research"**, the flow is:
1. Click → browser opens Nous Portal sign-in page
2. User clicks **"Sign in with GitHub"** (or Google/email — whatever the Portal account was created with)
3. GitHub OAuth → consent → redirect back to Portal → Portal redirects back to desktop app authenticated

GitHub is **not** a direct OIDC provider for the dashboard. The Nous Portal sits in front of it. If the user says "my login is via github," they mean their Nous Portal account is GitHub-backed — the desktop app still uses the Nous button, the GitHub step is one click deeper in the browser flow.

GitHub is not a generic OIDC provider (no `/.well-known/openid-configuration`, no ID token claims), so wiring GitHub directly as the dashboard's identity provider requires a thin OIDC wrapper (e.g. `oauth2-proxy`) — usually not worth it. Use the Portal.

### Step-by-step OAuth setup

```bash
# 1. Log in to Nous Portal (REQUIRED before register will work).
#    This is interactive — needs a TTY and a browser. Cannot be scripted
#    headlessly from a non-interactive shell. Run from your own terminal.
hermes setup --portal

#    The CLI prints a URL and a short code. Open the URL in any browser,
#    sign in (e.g. "Sign in with GitHub"), enter the code when prompted.
#    Token is stored in ~/.hermes/ and hermes auth status nous shows
#    "logged in" with the account email.

# 2. Register the dashboard with the Portal.
hermes dashboard register --name "Hermes VPS"

#    Writes HERMES_DASHBOARD_OAUTH_CLIENT_ID into ~/.hermes/.env.

# 3. Restart so the dashboard picks up the new env var.
systemctl --user restart hermes-dashboard

# 4. Verify both providers are advertised.
curl -s http://<tailscale-ip>:9119/api/status | python3 -m json.tool | grep -A 5 auth
#    Expected: auth_required: True, auth_providers: ["basic", "oauth"]
#    Both coexist until you remove the BASIC_AUTH_* env vars.

# 5. In the desktop app: Settings → Gateway → Remote gateway → Save and reconnect.
#    The sign-in popup will switch from the username/password form to
#    "Sign in with Nous Research" → click → browser → GitHub → SSO back.
```

### Two distinct errors from `hermes dashboard register` — don't conflate them

```
Error A:  "You're not logged into Nous Portal.
           Run `hermes setup` (or `hermes auth login nous`) first, then retry."
           → The Portal account isn't logged in. Run `hermes setup --portal`.
           → Note: the error message references `hermes auth login nous`,
             which is NOT a real subcommand (use `hermes setup --portal`).

Error B:  "Registration failed: Self-hosted dashboard registration is not
           available for this account."
           → Login succeeded, but the Portal account lacks the self-hosted
             dashboard feature. This is gated by Nous (account tier, beta
             access, or waitlist). Not fixable from the VPS side.
           → Check Portal account settings at https://portal.nousresearch.com
             for a "Self-hosted dashboards" / "Local dashboards" toggle or
             enrollment step. If absent, basic auth is the only path.
           → The dashboard's `auth status nous` may still show "logged out"
             even when a token was saved, because that check uses a different
             state than what register validates. Don't rely on `auth status`
             alone to confirm Portal login.
```

**Diagnostic shortcut for the desktop app popup:**
- Heading **"SIGN IN WITH USERNAME & PASSWORD"** + footer **"PUBLIC BIND · AUTH REQUIRED"** = basic auth provider active. Username/password form is correct.
- Heading **"Sign in with Nous Research"** = OAuth provider active. Browser-based SSO flow is correct.

If the user expected OAuth but the popup shows the username/password form, the `oauth` provider is missing from `auth_providers` in `/api/status` — either `dashboard register` didn't run, didn't write `HERMES_DASHBOARD_OAUTH_CLIENT_ID`, or the dashboard hasn't been restarted since.

## Verification

**From the VPS:**
```bash
# Auth gate is on:
curl -s http://127.0.0.1:9119/api/status | jq '.auth_required, .auth_providers'

# Health/auth reachable over Tailscale:
curl -s http://100.113.2.25:9119/api/status | jq '.auth_required, .auth_providers'
```

**From a remote machine on the tailnet:**
```bash
# Without credentials → should 401:
curl -s -o /dev/null -w "%{http_code}\n" http://100.113.2.25:9119/api/status
# → 401

# With credentials → should 200:
curl -s -u user:pass http://100.113.2.25:9119/api/status | jq .
# → JSON with auth_required: true, auth_providers: ["basic"]
```

**In the desktop app:** sign in, send a message. If it round-trips, the setup is good.

## Troubleshooting

**Sign-in fails with 401 / "Invalid credentials"**
Username or password doesn't match the backend's `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` / `_PASSWORD`. The backend returns the same generic error for unknown user and wrong password (no enumeration oracle). Double-check both values in `.env` and that the dashboard process actually loaded them after a restart.

**No "Sign in" button — asks for session token instead**
The username/password provider isn't active. `/api/status` won't list `"basic"` in `auth_providers`. Make sure both username and a password (or hash) are set in `.env` and the dashboard process actually loaded them.

**Signed out on every restart**
`HERMES_DASHBOARD_BASIC_AUTH_SECRET` is missing or regenerated. Set it to a stable value (e.g. `rand -base64 32`) and restart.

**Connection refused / times out**
The backend is bound to `127.0.0.1` (the default) or a firewall/VPN is blocking the port. Bind to `0.0.0.0` or the Tailscale IP and open the port to your trusted network.

**`curl /api/status` shows `auth_required: false` on a non-loopback address**
The gate didn't engage. Either `--insecure` is in the systemd unit (legacy) or the basic auth env vars are missing. The auth gate engages **only** when the dashboard is bound to a non-loopback address AND basic auth is configured. Set the env vars, remove `--insecure`, restart.

**WebSocket disconnects with cryptic close codes**
See the official guide's "Web Dashboard → Connecting Hermes Desktop to a remote backend" section for close-code triage. Common ones: 4001 (auth expired → `_SECRET` missing), 1006 (network → tailnet route down).

## What About the API Server (port 8642)?

The API server adapter (`API_SERVER_HOST`/`API_SERVER_PORT`/`API_SERVER_KEY` in `.env`) is a **separate** OpenAI-compatible interface. It's used by:

- The **community** desktop app (`fathah/hermes-desktop`)
- Third-party tools (Open WebUI, custom integrations, local llama.cpp frontends)
- Direct curl/OpenAI SDK calls

The official desktop app does **not** use it. Don't conflate the two — if someone tells you "set `API_SERVER_HOST=0.0.0.0` for desktop access" and you have the official app, that's outdated advice from when only the community app existed.

If you need both surfaces (e.g. official desktop + Open WebUI), they run on different ports and don't conflict. Just don't expose the API server to the internet either — same auth caveats apply.

## Pitfalls

1. **Running the dashboard with `--insecure` and `--host 0.0.0.0`** — anyone who reaches the port can drive the agent. Reads `.env`, runs tools, sends messages as you on Telegram/Discord. This was a common shortcut in older guides but is no longer recommended. Use basic auth + Tailscale IP, or OAuth for public.

2. **Setting only the password, not the secret** — sessions don't survive a restart, you get logged out every reboot. The `_SECRET` is separate from the password and the username. All three go in `.env`.

3. **Binding to `0.0.0.0` because "Tailscale is already there"** — defense in depth. If the VPS firewall fails or the user adds a new network interface later, the port is already exposed. Bind explicitly to the Tailscale IP so the port is **only** open on the tailnet interface.

4. **Trying to sign in to a Tailscale-only dashboard from the public internet** — won't work by design. The Desktop app's URL must be reachable. If you're on the road, connect to Tailscale on the laptop first.

5. **Systemd unit missing `EnvironmentFile=%h/.hermes/.env`** — env vars set in shell don't reach the systemd-managed process. The dashboard starts without auth, looks like the gate didn't engage, you go in circles. Always use `EnvironmentFile` for systemd-managed dashboards.

6. **Mixing up dashboard and API server in old guides** — pre-2026 guides often say "set `API_SERVER_HOST=0.0.0.0` and use the API key in the desktop app." That was for the community app. The official app uses the dashboard, port 9119, with basic auth or OAuth.

7. **The community app's "first launch wizard" doesn't appear** — you already have a `~/.hermes` from a previous install. Delete or rename the existing HERMES_HOME to trigger the wizard again, or use the official app's Settings → Gateway → Remote gateway path instead.

8. **Dashboard restart after a `hermes update` breaks the connection** — the update may overwrite the systemd unit. Check the unit's `ExecStart` line after updates and re-add `EnvironmentFile` if it's gone.

9. **`hermes setup --portal` looks like a setup wizard but is actually an OAuth browser flow** — it prints a URL + code, you sign in via browser, the token is stored. It needs a real TTY. `pty=true` on the terminal tool does NOT satisfy its internal TTY check — it still bails with "non-interactive environment (no TTY detected)." Run it from the user's own terminal (SSH session, local shell), not from an agent session. The CLI command itself runs in <60s once the user completes the browser step.

10. **Conflating "logged in" with "Portal account has the feature"** — `hermes auth status nous` shows whether a token was saved. `hermes dashboard register` shows whether the saved token's account has the self-hosted dashboard feature. These are different checks. A user saying "I'm logged in" or seeing "logged in" status does not mean `register` will succeed. After `hermes setup --portal`, run `dashboard register` immediately as the verification step — don't take "logged in" as success.

11. **The two `auth` providers coexist until you remove basic auth** — adding OAuth does NOT disable basic auth. The dashboard advertises both, the desktop app picks one. To drop basic auth, remove the three `HERMES_DASHBOARD_BASIC_AUTH_*` env vars from `~/.hermes/.env` and restart the dashboard. Don't leave basic auth active "just in case" on a public-internet deployment — the guide is explicit that username/password is not safe for that.

12. **Don't ask the user to choose between two auth paths after they've already said "go"** — when the user has approved the broader action (e.g. "yeah let's add auth"), pick the right default and execute. Use basic auth by default for Tailscale-only deployments (zero Portal dependency, fully working today). Use OAuth only when the user explicitly says "with OAuth" / "with Nous Portal" / "with GitHub login" / or the deployment is public-internet. Re-asking after "go" breaks their flow.

## References

- `references/hardening.md` — security hardening checklist, scrypt password hashing, OAuth vs basic auth decision tree, transcripts from real `--insecure` → `Tailscale IP + auth` migrations
- `references/desktop-app-architecture.md` — internal architecture of the Electron app (routes, IPC, plugin SDK)
- `references/oauth-flow.md` — full Nous Portal OAuth flow: TTY requirement, the two distinct `dashboard register` errors, popup diagnostic, the GitHub→Portal mental model, and a verified transcript of a `--insecure` → `basic auth` → `OAuth` migration
- Official guide: `https://hermes-agent.nousresearch.com/docs/user-guide/desktop#connecting-to-a-remote-backend`
- Web Dashboard deep-dive: `https://hermes-agent.nousresearch.com/docs/user-guide/web-dashboard`
