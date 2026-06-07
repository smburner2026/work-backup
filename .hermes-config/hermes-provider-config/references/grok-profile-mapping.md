# Grok Profile Mapping (User-Approved — June 2026)

User explicitly approved the following assignment after reviewing multiple iterations. This mapping respects persona, workload, and the preference for lighter models on soft profiles (especially Euphy).

## Final Mapping

- **default**: `x-ai/grok-4.3` (balanced flagship)
- **euphy**: `x-ai/grok-4.2-non-reasoning` (light — keeps warm, deferential, soft feminine style; user explicitly said Euphy does not need high-spec)
- **mike**: `x-ai/grok-4.2-reasoning` (strong reasoning for Socratic DABT tutor, first-principles, precision)
- **research**: `x-ai/grok-4.3` (maximum reasoning depth for four-lens historical analysis: Burckhardt, Nietzschean vitalism, class, covert/Luttwak)
- **scraper**: `x-ai/grok-4.2-non-reasoning` (efficient for mechanical scraping/extraction tasks; user explicitly approved)
- **worker**: `x-ai/grok-4.2-multi-agent` (optimized for kanban orchestration, background tasks, parallel streams)

## Update Commands Used (Verified Working)

```bash
hermes --profile <name> config set model.provider xai
hermes --profile <name> config set model.default <exact-grok-id>
```

## Key User Preferences Embedded
- **Profile-specific assignment is preferred** over uniform model across all profiles.
- **Lighter/non-reasoning models for soft or mechanical personas** (Euphy, scraper, worker).
- **High-reasoning or flagship (4.3) for intellectual depth** (mike, research).
- **Never reference deleted systems** (GBrain, PGLite, old deepseek mandates). User has removed the entire infrastructure. Any mention triggers frustration. This skill must actively prevent it.

This file is the canonical record. Future agents should consult it before suggesting model configurations.

Last updated: After user review of full conversation (Grok 4.3 confirmation, profile tweaks for mike/scraper, deletion of old GBrain system).