# VPS File Server — Tailscale-Bound File Delivery

## Problem

The user creates/downloads files on the VPS and needs them on their local Windows machine. SCP commands are friction. File size limits prevent Telegram/Discord delivery for large files (PDF textbooks at 50-100 MB).

## Solution: Tailscale-Bound HTTP File Server

A lightweight Python HTTP server bound to the VPS's Tailscale IP, serving a ~/deliver/ directory. The user opens a browser on their local machine, clicks to download, and tells the agent to "nuke them" when done.

### Architecture

- VPS port 8080 bound to Tailscale IP only
- No public ports exposed -- only accessible within the tailnet
- No authentication needed -- Tailscale mesh is the auth layer
- Directory listing enabled for easy browsing

### Setup

**1. File server script** (~/.hermes/bin/hermes-file-server.py):
- Python http.server bound to Tailscale IP (100.113.2.25)
- Serves ~/deliver/ with directory listing
- Single-threaded but fine for one-off transfers

**2. Systemd user service** (~/.config/systemd/user/hermes-file-server.service):
- After network-online.target and tailscaled.service
- Restart on failure

**3. Management script** (~/.hermes/bin/deliver):
- deliver start | stop | status | url | ls | put <file> | cleanup

### Workflow

1. Agent creates/downloads files -> deliver put /path/to/file
2. User opens http://100.113.2.25:8080 in local browser
3. User clicks to download
4. User tells agent "downloaded now, nuke them"
5. Agent runs deliver cleanup

### Notes

- The Python http.server module is single-threaded -- large file transfers block other connections. Acceptable for one-off delivery.
- For production continuous access, use tailscale serve or a production-grade server.
- Start the server only when files need to be delivered; stop it after. The user requested minimal surface area ("shutdown all online services except the gateway").
- The deliver script assumes ~/.hermes/bin is in PATH.
