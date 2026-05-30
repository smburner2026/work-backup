# Pi Extension Catalog

Recommended extensions from the Pi examples repo (`earendil-works/pi/packages/coding-agent/examples/extensions/`). All are MIT-licensed example code — copy, modify, ship.

## Safety Layer

| Extension | Source | What it does |
|-----------|--------|--------------|
| **protected-paths** | `extensions/protected-paths.ts` | Intercepts `write`/`edit` tool calls and blocks them if the path contains `.env`, `.git/`, or `node_modules/`. In TUI mode shows a warning notification; in headless mode blocks silently. |
| **dirty-repo-guard** | `extensions/dirty-repo-guard.ts` | Prevents session switch (`session_before_switch`) and fork (`session_before_fork`) when `git status --porcelain` shows uncommitted changes. In headless mode: blocks automatically. In TUI mode: asks "You have N uncommitted file(s). Proceed anyway?" |
| **git-checkpoint** | `extensions/git-checkpoint.ts` | Runs `git stash create` before each turn (non-destructive — creates a commit ref without touching working tree). On `/fork`, looks up the stash ref for that entry and offers to `git stash apply` the code state to match the conversation branch. |
| **sandbox/** | `extensions/sandbox/` | Replaces the built-in `bash` tool with an OS-level sandboxed version (bubblewrap on Linux, sandbox-exec on macOS). Config via `~/.pi/agent/extensions/sandbox.json` (global) or `.pi/sandbox.json` (project). Default denies read of `~/.ssh`, `~/.aws`, `~/.gnupg` and write of `.env`, `*.pem`, `*.key`. Requires `@anthropic-ai/sandbox-runtime` npm dep + `bubblewrap` system package. |

## Interaction Extensions

| Extension | Source | What it does |
|-----------|--------|--------------|
| **question** | `extensions/question.ts` | Registers a `question` tool the LLM can call to ask the user for input. Options list + "Type something" custom input mode. Falls back gracefully in headless/non-interactive mode. Uses `@earendil-works/pi-tui` Editor component. |
| **questionnaire** | `extensions/questionnaire.ts` | Multi-question version of question.ts. Tabbed interface (Q1 → Q2 → ... → Submit). Each question supports options + optional custom input. Submit tab shows all answers with "Unanswered" warnings. Single-question mode auto-submits. |
| **tools** | `extensions/tools.ts` | Registers a `/tools` TUI command that lets users toggle Pi's built-in tools on/off. State is persisted per session branch via custom session entries, so different forks can have independent tool sets. Automatically restores on session start and tree navigation. |

## How They Layer

```
question / questionnaire      ← Pi asks you before acting
  └─ tools                    ← You control what Pi is allowed to do
       └─ protected-paths     ← Safety net for sensitive files
       └─ dirty-repo-guard    ← Safety net for git state
       └─ git-checkpoint      ← Safety net for code history
       └─ sandbox             ← OS-level sandbox for bash execution
```

## Installation

All standalone `.ts` files go in `~/.pi/agent/extensions/` — zero config, auto-loaded.
The sandbox directory with its own package.json needs `npm install` inside it.
Run `/reload` in Pi TUI to pick up changes without restarting.
