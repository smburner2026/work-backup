# Flashcard GBrain Recording — Page Templates

Consolidated reference for the 3-page gbrain write cascade that fires after every flashcard creation or review session.

## Cascade Order

```
Create cards → (1) Collection page → (2) Master index → (3) Learner profile
Review cards → (1) Miss journal entry → (2) Collection page review history → (3) Learner profile
```

## 1. Collection Page (`dabt/flashcards/<topic-slug>`)

Written at card creation. Appended to on review.

### Creation template
```markdown
---
title: <Topic> — Flashcards
type: reference
tags: [dabt, flashcards, memento, <topic-tags>]
created: YYYY-MM-DD
collection: DABT - <Collection Name>
card_count: N
status: learning
---

# <Topic> — Flashcard Collection

<N> cards covering <scope>.

## Card Concepts

### <Sub-topic 1> (N cards)
1. **Q short** — A short
2. **Q short** — A short
...

### <Sub-topic 2> (N cards)
...

## Review History
- **YYYY-MM-DD:** N cards reviewed — results
- ...

## Precision Gaps (to watch)
- <gap 1>
- <gap 2>
```

### Review History append format
```markdown
- **YYYY-MM-DD:** N cards reviewed — X easy, X good, X hard
- **Key misses:** <concept> (root cause: <cause>)
- **Precision gaps:** <gap>
```

## 2. Master Index (`dabt/flashcards/master-index`)

Updated whenever a collection is created or review history changes.

### Structure
```markdown
# DABT Flashcard Collections — Master Index

**Total cards:** N
**Status:** N learning, N retired, N due now
**Last updated:** YYYY-MM-DD

## Collections

| Collection | Cards | Created | Domain | Status |
|------------|-------|---------|--------|--------|
| [[dabt/flashcards/<slug>\|<Name>]] | N | Mon DD | Domain | Status |

## Review History

| Date | Collection | Cards Reviewed | Result |
|------|------------|---------------|--------|
| YYYY-MM-DD | Name | N | X/Y correct |

## Cumulative Performance
- **Total reviews logged:** N
- **Correct:** N (X%)
- **Pattern:** <emerging observation>
```

### Update logic
- On **creation**: add row to Collections table
- On **review**: add row to Review History table, update Cumulative Performance counts
- Never delete existing rows (history accumulates)

## 3. Miss Journal Entry (`dabt/miss-journal/YYYY-MM-DD-flashcard-review-<topic>`)

Written after each review session where cards were rated.

### Template
```markdown
# DABT Flashcard Review — <Collection Name>

## Date
YYYY-MM-DD

## Coverage
- <N> cards reviewed from [[dabt/flashcards/<slug>|<Collection Name>]]

## Results
Total reviewed: N
Easy: N
Good: N
Hard: N

## Detailed Misses

### Miss 1 — <Card front text>
**Prompt:** <exact card front>
**Answer given:** <what user said>
**Correct answer:** <card back>
**Rating:** hard
**Root cause:** <analysis>

### Miss 2 — ...
...

## Precision Gaps Identified
- <gap 1> — <one-line description>
- <gap 2>

## Pattern Observations
- <confusability clusters, compound card issues, first-pass learning indicators>
```

### After writing
1. Update collection page review history
2. Update learner profile weak areas

## 4. Learner Profile Update

### After each flashcard review session
- Add new weak areas to the Known Weak Areas list (numbered, deduped)
- Add new precision gaps to the Precision Gaps section
- Update the flashcard table in Completed Study if counts changed
- Update cumulative review stats (total reviewed, running accuracy)

## Source Data

Read from Memento cards.json at:
`~/.hermes/skills/productivity/memento-flashcards/data/cards.json`

Card fields: `id`, `question`, `answer`, `collection`, `status`, `review_history[]` (each review has `rating`, `date`), `next_review_at`, `created_at`

## Tools

- `mcp_gbrain_put_page` — write all pages
- `mcp_gbrain_query` — verify the page is searchable after write
