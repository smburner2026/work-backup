---
name: git-secret-remediation
description: "Remediate leaked secrets/credentials committed to git history — detect, revoke, purge with git-filter-repo, verify, and harden backup/automation to prevent recurrence."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Git, Security, Secrets, Credentials, git-filter-repo, Incident-Response]
    related_skills: [github-repo-management, github-auth]
---

# Git Secret Remediation

See `references/telegram-token-leak-incident.md` for a complete worked example of a Telegram bot token leak — from GitHub alert through revocation, git-filter-repo purge, force-push, garbage collection, and backup-script hardening.

When a secret (API token, password, SSH key, bot token) has been committed to a git repo — whether the repo is local-only or pushed to GitHub/GitLab — this procedure removes it from all history, verifies the purge, and prevents recurrence.

## When to Use

- GitHub sends a secret-scanning alert (email or push rejection)
- Someone reports a leaked token on a public repo
- You discover a `.env`, `config.yaml` with credentials, or hardcoded secret in git history during an audit
- A `git grep` finds a known credential pattern in the repo

## Danger: Know Which Phase You're In

The distinction between **Before push** and **After push** is the single most important thing to get right:

### BEFORE PUSH (secret never left your machine)

If the secret is only in local commits that haven't been pushed to any remote:

```bash
# If it's the very last commit:
git reset --soft HEAD~1
# Unstage the secret file, then recommit without it

# If it's deeper in history — use git-filter-repo (same procedure as pushed case,
# but no force-push needed, no collaborators to warn, no GitHub cache concerns)
# Proceed with the purging procedure below — just skip step 3 (push).
```

### AFTER PUSH (secret made it to a remote)

**The clock is ticking.** Once a secret is on GitHub/GitLab, treat it as compromised:
1. **Revoke the secret FIRST** — before anything else. Any remediation that doesn't start with revocation leaves a window where the live secret can be exploited.
2. Then purge from git history.
3. Then force-push.
4. Then verify.

Even after force-pushing, GitHub may cache the old commits in pull request merge commits, fork networks, or action artifacts. If the repo is public, the secret may have been scraped already. **Revocation is the only real fix.** Git history purge is damage control.

---

## The Full Procedure

### Step 1: Detect and Identify

```bash
# Find what was committed — search the entire repo (working tree + history)
cd /path/to/repo

# Search for known credential patterns
git grep -n -I -E '[0-9]{8,10}:[A-Za-z0-9_-]{35,}' -- .    # Telegram bot tokens
git grep -n -I -E 'sk-[A-Za-z0-9]{20,}' -- .               # OpenAI keys
git grep -n -I -E 'ghp_[A-Za-z0-9]{36,}' -- .              # GitHub PATs (old format)
git grep -n -I -E 'github_pat_[A-Za-z0-9]{36,}' -- .       # GitHub PATs (new format)
git grep -n -I -E 'AKIA[0-9A-Z]{16}' -- .                  # AWS access keys
git grep -n -I -E '-----BEGIN (RSA |EC )?PRIVATE KEY-----' -- .  # SSH keys

# Also check all history
git log --all -p -- . | grep -n -E '(token|secret|password|key).*[:=]' | head -30
```

**Identify the exact commit** that introduced the secret:

```bash
git log --all -p --reverse -- . | grep -B5 -A5 'THE_SECRET_VALUE'
# Or use git blame on the file
git log --all --oneline -- <file-containing-secret>
```

If GitHub sent the alert, it often tells you which commit. Use:

```bash
git show <commit-hash> --stat
```

**Check what else is exposed in that commit** — the user may have committed more than just the token:

```bash
git show <commit-hash> --name-only
git show <commit-hash>
```

### Step 2: Revoke the Secret (CRITICAL — DO THIS FIRST)

Before touching git, revoke the credential at its source:

| Secret Type | Revocation Method |
|---|---|
| Telegram Bot Token | @BotFather → /mybots → select bot → Bot Settings → Revoke token |
| GitHub PAT | github.com → Settings → Developer settings → Personal access tokens → Delete |
| OpenAI/Anthropic/Mistral API key | Provider dashboard → Keys → Revoke |
| Discord Bot Token | Discord Developer Portal → Application → Bot → Reset Token |
| AWS Access Key | AWS Console → IAM → Users → Security credentials → Make inactive → Delete |
| Slack Token | api.slack.com → Apps → Your App → OAuth & Permissions → Reinstall |
| Generic password | Change password at the service + rotate any dependent credentials |

**Do not skip this step.** The git history purge that follows protects future exposure. Revocation stops active exploitation.

### Step 3: Prepare git-filter-repo

`git-filter-repo` is the recommended tool. It rewrites history by applying text replacements across all commits:

```bash
# Install if not present
which git-filter-repo 2>/dev/null || pip install git-filter-repo

# Confirm the repo is clean — no uncommitted changes
cd /path/to/repo
git status --short
# If anything shows, commit or stash it first

# Save the remote URL (you'll need it later)
REMOTE_URL=$(git remote get-url origin)
echo "Remote: $REMOTE_URL"
```

**Create the replace-text file.** The format is:

```
literal:EXACT_STRING_TO_REPLACE==>REPLACEMENT_TEXT
```

Always replace with `REDACTED` or `***REMOVED***` — NOT with an empty string (which could break the file structure):

```bash
# One secret per line
cat > /tmp/secret-replace.txt << 'EOF'
literal:actual-token-value==>REDACTED
EOF

# For Telegram bot tokens (which contain ":" that confuses literal: parsing):
# Write just the token itself on a line
printf 'actual-token-value==>REDACTED\n' > /tmp/secret-replace.txt
```

**CRITICAL — Format Pitfall:** The `==>` delimiter is exact. If the token contains characters that break the format (colons, semicolons, spaces), use a simpler approach:

```bash
# With a single literal replacement file per token
printf '%s==>REDACTED\n' '8910979795:AAG5-...' > /tmp/secret-replace.txt

# Verify the file bytes are correct
od -c /tmp/secret-replace.txt | head -3
```

### Step 4: Clone Fresh and Purge

Always operate on a **fresh clone** — never run `git-filter-repo` directly on the original working tree:

```bash
cd /tmp
git clone /path/to/original-repo /tmp/purge-work
cd /tmp/purge-work

git filter-repo --replace-text /tmp/secret-replace.txt --force
```

**What this does:** Rewrites every commit in every branch, replacing all instances of the secret text with `REDACTED`. The `--force` flag is needed because the target isn't a bare repo.

**Verify the purge:**

```bash
# Search for the original secret — should return 0 matches
git log --all -p | grep -c 'THE_ORIGINAL_SECRET'

# Verify replacement worked
git log --all -p | grep 'REDACTED' | head -5

# Check no other token lines look suspicious
git log --all -p | grep 'token:' | sort -u

# Check the current HEAD config.yaml or .env
git show HEAD:.path/to/config.yaml 2>/dev/null | grep 'token:'
```

### Step 5: Force-Push the Cleaned History

```bash
# Add the remote
cd /tmp/purge-work
git remote add origin "$REMOTE_URL"

# Force-push all branches
git push origin --force --all

# Force-push tags (if any)
git push origin --force --tags
```

**CRITICAL — GitHub Collaboration:** If others have the repo cloned:
- Force-push rewrites history — anyone who has pulled the old commits will have divergence
- Notify collaborators to `git fetch origin && git reset --hard origin/main`
- If there are open PRs, GitHub may show the old commits — close and reopen or create fresh branches

### Step 6: Reset the Local Working Tree

After forcing the remote, sync the original local repo:

```bash
cd /path/to/original-repo
git fetch /tmp/purge-work main 2>&1
git reset --hard FETCH_HEAD

# Verify local copy is clean
git log --all -p | grep -c 'THE_ORIGINAL_SECRET'
```

### Step 7: Expunge Traces — Garbage Collection

The secret may still exist in git's object storage (reflog, pack files). Force immediate garbage collection:

```bash
# Expire all reflog entries immediately
git reflog expire --expire=now --all

# Prune all unreachable objects aggressively
git gc --prune=now --aggressive 2>&1

# Remove the backup refs that git-filter-repo creates
rm -rf .git/refs/original/

# Verify one more time
git log --all -p | grep -c 'THE_ORIGINAL_SECRET'
```

### Step 8: Harden Against Recurrence

The most common vector for a secret leak is an automation script that copies config files into a git-tracked directory, or a `.env` file that gets `git add -A`'d:

**Check 1 — Is the secret file in `.gitignore`?**

```bash
# Check if the source config files are tracked
git ls-files .env .env.* config.yaml 2>/dev/null
# If tracked and they contain secrets, they need to be untracked AND removed from history

# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "config.yaml" >> .gitignore  # Only if config contains secrets
```

**Check 2 — Does the backup script redact before pushing?**

If a script (cron job, rsync, etc.) copies config files into the repo, it should redact secrets before committing:

```bash
# Example: In the backup script, before git add, redact known secret fields
sed -i 's/token:.*/token: REDACTED/' .hermes-config/config.yaml
sed -i 's/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=REDACTED/' .env
# Or use a .env.example that's git-tracked instead of the actual .env
```

**Check 3 — Separate secrets from the repo:**

Best practice: Keep secrets OUT of the git-tracked tree entirely. Use environment variables or a secrets manager:

- The actual `.env` lives outside the repo workspace
- Config files are templated (`.env.example`, `config.template.yaml`) with placeholder values
- A deploy script injects real secrets from environment variables or a secure store
- Pre-commit hooks (e.g., `pre-commit` framework) scan for credential patterns and block the commit

**Check 4 — Enable GitHub secret scanning:**

For GitHub repos, secret scanning is free for public repos and available for private repos with GHAS. Enable it:

```bash
# Via API
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{"security_and_analysis": {"secret_scanning": {"status": "enabled"}}}'
```

### Step 9: Post-Mortem Checklist

- [ ] Secret revoked at source
- [ ] New credential created and deployed
- [ ] All config files/automation updated with new credential
- [ ] Old secret purged from git history (verified with grep)
- [ ] Force-pushed to all remotes
- [ ] Collaborators notified of history rewrite
- [ ] Backup/automation scripts hardened to redact secrets before commit
- [ ] `.gitignore` updated
- [ ] Pre-commit secret scanner installed (if appropriate)
- [ ] GitHub secret scanning enabled for the repo

---

## Pitfalls

### git-filter-repo vs BFG vs Filter-Branch

| Tool | Recommendation | Reason |
|---|---|---|
| `git-filter-repo` | ✅ **Use this** | Fast, Python scriptable, `--replace-text` with literal mode, safe fresh-clone workflow |
| `bfg` | ⚠️ Avoid | No longer actively maintained, requires Java, less precise replacement control |
| `git filter-branch` | ❌ Avoid | Deprecated by git, extremely slow on large repos, easy to get wrong |

### git-filter-repo Format Pitfalls

The `--replace-text` file has a specific format that can be unintuitive:

- `literal:VALUE==>REPLACEMENT` — replaces exact VALUE with REPLACEMENT. The `literal:` prefix is literal text.
- `VALUE==>REPLACEMENT` — same as `literal:` by default
- `regex:PATTERN==>REPLACEMENT` — regex replacement

**CRITICAL:** If the token contains a colon (`:`), the `literal:` prefix may not work as expected because the parser sees the token's colon as the end of `literal:`. In that case:

```bash
# Write without any prefix — just the raw replacement expression
printf '%s==>REDACTED\n' 'token-with-colons:and-stuff' > /tmp/replace.txt
```

**Always verify the file with `od -c` before running git-filter-repo:**

```bash
od -c /tmp/secret-replace.txt | head -5
# Should show: l i t e r a l : T O K E N = = > R E D A C T E D
# Or if no literal prefix:    T O K E N = = > R E D A C T E D
```

### Token in Current Working Copy Still Live

After purging history, the token may still be in the **current working tree** (HEAD). If the current config.yaml still has the real token:

1. The current file still has the secret — git-filter-repo only rewrites history, not the working tree
2. Edit the file to use REDACTED or the new token
3. Then commit the fix

### GitHub Commit Cache

After force-pushing, GitHub may still cache the old commit data in:
- **Pull request merge commits** — if the secret was merged via a PR, the merge commit may still contain it. Close and reopen the PR, or create a fresh PR.
- **Actions artifacts** — if CI runs built artifacts from the compromised commit, those artifacts may still contain the secret. Delete them from the Actions UI.
- **Fork networks** — all forks of a repo before the force-push will still have the secret. Notify fork maintainers.
- **Commit search** — GitHub's commit search may index the old commit SHA. This is cleared when GitHub re-indexes.

### Pre-Commit Hook Blocking

If the repo has pre-commit hooks that check for credentials (or a general `pre-commit` framework), git-filter-repo's rewrite may trigger them on the fresh clone. Add `--force` to bypass.

### Multiple Secrets in One Incident

If you're purging one secret, check if the same commit or file pattern exposed other secrets. The user may have committed a whole config file. Check the diff of the offending commit carefully:

```bash
git show <commit-hash> --name-only
git show <commit-hash>
```

---

## Quick Reference — Minimal Workflow

```bash
# 1. REVOKE at source FIRST
# 2. Install tool
pip install git-filter-repo

# 3. Clone fresh
cd /tmp && git clone /path/to/repo cleanup-tmp && cd cleanup-tmp

# 4. Purge
printf 'THE_SECRET==>REDACTED\n' > /tmp/replace.txt
git filter-repo --replace-text /tmp/replace.txt --force

# 5. Verify
git log --all -p | grep -c 'THE_SECRET'    # → 0

# 6. Push
git remote add origin $(cd /path/to/repo && git remote get-url origin)
git push origin --force --all --tags

# 7. Reset local
cd /path/to/repo && git fetch cleanup-tmp main && git reset --hard FETCH_HEAD
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# 8. Fix the backup script to redact before commit
```
