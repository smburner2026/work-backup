# Community Additions Manifest — Reference

Location: `~/.hermes/community-manifest.json`

## Purpose

Single source of truth for every addition to a Hermes instance that falls outside `hermes update`. Prevents drift — you never lose track of what's been bolted on, where it came from, or how to update it.

## Current Entries (this instance)

| Name | Type | Version | Update path |
|------|------|---------|-------------|
| DOGA | plugin | 1.1.0 | manual git clone → recopy |
| hermes-lcm | plugin (bundled dir) | 0.11.1 | git pull in install dir |
| mnemosyne-memory | pip package | 3.0.0 | pip install --upgrade |
| HERM | external tool | unknown | git pull + Bun rebuild (VPS) |
| HMS | bash_script | 1.1 | edit / refresh from skill |
| work-backup | cron_script | N/A | edit directly |
| hub-skills (43) | skills_group | N/A | hermes skills update |
| touchdesigner-mcp | skill | unknown | hermes skills update |

## How to update

1. Read the manifest: `cat ~/.hermes/community-manifest.json`
2. Find the entry's `update_command`
3. Run the command
4. If version changed, update the `version` field
5. If entry removed, set `status` to `archived`

## Common update commands

```bash
# Hermes base
hermes update

# Hub skills
hermes skills update

# Pip packages
pip install --upgrade mnemosyne-memory

# Plugins with git remotes (LCM)
cd /usr/local/lib/hermes-agent/plugins/context_engine/lcm && git pull

# Manual plugins (DOGA) — from source repo
cd /tmp && git clone https://github.com/0z1-ghb/doga-hermes.git --depth 1
cp doga-hermes/doga/*.py ~/.hermes/plugins/doga/
cp doga-hermes/plugin.yaml ~/.hermes/plugins/doga/
rm -rf /tmp/doga-hermes
```
