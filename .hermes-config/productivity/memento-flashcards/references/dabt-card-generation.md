# DABT Card Generation from Practice Question Database

## Source

Database at: `/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx`
446 questions from Mini-ABT Exams 1-11. Sheet name: `Questions`.
Columns: `ID, Source Exam, Question #, Question, A, B, C, D, E, F, G, H, Correct Answer, Correct Answer Text, Explanation, Topic (Primary), All Topics, Source File`

## On-Demand Generation Workflow

When user says "cards on [topic]" in the flashcard channel:

1. **Query the database** for matching questions. Use multi-column search — the keyword often appears in the answer choices, not just the question stem:

   ```python
   # Search across: Question text, Correct Answer Text, and ALL answer choices
   q_mask = df['Question'].str.contains(keywords, na=False, case=False)
   a_mask = df['Correct Answer Text'].str.contains(keywords, na=False, case=False)
   choice_mask = df[['A','B','C','D','E','F','G','H']].apply(
       lambda row: row.astype(str).str.contains(keywords, na=False, case=False).any(), axis=1
   )
   results = df[q_mask | a_mask | choice_mask].drop_duplicates(subset='ID')
   ```

   Without the choice_mask scan, you miss questions where the keyword only appears in the options (common for identify-the-correct-chelator type questions).

2. **Filter for genuine relevance.** A keyword match on choices doesn't guarantee the question is about that topic — e.g., a methylmercury question might mention "penicillamine" in a distractor option. Review each match's question text and correct answer to confirm topical relevance before making cards.

   ⚠️ **Caveat: The database's own Topic (Primary) column is unreliable.** Questions about organophosphates (parathion, pralidoxime), fluoride, and other non-metal toxicants are tagged "Metals & Metalloids" in the database. Never trust the topic column alone — always verify by reading the actual question stem and correct answer. A question's correct answer will name an actual metal or chelator if it belongs in a metals collection; if it names atropine, pralidoxime, or calcium salts, it's out of scope for that collection.

3. **Categorise matches by knowledge type.** Group matching questions into card archetypes (see below) to ensure diverse coverage rather than all questions turning into the same card type.

4. **Synthesise atomic fact pairs** from each question:
   - Distill the single piece of knowledge the question tests
   - One card per atomic fact (some questions yield 2-3 cards)
   - Format: concise FRONT prompt → precise BACK answer
   - Never reproduce the full vignette as front text — the card tests recall, not situational diagnosis
   - For "which is NOT correct" questions, reverse to a TRUE statement as the card back

5. **Import into Memento**:

   **Option A — `add` (card-by-card from a loop):** Best when curating cards individually and JSON construction is unnecessary overhead.
   ```bash
   python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add \
     --question "FRONT" --answer "BACK" --collection "DABT - <Domain>"
   ```

   **Option B — `add-quiz` (one-shot JSON batch):** Best when you already have card data as a JSON array.
   ```bash
   python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py add-quiz \
     --video-id "dabt-<topic>-<YYYY-MM-DD>" \
     --questions 'JSON_ARRAY' \
     --collection "DABT - <Domain>"
   ```
   Note: `add-quiz` requires `--video-id` — it's not optional. If you don't have a video ID, use `add` in a loop instead.

6. **Handoff — show the first card immediately.** After import, run `memento_cards.py due --collection "COLLECTION"` and present the first card's FRONT to the user. The user sees the card in the channel and understands the conversational interface IS the review system. Without this step, the user will ask "where are the cards?"

## Collection Convention

| Collection | Topics | Examples |
|------------|--------|---------|
| `DABT - Metals` | Metals & Metalloids | Arsenic, lead, cadmium, mercury, chelators, transporters |
| `DABT - Risk Assessment` | Risk Assessment & Regulatory | UFs, BMD, NOAEL vs LOAEL, RfD derivation |
| `DABT - Mechanistic` | Mechanisms, Carcinogenesis, Genotoxicity | MOA steps, AOP, Ames test, DNA repair |
| `DABT - Conduct of Studies` | Study design, interpretation, statistics | Dose selection, controls, power analysis |
| `DABT - Applied Tox` | Applied topics | Pesticides, solvents, gases, plant toxins |
| `DABT - Organ Systems` | Cross-cutting organ toxicity | Liver, kidney, neuro, CV, heme, skin |

Use the narrowest collection that fits. When in doubt, `DABT - Metals` or `DABT - Applied Tox`.

## Card Archetypes

| Question type → Card pattern | Example |
|------------------------------|---------|
| "Which X is correct?" → FRONT: Fact about X | "Which metal has NO effective chelator?" → "Cadmium" |
| "Which is NOT true about X?" → FRONT: True fact about X | "Chelator for chronic arsenic (CNS involved)?" → "BAL (dimercaprol)" |
| "What is the treatment for X?" → FRONT: X → treatment | "Antimony poisoning → treatment?" → "CaEDTA" |
| "Which X pairs with Y?" → FRONT: X → Y | "Dimercaprol (BAL) is chelator for?" → "Mercury, arsenic" |
| Vignette → mechanism | "Metal fume fever (12h post-welding) → agent?" → "ZnO (zinc oxide)" |
| Numeric fact | "OSHA blood Pb action level in workers?" → "40 μg/dL" |
| "All of the following EXCEPT" → FRONT: The misleading option as a true/false fact | "Ferritin is a clinically useful chelator?" → "FALSE (it's a storage protein)" |
| Mechanism anchor → FRONT: Overarching principle for a metal class | "What are the 3 main mechanisms of heavy metal toxicity?" → "SH binding, metal substitution, oxidative stress" |
| Integration/comparison → FRONT: Head-to-head across items | "Which of As/Cd/Cr has an effective chelator?" → "Only As (BAL/DMSA). Cd has NO effective chelator. Cr(VI) uses supportive care." |

## Card Triage During Review: Delete-and-Replace Workflow

When the user flags a card as out-of-scope for its collection during review:

1. **Delete the orphan:** `memento_cards.py delete --id CARD_ID`
2. **Query the database for proper replacements** (see On-Demand Generation Workflow above, including the choice_mask scan)
3. **Filter for genuine relevance** — a keyword match on choices doesn't guarantee the question is about the collection's topic. Review each match's question text and correct answer to confirm.
4. **Categorise by knowledge type** (same as Step 2 of generation) to ensure diverse coverage
5. **Add replacements** using the Python subprocess wrapper (see JSON Piping Workaround below) — same collection name
6. **Resume the review loop**

**Why source from the database?** The database questions are exam-realistic. A card generated from general knowledge might be technically correct but miss the exam's framing. Always prefer database-sourced cards for DABT.

## JSON Piping Workaround for `add-quiz`

The shell command-line `--questions 'JSON'` flag breaks on special characters (Unicode arrows →, superscripts ²⁺, em-dashes —, quotes within answer text). The DABT answer text is full of these.

**Always use the Python subprocess wrapper when the JSON contains special characters:**

```python
import json, subprocess, os
MEMENTO = os.path.expanduser("~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py")

with open("/tmp/cards.json") as f:
    questions = json.load(f)

cmd = [
    "python3", MEMENTO, "add-quiz",
    "--video-id", "dabt-<topic>-<seq>",
    "--questions", json.dumps(questions),
    "--collection", "DABT - <Domain>"
]
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
```

This bypasses shell interpretation entirely. The JSON file at `/tmp/cards.json` should be a JSON array of `{"question": "...", "answer": "..."}` objects.

## Card Design Pitfalls — Lessons from the As/Cd/Cr Rebuild

The original 45-card biomarker+chelator deck failed because of these structural problems. **Every deck must be checked against these before presentation:**

### Pitfall 1: Compound Cards (Multiple Facts Per Retrieval)

**Bad:** "What is the approximate half-life of cadmium in the human body and its biomarker implication?" — this tests TWO independent retrievals (a number AND a consequence). Partial knowledge → punish.

**Fix — atomic cards:** Each card tests EXACTLY ONE retrieval:
- "What is the half-life of cadmium in humans?" → ">26 years."
- "What does cadmium's long half-life imply for biomonitoring?" → "Urine Cd reflects cumulative lifetime body burden, not recent exposure."

### Pitfall 2: No Mechanism Anchors

Mnemonic-only cards (e.g., "β₂-MG = Cd renal damage") create confusable slots. Without the *why*, similar facts collapse into each other.

**Fix — add mechanism-anchor cards before specifics:**

| Layer | Card type | Example |
|-------|-----------|---------|
| **Anchor** (framework) | "What are the 3 mechanisms of heavy metal toxicity?" | SH binding, metal substitution, oxidative stress |
| **Why-specific** (mechanism) | "Why does valence determine Cr toxicity?" | Cr(VI) enters cells via sulfate transporters; Cr(III) does not |
| **What-specific** (fact) | "What is the Cr(VI) target organ?" | Lung cancer (IARC Group 1) |

Always generate 3-5 anchor cards covering the metal class's overarching principles before generating metal-specific cards. Without the anchor, the specific facts have no cognitive scaffolding to hang on.

### Pitfall 3: High Confusability Clusters

Similar facts across different metals collapse into the same memory slot (β₂-MG vs NAG vs metallothionein — all "cadmium renal biomarker" but testing different things).

**Fix — add explicit **contrast cards** and **discriminators** to each fact card:**

When generating cards for multiple similar items, add a Discriminator column to your generation plan — a one-sentence rule that prevents confusion:

| Card | Discriminator |
|------|--------------|
| β₂-MG = Cd renal tubular damage | See WHY: low-MW protein → filtered → normally reabsorbed → spills when tubules die |
| NAG = Cd early nephrotoxicity | See WHY: lysosomal enzyme → released from dying cells directly |
| Metallothionein = Cd binding | See WHY: inducible cysteine-rich protein that sequesters Cd |

### Pitfall 4: No Integration/Comparison Cards

After generating scattered metal-specific cards, add a set of **integration cards** that test head-to-head comparisons. These prevent the "I know each in isolation but can't distinguish them on the exam" problem.

| Integration question | Purpose |
|---------------------|---------|
| "Which of As/Cd/Cr has an effective chelator?" | Sharpens chelator boundaries | 
| "Rank As/Cd/Cr by half-life, shortest to longest" | Prevents half-life confusion |
| "Which of As/Cd/Cr is an essential trace element?" | Highlights the Cd/As non-essential fact |
| "Compare carcinogenic mechanisms of As, Cd, Cr" | Tests the direct vs indirect genotoxic distinction |

Generate these as the LAST batch (card archetype = Integration). Always use the pattern: scattered facts → integration comparisons → review.

### Pitfall 5: First-Pass Learning ≠ Review

When cards are newly generated (all ease_streak=0, last_user_answer=null), the user is doing first-pass learning, not spaced repetition. The user feels like they're failing at review when really they've never seen the material before.

**Fix — rate ALL cards `hard` on first pass**, regardless of accuracy. This reschedules them to 24h, which is appropriate for fresh material. (The old system rated correct answers `good`/`easy`, which pushed cards 3-7 days out — causing them to be forgotten before the second encounter.) After the 24h gap, the user can earn `good` or `easy` ratings on cards they genuinely retained.

**Concrete flow for new decks:**
1. "These are fresh cards — first-pass learning. I'll rate everything `hard` so you see them again tomorrow. Ready?"
2. Present each card, grade the answer, show back
3. Rate `hard` every time regardless of answer quality
4. When done: "34 cards reviewed. Rated all `hard` — they'll be due again in 24 hours. That's the first spaced repetition cycle."

## Card Quantity Defaults

- **Per topic request:** 10–15 cards (covers the core facts without overwhelming)
- If the database has < 10 matching questions, supplement with cards from general knowledge on the topic (sourced from the DABT reference library if available)
- If the database has > 30 matching questions, sample for diversity: cover each sub-topic at least once, avoid over-representing a single question type

## Worked Example: Chelator Cards from the Database

When the user asked for flashcards on chelators, this is the exact workflow:

### Step 1: Query the database

Use multi-column search across Question text + Correct Answer Text + all choices A-H:

```python
chelator_terms = 'chelat|BAL|dimercaprol|DMSA|succimer|EDTA|CaEDTA|deferoxamine|deferasirox|penicillamine|trientine|British anti|Lewisite|unithiol|DMPS|DMPSA|D-penicillamine|heavy metal antidote|antidote for'

q_mask = df['Question'].str.contains(chelator_terms, na=False, case=False)
a_mask = df['Correct Answer Text'].str.contains(chelator_terms, na=False, case=False)
choice_mask = df[['A','B','C','D','E','F','G','H']].apply(
    lambda row: row.astype(str).str.contains(chelator_terms, na=False, case=False).any(), axis=1
)

matches = df[q_mask | a_mask | choice_mask].drop_duplicates(subset='ID')
```

This returned 23 questions from 446. The choice_mask was essential — many chelator questions are "identify the correct antidote" type where the chelator name only appears in answer choices.

### Step 2: Categorise by knowledge type

The matching questions fell into groups mapping to specific card archetypes:

| Group | Card type | Example cards |
|-------|-----------|---------------|
| Chelator-metal matches | Which X pairs with Y | EDTA→Pb, BAL→As/Hg, penicillamine→Cu |
| Ineffective pairs | Which is NOT correct | EDTA+Hg is ineffective |
| Chelator properties | True/fact about X | BAL = 2 sulfhydryl groups |
| Antidote matching | X → treatment | OP→2-PAM, fluoride→Ca salts |
| Metal toxicology | Mechanism fact | Kidney binds metals in lysosomes |

### Step 3: Curate → import → handoff

**Curate**: Extract atomic fact pairs from each group. Some questions yield 0 cards (long vignettes testing clinical reasoning), others yield 1-2. Prioritise clear, testable fact pairs over comprehensive coverage. Discard duplicates across groups.

**Import**: Use `memento_cards.py add` in a loop — simpler than constructing JSON for individually curated cards:

```python
cmd = f"{MEMENTO} add --collection 'DABT - Chelators' --question '{front}' --answer '{back}'"
subprocess.run(cmd, shell=True, timeout=15)
```

**Handoff**: Immediately pull the first due card and present it. Without this, the user says "where are the cards?"

## Review Mode

When user says "review" or "show cards" in the flashcard channel:

1. Call `memento_cards.py due [--collection COLLECTION]`
2. Present FRONT of each due card, one at a time
3. Wait for user's free-text answer
4. **Grade and show the BACK** — confirm correct or correct the error
5. **Supplementary context (optional):** If the user answers correctly and then asks "what else?" / "another option?" or shows curiosity about alternatives, provide bonus comparative info alongside the back. Keep it brief — 1-2 sentences max. Don't add it unprompted.
6. Rate via `memento_cards.py rate --id ID --rating easy|good|hard|retire`
   - Rate even when the user didn't answer or answered "I don't know" — rate `hard` and move on
7. After rating, auto-present the next due card
8. When no more due cards: "All caught up. N cards reviewed. Next due: [time]."

### Partial / no-answer handling

- If the user says "zero idea" / "no clue" / doesn't answer → show the BACK, rate `hard`, next card
- If the user says "Hard" without answering first (treating rating as a skip) → show the BACK, rate `hard`, next card
- If the user gives a partially correct answer → show the BACK with clarification on what was right vs wrong, rate `hard`

The conversational rhythm is: FRONT → answer → BACK + grade → rating → next. If the user skips or truncates a step, fill the gap gracefully and keep the flow moving.
