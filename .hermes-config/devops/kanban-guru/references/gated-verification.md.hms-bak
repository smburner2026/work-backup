# Gated Verification Cards + Cron Notification

## When to Use

You've created a batch of kanban cards that do recovery/ generation/refactor work, and you want an automatic verification pass to run once they're all done — then notify the user with results.

## Workflow

```
1. Create work cards (independent, parallel)
   hermes kanban create "Fix batch A" --assignee default
   hermes kanban create "Fix batch B" --assignee default
   hermes kanban create "Fix batch C" --assignee default

2. Create verification card gated on all parents
   hermes kanban create "Truth audit: verify all fixes" \
     --assignee default \
     --parent t_aaaaaa --parent t_bbbbbb --parent t_cccccc

   Note: --parent is repeatable. Include ALL work cards as parents.
   The verification card auto-promotes from "todo" to "ready"
   only after every parent completes.

3. Set up a cron job to watch for completion
   hermes cronjob create \
     --name "Verification Watch" \
     --schedule "every 30m" \
     --repeat 48 \
     --deliver origin \
     --prompt "Check status of kanban card t_xxxxxxxx.
               If done with summary: output the full summary.
               If still todo/ready/running: output [SILENT]"
```

## Antipatterns

- **Don't set the verification card to --initial-status blocked** — it starts in "todo" naturally because of parent dependencies. Blocked is for cards needing human ops.
- **Don't forget the --deliver origin flag on the cron** — without it, the cron output lands in CLI, not the user's channel.
- **The cron's [SILENT] protocol** is important — it checks every 30 min and stays quiet until the card is actually done. Without it, the user gets "card is still running" spam.
- **48 repeats = ~24 hours** — if the work takes longer, create a fresh cron or increase repeat count.
- **Include ALL relevant parents** — missing one means the gate fires early. Include the verification card's OWN parents plus any other work cards you want verified.
