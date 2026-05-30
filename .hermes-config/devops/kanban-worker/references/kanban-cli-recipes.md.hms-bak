# Kanban CLI Recipes — Create → Assign → Dispatch → Inspect

> CLI usage patterns for the `hermes kanban` command. The "CLI fallback" section in the parent SKILL.md maps individual tools to CLI equivalents; this reference covers **workflow sequencing** and the gotchas that aren't visible from a single-tool mapping.

## Recipe: create, assign, dispatch, track

```
# 1. CREATE — priority is an integer, not P1/P2
hermes kanban create "task title" --body "description" --priority 2 --json

# NOTE: --priority expects an int. "P2", "p1", "high" all fail with:
#   error: argument --priority: invalid int value: 'P2'

# 2. INSPECT after creation
# New cards default to assignee: null, status: ready
hermes kanban show <task-id> --json

# 3. ASSIGN — required before dispatch can spawn a worker
hermes kanban assign <task-id> <profile-name>

# Cards with assignee: null are silently skipped by the dispatcher:
#   {"skipped_unassigned": ["t_..."]}
# Use `hermes kanban assign` to fix before dispatch.

# 4. DISPATCH — processes the queue, NOT a single task
hermes kanban dispatch --max 1

# dispatch takes NO task-id argument. It scans the queue for ready + assigned
# cards and spawns workers. Use --max to cap concurrent spawns.
# Wrong:   hermes kanban dispatch t_ac674fac   # → unrecognized arguments
# Correct: hermes kanban dispatch

# 5. INSPECT status
hermes kanban show <task-id> --json
# Returns full task object including runs[], events[], and latest_summary.
# Check runs[N].status to see if worker is "running", "completed", etc.

# 6. TAIL — live events (blocks until timeout or Ctrl-C)
hermes kanban tail <task-id>
# Prints timestamped events as they arrive (created, assigned, claimed, spawned,
# heartbeats, completed). Blocks indefinitely — use timeout or Ctrl-C.
```

## Gotchas

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Priority as string | `error: argument --priority: invalid int value: 'P2'` | Use integer: `--priority 2` |
| No assignee | Card created, dispatch silently skips it in `skipped_unassigned` | `hermes kanban assign <id> <profile>` then dispatch |
| dispatch with task-id | `unrecognized arguments: t_abc123` | Drop the arg — dispatch processes the whole queue |
| tail blocking | Command doesn't return (hangs) | It's a live tail — expects Ctrl-C or timeout. Use `show --json` for a point-in-time snapshot instead |
| Invented profile name | Card sits in `ready` forever, no error | Verify with `hermes profile list` first |

## Inspecting worker output

To check what a running or completed worker produced:

```bash
# Full task state with run history
hermes kanban show <task-id> --json

# Read the worker's workspace (if scratch dir)
ls /root/.hermes/kanban/workspaces/<task-id>/
```

## Available flags on key commands

- `create` — `--body`, `--priority N` (int), `--assignee`, `--parent`, `--triage`, `--json`
- `assign` — `<task-id> <profile>`
- `dispatch` — `--max N`, `--dry-run`, `--failure-limit N`, `--json`
- `show` — `<task-id> --json`
- `tail` — `<task-id>` (no `--json`)
