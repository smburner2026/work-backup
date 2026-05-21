# C: Drive Walkthrough Session — 2026-05-16

## Folders reviewed and decisions
- adobeTemp: 2019-2020 ETR*.tmp folders — delete (stale Adobe installer debris)
- OneDriveTemp: empty SID folder — delete
- DumpStack.log.tmp: delete
- ProgramFilesFolder: empty — delete
- Intel: ExtremeGraphics (Jan 2020) + empty GfxCPLBatchFiles — delete entire folder
- ControlD: ctrld.exe 7.1 MB + toml — keep unless user confirms no longer using Control D DNS
- Games/Steam: 1.2 GB full client copy (old 2012-2017 DLLs mixed with recent) — redundant to /Program Files (x86)/Steam — delete
- $SysReset: AppxLogs, OldOS, MDM — conditional, verify no rollback needed
- $GetCurrent: Logs + SafeOS — conditional post-update

## Size artifacts noted
du repeatedly returned E (exabyte) sizes on AppData, Searches, Videos, OneDrive due to WSL reparse point handling of cloud-synced and junction folders. Never trust numeric size on those paths; inspect contents directly.

## Primary vs secondary confirmation pattern
- Always cross-check Steam location: presence of uninstall.exe and steam.exe in Program Files (x86) marks it primary.
- Games/Steam lacked uninstall.exe and contained older artifacts — clear secondary.

## WSL boundary reminder
Only access /mnt/c/ when user explicitly requests C: drive review. Default to /home/vthen/ otherwise.