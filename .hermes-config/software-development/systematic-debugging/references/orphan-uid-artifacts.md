# Orphan UID Artifacts (Cross-Platform Copy)

## Pattern

Files on a Linux system owned by a UID that does not exist in `/etc/passwd`.
Typically manifests as `ls -la` showing a numeric UID (e.g., `1000 1000`) instead
of a username, and `getent passwd <UID>` returns nothing.

## Root Cause

The files were created on a different machine (often WSL) where that UID mapped
to a real user. They were then copied to the current machine (via rsync, scp,
tar, or filesystem migration) **preserving numeric UIDs**. Linux stores file
ownership as integers — when the integer doesn't match any local user, it
displays as a bare number.

**Common scenario:** Repo created on WSL (user `vthen`, UID 1000) → rsynced to
a Linux VPS running as root (UID 0). All `.git/` objects, source files, and
configs arrive tagged with UID 1000, which doesn't exist on the VPS.

## Symptoms

- `ls -la` shows `1000 1000` (numeric, not a name) for file ownership
- `chown` or `stat` on such files shows `Uid: ( 1000/ UNKNOWN)`
- Operations that require the file owner checks may behave unexpectedly
- On the **source machine** (WSL), the user cannot access files under `/root/`
  because WSL's `/root/` is owned by root with restricted permissions

## Diagnosis

```bash
# Find orphan UID files
find /path -not -user root 2>/dev/null | head -20

# Check if the UID exists
getent passwd 1000

# Stat a suspicious file
stat somefile | grep -i "uid\|gid"
```

## Fix

```bash
# Change ownership to current user (typically root on a VPS)
chown -R root:root /path/to/repo/.git

# Or for the entire tree
chown -R root:root /path/to/repo/
```

## Prevention

- When rsyncing between WSL and a Linux server, consider `--chown=root:root`
  to remap ownership at transfer time
- Or use `--no-owner --no-group` to strip ownership and let the receiving
  side set defaults
- Clone the repo fresh on the target machine rather than copying the `.git/`
  directory (avoids carrying UID metadata entirely)

## Related

- `engineering-discipline` — Principle 7 (Cleanup Verification) covers
  post-migration audit patterns that catch these artifacts
