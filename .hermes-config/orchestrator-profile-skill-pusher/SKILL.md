---
name: orchestrator-profile-skill-pusher
description: "Controlled one-way skill push from default (orchestrator) to isolated profiles. Audited, logged, research-skill only, user confirmation required. Preserves strict 5-profile isolation model."
version: 1.0.0
author: Default Orchestrator
license: MIT
category: devops
tags: [hermes, profiles, isolation, skills, orchestrator]
---

# Orchestrator Profile Skill Pusher

## Purpose
Allows the default orchestrator profile to push specific skills into isolated profiles (jacob, mike, euphy, etc.) without granting unrestricted access or reading from the target profile. All actions are one-way, logged, and require explicit confirmation.

## Constraints (enforced)
- Only skills in the `research` category or explicitly whitelisted.
- One-way only (default → target). Never reads from target profile.
- Every push is logged to `~/.hermes/orchestrator-audit.log`.
- User confirmation required before any file operation.
- Target profile must already exist (`hermes profile list`).
- No modification of SOUL.md, config, or memory — skills only.

## Usage
```bash
# From default profile
hermes skills run orchestrator-profile-skill-pusher --target jacob --skills historical-source-acquisition,book-hunting
```

Or via the skill in-session:
`/skill orchestrator-profile-skill-pusher target=jacob skills=historical-source-acquisition,book-hunting`

## Implementation Notes
- Copies the skill directory from `~/.hermes/skills/<skill-name>/` into `~/.hermes/profiles/<target>/skills/<skill-name>/`.
- Verifies the target profile directory exists before copying.
- Creates the profile skills directory if missing.
- Appends a timestamped entry to the audit log with source, target, skills, and outcome.
- On success, suggests running `hermes profile use <target>` to verify.

## Safety
- All operations use `cp -r` with explicit paths.
- No deletion or overwrite of existing files without confirmation.
- If the target profile has a `profile-guard-<name>` skill, the push is blocked unless explicitly overridden.

## Response Style Rules
- Avoid repetitive sign-offs or closing phrases (e.g., "The Hoang-Tham already burns in the vault").
- Ensure tool output is complete and the response is not cut off before delivering the final answer.
- The user finds repetition and incomplete responses annoying.

## Future Extensions
- Support for SOUL.md patches (read-only from source).
- Batch mode with kanban card output.
- Dry-run mode.

## Verification
After push, switch to the target profile and run:
`hermes skills list`

The pushed skills should appear.