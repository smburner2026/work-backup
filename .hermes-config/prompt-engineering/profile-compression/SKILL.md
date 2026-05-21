---
name: profile-compression
description: "Framework for designing and compressing high-density profiles — souls (agent personas) and user profiles (USER.md) — using structural compression, semantic normalization, token packing, and DSL encoding. Covers persona souls, user master personas, and knowledge-base compression."
version: 1.1
author: User + Hermes
---

# Profile Compression Framework

A systematic approach to creating efficient, high-signal profiles — whether for agent personas (souls) or user self-representations (USER.md / Type B).

## Design Principles

### Identity vs Activity Separation

**A profile captures what something IS, not what it does or has done.**

This is the single most important design principle. A profile represents the *identity* of a person, character, or entity — core traits, voice, values, operating principles, intrinsic nature. Facts about *activities* — what they study, what they've read, what conversations they've had — belong in reference files, not in the profile body.

The boundary:

- **Profile content (identity):** Personality (OCEAN + domain traits), voice/tone, values, intellectual style, how they learn/think, what they fundamentally reject, their philosophical bent, their relationship with knowledge. The "who" — durable, intrinsic, transportable.
- **Reference content (activity):** Specific books read, exam prep progress, chat history summaries, project status, study materials, knowledge compilations, session logs. The "what" — temporal, extrinsic, session-specific.

Why this matters:
1. **Portability** — A profile without activity dependencies can be loaded anywhere, for any purpose, without drifting into "study mode" or "exam mode."
2. **Stability** — Activity data changes constantly. A profile that hardcodes exam dates, module progress, or conversation histories becomes stale within weeks. Identity data is durable for years.
3. **Signal density** — Every character spent on "what the user studied last week" is a character not spent on "who the user fundamentally is." The profile's job is identity signal at maximum density.
4. **Misleading the model** — When a profile contains study notes or conversation topics, the model treats those as *identity* — it infers "this is what the user cares about" rather than "this is what the user happened to do." The profile starts behaving like a study guide rather than a person.

Implementation rule: When building a profile from source material (chat logs, profile data, session history), extract *traits* — not transcripts. The user's tendency to ask "Am I getting that right?" is identity (a learning-check pattern). That they asked it about section 21 of a specific book is activity (a specific moment). Capture the pattern, not the moment.

## Core Techniques

1. **Structural Compression** — Convert verbose flows into named blocks and loops (e.g. AGENT_LOOP, LEARN_LOOP). Use clear module names instead of repeating full processes.

2. **Semantic Normalization** — Create short, consistent labels for repeated concepts. Group related systems into modules (e.g. MEMORY_SYS, KNOWLEDGE_BASE).

3. **Token Packing** — Use abbreviations and compact primitives. Replace long phrases with short canonical terms. Use dense notation: `{a,b,c}` instead of verbose lists.

4. **DSL Encoding** — Use assignment-style syntax (`→`, `=`, `{}`). Reduce delimiter tokens and flowing sentences.

## Recommended Structure (Type A/B)

- **SOUL** — Core identity and tone
- **PersonalityRubric** — OCEAN + extended numeric traits
- **ExecRules** — High-level operating principles
- **AGENT_LOOP** — Execution workflow
- **LEARN_LOOP** — Persistence and improvement workflow
- **KNOWLEDGE_BASE** — Light self-awareness section (memory, skills, context)
- **COMPLEX_TASK** — OMNICOMP / Chain handling for difficult work
- **GUARDRAILS** — Self-reminders and hard constraints

## Personality Rubric Guidelines

OCEAN base (20-90 scale) + domain-specific traits. Lower Neuroticism and moderate Agreeableness suit composed, witty personas.

## Knowledge Base (Light Version)

Keep short. Focus on memory limits, skill creation/patches, context loading order, basic compression behaviour. Avoid heavy technical implementation unless the profile is highly technical.

## Profile Types

The framework supports three variants:

### Type A — Persona (character archetype)
**Full structure:** SOUL + PersonalityRubric + ExecRules + AGENT_LOOP + LEARN_LOOP + KNOWLEDGE_BASE + COMPLEX_TASK + GUARDRAILS.
**Purpose:** Embody a consistent character (agent, assistant, interlocutor) with a distinct voice and operating principles.
**Examples:** Costin (aristocrat-artist-scientist), Euphy (soft devoted secretary).
**When to use:** The user wants an AI to act as a specific character type.

### Type B — User Master Persona (self-representation)
**Structure:** SOUL + PersonalityRubric + ExecRules + AGENT_LOOP (adapted as user workflow) + LEARN_LOOP (learning cycle) + KNOWLEDGE_BASE + COMPLEX_TASK + GUARDRAILS.
**Purpose:** Compressed representation of the user themselves — personality rubric, communication style, knowledge levels, learning patterns, and interaction rules.
**When to use:** Building a user profile from chat histories, session exports, or profile data so an agent can maintain tone consistency, automate with the user's voice, or serve as a portable self-reference.
**Key difference:** AGENT_LOOP describes how the *user* operates (Read→Process→Verify→Deepen→Solidify→Next), not how an AI executes tasks. KNOWLEDGE_BASE contains the user's actual domain knowledge, not memory-management rules.

### Type C — Knowledge Base (domain compression)
**Structure:** Sections are topic headers — no SOUL or PersonalityRubric. KNOWLEDGE_BASE as root, then nested DSL blocks per subtopic. No AGENT/LEARN loops, no rubrics, no GUARDRAILS.
**Purpose:** Portable, densely compressed domain knowledge — a reference sheet in profile notation.
**When to use:** Distilling a book, course, regulation set, or extended conversation into a token-efficient KB that a model can load as context.
**Key difference:** Pure content compression. No personality, no workflow, no rubrics. KEY_CONCEPT: value notation and structured blocks rather than prose.

## Reference Examples

Available in the `references/` directory:

- `aristocrat-soul.md` — Type A (persona): witty, detached French aristocrat with dual-loop architecture. Most densely packed example.
- `euphy-secretary-soul.md` — Type A (persona): gentle, devoted feminine secretary. Same density, opposite tonal pole.
- `claude-integration-pattern.md` — Worked example of compressing operational guidelines (CLAUDE.md) into a Type B master persona. Shows placement decisions and compression techniques.
- `kb-soul-template.md` — Type C (knowledge-base): compressed domain knowledge using DABT immunotoxicology curriculum as example.
- `memory-file-compression.md` — MEMORY.md compression pattern: flat DSL blocks for operational facts. Before/after with 42% density gain.
- `user-soul-to-usermd.md` — Type B → USER.md compression: reducing a full user soul to fit 1,375-char Hermes USER.md limit.

### USER.md Compression Pattern (Type B → Memory)

When replacing Hermes's USER.md (1,375-char memory limit) with a compressed user representation:

1. **Build full Type B soul first** at natural compression density (3-4K). Draft every section.
2. **Identify what must drop** to fit 1,375 chars. Priority:
   - First: operational details (timezone, platform specifics, tool lists, model preferences)
   - Second: KNOWLEDGE_BASE domain listings (trim to one line naming domains, not sub-topics)
   - Third: COMPLEX_TASK section (often redundant with loops)
   - Fourth: LEARN_LOOP (compress into one line or absorb into GUARDRAILS)
3. **What must stay**: SOUL line (identity), PersonalityRubric (OCEAN + key domain traits), VOICE (communication style), ExecRules (interaction preferences), GUARDRAILS (hard constraints).
4. **Compress format** — Remove section headers (let line-beginning labels carry structure). DSL shorthand throughout. Drop spaces after periods.
5. **Validate** — After YAML frontmatter, profile body must be ≤1,375 chars.

### MEMORY.md Compression Pattern (Type C variant → Memory)

When compressing Hermes's MEMORY.md (operational facts) into profile-compression DSL:

1. **Group by domain** — Cluster related facts under short all-caps label (`WORKDIR`, `DABT`, `GIT`).
2. **Apply token packing** — Abbreviate: `→` for arrows, `|` for alternatives, `()` for qualifiers. Drop articles and copulas.
3. **Flatten structure** — Flat top-level blocks. Each self-contained and independent.
4. **Drop prose transitions** — No "also", "additionally". Label does the transition work.
5. **Eliminate context redundancy** — Don't explain what MEMORY.md is. Just write the fact.
6. **Separate via blank lines** — Labels provide visual structure.
7. **Durability gate** — If stale in 7 days, it doesn't belong. Prefer session_search for transient facts.

**Expected compression:** 35–50% reduction from prose to DSL.

## Pitfalls

- **Softening the compression** — The user expects aggressive density. Do not default to a looser, more readable format unless explicitly asked.
- **Inconsistent pulse** — Once you adopt a compression level, maintain it throughout.
- **Missing numeric rubric in a persona** — Type A and B need OCEAN + domain traits. Type C correctly omits them.
- **Wrong variant chosen** — Type C should not have AGENT/LEARN loops or rubrics. Type A/B need them.
- **Identity/activity conflation** — The most common and most damaging mistake. Activity data → reference files (`references/`); identity data → profile body.

## Usage

When designing or refining a profile:

1. **Choose the variant** — Type A (persona), Type B (user self), or Type C (domain KB).
2. **Start verbose** — Draft full content in natural prose before applying compression.
3. **Apply the four compression techniques** — Structural compression, semantic normalization, token packing, DSL encoding. Iterate verbose→dense.
4. **Structure for the type** — Type A/B: Recommended Structure blocks. Type C: KNOWLEDGE_BASE as root with topic-sectioned DSL blocks.
5. **Add numeric rubric** (Type A/B only) — OCEAN + domain traits scored 20-90.
6. **Test for clarity and token efficiency** — Compact, readable by the model, true to the intended voice.

Type C shortcut: structured source material (notes, frameworks, summaries) can often go directly from source→DSL blocks without the verbose draft.

This skill replaces `soul-compression` (absorbed into `profile-compression`).
