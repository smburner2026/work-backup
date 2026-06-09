---
name: profile-isolation
category: devops
description: Enforces strict compartmentalization between Hermes profiles. Default behavior is full isolation unless the user explicitly requests cross-profile access.
---

# Profile Isolation

## Core Rule
**Default = complete isolation.** Never create symlinks, shared folders, or cross-profile backlinks between profiles unless the user explicitly confirms the desired linking model.

## When User Asks to "Link" or "Share" Vaults
Always clarify the exact model before acting:
- Intravault linking only (within one profile's vault)
- Cross-vault backlinks via symlinks
- Shared cross-vault folder
- Full isolation (no links at all)

The user has repeatedly and emphatically rejected cross-linking. When they say "no cross linking" or "intravault only", treat this as a hard constraint for that profile set.

## Profile Ownership (Current)
- mike: DABT work only
- euphy: librarian + artifact management only
- jacob (formerly historian): 4-lens historical / VSTB work only
- default: infrastructure, general maintenance, plugin/skill updates
- scraper: ingestion only

## Gateway Architecture (Unified Messaging)
When the user uses a single/shared Telegram + Discord account across profiles, run **only one gateway** under the default (orchestrator) profile. Do not start per-profile gateways in this case. The user explicitly prefers this model for simplicity while maintaining strict isolation.

Never route work across these boundaries without explicit approval.

## Pitfalls to Avoid
- Assuming "link the vaults" means creating shared folders or symlinks.
- Creating convenience symlinks without confirmation (user has rejected this multiple times).
- Treating profile renaming (historian → jacob) as creating orphans — always verify cron and reference cleanup.
- **active_profile drift:** `~/.hermes/active_profile` is the sticky profile selector. If this file contains a non-default name, every `hermes` TUI/terminal session boots into that profile — silently. After updates or gateway restarts, always verify `active_profile` is absent (canonical default state) or contains the intended profile. See `scripts/active_profile_guard.sh` for an automated drift guard.

## active_profile Mechanics
- **File absent** = default profile (canonical "hermes profile use default" state — it *deletes* the file, not writes "default")
- **File present with name** = that profile is used for every terminal/TUI session without explicit `-p` flag
- `hermes profile use <name>` writes to this file with an atomic rename
- `hermes profile use default` deletes the file entirely
- The main gateway process spawns profile-specific gateway children; the active_profile file determines which profile the TUI connects to

## Preventing Drift
Use the guard script at `scripts/active_profile_guard.sh` to detect and auto-correct drift. Schedule it as a cron job (every 30 min) to catch unintended changes:
```
cronjob create: "bash ~/.hermes/skills/devops/profile-isolation/scripts/active_profile_guard.sh" every 30m
```
The guard only acts when `active_profile` contains a non-default value — it stays silent otherwise.

## Related Patterns
- When consolidating profiles or moving artifacts, always confirm the new ownership boundary first.
- For Obsidian work, default to fully separate vaults unless the user specifies the linking style.
- After removing a profile, check for orphaned systemd services (`/etc/systemd/system/hermes-gateway-<name>.service`) and remove them.