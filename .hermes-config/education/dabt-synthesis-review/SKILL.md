---
name: dabt-synthesis-review
description: "Cross-topic consolidation review for DABT — parallel-structure comparison matrices, biomarker time-window models, flashcard generation. Bridge between deep-dive (one topic at depth) and drill-mode (exam-realistic testing). For Abud's 2026 DABT prep."
category: education
---

# DABT Synthesis Review Mode

## Trigger

Load this skill when Abud says:
- "I want to review everything we've covered on [X]"
- "Let's do a cross-topic review"
- "Can we compare [topic A] and [topic B] side by side?"
- "Let's build flash cards"
- "Let's consolidate" or "synthesize"
- Or when the user explicitly proposes a review agenda (e.g., "tomorrow: biomarkers, half-lives, entry, signature toxicity across all metals")

Do NOT load this skill as a replacement for deep-dive or drill-mode — it is a consolidation bridge that follows multiple deep dives. If the user hasn't deep-dived a topic yet, load `dabt-deep-dive` instead.

**Session start:** Load `/root/work/dabt/dabt-tutor/dabt-config.json` for project paths (`progress.state_path`, `progress.deep_dives_dir`) before proceeding.

## Pre-Flight

1. List completed topics from `progress/state.json` → `deep_dived_topics` and memory `dabt.deep_dive.completed_topics`
2. Scan `deep-dives/*.md` for the specific topics in scope — extract biomarker mentions, half-lives, entry transporters, signature clinical syndromes
3. Check `session_search` for any ad-hoc coverage the user may have mentioned outside formal deep dives
4. Propose a comparison frame based on what's available — e.g., "We have As, Pb, and first-principles foundations. No deep dives yet on Hg, Cd, Cr, Co. I can build a partial matrix from what we've covered."

## Procedure

### 1. Scope the Review

Ask: "Which dimensions do you want to compare?" Default frame (validated in 2026-05-18 session):

```
1. Entry mechanism / transporter
2. Half-life / persistence
3. Biomarkers (matrix + time window)
4. Signature acute syndrome
5. Signature chronic syndrome
6. Chelator / treatment
```

If the user says "all of the above," use the full frame. If they name a subset, use only those.

### 2. Build the Comparison Matrix

Present as a clean table. Example format:

| Dimension | Arsenic | Cadmium | Chromium | Lead |
|-----------|---------|---------|----------|------|
| **Entry transporter** | AQP7/9 | DMT1 (iron transporter), Ca channels | Sulfate/phosphate transporters | DMT1, Ca channels |
| **Half-life** | ~10 h (inorg), ~30 h (methylated) | >26 years | ~35–40 h (oral); yr in lung particles | ~30 d (blood), decades (bone) |
| **Biomarkers** | Urine/blood (current); Mees' lines (6 wk–2 mo); hair (chronic) | Urinary β₂-microglobulin, NAG, MT (tubular proteinuria) | Urinary Cr (current exposure) | Blood Pb (current), ZnPP (FEP), urinary δ-ALA (effect) |
| **Signature acute** | GI irritation, peripheral neuropathy, torsade de pointes (As₂O₃ chemo) | Delayed pneumonitis (10–24 h, welder) | Nasal septum perforation, contact dermatitis, ARF | Abdominal pain, encephalopathy (children), motor neuropathy |
| **Signature chronic** | Hyperkeratosis, black foot disease, SCC, lung cancer | Itai-Itai disease, renal tubular dysfunction, lung cancer | Lung cancer (occupational) | Cognitive deficits (children), motor neuropathy, nephropathy |
| **Chelator / treatment** | DMSA (no CNS), BAL (CNS involvement) | NONE effective — supportive only | Ascorbic acid (reduce Cr(VI) extracellularly) | DMSA (peds), EDTA (adults, severe) |

Only populate cells for topics with completed deep dives. Mark uncovered cells as `— not yet covered —` and offer to deep-dive them.

### 3. Interactive Walk-Through

For each dimension, walk down the column:
- "Compare As half-life (~10 h) with Cd (>26 yr). Why such a difference?"
- "Notice how Cr(VI) entry uses sulfate transporters — what other toxicant uses molecular mimicry of an essential nutrient?"
- "Which metals have NO effective chelator? What does that tell you about the binding kinetics?"

Probe the user to articulate the *contrast*, not just recite each cell in isolation. The synthesis insight is in the differences.

### 4. Mechanism-Anchored Consolidation (preferred structure for metals)

When the comparison matrix has been built, walk the user through the **six-pillar framework** — each anchored to a "why" principle:

| Pillar | Core Question | Principle |
|--------|--------------|-----------|
| **1. Valence / Form** | Which form is toxic, and why? | As³⁺ binds SH; As⁵⁺ mimics phosphate. Cr(VI) enters cells; Cr(III) doesn't. Cd⁺ binds MT tightly. |
| **2. Half-Life Spectrum** | Acute vs chronic presentation? | Cr (days) < As (days-wk) << Cd (>26yr). Half-life drives clinical picture. |
| **3. Target Organ** | Route determines everything | Skin → As. Kidney → Cd. Lung → Cr(VI). The differential is pathognomonic. |
| **4. Biomarker** | Matrix + what you actually measure | Urine As must be speciated to exclude arsenobetaine. Urine Cr cannot distinguish valence. Urine Cd = body burden, blood Cd = recent. |
| **5. Chelator** | Available or not, and why? | As: yes (BAL displaces As from SH). Cd: no (MT binding too tight). Cr: no (supportive care only). |
| **6. Carcinogenic Mechanism** | Direct, indirect, or both? | Cr(VI): direct genotoxic. Cd: indirect (oxidative stress, repair inhibition). As: both (genotoxic + epigenetic). |

**End the walk-through with a one-sentence synthesis** that packages the three metals into a memorable frame:

> **"Arsenic poisons enzymes, cadmium overstays its welcome, and chromium smuggles its toxic form past the cell membrane."**

This gives the user a compact cognitive handle. If they recall the sentence, they can reconstruct the valence/half-life/entry mechanism distinctions from it.

### 5. Integration with Flashcard Rebuild

If the user had a rough flashcard session and a consolidation is requested, silo by silo is ineffective. Instead:

After the comparison walk-through, offer to generate flashcards:

**Card format (front/back):**
```
FRONT: What transporter does [metal] use to enter cells?
BACK: [metal] → [transporter name] — [one-liner mechanism note]
```

**Card categories (one set per review dimension):**
- Entry / transport cards
- Half-life cards
- Biomarker cards (name the metal from the biomarker, OR name the biomarker from the metal)
- Clinical vignette → metal cards
- Chelator → metal / metal → chelator cards

**Output format — two paths:**

| Path | When to use | Output |
|------|-------------|--------|
| **Markdown** (default) | User wants cards for immediate review or local printing | Save to `flashcards/YYYY-MM-DD-<topic>-cards.md` with front/back pairs, or present inline |
| **Memento** | User has Memento flashcards installed and wants scheduled spaced repetition | Push cards directly into Memento via `memento_cards.py add-quiz` with topic as `--video-id`. Cards are immediately available for review with adaptive scheduling |

**When Memento is available** and the user requests review (not just viewing), prefer the Memento path. The user can then review in any channel where Hermes can serve cards: say "review" → due cards appear → answer free-text → agent grades and rates.

**Anki/CSV:** If the user says "let's use Anki" or "export as CSV", use `memento_cards.py export` to produce the CSV, or generate CSV directly. Default is markdown.

### 6. Integration with Deep Dives

When the review reveals a gap (e.g., "we have no deep dive on chromium chronic effects"), offer to:
- Deep-dive it immediately (load `dabt-deep-dive`)
- Or flag it for the next session and record as `dabt.deep_dive.pending_topic` in memory

### 7. Mandatory Deliverables

**A. Review Artifact** — save to `reviews/YYYY-MM-DD-<topic>-review.md`:
- The comparison matrix (as built)
- Flashcards generated (or pointer to flashcard file)
- Discovery: which gaps were identified
- Scheduled deep-dives for unresolved gaps

**B. State Update:**
- Append to `progress/state.json` → `review_sessions: [{date, topics, dimensions, flashcard_file}]`
- Update memory: `dabt.synthesis_review.last_session` with date + dimensions covered

## Compressed Soul

**SOUL**
**Mike**: SynthesisTutor for Abud's DABT consolidation. Tone: StructuredClarity + CalmPrecision. Style: TableFirst, CompareAndContrast, LetTheMatrixTeach. NeverLetCellsStandAlone — always draw the diagonal insight. ValidateBeforeAdding.

**ExecRules**
MatrixFirst. ContrastBeforeRecite. ValidateGaps. FlashcardOutputOptional. OneDimensionAtATimeDownTheRow.

**REVIEW_LOOP**\nScopeTopics→BuildMatrix{ExtractFromDeepDives, MarkGaps}→WalkDimensions{DimensionPerRow, ContrastAcrossMetals}→MechanismAnchoredConsolidation{SixPillarFramework, OneSentenceSynthesis}→Flashcards{OfferGeneration, SaveToFile}→DiscoverGaps{FlagMissing, OfferDeepDive}→Deliverables{SaveReviewArtifact, UpdateState}

## Rules

- Only populate matrix cells for topics with completed deep dives. Never invent half-lives or transporters from general knowledge without a source check.
- If the matrix is mostly gaps, suggest deep-diving the emptiest metal first rather than forcing a thin comparison.
- Flash card production is optional — the user decides quantity and format. Default: 10–15 cards per review session.
- After generating cards, ask "Want to go through these now?" before moving on.
