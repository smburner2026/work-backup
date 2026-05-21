# Program Files & Related Findings (2026-05-16)

## Verified via web_search

- **WindowsInstallationAssistant**: Official Windows Update feature upgrade tool. Leaves empty folder after update completes. Safe to delete.
- **RUXIM**: Microsoft Reusable UX Interaction Campaign Scheduler used by Windows Update. Official component. Do not delete.
- **BCUninstaller**: Bulk Crap Uninstaller — legitimate third-party bulk uninstall tool. Keep if used.
- **DeleteEmptyFolders**: Small Explorer context-menu utility. Matches installer seen in Downloads. Not bloat.
- **Dell**: Dell support/driver utilities. Bloat only if user no longer owns Dell hardware.
- **NordUpdater**: NordVPN update service. Keep if VPN is active.
- **.openjfx**: JavaFX native library cache (151 MB of DLLs). Pure cache — safe to delete, will be recreated.

## High-risk items confirmed
- LastGood.Tmp (502 MB under Windows): Last Known Good recovery snapshot containing system32 copies. Never delete.

## Tool usage pattern
After manual cleanup of Program Files, run the installed DeleteEmptyFolders utility in review mode on both Program Files and Program Files (x86) before committing deletes.