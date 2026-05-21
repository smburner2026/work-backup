---
name: memento-flashcards
description: >-
  Spaced-repetition flashcard system. Create cards from facts or text,
  chat with flashcards using free-text answers graded by the agent review,
  and export/import decks as CSV.
version: 1.0.0
category: productivity
---

# Memento Flashcards — Spaced-Repetition Skill

## Overview

Local, file-based flashcard system. All data in a single JSON file at:
`~/.hermes/skills/productivity/memento-flashcards/data/cards.json`

## Commands

```bash
MEMENTO="python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py"
```

### Create a single card (simplest — use for curated card-by-card generation)
```bash
$MEMENTO add --question "What transporter does arsenic use?" --answer "AQP7/9" --collection "DABT - Metals"
```

### Batch-add from JSON (use when you have a pre-built JSON array)
```bash
$MEMENTO add-quiz --video-id "topic-name" --questions '[{"question":"Q","answer":"A"}]' --collection "DABT - Chelators"
```

### Decision: `add` vs `add-quiz`

| Command | When to use | Flags |
|---------|-------------|-------|
| `add` | Curating one card at a time from individual facts; looping in a script where JSON construction is overhead | `--question TEXT`, `--answer TEXT`, `--collection NAME` |
| `add-quiz` | Already have card data as JSON; importing a structured batch in one call | `--video-id ID`, `--questions JSON_ARRAY`, `--collection NAME` |

### See due cards
```bash
$MEMENTO due --collection "DABT - Metals"
```

### Rate a card after answering
```bash
$MEMENTO rate --id CARD_ID --rating easy|good|hard|retire --user-answer "my guess"
```

### Export to CSV (Anki-compatible)
```bash
$MEMENTO export --output ~/dabt-cards.csv
```

### Import from CSV
```bash
$MEMENTO import --file ~/dabt-cards.csv --collection "DABT - Imported"
```

### Stats
```bash
$MEMENTO stats
```

## Card Model

Each card stores: id, question, answer, collection, status (learning/retired), ease_streak, next_review_at, last_user_answer, created_at.

## Spaced Repetition Schedule

- **hard** → next review in 1 day
- **good** → next review in 3 days
- **easy** → next review in 7 days; after 3 consecutive easy ratings, card is auto-retired
- **retire** → card is permanently done

## DABT Usage

Cards are organised by DABT domain/topic as collections:
- `DABT - Metals` — transporters, half-lives, biomarkers, chelators
- `DABT - Risk Assessment` — UFs, BMD concepts, regulatory thresholds
- `DABT - Mechanistic` — MOA, AOP, carcinogenesis steps
- `DABT - Conduct of Studies` — study design, statistics, interpretation

## Workflow

1. **Generate**: user requests cards on a topic → I query the DABT database or reference materials → generate front/back pairs → batch-add to Memento
2. **Handoff**: immediately after generation, pull the first due card and present it to demonstrate the review flow. Say something like "18 cards loaded. Here's your first one:" then show FRONT. This prevents "where are the cards?" confusion — the user sees the card in the channel right away.
3. **Review**: user opens the flashcard channel on Discord → says "review" or "show me due cards" → I pull due cards from Memento → present FRONT → user answers free-text → I grade and rate
4. **Repeat**: after rating the last card, tell the user how many were reviewed and when the next batch is due

## Pitfall: Silent Card Creation

**Do not** batch-add cards and then just say "they're loaded" or "type 'review' to start." The user will ask "where?" and rightfully so. Always **show the first card immediately** after creation to make the Memento conversational flow tangible. The user needs to see the card in the channel to understand that this *is* the review interface.

## Pitfall: JSON Piping Through Shell with `add-quiz`

Passing JSON with special characters (quotes, em-dashes, arrows →, Unicode) via `--questions 'JSON'` on the shell command line breaks on escape sequences — the shell interprets `$`, `!`, backticks, and malformed quotes before Python ever sees them. This is especially common with DABT answer text containing chemical formulas (Pb²⁺, →, µg/dL).

**Don't:**
```bash
$MEMENTO add-quiz --questions '[{"question":"What → Pb²⁺?"}]' --collection "X"
# Shell mangling, syntax errors
```

**Do: Write the JSON to a file, then call memento_cards.py from a Python wrapper:**
```python
import json, subprocess, os
MEMENTO = os.path.expanduser("~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py")
with open("/tmp/cards.json") as f:
    questions = json.load(f)
cmd = ["python3", MEMENTO, "add-quiz", "--video-id", "<topic>", 
       "--questions", json.dumps(questions), "--collection", "X"]
subprocess.run(cmd, capture_output=True, text=True)
```

This avoids shell interpretation entirely and keeps the JSON intact.

## Card Triage During Review

During a review session, the user may flag a card as wrong, outdated, or **out-of-scope for its collection** (e.g., an organophosphate antidote card sitting in "DABT - Chelators"). When this happens:

1. **Acknowledge** the card doesn't belong
2. **Delete** the orphan card with `$MEMENTO delete --id CARD_ID`
3. **Source a replacement** from the project's reference database (if one exists — e.g., the DABT 446-question xlsx) — query for genuine matches on the collection's topic
4. **Batch-add replacements** with `add-quiz` (using the Python wrapper above to avoid shell escaping issues)
5. **Resume review** — the next due card comes up naturally

**Why not just delete?** Deleting without replacing leaves a knowledge gap. The user is reviewing to learn — if a card was wrong, the right information should take its place. Source the replacement from the project's canonical database, not from general knowledge, so the card reflects exam-realistic content.

**Collection purity rule:** Every card in a collection should directly test knowledge about that collection's topic. "DABT - Chelators" should only contain cards about chelation therapy, chelating agents, and metal-antidote matching. Off-topic cards erode the collection's signal.

## Pitfall: Shell Escaping with `add-quiz`

Passing JSON containing special characters (→, Pb²⁺, µg/dL, em-dashes, Unicode arrows) via `--questions 'JSON'` on the shell command line fails — the shell interprets quotes, `$`, `!`, and backticks before Python sees them.

**Don't** inline the JSON in a bash command:
```bash
# Shell mangling on special characters
$MEMENTO add-quiz --questions '[{"question":"What → Pb²⁺?"}]' ...
```

**Do** write the JSON to a file and call memento_cards.py from a Python wrapper:
```python
import json, subprocess, os
MEMENTO = os.path.expanduser("~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py")
with open("/tmp/cards.json") as f:
    questions = json.load(f)
cmd = ["python3", MEMENTO, "add-quiz", "--video-id", "<topic>",
       "--questions", json.dumps(questions), "--collection", "X"]
subprocess.run(cmd, capture_output=True, text=True)
```

This bypasses shell interpretation entirely.

## Card Triage During Review

If the user flags a card as wrong, outdated, or **out-of-scope for its collection** (e.g., an OP-antidote card in "DABT - Chelators"):

1. **Acknowledge** the card doesn't belong there
2. **Delete** the orphan: `$MEMENTO delete --id CARD_ID`
3. **Source a replacement** from the project's reference database (if one exists) — query for genuine matches on the collection's topic
4. **Batch-add replacements** using the Python wrapper above to avoid shell escaping
5. **Resume review** — natural next card comes up

**Collection purity rule:** Every card in a collection should test knowledge about that collection's topic. Off-topic cards erode the signal. Deleting without replacing leaves a knowledge gap — source replacements from canonical project data.

## Pitfall: Compound Cards

**Don't** pack multiple independent retrievals into a single card's FRONT or BACK. A card that asks "What is cadmium's half-life and its biomarker implication?" tests two separate facts: the number (>26 yr) AND the consequence (cumulative poison). The user may know one but not the other — the card punishes partial knowledge and the rating becomes meaningless.

**Recognise compound cards by:** the FRONT contains "and" / "vs" / "compared to" / a semicolon joining two independent clauses, or the BACK has two unrelated facts that could stand alone.

**Split pattern — one atomic fact per card:**

| Compound → split |
|------------------|
| "What is Cd half-life and what does it mean?" → Card A: "Cd body half-life?" → ">26 yr". Card B: "Why is Cd a cumulative poison?" → "26 yr half-life + high MT affinity + slow renal elimination" |
| "How do inorganic Pb and tetraethyl Pb biomarkers differ?" → Card A: "Inorganic Pb biomarkers?" → "Blood Pb, ZnPP, δ-ALA". Card B: "Tetraethyl Pb biomarkers?" → "Neuropsychiatric symptoms dominate; blood Pb less elevated" |
| "What is molecular mimicry and which metal uses it?" → Card A: "What is molecular mimicry in toxicology?" → "Toxic species structurally mimics endogenous molecule, hijacks its transporters". Card B: "Which metal crosses BBB via molecular mimicry?" → "Methylmercury (cysteine conjugate, mimics methionine)" |

**Review hook:** if the user struggles repeatedly on one side of a compound card, split it on the spot — retire the compound, create two atomic cards, present them separately.

## DABT Card Generation Reference

See `references/dabt-card-generation.md` for the full workflow:
- Topic-to-collection mapping
- Card archetype patterns from practice questions
- On-demand generation procedure from the 446-question database
- Review protocol (due → present → grade → rate → next)

## Post-Review Performance Assessment

After a review session where the user reports struggling ("I missed all of them", "I can't remember despite studying", "rough session"):

**Do NOT just say "try again" or "rate harder."** Analyse *why* they missed. This is distinct from grading individual cards — it's a meta-cognitive diagnosis of the study system itself.

### Common failure modes to check

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| All cards feel new despite "reviewing" | Cards were recently created (hours old) — user did first-pass learning, not spaced recall. The system presented them as due before they'd been through a single cycle. | Rate everything `hard` (24h gap). Second pass tomorrow recovers. Do not create large batches before a review session — create them the day before so first pass is a genuine recall attempt. |
| Confuses similar biomarkers for same metal (β₂-MG vs NAG vs MT for Cd) | High confusability cluster — cards test *which name* without the *why* distinction anchoring each one | Add mechanism-anchor cards first: "Why does β₂-MG appear in urine?" → "Low molecular weight protein, filtered by glomerulus, NOT reabsorbed by damaged proximal tubule". "Why is NAG elevated?" → "Lysosomal enzyme released when proximal tubular cells are damaged". The mechanism IS the mnemonic. |
| Misses one side of a paired fact | Compound card (see Pitfall: Compound Cards) | Split the card. Retire the compound, create two atomics. |
| Remembers reading the material but can't recall | Passive re-reading vs active recall — fluency illusion | Recommend retrieval practice: before looking at answers, write down what they remember. The card itself IS forced recall — the gap is between study sessions. Add a "preview" step: before the review, ask the user to verbally summarise the topic from memory. |
| Misses every Nth card in a row | Blocked practice fatigue — after 5+ cards on one sub-topic, the brain pattern-matches rather than retrieves | Interleave: mix collections. Never present more than 5 cards from a single sub-topic consecutively. If 10 Cd cards are due, intersperse with Pb or As cards. |
| Answers partially correct but grading penalised | User learned the gist, not the specific exam-relevant fact | Check card answer design: is the BACK too long? Does it state the minimum exam-worthy fact or a paragraph? Trim answers to 1-2 sentences. The card tests the fact, not the surrounding explanation (explanation can go in a separate card or as bonus context after grading). |

### Assessment protocol

When user says "I missed all of them":

1. **Check timestamps** — when were the cards created? If < 24h ago, flag first-pass learning issue.
2. **Check collection distribution** — are they all from one collection? Blocked practice issue.
3. **Scan card text** — are there compound cards? Confusable clusters?
4. **Ask one diagnostic question:** "When you studied, were you reading the material or testing yourself?"
5. **Present the fix** — a specific, actionable recommendation from the table above. Don't give generic "study more" advice.
6. **Offer to restructure** — split compounds, add anchors, rebalance collection mix. Do it on the spot if the user agrees.

### Reference file

See `references/post-review-assessment.md` for detailed case studies and worked examples of each failure mode.
