# Cross-Environment Git — Permission and UID Debugging

## The Pattern

A git repo created on one machine and synced/copied to another (e.g., WSL → VPS) **preserves the original UID ownership** in `.git/`. If the two machines run different users (e.g., `vthen`/UID 1000 on WSL vs. `root`/UID 0 on VPS), this creates a fragile setup where permissions work by accident or fail silently.

## Symptom

```
ls: cannot open file '/root/work/.git/': Permission denied
```

This happens when user on the target machine (WSL's `vthen`, UID 1000) tries to access a git repo at a path they don't own. On WSL, `/root/` is `drwx------` root-owned — `vthen` can't even list the directory.

## Diagnostic

```bash
# Check .git/ ownership
ls -la /path/to/repo/.git/ | head -5
# Look for UID:GID that don't match the running user

# Check if the orphan UID exists on this machine
getent passwd 1000
getent group 1000
# "No user with UID 1000" = orphan UID from cross-machine copy

# See what user you're running as
id

# Check if git operations work despite the mismatch
cd /path/to/repo && git status 2>&1 | head -20
```

## Root Cause

1. Repo cloned/created on Machine A (user X, UID 1000)
2. Entire repo (including `.git/`) synced via rsync/scp to Machine B (user Y, UID 0)
3. Rsync preserves UID unless told otherwise (`--no-owner --no-group`)
4. Machine B's git works by accident if user Y is root (root reads everything)
5. If files are synced back to Machine A, writes from Machine B may land with wrong UID → Permission denied on Machine A
6. If a Hermes cron job or script runs as a non-root user on Machine B → immediate crash

## Fixes

### Fix A — Take ownership on the VPS (simplest, one authoritative machine)

```bash
chown -R root:root /path/to/repo/.git/
```

This makes the VPS authoritative. Works when you always work on the VPS and only clone/pull from WSL.

### Fix B — Clone separate per-machine working copies

Don't share the `.git/` across machines. Each machine gets its own clone:

```bash
# On WSL (as vthen)
git clone git@github.com:owner/repo.git /home/vthen/work

# On VPS (as root)
git clone git@github.com:owner/repo.git /root/work
```

Push from one, pull from the other. No UID collisions because each `.git/` is owned by the local user.

### Fix C — Recreate UID 1000 on the VPS (advanced, not recommended)

```bash
useradd -u 1000 gituser
chown -R 1000:1000 /path/to/repo/.git/
```

Fragile — creates a phantom user just to match file ownership. Breaks on reimage.

## Verification

After fixing, run these as the user who will use the repo:

```bash
cd /path/to/repo && git status
git log --oneline -3
git config --list | head -5
```

If all three pass cleanly without Permission denied or `detected dubious ownership` warnings, the fix is solid.

## Pitfalls

- **`git status` says "detected dubious ownership in repository"** — newer git versions (2.35+) refuse to operate on repos owned by a different user. Fixed by: `git config --global --add safe.directory /path/to/repo` (per-user workaround) or Fix A above (proper ownership).
- **Cron jobs that run git commands** — if the cron job's `workdir` is set to a path the cron runtime user can't access, the job will fail silently. Check cron job state with `cronjob action=list` and verify `last_status`.
- **Nightly self-improvement runs that scan work dirs** — if Phase 3 tries to `cd /root/work/` as a non-root user, it crashes the entire cron run. Add the workdir to the scan's exclusion list or fix ownership.
- **rsync preserves UIDs** — default rsync with no `--no-owner` flag tries to preserve original UIDs. On a different machine those UIDs may not exist. Always add `--no-owner --no-group` when syncing git repos between machines with different users.
