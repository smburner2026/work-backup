# Hermes Desktop — Remote Gateway on VPS via Tailscale

Connecting the official Hermes Desktop (Nous Research Electron app) to a remote VPS instance using the **dashboard** service behind Tailscale.

## Architecture

```
Desktop App (Windows/Mac)          VPS
┌──────────────────────┐          ┌──────────────────────┐
│  Settings → Gateway   │          │  hermes dashboard    │
│  → Remote gateway    │  ◄──────►│  :9119               │
│  http://100.x.y.z    │ Tailscale│  --host 0.0.0.0      │
│  :9119               │   mesh   │  --insecure           │
│  + session token     │          │  --tui                │
└──────────────────────┘          │  --no-open            │
                                  └──────────────────────┘
```

The desktop app is an **Electron GUI** for the Hermes Agent runtime. It is NOT a thin remote client — it installs its own agent locally by default. Remote gateway mode lets it talk to a VPS-hosted instance instead, using the **dashboard** HTTP service.

## Prerequisites

- Hermes Agent already running on the VPS (with gateway, cron, etc.)
- Tailscale installed on both VPS (`sudo tailscale up`) and the local machine
- Both on the **same tailnet** — verify with `tailscale status`

### ⚠️ WSL Tailscale ≠ Windows Tailscale

Tailscale inside WSL is a **separate network identity** from the Windows host. Installing Tailscale in WSL (`curl -fsSL https://tailscale.com/install.sh | sh`) gives WSL its own `100.x.y.z` IP — but that IP belongs to WSL's Linux network namespace, NOT Windows.

The Hermes Desktop app runs on **Windows**, so it needs **Windows-native Tailscale** installed directly on Windows. WSL's Tailscale won't make `100.x.y.z` addresses reachable from Windows.

**Verify on Windows:**
```cmd
ping 100.x.y.z
```
If you get "General failure" or 100% loss, Windows isn't on the tailnet. Install Tailscale from [tailscale.com/download/windows](https://tailscale.com/download/windows) and sign in with the same account.

## Setup Steps

### 1. Generate a Dashboard Session Token

```bash
# On the VPS:
openssl rand -hex 32
```

Store it in `~/.hermes/.env`:

```bash
echo 'HERMES_DASHBOARD_SESSION_TOKEN=<generated-token>' >> ~/.hermes/.env
```

This token authenticates the desktop app to the dashboard. The field in the desktop app is labelled **"Session Token"**.

### 2. Start the Dashboard

```bash
HERMES_DASHBOARD_SESSION_TOKEN=<token> \
  hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open --tui
```

Key flags:

| Flag | Why |
|------|-----|
| `--host 0.0.0.0` | Binds to all interfaces so Tailscale can reach it |
| `--insecure` | Required for non-localhost binding |
| `--tui` | Exposes the Chat tab (the core agent interaction) |
| `--no-open` | Don't launch browser on the VPS (no display) |

For **production persistence**, wrap it in a systemd service (see the parent skill's systemd patterns).

### 3. Configure the Desktop App

1. Close any existing/stuck connection attempt
2. Open the app
3. ⚙️ **Settings → Gateway → Remote gateway**
4. Enter:
   - **URL:** `http://<VPS-TAILSCALE-IP>:9119`
   - **Session Token:** the token from step 1

Find the VPS Tailscale IP:

```bash
tailscale ip -4
```

### 4. Verify

The app should connect and show the chat interface. You're now talking to the VPS agent from your local desktop.

**From the VPS side,** verify the token works:
```bash
curl -fsS -H "X-Hermes-Session-Token: $TOKEN" http://127.0.0.1:9119/api/config >/dev/null \
  && echo "✅ Token works" || echo "❌ Token failed"
```

**From the Windows side,** confirm the tailnet can reach the dashboard:
```cmd
ping <VPS_TAILSCALE_IP>
```
Should return replies, not "General failure" or "Request timed out."

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Connecting..." stuck (first attempt) | Wrong port/token | Dashboard is on **9119**, uses `HERMES_DASHBOARD_SESSION_TOKEN` (not API_SERVER_KEY on port 8642) |
| "Connecting..." stuck (after failed attempt) | App cached stale connection state | Fully close the app (check system tray too), reopen, re-enter URL + token |
| Connection refused | Dashboard not running | `ss -tlnp \| grep 9119` on VPS to check |
| "Not authorized" / bad token | Token mismatch | Regenerate with `openssl rand -hex 32` and update both `.env` and desktop app |
| Gateway restart blocked | Can't restart from within gateway session | Send `/restart` in Telegram, or `systemctl --user restart hermes-gateway` from SSH |
| Ping returns "General failure" | Windows not on the tailnet | Install Tailscale on Windows directly (WSL Tailscale doesn't carry over) |
| Ping fails, then works after turning off VPN | VPN (NordVPN, etc.) blocking Tailscale | Whitelist Tailscale in VPN settings, or disconnect VPN for tailnet traffic |
| Dashboard stops after reboot | No persistence — dashboard not wrapped in systemd | Add systemd service (see "Production Persistence" below) |

## Production Persistence (Systemd)

The dashboard does **not** auto-start with the gateway. After a VPS reboot, the dashboard process dies until manually restarted. Wrap it in a systemd service for persistence.

Create `~/.config/systemd/user/hermes-dashboard.service`:

```ini
[Unit]
Description=Hermes Dashboard — Remote gateway for Desktop App
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open --tui
Restart=on-failure
RestartSec=5
EnvironmentFile=%h/.hermes/.env

[Install]
WantedBy=default.target
```

Note: `EnvironmentFile=%h/.hermes/.env` loads `HERMES_DASHBOARD_SESSION_TOKEN` automatically. `%h` expands to the user's home directory.

Enable and start:

```bash
systemctl --user daemon-reload
systemctl --user enable hermes-dashboard
systemctl --user start hermes-dashboard
```

Verify:

```bash
systemctl --user status hermes-dashboard --no-pager
ss -tlnp | grep 9119
```

## Common Confusions

- **Port 9119 (dashboard) ≠ port 8642 (API server).** The desktop app connects to the dashboard service, not the API server. These are different processes with different auth mechanisms.
- **API_SERVER_KEY (in .env) ≠ HERMES_DASHBOARD_SESSION_TOKEN (in .env).** The API server authenticates with `API_SERVER_KEY` for OpenAI-compatible endpoints. The dashboard authenticates with `HERMES_DASHBOARD_SESSION_TOKEN` for the desktop app. They are independent.
- **The SSH-based Hermes Desktop (fathah/hermes-desktop).** There is a separate community project (`fathah/hermes-desktop`) that connects via SSH, not the dashboard. The official Nous Research desktop app uses the dashboard (port 9119) for remote gateway.
- The `--insecure` flag only affects binding (allows `0.0.0.0` instead of `127.0.0.1`). It does NOT disable auth. The session token is still required.
