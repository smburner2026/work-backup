# Community Manifest — Tracking Hermes Additions

File: `~/.hermes/community-manifest.json`

Single source of truth for everything added on top of base Hermes that has an update path outside `hermes update` or `hermes skills update`.

## Manifest Schema

```json
{
  "manifest_version": 1,
  "created": "YYYY-MM-DD",
  "note": "Describe purpose",
  "entries": [
    {
      "name": "doga",
      "type": "plugin|pip_package|skill|tool|config|other",
      "source": "URL or origin",
      "install_date": "YYYY-MM-DD",
      "version": "x.y.z",
      "install_method": "How it was installed",
      "update_command": "Shell command to update",
      "post_update": "Steps after updating (reload, reset, restart)",
      "status": "active|inactive|deprecated"
    }
  ],
  "update_policies": {
    "plugins": "Manual per entry",
    "pip_packages": "pip install --upgrade",
    "hub_skills": "hermes skills update",
    "agent_skills": "Managed by hermes curator",
    "base_hermes": "hermes update"
  }
}
```

## Status Values\n\n| Status | Meaning |\n|--------|---------|\n| `active` | Currently installed and in use on this machine |\n| `inactive` | Installed but disabled/dormant |\n| `deprecated` | No longer useful |\n| `known` | Tracked for awareness but NOT installed on this machine (e.g. installed on VPS or another machine) |\n\nUse `known` with a `note` explaining where it lives, so cross-machine dependencies are visible in one manifest.\n\n## Update This Manifest

Whenever adding something new to Hermes that isn't covered by `hermes update` or `hermes skills update`, add an entry and update `manifest_version` by +1.
