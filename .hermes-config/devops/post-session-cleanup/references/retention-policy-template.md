# Retention Policy Template

Use this when defining rotation rules for Hermes or project artifacts.

## Hermes default policy

| Category | Rule | Value |
|---|---|---|
| session JSON | archive older than | 14 days |
| session JSON | keep recent per prefix | 12 files |
| session JSON | compress | gzip |
| protected files | do not move | sessions.json, sessions.db |
| request dumps | archive older than | 7–14 days |
| config backups | keep latest | 1 |
| config backups | archive older than | immediate |

## Implementation checklist

- Protected files listed in policy must match the live-path prune/compress script.
- Archive path must exist before cleanup runs.
- Runs must report compressed count, moved config count, and final archive size.
- Cron jobs must run with a stable working directory so relative scripts resolve.
