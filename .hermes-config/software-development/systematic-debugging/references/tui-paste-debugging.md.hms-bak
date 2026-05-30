# TUI Paste Debugging

## Pattern

Paste (Ctrl+V, Ctrl+Shift+V, right-click) doesn't insert text in a raw-mode TUI app, but works in other terminal apps like the official Hermes TUI.

## Root Cause

**Bracketed paste mode (`DEC 2004`) is disabled** — either never enabled at startup, or explicitly turned off by a terminal-reset function and never re-enabled.

Without bracketed paste, the terminal emulator (Windows Terminal, kitty, etc.) sends clipboard content as raw character bytes rather than wrapped in `\x1b[200~`…`\x1b[201~` markers. The TUI framework never receives a `PasteEvent`, so:
- The textarea's `onPaste` handler never fires
- Rich paste handling (image detection, path detection, paste-collapse for large pastes) is dead
- Raw bytes may confuse the keyboard input parser (control chars dropped, escape sequences misinterpreted)

## Investigation Steps

### 1. Check for bracketed paste enable/disable in the codebase

```bash
# Find where bracketed paste is explicitly controlled
rg "2004[hl]" src/
rg "2004" node_modules/@opentui/core/ --include "*.js"
```

Look for:
- Terminal mode reset functions on startup (often named `resetTerminalModes`, `terminalReset`, `initTerminal`)
- Startup self-heal code that blindly disables all terminal modes
- Whether the TUI framework re-enables bracketed paste after initialization

### 2. Check startup order

```
resetTerminalModes()        ← sends \x1b[?2004l (DISABLE)
    ↓
createCliRenderer()         ← OpenTUI/Ink init (may not send \x1b[?2004h)
    ↓
... framework ready
```

If bracketed paste is disabled *after* the framework initializes, or the framework doesn't enable it, paste is broken.

### 3. Compare against a working reference (official Hermes TUI)

The official Hermes TUI (Ink-based, in `ui-tui/`) explicitly enables bracketed paste at startup:

```ts
// ui-tui/src/app/useMainApp.ts
const BRACKET_PASTE_ON = '\x1b[?2004h'
if (stdout.isTTY) {
    stdout.write(BRACKET_PASTE_ON)
}
```

It also detects paste markers in the input stream:

```ts
// packages/hermes-ink/src/ink/termio/csi.ts
export const PASTE_START = csi('200~')
export const PASTE_END = csi('201~')
```

### 4. Check keybinding catalog for Ctrl+V

If Ctrl+V is bound to a global action (e.g. `clipboard.attach` for image paste), the global key handler consumes it before the textarea sees it:

```ts
// keys/catalog.ts — look for ctrl+v binding
"clipboard.attach":  def("ctrl+v", "Attach clipboard image", "global"),
```

In `useAppKeys`, this match calls `key.stopPropagation()`, starving the textarea of the paste keystroke. Text paste via Ctrl+V is impossible regardless of bracketed paste mode.

### 5. Test bracketed paste mode live

```bash
# In a TUI session, enable bracketed paste manually:
printf '\x1b[?2004h'
# Then try Ctrl+Shift+V or right-click paste
```

If paste starts working after this, the fix is to enable bracketed paste in the app's startup sequence.

## The Fix

Add bracketed paste re-enable **after** the TUI framework initializes, patterned after the official Hermes TUI:

```ts
// Re-enable bracketed paste mode — required for textarea onPaste events
if (process.stdout.isTTY) {
    process.stdout.write('\x1b[?2004h')
}
```

Also add it on a focus event handler so it re-asserts after terminal suspension:

```ts
renderer.on("focus", () => {
    if (process.stdout.isTTY) {
        process.stdout.write('\x1b[?2004h')
    }
})
```

If Ctrl+V needs to paste text (not just images), either:
- Unbind `clipboard.attach` from `ctrl+v` (move to `ctrl+shift+v` or `<leader>v`)
- Or make the paste handler detect text vs image in the clipboard

## Verify the Fix

After applying the changes, confirm nothing is stale:

### 1. Check what binary actually runs

A globally-installed Bun binary may be a symlink. Verify the source edited matches where the binary reads from:

```bash
# Resolve the actual path
realpath $(which herm)
# Check process started after edits
ps -p $(pgrep -f herm) -o lstart,etime
```

### 2. Check for cached/stale compilation

Bun runs `.tsx` files directly and does NOT cache compiled output for `bun run` (unlike `bun build`). If the source file changed before the process started, the new code is live. Restart the TUI to pick up edits — watch mode (`bun run --watch`) auto-reloads.

### 3. Test from the user's actual running session

Ask the user to test the key combination in the currently running TUI, not a new terminal. If the user restarted the app (new terminal tab) but the old process is still running, they're testing the old code.

## Investigation — Additional Checks

### 6. Check the actual binary vs source directory

Bun global installs (`bun install -g`) create a symlink from `~/.bun/bin/<name>` → `~/.bun/install/global/node_modules/<pkg>/src/index.tsx`. This may or may not resolve to the same directory as the local git clone:

```bash
realpath ~/.bun/bin/herm
# → ~/.bun/install/global/node_modules/herm-tui/src/index.tsx
# → /home/user/herm/src/index.tsx  (if symlink-farmed)
```

If the global install is a copy (not a symlink), edits to the source directory are invisible to the running binary. Verify:

```bash
# Check if global install is same directory as git repo
realpath ~/.bun/install/global/node_modules/herm-tui
realpath ~/herm
# Compare directory listings (should match)
```

### 7. Check Windows Terminal keybindings

Windows Terminal's `settings.json` can override `Ctrl+V` and `Ctrl+Shift+V`, intercepting them before they reach the TUI. Both may be bound to `Terminal.PasteFromClipboard`, which creates ambiguity:

```json
"keybindings": [
    {"id": "Terminal.PasteFromClipboard", "keys": "ctrl+v"},
    {"id": "Terminal.PasteFromClipboard", "keys": "ctrl+shift+v"}
]
```

Check the actual settings:

```bash
cat /mnt/c/Users/*/AppData/Local/Packages/Microsoft.WindowsTerminal*/LocalState/settings.json 2>/dev/null
```

If `Ctrl+V` is also bound to paste, unbinding `clipboard.attach` from `ctrl+v` in the TUI's key catalog has no effect — WT handles the keystroke before the TUI sees it. The paste still works (WT sends bracketed content), but the TUI never sees a raw `Ctrl+V` keystroke.

### 8. Check native clipboard tools (for COPY, not paste)

When copy (Ctrl+Y) targets the OS clipboard, the TUI may use:
- **OSC 52** — escape sequence `\x1b]52;c;base64\x07` written to stdout — handled by the terminal emulator
- **Native tools** (fallback) — xclip, xsel, wl-copy, pbcopy, clip.exe

Verify what's available:

```bash
which xclip xsel wl-copy 2>/dev/null
```

In WSL, `xclip`/`xsel` are often missing. If the TUI is in a terminal emulator that supports OSC 52 (Windows Terminal does and is detected via `WT_SESSION`), the OSC 52 path alone should work — but only if `process.stdout.write()` actually reaches the terminal.

### 9. Verify OpenTUI stdout passthrough mode

OpenTUI does NOT hijack `stdout.write` in default (alt-screen) mode. The `_externalOutputMode` defaults to `"passthrough"` for alt-screen mode, meaning `stdout.write` stays as the original function:

```js
// In CliRenderer constructor:
this.realStdoutWrite = stdout.write;
// Later:
this.stdout.write = externalOutputMode === "capture-stdout"
  ? this.interceptStdoutWrite
  : this.realStdoutWrite;  // passthrough — write goes directly to fd
```

This means OSC 52 escape sequences for copy, and `\x1b[?2004h` for bracketed paste, DO reach the terminal emulator when written via `process.stdout.write()`. If they're not working, the issue is NOT stdout hijacking — look elsewhere (terminal support, timing, capability detection).

### 10. OpenTUI's built-in clipboard API

OpenTUI has its own clipboard methods via the native renderer:

```js
renderer.clipboard.copyToClipboardOSC52(text, target)
renderer.clipboard.isOsc52Supported()
```

If the TUI's custom `clipboard.ts` implementation isn't working (e.g. herm's hand-rolled `process.stdout.write(osc52)`), it may be worth switching to OpenTUI's native API, which:
- Goes through the native renderer output pipeline directly
- Has capability detection built in  
- Avoids potential interleaving with the render loop

### 11. Check bracketed paste capability detection

OpenTUI tracks `bracketed_paste` as a terminal capability via FFI:

```js
// TerminalCapabilitiesStruct
["bracketed_paste", "bool_u8"],
["osc52", "bool_u8"],
```

The TUI can query `renderer.capabilities?.bracketed_paste` to know if the terminal reported support. Some TUI frameworks will refuse to emit `PasteEvent` if this capability isn't detected.

## OpenTUI-Specific Debugging

- OpenTUI's stdio parser (embedded native code in `@opentui/core`) recognizes bracketed paste start marker `\x1b[200~` on line 7636 of the bundled JS and creates a paste collector.
- On paste end marker `\x1b[201~`, it emits a `PasteEvent` with the collected bytes.
- This flow is entirely independent of the TUI's React component tree — it works at the raw stdin parser level.
- If paste bytes reach the terminal but are not wrapped in `\x1b[200~`/`\x1b[201~`, the parser treats them as typed input.

## Common Pitfall: Timing of Bracketed Paste Re-enable

The most common failure mode: the startup sequence sends multiple mode resets, and the bracketed paste enable lands before one of them:

```
resetTerminalModes()        ← \x1b[?2004l (DISABLE)
    ↓
native setupTerminal()      ← may also send \x1b[?2004l (DISABLE)
    ↓
\x1b[?2004h (ENABLE)        ← our fix — but does it race?
    ↓
root.render()               ← render loop starts
```

If OpenTUI's native `setupTerminal` also sends `\x1b[?2004l`, it resets after our enable. Confirm by adding the enable **after** `setupTerminal` returns and verifying no later reset overwrites it. A focus-event handler (`renderer.on("focus", ...)`) can re-assert on each focus cycle.

## Platform Notes

- **Windows Terminal**: Always sends clipboard content on paste actions (Ctrl+V, Ctrl+Shift+V, right-click). With bracketed paste ON, content is wrapped in `\x1b[200~`…`\x1b[201~`. With bracketed paste OFF, content is sent as raw bytes. Windows Terminal IS in OpenTUI's OSC 52 allowlist — `shouldUseNativeClipboard()` returns false for it, so copy relies solely on OSC 52.
- **WSL**: The clipboard bridge (`clip.exe`) is available separately for copy-out, but paste-into-terminal is handled by Windows Terminal's paste action, not `clip.exe`. `xclip`/`xsel` are NOT pre-installed in WSL — if OSC 52 fails, copy silently fails too.
- **kitty/Alacritty**: Similar behavior — bracketed paste mode controls whether paste is wrapped in markers.
- **tmux**: Has its own paste buffer and may handle bracketed paste independently. TMUX also wraps OSC 52 sequences in tmux passthrough (`\x1bPtmux;\x1b...\x1b\\`).
