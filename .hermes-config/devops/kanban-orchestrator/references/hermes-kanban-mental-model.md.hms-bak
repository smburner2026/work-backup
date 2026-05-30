# Hermes Kanban — Mental Model & Orientation

> New to Kanban in Hermes? Start here. This is the fundamental mental model — what Kanban is, how it relates to other Hermes tools, and the simplest way to start.

## What Kanban Is

A **persistent task board** stored in SQLite. Four states:

```
todo → ready → doing → done
                   ↕
               ⚠ blocked
```

That's it. No columns to configure, no WIP limits to set, no dashboard to install. Cards survive crashes, restarts, and cross-session gaps.

## The Three-Layer Model

This is the most important concept for knowing WHEN to use Kanban vs other Hermes mechanisms:

| Layer | Job | Tool | Example |
|-------|-----|------|---------|
| **Cron** | *When* it runs | `hermes cron create` | "Every morning at 8am" |
| **Kanban** | *Who* does it + *what state* is it in | `hermes kanban` | "Mike is researching nickel tox, card is in progress" |
| **Skill** | *How* to do it | `.hermes/skills/` | "The procedure for formatting flashcards and delivering them" |

### When to use which

- **Cron** — needs to fire at a specific time, repeatedly, without anyone asking. E.g. daily journal prompt, weekly digest.
- **Kanban** — batch of work you want to assign to profiles and track. E.g. "research X + test Y + draft Z, across 3 profiles, check results later."
- **Skill** — procedural memory for how to do a class of work. E.g. "this is how you create a DABT flashcard, with the correct format and delivery channel."
- **Cron + Kanban** — cron creates a card on a schedule, a profile picks it up.
- **Cron + Skill** — cron loads a skill and runs it on schedule. Memento flashcards work this way (cron triggers the flashcard skill at 8am).

### What NOT to use Kanban for

- Tightly-coupled reasoning (multi-agent debate). The board serializes handoffs — use `delegate_task` for parallel LLM calls.
- High-frequency micro-tasks. Each transition costs ~s — direct tool calls are faster.
- Time-sensitive delivery at an exact hour. Use cron — Kanban has no clock, cards wait in `ready` until claimed.

## `/goal` vs Kanban

`/goal` is a session-level sticky instruction. You set it mid-conversation, and the current agent keeps it in mind across turns. One at a time. Gone when the session ends.

Kanban is a persistent board. Tasks survive restart. Multiple tasks can coexist. They're assignable to different profiles.

| | `/goal` | Kanban |
|---|---|---|
| Persistence | Session only | SQLite — survives restarts |
| State tracking | None | todo → ready → doing → done |
| Multi-task | One at a time | Unlimited cards |
| Assignment | Current agent only | Any profile |
| Visibility | Only in current chat | `hermes kanban list` anytime |

**Rule of thumb**: `/goal` for "keep this in mind while we talk." Kanban for "this work should exist independently of this conversation."

## CLI Lifecycle

Three commands make up 90% of usage:

```
hermes kanban create "Task name" --assign <profile>
    → Creates a card in 'ready' state
    → Returns a task ID like t_4f1d74ab

hermes kanban claim <task_id>
    → Moves it from 'ready' to 'doing'
    → A worker profile does this automatically

hermes kanban complete <task_id>
    → Marks it 'done'
```

Other verbs: `block` (stuck), `unblock` (unstuck), `list` (view all), `show <id>` (details), `comment` (add note).

**Common pitfall**: there is no `transition` verb. The states are managed through specific verbs: `claim` (ready→doing), `complete` (doing→done), `block`/`unblock`.

## The "Batch and Forget" Pattern

This is the primary value of Kanban for non-technical users:

1. In a session, create multiple cards for independent tasks
2. Assign each to the appropriate profile (or `default`)
3. Keep talking — a separate Hermes worker spawns for each card
4. Workers run asynchronously, don't interrupt the current conversation
5. Later, review results: `hermes kanban list`

The worker is a fully independent Hermes process — separate session, fresh tools, isolated context. It doesn't burden the current conversation.

## You Don't Need Extra Profiles

The `default` profile is your main Hermes agent. Assigning a card to `default` just means "the main agent handles this." No special setup needed. Named profiles (`euphy`, `mike`, etc.) are for specialization and parallel execution — optional layers, not requirements.

A single-profile setup with `default` works fine for personal Kanban. The board tracks the task; the main agent executes it.

## Dispatcher Mechanics (What Happens After You Create a Card)

1. The card sits in `ready` state on the board
2. The dispatcher (runs inside the gateway) finds ready cards
3. It atomically claims a card and spawns a worker process under the assigned profile
4. The worker receives the card details, toolset, and workspace
5. Worker runs the task, calls `kanban_complete()` when done
6. If the worker crashes or goes silent, the dispatcher auto-reclaims after ~15 minutes
7. After 5 consecutive spawn failures, the card auto-blocks instead of retrying forever

## Summary

- Kanban = persistent tasks with state and assignment
- Cron = timing. Kanban = routing. Skills = procedure.
- Three commands: `create`, `claim`, `complete`
- Workers run independently — they don't interrupt the session
- The `default` profile works fine — no extra profiles needed
- Cards survive crashes and restarts (SQLite)
