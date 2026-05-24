# Hermes Migration Pattern

When transferring a Hermes installation to a new machine (fresh OS, offline box, different user), use this bundle-and-restore pattern.

## What to Transfer

| Priority | Path | Typical Size | Notes |
|---|---|---|---|
| Critical | `~/.hermes/sessions/` | 168 MB | All conversation history |
| Critical | `~/.hermes/skills/` | 14 MB | Custom/adapted skills |
| Critical | `~/.hermes/config.yaml` | 16 KB | API keys, MCP servers, profiles |
| Critical | `~/.hermes/lcm.db` | 6 MB | Conversation context engine |
| Important | `~/.hermes/mnemosyne/` | 649 MB+ | Memory database (can be compressed) |
| Important | `~/.hermes/cache/documents/` | 5 MB | Uploaded CSVs, user files |
| Important | `~/.hermes/cron/` | 184 KB | Scheduled jobs |
| Nice to have | `~/.hermes/logs/` | 15 MB | Past run logs |
| Nice to have | `~/.hermes/image_cache/` | 1 MB | Chart screenshots |
| Project | Work directories (e.g. `~/bambam-fatcat-project/`) | Varies | Project artifacts |

## Pre-Backup Optimization

Mnemosyne accumulates massive session-scoped working memory that bloats the DB. Consolidate first:

```
# Dry run to see what will be consolidated
mnemosyne_sleep(all_sessions=True, dry_run=True)

# Real consolidation (estimates: 649MB → 7.2MB for ~80 sessions, 1,300+ items)
mnemosyne_sleep(all_sessions=True)
```

Also purge stale global memory entries that are superseded by newer findings, especially session artifacts that got saved as global:

```
mnemosyne_invalidate(memory_id="<id_of_stale_entry>")
```

## Backup Command

```bash
tar -czf /tmp/hermes-transfer.tgz \
  -C / \
  home/<user>/.hermes/sessions \
  home/<user>/.hermes/lcm.db \
  home/<user>/.hermes/skills \
  home/<user>/.hermes/config.yaml \
  home/<user>/.hermes/cron \
  home/<user>/.hermes/cache/documents \
  home/<user>/.hermes/image_cache \
  home/<user>/.hermes/mnemosyne/data \
  home/<user>/.hermes/memories \
  home/<user>/bambam-fatcat-project
```

Adjust paths relative to the target extraction root. The `-C /` switch lets paths be specified relative to `/` and extracted relative to whatever root is desired.

## Restore on Fresh Install

1. Install Hermes fresh on the new machine (this creates the directory structure)
2. Stop Hermes: `hermes stop`
3. Extract the tarball OVER the fresh installation:

```bash
# If running as root, paths are root/.hermes/
cd / && tar -xzf /path/to/hermes-transfer.tgz

# If running as a regular user with different home:
tar -xzf /path/to/hermes-transfer.tgz --strip-components=1 -C ~/
```

4. Verify critical files landed before starting:
   - `ls ~/.hermes/sessions/` — should show 100+ session files
   - `ls ~/.hermes/mnemosyne/data/` — should show `mnemosyne.db`
   - `ls ~/.hermes/skills/` — should show 60+ skill directories
   - `ls ~/.hermes/cache/documents/` — should show CSV/data files

5. Restart Hermes: `hermes start` (or close/reopen Telegram chat)

## Notes

- `~/.hermes/hermes-agent/` (1.9 GB) is the source installation — DO NOT transfer it. Install fresh via `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
- `~/.hermes/state-snapshots/` (1.3 GB) are backup snapshots from the previous Hermes version. Only transfer if you need rollback capability.
- `~/.hermes/node/` (222 MB) is Node.js runtime — reinstall on target via `nvm` or system package.
- Config contains API keys — sanitize if the tarball will be stored or transmitted insecurely.
