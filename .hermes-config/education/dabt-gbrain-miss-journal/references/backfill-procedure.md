# Backfill — Session Miss Journal Reconstruction

Use when you discover drill/deep-dive sessions happened before the `dabt-gbrain-miss-journal` skill was created, or on a platform/agent that wasn't writing to G-Brain.

## Trigger

- User asks "are all my misses recorded in gbrain?"
- You audit G-Brain and find session dates with no corresponding `dabt/miss-journal/YYYY-MM-DD-*` page
- A new study platform or agent model was used that didn't have the inline-write hook

## Procedure

### 1. Discover What's Missing

```
session_search() — browse recent sessions
session_search(query="DABT drill|DABT deep dive", limit=10, sort="newest")
```

For each returned session, check if G-Brain has a `dabt/miss-journal/<session-date>-*` page. If not, flag for reconstruction.

### 2. Reconstruct Session Content

Scroll into each missing session to extract:
```
session_search(session_id="<id>", around_message_id=<match>, window=10)
```

For deeper sessions, paginate by passing the last message_id as `around_message_id` to scroll forward.

### 3. Extract Structured Data

For each session, capture:
- **Date and topic** — from the user's first message
- **Questions attempted** — count MCQs or deep-dive rungs
- **Correct/incorrect** — tally from assistant feedback
- **Misses** — each wrong answer with:
  - Topic/context
  - What the user said (their reasoning)
  - The correction
  - Root cause (terminology? formula? concept? arithmetic?)
- **Hits** — topics where user was solidly correct
- **Flashcards created** — Memento deck name and count
- **Protocol changes** — any learning style corrections the user made

### 4. Write Magnitude-Appropriate Summaries

For sessions with **no actual drill work** (planning, skills setup, discussion):
→ Write a minimal summary or skip — these contribute no miss/hit data.

For sessions with **drill blocks or deep dives**:
→ Write full structured `session-summary` pages to `dabt/miss-journal/YYYY-MM-DD-<topic>`.

For **flashcard reviews**:
→ Write as separate pages under `dabt/miss-journal/` with hit/miss counts and precision gap details.

### 5. Update Learner Profile (if warranted)

If the backfill reveals new weak areas not yet captured:
- `mcp_gbrain_put_page` on `dabt/learner-profile`
- Add to the Known Weak Areas section

### 6. Verify Coverage

```
mcp_gbrain_list_pages(tag="dabt", limit=20)
```

Check every session date with drill activity has a corresponding miss journal page.

## Pitfalls

- **Old sessions from different models/agents** may have different output formats. The assistant might have given answers inline differently. Extract the user's answers and the corrections, not the formatting.
- **API-server sessions** (api-server source) may only contain the session setup, not the drill content itself — the actual Q&A may have happened in follow-up turns not captured in the session DB.
- **Cron job sessions** are not drill sessions — skip them.
- **Session previews truncate** — use scroll mode (`session_search(session_id=..., around_message_id=..., window=10)`) to get full content.
- **Don't record what you can't verify.** If a session transcript doesn't show the actual user answer (only the assistant's generic explanation), don't fabricate a miss/hit tally.

## Example Output Pages

- `dabt/miss-journal/2026-05-26-risk-assessment-dose-response` — 7-rung deep dive with specific misses
- `dabt/miss-journal/2026-05-27-risk-assessment-flashcard-review` — flashcard review with precision gaps
- `dabt/miss-journal/2026-05-14-early-drill-sessions` — early calibration with weaker session data
