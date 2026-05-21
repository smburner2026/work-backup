# Component Removal — Complete Verification Checklist

Use this checklist after removing any component (service, package, workspace, tool) to ensure zero traces remain. General-purpose post-mortem audit; adapt per component.

## Checks

1. **Filesystem** — install directories, secondary dirs, startup scripts, config/data/cache files
2. **Services** — systemd service removed, stopped, disabled, daemon-reload, no stale processes
3. **Network** — port unbound (`ss -tlnp | grep <port>`), no reverse-proxy pointing at it
4. **Config & Env** — `config.yaml`, `.env`, profile configs free of stale references
5. **Automation** — cron jobs don't reference its URL, paths, or commands
6. **Independent components** — verify remaining services still work (Dashboard, gateway, etc.)

## Example: Hermes Workspace Removal

| Check | Result |
|---|---|
| Install directory | ✅ purged |
| Systemd service | ✅ removed, disabled, stopped |
| Port 3000 | ✅ dead |
| Node processes | ✅ none |
| config.yaml/.env refs | ✅ zero |
| Cron job refs | ✅ cleaned |
| Dashboard (9119) | ✅ 200 OK |
