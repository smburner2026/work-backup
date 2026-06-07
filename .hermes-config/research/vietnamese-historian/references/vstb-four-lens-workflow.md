# VSTB Four-Lens Analysis Workflow

**Context:** The June 2026 session applying the four-lens historiographical method to Phạm Văn Sơn's *Việt Sử Tân Biên* (VSTB), specifically the translated chapters covering 1885–1896 (ch2-ch6, ch9 of the translation output).

**Core insight:** The four lenses can be applied to the *historian* as much as to his *subject*. The question is not just "what does Phạm Văn Sơn say happened" but "what is Phạm Văn Sơn constructing, and what does he suppress?" This is the method for separating the historian's narrative from the historical record.

---

## The Workflow: Primer → Deep Dive → Source Strategy

### Stage 1: Primer (overview, ~2,500 words)

Before any passage-level work, write a primer that establishes the four-lens reading. This is the *frame* that makes the deep dive coherent.

**Structure of the primer:**
1. Burckhardtian reading — what is the "spirit of the era" the historian constructs?
2. Nietzschean Vitalist reading — what kind of beings produce force in the narrative?
3. Class reading — whose interests are served?
4. Covert+Luttwak reading — what strategic logic is operating, and does the historian see it?
5. Synthesis — what is the historian building? A national myth? A usable past? A scholarly synthesis?
6. Source-finding strategy — what sources would fill the gaps each lens reveals?

The primer is intentionally compact. It establishes the *questions*; the deep dive develops the *evidence*.

### Stage 2: Deep Dives (passage-level, ~4,000 words each)

For each of the four lenses, write a deep-dive document. Each follows a fixed structure:

**Fixed structure for each lens deep dive:**

1. **Passage Inventory (10-15 quotes with line citations)** — the actual evidence. Quote the historian liberally. Cite line numbers from the source files.

2. **What He Sees / What He Misses** — pair findings. For every dimension the lens reveals, identify both what the historian captures AND what he suppresses. The "misses" are the gaps that primary sources could fill.

3. **Cross-Sectional Analysis (for Burckhardtian) or Case Studies (for other lenses)** — pick 2-3 specific moments in the source text and analyze them in depth through the lens. The cross-section / case study is where the abstract framework meets concrete evidence.

4. **His Own Moment / Hidden Architecture** — the meta-analysis: what does the text reveal about the historian's own context and project? Why does he emphasize X and suppress Y? Who is he writing for?

5. **Source Gaps** — specific source types that would fill the missing dimensions. Name archives, document types, languages, and access points. The source gaps are the *output* that drives future acquisition.

**Critical rule:** the deep dive must quote the historian with line citations. No generalities, no "this is interesting because...". Direct evidence → analysis.

### Stage 3: Source Strategy (synthesis of gaps)

After all four deep dives, the source gaps aggregate into a source-finding strategy. Each lens points to different archives:

| Lens | Primary Sources |
|------|-----------------|
| Burckhardt | EFEO ethnography, Catholic mission records, Mường oral traditions, Qing court records, popular religion studies |
| Vitalism | French colonial census data, ecological/disease studies, archaeological excavations, population genetics |
| Class | Colonial economic reports, Nguyễn land/tax records, Catholic community records, plantation records, Mường-Vietnamese economic relations |
| Covert+Luttwak | Quai d'Orsay archives, Service Historique de la Défense, British National Archives, Chinese diplomatic archives, missionary intelligence networks, captured resistance documents |

The strategy identifies **what is accessible** vs **what is foundational**. Some sources (e.g. Mường oral traditions) are foundational but hard to access. Others (e.g. French colonial economic reports) are more accessible and yield immediate evidence.

---

## The Method: Applying the Lenses to the Historian

This is the *meta-level* move that distinguishes the four-lens analysis of a translated historical text from a generic book review. The question is not "is the historian right or wrong" but "what is the historian *doing*?"

### Burckhardtian — Culture

The Burckhardtian lens applied to the *historian* asks: what is the *cultural moment* the historian is writing from, and how does that shape what he sees? In Phạm Văn Sơn's case, he was writing in the 1950s (VSTB published 1957+) — post-First Indochina War, partition of Vietnam, need for a usable national past. His cultural framing of 1885 is shaped by 1957's needs.

Specific techniques:
- Find passages where the historian's *own era* leaks through (anachronistic framings, present-tense concerns)
- Identify what is *omitted* (religious diversity, ethnic minorities, women) — omissions reveal cultural assumptions
- Read the text as a *document of the historian's era* as much as a document of his subject era

### Nietzschean Vitalist — Biology, Force

Applied to the *historian*, the Vitalist lens asks: does the historian understand, even unconsciously, that historical force is *biological*? Phạm Văn Sơn is a *secret vitalist* — his narrative structure assumes that great men are beings of extraordinary force, and that the population's biology produces them. But he lacks the analytical framework to develop the question.

Specific techniques:
- Catalog the historian's language for *bodies*, *disease*, *endurance*, *death*
- Identify the historian's "great man taxonomy" — who is presented as a force, who as weak?
- Find the *unconscious vitalist moves* — passages where biology matters but the historian doesn't analyze it
- Note the *absences*: the demographic questions never asked, the ecological conditions never named

### Class — Property, Labor, Exploitation

Applied to the *historian*, the class lens asks: whose interests does the narrative serve? Phạm Văn Sơn was a mandarin-class intellectual writing for mandarin-class readers. His "national unity" framing suppresses the class conflicts that existed within Vietnamese society.

Specific techniques:
- Identify the implicit class structure in the narrative (court / gentry / common people / minorities / Catholics / collaborators)
- For each tier: what do they own? what do they do? how are they treated?
- Find the *material details* (silver taels, rice quantities, labor forces) and ask where they came from, who controlled them, who benefited
- Recognize the *class violence disguised as patriotism* (anti-Catholic violence as gentry reasserting class control)

### Covert+Luttwak — Strategic Logic

Applied to the *historian*, the strategic lens asks: does the historian see the *systems* at work, or only the *events*? Phạm Văn Sơn is a good *narrator* of military events but a poor *analyst* of strategic systems. He misses the French grand strategy, the covert apparatus, the second-order effects.

Specific techniques:
- Apply the Luttwak test: what is the *stated* strategy vs. the *actual* strategy?
- Find the *covert dimensions* the historian ignores (missionary intelligence, puppet government management, propaganda operations)
- Trace the *second-order effects* the historian misses (anti-Catholic violence as strategic self-destruction, fragmentation as strategic dispersal failure)
- Identify the *strategic absences* (no Vietnamese grand strategy, no alliance framework, no logistics system)

---

## The "Forum Debate" Technique

For generating initial ideas when the user is uncertain about how to proceed, the "forum debate" structure works well. The user prompts: "give me a few approaches to take on this text." The agent generates 4 distinct cuts (one per lens), each:

- Named after a specific lens
- With a clear *core question*
- Connecting the lens to a specific analytical move
- Ending with a meta-question that synthesizes

**Why this works:** the user can scan the four approaches quickly, pick the one that sparks interest, and the agent has a structured entry point. The lens names provide a vocabulary for further discussion.

**When to use:** when the user has a translated secondary source and wants to begin analysis but is uncertain about direction. The forum debate turns "I don't know how to proceed" into "which of these four cuts interests you most?"

---

## Subagent Dispatch Failure: Fallback Pattern

**Pattern observed in this session:** When subagent dispatch fails (API errors, model routing issues, max_concurrent_children limits), the fallback is *direct sequential analysis* by the orchestrating agent. The orchestrating agent:

1. Reads the source material into context directly
2. Writes the four deep-dive documents sequentially (not in parallel)
3. Same depth, same passage-level evidence
4. No kanban card execution needed — the agent IS the worker

**When this works:** for analysis tasks of ~3,000-5,000 words per document, with 4-6 source files, the orchestrating agent can produce equivalent quality to parallel subagents. The cost is sequential (not parallel) execution time.

**When it doesn't work:** for tasks requiring *physical actions* on remote systems (SSH to WSL, file I/O on the local machine), for tasks requiring fresh tool-use budgets, or for tasks where the orchestrating agent's context is already full.

**Pitfall to remember:** When subagent dispatch fails, the kanban card remains in `ready` state. The agent should *mark them complete manually* after the direct work is done — the kanban board should reflect actual progress, not dispatch attempt status.

---

## Key Finding: Post-Colonial Nationalist Historiography

The four-lens analysis revealed a pattern that recurs across post-colonial nationalist historiography:

**The nation is constructed as:**
- *Culturally monolithic* (one spirit, one civilization, one people)
- *Led by great men* (individual force, personal will)
- *Class-unified* (national interest above class interest)
- *Heroically tragic* (brave but outmatched, noble but doomed)

**This construction is not false** — it captures something real. But it is *partial*. It suppresses:
- Internal diversity (religious, ethnic, regional, class)
- Population-level forces (demography, ecology, biology)
- Material interests (whose class benefits, whose loses)
- Strategic systems (grand strategy, covert apparatus, second-order effects)

**The historian's own context shapes what is suppressed.** Phạm Văn Sơn in 1957 needed a unified past for a partitioned nation. That need shaped the narrative.

**The task for the reader:** separate the *usable past* from the *historical record*. The usable past serves the present; the historical record serves the truth. Both are valuable, but they are not the same thing.

---

## Outputs from June 2026 Session

The following documents were produced:

| File | Words | Description |
|------|-------|-------------|
| `/root/work/post-colonial-vietnam/analysis/vstb-four-lenses.md` | ~2,600 | Primer — overview of all four lenses |
| `/root/work/post-colonial-vietnam/analysis/lens1-burckhardtian-deep.md` | ~3,100 | Burckhardtian deep dive |
| `/root/work/post-colonial-vietnam/analysis/lens2-vitalism-deep.md` | ~4,000 | Nietzschean Vitalist deep dive |
| `/root/work/post-colonial-vietnam/analysis/lens3-class-deep.md` | ~4,000 | Class/Material deep dive |
| `/root/work/post-colonial-vietnam/analysis/lens4-strategic-deep.md` | ~4,400 | Covert+Luttwak deep dive |
| `/root/work/post-colonial-vietnam/analysis/INDEX.md` | ~1,000 | Navigation guide |

**Kanban board:** `vstb-four-lenses` (4 cards, all complete)

---

*Reference for the Vietnamese Historian skill. Use this workflow for any translated historical text that needs four-lens analysis, not just VSTB.*
