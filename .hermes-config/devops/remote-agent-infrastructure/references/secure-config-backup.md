# Secure Hermes Config Backup to Git

## The Problem

Hermes stores configuration, persona files, memory, and skills under `~/.hermes/`. Some of these files contain **secrets** — Discord bot tokens, API keys, passwords — that must never reach a git remote, even a private one.

Backing up the full `~/.hermes/` directory to a git repo without precautions will leak those secrets.

## The Pattern — Staged Backup with Redaction

### 1. Sync to a staging directory inside the git working tree

```bash
rsync -a --delete ~/.hermes/config.yaml ~/.hermes/SOUL.md \
  ~/.hermes/memories/ ~/.hermes/skills/ \
  /path/to/repo/.hermes-config/
```

This copies everything you want backed up into a subdirectory of your git working tree. The original `~/.hermes/` is untouched.

### 2. Redact secrets in the staging copy

Any token or password that appears in `config.yaml` must be stripped **before** the staged copy hits git. Use `sed` to replace known secret patterns:

```bash
sed -i 's/    token: [0-9].*/    token: REDACTED/' /path/to/repo/.hermes-config/config.yaml
```

The original `~/.hermes/config.yaml` is untouched — this only modifies the staging copy.

### 3. Never include `.env` in git

The `.env` file contains API keys. It should never be copied into the staging directory. The rsync command above doesn't include it. If you add it later, add it to `.gitignore`:

```bash
echo ".hermes-config/.env" >> .gitignore
```

### 4. Commit as part of regular backup

```bash
cd /path/to/repo
git add -A
git commit -m "backup $(date +'%Y-%m-%d %H:%M UTC')"
git push
```

## Full Workflow Script

```bash
#!/bin/bash
# backup.sh — run before any git commit that includes Hermes config
set -e

REPO_DIR="/root/work"

# 1. Sync config to work dir
rsync -a --delete ~/.hermes/config.yaml ~/.hermes/SOUL.md \
  ~/.hermes/memories/ ~/.hermes/skills/ \
  "$REPO_DIR/.hermes-config/"

# 2. Redact known secrets
sed -i 's/    token: [0-9].*/    token: REDACTED/' \
  "$REPO_DIR/.hermes-config/config.yaml"

# 3. Commit and push (assumes git add was already done)
cd "$REPO_DIR"
git add .hermes-config/
git commit -m "backup $(date +'%Y-%m-%d %H:%M UTC')"
git push
```

## Verification

After a backup push, verify no secrets leaked:

```bash
# On a fresh clone of the repo
grep -rn "token:\|api_key:\|password:\|secret:" .hermes-config/ \
  | grep -v "REDACTED\|''\|: ''"
```

If this produces any output, a secret is still leaking. Add it to the sed redaction pattern.

## Disaster Recovery

If the VPS dies:

```bash
git clone git@github.com:owner/repo.git
cp -r repo/.hermes-config/* ~/.hermes/
```

Then manually recreate `~/.hermes/.env` with API keys from your password manager.

## Known Secret Locations in Hermes Config

| File | Secret field | Redaction pattern |
|---|---|---|
| `config.yaml` | `gateway.telegram.token` | `sed -i 's/    token: [0-9].*/    token: REDACTED/'` |
| `config.yaml` | `gateway.discord.token` | Same pattern (different key, same format) |
| `.env` | ALL keys | **Never sync this file to git** |

## Pitfalls

- **Redact BEFORE add** — if you `git add` the staging directory first and then `sed`, the add command already staged the unredacted file. Sequence: rsync → sed → git add.
- **Not all secrets live in config.yaml** — check `config.yaml` for any field with a real opaque value (non-empty, non-boolean, non-integer) and evaluate whether it's a secret.
- **GitHub will alert you** — GitHub's secret scanning catches pushed tokens. If you get an alert, rotate the leaked token immediately and update the redaction pattern to prevent recurrence. The commit with the secret stays in git history even after a follow-up redacting commit — rotate the credential, don't trust the redaction commit as a fix.
- **Private repos are not safe for secrets** — GitHub scans private repos for secrets if secret scanning is enabled on the repo. Even without scanning, anyone with repo access has the credential.
- **Rsync default preserves UIDs** — when syncing between machines with different users, add `--no-owner --no-group` to rsync to avoid orphan UID artifacts in the staging directory. See `references/git-cross-environment.md` for the UID ownership pitfall.
