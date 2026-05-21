---
name: github-auth
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login."
version: 1.4.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Authentication, Git, gh-cli, SSH, Setup]
    related_skills: [github-pr-workflow, github-code-review, github-issues, github-repo-management]
---

# GitHub Authentication Setup

This skill sets up authentication so the agent can work with GitHub repositories, PRs, issues, and CI. It covers two paths:

- **`git` (always available)** — uses HTTPS personal access tokens or SSH keys
- **`gh` CLI (if installed)** — richer GitHub API access with a simpler auth flow

## Detection Flow

When a user asks you to work with GitHub, run this check first:

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"

# Check if already authenticated
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated → you're good, use `gh` for everything
2. If `gh` is installed but not authenticated → use "gh auth" method below
3. If `gh` is not installed → use "git-only" method below (no sudo needed)

---

## Method 1: Git-Only Authentication (No gh, No sudo)

This works on any machine with `git` installed. No root access needed.

### Option A: HTTPS with Personal Access Token (Recommended)

This is the most portable method — works everywhere, no SSH config needed.

**Step 1: Create a personal access token**

Tell the user to go to: **https://github.com/settings/tokens**

- Click "Generate new token (classic)"
- Give it a name like "hermes-agent"
- Select scopes:
  - `repo` (full repository access — read, write, push, PRs)
  - `workflow` (trigger and manage GitHub Actions)
  - `read:org` (required for `gh auth login --with-token` — the gh CLI validates this scope even for personal repos; also needed for org repo access)
- **Expiration:**
  - **No expiration** — for backup tokens on a single machine; lowest maintenance
  - **90 days** — reasonable compromise if you want some rotation without constant churn
  - **30 days** — stricter; acceptable if you have a way to be reminded
  - Fine-grained PATs cannot have no-expiration; use classic PAT for permanent setups
- Copy the token — it won't be shown again

**Step 2: Configure git to store the token**

```bash
# Set up the credential helper to cache credentials
# "store" saves to ~/.git-credentials in plaintext (simple, persistent)
git config --global credential.helper store

# Now do a test operation that triggers auth — git will prompt for credentials
# Username: <their-github-username>
# Password: <paste the personal access token, NOT their GitHub password>
git ls-remote https://github.com/<their-username>/<any-repo>.git
```

After entering credentials once, they're saved and reused for all future operations.

**Alternative: cache helper (credentials expire from memory)**

```bash
# Cache in memory for 8 hours (28800 seconds) instead of saving to disk
git config --global credential.helper 'cache --timeout=28800'
```

**Alternative: set the token directly in the remote URL (per-repo)**

```bash
# Embed token in the remote URL (avoids credential prompts entirely)
git remote set-url origin https://<username>:<token>@github.com/<owner>/<repo>.git
```

**Step 3: Configure git identity**

```bash
# Required for commits — set name and email
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

**Step 4: Verify**

```bash
# Test push access (this should work without any prompts now)
git ls-remote https://github.com/<their-username>/<any-repo>.git

# Verify identity
git config --global user.name
git config --global user.email
```

### Option B: SSH Key Authentication

Good for users who prefer SSH or already have keys set up.

**Step 1: Check for existing SSH keys**

```bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"
```

**Step 2: Generate a key if needed**

```bash
# Generate an ed25519 key (modern, secure, fast)
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Display the public key for them to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

Tell the user to add the public key at: **https://github.com/settings/keys**
- Click "New SSH key"
- Paste the public key content
- Give it a title like "hermes-agent-<machine-name>"

**Step 3: Test the connection**

```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

**Step 4: Configure git to use SSH for GitHub**

```bash
# Rewrite HTTPS GitHub URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

**Step 5: Configure git identity**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

---

## Method 2: gh CLI Authentication

If `gh` is installed, it handles both API access and git credentials in one step.

### Installing gh CLI

If `gh` is not installed and you have sudo, install it:

**Linux (Debian/Ubuntu):**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
  https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update -qq && sudo apt install -y -qq gh
```

**macOS (Homebrew):** `brew install gh`

**Windows (winget):** `winget install GitHub.cli`

**No sudo?** Download the `.deb`/`.rpm` from https://github.com/cli/cli/releases and extract to a user-local bin directory, or use the git-only method above.

### Interactive Browser Login (Desktop)

```bash
gh auth login
# Select: GitHub.com
# Select: HTTPS
# Authenticate via browser
```

### Token-Based Login (Headless / SSH Servers)

```bash
# IMPORTANT: Ensure GH_TOKEN and GITHUB_TOKEN are NOT set first.
# If they are, gh ignores --with-token and silently uses the env var.
unset GH_TOKEN GITHUB_TOKEN

echo "<THEIR_TOKEN>" | gh auth login --with-token

# Set up git credentials through gh
gh auth setup-git
```

**Pitfall — GH_TOKEN env var conflict:** If `GH_TOKEN` or `GITHUB_TOKEN` is set in the environment (e.g., from sourcing a detection script, or from a previous `export` in the session), `gh auth login --with-token` appears to succeed but actually ignores the piped token and uses the env var instead. The resulting auth state may not match expectations. **Always `unset GH_TOKEN GITHUB_TOKEN` before running `gh auth login`** if you've been extracting tokens earlier in the session. The detection flow and `gh-env.sh` script below both export `GITHUB_TOKEN` — running `gh auth login` after sourcing them will hit this silently.

### Verify

```bash
# Unset env vars first so you're testing the stored config, not a stale env
unset GH_TOKEN GITHUB_TOKEN && gh auth status
```

---

## Using the GitHub API Without gh

When `gh` is not available, you can still access the full GitHub API using `curl` with a personal access token. This is how the other GitHub skills implement their fallbacks.

### Setting the Token for API Calls

```bash
# Option 1: Export as env var (preferred — keeps it out of commands)
export GITHUB_TOKEN="<token>"

# Then use in curl calls:
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### Extracting the Token from Git Credentials

If git credentials are already configured (via credential.helper store), the token can be extracted:

```bash
# Read from git credential store
grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
```

### Detect Token Type (Classic vs Fine-Grained)

GitHub has two token formats. They behave differently and the difference matters:

| Prefix | Type | Can create repos? | Scope model |
|--------|------|-------------------|-------------|
| `ghp_` | Classic PAT | Yes (with `repo` scope) | Broad scopes (`repo`, `workflow`, etc.) |
| `github_pat_` | Fine-grained PAT | Only if granted per-repo creation permission | Per-repo permissions, no global create |

**Quick check:**
```bash
TOKEN=$(grep 'github.com' ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
case "$TOKEN" in
  ghp_*)          echo "Classic PAT — full capabilities" ;;
  github_pat_*)   echo "Fine-grained PAT — may be restricted" ;;
  *)             echo "Unknown token type" ;;
esac
```

**Fine-grained PAT limitations:** Cannot create new repos (`gh repo create`, `POST /user/repos`) unless the token was explicitly granted the "Create repositories" permission at creation time. If you get `Resource not accessible by personal access token` when creating a repo, the user needs a classic PAT with `repo` scope, or you can ask them to create the repo on github.com manually and push to it.

### Helper: Detect Auth Method

Use this pattern at the start of any GitHub workflow:

```bash
# Try gh first, fall back to git + curl
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
elif [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
  export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
  echo "AUTH_METHOD=curl"
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need to set up authentication first"
fi
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | GitHub disabled password auth. Use a personal access token as the password, or switch to SSH |
| `remote: Permission to X denied` | Token may lack `repo` scope — regenerate with correct scopes |
| `fatal: Authentication failed` | Cached credentials may be stale — run `git credential reject` then re-authenticate |
| `gh auth login --with-token` silently does nothing | `GH_TOKEN` or `GITHUB_TOKEN` env var is set. `gh` prioritises the env var over `--with-token`. Run `unset GH_TOKEN GITHUB_TOKEN` first |
| `gh auth login --with-token` fails: `error validating token: missing required scope 'read:org'` | The gh CLI requires `read:org` scope for token-based login even if you never touch org repos. Regenerate the classic PAT with `read:org` ticked (it's under the `admin:org` scope group). Workaround without regenerating: use `GH_TOKEN` env var — `gh` skips scope validation when the token comes from the environment. |
| Credentials not persisting | Check `git config --global credential.helper` — must be `store` or `cache` |
| Multiple GitHub accounts | Use SSH with different keys per host alias in `~/.ssh/config`, or per-repo credential URLs |
| `Resource not accessible by personal access token` on `gh repo create` | Token is fine-grained PAT (`github_pat_...`). Fine-grained PATs cannot create repos unless explicitly granted that permission. Use a classic PAT (`ghp_...`) with `repo` scope, or create the repo on github.com manually and push |
| `git credential approve` doesn't update credential store | `git credential approve` can fail silently (non-zero exit but no error message). The credential file is at `~/.git-credentials` — write it directly: `echo 'https://user:token@github.com' > ~/.git-credentials` and set proper perms: `chmod 600 ~/.git-credentials`. Format is a single line per host. |
| Token replacement in credential store not taking effect | Old credentials linger. Use `git credential reject` first (as above), then verify the file content with `cat ~/.git-credentials` rather than trusting `git credential approve`'s exit code. |
| `gh repo create --source=. --push` fails with "no commits found" | `--push` tries to push the local branch to the new remote, but fails if the local branch has no commits yet. You need at least `git commit` before running this. Run `git add -A && git commit -m "initial"` first, or omit `--push` and push manually after the repo is created. |
| `gh auth setup-git` breaks git push after store-based auth | `gh auth setup-git` installs a URL-specific credential helper (`credential.https://github.com.helper`) that takes priority over the global store helper. If gh is missing `read:org`, this helper causes all git pus pull operations to fail with "Password authentication not supported". Fix: `git config --global --unset-all credential.https://github.com.helper && git config --global --unset-all credential.https://gist.github.com.helper`. Verify with `git config --list --show-origin | grep credential`. |
| `credential.helper=store` has correct token in `~/.git-credentials` but git push still gets 403 / "Password authentication not supported" | Known with some git versions (2.43 observed). The embedded token URL is a reliable workaround: `git remote set-url origin https://USER:TOKEN@github.com/OWNER/REPO.git`. Bypasses credential helpers entirely. To diagnose, compare `git credential fill` output against the actual file content: `python3 -c "import re; open('/root/.git-credentials').read()"` vs `echo 'url=https://github.com/...' \| git credential fill`. |
| Cannot create repo (token lacks `read:org` or fine-grained PAT restriction) | Use the GitHub API via curl instead of gh: `curl -s -X POST -H "Authorization: token $TOKEN" https://api.github.com/user/repos -d '{"name":"REPO","description":"DESC","private":false}'`. Then `git remote add origin URL && git push -u origin main`. |
