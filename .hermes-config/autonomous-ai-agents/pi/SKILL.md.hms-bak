---
name: pi
description: "Delegate coding to Pi CLI (@earendil-works/pi-coding-agent) — minimal TypeScript coding agent with tree-based sessions, extensions API, and aggressive token efficiency."
version: 1.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Pi, Autonomous, TypeScript, Extensible]
    related_skills: [claude-code, codex, opencode, hermes-agent]
---

# Pi CLI

Use [Pi](https://pi.dev) as an autonomous coding worker orchestrated by Hermes terminal/process tools. Pi is a minimal terminal coding harness by @badlogicgames / earendil-works — TypeScript-based, 53.5k+ stars, known for extremely low token usage and a philosophy of primitives-over-features.

## When to Use

- User explicitly asks to use Pi
- User has set Pi as the default coding agent (all pure coding tasks routed through Pi)
- You want a **token-efficient** coding agent for one-shot or iterative tasks
- You need to delegate coding to a Node.js/TypeScript agent (lighter than Python-based agents)
- The task benefits from Pi's **minimal system prompt** — less context overhead per turn
- You want parallel task execution in isolated workdirs
- **Code review** of domain-specific languages (Pine Script, SQL, DSLs) — Pi's fast iteration and minimal overhead makes it ideal for reviewing script output and catching semantic issues that the original writer missed

## Prerequisites

- Pi installed: `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` or `curl -fsSL https://pi.dev/install.sh | sh`
- Auth configured: run `/login` inside Pi for subscription providers (Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot), or set `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / etc. as env vars
- Verify: `pi --help` shows usage
- Git repository for code tasks (recommended)
- `pty=true` for interactive TUI sessions

## Binary Resolution

Check which Pi binary Hermes resolves to:

```bash
terminal(command="which -a pi")
terminal(command="pi --version")
```

If needed, pin the install path explicitly.

## One-Shot Tasks (Print Mode)

Use `pi -p` for bounded, non-interactive tasks. No PTY needed:

```bash
terminal(command="pi -p 'Add retry logic to API calls and update tests'", workdir="~/project")
```

Pipe stdin as context:

```bash
terminal(command="cat README.md | pi -p 'Summarize this project'")
```

**Large file code review** (preferred over `@` for files >10KB — avoids path resolution issues with spaces in paths and timeouts on large context):

```bash
terminal(command="cat /path/to/file.pine | pi -p 'Review this for syntax errors, logic bugs, and edge cases'", timeout=300)
```

Reference files with `@` prefix:

```bash
terminal(command="pi -p @src/api.ts @src/api.test.ts 'Review these together for correctness'", workdir="~/project")
```

Force a specific model:

```bash
terminal(command="pi -p 'Refactor auth module' --model anthropic/claude-sonnet-4", workdir="~/project")
```

Specify provider:

```bash
terminal(command="pi -p '...' --provider openai", workdir="~/project")
```

Use JSON event mode for structured output:

```bash
terminal(command="echo 'add logging to all handlers' | pi --mode json -p 'Write the code'", workdir="~/project")
```

## Interactive Sessions (Background + PTY)

For iterative work requiring multiple exchanges, start the TUI in background:

```bash
terminal(command="pi", workdir="~/project", background=true, pty=true)
# Returns session_id

# Send a prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Steer mid-task (sent after current tool finishes)
process(action="submit", session_id="<id>", data="Use PKCE flow, not implicit")

# Follow-up (sent after all work finishes)
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit cleanly — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# OR
process(action="kill", session_id="<id>")
```

## Session Management

```bash
pi -c             # Continue most recent session
pi -r             # Browse and select a session
pi --session <ID> # Specific session
pi --fork <ID>    # Fork a session into a new file
pi --no-session   # Ephemeral mode (no save)
```

Inside Pi TUI:

| Command | Description |
|---------|-------------|
| `/resume` | Pick from previous sessions |
| `/new` | Start fresh session |
| `/tree` | Navigate session tree; view branches |
| `/fork` | Branch from any prior message |
| `/clone` | Duplicate current branch into new session |
| `/session` | Show session metadata (file, ID, tokens, cost) |
| `/compact [prompt]` | Manual context compression |
| `/export [file]` | Export session to HTML |
| `/share` | Upload as private GitHub Gist |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/login`, `/logout` | Manage credentials |
| `/model` | Switch models |
| `/settings` | Thinking level, theme, transport |
| `/reload` | Reload extensions, skills, keybindings, context files |
| `/hotkeys` | Show all keyboard shortcuts |
| `/quit` | Exit |

## Editor Features

| Action | Key/Input |
|--------|-----------|
| File reference | `@` fuzzy search |
| Multi-line | `Shift+Enter` (`Ctrl+Enter` on Windows Terminal) |
| Paste image | `Ctrl+V` (`Alt+V` on Windows) |
| Shell command (visible) | `!command` — runs + output to model |
| Shell command (hidden) | `!!command` — runs, no output to model |
| External editor | `Ctrl+G` opens `$VISUAL` / `$EDITOR` |

## Message Queue

While the agent is working:

- **Enter** — steer message (delivered after current tool finishes)
- **Alt+Enter** — follow-up (delivered after all work finishes)
- **Escape** — abort queued messages, restore to editor

## Model Switching

- `/model` or `Ctrl+L` — open model picker
- `Shift+Tab` — cycle thinking level
- `Ctrl+P` / `Shift+Ctrl+P` — cycle through scoped favorites

## Common Flags

| Flag | Use |
|------|-----|
| `-p`, `--print` | One-shot, non-interactive, print response and exit |
| `--mode json` | JSON event output (machine-readable) |
| `--mode rpc` | RPC mode over stdin/stdout |
| `--provider` | Force provider (anthropic, openai, google, etc.) |
| `--model` | Model pattern (`provider/id` syntax) |
| `--api-key` | Override API key for this session |
| `-c` | Continue most recent session |
| `-r` | Browse sessions |
| `--session <ID>` | Open specific session |
| `--fork <ID>` | Fork a session |
| `--no-session` | Ephemeral mode |
| `--no-context-files`, `-nc` | Skip AGENTS.md / CLAUDE.md loading |

## Custom Providers (models.json)

Configure custom OpenAI-compatible endpoints, local models (Ollama, vLLM, LM Studio), or routed providers in `~/.pi/agent/models.json`. The file hot-reloads every time `/model` opens — no restart needed.

### Structure

The root must be an object with a `providers` key (NOT an array):

```json
{
  "providers": {
    "my-provider": {
      "baseUrl": "https://api.example.com/v1",
      "api": "openai-completions",
      "apiKey": "MY_API_KEY",
      "authHeader": true,
      "models": [
        {
          "id": "my-model",
          "name": "My Model",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 128000,
          "maxTokens": 16384
        }
      ]
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `baseUrl` | API endpoint URL |
| `api` | API type: `openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative-ai` |
| `apiKey` | API key — see resolution below |
| `authHeader` | Set `true` to auto-add `Authorization: Bearer <apiKey>` |
| `headers` | Custom headers (static or shell command values) |
| `models` | Array of model configs |
| `compat` | Provider compatibility overrides (e.g. `{ "supportsDeveloperRole": false }` for Ollama) |

### API Key Resolution (three formats)

| Format | Syntax | Example |
|--------|--------|---------|
| Env var name | `"ENV_VAR_NAME"` | `"apiKey": "OPENCODE_GO_API_KEY"` |
| Shell command | `"!command"` | `"apiKey": "!grep '^KEY=' ~/.env \| cut -d= -f2"` |
| Literal | `"sk-..."` | Direct value (least secure) |

**Env var format requires the variable to be EXPORTED** — Pi and its subprocesses inherit the environment. If the var is set but not exported (common with Hermes `.env` files), use the shell command format instead:

```json
"apiKey": "!grep '^MY_API_KEY=' /path/to/.env | head -1 | cut -d= -f2"
```

### Selecting Custom Models

Use `--model provider-name/model-id`:

```bash
pi -p "Write fibonacci" --model my-provider/my-model
```

The `/model` TUI command lists all custom providers and models. Shell-command-based `apiKey` entries show as "configured" in the model picker (the command is NOT executed during availability checks).

### Common Patterns

**Proxy through an existing provider** (add baseUrl only, keep built-in models):
```json
{ "providers": { "openai": { "baseUrl": "https://my-proxy.example.com/v1" } } }
```

**Merge custom models into a built-in provider**:
```json
{ "providers": { "anthropic": { "models": [{ "id": "my-clone", "name": "Custom Claude" }] } } }
```

**Local models** (Ollama/vLLM — only `id` required):
```json
{ "providers": { "ollama": { "baseUrl": "http://localhost:11434/v1", "api": "openai-completions", "apiKey": "ollama", "models": [{ "id": "llama3.1:8b" }] } } }
```

## Extensions

Pi extensions are TypeScript modules with full access to tools, commands, keyboard shortcuts, and TUI widgets. The extension directory auto-loads — just drop a file and restart Pi.

### Directory Structure

```
~/.pi/agent/extensions/
├── my-extension.ts               ← standalone file, auto-loaded
└── sandbox/                      ← directory with npm deps
    ├── index.ts                  ← entry point (declared in package.json)
    ├── package.json
    └── node_modules/             ← npm install'd separately
```

Project-scoped extensions go in `.pi/extensions/` inside your project directory.

### Installation

1. **Standalone `.ts` file** — copy to `~/.pi/agent/extensions/`. No config needed, auto-loaded on next start.
2. **Directory with `package.json`** — copy the directory + run `npm install` inside it. Pi loads the entry point declared under `"pi"."extensions"` in the package.json.
3. **Project-scoped** — use `<project>/.pi/extensions/` instead of the global path.

Run `/reload` inside Pi's TUI to pick up new extensions without restarting.

### Listing Loaded Extensions

Ask Pi directly:

```bash
pi -p "List which extensions are currently loaded" --model <your-model>
```

### Recommended Stack

See `references/pi-extensions.md` for the full catalog of safety and quality extensions from Pi's examples repo (protected-paths, dirty-repo-guard, git-checkpoint, tools, question, questionnaire, sandbox).

## Hermes Integration Model

Pi is a standalone CLI tool — Hermes calls it as a sub-process via `terminal()`. There is no plugin, no embedding, no shared state, no background daemon. When neither you nor Hermes is calling `pi`, it is not running.

### Interaction Patterns

| Pattern | How Hermes calls it | Best for |
|---------|--------------------|----------|
| **One-shot** | `terminal(command="pi -p '...' --model X")` — no PTY, exits when done | Bounded coding tasks, simple scripts, quick fixes |
| **Interactive** | `terminal(command="pi", background=true, pty=true)` + `process(action="submit")` | Iterative sessions needing back-and-forth |
| **Delegated** | `delegate_task(goal=..., toolsets=["terminal"])` — subagent loads pi skill | Isolated coding tasks in parallel |

### Division of Labor

| Hermes owns | Pi owns |
|-------------|---------|
| Conversation with you, multi-tool orchestration, long-running state, deciding WHEN to code | The actual coding session, file edits, git ops, fast code iterations, its own extension safety net |

### Uninstall

```bash
npm uninstall -g @earendil-works/pi-coding-agent   # Remove the CLI
rm -rf ~/.pi                                        # Remove all config, extensions, sessions
```

No Hermes configs, no system services, no cron jobs, no orphan processes. Pi only runs when invoked.

## Context Files (AGENTS.md)

Pi loads project instructions from:

1. `~/.pi/agent/AGENTS.md` — global instructions
2. Parent directories (walking up from cwd)
3. Current directory `AGENTS.md` or `CLAUDE.md`

**Recommended global AGENTS.md:** the Karpathy-inspired behavioral guidelines from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills). These encode "think before coding, simplicity first, surgical changes, goal-driven execution" — pair well with Pi's minimal-overhead philosophy. Fetch and save:

```bash
curl -sL "https://raw.githubusercontent.com/multica-ai/andrej-karpathy-skills/main/CLAUDE.md" -o ~/.pi/agent/AGENTS.md
```

System prompt overrides:
- Replace default: `~/.pi/agent/SYSTEM.md` (global) or `.pi/SYSTEM.md` (project)
- Append to default: `APPEND_SYSTEM.md` in either location

## Procedure

1. Verify tool readiness:
   - `terminal(command="pi --version")`
   - Ensure auth is configured (env var or `/login` done)
2. For bounded tasks, use `pi -p '...'` (no pty needed).
3. For iterative tasks, start `pi` with `background=true, pty=true`.
4. Monitor long tasks with `process(action="poll"|"log")`.
5. Send steering messages via `process(action="submit", data="...")`.
6. Exit with Ctrl+C (`\x03`) or `process(action="kill")`.
7. Summarize file changes, test results, and next steps back to user.

## Parallel Work Pattern

Use separate workdirs to avoid collisions:

```bash
terminal(command="pi -p 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="pi -p 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

## Pi-Specific Design Notes

- **No built-in MCP** — Pi deliberately doesn't ship MCP. Use CLI tools via Skills or Extensions instead
- **No built-in sub-agents** — spawn additional Pi instances via tmux or build an extension for that
- **No plan mode** — write plans to files or build an extension
- **Extensions API** — TypeScript modules with full access to tools, commands, keyboard shortcuts, TUI widgets. 50+ examples available. Extensions run inside Pi's process; Hermes neither knows nor cares about them. See the Extensions section for installation guide and `references/pi-extensions.md` for a recommended catalog.
- **Skills** — on-demand capability packages loaded via AGENTS.md
- **Packages** — share extensions, skills, templates, themes via npm or git
- **Token efficiency** — Pi has one of the smallest system prompts among coding agents. This means less context overhead per turn for the same work

## Pitfalls

- One-shot mode (`pi -p`) does NOT need PTY. Interactive (`pi` alone) DOES need `pty=true`.
- **WSL npm global installs** — `npm install -g` on WSL puts binaries under `~/.hermes/node/bin/`, which is NOT in default PATH. Add `$HOME/.hermes/node/bin` to `~/.profile` (not just `~/.bashrc`, which has an interactive-mode guard that skips PATH exports in non-interactive shells). Without this, `pi` (and other npm globals) won't resolve in Hermes terminal() calls or login shells.
- Pi's TUI may require Enter twice in some terminals (once to finalize text, once to send).
- PATH can resolve the wrong Pi binary if multiple Node versions are installed. Use full path if needed.
- Pi's `--mode json` output is a JSON-per-line event stream, not a single JSON blob. Pipe to `jq -c` for per-event filtering.
- **Env var API keys must be EXPORTED** — Pi and its subprocesses inherit the process environment. If a key is set in a `.env` file without `export`, Pi won't see it via the env-var-name syntax. Use the shell-command format (`!grep ...`) to read from the file at runtime instead.
- Pi sessions are saved per-working-directory. Use `--no-session` for truly ephemeral runs.
- The `!command` feature in Pi's TUI runs commands inside your environment — aware of this when delegating sensitive work.
- Pi loads `AGENTS.md` from parent directories up to root — ensure project-level AGENTS.md doesn't inherit global instructions unexpectedly.
- Pi's extensions API gives full access — treat third-party Pi packages like any other npm dependency for supply-chain risk.
- **Pine Script `strategy.entry()` deduplication:** Using a fixed entry ID (e.g., `strategy.entry("BEAR", ...)`) causes Pine to merge all same-direction signals into one position, producing as few as 2 CSV rows total in Strategy Tester exports. Always use unique IDs per signal for export scripts: `strategy.entry("BEAR_" + str.tostring(bar_index), ...)`.
- **Pine Script `str.tostring(na)` produces the literal string "na":** During indicator warm-up or edge cases, this can crash downstream Python parsers with `float("na")` ValueError. Guard signal entries with `bar_index >= lookback` checks.
- **Large file context with slow models:** Files over ~10KB + slow reasoning models (DeepSeek V4 Flash) can cause 120s+ response times. Use higher `timeout` values in `terminal()` calls (300s) when reviewing large codebases.

## Verification

Smoke test:

```bash
terminal(command="pi -p 'Respond with exactly: PI_SMOKE_OK'")
```

Success criteria:
- Output includes `PI_SMOKE_OK`
- Command exits without provider/model errors
- For code tasks: expected files changed and tests pass

## Rules

1. Prefer `pi -p` for one-shot automation — simpler, no PTY needed.
2. Use interactive background mode only when iteration is needed.
3. Always scope Pi sessions to a single repo/workdir.
4. For long tasks, provide progress updates from `process` logs.
5. Report concrete outcomes (files changed, tests, remaining risks).
6. Exit interactive sessions with Ctrl+C or kill, never `/quit` via process write.
7. Pi's token efficiency advantage is most valuable on tasks with many back-and-forth turns.
8. When the user has set Pi as default coding agent, route all pure coding tasks through Pi without asking. Fall back to Hermes' own tools only if Pi is unsuitable (platform ops, credentials work, irreversible operations).
