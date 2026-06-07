---
name: discord-bot-windows-setup
description: End-to-end Discord bot creation and first-run on Windows for users with no programming background. Covers Developer Portal, Python install, token handling, file creation pitfalls, and reliable execution.
triggers:
  - User wants to make a Discord bot work on Windows
  - Bot shows in server but stays offline/inactive
  - Python/pip not found or file not found errors during setup
---

# Discord Bot Setup on Windows (Non-Technical Users)

## Core Flow
1. Python installation (official installer with PATH)
2. Discord Developer Portal: create Application → add Bot → copy token (or Reset Token)
3. Notepad file creation with explicit "All Files" save
4. Execution using full absolute path (never rely on `cd`)
5. Keep terminal open for the bot to stay alive

## Critical Windows-Specific Pitfalls
- **OneDrive Desktop redirection**: Many users have Desktop at `C:\Users\<name>\OneDrive\Desktop`. Always use the full path shown in File Explorer.
- **Notepad default extension trap**: If "Save as type" is left on Text Documents, the file becomes `bot.py.txt`. Force "All Files".
- **Token visibility**: Tokens are shown only once. Reset Token is the only recovery.
- **Application vs Bot confusion**: Creating an app does not automatically create a bot. Must explicitly click "Add Bot" in the Bot tab.
- `cd Desktop` frequently fails; use absolute paths in the run command instead.

## Verification
After `python "full\path\to\bot.py"` the terminal must show:
- "logging in using static token"
- "Shard ID None has connected to Gateway"
- "Bot is online as ..."

If any of those lines are missing, the bot is not connected.

## Template
See `templates/bot.py` for the minimal working starter.
