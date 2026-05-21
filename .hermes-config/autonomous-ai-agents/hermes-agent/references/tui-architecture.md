# TUI Architecture

## What It Is

`hermes --tui` launches a terminal user interface rendered with **Ink** (Vercel's React-for-terminals, built on Yoga layout engine + React Reconciler). It is a separate front-end process that communicates with the same Python backend as the CLI.

### Process Split

```
┌──────────────────────┐     JSON-RPC over     ┌──────────────────────────┐
│   TUI (Node/Ink)    │ ◄───── stdin/stdout ──► │   Python Backend        │
│   ui-tui/src/       │                         │   tui_gateway/server.py │
│   app.tsx           │                         │   imports AIAgent       │
│   components/       │                         │   from run_agent.py     │
│   gatewayClient.ts  │                         │   opens state.db        │
└──────────────────────┘                         └──────────────────────────┘
```

The Node process handles rendering only. The Python subprocess loads config, connects to `state.db`, instantiates `AIAgent`, and runs the conversation loop. All tool execution, memory, skills, session persistence, and compression happen in Python — identical code path to CLI and gateway.

## What the TUI Actually Provides

| Feature | CLI (`hermes`) | TUI (`hermes --tui`) |
|---------|----------------|----------------------|
| Rendering | prompt_toolkit + Rich | Ink (React) with virtualized rows |
| Input area | Bottom of scrollback, chases the cursor | Fixed at screen bottom, never moves |
| Session list | `hermes sessions list` or `hermes sessions browse` (separate shell command) | **Overlay** triggered by `/resume` or `/session` at the prompt |
| Sidebar | None | None. The session picker is an overlay, not a persistent panel |
| Split views | None | None. Single-pane layout: transcript scrolls above, input below |
| Mouse support | Limited | Yes — click to position cursor, scroll wheel, click on session list items |
| Streaming render | Plain text with spinner | Character-by-character with proper markdown formatting |
| Slash commands | Full registry + `prompt_toolkit` autocomplete dropdown | Same, with a completions popup above the input |
| Memory/Skills/Tools | Identical | Identical (same Python backend) |
| Resuming old sessions | `--resume` flag or `/resume` in-session | `/resume` or `/session` opens overlay picker |

### The Session Picker (Not a Sidebar)

The TUI session list appears as a floating overlay positioned above the input bar, only when triggered. To see it:

```
/resume       # Opens picker with recent sessions
/session      # Same overlay
```

The picker shows:
- Session ID, message count, age, source
- Title (or first user message preview)
- Arrow keys to select, Enter to resume
- `d` to delete (press twice to confirm)
- `1`-`9` for quick jump to that slot

When you select a session, the overlay closes and the conversation loads into the chat area. There is no visible indication that you've switched sessions beyond the transcript content changing — no "now viewing session X" header, no sidebar highlight.

The overlay is rendered at `src/components/sessionPicker.tsx`. It fetches sessions via RPC call `session.list` and renders up to 200 items, 15 visible at a time.

### Layout Architecture

Source: `src/components/appLayout.tsx`

```
┌───────────────────────────────────────┐
│  TranscriptPane (ScrollBox)           │
│  - Virtualized message rows           │
│  - Streaming assistant area           │
│  - Banner on fresh session            │
├───────────────────────────────────────┤
│  StatusRulePane (top or bottom)       │
│  - Model, cost, session age, cwd      │
├───────────────────────────────────────┤
│  ComposerPane (fixed, flex-shrink=0)  │
│  - Queued messages                    │
│  - Prompt prefix + TextInput          │
│  - Sticky prompt (when set)           │
│  - FloatingOverlays (absolute pos)    │
│    → SessionPicker                    │
│    → ModelPicker                      │
│    → SkillsHub                        │
│    → Completions popup                │
│    → Pager (for history, help)        │
│    → ApprovalPrompt / ClarifyPrompt   │
└───────────────────────────────────────┘
```

Key detail: overlays are positioned `bottom="100%"` relative to the composer, meaning they float upward from the input bar. The composer row itself reserves the scrollbar gutter width even when hidden (`TranscriptScrollbar`) so that typing never causes line-wrapping to shift when the scrollbar column appears/disappears.

### Config & State Shared with CLI

- Same `~/.hermes/config.yaml`
- Same `~/.hermes/.env` (API keys)
- Same `~/.hermes/state.db` (SQLite sessions)
- Same `~/.hermes/skills/`
- Same `~/.hermes/logs/`
- Same `hermes_constants.get_hermes_home()` paths
- Same `AIAgent` class from `run_agent.py`

### Launch

```bash
hermes --tui                    # Full TUI (AlternateScreen mode)
HERMES_TUI_INLINE=1 hermes --tui   # Inline mode (no AlternateScreen — scrollback preserved)
```

Inline mode (`INLINE_MODE` env var check at `src/config/env.ts`) skips the alternate screen, so rows scrolled-off remain in the terminal's native scrollback buffer.

### Known Gaps vs CLI

| CLI has | TUI lacks |
|---------|-----------|
| `--resume` flag at process start | Must start fresh, then `/resume` |
| `--source` session tagging | No per-session source override |
| Alt+F file attach (keybinding) | No keyboard file attach |
| Ctrl+B push-to-talk (keybinding) | No voice mode keybinding |
| `/history` scrollable pager | Overlay-based (same content) |
| Skin engine (color themes) | Theme is hardcoded per skin ID — less flexible |

## When to Recommend CLI Over TUI

- User works in a terminal multiplexer (tmux/screen) and wants the session to stay in the scrollback
- User frequently uses `--resume` with specific session IDs
- User needs voice mode with push-to-talk
- User is on a slow connection (TUI adds a Node process + JSON-RPC overhead)
- User wants the simplest possible thing — CLI is one Python process, no Node dependency
