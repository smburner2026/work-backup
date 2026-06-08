---
name: cronjob-management
category: devops
description: Standard operating procedure for managing Hermes cron jobs across profiles, ensuring correct profile assignment, and consolidating duplicates.
---

# Cronjob Management Skill

## When to Use
- You need to list, create, update, or remove cron jobs.
- You want to verify that cron jobs are running under the intended Hermes profile.
- You detect duplicate cron jobs (same name/schedule) across profiles and wish to consolidate.
- You need to move a cron job from one profile to another.

## Steps

### 1. List All Cron Jobs (Profile-Agnostic)
```bash
hermes profile use default   # or any profile; listing shows all profiles
hermes cronjob list
```
Review the output for:
- `profile` field indicating which profile the job belongs to.
- `name`, `schedule`, `script`, `deliver`, `enabled` status.
- `last_status` and `last_run_at` for health checks.

### 2. Verify Profile Assignment
For each job, confirm that the `profile` matches the intended profile:
- Euphy-related jobs (bullet journal, vault audits, consolidation) → `euphy`
- DABT/Mike-related jobs (truth audit, flashcard, weak areas, vault orphan, maintenance) → `mike`
- Infrastructure/hygiene, backup, artifact housekeeping → `default`
- Jacob/Vietnam historian jobs → `jacob` (if any)
- Research/scraper/worker profiles → respective names

If a job is misplaced, note its `job_id` for relocation.

### 3. Remove Duplicate or Misplaced Jobs
To delete a job:
```bash
hermes cronjob remove --job_id <job_id>
```
Always list first to confirm the correct `job_id`.

### 4. Create a Cron Job Under the Correct Profile
Switch to the target profile, then create:
```bash
hermes profile use <target_profile>
hermes cronjob create \
  --name "<Job Name>" \
  --schedule "<cron schedule>" \
  --script "<script_path>" \
  --deliver "<delivery_target>" \
  [--no_agent true|false] \
  [--enabled_toolsets "terminal,file,..."] \
  [--workdir "/absolute/path"] \
  [--model "<model>"] \
  [--provider "<provider>"]
```
Key flags:
- `--no_agent true` for simple script-only jobs (no LLM reasoning needed).
- `--deliver` can be `origin` (current chat), `local` (no delivery), or a platform target like `discord:#channel` or `telegram:-1001234567890:123`.
- If the job requires skills, add them via the `skills` parameter (not shown in CLI; see tool docs).

### 5. Consolidate Similar Jobs
If you find two jobs with identical purpose but different profiles (e.g., orphan audit in both `mike` and `euphy`):
1. Determine which profile is the correct owner based on job content.
2. Keep the job in the correct profile, delete the duplicate.
3. If the job should exist in both profiles (rare), ensure they are truly distinct (different scripts/schedules).

### 6. Verify After Changes
Run `hermes cronjob list` again to confirm:
- Each job appears under the expected profile.
- No duplicate names/schedules remain unless intentional.
- `next_run_at` timestamps are sensible.

### 7. Common Pitfalls
- **Forgot to switch profiles**: Creating a job while in the wrong profile attaches it to that profile. Always `hermes profile use <target>` before `cronjob create`.
- **Missing `workdir`**: Scripts that rely on relative paths fail. Set `--workdir` to the directory containing the script or use absolute paths in the script.
- **Delivery misconfiguration**: Using `origin` when you want a specific Discord/Telegram channel leads to messages appearing in the wrong place. Double-check the `deliver` format.
- **Overlooking `no_agent`**: Script-only jobs should set `--no_agent true` to avoid unnecessary LLM overhead and token usage.
- **Ignoring skill requirements**: If a job needs specific skills (e.g., `profile-compression`), include them via the `skills` parameter; otherwise the job may fail silently.
- **Skipping verification**: Assuming the job is correctly created or moved without checking. After any creation, removal, or modification, always run `hermes cronjob list` to confirm the job appears under the expected profile with correct parameters, schedule, and delivery target.

## Verification
After creating or moving a job, you can optionally trigger an immediate run to test:
```bash
hermes cronjob run --job_id <job_id>
```
Check the output for success, then revert to scheduled runs.

## References
- See `references/cronjob-cleanup-session.md` for a real-world example of consolidating orphan audit and backup jobs across profiles.