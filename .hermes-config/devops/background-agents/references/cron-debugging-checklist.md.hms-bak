# Cron Job Debugging Checklist

When a cron job didn't fire or didn't deliver as expected, work through this checklist systematically. Each step narrows the failure domain.

## 1. Does the job exist?

```python
cronjob(action='list')
```

Check that the job appears in the list with the expected name. If it doesn't exist, it was never created or was deleted.

## 2. Has the job ever fired?

Check `last_run_at`:
- `null` = never fired (scheduler missed it or schedule was wrong)
- A timestamp = it has fired before

Also check `last_status` and `last_delivery_error`:
- `ok` = the agent ran successfully and delivered
- `error` = the agent failed or timed out
- `null` with last_run_at=null = never attempted

The jobs.json file at `~/.hermes/cron/jobs.json` shows the full state including `completed` count and `last_error`.

## 3. Does the schedule match the user's expectation?

Verify the cron expression against the user's stated time and timezone:

```bash
date -u   # current UTC time
date      # current local time
```

Common mistakes:
- `0 13 * * *` = 13:00 UTC = 20:00 UTC+7. If the user says "8 AM my time (UTC+7)," this should be `0 1 * * *`.
- Forgetting AM vs PM: `0 1 * * *` = 1 AM = morning, `0 13 * * *` = 1 PM = afternoon. Off by 12 hours is the most common error.
- Hour/minute swapped: `30 8 * * *` = 08:30, not 08:30.
- Day-of-week off: `0 1 * * 0` = only on Sunday at 01:00.

Fix: `cronjob(action='update', job_id='...', schedule='corrected expression')`

## 4. Is the scheduler running?

The scheduler is part of the gateway process. Check:

```bash
systemctl --user status hermes-gateway.service
journalctl --user -u hermes-gateway.service --since "YYYY-MM-DD HH:MM:SS" --no-pager
```

Look for scheduler-related log lines:
- Cron ticks: look for "tick" or the job ID in the logs
- Delivery warnings: "delivery target lost thread_id" indicates the message will arrive in the channel but not in the correct thread
- Gateway restart time vs expected fire time — if the gateway restarted after the fire time, the tick was missed

The `.tick.lock` file at `~/.hermes/cron/.tick.lock` shows when the last scheduler tick ran.

## 5. Is the delivery target correct?

Check the `deliver` field:
- `discord:channel_id` — delivers to a Discord channel. If the user expects it in a thread, the `channel_id` must include the thread context.
- `origin` — delivers back to the conversation where it was created
- `local` — saves output only, no delivery

Warning sign in gateway logs:
```
WARNING cron.scheduler: Job '...': origin has thread_id=... but delivery target lost it
```
This means the job was created in a thread context, but the delivery target is a bare channel without the thread_id. The message will arrive in the channel, not the thread. Fix by updating the `deliver` field to include the thread_id: `discord:channel_id:thread_id`.

Check the cron jobs.json at `~/.hermes/cron/jobs.json` and look at the `deliver` vs `origin.thread_id` fields.

## 6. Manual test

Trigger the job immediately to test the full pipeline:

```python
cronjob(action='run', job_id='...')
```

This runs the job in a fresh cron session. Check:
- Does the agent produce the expected output?
- Does the output arrive at the delivery target?
- Check `~/.hermes/cron/output/<job_id>/` for the run log

## 7. Check the output log

Each cron run produces a markdown log at `~/.hermes/cron/output/<job_id>/<timestamp>.md`. Read it to see:
- What prompt the agent received
- What tools it called (if any)
- What final response it generated (this is what gets delivered)

Note: the output log shows the full prompt+skill context, not just the delivered message. The agent's final response (the last thing it says) is what gets sent to the delivery target.

## 8. One-time jobs vs recurring

- `repeat=1` — fires once, then state becomes `completed` (one-shot background agent)
- `repeat` omitted — fires forever on schedule (recurring maintenance job)
- `repeat=N` — fires N times total

A one-shot job with `repeat=1` that already fired (completed count = 1) won't fire again. The `cronjob` tool's `list` output shows `last_run_at` and `repeat` to distinguish idle from finished.

## 9. Diagnosing Script-Based (no_agent) Cron Failures

When a cron job has `no_agent=True` and `last_status: "error"`, the script ran but exited with a non-zero code. Here's how to diagnose.

### Step 1 — Read the failure output

Each cron run saves an output file at `~/.hermes/cron/output/<job_id>/<timestamp>.md`. For a no_agent job, the file shows:

```
**Status:** script failed
Script exited with code 128
stdout:
[main abc1234] backup 2026-05-31 06:00 UTC
 1156 files changed...
fatal: 'origin' does not appear to be a git repository
```

Key signals:
- **Exit code 128** = git command failure (the script likely has `set -e` which aborts on ANY non-zero exit)
- **Commit succeeded** (SHA appears in stdout) but **push failed** (fatal error after commit)
- Empty stdout with exit code 1 or 127 = runtime error (missing file, bad command) or syntax error

### Step 2 — Read the script to find the failing line

```bash
cat ~/.hermes/scripts/<script-name>.sh
```

Look for `set -e` at the top — this makes the script exit on ANY failure. Work backward from the last visible stdout line:
- Commit appeared but nothing after → failing command is right after the commit
- No stdout at all → failure near the top (cd, rsync, git commands)

### Step 3 — Check the dependency chain

For git backup scripts specifically:

```bash
# 1. Does the git repo exist?
cd /root/work && git status

# 2. Is the remote configured?
git remote -v
# Empty = remote was deleted or never set. Fix: git remote add origin <url>

# 3. Is auth valid?
gh auth status
# If token invalid, git push fails with 128.

# 4. If insteadOf URL rewriting is used, check git config:
git config --list | grep insteadof
# This rewrites https://github.com/ URLs to include embedded tokens.
# If token expired, ALL git operations fail.

# 5. Check branch name matches script
git branch
# Script pushes to "main" — verify the repo actually uses main, not master
```

### Step 4 — Fix and re-test

```bash
git remote add origin https://github.com/<user>/<repo>.git
gh auth login -h github.com
cd /root/work && git push origin main
```

Then trigger a manual run:
```python
cronjob(action='run', job_id='<id>')
```

### Pitfalls

- **`set -e` hides partial progress** — The script may succeed at steps 1-4 and only fail at step 5. The local commit IS created; don't assume the whole backup failed.
- **GitHub token expiry** — Classic PATs expire. `gh auth status` tells you immediately. `~/.git-credentials` at 0 bytes = no stored auth.
- **`insteadOf` URL config** — `url.https://user:token@github.com/.insteadof=https://github.com/` rewrites ALL github URLs to include auth. If token is bad, every git operation fails, even to public repos.
- **No delivery of failure** — A no_agent script that fails does NOT deliver the failure to the user (script aborts before `echo`). The scheduler records `last_status: "error"` but the user isn't notified unless they check. **LLM-driven jobs produce better failure output.**
- **Remote deletion** — If the remote was removed (via `git remote remove origin` or `.git/config` reset), commit works locally but push fails. Check `git remote -v`.

## Common Failure Modes

| Symptom | Likely Cause |
|---------|-------------|
| last_run_at=null, but job is enabled | Schedule hasn't arrived yet, or scheduler wasn't running at fire time |
| Job fires but empty delivery (just "—" or blank) | Agent had no data source instructions — the prompt didn't tell it to read the relevant file. Cron agents have zero session context; they won't infer file paths from the skill. Fix: add explicit "Read file <absolute_path>" to the prompt. |
| Message arrives in wrong channel/thread | delivery field lacks thread_id. Check origin vs deliver. |
| Job was "ok" but user didn't see it | Delivery target mismatch. User may be in a different channel. |
| Schedule looks right but job never fires | Gateway restart during the fire window. The scheduler resumes but doesn't retro-fire missed jobs. |
| completed count increasing but no output | Job runs but the agent's response is a no-op or error. Check output logs for tool errors. |
