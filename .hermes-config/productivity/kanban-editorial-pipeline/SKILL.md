---
name: kanban-editorial-pipeline
description: Produce long-form written works (books, theses, major syntheses) using Kanban as the orchestration layer. Decompose into chapter-level cards, draft them one at a time, review at every gate, build toward a synthesis epilogue that reads all parent handoffs.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, writing, editorial, book, research, synthesis]
    related_skills: [kanban-orchestrator, kanban-worker]
---

# Kanban Editorial Pipeline

> The author writes by commissioning chapters, not by typing them. The board is the manuscript; the cards are the chapters; the user is the editor-in-chief.

## When to use this skill

- The user wants to produce a **long-form work** (book, monograph, major essay, research synthesis)
- The work can be decomposed into **discrete, bounded chapters or sections**
- The user wants to **review each piece before the next is written**
- The work requires **multiple intellectual lenses** (political, economic, cultural, philosophical) that need to remain in tension rather than being flattened into one voice
- The user wants to **plan the architecture together** and then have the agent draft to a brief

If the work is a short essay or article that can be written in one shot, use `delegate_task` or write it directly. This skill is for projects with a natural chapter structure and editorial gates.

## Core principle: the book as a Kanban board

```
Prelude (card 0)               Phase 1                        Phase 2               Epilogue
┌──────────────┐          ┌──┬──┬──┬──┬──┐              ┌──┬──┬──┐            ┌──────────────┐
│ Opening frame │          │C1│C2│C3│C4│C5│              │C6│C7│C8│            │  Synthesis   │
│ (Nietzsche,   │          └──┴──┴──┴──┴──┘              └──┴──┴──┘            │  epilogue    │
│  Napoleon,    │                │                              │               │  reads all   │
│  a question)  │         you review                     you review            │  parents     │
└──────┬───────┘                │                              │               └──────┬───────┘
       │                        └──────────────┬───────────────┘                      │
       │                                       │                                      │
       └──────────────┬────────────────────────┘──────────────────────────────────────┘
                      │
              All gates before epilogue
```

**Key properties:**
- Each card is a **bounded chapter** — reviewable in ~10 minutes
- Cards within a phase are **independent** (parallel-capable)
- Phases are **sequential** — each ends with a human review gate
- The **epilogue/synthesis card** has *all prior cards as parents* and reads their handoffs to produce the final integration
- **Nothing auto-advances** — every gate requires explicit human approval

## Planning phase

Before any cards are created, **design the architecture together** with the user:

### Step 1 — Establish the analytical framework

What lenses will every chapter be written through? Capture these as card instructions. Common frameworks from the session that produced this skill:

Every project needs an **operating system** — the analytical method the author *sees with* — and an **application layer** — what the reader sees on the page. Distinguish these when planning.

| Lens | Level | What it does |
|---|---|---|
| **Nietzsche's physiology** | Operating system | The ground, not the figure. Always running underneath every chapter as the author's method. Asks: what kind of human being did this civilisation produce? Was the type strengthened or weakened? **Only surfaces in prose when the material demands it** — Montaigne's kidney stones, the court's breeding of a new type, the demographic collapse after civil war. The reader should *feel* it without having it labelled. |
| **Three-force analysis** | Application | How did nomos (institutions, laws, structures), the invisible hand (economics, material conditions, unintended consequences), and great individuals (decisive choices) interact in this chapter? Every card traces the *connections* between these forces. |
| **Burckhardt's total view** | Application | How does this chapter contribute to the civilisation as a work of art? The eye that sees a culture as a whole, not as separate compartments. |
| **George-Circle portraiture** | Register | Carve figures as *types*, not biographies. Summon them as spirits — Gundolf's Caesar, Kantorowicz's Frederick II. The prose itself should be a manifestation. |
| **Moraliste ear** | Register | The inner voice, the aphorist's glance, Montaigne's "what do I know?" A counterpoint to the heroic portrait — the self-awareness that shadows every great action. |
| **Blood and climate** | Operating system | The mixing of north and south — Frankish vigour meeting Gallo-Roman refinement, northern instinct meeting southern *ratio*. A people stretched between two bloods produces a distinctive type. Trace this tension in every figure and institution. |

Make the frameworks explicit before card 1. The user will adjust them. They may reject some lenses entirely or demand different emphasis. The operating-system vs application-layer distinction is itself a preference: some users want physiology as foreground (it colours every paragraph), some want it as undercurrent (it informs the analysis but rarely names itself). **Establish which before writing begins.**

### Step 2 — Decompose into parts and chapters

Work outward: **frame → parts → chapters → per-chapter brief**.

Each chapter brief should specify:
- **Subject** (what it covers)
- **Register** (portrait, landscape, artifact, philosophical meditation, etc.)
- **Analytical dimensions** (which of the frameworks above to apply)
- **Length** (approximate word count or pages)
- **End note** (what judgment or insight this chapter should deliver)

### Step 3 — Design the dependency graph

Chapters in the same part are **independent** — no parent links between them. Parts are **sequential** — part 1 is parent to part 2's first card (conceptually; in practice, the human gate is the link).

The **epilogue/synthesis card** gets *all* prior cards as parents. Its instruction is: "Read all parent handoffs. Synthesise across them. Deliver the final integration."

### Step 4 — Show the graph to the user

Before creating any cards, present the full architecture. Let them reorder, rename, add, remove. The planning session is the most important step — it's where the user does their real intellectual work.

## Card design

### The brief

Every card body must be self-contained. A good chapter brief:

> Chapter X — [Title]
>
> Register: portrait. Carve this figure as a type, not a biography.
>
> Analytical dimensions:
> - Nietzsche's physiology: what kind of human being is this?
> - Three-force: how did institutions, economics, and personal agency intersect here?
>
> Specifics to cover:
> - [item 1]
> - [item 2]
> - [item 3]
>
> Tone: oracular, elevated, aphoristic. Write as if for the Stefan George Circle. No academic apparatus.
>
> Length: ~2,000 words.

### The handoff

When a chapter card completes, `kanban_complete` must include:

```python
kanban_complete(
    summary="Chapter X: [Title] — [one-line judgment of what it delivers]",
    metadata={
        "word_count": 2150,
        "key_claims": ["claim 1", "claim 2"],
        "register": "portrait",
        "sources_consulted": ["source A", "source B"],
        "open_questions": ["question for the editor callout"],
    },
)
```

The summary + metadata is what the epilogue card reads. Make it rich enough for synthesis without re-reading the full chapter.

## The editorial workflow

The loop for each chapter:

1. **Plan together** — propose the next chapter's brief. User approves or redirects.
2. **Draft** — agent writes the chapter as a kanban card. This runs while the user sleeps.
3. **Review** — user reads the draft, marks it up, sends feedback.
4. **Revise** — a new card for the revision, linked from the original. Or move to the next chapter.
5. **Gate** — user explicitly says "proceed" before the next card is created.

**Never create the next card until the current one is reviewed.** The board holds the plan; it doesn't execute the plan independently.

## The synthesis epilogue

The final card is always a synthesis that reads all parent handoffs.

Its brief must:
- Name the analytical framework for the synthesis itself (e.g., "reconcile Nietzsche's judgment and Napoleon's judgment")
- Specify the voice (e.g., "a third voice, the editor's, standing beside both")
- Deliver a verdict, not a summary
- End with an open question — the book should close on a note that invites the reader to continue thinking

The synthesis card's `parents` list includes every prior card ID. Its body says "Read all parent summaries. Produce the epilogue."

## Pitfalls

**Over-decomposing.** A chapter should be reviewable in ~10 minutes. If the brief would produce something longer, split it. If the brief is so narrow it can only produce a paragraph, merge it.

**Under-specifying the register.** "Write a chapter about X" produces generic academic prose. The register must be specified explicitly (portrait, aphoristic, oracular, landscape, polemical, etc.) or the voice will drift.

**Losing the analytical framework.** Midway through a long project, cards start being written without the agreed lens. Every card body must restate the frameworks. Add them as a checklist in the brief.

**Creating the epilogue too early or too late.** It only makes sense as the *last* card. Its parents must be *all* prior cards. If chapters are still being written when the epilogue runs, it produces a partial synthesis that will be wrong.

**Allowing the agent to set the agenda.** The user is the editor. The agent proposes; the user disposes. If the user hasn't approved the next chapter's brief, don't write it. This is the cardinal rule.

**Register drift across chapters.** One chapter written in the George-Circle voice, another in academic prose. The skill should enforce consistency by restating the register in every card brief. If drift is caught at review, the revision card must specify the correction explicitly.

**Parallel execution without permission.** Within a phase, cards can technically run in parallel. Never do this unless the user explicitly says "run the next two while I read." Default: one chapter at a time, human gate between each.

**Omitting analytical dimensions from the epilogue brief.** The synthesis card needs to know *how* to synthesise. If the book was built around three-force analysis, the epilogue must be told to trace connections across those three forces, not just summarise each chapter in sequence.

**Dominance of a single lens.** Any analytical lens pushed too hard into the prose becomes caricature. The operating-system lenses (physiology, blood-and-climate) should colour the writing, not announce themselves on every page. The user will correct you when a lens has moved from lighting to furniture. When they do, adjust — don't abandon the lens, just push it back to where it belongs.

**Platform blindness.** The user interacts via Telegram, Discord, or another messaging platform, not the CLI. Running terminal commands without explaining what you're doing and why will confuse them. Before executing any kanban operation, tell the user what you're about to do and interpret the result in their platform's idiom. A kanban card created via CLI is just a line of text to them; frame it.

## User preferences (this session's origin)

This skill was produced during a session where the user:
- Wanted to understand why Napoleon called 16th-century France the peak of European civilisation
- Rejected Marxist historiography; subscribed to great-man theory tempered by institutional awareness (identified Chris Wickham as a "good" Marxist historian)
- Demanded Nietzsche's physiological lens as the **operating system** — informing every chapter but only surfacing in prose when the material demands it. "Undercurrent, not furniture" was the user's explicit correction after an initial draft pushed physiology too hard
- Wanted the George-Circle register: portrait-driven, oracular, hagiographic in tone, not academic
- Valued the interplay of nomos (institutions), the invisible hand (economics), and great individuals as the primary application-layer framework
- Wanted the mixing of north and south (Frankish vigour + Gallo-Roman refinement, blood + climate) as a core analytical thread
- Wanted the book framed by Nietzsche (open) and Nietzsche+Napoleon+editor (close)
- Preferred the agent as amanuensis and editorial partner, not autonomous author
- Insisted on bounded, reviewable tasks over autonomous multi-hour execution
- Interacted via messaging platforms (Telegram, Discord), not the CLI terminal — commands run on their behalf must be framed and explained

When a new user presents a similar project, ask: what lenses do you want to see through? The planning phase establishes this before any writing begins. **Crucially, distinguish operating-system lenses (always on, rarely named) from application-layer lenses (explicit in every chapter brief).** The user may push back if you get this balance wrong.

## Reference files

- `references/crowned-century-architecture.md` — full worked example from the session that produced this skill: a 26-chapter book on 16th-century France using Nietzsche, Napoleon, Burckhardt, and George-Circle lenses. Adapt this architecture for new projects rather than starting from scratch.
