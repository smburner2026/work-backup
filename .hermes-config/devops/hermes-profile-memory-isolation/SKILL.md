---
name: hermes-profile-memory-isolation
description: Design and implement strict per-profile memory isolation in Hermes (Mnemosyne profile_id + filtered views, o2b per-vault Brain/, or full DB splitting) while respecting user-enforced compartmentalization rules.
---

# Hermes Profile Memory Isolation

## Core Principle
Every memory fact, preference, instruction, and timeline entry must be permanently scoped to exactly one profile (mike, euphy, jacob, or default). Cross-profile leakage is never acceptable.

## Decision Matrix
- Use `profile_id` column + filtered views when staying with single Mnemosyne DB (lightest migration).
- Use o2b `Brain/` folders inside each profile's existing Obsidian vault when deterministic consolidation and Markdown editability are priorities.
- Use full per-profile Mnemosyne DB files only when maximum isolation is required and migration cost is accepted.

## Implementation Patterns
- Add `profile_id TEXT` column + indexes to facts, instructions, preferences, timelines.
- Create read-only views (`mike_facts`, `euphy_facts`, etc.).
- Modify `mnemosyne_remember`, `mnemosyne_recall`, `mnemosyne_sleep`, and graph tools to default to or require the active profile context.
- Backfill existing data using session context or manual tagging.

## References
- See `references/profile-memory-patterns.md` for concrete SQL and tool patch examples from real sessions.
- See `references/isolation-audit-checklist.md` for verification steps.

## Anti-Patterns
- Never create cross-vault symlinks or shared folders.
- Never allow a global consolidation pass to mix profiles.
- Never repeat work already done in a profile-specific context.