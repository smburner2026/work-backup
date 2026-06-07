---
name: terminal-io-debugging
description: "Debug terminal I/O issues in TUI applications — bracketed paste, clipboard, escape sequences, keyboard modes, and OpenTUI interaction quirks."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [terminal, tui, clipboard, bracketed-paste, escape-sequences, opentui, debugging]
    related_skills: [debugging-hermes-tui-commands, systematic-debugging]
---

# Terminal I/O Debugging

## Overview

Terminal UIs (TUIs) rely on escape sequences for copy/paste, keyboard modes, mouse events, and terminal capabilities. These sequences interact with the terminal emulator (Windows Terminal, iTerm2, kitty, etc.) and the TUI framework (OpenTUI, Ink, React Terminal, etc.) — and the interaction is often fragile.

This skill covers debugging patterns for terminal I/O issues: bracketed paste not working, copy failing, keyboard shortcuts intercepted, and escape sequences being eaten or duplicated.

## When to Use

- Copy (Ctrl+C, Ctrl+Y, etc.) doesn't put text in the system clipboard
- Paste (Ctrl+V, Ctrl+Shift+V, right-click) inserts nothing or garbage
- Keyboard shortcuts don't reach the TUI app (e.g. Ctrl+Tab, Ctrl+digit)
- Terminal mode reset sequences are visibly printed in the TUI
- A fix that worked previously stops working after restart

## Core Concepts

### Bracketed Paste (`?2004`)

When **disabled** (`\x1b[?2004l`): the terminal emulator sends pasted text character-by-character as if typed.

When **enabled** (`\x1b[?2004h`): the terminal wraps pasted text in `\x1b[200~` and `\x1b[201~` markers. The TUI can distinguish paste input from keyboard input and handle it correctly.

**Key symptom:** If bracketed paste is disabled, the TUI receives raw paste bytes mixed into its input stream. In OpenTUI-based apps, the textarea's `onPaste` never fires because the paste markers never arrive.

**`writeSync(fd)` vs `process.stdout.write`:** OpenTUI's native (Zig/WASM) layer writes to the terminal via raw fd operations — NOT through `process.stdout.write()`. If you write escape sequences via `process.stdout.write()` while OpenTUI is also writing, the kernel may deliver them out of order. Always prefer `fs.writeSync(fd, ...)` for terminal escape sequences that must be interleaved correctly with OpenTUI's frames:

```typescript
import { writeSync } from "node:fs"

function sendEscape(seq: string) {
  const fd = (process.stdout as any).fd
  if (typeof fd === "number") writeSync(fd, seq)
  else process.stdout.write(seq)
}
```

Note: this requires ESM import — `require("fs")` does not work in Bun/ESM projects. Use top-level `import { writeSync } from "node:fs"`.

### Windows Terminal Clipboard Interception

Windows Terminal intercepts `Ctrl+V` at the OS level as `PasteFromClipboard`. When bracketed paste is enabled, WT wraps the clipboard text in `\x1b[200~...\x1b[201~`. When disabled, WT sends raw bytes directly.

WT also steals `Ctrl+C` as "copy selected text" in some configurations — this is a separate setting (Terminal.CopySelection).

### OSC 52 Clipboard

`\x1b]52;c;BASE64...\x07` — terminal-based clipboard write. Works on any terminal that supports it. The `clipboard.copyToClipboardOSC52()` method in OpenTUI uses this.

## The Triple-Fix Pattern (Bracketed Paste)

When paste works in some sessions but not others, or stops working after restart, the root cause is almost always one of three issues:

### Fix 1: Startup Reset Sequence

The TUI's startup reset sequence (`resetTerminalModes()` or equivalent) often sends `\x1b[?2004l` (disable) to "clean up" from a crashed prior process. This disables bracketed paste before the TUI ever needs it.

**Fix:** Change the reset sequence to `\x1b[?2004h` (enable). Bracketed paste should be on from the very first escape sequence.

```typescript
// BAD: resets bracketed paste to disabled
export const RESET = "\\x1b[?2004l" + ...

// GOOD: starts with bracketed paste enabled
export const RESET = "\\x1b[?2004h" + ...
```

### Fix 2: Competing Native Terminal Setup

OpenTUI's native `setupTerminal()` (Zig/WebAssembly layer) runs **inside** `createCliRenderer()`. It:
- Sends capability probes (DA, DA2, XTVERSION) asynchronously
- Saves terminal mode state
- May call native `restoreTerminalModes()` later (e.g. on focus events)

If native setupTerminal queries terminal state BEFORE our `\x1b[?2004h` takes effect, it records "bracketed paste: disabled" and restores that state later.

**Fix:** Re-assert `\\x1b[?2004h` after `createCliRenderer()` returns, using **`writeSync(fd)`** (not `process.stdout.write`) to match OpenTUI's raw fd output path. Hook into both the `focus` and `capabilities` events. Add `setTimeout` delayed re-assertions to catch the async probe settle window (capability DA/DA2/XTVERSION exchanges take ~100-300ms):

```typescript
import { writeSync } from "node:fs"

const pasteOn = () => {
  if (!process.stdout.isTTY) return
  const fd = (process.stdout as any).fd
  // writeSync(fd) matches OpenTUI's native fd path — avoids
  // buffering/interleaving issues with process.stdout.write
  if (typeof fd === "number") writeSync(fd, "\x1b[?2004h")
  else process.stdout.write("\x1b[?2004h")
}
pasteOn()

// Also fire delayed re-assertions — OpenTUI's async capability
// probing exchanges take ~100-300ms, and the native response
// handler may restore terminal modes without bracketed paste.
// Catching at 500ms and 2s covers the settle window even on
// slow WSL bridge latency.
setTimeout(pasteOn, 500)
setTimeout(pasteOn, 2000)

// Hook into focus events (native restoreTerminalModes happens
// before JS focus event, so this catches any restore)
renderer.on("focus", pasteOn)

// Hook into capabilities event (fires after async probing settles)
renderer.on("capabilities", pasteOn)
```

### Fix 3: Native restoreTerminalModes on Focus

OpenTUI's `focusHandler` (native) calls `restoreTerminalModes()` on focus regain **before** emitting the JS `"focus"` event. If the saved state doesn't have bracketed paste enabled, the restore undoes it.

The `capabilities` hook in Fix 2 covers this case — but only if the focus event retriggers capability probing. Some terminals don't re-probe on focus.

**Fix:** Combine Fixes 1 and 2. The three hooks (post-setup, capabilities, focus) together cover all timing scenarios.

## Debugging Workflow

### Step 1: Verify source of truth

When paste breaks, first check whether the source code changes are still in place — restart may have cleared hot-reload state:

```bash
grep -n "2004" src/index.tsx src/utils/terminal-reset.ts
```

### Step 2: Check how the TUI is launched

The TUI may run from source (dev mode) or compiled output. Check:

```bash
# How is the binary invoked?
which <binary>
readlink -f $(which <binary>)

# Is there a dist/ or build/ directory?
ls -la dist/ 2>/dev/null || echo "no dist"
```

If run via `bun run dist/index.js` or similar, the compiled output is stale — rebuild first.

### Step 3: Test OpenTUI's internal paste handling

OpenTUI's input parser handles paste events natively (see `handleStdinEvent`, case `"paste"`). If paste data reaches OpenTUI but isn't handled, the issue is in the key handler layer.

### Step 4: Test with raw escape sequences

Send bracketed paste test data manually:

```bash
# Send a bracketed paste sequence to the TUI process
echo -e '\x1b[200~test text\x1b[201~' > /proc/<PID>/fd/0
```

### Step 5: Check terminal emulator settings

Windows Terminal:
- `Ctrl+V` should be bound to `PasteFromClipboard` (default)
- `Ctrl+Shift+V` may also be bound — add it as a second binding
- `Ctrl+C` should NOT have `CopySelection` bound if you need Ctrl+C in the TUI

## Common Pitfalls

- **Source changes are correct but paste still broken after restart.** The running process may be a different binary (global install vs local dev). Check `which <binary>` and `readlink -f`.
- **Fix worked once then broke on restart.** Likely a build artifact issue (dev mode vs compiled mode) or OpenTUI caching native terminal state across process launches.
- **OpenTUI's native setupTerminal and JS escape sequences race.** The native layer runs synchronously inside `createCliRenderer()`, but capability queries are async. Always use the `capabilities` event hook.
- **`/dev/tty` vs `process.stdout` writes.** Some escape sequences need to go to `/dev/tty` directly (via `fs.writeSync`) rather than `process.stdout.write` to bypass OpenTUI's output buffer.
- **OSC 52 doesn't reach clipboard.** Check `xclip` or `xsel` on Linux/WSL. On macOS, OSC 52 should work natively through the terminal. On Windows Terminal, OSC 52 is supported since WT v1.x but may need the `clipboard` setting enabled.
- **`require("fs")` breaks in ESM modules.** Bun/ESM projects use top-level `import { writeSync } from "node:fs"`. `require()` throws a ReferenceError at module evaluation time — the issue isn't caught until you actually run the TUI and the paste handler is triggered.
- **setTimeout with 0ms doesn't catch late frames.** OpenTUI's native capability probes fire asynchronously and their response handlers may fire many frames later. Use 500ms and 2000ms as safety margins — anything under 100ms may still race.

## References

| File | What |
|------|------|
| `references/herm-bracketed-paste-fix.md` | Full debugging session: OpenTUI internals, exact fix code, regression notes |

## Verification

After applying fixes:

1. Kill and restart the TUI entirely (not just hot-reload)
2. Test all three paste methods: Ctrl+V, Ctrl+Shift+V, right-click
3. Test copy: Ctrl+Y or equivalent
4. If copy works but paste doesn't, bracketed paste is the issue
5. If paste works on first start but breaks on restart, check for stale build artifacts

## Related

- `debugging-hermes-tui-commands` — Hermes TUI slash command debugging (different codebase)
- `systematic-debugging` — general 4-phase root cause debugging methodology

## TUI Crash → Terminal Corruption Recovery

A TUI (yazi, herm, vim, htop) that crashes or is killed unexpectedly often leaves the terminal in raw mode. The user sees "random characters" (escape sequences as literal text) or their keyboard input appears garbled.

### Common causes

| Cause | Pattern | Example |
|-------|---------|---------|
| **TUI process killed** | `SIGKILL` or crash while in raw mode | `yazi` killed during file preview, `herm` crashed mid-render |
| **Binary file opened in TUI** | TUI tries to render binary as text | Opening a `.db`, `.zip`, or `.pdf` in `yazi`'s preview panel |
| **SSH session reconnect** | Buffered escape sequences replay | Disconnected SSH, reconnected to same session — old raw-mode output replays |
| **tmux state corruption** | tmux pane stuck in alternate screen | A pane exited a TUI but the alternate screen buffer wasn't restored |

### The "mms" pattern

When a process writes raw bytes to stdout (binary data or partial escape sequences), the terminal interprets them as characters. "mms", `~`, and other repeating characters are typical of a TUI that crashed while outputting frame data — the terminal receives mid-frame bytes that happen to decode as visible ASCII.

### Recovery commands

Try in order — each resets the terminal to a known good state:

```bash
# 1. Reset terminal driver (blind type — works even when screen is garbled)
reset

# 2. Alternative: sane terminal settings
stty sane

# 3. If inside tmux, kill the broken pane
# (within tmux): Ctrl+B, then type :kill-pane
# OR from outside: tmux kill-pane -t <session>:<window>.<pane>

# 4. If a process is actively spewing, find and kill it
ps aux | grep -E 'tail|watch|cat|loop' | grep -v grep
kill <PID>

# 5. Last resort — close SSH session and reconnect
exit
```

### Prevention

```bash
# Guard auto-launched TUI apps from stderr noise
# In ~/.bashrc or similar:
workbench 2>/dev/null

# Use tmux's remain-on-exit to catch crashes
tmux set -g remain-on-exit on
# Or per-pane: Ctrl+B :set remain-on-exit on

# Disable yazi's file preview if it keeps crashing on specific file types
# In ~/.config/yazi/yazi.toml:
# [preview]
# max_width = 0
# max_height = 0
# or: skip_files = ["*.db", "*.zip", "*.bin"]
```

### Quick triage

When a user says "my terminal is showing random characters":

1. Is this inside tmux? → Kill the pane, or `reset` inside it
2. Is this a direct SSH session? → `reset` then `stty sane`
3. Does it stop when you close and reopen? → Connection replay, not permanent
4. Does it keep happening after reconnect? → A process is auto-starting and spewing. Check `.bashrc`, `.profile`, systemd services

### Pitfalls

- **`reset` sends escape sequences too** — if the terminal is truly broken, `reset` output may also be garbled. Type it blindly and press Enter. The termios driver processes it in the kernel regardless of what the screen shows.
- **Don't confuse terminal corruption with SSH key issues** — if the "random characters" appear during SSH login (before the shell prompt), it's an SSH banner or motd issue, not a TUI crash.
- **`stty sane` fixes termios but not the display** — after `stty sane`, the terminal mode is correct but the screen may still look garbled. Run `reset` or `clear` to redraw.
- **When tmux reconnects to a crashed pane** — the pane's process is dead but the output buffer may still hold escape sequences. `reset -I` (initialize terminal) is more thorough than plain `reset`.
- **Multiple users on the same machine** — one user's broken terminal doesn't affect others. Each SSH session has its own termios state.
- **tmux `workbench` auto-launch pattern** — if `/usr/local/bin/workbench` starts `yazi` in a tmux pane, and `yazi` crashes on a file with terminal escape sequences in its content, the pane shows the corrupted output to every subsequent SSH login. Fix: remove the crashing TUI from the auto-launch, or add `2>/dev/null` guard. Refs: common workbench patterns at `engineering-discipline` and `references/` under that skill.