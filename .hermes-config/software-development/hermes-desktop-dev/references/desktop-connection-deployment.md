# Desktop App → VPS Connection (2026-06-04)

## Architecture: Two Servers, Not One

The gateway process runs **two** HTTP servers:

| Server | Default Port | Purpose | Desktop App Uses? |
|--------|-------------|---------|-------------------|
| **Dashboard web server** (FastAPI) | 9119 | REST API + WebSocket for desktop app + web UI | **YES** — this is what the desktop connects to |
| **API server** (platform adapter) | 8642 | Telegram/Discord webhook endpoints | NO — desktop app cannot connect here |

**Common mistake:** pointing the desktop app at port 8642 (the API server). The desktop app probes `${baseUrl}/api/status` — this endpoint only exists on the dashboard server (port 9119). The API server returns 404 for `/api/status`.

## Starting the Dashboard

```bash
# Local only (loopback) — safe, no auth needed
hermes dashboard

# Remote access via Tailscale/private network — needs --insecure
hermes dashboard --port 9119 --host 0.0.0.0 --insecure

# The dashboard REFUSES 0.0.0.0 bind without an auth provider:
# "Refusing to bind dashboard to 0.0.0.0 — the OAuth auth gate engages
#  on non-loopback binds, but no auth providers are registered"
# --insecure bypasses this gate. Only use on trusted networks (Tailscale, etc.)
```

## Session Tokens

- Token is ephemeral: generated fresh on every dashboard/gateway process start
- Stored in `~/.hermes/.env` as `HERMES_DASHBOARD_SESSION_TOKEN`
- Desktop app sends it via `X-Hermes-Session-Token` header (REST) or `?token=` query param (WebSocket)
- **Breaks on restart** — if the dashboard restarts, the desktop app must reconnect (it re-probes `/api/status` on startup)

## Auth Modes

Two modes (detected via `/api/status` → `auth_required` field):

1. **Token mode** (default, `auth_required: false`) — static session token, breaks on restart
2. **OAuth mode** (`auth_required: true`) — cookie-based, auto-refreshes via `/api/auth/ws-ticket`

Token mode is what self-hosted setups use. OAuth requires a configured provider (`dashboard.oauth.client_id` + `portal_url` in config.yaml).

## Tailscale Deployment Pattern

For desktop app connecting to VPS over Tailscale:

1. VPS must have Tailscale installed and connected (`tailscale status`)
2. Start dashboard with `--host 0.0.0.0 --insecure` (Tailscale is a private network)
3. Desktop app connects to `http://<VPS_TAILSCALE_IP>:9119`
4. Session token from `~/.hermes/.env` → `HERMES_DASHBOARD_SESSION_TOKEN`

```bash
# Verify VPS Tailscale IP
tailscale ip

# Verify dashboard reachable via Tailscale
curl -s -w "\nHTTP:%{http_code}" \
  -H "X-Hermes-Session-Token: $TOKEN" \
  http://<TAILSCALE_IP>:9119/api/status
```

## Persistence

The dashboard does NOT auto-restart on VPS reboot. Options:
- Add to systemd user service (like the gateway)
- Run via `hermes gateway` with embedded dashboard (if supported)
- Manual start on connect

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Desktop shows "cannot connect" | Wrong port (8642 instead of 9119) | Use port 9119 |
| 404 on `/api/status` | Hitting API server, not dashboard | Switch to dashboard port |
| "Unauthorized" after update | Session token changed on restart | Re-enter token from `~/.hermes/.env` |
| Dashboard won't start on 0.0.0.0 | No auth provider configured | Add `--insecure` for private networks |
| Desktop connects but chat doesn't work | WebSocket auth failing | Check token matches, try reconnecting |
