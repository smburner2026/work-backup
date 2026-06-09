---
name: memento-flashcards
description: >-
  Spaced-repetition flashcard system. Create cards from facts or text,
  chat with flashcards using free-text answers graded by the agent review,
  and export/import decks as CSV.
version: 1.3.0
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
   - **Speed rule**: When the user names a topic or block, go DIRECTLY to card production. Do NOT multi-round session-search archaeology to map what was covered unless the topic is genuinely ambiguous. Trust the named topic. Generate cards in one Python call with inline stagger. If the user called out slowness, they want faster pipeline.
   - **Inline stagger pattern**: When creating new cards in a Python script (using `add-quiz` via subprocess), spread their `next_review_at` in the same pass. Do not create all cards with the same timestamp and then separately backfill — that doubles the work. Instead, after adding the cards, read the JSON, find the newly created ones (by `video_id` match), and stagger them inline:

     ```python
     import json
     from datetime import datetime, timedelta, timezone
     from pathlib import Path

     cards_file = Path.home() / '.hermes/skills/productivity/memento-flashcards/data/cards.json'
     data = json.loads(cards_file.read_text())
     now = datetime.now(timezone.utc)
     new_cards = [c for c in data['cards'] if c.get('video_id') == '<topic-slug>']
     stagger_days = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11]
     for i, card in enumerate(new_cards):
         card['next_review_at'] = (now + timedelta(days=stagger_days[i % len(stagger_days)])).isoformat()
     cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
     ```
     
     This keeps creation + stagger as one pipeline step. The first card comes due tomorrow, not immediately, preventing the "50 cards due on day 1" flood.
   - **Self-check**: Before presenting the first card, verify your own card framing is internally consistent (e.g., don't say "three categories" then list four). The user WILL catch mismatches. If a card needs fixing mid-review, fix the card text immediately after rating. Track fixes to prevent recurrence.
2. **Optional recording**: If a local log is desired, save a summary of the new collection (collection name, card count, topics) to a local markdown file (e.g., `~/.hermes/data/flashcard-log.md`). Otherwise, skip — the cards are persisted in Memento's `cards.json`.
3. **Handoff**: immediately after card creation, pull the first due card and present it to demonstrate the review flow. Say something like "18 cards loaded. Here's your first one:" then show FRONT. This prevents "where are the cards?" confusion — the user sees the card in the channel right away.
4. **Review**: user opens the flashcard channel on Discord → says "review" or "show me due cards" → I pull due cards from Memento → present FRONT → user answers free-text → run the **Precision Loop** (below) → rate the card

   ### Precision Loop (required for TempMoon — confirmed May 27 session)
   
   Do NOT just rate and move on. Execute these sub-steps on every card:
   
   a. **Identify** — pinpoint the exact terminology or fact gap. Not "you're wrong" but *"you said X, the exam asks for Y."*
   b. **Correct** — state the correct phrasing verbatim in compact, exam-relevant form. Include the standard term (e.g., *Hazard Identification* not "Hazard assessment").
   c. **User repeat** — prompt the user to repeat the corrected phrasing back. This locks the precise retrieval pathway.
   d. **Rate** — assign `hard` (missed entirely), `good` (near miss, partial recall), or `easy` (solid retrieval). Calibrate honestly.
   
   **Pacing calibration**: Watch for brevity signals. If the user abbreviates their answer ("Cohort = rare, case control = rare"), they understand the core concept and want to move on. Skip step (c) once they've demonstrated grasp of the key distinction. Reserve the full repetition for cards where they genuinely missed the concept. Users who catch YOUR errors mid-review are advanced enough to self-assess — trust their speed signals.
   
   **Deep-dive extension**: If the error reveals a conceptual gap beyond terminology (e.g., confusing the *mechanism* not just the *name*), add a brief mechanism-anchor explanation after step (c) before rating.

**Comparison table technique**: When the user keeps mixing up 2+ related concepts across multiple cards (e.g., cohort vs case-control vs cross-sectional), stop correcting card-by-card. Build a **side-by-side comparison table** anchoring the key distinguishing dimensions (measure, direction, when preferred). Present it ONCE as a reference frame. The table IS the mnemonic — it gives the user a single structured image to retrieve from, rather than trying to keep 3 separate fact-sets straight. Then test the next card against the table. Works for any N-way confusability cluster.
   
   **Card scope clarification**: If the user asks "what do you mean by X?" or "can you clarify the question?", the card's FRONT is too ambiguous. Clarify the scope **without giving away the answer** — state what domain the card tests, not the specific fact. Example: "This card is asking which regulatory agencies use which threshold names for safe exposure levels." Then present the card again. If the FRONT is genuinely confusing, fix the card text after rating.

**Daily card cap (user preference — confirmed Jun 4):** User wants max ~20 cards due per session, not a flood of 40+. When due counts exceed 20, stagger the excess across future days using the daily-cap stagger script (below). The daily briefing cron should also reflect this cap — if >20 are due, the briefing notes that some have been spread out.

**Mid-session continuity rule (confirmed Jun 4):** If the agent runs a stagger script mid-session (to cap daily due cards), it must NOT reshuffle the cards the user has already started reviewing. The user was on card 8 of 20 when the stagger ran — they said "start from the eight we've already done." Preserve the current review position. Only stagger cards that haven't been presented yet in this session. If a stagger is needed mid-session, apply it to the remaining unseen cards only, then resume from where the user left off.

**Daily-cap stagger script:**
```python
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

cards_file = Path.home() / '.hermes/skills/productivity/memento-flashcards/data/cards.json'
data = json.loads(cards_file.read_text())
now = datetime.now(timezone.utc)
MAX_PER_DAY = 20

# Find due cards
due_cards = [c for c in data['cards']
             if c['status'] == 'learning'
             and datetime.fromisoformat(c['next_review_at']) <= now]

# Count existing future schedule per day
future_counts = defaultdict(int)
for c in data['cards']:
    if c['status'] == 'learning':
        dt = datetime.fromisoformat(c['next_review_at'])
        if dt > now:
            future_counts[dt.date()] += 1

# Build capacity map for next 10 days
schedule = {}
for i in range(10):
    day = (now + timedelta(days=i)).date()
    schedule[day] = max(0, MAX_PER_DAY - future_counts.get(day, 0))

# Distribute due cards
import random; random.shuffle(due_cards)
for card in due_cards:
    for day in sorted(schedule):
        if schedule[day] > 0:
            card['next_review_at'] = datetime.combine(
                day, datetime.min.time().replace(hour=12),
                tzinfo=timezone.utc
            ).isoformat()
            schedule[day] -= 1
            break

cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
```

**Card triage**: If a card is compound, out-of-scope, or wrong, defer to Card Triage (section below) before rating.
5. **Optional session log**: After the review session ends (all due cards rated), optionally save a summary to a local markdown file (e.g., `~/.hermes/data/flashcard-log.md`) recording cards reviewed, ratings breakdown, and any precision gaps identified. This is optional — the Memento system tracks all ratings internally.
6. **Wrap up**: Tell the user how many were reviewed and when the next batch is due.

## Daily Card Limit — Max 20 Per Session

The user has a hard preference: **no more than 20 cards due per day**. When the due count exceeds 20, stagger the excess across future days before starting the review. This prevents overwhelm and keeps sessions focused.

### Stagger procedure (run before review when due > 20)

```python
import json, random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

cards_file = Path.home() / '.hermes/skills/productivity/memento-flashcards/data/cards.json'
data = json.loads(cards_file.read_text())
now = datetime.now(timezone.utc)
MAX_PER_DAY = 20

# Find all due cards
due_cards = [c for c in data['cards']
             if c['status'] == 'learning'
             and datetime.fromisoformat(c['next_review_at']) <= now]

# Count already-scheduled future cards per day
future_counts = defaultdict(int)
for card in data['cards']:
    if card['status'] == 'learning':
        review_at = datetime.fromisoformat(card['next_review_at'])
        if review_at > now:
            future_counts[review_at.date()] += 1

# Build capacity map for next 10 days
schedule = {}
for i in range(10):
    day = (now + timedelta(days=i)).date()
    schedule[day] = max(0, MAX_PER_DAY - future_counts.get(day, 0))

# Distribute due cards across days with capacity
random.shuffle(due_cards)
for card in due_cards:
    for day in sorted(schedule):
        if schedule[day] > 0:
            review_time = datetime.combine(day, datetime.min.time().replace(hour=12), tzinfo=timezone.utc)
            card['next_review_at'] = review_time.isoformat()
            schedule[day] -= 1
            break

cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\\n')
```

### Pitfall: Staggering mid-session
If the user interrupts a review session to request staggering, the cards already rated in that session have future `next_review_at` dates. Only the remaining unrated due cards get spread. Run the stagger script AFTER the interruption, not before — otherwise you'd reschedule cards the user just answered.


## Resetting and spreading due dates (e.g., 10-20 per day)

When you want to clear the current due backlog and spread reviews evenly over the coming days (e.g., 10‑20 cards per day), use the following procedure. This is useful after a large batch of new cards or when the review schedule has become uneven.

```python
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

cards_file = Path.home() / '.hermes/skills/productivity/memento-flashcards/data/cards.json'
data = json.loads(cards_file.read_text())
now = datetime.now(timezone.utc)

# Desired cards per day (adjust as needed)
CARDS_PER_DAY = 15  # change to 10‑20 as preferred

# Reset all learning cards to have no review date (they will be scheduled from today)
for card in data['cards']:
    if card['status'] == 'learning':
        # Remove any existing next_review_at; we will set fresh schedule below
        pass

# Build list of learning cards
learning_cards = [c for c in data['cards'] if c['status'] == 'learning']

# Distribute starting tomorrow (you can change start date)
start_date = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc) + timedelta(days=1)
for idx, card in enumerate(learning_cards):
    day_offset = idx // CARDS_PER_DAY
    due_date = start_date + timedelta(days=day_offset)
    # Set to noon UTC for consistency
    card['next_review_at'] = datetime.combine(due_date.date(), datetime.min.time().replace(hour=12), tzinfo=timezone.utc).isoformat()

# Save
cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\\n')
print(f\"Rescheduled {len(learning_cards)} cards to ~{CARDS_PER_DAY} per day starting {start_date.date()}.\")
```

After running this script, verify the new distribution with:

```bash
$MEMENTO stats
```

You should see a manageable due count (roughly CARDS_PER_DAY) for the next days.

**Note:** This operation discards the current spaced‑repetition intervals and starts a fresh schedule. Use it only when you want to reset the clock (e.g., after a large import or when the review backlog has grown unevenly). For routine adjustments, prefer the daily‑cap stagger script described earlier.

## Mid-Session Resumption

When a user interrupts a review session and returns later, **do not restart from card 1**. Continue from where they left off:

1. Pull the current due list from Memento
2. The cards already rated in the prior session now have future `next_review_at` dates — they won't appear in the due list
3. The remaining unrated cards are still due — present the next one in sequence
4. If the user specifies "start from card N" or "pick up where we left off," respect that directly

### Pitfall: Restarting from card 1
Users find it frustrating when the agent re-presents cards they already answered. The Memento system handles this automatically — rated cards drop out of the due list. Trust the system, don't second-guess it.

## Scheduled Review — Cron Automation

Memento's spaced repetition is only effective when cards are **reviewed on their due dates**, not whenever the user feels like it. For TempMoon, the system runs a daily morning briefing (`08:00 UTC+7`) that proactively notifies the user about due cards, eliminating the "brush it off" failure mode.

### Architecture

```
Cron job (no_agent, script mode)
    │ daily 01:00 UTC
    ▼
daily-flashcard-reminder.py
    │ checks Memento stats
    ▼
Discord delivery — formatted briefing
    │ user says "review"
    ▼
Agent (live session) — interactive Memento loop
    │ Precision Loop on each card
    ▼
memento rate — updates next_review_at
```

### Daily Briefing Script

Location: `~/.hermes/scripts/daily-flashcard-reminder.py`
Runs in `no_agent=True` mode (no LLM tokens — pure script → stdout → delivery).

The script:
1. Calls `memento_cards.py stats` for total/collection counts
2. Calls `memento_cards.py due --collection <name>` per collection for due counts
3. Formats a Discord-friendly message with per-collection progress bars
4. Includes a CTA: "Reply \`review\` to start a session"

### Cron Registration

```bash
hermes cron create \
  --name "Daily flashcard briefing" \
  --schedule "0 1 * * *" \
  --script daily-flashcard-reminder.py \
  --deliver origin \
  --no-agent
```

Schedule: `0 1 * * *` = 08:00 UTC+7 daily.

### Backfill Procedure — First-Time Spacing

When cards are created during teaching sessions but never formally rated through Memento, **all of them come due at once** (because `next_review_at` = creation time). Presenting 50+ cards to the user in one go defeats spaced repetition.

**Fix — one-time mass backfill:**

```python
# Set all cards with null last_user_answer to 3 days from now
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

cards_file = Path.home() / '.hermes/skills/productivity/memento-flashcards/data/cards.json'
data = json.loads(cards_file.read_text(encoding='utf-8'))
now = datetime.now(timezone.utc)
for card in data['cards']:
    if card.get('last_user_answer') is None and card['status'] == 'learning':
        review_at = datetime.fromisoformat(card['next_review_at'])
        if review_at <= now:
            card['next_review_at'] = (now + timedelta(days=3)).isoformat()
cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
```

This spreads the entire backlog over 3-day intervals. As the user reviews each card, the proper rating (hard/good/easy) adjusts the schedule from there. Do this **before** the first cron run after a large card creation session.

### Interaction Pattern

1. Cron delivers the briefing to the user's channel
2. User replies **`review`** → agent enters interactive Memento loop (see Workflow Step 4)
3. User replies **`review [collection name]`** → agent filters to that collection
4. After the session, agent rates all cards (see Workflow Step 5)
5. Next morning, the cron shows updated due counts reflecting the new review dates

### Pitfall: Cron-Only vs Interactive

The cron delivers **notification only** — it cannot run the interactive review loop. Do not try to make the cron present cards one-by-one. The cron's job is to **remind and prompt**, not to review. The actual card-by-card review requires the live agent in the channel.

### Pitfall: Backlog Before Cron

If you set up the cron before backfilling unrated cards, the first briefing will say "104 cards due" and overwhelm the user. Always run the backfill procedure first, so the due count is manageable (single digits) on day one.

### Archiving a Collection (Bulk Retire with Reversible Dates)

When the user asks to set aside a flashcard collection for later (e.g., "archive the Metal Talks cards for now, I'll come back to them"), use a date-based archive: push every learning-status card in the collection to `next_review_at = now + 365 days`. This removes them from due-checks without deleting any data and is fully reversible.

**Archive script (from Python):**

```python
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

cards_file = Path.home() / '.hermes/skills/productivity/memento-flashcards/data/cards.json'
data = json.loads(cards_file.read_text())
now = datetime.now(timezone.utc)
target_collection = "DABT - Metals"  # ← set to whatever the user named

count = 0
for card in data['cards']:
    if card.get('collection') == target_collection and card.get('status') == 'learning':
        card['next_review_at'] = (now + timedelta(days=365)).isoformat()
        count += 1

cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print(f"Archived {count} cards in '{target_collection}'")
```

**Restore script (when user wants them back):**

```python
target_collection = "DABT - Metals"  # ← same collection name
restore_offset = timedelta(hours=1)  # due right away so user can start

count = 0
for card in data['cards']:
    if card.get('collection') == target_collection and card.get('status') == 'learning':
        card['next_review_at'] = (now + restore_offset).isoformat()
        count += 1

cards_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print(f"Restored {count} cards in '{target_collection}' — due in 1 hour")
```

**Verification after archive:** Run `memento_cards.py due --collection "X"` or query the JSON file directly to confirm zero due cards in the archived collection. Then confirm to the user: "Archived — 30 Metal Talks cards pushed to [date]. None will appear in daily due checks. Say the word when you want them back."

**Caveats:**
- This does NOT affect cards that were already `retired` or have non-learning status — those have already aged out of the deck.
- The archive is date-based only, not flagged in a separate metadata field. If the user has cards due naturally in >365 days (from `easy` ratings), those survive the archive sweep unintentionally — but in practice, `easy` ratings only push 7 days out, so 365 is a clean sweep.
- Always confirm the *exact* collection name with the user before archiving. If they say "archive Metal Talks" and there's both `DABT - Metals` and `DABT - AsCdCr Deepdive`, clarify which one.

### Pitfall: Daily Reminder Script Crashes on Empty Subprocess Output

The `daily-flashcard-reminder.py` script at `~/.hermes/scripts/daily-flashcard-reminder.py` calls `memento_cards.py` via `subprocess.run()` and immediately does `json.loads(result.stdout)`. If the subprocess returns empty stdout (e.g., `HERMES_HOME` not set, script not found, or Python error), this produces the unhelpful error `Expecting value: line 1 column 1 (char 0)`.

**Fix:** The `run_cmd()` function must check `result.returncode` and `result.stdout.strip()` before calling `json.loads`. A fixed version of the script is at `scripts/daily-flashcard-reminder-fixed.py` within this skill directory. To apply the fix:

```bash
cp ~/.hermes/skills/productivity/memento-flashcards/scripts/daily-flashcard-reminder-fixed.py ~/.hermes/scripts/daily-flashcard-reminder.py
```

**Verification after fix:** Run `python3 ~/.hermes/scripts/daily-flashcard-reminder.py` — should output a formatted briefing card with per-collection due counts, not an error.
When pulling due cards by question text (e.g., searching for "BMR"), verify the card ID matches the question you're discussing before calling `rate`. It's easy to accidentally rate a different card with a similar question. Always confirm the ID from the due list output, not from memory.

### Pitfall: Vague Card FRONT

If the user says "this is unclear" or "what do you mean by X?", the card's FRONT is too ambiguous — it doesn't specify what's being tested. Different from Framing Mismatch (below) where FRONT contradicts BACK; here the FRONT is just vague.

**Example:** "Name the key safety thresholds and when each is used." — which thresholds? How many? What level of detail? The user had no way to know the card expected 5 agency-specific acronyms.

**Fix mid-review:**
1. Clarify the scope **without giving away the answer** — state what domain the card tests, not the specific fact
2. After rating, **patch the card text** to be specific: "Name the 5 safety threshold standards and match each to its regulatory agency: EPA, WHO, Health Canada, OSHA/ACGIH, ECHA/REACH."
3. Use `execute_code` to patch the JSON directly (find card by ID, update `question` field)

**Prevention:** When creating cards, the FRONT should constrain the answer scope. "Name the 5 X and match each to Y" is better than "Name the key X." Vague FRONTs waste review time and erode trust.

### Pitfall: Card Framing Mismatch Caught Mid-Review

The user may catch that your card's FRONT framing contradicts its own answer — e.g., asking for "three categories" but the answer lists four. This erodes trust and wastes time.

**Prevention:** Before presenting the first card from a new batch, skim the question-answer pairs for internal consistency. Does the question scope match the answer scope? Does the question constrain the answer properly? If a question says "three X" but the canonical answer is "four X," fix the question before presenting.

**When caught mid-review:** 
1. Acknowledge the error immediately ("Fair — you're right, the card was wrong")
2. Rate the card based on what the user actually knew (their answer was penalised by the bad framing — adjust rating upward if their concept was right)
3. Fix the card text on the spot (patch the question or answer to resolve the inconsistency)
4. Continue to next card without dwelling

## Pitfall: Silent Card Creation

**Do not** batch-add cards and then just say "they're loaded" or "type 'review' to start." The user will ask "where?" and rightfully so. Always **show the first card immediately** after creation to make the Memento conversational flow tangible. The user needs to see the card in the channel to understand that this *is* the review interface.

**Exception — user signals session end:** If the user explicitly says they're done for the session (e.g., "we are done for today", "that's enough for now", "wrap it up"), do NOT force a card presentation. Respect their closing signal — instead, note the first card's topic in your summary so they know what to expect tomorrow. Example: "First card coming due tomorrow: SD vs SE — which describes individual animal variability and which describes precision of the mean estimate." This previews the content without demanding interaction.

## Pitfall: JSON Piping Through Shell with `add-quiz`

Passing JSON with special characters (quotes, em-dashes, arrows, Unicode) via `--questions 'JSON'` on the shell command line breaks on escape sequences — the shell interprets `$`, `!`, backticks, and malformed quotes before Python ever sees them. This is especially common with DABT answer text containing chemical formulas (Pb²⁺, →, µg/dL).

**Don't:**
```bash
$MEMENTO add-quiz --questions '[{"question":"What -> Pb²⁺?"}]' --collection "X"
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

## Pitfall: Reviewing Cards the User Already Got Right

In targeted review sessions, the user may say something like "skip the ones I got right yesterday" or "just give me the hard ones." This goes beyond the Conversational Review Gap — it's an explicit workflow preference: **don't re-present cards rated good or easy, only hard/miss.**

**How this manifests:** Agent pulls due cards and starts from card #1, which was rated good yesterday. User pushes back: "I don't have time to go through all the cards that were good."

**Prevention:** When entering a targeted review (hard/miss only), cross-reference the due list against Memento's rating history. Cards rated good or easy yesterday should be skipped entirely — they're due according to Memento's schedule but the user explicitly doesn't want them today. Only present cards that were rated hard or missed.

**When the user corrects you mid-session:** Acknowledge immediately, check Memento's ratings, and restart from the hard/miss cards only. Do not continue with good/easy cards unless the user explicitly asks for them.

## Pitfall: Conversational Review Gap

Cards reviewed conversationally in a prior session (graded verbally, no `memento rate` call) will still show as due/never-reviewed in the Memento tool. Their `last_user_answer` stays `null`, `next_review_at` stays at creation time.

**How this manifests:** The agent pulls due cards, starts from card #1 (the earliest created), and presents a card the user already answered — making the user feel the agent isn't tracking progress.

**Prevention (add to Workflow Step 4):** Before pulling due cards for a collection, call `session_search` with the collection topic to check for prior verbal review sessions. If matches exist, inspect which cards were discussed (check conversation transcript for card topics covered). Skip those cards and start from the first card the user *hasn't* seen in a verbal session.

**When the user corrects you mid-session (as happened May 27):** Immediately acknowledge, skip the card, and start from further in the due list. After the session, consider whether to backfill the verbally-reviewed cards into Memento by running `rate` on each one with the rating from the verbal session. This keeps Memento's state truthful and prevents recurrence next review cycle.

## Trigger: Targeted Review From Prior Session

When the user asks for cards from a *specific prior session* by rating level — phrases like:
- "Let's do the hard risk assessment flash cards from yesterday"
- "Show me the ones I missed"
- "The difficult cards we went through"
- "Hit me with the hard ones again"

**Do NOT** just pull all due cards. The user wants a focused pass at their weak spots. Execute this workflow:

### Step 1 — Find prior review data
Call `session_search()` with the collection name + a date/time reference. Look for review session records or conversation transcripts that match:

- The collection the user named ("risk assessment", "metals", etc.)
- The time reference ("yesterday", "last session", "May 27")
- The rating level ("hard", "miss", "difficult")

### Step 2 — Extract the hard/miss card topics
Read the session transcript or Memento rating history. Look for cards rated `hard` — these are the specific card topics that need re-testing.

Identify hard-rated cards by checking Memento's `last_user_answer` and rating history for the collection.

### Step 3 — Map to Memento cards
Pull the collection's due cards from Memento (`$MEMENTO due --collection "DABT - Risk Assessment"`). For each hard/miss topic from Step 2, find the matching Memento card by:
- Matching keywords from the hard card's description to the Memento card's `question` field
- Or cross-reference any `video_id` / topic grouping that connects the session data to Memento's grouping

Present those cards **first**, in the order they appear in the session data (hard first). Use the standard Precision Loop from Workflow Step 4.

### Step 4 — Scope the session to hard/miss ONLY
After the targeted hard/miss cards are exhausted, **stop**. Do NOT automatically continue with the rest of the due cards. The user asked for weak-spot review specifically — dumping the full due pile after defeats the purpose. If they want more, they'll ask. Exception: if the user explicitly says "keep going" or "show me the rest," then continue with remaining due cards.

### Reference files
- `references/risk-assessment-full-deck-review-may28.md` — complete 38-card Risk Assessment review with hard/miss breakdown. Use as template for session review parsing.
- `references/risk-assessment-full-deck-review-jun1.md` — 47-card rapid-fire review. Hard cards: NRC terminology, 4 UF types, study durations, limit dose direction, irritation vs corrosion, IARC groups, OECD guidelines. Trend: hard count dropped from 18→10 vs May 28.
- `references/hard-deck-replay-jun3.md` — 12-card hard replay. 75% first re-test. 3 remaining gaps: threshold names, subacute/subchronic, OECD 414/416/443.

### Protocol: Backfilling Verbal Reviews into Memento

When you've confirmed (via session_search) that specific cards were reviewed conversationally, rate them into Memento so they don't reappear as due:

```bash
$MEMENTO rate --id CARD_ID --rating good --user-answer "verbal session, no typed answer"
```

Backfill **immediately after** the session where the conflict was discovered, not later.

## Rapid-Fire Review Mode

Reference: `references/rapid-fire-dabt-review.md` — covers STT garble patterns, duplicate card detection, and rapid-fire calibration signals.

When the user wants to push through all due cards in one sitting (e.g., "I want to go through all of the flashcards today"), adapt the Precision Loop:

| User performance | Loop intensity |
|----------------|----------------|
| `good` (right concept, clean phrasing) | Skip precision loop. Say "good" + 1 sentence of polish if useful → rate `good` → next card |
| `hard` (concept right, precision off) | Run full loop: Identify → Correct → User Repeat → Rate `hard` |
| `miss` (concept wrong or wrong question) | Run full loop + mechanism anchor |

This trades depth for volume — ideal for first-pass learning on a fresh deck where most cards are due. The full loop on every card would make a 38-card deck take 3 hours instead of 45 minutes. Reserve the full loop for cards that genuinely need it.

**Signal to switch back to full-loop mode:** user consistently misses 3+ cards in a row → the deck has deeper conceptual gaps that rapid review won't fix. Pause, diagnose (see Post-Review Performance Assessment), and switch to a deep-dive format.

## Pitfall: Voice-to-Text (STT) Garbling During Live Reviews

TempMoon uses voice-to-text for flashcard answers. STT frequently garbles technical terms — the user's knowledge is correct but the transcription is not. Common garbles:

| STT output | Likely intended | Domain |
|------------|----------------|--------|
| CIP 450 / CIP four five fifty | CYP450 | Biotransformation |
| NOAA L / NOADL | NOAEL | Risk Assessment |
| certainty factor | uncertainty factor | UFs |
| CBCK / CIPK | PBPK | PK modeling |
| RFC | RfC | Reference Concentration |
| hazard assessment | hazard identification | Red Book Step 1 |

**Rule: interpret phonetically and structurally before assuming the user is wrong.** If the garbled answer is phonetically close to the correct term AND structurally fits the question (right number of items, right concept), treat it as correct and move on. If genuinely ambiguous, confirm: *"Did you say [X] or [Y]?"* — but err on the side of trust.

The user will correct directly if misread. Do NOT penalize STT artifacts as knowledge gaps — that erodes the review flow and wastes time.

## Pitfall: Speech-to-Text (STT) Garble

The user frequently uses voice-to-text. STT routinely mangles technical terms — "certainty" for "uncertainty", "CBPK" for "PBPK", "NOAL" for "NOAEL", "Cynogen" for "Carcinogen", etc. This happens 6+ times per review session.

**Rules:**
1. **Never assume the answer is wrong based on STT output alone.** Read context to reconstruct intent.
2. **If conceptually correct but term garbled** → accept, correct term in BACK, rate on actual knowledge.
3. **If user says "STT screwed up"** → immediately correct rating and acknowledge. Don't defend.
4. **Present correct term clearly** in BACK so user sees the right spelling regardless.

Common STT corruptions and their actual terms are catalogued in `references/rapid-fire-dabt-review.md`.

## Pitfall: Missing Cards for Hard-Review Topics

When using the targeted review workflow, the session data may flag topics as "hard" that **have no corresponding Memento card**. This happens when the topic was discussed during a session but no card was ever created for it (e.g., IARC classifications, OECD guideline numbers, irritation vs corrosion were hard topics from June 1 but never made into the deck).

**Detection:** After Step 3 (map to Memento cards), check if every hard/miss topic from the session data found a matching Memento card. Topics with no match are orphan gaps.

**Fix:** Present the orphan gaps to the user as a list: *"These topics were flagged as hard but don't have cards yet: [list]. Want me to create cards for them now?"* Create cards on the spot if the user agrees. This prevents the same gap from recurring next session — the review identified the weakness, but without a card, there's no mechanism to re-test it.

**Prevention:** When logging review session data, tag each hard/miss item with `[CARD EXISTS]` or `[NO CARD]` based on whether a Memento card was matched during the review. This makes gap detection trivial in future sessions.

## Pitfall: Duplicate Cards

If two cards in the same review session ask essentially the same question (e.g., "systemic vs local toxicant" and "local vs systemic effect"), flag it immediately and offer to delete the weaker duplicate with `$MEMENTO delete --id CARD_ID`. Prevents wasted review time and keeps deck quality high.

### Pitfall: Compound Cards

**Don't** pack multiple independent retrievals into a single card's FRONT or BACK. A card that asks "What is cadmium's half-life and its biomarker implication?" tests two separate facts: the number (>26 yr) AND the consequence (cumulative poison). The user may know one but not the other — the card punishes partial knowledge and the rating becomes meaningless.

**Recognise compound cards by:** the FRONT contains "and" / "vs" / "compared to" / a semicolon joining two independent clauses, or the BACK has two unrelated facts that could stand alone.

**Split pattern — one atomic fact per card:**

| Compound → split |
|------------------|
| "What is Cd half-life and what does it mean?" → Card A: "Cd body half-life?" → ">26 yr". Card B: "Why is Cd a cumulative poison?" → "26 yr half-life + high MT affinity + slow renal elimination" |
| "How do inorganic Pb and tetraethyl Pb biomarkers differ?" → Card A: "Inorganic Pb biomarkers?" → "Blood Pb, ZnPP, δ-ALA". Card B: "Tetraethyl Pb biomarkers?" → "Neuropsychiatric symptoms dominate; blood Pb less elevated" |
| "What is molecular mimicry and which metal uses it?" → Card A: "What is molecular mimicry in toxicology?" → "Toxic species structurally mimics endogenous molecule, hijacks its transporters". Card B: "Which metal crosses BBB via molecular mimicry?" → "Methylmercury (cysteine conjugate, mimics methionine)" |

**Review hook:** if the user struggles repeatedly on one side of a compound card, split it on the spot — retire the compound, create two atomic cards, present them separately.

### Pitfall: Multi-Part Card Found Mid-Review

Some cards in the existing deck have a FRONT that asks two separate questions joined by "and" or a semicolon (e.g., "What is the formula for Vd, AND does a high Vd mean fast or slow elimination?"). This is distinct from the Compound Cards pitfall above — that one governs card CREATION; this one governs LIVE REVIEW of cards already in the deck.

When the user answers only one part:

1. **Acknowledge** the correct part, then supply the missed part verbatim
2. **Rate `good`** — the gap is in the card design (split focus), not a knowledge gap. Reserve `hard` for genuine conceptual misses
3. **Split after the session** — retire the compound, create two atomic cards. Present them in the next review so each tests one fact independently

**Exception:** If the user expressly says "this question is confusing" or "I'm not sure what you're asking," split mid-session. Otherwise, keep momentum and fix post-review.

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
| Confuses paired/grouped concepts (cohort vs case-control vs cross-sectional; Phase I vs Phase II) | Structural confusability — user knows each concept exists but keeps assigning the wrong attributes to the wrong one (e.g., "case-control generates incidence" — that's cohort) | **Comparison table technique**: build a side-by-side table anchoring the key distinguishing dimensions (measure, direction, when preferred). Present it ONCE as a reference frame, then test against the table. The table IS the mnemonic. Works for any N-way confusability cluster. For TempMoon specifically: cohort (RR/forward/rare-exposure), case-control (OR/backward/rare-outcome), cross-sectional (prevalence/snapshot/no-causation). |
| Misses one side of a paired fact | Compound card (see Pitfall: Compound Cards) | Split the card. Retire the compound, create two atomics. |
| Remembers reading the material but can't recall | Passive re-reading vs active recall — fluency illusion | Recommend retrieval practice: before looking at answers, write down what they remember. The card itself IS forced recall — the gap is between study sessions. Add a "preview" step: before the review, ask the user to verbally summarise the topic from memory. |
| Misses every Nth card in a row | Blocked practice fatigue — after 5+ cards on one sub-topic, the brain pattern-matches rather than retrieves | Interleave: mix collections. Never present more than 5 cards from a single sub-topic consecutively. If 10 Cd cards are due, intersperse with Pb or As cards. |
| Answers partially correct but grading penalised | User learned the gist, not the specific exam-relevant fact | Check card answer design: is the BACK too long? Does it state the minimum exam-worthy fact or a paragraph? Trim answers to 1-2 sentences. The card tests the fact, not the surrounding explanation (explanation can go in a separate card or as bonus context after grading). |
| Systematic direction errors (multiply vs divide, input vs output, adds vs replaces) | User learns concepts direction-agnostic first — knows the components exist but doesnt anchor which direction they flow | After correction on a direction error, explicitly contrast the two directions side-by-side in a 2-column comparison. E.g., UF = divisor (POD / UF = RfD), not multiplier (POD x UF = ?). Add a separate orientation card to the deck that tests the direction in isolation. |

### Assessment protocol

When user says "I missed all of them":

1. **Check timestamps** — when were the cards created? If < 24h ago, flag first-pass learning issue.
2. **Check collection distribution** — are they all from one collection? Blocked practice issue.
3. **Scan card text** — are there compound cards? Confusable clusters?
4. **Ask one diagnostic question:** "When you studied, were you reading the material or testing yourself?"
5. **Present the fix** — a specific, actionable recommendation from the table above. Don't give generic "study more" advice.
6. **Offer to restructure** — split compounds, add anchors, rebalance collection mix. Do it on the spot if the user agrees.

### Reference files
- `references/post-review-assessment.md` — detailed case studies and worked examples of each failure mode
- `references/risk-assessment-full-deck-review-may28.md` — full 38-card Risk Assessment review session (ratings, new precision gaps, direction error pattern, protocol used)
- `references/epi-study-designs-confusability.md` — cohort vs case-control vs cross-sectional comparison table, memory hooks, common errors (frequently confused by TempMoon)
- `references/review-jun5-2026.md` — 20-card mixed collection review (Risk Assessment + Conduct of Studies), 3 hard: linear non-threshold term, cohort direction, first-pass routes enumeration
