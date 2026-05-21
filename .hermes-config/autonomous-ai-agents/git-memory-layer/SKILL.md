---
name: git-memory-layer
description: "Use a git repo as persistent agent working memory — pull before work, commit+push after output. Structured commit messages as queryable cross-session journal. Covers SSH deploy key setup, identity/activity boundary, and concurrent-session safety."
version: 1.1
author: Randoooos + Hermes
---

# Git Memory Layer

Use a git repository as persistent shared state for agent work across sessions. The commit history becomes a deterministic, searchable record of what was done and why — immune to context compression and model rolls.

## When to load

- User asks to set up or use git repo as persistent agent memory
- User wants an auditable trail of agent work across sessions
- Working in a project repo where each task should leave a trace
- Cross-session context or multi-surface (phone, laptop, SSH) usage of the same repo

## Boundary: what goes in, what stays out

**Commits get:** Artifacts, outputs, decisions, scripts, configuration, docs — anything you'd version-track or show someone else.

**Commits do NOT get:** Chat dialogue, back-and-forth clarification, personality data, memory files (MEMORY.md/USER.md), infra secrets, API keys, session metadata. Conversations live in the session store, not in git history.

This aligns with the soul-compression identity/activity principle: git stores *activity* (what was produced); souls store *identity* (who the user is).

## Workflow

```
# Before material work:
git pull --ff-only

# After material output:
git add -A && git commit -m "cat: short description" && git push
```

## Commit convention

| cat | When |
|---|---|
| `work` | New feature, output, analysis, pipeline |
| `fix` | Bug correction |
| `docs` | Notes, commentary, markdown |
| `chore` | Config, tooling, scripts |

Single-line messages only. No ticket numbers, no signed-off-by, no multiline bodies. Just category + what changed.

## When to commit

Only on material output. Do NOT commit for:
- Config reads or inspection that changed nothing
- Casual conversation or clarification
- Failed attempts with no useful artifact
- Pulling pre-existing state

## User preferences

Low-ceremony, iterative workflow. Start minimal and tweak. No formalism. Token efficiency matters — keep commit messages short and the pipeline automatic.

## Security & Setup

### SSH deploy key (preferred — never expose a PAT)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/github-<repo> -N "" -C "hermes-agent-<host>"
cat ~/.ssh/github-<repo>.pub
```

Add public key to GitHub: repo → Settings → Deploy keys → Add deploy key (✅ write access).

Configure SSH:

```bash
cat >> ~/.ssh/config << 'EOF'
Host github.com
    HostName github.com
    IdentityFile ~/.ssh/github-<repo>
EOF
```

Switch remote from HTTPS (with embedded PAT) to SSH:

```bash
git remote set-url origin git@github.com:<user>/<repo>.git
```

### Gitignore (set up early)

```bash
cat >> .gitignore << 'EOF'
*.log
.env
*.key
__pycache__/
EOF
```

### What never goes in

- PATs, API keys, passwords — in `.env` or credential helpers, never in git config or committed files
- Session transcripts — local to Hermes session store (`hermes_state.db`)
- Hermes memory files (MEMORY.md, USER.md) — infra config, not project artifacts

## Extended finalization pattern (after major work)

Skills, cron jobs, and memory files are part of the artifact surface but live outside the work directory. After a major work block, use the `references/work-finalization-pattern.md` checklist to:

1. Commit material work to the repo
2. Snapshot relevant skills into the work directory for backup
3. Document cron job definitions as files
4. Compress memory files (MEMORY.md, USER.md) if near capacity
5. Push everything

See the reference file for the full checklist and per-project snapshot locations.

## Pitfalls

- `--ff-only` prevents messy merge commits. If it fails, something is out of sync — investigate rather than forcing.
- Commit before switching tasks to avoid mixed-state commits.
- If a `git push` fails (credential issues, network), commit is already local — push later.
- Credential setup (PAT in URL, SSH key) is a prerequisite, not part of this workflow.
- **Concurrent push conflicts.** Two sessions pushing simultaneously → rejected push. Mitigation: sequential discipline, or `git pull --rebase && git push` on rejection. True concurrency needs feature branches per session.
- **Oversized files.** Large PDFs or datasets bloat history and slow pushes. Git LFS or keep them out of the repo entirely (reference by path).
- **.gitignore neglect.** Temp files, venv, __pycache__ produce meaningless diffs if not excluded. Set gitignore before first real commit.
- **Committing session dialogue.** The most common mistake — chat transcript does not belong in the repo. See Boundary section above.
