---
name: hermes-plugins
description: "Install, enable, update, and track community/third-party Hermes plugins — plugins not shipped with base Hermes."
version: 1.0.0
author: agent
tags: [hermes, plugins, community, devops]
---

# Hermes Plugins — Community Plugin Management

Covers the lifecycle of third-party Hermes plugins that don't ship with the base install. Bundled plugins (shipped via `hermes update`) are handled separately.

## How Hermes Plugin System Works

Each plugin is a directory under one of:
- `<repo>/plugins/<name>/` — bundled (shipped with Hermes)
- `~/.hermes/plugins/<name>/` — user-installed
- `./.hermes/plugins/<name>/` — project-local (opt-in via `HERMES_ENABLE_PROJECT_PLUGINS`)

Each directory must contain:

1. **`plugin.yaml`** — manifest declaring hooks, toolsets, and commands (the canonical manifest, always required)

2. **Python entry point** — either:
   - A top-level `__init__.py` with a `register(ctx)` function (traditional pattern) — **the loader currently REQUIRES this at the plugin root**
   - A Python subpackage (e.g. `plugin-name/plugin-name/`) referenced from `plugin.yaml` or `pyproject.toml` — the loader attempts to discover the `register(ctx)` entry point from the package metadata, but this currently fails with `No __init__.py` if no top-level `__init__.py` exists

   **Net**: always ensure a top-level `__init__.py` exists at `~/.hermes/plugins/<name>/__init__.py`. For repos that nest their package inside a subdirectory, create a thin re-export (see "Verify the Copy" below).

### `plugin.yaml` Structure

```yaml
name: my-plugin
version: "1.0.0"
description: "What it does"
author: "name"
license: MIT
homepage: "https://github.com/..."
hooks:          # Optional — lifecycle hooks the plugin registers
  - pre_llm_call
  - transform_llm_output
  - post_tool_call
toolsets:       # Optional — toolset names the plugin provides
  - my-toolset
commands:       # Optional — slash commands the plugin registers
  - my-command
```

### `register(ctx)` Function

The `__init__.py` must expose a top-level `register(ctx)` function that receives a `PluginContext` object with these methods:

```python
def register(ctx) -> None:
    # Register lifecycle hooks
    ctx.register_hook("pre_llm_call", my_pre_call_handler)
    ctx.register_hook("transform_llm_output", my_output_handler)
    ctx.register_hook("post_tool_call", my_post_tool_handler)

    # Register tools (appear in model's tool schema)
    ctx.register_tool(
        name="my_tool",
        toolset="my-toolset",
        schema={...},          # OpenAI function-calling schema
        handler=my_handler,    # Callable
        check_fn=my_check,     # Returns bool — tool availability gate
        description="...",
        emoji="🔧",
    )

    # Register slash commands
    ctx.register_command(
        "my-command",
        handler=my_command_handler,
        description="...",
        args_hint="...",
    )
```

## Installing a Community Plugin

### From a GitHub Repo

```bash
# 1. Clone the repo
cd /tmp
git clone https://github.com/user/repo.git --depth 1

# 2. Copy plugin files to ~/.hermes/plugins/<name>/
mkdir -p ~/.hermes/plugins/<name>/
cp repo/<plugin-dir>/*.py ~/.hermes/plugins/<name>/
cp repo/plugin.yaml ~/.hermes/plugins/<name>/

# 3. Enable via Hermes
hermes plugins enable <name>

# 4. Verify it's active
hermes plugins list | grep <name>
# → should show "enabled"

# 5. Clean up temp clone
rm -rf /tmp/repo
```

### Post-Install

- Plugin takes effect on **next session** (`/reset` or fresh `hermes` invocation).
- If the plugin registers a toolset, the tools appear automatically — no separate toolset enable needed.
- If the plugin uses Mnemosyne or other optional deps, those must be installed separately.

### Verify the Copy — the `cp -r` Trap

Community repos often have the Python package **nested inside a repo-root subdirectory** (e.g. `doga/` repo → `doga/doga/__init__.py`). A naive `cp -r repo ~/.hermes/plugins/<name>/` produces:

```
~/.hermes/plugins/<name>/
├── plugin.yaml
└── repo-name/             ← extra nesting level
    └── __init__.py
```

This **will not load**. The Hermes plugin loader expects `__init__.py` at the plugin root:

```
~/.hermes/plugins/<name>/
├── plugin.yaml
└── __init__.py            ← HERE, not one level deeper
```

**After any `cp -r` install, always verify the structure:**

```bash
ls -la ~/.hermes/plugins/<name>/__init__.py   # should exist at top level
```

If it's nested, either:
- Re-copy just the inner directory's contents (`cp repo/<subdir>/*.py ~/.hermes/plugins/<name>/`)
- Or create a thin `__init__.py` that re-exports from the nested package:

```python
# ~/.hermes/plugins/<name>/__init__.py
from .nested_package import register
```

This is the single most common cause of "plugin doesn't load" for community plugins.

## Updating a Plugin

Since user plugins are file-copies (not package-managed), updating means repeating the install:

```bash
cd /tmp
git clone https://github.com/user/repo.git --depth 1
cp -r repo/<plugin-dir>/* ~/.hermes/plugins/<name>/
hermes plugins enable <name>   # re-enable if needed
rm -rf /tmp/repo
```

Then `/reset` for the new version.

## Tracking in Community Manifest

After installing a new plugin, add an entry to `~/.hermes/community-manifest.json`:

```json
{
  "name": "plugin-name",
  "type": "plugin",
  "source": "https://github.com/...",
  "install_date": "YYYY-MM-DD",
  "version": "x.y.z",
  "install_method": "git clone → cp to ~/.hermes/plugins/<name>/",
  "update_command": "...",
  "post_update": "hermes plugins enable <name> (if needed) + /reset",
  "status": "active"
}
```

## CLI Reference

```bash
hermes plugins list              # Show all plugins + status
hermes plugins enable <name>     # Enable a plugin
hermes plugins disable <name>    # Disable a plugin
hermes plugins install <name>    # Install from bundled/pip (NOT community)
hermes plugins remove <name>     # Remove a plugin from registry
```

## Community Plugin Evaluation

Before installing any community plugin, run this checklist. Most "popular" plugins fail at least 2 of these gates.

**Gate 1 — Environment compatibility:**
- Does it import from a fixed path (e.g., `../evey_utils.py`)? If yes, it breaks if installed anywhere except the exact expected directory.
- Does it assume specific env vars (`OPENAI_BASE_URL`, `OPENAI_API_KEY`)? Check if those vars point to a compatible provider on this system.
- Does it hardcode a model name? If the model isn't available through your provider, the plugin silently degrades or fails.

**Gate 2 — Maintenance reality:**
- How many contributors? Single-author repos are high-risk for abandonment.
- When was the last commit? >3 months stale = maintenance risk.
- Are there open issues/PRs that haven't been addressed?

**Gate 3 — Redundancy check:**
- Does it duplicate what Hermes already does natively? (Memory → Mnemosyne, Goals → built-in, Delegation → built-in, Identity → SOUL.md)
- Count the plugins that add real value vs. the ones that wrap existing capabilities.

**Gate 4 — Token overhead:**
- Every registered tool adds schema to the system prompt on every turn. On free models with limited context, this costs headspace.
- Is the tool used frequently enough to justify its per-turn cost?

**Gate 5 — Disk and resource impact:**
- Does it write to disk unconditionally (logs, events, caches)? On a 2GB VPS, every MB matters.
- Does it make external network calls that could fail or leak data?

**The Parliament Method** — for weighing multiple plugins or options, simulate a parliamentary debate with committees (Infrastructure, Security, Operations, Value). Each committee presents findings, then a floor vote. This surfaces tradeoffs that a flat pro/con list misses.

## Troubleshooting

| Symptom | Likely Cause |
|---------|-------------|
| Plugin shows "enabled" but tools don't appear | Plugin hasn't been loaded yet — needs `/reset` or new session |
| `hermes plugins enable` fails with "not found" | Plugin directory missing from `~/.hermes/plugins/<name>/` or no valid `plugin.yaml` |
| Plugin loads but hooks don't fire | `register(ctx)` function missing or didn't call `ctx.register_hook()` |
| Tools registered but model doesn't use them | Model needs to be a tool-calling model; check provider supports function calling |
| `Failed to load plugin 'X': No __init__.py` | Plugin's Python module is nested inside a subdirectory (e.g. `plugins/X/X/__init__.py`) instead of at the plugin root (`plugins/X/__init__.py`). Check with `ls ~/.hermes/plugins/X/__init__.py`. Fix: create a thin top-level `__init__.py` that re-exports `register` from the nested package, or recopy the files to flatten the structure (see "Verify the Copy — the `cp -r` Trap" above). |
\n## Auditing Community Additions\n\nRun a full inventory whenever the user asks what's been added, or when setting up a new environment. Check these locations:\n\n1. **User plugins** — `~/.hermes/plugins/*/plugin.yaml`\n2. **Bundled plugins with .git** — `find /usr/local/lib/hermes-agent/plugins -name .git -type d` (community plugins cloned directly into bundled dir)\n3. **User scripts** — `~/.hermes/scripts/`\n4. **Custom binaries** — `~/.hermes/bin/` (check `head` for bash vs ELF vs downloaded binary)\n5. **Pip packages** — `pip list | grep` for community packages (mnemosyne-memory, etc.)\n6. **Git repos under /root** — `find /root -maxdepth 4 -name .git -type d` (exclude Hermes own)\n7. **Local skills** — `hermes skills list` filtered by `local` source\n8. **Community manifest** — Check `~/.hermes/community-manifest.json` for existing entries\n\nUpdate the manifest with any findings. This is the checklist we used in the initial audit.\n\n## Pitfalls\n\n- Plugin names with hyphens in the directory name are fine, but Python module names can't have hyphens — the loader converts them to underscores internally.\n- The `plugin.yaml` hooks field is **informational** (used for listing/UI). The actual registration happens in `register(ctx)` via `ctx.register_hook()`. Both should agree.\n- User plugins override bundled plugins of the same name (last-writer-wins on name collision).\n- **Bundled-dir clones**: Community plugins may be cloned directly into `/usr/local/lib/hermes-agent/plugins/<category>/<name>/` (e.g. hermes-lcm in `context_engine/lcm/`). This creates problems: `hermes update` may overwrite them, and the git remote URL may contain embedded credentials (`https://user:***@github.com/...`). Check `cd <dir> && git remote -v` for credential exposure. Prefer `~/.hermes/plugins/<name>/` for all new community plugins.\n- Plugins cannot use `delegate_task`, `clarify`, `memory`, `send_message`, or `execute_code` — those are agent-level tools, not plugin-level.

- **Pip-dependency side effects at import time**: When a plugin's `__init__.py` does `from some_package import something`, and that pip package runs DB initialization, file I/O, or other side effects at **module level** (inside its own `__init__.py`, not lazily in functions), the import may fail with `OperationalError`, `PermissionError`, or similar — *not* `ImportError`. Catching only `ImportError` won't handle this. Prefer either:
  - Catch `Exception` instead of `ImportError` when importing optional pip deps
  - Or use lazy imports inside the handler/function rather than at module level
  - Example: `mnemosyne` pip package calls `init_db()` at module level, so `except ImportError` doesn't catch DB-lock failures. Fix: `except Exception`.\n