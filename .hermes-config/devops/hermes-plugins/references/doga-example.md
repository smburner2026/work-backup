# DOGA Plugin — Example Community Plugin

Source: https://github.com/0z1-ghb/doga-hermes
Installed: 2026-05-24
Author: 0z1-ghb
Version: 1.1.0

⚠️ **Loading history: DOGA failed to load on 11+ gateway restarts due to a structural mismatch. Fix applied 2026-05-26. See "Loading Failure" below.**

## Actual Installed Structure

The DOGA repo has the Python package nested inside a repo-root subdirectory (both named `doga/`):

```
~/.hermes/plugins/doga/
├── plugin.yaml              # Manifest: hooks, doga toolset, doga command
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── LICENSE
├── .gitignore
├── assets/
├── .github/
├── tests/
└── doga/                    ← NESTED Python package (not at root!)
    ├── __init__.py          ← register(ctx) — hooks, tools, slash command
    ├── de_bono_hats.py
    ├── depth_selector.py
    ├── simulation_engine.py
    ├── thinking_prompt.py
    └── output_formatter.py
```

There is **no** `__init__.py` at `~/.hermes/plugins/doga/__init__.py` — the Hermes plugin loader needs one at the plugin root.

## Loading Failure

The log shows the error on every gateway restart since install (11+ occurrences):

```
WARNING hermes_cli.plugins: Failed to load plugin 'doga': No __init__.py in /root/.hermes/plugins/doga
```

**Root cause:** `cp -r doga ~/.hermes/plugins/doga` copies the entire repo root, but the Python package lives inside `doga/doga/` (nested). The loader expects `plugins/doga/__init__.py`, not `plugins/doga/doga/__init__.py`.

**Fix:** Create a thin top-level `__init__.py`:

```python
# ~/.hermes/plugins/doga/__init__.py
from .doga import register
```

Or recopy just the inner package:

```bash
cp -r ~/.hermes/plugins/doga/doga/*.py ~/.hermes/plugins/doga/
```

Then `/reset` or restart the gateway.

### Secondary Fix (2026-05-26)

The nested `doga/__init__.py` had `except ImportError:` when importing `from mnemosyne import remember, recall`. The `mnemosyne` pip package calls `init_db()` at module level, which raises `OperationalError: database is locked` when another Hermes process holds the DB lock — not `ImportError`. The `except ImportError` doesn't catch this, causing the entire DOGA plugin load to fail even after the structural fix.

**Fix applied:** broadened to `except Exception:` — DOGA degrades gracefully when Mnemosyne is unavailable.

```python
try:
    from mnemosyne import remember, recall
    MNEMOSYNE_AVAILABLE = True
except Exception:  # was: except ImportError
    MNEMOSYNE_AVAILABLE = False
```

This pattern is now documented as a general pitfall in `hermes-plugins` SKILL.md.

## What DOGA Does (once it loads)

- **Goal Detection** — classifies queries as Information / Understanding / Action
- **Scenario Generation** — enumerates and weighs multiple interpretations
- **Monte Carlo Simulation** — pure-Python engine (10K–50K iterations) via `simulate` tool
- **Thinking Panel** — `<world_model>` blocks extracted and formatted as `[DOGA: Thinking Process]`
- **Auto Depth** — complexity-based depth selection (0 LLM tokens)
- **De Bono Six Thinking Hats** — structured parallel reasoning
- **Recursive Reasoning** — `reason_deeper` tool for multi-level self-critique
- **Hard-Break Safety** — auto-stop after 3 ignored `reason_deeper` calls

## Hooks

| Hook | Purpose |
|------|---------|
| `pre_llm_call` | Inject goal detection + scenario guidance into prompt |
| `transform_llm_output` | Extract `<world_model>` blocks, format as thinking panel |
| `post_tool_call` | Log tool usage; track `reason_deeper` recursion depth |

## Tools

| Tool | Toolset | Description |
|------|---------|-------------|
| `simulate` | doga | Monte Carlo simulation over probabilistic scenarios |
| `reason_deeper` | doga | Recursive self-critique with per-level hat rotation |

## Slash Commands

| Command | Effect |
|---------|--------|
| `/doga on/off` | Toggle |
| `/doga status` | Show current settings |
| `/doga auto` | Auto depth (default) |
| `/doga manual low|medium|high` | Force level |
| `/doga depth <1-5>` | Set depth (manual mode) |
| `/doga hats on/off` | Toggle De Bono |
| `/doga show/hide` | Simulation panel |
| `/doga memory on/off` | Mnemosyne goal memory |
| `/doga max_recursion <1-5>` | Reason deeper limit |

## Update Command

```bash
cd /tmp && git clone https://github.com/0z1-ghb/doga-hermes.git --depth 1 && \
  cp doga-hermes/doga/*.py ~/.hermes/plugins/doga/ && \
  cp doga-hermes/plugin.yaml ~/.hermes/plugins/doga/ && \
  rm -rf /tmp/doga-hermes
```

Then `hermes plugins enable doga` (if needed) + `/reset`.

Note: the update command copies only the inner `doga/*.py` files (not the repo root), so it avoids the nesting trap.

## Dependencies

- Zero required (pure stdlib Python)
- Optional: `mnemosyne-memory` (pip) for goal memory persistence
