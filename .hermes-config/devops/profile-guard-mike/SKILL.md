---
name: profile-guard-mike
description: Enforces that all DABT work runs exclusively inside the mike profile. Checks active profile and blocks or warns if DABT work is attempted elsewhere.
tags: [mike, DABT, profile, guard]
---

## Purpose
Prevents DABT context pollution by ensuring all DABT skills, tasks, and artifacts stay inside the mike profile.

## When to Use
- Before any DABT skill is loaded.
- At the start of any DABT-related task.
- Can be auto-injected by the DABT project workflow.

## Logic
1. Check if current profile is `mike`.
2. If not, refuse and guide the user to switch to `mike`.
3. If yes, proceed.

## Enforcement
- Do not create DABT artifacts outside mike.
- Do not write DABT memory outside mike.
- Do not run DABT cron jobs outside mike.