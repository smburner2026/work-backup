# Component Removal Audit

## The Problem

When removing a service, tool, or deployment from the workspace, incomplete cleanup leaves behind stale files, orphaned config references, running processes, and security traces. Over time these accumulate into disk bloat and confusing behavior.

## The Pattern — Post-Mortem Audit

When the user says "remove X completely, like it was never installed":

### Phase 1: Kill it

Stop and disable all running instances:

```bash
systemctl stop <service-name>     # or kill <PID>
systemctl disable <service-name>
rm /etc/systemd/system/<service-name>.service
systemctl daemon-reload
```

Check for leftover processes: `ps aux | grep <service-name>`

### Phase 2: Delete it

```bash
rm -rf /path/to/installation/
```

Check for secondary directories the service may have created.

### Phase 3: Trace it

Search for any remaining references in active configs:

```bash
# Config files
grep -rn <service-name> ~/.hermes/config.yaml ~/.hermes/.env ~/.hermes/profiles/

# Cron jobs
grep -rn <service-name> ~/.hermes/cron/

# Skills
grep -rn <service-name> ~/.hermes/skills/ --include='*.md' --include='*.yaml'

# Session DB leftovers (passive, no action needed)
```

### Phase 4: Audit checklist

| Check | Command | Clean state |
|---|---|---|
| Directory | `ls -la /path/to/service/` | "No such file or directory" |
| Systemd service | `systemctl is-enabled <name>` | "not-found" |
| Port | `ss -tlnp 'sport = :PORT'` | Empty |
| Process | `ps aux \| grep <name>` | grep-only (no process) |
| Config refs | `grep -rn '<path>' ~/.hermes/config.yaml` | Empty |
| Cron refs | `grep <name> ~/.hermes/cron/jobs.json` | Empty (or expected passive history) |
| Memory refs | `memory action=list` | Remove stale entries |

### Phase 5: Report

Present a structured verdict:

```
| Check | Result |
|---|---|
| Directory /path/ | ✅ purged |
| Systemd service | ✅ removed |
| Port XXXX | ✅ dead |
| Running processes | ✅ none |
| Config references | ✅ zero |
```

## Variation: Soft Removal (Experimental/Uncertain)

If the user isn't sure they'll want the service back, use the recycle-bin pattern instead:

```bash
mv /path/to/service/ ~/recycle-bin/YYYY-MM-DD/<path>
```

Then proceed with the audit. The files survive until they empty the recycle bin.

## Known Applications of This Pattern

- **Hermes Workspace** (port 3000): Node.js web UI, systemd service, 2GB. Post-mortem: directory, systemd, port 3000, config refs in cron prompts all cleaned.
- **WSL Hermes CLI**: Local terminal UI, no systemd, path-only cleanup.
- **NordVPN**: Desktop VPN client that interferes with Tailscale WireGuard tunnels causing `DERP-relay only` mode.
