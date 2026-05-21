# Mobile Phone VPS Access via Tailscale + Termux + SSH

## Purpose
Emergency/on-the-go access to the Hermes VPS from a phone when the Telegram/Discord relay is unavailable or insufficient. Creates a secure SSH path through Tailscale's mesh network.

## Architecture

```
Phone (Termux) ─── Tailscale ─── VPS
     ↑                              │
     │           ┌──────────────────┘
     └─── SSH (tailscale ssh) ──────┘
```

The normal path (Phone → Telegram/Discord → Hermes → VPS) handles 99% of usage. This is the **maintenance back door** — for rebooting the agent, editing raw configs, checking disk, or fixing Hermes itself.

## Prerequisites

- **VPS**: Linux (Ubuntu 24.04 in this setup)
- **Phone**: Android (Termux via F-Droid)
- **One Tailscale account** (free tier supports 3 devices)

## VPS Setup (Server Side)

```bash
# Install Tailscale (one-time)
curl -fsSL https://tailscale.com/install.sh | sh

# Start daemon and authenticate
systemctl start tailscaled
tailscale up
# → Visit the printed URL in a browser to log into your Tailscale account
```

Tailscale runs as a systemd service — it persists across reboots automatically.

## Phone Setup

### 1. Install Termux via F-Droid
- Install **F-Droid** from f-droid.org (NOT Google Play — Play version is outdated)
- From F-Droid, install **Termux**

### 2. Install termux packages
```bash
pkg update && pkg upgrade
pkg install openssh tailscale
```

### 3. Authenticate Tailscale on phone
```bash
tailscale up
# → Opens browser to log into same Tailscale account as VPS
```

### 4. Find phone's Tailscale IP
```bash
tailscale ip -4
# → e.g. 100.x.x.x
```

### 5. Optional: SSH into phone from local machine
```bash
# On phone (in Termux):
passwd        # set a password for Termux's user
sshd          # starts SSH on port 8022 (Termux uses non-privileged port)

# From local machine (on same tailnet):
ssh <termux-user>@<phone-tailscale-ip> -p 8022
```

## Connecting to VPS from Phone

```bash
# In Termux after Tailscale is authenticated on both devices:
tailscale ssh root@<vps-tailscale-ip-or-hostname>
```

Tailscale SSH uses the tailnet's auth layer — no password needed, no SSH key management.

## When to Use

| Scenario | Use Telegram/Discord | Use Tailscale+SSH |
|---|---|---|
| Normal agent work | ✅ | ❌ |
| Hermes crashed/not responding | ❌ | ✅ |
| Telegram/Discord is down | ❌ | ✅ |
| Edit raw config files | ❌ | ✅ |
| Check disk/memory/uptime | ❌ | ✅ |
| Reboot VPS | ❌ | ✅ |
| Quick git push/pull | ❌ | ✅ |

## How Telegram Handles Disconnects (Why tmux Is Not Needed for Normal Use)

Telegram acts as a message relay. When the phone loses signal mid-conversation:
- Telegram's servers queue the reply → delivered when the phone reconnects
- Hermes on the VPS doesn't notice the phone disconnected
- No session to preserve — tmux only matters when SSH is the direct link

## tmux (Optional, for SSH-Only Workflows)

Only needed if you plan to run long processes directly over SSH from Termux (not through Hermes):
- `tmux new -s work` — start a named session
- `tmux attach -t work` — reattach after disconnect
- Keeps terminal state, scrollback, and running processes alive across network drops

For emergency access (fix-reboot-leave), tmux is unnecessary complexity.

## Key Facts from Setup

- VPS Tailscale auth URL (still valid until authenticated): `https://login.tailscale.com/a/1916df4901b0ee`
- Termux SSH port: 8022 (non-privileged, not 22)
- Tailscale free tier: up to 3 devices (VPS + phone + laptop fits easily)
