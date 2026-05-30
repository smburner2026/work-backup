# WSL Cron Auto-Start via Windows Startup Folder

Ensures WSL's cron service restarts automatically after every Windows reboot or login, so HMS sync jobs keep firing without manual intervention.

## The Problem

WSL with systemd marks cron as `enabled`, but the init sequence doesn't reliably restart it after a full Windows reboot. The cron daemon stays dead until you run `sudo service cron start` manually. Since HMS auto-sync and push jobs are cron-triggered, this means sync silently stops after every reboot until you notice.

## The Fix

A VBScript in the Windows Startup folder runs `wsl.exe -d Ubuntu -u root service cron start` with a hidden window at every login. No console flash, no manual step.

## VBScript Template

Save this as `start_wsl_cron.vbs`:

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "wsl.exe -d Ubuntu -u root service cron start", 0, False
```

Parameters:
- `0` — window style: hidden (no terminal window appears)
- `False` — don't wait for the command to finish (fires and forgets)

## Deployment

```powershell
# Find your Startup folder
$startup = [Environment]::GetFolderPath('Startup')
Write-Output $startup
# → C:\Users\<you>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

# Create the VBScript there
@"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "wsl.exe -d Ubuntu -u root service cron start", 0, False
"@ | Out-File -FilePath "$startup\start_wsl_cron.vbs" -Encoding ASCII
```

Or from WSL directly:

```bash
# Write to the Windows filesystem via /mnt/c/
startup="/mnt/c/Users/vthen/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
cat > "$startup/start_wsl_cron.vbs" << 'VBS'
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "wsl.exe -d Ubuntu -u root service cron start", 0, False
VBS
```

## Verify

1. Reboot Windows (or just log out/in)
2. Open WSL terminal and check: `sudo service cron status`
3. Should show `Active: active (running)`

## Notes

- Uses `-u root` because `service cron start` needs root. If your default WSL user has passwordless sudo, you can omit `-u root` and use `sudo service cron start` instead.
- Distro name: replace `Ubuntu` with your actual distro (`wsl -l -q` to list).
- The VBS runs at every user login (not system boot). If the user's session auto-logs in, this is effectively the same timing as boot.
- Fallback: a `.bat` file with `start /min wsl.exe ...` also works but briefly flashes a console window.
