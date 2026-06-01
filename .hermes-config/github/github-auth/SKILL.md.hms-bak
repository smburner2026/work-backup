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
1. **Try the simplest thing first** — if the user mentions a specific repo, try a read-only test before any auth setup. If the repo is public, no auth needed:
   ```bash
   git ls-remote https://github.com/<owner>/<repo>.git 2>&1
   ```
   If it returns refs, the repo is accessible without auth. Skip straight to clone. Only proceed to auth setup if this fails.
2. If `gh auth status` shows authenticated → you're good, use `gh` for everything
3. If `gh` is installed but not authenticated → use "gh auth" method below
4. If `gh` is not installed → use "git-only" method below (no sudo needed)

### Pitfall — Skipping the public-repo check

The agent should always try the read-only test (`git ls-remote`) before initiating auth setup. The user may say "we need auth" when the repo is actually public, or you may assume auth is needed because the repo was previously private. A single `git ls-remote` costs almost nothing and can save the entire auth setup loop.

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

**Pitfall — Device code visibility in agent-mediated sessions:**
`gh auth login --web` uses the **device code flow**: it prints a one-time code (e.g. `92D2-4813`) to stdout and blocks until the user completes the flow in their browser. This is fine on a desktop terminal, but **when an agent runs this command, the code is buried in terminal output that the user may not see** — particularly if they're in a TUI (herm, tmux splits) or reading compressed agent responses. The command then blocks for up to 5+ minutes and times out silently.

**Rule of thumb for agents:**
- **Desktop terminal / user sees raw output** → device code flow is fine
- **Agent-mediated session (TUI, CLI relay, SSH relay)** → always use `--with-token` (PAT-based) or SSH key instead. If you must use device code, extract the code from the terminal output and present it prominently to the user in your response text; do not rely on them reading the raw stdout.

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

## Token Expiry Recovery (Diagnostic Flow)

When a previously-working backup or push cron fails with auth errors, the token may have expired. Use this diagnostic flow instead of jumping to re-setup.

### Phase 1 — Identify the Failure Mode

```bash
git push origin main 2>&1
```

**Common error signatures:**

| Error | Likely cause |
|-------|-------------|
| `fatal: Authentication failed` / `Password authentication not supported` | Token expired or credential config stale |
| `remote: Invalid username or token` | Token expired or URL has embedded old token |
| `fatal: 'origin' does not appear to be a git repository` | Remote origin missing — add it back |
| `fatal: could not read Username` | No credential helper and no token in URL |

### Phase 2 — Verify Token State

```bash
gh auth status 2>&1
git config --global --list | grep credential
git config --global --list | grep insteadOf
```

**If gh shows "Token is invalid":** token expired. Run `gh auth login` with a fresh PAT.

**If gh shows OK but git push still fails:** gh has a good token but git routes through a stale URL rewrite — go to Phase 3.

### Phase 3 — Clean Stale Git Config

**A. Stale `insteadOf` URL with embedded expired token**

If `git config --global` shows an entry like `[url "https://user:old_token@github.com/"]` with `insteadOf = https://github.com/`, every GitHub URL gets rewritten to include the dead token. gh auth login doesn't touch this.

Remove it:
```bash
# Read exact URL from config
grep -A2 'insteadOf' ~/.gitconfig
# Remove it:
git config --global --unset-all url.https://USER:OLD_TOKEN@github.com/.insteadof
# If that fails (special chars in URL), delete the [url "..."] block from ~/.gitconfig directly
git config --global --list | grep insteadOf   # verify gone
```

**B. gh auth setup-git credential helper conflict**

If you had `credential.helper store` globally, running `gh auth setup-git` adds a URL-scoped helper that takes priority. If gh's helper fails (e.g., missing read:org), git breaks:

```bash
git config --global --unset-all credential.https://github.com.helper
git config --global --unset-all credential.https://gist.github.com.helper
```

### Phase 4 — Repair Remote Config

```bash
git remote -v   # check what exists
git remote add origin https://github.com/OWNER/REPO.git
```

### Phase 5 — Handle Diverged History

If pushes failed for weeks, local and remote have diverged:

```bash
git log --oneline --all --decorate | head -10
git push --force-with-lease origin main
# or: git reset --soft origin/main && git commit -m "backup $(date +%Y-%m-%d)" && git push origin main
```

For personal backup repos, force-with-lease is acceptable. Never on shared repos.

### Phase 6 — Verify

```bash
git fetch origin
git rev-parse HEAD && git rev-parse origin/main   # should match
git push origin main 2>&1                         # should succeed
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | GitHub disabled password auth. Use a personal access token as the password, or switch to SSH |
| `remote: Permission to X denied` | Token may lack `repo` scope — regenerate with correct scopes |
| `fatal: Authentication failed` | Cached credentials stale — run `git credential reject` then re-authenticate. If persists, check for stale `insteadOf` URL (see Token Expiry Recovery Phase 3A) |
| `gh auth login --with-token` silently does nothing | `GH_TOKEN` or `GITHUB_TOKEN` env var is set. `gh` prioritises the env var. Run `unset GH_TOKEN GITHUB_TOKEN` first |
| `gh auth login --with-token` fails: `error validating token: missing required scope 'read:org'` | gh CLI requires `read:org` even for personal repos. Regenerate classic PAT with `read:org` ticked (under `admin:org` scope group). Workaround: use `GH_TOKEN` env var to skip scope validation |
| Credentials not persisting | `git config --global credential.helper` must be `store` or `cache` |
| Multiple GitHub accounts | SSH with different keys per host alias in `~/.ssh/config` |
| `Resource not accessible by personal access token` on `gh repo create` | Fine-grained PAT cannot create repos unless explicitly granted that permission. Use classic PAT with `repo` scope, or create repo on github.com manually and push |
| `git credential approve` doesn't update credential store | Can fail silently. Write directly: `echo 'https://user:token@github.com' > ~/.git-credentials && chmod 600 ~/.git-credentials` |
| Token replacement not taking effect | Use `git credential reject` then verify file content with `cat ~/.git-credentials` |
| `gh repo create --source=. --push` fails with "no commits found" | Need at least one commit before `--push`. Run `git add -A && git commit -m "initial"` first |
| `gh auth setup-git` breaks git push after store-based auth | Two causes: (1) URL-specific credential helper conflict — clear URL-scoped helpers (Phase 3B). (2) Stale `insteadOf` URL with expired embedded token — remove `[url]` block from `~/.gitconfig` (Phase 3A) |
| `credential.helper=store` has correct token but git push still gets 403 | Embedded token URL workaround: `git remote set-url origin https://USER:TOKEN@github.com/OWNER/REPO.git`. Bypasses credential helpers |
| Cannot create repo (token lacks read:org or fine-grained restriction) | Use curl + GitHub API: `curl -s -X POST -H "Authorization: token $TOKEN" https://api.github.com/user/repos -d '{"name":"REPO"}'`. Then `git remote add origin URL && git push -u origin main` |
