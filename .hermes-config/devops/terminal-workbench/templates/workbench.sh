#!/bin/bash
# workbench — Hermes CLI in tmux
# Opens a tmux session with herm (chat) on the left pane.
# Run 'workbench' to start or resume.
# ---
# Configurable:
SESSION="workbench"
HERM_PATH="/root/.hermes/node/bin/herm"
BUN_PATH="/root/.bun/bin/bun"
WORK_DIR="/root/work"

# Attach if already running
tmux has-session -t "$SESSION" 2>/dev/null && {
  echo "→ Resuming workbench session..."
  exec tmux attach-session -t "$SESSION"
fi

# Create fresh session
tmux new-session -d -s "$SESSION" -c "$WORK_DIR"

# Left pane: herm (agent chat CLI)
tmux send-keys -t "$SESSION" "PATH=\"$HOME/.bun/bin:\$PATH\" $HERM_PATH" Enter

# Yazi file browser was removed from this template — preview crashes on
# large/binary files leave terminal corrupted on reconnect. To re-add:
#   tmux split-window -h -t "$SESSION" -c "$WORK_DIR"
#   tmux send-keys -t "$SESSION" "yazi" Enter
#   tmux select-layout -t "$SESSION" even-horizontal

exec tmux attach-session -t "$SESSION"
