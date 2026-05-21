---
name: hermes-soul-design
description: "Understanding, explaining, inspecting, and working with Hermes Agent SOUL.md files — including personality rubrics, dual skill chains, prompt compression, and the soul file architecture."
version: 1.3.0
---

# Hermes Soul Design

This skill governs sessions where the user wants to **study, inspect, or understand** how Hermes souls are structured, where they live, and how they work. Covers both explanatory mode (pure understanding) and practical navigation (finding and reading soul files).

## Interaction Rules — Study & Inspect Mode
- When the user says variations of "explain", "help me understand", "I want to learn", or "don't edit / no changes", switch to pure explanatory mode.
- When the user says variations of "look at", "show me", "open", "inspect", "what's in" the soul, switch to practical navigation mode.
- Provide clear breakdowns of structure, components, and design decisions.
- Do NOT propose edits, refinements, or improved versions unless explicitly asked.
- Focus on teaching the existing approach and its rationale.

## Interaction Rules — Design & Build Mode
- When the user asks to "edit", "rewrite", "customize", "update", "name", or otherwise modify their soul, switch to design mode.
- Design mode covers: creating new souls, rewriting existing ones, merging external influences, or adding persona layers.
- Before proposing any rewrite, first inspect the current SOUL.md and ask what changes the user wants.
- Follow the Compressed DSL Format Guide below — the proper format uses the dense Hermes dialect, not loose prose.
- After writing a new soul, always verify all requested layers are present by re-reading the file.

## Four-Layer Architecture Pattern

Souls can be built in layers that each serve a distinct function. The canonical four-layer architecture, ordered from foundation to surface:

| Layer | Purpose | Example | Immutable? |
|-------|---------|---------|------------|
| **0. Charter** | Constitutional rules, governance, agent-user relationship | Operating Charter (stance, accountability, pushback, autonomy, mission) | Yes — permanent once set |
| **1. System** | Hermes architecture, loops, memory, tools, platform rules | AGENT/LEARN loops, HERMES-KB, ExecPrinciples, compression | Yes — permanent once set |
| **2. Discipline** | Behavioral principles, coding rigor, decision rules | Karpathy CLAUDE.md (think, simplify, surgical, verify) | Yes — permanent once set |
| **3. Persona** | Voice, tone, posture, aesthetic, temperament | Costin (aristocrat-artist-scientist, BAP×HM edge) | **No** — the only swappable layer |

**Key rule:** Layers 0, 1, and 2 are permanent once agreed. Only Layer 3 (the persona mask) changes when the user wants a different voice. The operating constitution, the system architecture, and the behavioral discipline stay anchored.

See `references/four-layer-soul-pattern.md` for the full pattern documentation with format guides for each layer.

## Compressed DSL Format Guide

The proper Hermes soul format uses a dense, zero-whitespace DSL. Key conventions:

**Role declaration:** `***Name*** adopts the role of ***Name***, a [archetype description]. Traits: [compressed comma-separated]. NOT [chatbot|IDE|copilot] wrapper.`

**Personality Rubric:** `PersRubric: O:score/C:score/E:score/A:score/N:score — Trait:score/Trait:score/...`
- OCEAN scores (0-100), then custom facet scores separated by `/`
- For the Costin archetype: lower A (~30, not mean but unrestrained), higher O (~85), include WillToShock and Uninhibited facets

**External principles:** `**SourceName**: 1.RuleName—Detail 2.RuleName—Detail...`
- Use bold heading, colon, then compressed numbered rules with em-dash separators

**Dual loops:** `[AGENT]:Assess—1a.Parse🎯Intent—1b.Scope🔍Tools—1c.ChkCtx📋State→[chain continues]`
- Use [AGENT] and [LEARN] as section headers
- Each step: number.letter.EmojiStepName
- Arrow `→` for flow transitions, em-dash `—` for step separators
- See the master soul at `~/.hermes/SOUL.md` for a live example

**System knowledge:** `HERMES-KB: [compressed key-value pairs using pipes, arrows, and curly-brace maps]`
- Concise, factual, all on one line. Use `=` for definitions, `→` for flows, `|` for alternatives, `{}` for structured maps

**Execution principles:** `ExecPrinciples: [colon-separated directives using >,→, hash-like pairs]`

**Complex task:** `COMPLEX_TASK: Use OMNICOMP when useful. ChainConstructor{...}→ChainSelector{...}→SkillgraphMaker{...}→[SKILLGRAPH]`

## Charter Integration Patterns

When the user wants to add a Layer 0 (Operating Charter) to an existing soul:

1. **Do NOT rewrite and present a finished draft.** The charter template is a starting point, not a final document. Walk through each section with the user.
2. **Expect heavy trimming.** The user will cut redundancies, tighten language, and remove anything that doesn't fit their register. Let them edit inline.
3. **Open with the right formula:** "You are [Name], my autonomous operator." — NOT "thought partner" or "assistant."
4. **Check for redundancy with Layer 1.** The charter's Stance, Standards, and Accountability sections may cover the same ground as ExecPrinciples. If they do, remove ExecPrinciples from Layer 1. The charter takes precedence.
5. **Verify against existing layers after editing.** The charter should not conflict with or duplicate Layers 1–3.
6. **Call the edit:** "walk through section by section" — each section gets discussed, edited, and approved before moving to the next.
7. **Drop the Tone section.** If the user asks about it, explain that voice, register, and aesthetic belong to the persona layer (Layer 3). The charter should not duplicate or constrain it.
8. **For general-purpose agents, leave Mission blank.** The section is scaffolding for specialist profiles — fill it only when there's a fixed mission.
9. **Verify after write.** After writing any new soul to `~/.hermes/SOUL.md`, always re-read the file and confirm every requested layer is present. Do not trust write confirmation alone — confirm by reading the file back.

See `references/operating-charter-template.md` for the full template to use as a starting point in charter design sessions.

## External Influence Integration

When merging external influence files (e.g., Karpathy's CLAUDE.md, custom instruction sets) into a soul:

1. **Extract the core principles** — don't inline the entire external file verbatim
2. **Compress them** into the `**SourceName**:` format under a new heading in the soul
3. **Cross-reference in guardrails** — add a `SourceName check:` line to the self-reminder section
4. **Overlay in ExecPrinciples** — add a "SourceName overlay:" line setting behavioral bias
5. **Classify the layer:** Coding behavior → Layer 2 (Discipline). Expression style → Layer 3 (Persona).

## Soul Architecture Overview

See `references/soul-architecture.md` for the full file-level anatomy. Quick reference:

| Component | Location | Notes |
|-----------|----------|-------|
| Master soul | `~/.hermes/SOUL.md` | Active persona (profile-dependent) |
| Profile souls | `~/.hermes/profiles/<name>/SOUL.md` | Per-profile persona override |
| Default template | `hermes_cli/default_soul.py` | Seeded on first run |
| Docker soul | `docker/SOUL.md` | Template in repo |
| Compressed soul refs | `skill:soul-compression/references/` | Example souls (aristocrat, euphy, etc.) |

**Key semantics:** SOUL.md is reloaded every message — no restart needed. Deleting it or clearing its contents reverts to the built-in default. The soul is not referenced from `config.yaml` — it's a standalone file in `HERMES_HOME`. Profile switching via `hermes profile switch <name>` activates that profile's SOUL.md.

## Key Concepts to Explain
- Four-layer soul architecture (Charter → System → Discipline → Persona)
- Dual execution + learning loops ([AGENT] and [LEARN])
- Numeric personality rubrics (OCEAN + custom facets)
- Embedded knowledge bases (HERMES-KB)
- Prompt compression techniques (structural compression, token packing, semantic normalization, DSL encoding)
- Self-referential guardrails
- Profile-isolated souls (each profile gets its own SOUL.md)
- Immutability rule: Layers 0–2 permanent, Layer 3 swappable

## Compression Techniques Reference
See `references/prompt-compression-techniques.md` for the four main methods observed in dense Hermes souls (structural compression, token packing, semantic normalization, and DSL encoding).

## Soul Architecture Reference
See `references/soul-architecture.md` for file locations, generation mechanism, loading semantics, and profile binding.

## Profile Worker Configuration Reference
See `references/profile-worker-configuration.md` for making a profiled soul actually *functional* — the toolset setup, model/auth verification, and pitfalls that turn a persona file into a working agent the kanban dispatcher can spawn. Profiles need more than a SOUL.md, and this reference covers what's missing.

## Operating Charter Template
See `references/operating-charter-template.md` for the reusable Layer 0 template.

## When to Use
- User shares a SOUL.md and asks for explanation
- User says "let's look at the soul" or "show me the master soul"
- User says "I want to design/rewrite/edit/customize my soul" or "give me a name"
- User says "merge this into my soul" or "add these principles to the soul"
- User says "let me walk you through my operating charter" or shares a governance document
- User asks about multiple souls or profile-specific souls
- User shares compression macros or DSL patterns and wants them decoded
- User is studying how to read or maintain complex agent personalities
- User asks about the relationship between SOUL.md, profiles, and config

## Inspection Pattern
When the user wants to see their active soul:
1. Check `~/.hermes/SOUL.md` for the master soul
2. If the user mentions a specific profile, check `~/.hermes/profiles/<name>/SOUL.md`
3. To see available profiles: `search_files path=~/.hermes/profiles pattern="SOUL.md" target=files`
4. For compressed soul examples: `skill_view name=soul-compression` then check its `references/` directory

## Anti-Patterns
- Do not default to editing or optimizing the soul
- Do not assume the user wants improvements when they say "explain" or "learn"
- You can only call memory and skill management tools. Other tools will be denied at runtime — do not attempt them.
- When the user says "add this to [profile name(s)] too" for Layer 0, find each profile's SOUL.md at `~/.hermes/profiles/<name>/SOUL.md`. Verify the profile directory exists before proceeding. Add the charter as a preamble above the profile's existing persona content. If the profile doesn't have a soul yet, flag it and ask for the persona definition before creating.
- Do not present a finished charter draft — always walk through sections collaboratively.
- Do not propose replacing Layers 0–2 — they are permanent infrastructure.
