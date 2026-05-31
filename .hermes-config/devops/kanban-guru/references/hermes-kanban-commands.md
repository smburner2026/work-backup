# Hermes Kanban — Command Reference

## States

| State | Meaning | How Cards Get There |
|-------|---------|---------------------|
| `todo` | Created but not yet ready to start | `kanban create` puts cards here |
| `ready` | Ready for the assigned profile to pick up | `kanban transition <id> ready` |
| `doing` | Currently being worked on by the assignee | `kanban transition <id> doing` (or auto by dispatcher) |
| `blocked` | Stuck, waiting on external input | `kanban block <id> "reason"` |
| `done` | Completed | `kanban complete <id>` |

The dispatcher automatically picks `ready` cards and transitions them to `doing`.

## Commands

### `hermes kanban create <title> [--assignee <profile>] [--parent <id>] [--priority <num>] [--initial-status {blocked,running}]`
Create a new card in `todo` state. The only required argument is the title.

- `--assignee default` — handled by the main agent (no special profile needed)
- `--assignee mike` — assigned to the `mike` profile
- `--parent t_xxx` — makes this card wait for another card to complete first
- `--body "text"` — detailed description

### `hermes kanban list [--assignee <profile>] [--state <state>]`
View all cards. No arguments = everything. Can filter by tag, assignee, or state.

### `hermes kanban show <id>`
Full card details including body, comments, and run history.

### `hermes kanban transition <id> <state>`
Manually move a card between states: `todo → ready`, `ready → doing`, `doing → todo` (push back).

### `hermes kanban complete <id> [--summary "text"]`
Mark a card done. Optional summary.

### `hermes kanban block <id> "reason"`
Stick a card in `blocked`. The reason appears in notifications so the human or upstream knows what's needed.

### `hermes kanban unblock <id>`
Return a blocked card to `doing`.

### `hermes kanban comment <id> --body "text"`
Add a comment to a card's thread (doesn't change state).

### `hermes kanban tail <id>`
Live-stream the run log of an active card. Useful for watching a profile work.

## Filters and Views\n\n```bash\n# Filter by state\nhermes kanban list --state ready\n\n# Filter by assignee\nhermes kanban list --assignee mike\n\n# Combined\nhermes kanban list --state doing
```

## Common Workflow Patterns
\n### Solo (one profile, no extra setup)\n```bash\nhermes kanban create "Write Ames test draft" --assignee default\nhermes kanban transition t_abc123 ready\nhermes kanban transition t_abc123 doing\n# ... work happens ...\nhermes kanban complete t_abc123\n```\n\n### Parallel research (fan-out)\n```bash\nhermes kanban create "Research A" --assignee researcher\nhermes kanban create "Research B" --assignee researcher\nhermes kanban create "Synthesize findings" --assignee writer --parent t_a1 --parent t_b2\n```\nThe synthesis card auto-promotes to `ready` only after both research cards complete.\n\n### Strategy-first (discuss before execute)

Cards created with `--assignee` go straight to `ready` state and the dispatcher picks them up immediately — there's no `todo` pause. If you need to discuss scope, priority, or approach before execution:

```bash
# Park the card so the dispatcher ignores it:
hermes kanban create "Build synthetic Domain III questions" --initial-status blocked --body "Need to decide: sub-domain classification first?"

# Or create without assignee — stays in todo (if the dispatcher respects it):
hermes kanban create "Recover 626 Group A quarantined Qs"

# When discussion is done, unblock and let it flow:
hermes kanban transition t_xxx ready
```

The dispatcher only picks `ready` cards. `blocked` and `todo` cards stay parked. Use this to control what the agent works on when.

### Pipeline with human review\n```bash\nhermes kanban create "Draft chapter" --assignee writer\n# Writer completes → human reviews → if changes needed:\nhermes kanban create "Revise chapter" --assignee writer --parent t_xxx\n```\n\n### Human-in-the-loop (blocking)\n```bash\nhermes kanban block t_xxx "Rate limit key: IP (NAT-unsafe) or user_id (requires auth)?"\n# Human unblocks when decision is made\nhermes kanban unblock t_xxx\n```
