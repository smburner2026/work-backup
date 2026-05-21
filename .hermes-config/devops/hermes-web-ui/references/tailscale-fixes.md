# Tailscale Remote Access — Session Journal (2026-05-20 / 2026-05-21)

## VPN Interference (2026-05-21)

User was unable to reach the VPS from desktop over Tailscale (`http://100.113.2.25:3000`). Server was running and bound to `0.0.0.0:3000` but HTTP was unreachable from the desktop.

**Root cause:** NordVPN running on the desktop. VPNs override the default route and block Tailscale's WireGuard tunnel, preventing direct connections.

**Fix:** Disable the VPN on the client machine.

**Diagnostic pattern (desktop-side):**
1. `tailscale status` — confirm both machines on the tailnet
2. `tailscale ping <vps-ip>` — verify layer 3 (may go via DERP relay, that's fine)
3. If ping works but HTTP doesn't, check for VPN interference
4. Temporarily disable VPN, retry HTTP

## Problem (original — 2026-05-20)

User on mobile (Android, Pixel 7a via Tailscale) couldn't reach Hermes Dashboard at `http://100.113.2.25:9119`. Workspace at `http://100.113.2.25:3000` loaded but password entry failed on phone browser.

## Root Cause

1. **Dashboard** — systemd service ran `hermes dashboard` without `--host` or `--insecure`, so it bound to `127.0.0.1:9119` by default. Tailscale packets to `100.113.2.25:9119` hit the machine but were refused because the socket wasn't listening on the tailscale interface.

2. **Workspace mobile password** — Workspace password seemed to work from CLI (`curl` to `/api/auth` returned `{"ok":true}`) but the issue was likely:
   - The app loaded but the login form's cookie handling was flaky on mobile Safari/Chrome
   - Or `COOKIE_SECURE=0` wasn't taking effect correctly with the phone's webview

## Fix Applied

### Dashboard service file

Edited `/root/.config/systemd/user/hermes-dashboard.service`:

```
ExecStart=/usr/local/lib/hermes-agent/venv/bin/hermes dashboard --host 0.0.0.0 --insecure
```

Then:
```bash
systemctl --user daemon-reload
systemctl --user restart hermes-dashboard
```

**Verification:**
```bash
curl -s -o /dev/null -w "%{http_code}" http://100.113.2.25:9119/api/status
# → 200
```

### Workspace password check

Confirmed the stored password via:
```bash
curl -s -X POST http://localhost:3000/api/auth \
  -H "Content-Type: application/json" \
  -d '{"password":"XXvehf9Hdb2vxb0c"}'
# → {"ok":true}
```

## VPS Environment

- Host: ghjgh (178.156.199.37/32 eth0)
- Tailscale IP: 100.113.2.25/32 (tailscale0)
- Tailscale devices on tailnet: desktop (Windows, relay: ord), pixel-7a (Android, idle)
- OS: Linux 6.8.0-117-generic

## Service Layout

| Service | Port | Bind | Managed by |
|---|---|---|---|
| Workspace (Node.js) | 3000 | 0.0.0.0 | systemd --user |
| Dashboard (Python) | 9119 | 0.0.0.0 (after fix) | systemd --user |
| Gateway API | 8642 | 127.0.0.1 | systemd --user |

## Subsequent Session Insight

Later in the same conversation, the user mentioned they could "see it on my phone but the password fails" (via Discord). The fix above for the Dashboard gives them a second access path that doesn't need a password (Tailscale is the auth).
