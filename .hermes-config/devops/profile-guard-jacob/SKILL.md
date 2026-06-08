---
name: profile-guard-jacob
description: Enforces that all historian/Vietnam four-lens work runs exclusively inside the jacob profile. Checks active profile and blocks or warns if Vietnam research is attempted elsewhere.
tags: [jacob, vietnam, four-lens, profile, guard]
---

## Purpose
Prevents Vietnam research context pollution by ensuring all four-lens work, source extraction, and artifacts stay inside the jacob profile.

## When to Use
- Before any Vietnam/historian skill is loaded.
- At the start of any post-colonial Vietnam task.
- Auto-injected by vietnam-four-lens-workflow.

## Logic
1. Check if current profile is `jacob`.
2. If not, refuse and guide the user to switch to `jacob`.
3. If yes, proceed.

## Enforcement
- Do not create Vietnam artifacts outside jacob.
- Do not write Vietnam memory outside jacob.
- Do not run Vietnam cron jobs outside jacob.
- Do not read or write Vietnam session state outside jacob.

## Upgrade Rule
When new profile-owned types emerge (artifacts, scripts, sessions, cron, logs, memories, kanban), update this file rather than treating them as legacy exceptions.

## Bundled Reference
See `references/migration-state.md` for current per-profile state ownership.