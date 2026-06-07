# Herm Bracketed Paste Triple-Fix

Resolved May 25, 2026.

## Symptom

Ctrl+Y (copy from herm via OSC 52) works, but Ctrl+V / Ctrl+Shift+V / right-click paste produces nothing. No garbage — paste data never reaches the composer.

## Root Cause

Three competing forces that disable bracketed paste mode (`\x1b[?2004h`):

1. **Startup reset disables it.** `resetTerminalModes()` sends `\x1b[?2004l` as part of its self-heal sequence (designed to clean up from a crashed prior process). This runs before anything else.

2. **OpenTUI's native `setupTerminal()` saves terminal state.** The Zig/WebAssembly layer inside `createCliRenderer()` queries the terminal for capabilities asynchronously. If the query runs before our `\x1b[?2004h` takes effect (escape sequences are buffered), it records "bracketed paste: disabled" and may restore that state later via `restoreTerminalModes()`.

3. **Native `restoreTerminalModes()` fires on focus *before* JS focus event.** OpenTUI's `focusHandler` (line 23016-23037 in index-jv9g79dk.js) calls `lib.restoreTerminalModes()` then emits the JS `"focus"` event. Our `renderer.on("focus", bump)` was always fighting one step behind.

## Fix Applied (3 changes, 2 files)

### File 1: `src/utils/terminal-reset.ts`
Changed `\x1b[?2004l` to `\x1b[?2004h` so the reset sequence enables bracketed paste instead of disabling it. This covers Fix 1 before OpenTUI ever initializes.

### File 2: `src/index.tsx`
Extracted `pasteOn` function and added three hooks:

```typescript
const pasteOn = () => {
  if (process.stdout.isTTY) process.stdout.write("\x1b[?2004h")
}

// 1. Immediate after createCliRenderer
bump()  // calls pasteOn internally

// 2. On focus (covers native restoreTerminalModes race)
renderer.on("focus", bump)

// 3. On capabilities event (covers async probing completion)
renderer.on("capabilities", pasteOn)
```

## OpenTUI Internals Discovered

| Code Location | What It Does |
|---|---|
| `index-jv9g79dk.js:22887` | `async setupTerminal()` — calls native `lib.setupTerminal()` |
| `index-jv9g79dk.js:22897` | `lib.setupTerminal(this.rendererPtr, ...)` — native Zig layer |
| `index-jv9g79dk.js:22989` | `_capabilities = lib.getTerminalCapabilities(...)` — captures terminal state |
| `index-jv9g79dk.js:22997` | `emit("capabilities", this._capabilities)` — fires after ASYNC probe |
| `index-jv9g79dk.js:23016-23037` | `focusHandler` — calls `lib.restoreTerminalModes()` BEFORE emitting `"focus"` |
│ `index-jv9g79dk.js:21816` | `stdout.write = ...` — in `capture-stdout` mode, hijacks stdout; in `passthrough` (alt-screen default), keeps original |

### OpenTUI Native Output Path

The native `lib.setupTerminal()` (Zig/WASM at line 22897) writes to the terminal via raw `write()` syscalls, NOT through `process.stdout.write()`. This means escape sequences sent via `fs.writeSync(fd, ...)` go through `write(2)` — the same kernel path as the native layer. But `process.stdout.write()` goes through Node's internal `Writable` stream buffering, which is a different kernel buffer path. The kernel guarantees ordering within a single fd for `write(2)` calls, but not between `write(2)` (native + writeSync) and `buffered write` (process.stdout.write).

## Second Session Fix (May 25, 2026 — Post-Restart Regression)

### Problem

Fix confirmed working in first session. After herm restart, paste broke again.

### Root Cause

The original fix used `process.stdout.write()` for the `pasteOn` function, but OpenTUI's native layer writes via raw fd. The two write paths aren't synchronized at the kernel level — `writeSync(fd)` goes directly to `write(2)` (same path as native), while `process.stdout.write()` goes through Node's `Writable` stream buffering. This caused a race condition on startup where OpenTUI's native sequences could reach the terminal before our `\x1b[?2004h` via `process.stdout.write`, even though our `writeSync(fd)` call happened chronologically first.

### Fix Applied (additions to original fix)

1. **Changed `pasteOn` to use `writeSync(fd)` instead of `process.stdout.write`.** This ensures our escape sequences use the same kernel fd path as OpenTUI's native layer, so the kernel guarantees ordering.

2. **Added `setTimeout(pasteOn, 500)` and `setTimeout(pasteOn, 2000)`.** OpenTUI's async capability probing (DA, DA2, XTVERSION exchanges) takes ~100-300ms. On slow WSL bridge connections, this can take even longer. The delayed re-assertions catch any late mode restores from response handlers.

3. **Added top-level ESM import** (`import { writeSync } from "node:fs"`) — `require()` doesn't work in Bun/ESM projects.

### Current Code (as of fix v2)

```typescript
import { writeSync } from "node:fs"

const pasteOn = () => {
  if (!process.stdout.isTTY) return
  const fd = (process.stdout as any).fd
  if (typeof fd === "number") {
    writeSync(fd, "\x1b[?2004h")  // direct kernel write — same path as native
  } else {
    process.stdout.write("\x1b[?2004h")
  }
}
pasteOn()
setTimeout(pasteOn, 500)
setTimeout(pasteOn, 2000)
renderer.on("focus", pasteOn)
renderer.on("capabilities", pasteOn)
```

## Compiled vs Source

Herm runs from source (`#!/usr/bin/env bun` → `src/index.tsx`). No `dist/` directory. The symlink chain:

```
~/.bun/bin/herm → ../install/global/node_modules/herm-tui/src/index.tsx
                                        ↓ realpath
                                  ~/herm/src/index.tsx
```

So source edits are live immediately — no build step needed.

## Regression on Restart (Still Open)

The fix was confirmed working in one session but reported broken after restarting herm in a fresh terminal session. Possible causes (unresolved):
- WT profile settings differ between terminal tabs/sessions
- Environment variables differ (TERM, WT_SESSION)
- Native OpenTUI Zig layer caches terminal state on first probe per process lifetime