---
name: terminal-workbench
description: "Set up a beginner-friendly terminal workbench on a Linux VPS — file browser (yazi) + agent TUI (herm/Hermes) side by side in tmux. Designed for non-CS users who need a visual file tree alongside their agent chat."
version: 1.1.0
author: Hermes Agent
platforms: [linux]
prerequisites:
  commands: [tmux, hermes]
metadata:
  hermes:
    tags: [vps, terminal, tmux, yazi, file-manager, workbench, beginner]
---

# Terminal Workbench

A one-command workbench that opens a tmux split-screen session with your agent TUI on one side and a terminal file browser (yazi) on the other.

## When to use

A user on a remote VPS wants to:
- Browse files alongside their Hermes chat session
- See directory trees without quitting the agent
- Avoid complex tmux keybinding learning curves
- Get a "Desktop-lite" experience in pure terminal

This skill is the full setup. Use it when setting up a new host/user.

## Communication level

This user has a non-CS background (bioscientist). When explaining any terminal concept, assume **high school / beginner level**:
- No assumed knowledge of tmux, multiplexers, split panes, or prefix keys
- Explain what each tool IS in one sentence before saying what it DOES
- Prefer concrete analogies over abstract descriptions (e.g. "like dividing a monitor into two screens" not "a terminal multiplexer multiplexes terminal sessions")
- Never use "simply" or "just" — if it were simple they wouldn't need explaining
- Tell them what they DON'T need to learn, not just what they need
- Flag the minimum viable knowledge (e.g. "you only need to know ONE command")

---

## Architecture

```
┌──────────────────────┬──────────────────────┐
│  herm/hermes --tui   │      yazi            │
│  (agent chat)        │  (file browser)      │
│                      │                      │
│  Left pane (50%)     │  Right pane (50%)    │
└──────────────────────┴──────────────────────┘
       ▲                          ▲
       │       tmux session       │
       └──────────┬───────────────┘
                  │
           SSH into VPS
                  │
            User's terminal
```

## Setup Steps

### 1. Install yazi

Yazi is a Rust-based terminal file manager with tree view, file previews, and vim-like navigation. Works great with tmux.

```bash
# Find latest release
curl -sL "https://api.github.com/repos/sxyazi/yazi/releases/latest" \
  | grep '"browser_download_url"' \
  | grep "x86_64-unknown-linux-gnu.deb"

# Download and install
wget -q -O /tmp/yazi.deb <URL>
dpkg -i /tmp/yazi.deb
apt-get --fix-broken install -y -qq  # resolves yazi deps
```

Yazi deps installed automatically: `file`, `fzf`, `fd-find`, `7zip`, `zoxide`, `jq`.

Optional but nice: `imagemagick` for image previews, `ripgrep` for text search.

### 2. Write a beginner tmux config

Key principles for non-CS users:
- **Mouse mode ON** — click to switch panes, drag to resize. No prefix key needed.
- **Alt+arrows** for keyboard switchers — no `Ctrl+B` prefix memorization.
- **Clean status bar** — hostname and time only, no clutter.
- **Escape-time 0** — removes the 500ms lag after Escape.

```bash
cat > ~/.tmux.conf << 'EOF'
# Mouse mode ON
set -g mouse on
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",*256col*:Tc"

# Simple status bar
set -g status-style "bg=#1a1b26,fg=#a9b1d6"
set -g status-left " #[fg=#7dcfff]#S #[default]"
set -g status-right "#[fg=#7dcfff] %H:%M #[default]"

# Alt+arrows switch panes (no prefix)
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Window navigation — Alt+[ and Alt+] for prev/next window
bind -n M-[ previous-window
bind -n M-] next-window

# Quick-open Yazi in a split pane from anywhere (Alt+Y)
bind -n M-y run-shell 'tmux split-window -h -l 40% "yazi"'
bind -n M-Y run-shell 'tmux split-window -h -l 40% "yazi ."'

# Larger scrollback
set -g history-limit 50000
set -sg escape-time 0
set -g base-index 1
EOF
```

### 3. Create the workbench script

This is the single entry point. It auto-creates or resumes the session.

```bash
cat > /usr/local/bin/workbench << 'SCRIPT'
#!/bin/bash
SESSION="workbench"
HERM_PATH="/root/.hermes/node/bin/herm"
BUN_PATH="/root/.bun/bin/bun"
WORK_DIR="/root/work"

tmux has-session -t "$SESSION" 2>/dev/null && {
  exec tmux attach-session -t "$SESSION"
}

tmux new-session -d -s "$SESSION" -c "$WORK_DIR"
tmux send-keys -t "$SESSION" "PATH=\"$HOME/.bun/bin:\$PATH\" $HERM_PATH" Enter

# Yazi file browser was removed — preview crashes on large/binary files
# left terminal corrupted on reconnect. See Pitfalls section.
exec tmux attach-session -t "$SESSION"
SCRIPT
chmod +x /usr/local/bin/workbench
```

> **Important:** Make sure the agent CLI (`herm` or `hermes --tui`) and `bun` (if needed by herm) are on PATH for non-interactive shells. Add to `~/.bashrc`:
> ```bash
> export BUN_INSTALL="$HOME/.bun"
> export PATH="$BUN_INSTALL/bin:$PATH"
> export PATH="$PATH:/root/.hermes/node/bin"
> ```

### 4. Verify

```bash
# Config
tmux -f /dev/null new-session -d \; source-file ~/.tmux.conf \; display-message -p "Config OK"

# Yazi
yazi --version

# Script creates session without errors
timeout 3 /usr/local/bin/workbench 2>/dev/null; tmux kill-session -t workbench 2>/dev/null

# herm accessible
PATH="$HOME/.bun/bin:$PATH" /root/.hermes/node/bin/herm --version
```

---

## Usage (for the user)

Once installed, the user has two ways to use it:

### Manual: one command

```bash
workbench
```

What happens:
1. If no `workbench` session exists → creates one with herm | yazi split
2. If session already exists → reattaches to it (survives SSH drops)
3. Left pane: agent chat. Right pane: file browser.
4. **Mouse works** — click either side, drag the divider
5. **Alt+arrows** — jump between panes without mouse
6. **Exit** — Ctrl+D/exit in both panes, or just disconnect (SSH reattach preserved)

### Auto-launch: zero commands

Add to the end of `~/.bashrc` to auto-start the workbench on every terminal/SSH login:

```bash
if [ -z "$TMUX" ] && command -v workbench &>/dev/null; then
    workbench 2>/dev/null    # stderr guard: yazi crash noise -> /dev/null
fi
```

This only fires on interactive shells (the `$PS1` guard at the top of `.bashrc` ensures this) and skips when already inside tmux to avoid nesting sessions.

### Yazi quick reference for user

| Key | Action |
|---|---|
| ↑↓ | Move through files |
| Enter | Open / enter directory |
| ~ | Toggle preview pane |
| Backspace | Go up |
| q | Quit |
| / | Search files |

---

## Variants

- **No herm installed?** Replace with `hermes --tui` in the script.
- **Prefer ranger over yazi?** Swap the command (ranger is older, slower, more dependencies).
- **Auto-launch on login?** See "Auto-launch: zero commands" in the Usage section above.
- **Boot-persistent (systemd)?** Instead of the workbench script, wrap the session in a systemd service so it starts on VPS boot automatically, without anyone SSHing in. See `devops/remote-agent-infrastructure` → section 3 (tmux) for the full service file pattern (`Type=oneshot + RemainAfterExit=yes`). For a 2-window setup (Window 1: Hermes, Window 2: shell/yazi), add an extra `ExecStart=/usr/bin/tmux new-window -t workbench -n files` after the Hermes window creation.
- **Want three panes?** Add another `split-window` for a terminal or log tail.
- **Windows user?** This works over any SSH client (Windows Terminal, WSL, PuTTY).

---

## Pitfalls

- **bun on PATH for non-interactive shells** — herm's launcher is a Node.js shim that execs `bun`. If bun isn't on PATH when tmux starts the pane, herm fails silently. Always set PATH explicitly in the script or .bashrc.
- **yazi deps** — the .deb pulls in heavy optional deps (imagemagick, 7zip, etc.). For a minimal server without image previews, consider installing yazi via a static binary instead.
- **mouse not working in SSH** — the SSH client must support mouse forwarding. Windows Terminal, iTerm2, and Kitty all do natively. PuTTY needs `Shift+click` to select text.
- **Alt+arrows captured by local terminal** — Windows Terminal may eat Alt+arrows for tab navigation. If so, user falls back to mouse clicks.
- **tmux nesting from auto-launch** — if the .bashrc auto-launch lacks the `[ -z "$TMUX" ]` guard, running `workbench` from inside an existing tmux session creates a nested tmux-in-tmux. Every SSH session that happens to share a shell will try to attach the same named session, causing conflicts. The guard prevents both issues.
- **Alt+[ / Alt+] captured by terminal** — some terminal emulators (GNOME Terminal, Windows Terminal) capture `Alt+[` for their own tab navigation. If window switching doesn't work in tmux, try `Ctrl+B 1` / `Ctrl+B 2` to jump directly to a window number. Or remap to unused keys in tmux.conf.
- **yazi crash leaves terminal corrupted** — yazi is a Rust TUI that switches to alternate screen mode. If it crashes while previewing a binary file, a large JSON dump, or any file whose preview triggers a segfault in the preview plugin, the terminal stays in raw mode. On reconnection (tmux or SSH reattach), the corrupted escape sequences render as random visible characters (e.g. "mms", garbled text). Fix: `reset` blind-typed into the broken session, or kill the tmux pane. To prevent recurrence:
  - Guard stderr in the auto-launch: `workbench 2>/dev/null` in .bashrc
  - Or remove yazi entirely and use a simpler file browser (e.g. `lf`, `nnn`) if preview crashes are persistent
  - Restart: `kill-session` → next SSH login creates clean session

---

## Yazi Theming (Flavors)

Yazi ≥26 uses **flavors** for theming (not theme.toml). Each flavor is a directory named `*.yazi/` containing a `flavor.toml` with all theme definitions.

> **Yazi default = dark blue directories on black** — notoriously hard to read. Installing a flavor is the fix.

### Install a flavor

`ya pack` may not be available (`pack` subcommand absent in older `ya` binaries). Fall back to manual clone:

```bash
git clone --depth 1 https://github.com/yazi-rs/flavors ~/.config/yazi/flavors
ls ~/.config/yazi/flavors/
```

### Activate a flavor

Create or edit `~/.config/yazi/yazi.toml`:

```toml
[flavor]
use = "catppuccin-mocha"  # no .yazi suffix
```

Yazi resolves this to `~/.config/yazi/flavors/catppuccin-mocha.yazi/flavor.toml`.

### Good flavors for readability

| Flavor | Background | Directory color | Notes |
|---|---|---|---|
| `catppuccin-mocha` | Dark (`#1e1e2e`) | Light blue (`#89b4fa`) | Best contrast — recommended |
| `catppuccin-macchiato` | Slightly lighter | Same palette | Good if you want slightly less contrast |
| `dracula` | Dark | Cyan | Nerdy, good readability |

### Verify

```bash
python3 -c "
import tomllib
with open('/root/.config/yazi/yazi.toml', 'rb') as f:
    print('yazi.toml:', tomllib.load(f))
with open('/root/.config/yazi/flavors/catppuccin-mocha.yazi/flavor.toml', 'rb') as f:
    d = tomllib.load(f)
    print('flavor sections:', len(d))
"
```

---

## Yazi Configuration

After installing and theming, configure Yazi's manager behaviour, previews, and file openers. A bare yazi.toml (just a flavor) means no hidden files shown, default sort order, system vi as the only opener.

### Manager settings

```toml
# ~/.config/yazi/yazi.toml
[manager]
ratio = [1, 4, 3]          # parent | current | preview column widths
show_hidden = true          # show .dotfiles by default
show_symlink = true
sort_by = "modified"        # newest files first
sort_reverse = true
linemode = "size"           # show file sizes in listing
scrolloff = 5

[preview]
max_height = 600
max_width = 1200
cache_dir = "/tmp/yazi-cache"
image_filter = "lanczos3"
```

### File openers (edit, read, open)

```toml
[opener]
edit = [
    { run = "vim '{path}'", block = true, desc = "Open in vim" },
]
read = [
    { run = 'bat -p --color=always "{path}"', block = true, desc = "View with bat" },
]
open = [
    { run = 'xdg-open "{path}"', desc = "Open with system default" },
]
```

- `edit` (Enter on a text file) → vim
- `read` (preview key) → bat for syntax-highlighted reading
- `open` (enter on a non-text file) → xdg-open for system default

### Optional: init.lua

Yazi ≥26 supports `~/.config/yazi/init.lua` for startup hooks. Useful for status bar customization or plugin setup:

```lua
-- ~/.config/yazi/init.lua
-- Show current directory path in the status bar
Status:children_add(function()
    if h ~= 0 then
        return ""
    end
    return ui.Line(" " .. tostring(cwd))
end, 500, Status.RIGHT)
```

### Shell aliases

Add to `~/.bash_aliases` (or `~/.bashrc`) for quick access:

```bash
alias y='yazi'                                 # Launch Yazi normally
alias yy='tmux send-keys -t workbench:2 "yazi" Enter'  # Launch in workbench window 2
```

`y` picks up where you last quit. `yy` sends Yazi to a dedicated shell window in the workbench session.

---

## Terminal Appearance Polish

After the workbench is running, the prompt and font are the next quality-of-life upgrades.

### 1. Starship prompt (install + configure)

```bash
# Install
curl -sS https://starship.rs/install.sh | sh -s -- -y

# Apply Tokyo Night preset (clean dark-theme layout with git info)
mkdir -p ~/.config
starship preset tokyo-night -o ~/.config/starship.toml

# Activate in bash (or fish/zsh)
echo 'eval "$(starship init bash)"' >> ~/.bashrc
```

The preset gives a multi-line layout: directory path → git branch → runtime info on line 1, then the cursor on line 2. No `user@host` noise.

To customise later: `$EDITOR ~/.config/starship.toml` or browse presets at [starship.rs/presets](https://starship.rs/presets).

### 2. Nerd Font (icons for Starship + Yazi)

Starship and Yazi use Nerd Font icons. If they render as blank squares, you need a patched font on the **client machine** (where the terminal emulator runs).

**On the VPS** (so the font is available for tools that check locally):

```bash
mkdir -p ~/.local/share/fonts
cd /tmp
curl -fLo "JetBrainsMono.zip" \
  "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip"
unzip -o JetBrainsMono.zip -d ~/.local/share/fonts/
fc-cache -f ~/.local/share/fonts/
```

**On the client** (where you see the terminal):

| Terminal | Setting |
|---|---|
| Windows Terminal | Settings → Profile → Appearance → Font face → `JetBrainsMono Nerd Font` |
| VS Code | `"terminal.integrated.fontFamily": "JetBrainsMono Nerd Font"` |
| Kitty | `font_family JetBrainsMono Nerd Font` in `kitty.conf` |
| Alacritty | `family: "JetBrainsMono Nerd Font"` under `font.normal` |

### 3. Verify everything works together

```bash
# Starship renders
starship module directory
starship module git_branch

# Font cache sees Nerd Font
fc-list | grep -i "NerdFont" | head -3

# Yazi starts and uses the flavor
yazi --version
```
