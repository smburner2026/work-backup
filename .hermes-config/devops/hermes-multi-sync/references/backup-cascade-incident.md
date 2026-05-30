# HMS Backup Cascade Incident — 2026-05-24

## Root Cause

The `RSYNC_SAFE` variable in `~/.hermes/bin/hms` used `--backup --suffix=.hms-bak` without excluding the backup files themselves. On every sync cycle:

1. Rsync overwrites file `X` with a newer version from the other side
2. The old version of `X` is renamed to `X.hms-bak` as a recovery copy
3. On the **next** sync cycle, `X.hms-bak` is a new file that hasn't been synced
4. Rsync copies it to the other side AND creates `X.hms-bak.hms-bak` as a backup of the backup
5. Cascade continues infinitely: `X.hms-bak.hms-bak.hms-bak`... (up to 11+ generations observed)

## Impact

- **15,714** `.hms-bak` files accumulated in `~/work/` within hours
- Hundreds of MB of disk wasted
- Files bounced back and forth between machines on every sync
- Other directories (`~/.hermes/skills/`, `~/.hermes/profiles/`, etc.) also affected

## Fix Applied

Added `--exclude=*.hms-bak*` to the `RSYNC_SAFE` variable in `~/.hermes/bin/hms`:
```
RSYNC_SAFE="-avz --no-o --no-g --no-t --update --backup --suffix=.hms-bak --exclude=*.hms-bak*"
```

## Cleanup

The existing `.hms-bak*` debris must be removed separately:

```bash
# Both directories, both machines
find ~/.hermes ~/work -name '*.hms-bak*' -type f -delete
```

**Important**: `hms cleanup` only scans `~/.hermes/` not `~/work/`. After a backup cascade, run the `find` command above on both sides.

## Symptoms to Watch

- `hms status` showing files named `*.hms-bak*` in the diff list
- Growing disk usage without new work
- Files with repeated `.hms-bak` suffixes (more than 2-3 generations means active cascade)

## Prevention

- `--exclude=*.hms-bak*` prevents new cascade cycles
- `hms cleanup` should be extended to also cover `~/work/` if the script hasn't been patched
- After upgrading HMS, always run the patch on **both** VPS and local WSL (script is not self-syncing)
