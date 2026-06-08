---
name: hermes-agent
description: "Configure, extend, or contribute to Hermes Agent. Load ONLY when the user explicitly asks about configuring, extending, troubleshooting, or contributing to Hermes itself. Do NOT load for general task work, normal chat, or skill queries."
version: 2.3.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent

## User Interaction Style (Critical)
- Just-run triggers: "just run them", "dispatch all of them", "do all three", "execute immediately". Switch to execution mode. Do not add analysis, kanban cards, or extra menus.
- Re-reading loop: never re-propose actions already completed in the conversation. If in doubt, search past tool output first.

## Free-Tier Billing Hygiene
See `references/delegation-drift-fix.md` for the recurring failure modes: subagent 404s caused by empty `delegation.provider/model`, auxiliary credit drain when auto resolves to the paid provider, and how to normalize all profiles to the same free-tier stack.

**Billing troubleshooting pattern**:
- "Non-inference" charges are typically from gateway-managed services (browser-use, FAL image/video gen, some web tools) rather than LLM tokens.
- Check `use_gateway`, `cloud_provider`, `image_gen`, `video_gen`, and the `nous` provider block first.
- The `auxiliary:` section and `delegation:` block must be explicitly set to avoid fallback.

See `references/nous-portal-billing.md` for the full diagnostic tree from this session.