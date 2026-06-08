---
name: historian-vietnam-artifact-enforcer
description: "Board-level policy for historian-vietnam (Vstb Four Lenses). Forces artifact production verification on every card before it can be marked done."
version: 1.0.0
author: Jacob profile
tags: [kanban, artifact-enforcement, historian-vietnam, 4-lens]
---

# Historian-Vietnam Artifact Enforcer

This skill is automatically loaded for all cards on the `historian-vietnam` board.

## Enforcement Rules

1. Every card **must** produce at least one verifiable artifact (file, note, or structured output) before `kanban_complete` is accepted.
2. The worker must explicitly call the artifact verification step before marking a card done.
3. If no artifact is produced, the card is automatically blocked with reason "No artifact produced".
4. This rule applies to all new and existing cards on this board.

## Implementation

- Loads `artifact-enforcer` skill automatically.
- Adds output gate check in the worker loop.
- Prevents silent "done" states with zero output (the failure mode seen on t_25508b79, t_83c9f54e, t_d57835f7, t_26c850ae).

## Quality Standard for 4-Lens Analysis

When producing 4-lens deep analysis documents on the `historian-vietnam` board:

- Target length: 1,800–4,000 words per lens (not short summaries).
- Must contain 8–15 direct quotes from the primary source with line or chapter citations.
- Must explicitly address what the source emphasizes, omits, and the author's own historical moment.
- Must include a "Source Gaps" section.
- The `OutputGate` must be configured with `min_content_length=1500` for these tasks.

## Activation

This skill is now the default for the `historian-vietnam` board. All future cards will inherit it. Existing blocked cards will be re-evaluated against this rule.