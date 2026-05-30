# Cron Schedule Audit (Timezone Validation)

When auditing or reviewing cron jobs after creation or when the user reports missed runs, validate every job's schedule against the user's timezone. A six-hour offset in UTC time can mean the difference between "fires at 8 AM" and "fires at 2 AM."

## Procedure

### Step 1 — List all jobs

```
cronjob(action='list')
```

If the `cronjob` tool is unavailable, read `~/.hermes/cron/jobs.json` directly and parse the `schedule.expr` field for each job.

### Step 2 — Map UTC to local time for every job

Each cron expression must be mentally converted: `HH UTC` → `HH local`.

For UTC+7 (common):
| UTC | Local (UTC+7) | Good for |
|-----|---------------|----------|
| 00:00 | 07:00 | Early morning |
| 01:00 | 08:00 | Morning |
| 02:00 | 09:00 | Mid-morning |
| 05:00 | 12:00 | Noon |
| 06:00 | 13:00 | Early afternoon |
| 08:00 | 15:00 | Afternoon |
| 12:00 | 19:00 | Evening |
| 13:00 | 20:00 | Night |
| 20:00 | 03:00 (next day) | **SUSPICIOUS — 3 AM** |

### Step 3 — Flag suspicious times

Any job that fires between **00:00–05:00 local time** (midnight to 5 AM) is likely a scheduling error unless the user explicitly confirmed it (e.g., a heavy batch job during sleep hours).

Common pattern: `0 20 28 * *` = 20:00 UTC on the 28th = **03:00 UTC+7 on the 29th**. This is almost always meant to be `0 13 28 * *` = 13:00 UTC = 20:00 UTC+7.

### Step 4 — Check `last_run_at`

| last_run_at | Meaning |
|-------------|---------|
| Has a recent timestamp | Job fired. Check `last_status` for errors. |
| null | Job was created but **never fired**. Either the schedule hasn't come around yet, or the scheduler doesn't tick. |
| Stale (days/weeks old) | Job was working but stopped. Check scheduler health and gateway uptime. |

If `last_run_at` is null for a job that should have fired already, the scheduler may not be ticking. Verify the gateway is running.

### Step 5 — Update the schedule if wrong

```
cronjob(action='update', job_id='<id>', schedule='<correct cron>')
```

### Common UTC+7 conversion errors

| Wrong UTC schedule | Local time (wrong) | What it should be for 08:00 UTC+7 | Correct UTC |
|---|---|---|---|
| `0 13 * * *` | 20:00 (8 PM) | 08:00 UTC+7 | `0 1 * * *` |
| `0 20 * * *` | 03:00 (3 AM) | 08:00 UTC+7 | `0 1 * * *` |
| `0 20 28 * *` | 03:00 next day | 20:00 UTC+7 on 28th | `0 13 28 * *` |

### Pitfalls

- **Day-of-month shifts**: 20:00 UTC = 03:00 local next day. A job meant for the 28th at 20:00 local actually fires at 03:00 on the 29th UTC — two problems: the hour is wrong AND the day is wrong.
- **DST**: UTC doesn't observe DST. If the user changes timezone or observes DST, all schedules may shift by ±1 hour. Re-audit when the user mentions a timezone change.
- **Scheduler restarts**: If the gateway was restarted after a job's scheduled time, the job may have been missed. The scheduler does NOT retroactively fire missed jobs.
- **Job creation timing**: A job created after its intended fire time on the same day will have `last_run_at: null` until the next scheduled tick. This is not a bug — the first fire is tomorrow.
