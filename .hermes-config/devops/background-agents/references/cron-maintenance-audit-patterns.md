# Cron Maintenance: Audit Patterns & Pitfalls

## SOUL.md Audit Pattern

When auditing SOUL.md files in a recurring maintenance job:

| File Type | Has YAML Frontmatter? | `---` Role |
|-----------|----------------------|-----------|
| Master SOUL (`~/.hermes/SOUL.md`) | Yes | Frontmatter delimiters |
| Profile SOULs (`profiles/*/SOUL.md`) | **No** | Markdown section separators |
| Skill SKILL.md | Yes | Frontmatter delimiters |

**Correct detection logic:**
```python
parts = content.split('---', 2)
if len(parts) >= 3:
    try:
        yaml.safe_load(parts[1])
        # Valid YAML frontmatter exists
    except yaml.YAMLError:
        # NOT a frontmatter file — likely a profile SOUL.md with --- section separators
```

Profile SOUL.md files at `profiles/euphy/SOUL.md` and `profiles/mike/SOUL.md` have `---` at lines 31, 43, 51 used as section dividers inside pure markdown. They are **not** parseable as YAML and that is correct behavior.

## Cron Job Storage Layout

```
~/.hermes/cron/
├── jobs.json              # All job definitions (JSON array of job objects)
└── output/                # Job run output artifacts
```

`jobs.json` contains schedule expressions (`schedule.expr`), last_run_at, next_run_at, last_status, last_error fields.

On this system, `crontab -l` returns "no crontab for root" — Hermes cron is managed through its internal system, not system crontab.

## Memory is Unavailable in Cron Environments

The `memory()` tool responds with `"Memory is not available. It may be disabled in config or this environment."` when called from a cron job session.

**Impact:** Cron jobs cannot save findings to persistent memory. All state must be file-based.

**Workaround:** Write findings to JSON files under the job's project directory or to `~/.hermes/cron/`. The next session (user-driven) can read those files and commit to memory.

## Skills Directory Structure

Skills are stored as: `~/.hermes/skills/<category>/<skill_name>/SKILL.md`

But if created without a `category` parameter in `skill_manage(action='create')`, they go directly under `~/.hermes/skills/<skill_name>/` (no category subdirectory). Example: `swingcatcher` skill is at `~/.hermes/skills/swingcatcher/SKILL.md` despite having `category: trading` in its frontmatter.

## Broken Symlinks: Expected vs Concerning

All symlinks under `~/.hermes/` are categorized:

| Location | Count | Severity | Notes |
|----------|-------|----------|-------|
| `hermes-agent/*/node_modules/.bin/` | ~58 | ⚠️ Normal | NPM workspace bin stubs — harmless, rebuild on `npm install` |
| `hermes-agent/venv/bin/python*` | 3 | ⚠️ Stale | Points to former dev's home (`/home/vthen/...`). Active Hermes runs from `/usr/local/lib/hermes-agent/venv/` |
| `~/.hermes/node/bin/*` | 7 | ⚠️ Stale | Node install bin wrappers — harmless if using system node |
| `cache/fastembed/models/*/blobs/` | 5 | ⚠️ Incomplete | Fastembed model cache — partial download, regenerate on use |
| `lsp/node_modules/.bin/*` | 6 | ⚠️ Stale | LSP binaries — rebuild on LSP setup |

None of these affect operational Hermes since the active venv is at `/usr/local/lib/hermes-agent/venv/`.

## Hermes Version

Current: v0.14.0 (2026.5.16), 26 commits behind. `hermes update` available.
