# Discover → Review → Execute Pattern

A general-purpose human-gated workflow for kanban that separates *discovery* from *action*.

## When to use this

Any task where you want a worker to research/analyze/audit before the main agent acts on the findings. Specific triggers:

- **System administration** — "audit disk usage and suggest deletions", "profile RAM and recommend optimizations"
- **Research then build** — "find the best library for X, then implement with it"
- **Analysis then fix** — "find what's causing the slowdown, then fix it"
- **Exploration then decision** — "investigate options and recommend, I'll decide which to pursue"

The pattern is right when the worker's output needs **human judgement** before execution — you want the raw findings, not an automated action chain.

## Workflow

```
1. CREATE discovery card
   User (via main agent): kanban create "Audit X and propose Y"
                         --assign default

2. WORKER discovers
   Kanban worker spawns, runs autonomously, completes with
   full findings in summary + comment
   
3. HUMAN reviews
   Main agent (same conversation): kanban show <task_id>
   → reads findings, discusses with user
   
4. MAIN AGENT executes
   User decides which recommendations to act on
   Main agent runs the actual commands/changes
```

## Key property: one-hop human gate

The worker never executes changes — it only discovers and reports. The human (via the main agent) decides what to act on. This contrasts with:

| Pattern | Worker does | Human does |
|---------|-------------|------------|
| Discover → Execute | Reports findings | Reviews + commands execution |
| Fan-out + fan-in | Parallel work | Reviews synthesis |
| Review-in-card | Produces output, blocks for review | Unblocks or rejects within the card |

The discover→execute pattern keeps the human in a **reviewer + commander** role rather than a **reader of final output** role. The worker's output is *input to a decision*, not an artifact to approve or reject.

## Concrete example (from a real session)

**Card:** "Disk space audit: propose deletable files and directory reorganization"

1. Worker scanned 38G filesystem, identified 5.5G safe-to-delete and 2.5G conditional
2. User reviewed findings and said: "Clean 2 and 3. Let me know what is in 1"
3. Main agent showed recycle-bin contents (373M of auto-backups)
4. User said: "Yes proceed" → main agent deleted it
5. Main agent also removed a stale gbrain repo (376M) after confirming with user

The kanban worker's output was the *agenda*; the main agent was the *executor*.

## Pitfalls

- **Worker's scratch workspace is GC'd on completion.** If the worker creates files, they vanish. The worker must embed findings in the kanban comment or summary. Use `kanban_comment(body=json.dumps(findings))` before `kanban_complete()`.
- **Summary alone isn't enough for complex audits.** The kanban show summary is truncated. Workers should leave a structured comment with the full breakdown.
- **The human still needs to act.** The discovery card being "done" doesn't mean the work is done — it means the research phase is complete. Keep a separate todo or note of what actions to take based on findings.
- **Not for time-sensitive execution.** The lag between worker completion and human review can be minutes or hours. If the action needs to happen immediately, skip the discovery phase and execute directly.
