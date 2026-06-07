# Windows Desktop and File Extension Quirks (Discord Bot Context)

## OneDrive Desktop Redirection
Many Windows users have their Desktop folder redirected through OneDrive.
- Normal path: `C:\Users\<username>\Desktop`
- OneDrive path: `C:\Users\<username>\OneDrive\Desktop`

Always use the path visible in File Explorer Properties or the full path in the python command. `cd Desktop` will fail when OneDrive is active.

## Notepad Save Trap
When saving from Notepad:
- Default "Save as type" = Text Documents (*.txt)
- Result: `bot.py.txt` (hidden extension on many systems)
- Fix: Change to "All Files" before clicking Save

This is the #1 reason for "file not found" after following Notepad instructions.

## Recommended Run Command
Use the absolute path every time:

```
python "C:\Users\<username>\OneDrive\Desktop\bot.py"
```

or

```
python "C:\Users\<username>\Desktop\bot.py"
```

Never start with `cd` when helping non-technical users on Windows.
