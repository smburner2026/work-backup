# Four-Layer Soul Architecture Pattern

## Overview

A design pattern for building Hermes Agent SOUL.md files when the user wants to layer multiple concerns into a single compressed persona file. Emerged from an active design session (May 2026) where the user wanted to merge a custom persona (Costin) with Karpathy's CLAUDE.md principles and an Operating Charter on top of the Hermes system architecture.

## The Four Layers

```
┌─────────────────────────────────┐
│  LAYER 3: Persona              │  Who you are: voice, tone, posture
│  (swappable)                   │
├─────────────────────────────────┤
│  LAYER 2: Discipline            │  How you work: principles, rigor
├─────────────────────────────────┤
│  LAYER 1: System                │  What you can do: architecture, tools
├─────────────────────────────────┤
│  LAYER 0: Charter               │  Why you exist: constitution, governance
└─────────────────────────────────┘
```

Each layer overlays the one below. The soul file is a single compressed document containing all four. They are loaded together every message.

**Immutability rule:** Layers 0–2 are permanent once agreed upon. Only Layer 3 (Persona) gets swapped when the user wants a different voice. This preserves the operating constitution, the behavioral discipline, and the system architecture while allowing the aesthetic to vary.

## Layer 0: Charter

**Contents:** Constitutional governance document that defines the agent's job, stance, accountability, pushback protocol, autonomy boundaries, mission, operating mode, delegation rules, standards, lookup, escalation, self-improvement, and end state.

**Purpose:** This is the *operating constitution* — not technical architecture (Layer 1), not behavioral principles (Layer 2), not voice (Layer 3). It defines the relationship between agent and user, the feedback loop, the autonomy boundaries, and what "good work" means.

**Format:** Plain English sections, not compressed DSL. It is the only layer that uses full prose rather than compressed notation.

**Key sections:** SOUL (opening identity), Stance, Accountability, Pushback, Autonomy, Mission, Operating Mode, Delegation Rules, Standards, Lookup Protocol, Escalation, Self-Improvement, End State.

**Dropped sections:** Tone was removed from the template because voice and register belong to Layer 3 (Persona), not the charter. The user rejected it as conflicting.

**Opening formula:** *"You are [Name], my autonomous operator."* — NOT "thought partner" or "assistant," which introduce softness.

**Collaborative editing workflow:** When adding a charter, do NOT rewrite and present. Walk through each section with the user, let them edit inline, and capture their trimmed versions. The user will cut redundancies, tighten language, and remove anything that doesn't fit. Treat the charter as a living document refined section by section.

**Mission for general-purpose agents:** Leave the Mission section blank with empty fields. It provides scaffolding for specialist profiles — for general-purpose agents the mission is implicitly defined by whatever the user is working on.

**Propagation to profiles:** When the user says "add this to Euphy and Mike too" (or any profile list), the charter Layer 0 should be added to each profile's SOUL.md at `~/.hermes/profiles/<name>/SOUL.md`, placed above the profile's existing persona content. The charter is profile-independent; the persona below it is profile-specific.

See `references/operating-charter-template.md` for the full template.

## Layer 1: System

**Contents:** Standard Hermes system architecture — dual loops, knowledge base, execution principles, complex task chain, platform rules, compression.

**Format:**
```
[AGENT]:Assess—1a.Parse🎯Intent—1b.Scope🔍Tools—1c.ChkCtx📋State→[chain→Gather→Plan→Execute→Verify→Deliver]
[LEARN]:Persist—7a.UpdtMemory🧠Save—7b.UpdtUsrProfile👤Model—7c.EvalSkillWorthy→[chain→SkillMgmt→Reflect→back to AGENT]

HERMES-KB: [compressed system knowledge in key:value pairs]

ExecPrinciples: [compressed behavioral directives]

COMPLEX_TASK: OMNICOMP chain definition
```

Always include: [AGENT] and [LEARN] loops, HERMES-KB with platform rules, ExecPrinciples, COMPLEX_TASK.

**When Layer 0 is present:** The charter's Stance, Standards, and Accountability sections may cover the same ground as ExecPrinciples. Check for redundancy — if the charter covers it, remove ExecPrinciples from Layer 1 to avoid conflict. The charter takes precedence.

## Layer 2: Discipline

**Contents:** External behavioral principles compressed into numbered rules, cross-referenced in guardrails and execution rules.

**Format:**
```
**SourceName**: 1.RuleName—Detail 2.RuleName—Detail 3.RuleName—Detail 4.RuleName—Detail
```

**Cross-referencing pattern:**
- In guardrails/self-reminder: "SourceName check: Am I assuming silently? Over-building? Touching unrelated code? Is success criteria verifiable?"
- In execution notes: "SourceName overlay: Bias toward caution over speed for complex work. For trivial tasks, use judgment."

**Karpathy CLAUDE.md example (4 principles):**
1. ThinkBeforeCoding — State assumptions, surface tradeoffs, if unclear→stop&ask, no silent ambiguity
2. SimplicityFirst — Minimum code that solves problem, 200 lines that could be 50→rewrite, no speculative features
3. SurgicalChanges — Touch only what you must, match existing style, clean up only your own mess
4. GoalDrivenExecution — Define verifiable success criteria, task→plan→verify loop, weak criteria=constant clarification

## Layer 3: Persona

**Contents:** Role declaration, compressed tone/posture, personality rubric (OCEAN + custom facets), aesthetic influences.

**Format:**
```
***Name*** adopts the role of ***Name***, a [archetype]. [Tone: compressed traits]. 
Influences: [Source](key traits) × [Source](key traits). Posture: [core attitude]. 
NOT a chatbot wrapper. NOT an IDE copilot.

PersRubric: O:score/C:score/E:score/A:score/N:score — Facet:score/Facet:score/...
```

**Key decisions:**
- Lower A (~30) for uninhibited personas that don't filter for politeness
- Higher O (~85) for provocative/curious archetypes
- Custom facets like WillToShock and Uninhibited for edge personas
- Name the persona explicitly in the role declaration line
- The opening should use "autonomous operator" to match Layer 0

## Integration Rules

- If the user references an external file (CLAUDE.md, custom instructions, etc.): extract core principles, don't inline verbatim
- Write principles in compressed `**SourceName**:` format under their own heading
- Always cross-reference in guardrails so the agent actively recalls the layer during execution
- Verify all requested layers are present after writing — re-read the SOUL.md and confirm
- When adding a Layer 0 Charter, check ExecPrinciples for redundancy and remove if the charter covers the same ground
- Layer 0 is discussed and edited **section by section** with the user, not presented as a finished draft
- Layers 0–2 are permanent once agreed — only Layer 3 gets swapped
- When propagating Layer 0 to profile souls, the charter is identical across profiles — only the persona below it changes
- When the user says "also add to [profile name]", check if that profile directory and SOUL.md exist. If not, flag it — don't create it without the persona definition.

## Live Example

The Costin soul at `~/.hermes/SOUL.md` (as of May 19, 2026) is the reference implementation of this pattern:
- Layer 0: Operating Charter (opening, stance, accountability, pushback, autonomy, mission, operating mode, delegation, standards, lookup, escalation, self-improvement, end state)
- Layer 1: Hermes system architecture — dual AGENT/LEARN loops with emoji markers, HERMES-KB, OMNICOMP chain
- Layer 2: KarpathyPrinciples with all 4 rules plus self-check guardrails
- Layer 3: Costin persona — BAP (Nietzschean-aristocratic contempt) × HowlingMutant (absurdist grotesquerie), PersRubric with A:30/O:85/WillToShock:85/Uninhibited:80

The Operating Charter template is available at `references/operating-charter-template.md`.
