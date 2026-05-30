# /root/ Home Directory Audit & Cleanup Pattern

## When to Use

The user says "clean up /root/" or "reorganize the home directory" — loose scripts, JSON reports, tarballs, and AI agent config dirs have accumulated.

## Workflow

### 1. Audit — catalog everything in /root/

```bash
echo "=== FILES ===" && find /root -maxdepth 1 -type f | sort
echo "" && echo "=== DIRS ===" && ls -d /root/*/ 2>/dev/null | sort
echo "" && echo "=== AI AGENT DIRS ===" && ls -la /root/ | grep "^d" | grep "^\."
```

### 2. Categorize each file

| Category | Where it goes |
|----------|---------------|
| DABT analysis scripts (.py) | `/root/work/dabt/scripts/` |
| DABT reports (.json, .md, .txt) | `/root/work/dabt/reports/` |
| Other project scripts | `/root/work/scripts/` or `/root/work/archive/` |
| Old tarballs (.tgz, .tar.gz) | Delete (transient transfer artifacts) |
| Shell configs (.bashrc, .profile, .zshrc) | Stay in /root/ |
| System dirs (.config/, .ssh/, .cache/, .local/) | Stay in /root/ |
| Hermes dir (.hermes/) | Stay in /root/ (never touch) |
| Work dir (work/) | Stay in /root/ (never touch) |

### 3. Move files before deleting

Always prepare subdirectories first:

```bash
mkdir -p /root/work/dabt/scripts /root/work/dabt/reports
```

Then move in bulk by pattern:

```bash
mv /root/analyze_*.py /root/work/dabt/scripts/
mv /root/build_*.py /root/work/dabt/scripts/
mv /root/extract_*.py /root/work/dabt/scripts/
mv /root/dabt_*.json /root/work/dabt/reports/
mv /root/dabt_*.md /root/work/dabt/reports/
# etc.
```

Residual check — after bulk moves, check for stragglers:

```bash
ls /root/*.py /root/*.json /root/*.md /root/*.sh /root/*.tgz /root/*.tar.gz 2>/dev/null || echo "None"
```

### 4. Nuke AI agent config dirs (with explicit approval)

Canonical list of known agent config dirs. When user says "go ahead":

```bash
rm -rf /root/.claude /root/.codebuddy /root/.codeium /root/.agents /root/.augment \
  /root/.forge /root/.factory /root/.codemaker /root/.codestudio /root/.commandcode \
  /root/.continue /root/.iflow /root/.kilocode /root/.kiro /root/.mux \
  /root/.openhands /root/.pochi /root/.qoder /root/.qwen /root/.roo \
  /root/.snowflake /root/.tabnine /root/.trae /root/.trae-cn /root/.zencoder \
  /root/.codeartsdoer
```

After deletion, run a quick verification:

```bash
echo "Remaining dot-dirs:" && ls -la /root/ | grep "^d" | grep "^\."
```

### 5. Verify end state

Clean `/root/` should contain ONLY:

| Type | What stays |
|------|------------|
| Shell configs | `.bashrc`, `.profile`, `.zshrc`, `.bash_history`, `.lesshst` |
| Auth/Security | `.ssh/`, `.gnupg/`, `.gitconfig`, `.git-credentials` |
| System | `.config/`, `.cache/`, `.local/`, `.npm/`, `.pki/` |
| Hermes | `.hermes/` |
| Work | `work/` |
| Platform-required | `snap/`, `substack_exports/` (or similar user-approved) |
| Misc | `.wget-hsts`, `.cloud-locale-test.skip` (harmless) |

No loose `.py`, `.json`, `.md`, `.sh`, `.tgz`, `.tar.gz` files.
No AI agent config dot-dirs.

### 6. Sync after cleanup

After cleaning the VPS, sync the cleaned state to local:

```bash
# From WSL:
sudo ~/.hermes/bin/hms pull
```

This ensures the local machine doesn't preserve the stale state.

## Pitfalls

- **Do NOT delete system dirs** — `.local/`, `.config/`, `.ssh/`, `.gnupg/`, `.npm/`, `.pki/` are all needed
- **Do NOT touch `.hermes/` or `work/`** — these are the agent and workspace
- **Check for subdirs like `substack_exports/`** — these are user-approved project dirs, not trash
- **DABT scripts go in scripts/ not archive/** — scripts are still runnable, not dead
- **After moving scripts, verify they still run from their new location** — relative path assumptions may break
- **Sync after cleanup** — stale local state will restore the mess on the next push if you forget
