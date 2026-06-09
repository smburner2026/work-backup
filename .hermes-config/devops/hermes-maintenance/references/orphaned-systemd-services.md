# Orphaned systemd Services Cleanup

When a Hermes profile is deleted or renamed, its systemd gateway service may persist at `/etc/systemd/system/hermes-gateway-<name>.service` — disabled but still registered, causing failed start attempts on boot.

## Detection

```bash
# List all hermes gateway services
systemctl list-unit-files | grep hermes-gateway

# Check for per-profile services
ls /etc/systemd/system/hermes-gateway-*.service 2>/dev/null
```

## Cleanup

```bash
# For each orphaned service:
sudo systemctl stop hermes-gateway-<name>.service
sudo systemctl disable hermes-gateway-<name>.service
sudo rm /etc/systemd/system/hermes-gateway-<name>.service
sudo systemctl daemon-reload
```

## Also Check active_profile

After profile removal, verify `~/.hermes/active_profile` doesn't reference the deleted profile:

```bash
cat ~/.hermes/active_profile 2>/dev/null
# If it references a deleted profile, delete the file (canonical default = file absent)
rm -f ~/.hermes/active_profile
```

See the `profile-isolation` skill for the active_profile guard script that automates this check.
