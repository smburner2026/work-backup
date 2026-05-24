# Telegram Bot Token Leak Incident — Worked Example

## Scenario

GitHub sent a secret-scanning alert: a Telegram bot token was found in a pushed git commit. The token was in `config.yaml` which had been backed up into the repo by an automation script.

## The Problem

A daily `work-backup.sh` script copied `~/.hermes/config.yaml` (containing the live Telegram bot token) into `~/work/.hermes-config/` and then `git add -A && git commit && git push` to GitHub. Both the committed file AND all git history now contained the plaintext token.

## The Fix — Step by Step

### 0. Assessment

```bash
# What was leaked?
cd ~/work
git show HEAD:.hermes-config/config.yaml | grep 'token:'
# → 8910979795:AAG5-...... (Telegram bot token)

# Which commit introduced it?
git log --all --oneline -- .hermes-config/config.yaml
# → 644e6f0 "add hermes config backup"

# What else was in that commit?
git show 644e6f0 --name-only
# → .hermes-config/config.yaml (the config file)
# → .hermes-config/.bundled_manifest
```

### 1. Revoke the Token (USER ACTION)

Go to [@BotFather](https://t.me/botfather) on Telegram → `/mybots` → select your bot → Bot Settings → Revoke token.

**This kills the old token immediately.** The git purge that comes next is damage control — revocation is the real fix.

### 2. Prepare git-filter-repo

```bash
# Install
pip install git-filter-repo

# Save remote URL
REMOTE_URL=$(cd ~/work && git remote get-url origin)

# Confirm clean working tree
cd ~/work && git status --short

# Create replacement file
# NOTE: TG token contains ":" so avoid literal: prefix — use raw format
printf '%s==>REDACTED\n' '8910979795:AAG5-w5l_tU6t1punzju7alSsAbRLKkq1fg' > /tmp/token-replace.txt

# ALWAYS verify the file
od -c /tmp/token-replace.txt | head -3
```

### 3. Clone Fresh and Purge

```bash
cd /tmp
git clone ~/work purge-work
cd purge-work

git filter-repo --replace-text /tmp/token-replace.txt --force
```

### 4. Verify

```bash
# Should return 0
git log --all -p | grep -c '8910979795'
git log --all -p | grep -c 'AAG5-w5l_tU6t1punzju7alSsAbRLKkq1fg'

# Verify REDACTED appears where the token was
git log --all -p | grep 'token:' | sort -u
# → token: REDACTED

# Check HEAD is clean
git show HEAD:.hermes-config/config.yaml | grep 'token:'
# → token: REDACTED
```

### 5. Force Push

```bash
git remote add origin "$REMOTE_URL"
git push origin --force --all
```

### 6. Reset Local

```bash
cd ~/work
git fetch /tmp/purge-work main
git reset --hard FETCH_HEAD
```

### 7. Garbage Collection

```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
rm -rf .git/refs/original/

# Final verification
git log --all -p | grep -c 'AAG5-w5l_tU6t1punzju7alSsAbRLKkq1fg'
# → 0
```

### 8. Harden the Backup Script

The script `work-backup.sh` was found to be redacting `token:` lines with sed, but only after the initial commit had already pushed the live token. Fix:

```bash
# In work-backup.sh: add redaction BEFORE git add, not after
# And verify .gitignore ignores .env and config files
echo ".env" >> .gitignore
```

## Key Time Measurements

- Detection to revocation: user action (immediate via BotFather)
- git-filter-repo purge: ~30 seconds (small repo, single secret)
- Force push: ~10 seconds
- Garbage collection: ~15 seconds
- Full incident: ~5 minutes

## What Went Wrong (Root Causes)

1. **The backup script copied config files directly** without redacting secrets first
2. **No `.gitignore`** protected the config directory from being tracked
3. **No pre-commit hooks** to catch credential patterns
4. **The repo was pushed to GitHub** before the token was redacted

## Checklist for This Incident

- [x] Token revoked at BotFather
- [x] Git history purged with git-filter-repo
- [x] Clean history pushed to GitHub (force push)
- [x] Local repo synced and garbage-collected
- [x] Verification: zero token instances remain in git history
- [ ] Backup script updated to redact before commit
- [ ] `.gitignore` updated
