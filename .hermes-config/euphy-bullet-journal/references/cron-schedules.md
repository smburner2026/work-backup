# Euphy Bullet Journal - Cron Schedules

Configured schedules (as of 2026-05-28):

- Daily: 0 12 * * * (12:00 UTC / 7AM CT)
- Weekly: 0 12 * * 0 (12:00 UTC Sunday / 7AM CT Sunday)
- Monthly: 0 13 28 * * (13:00 UTC on the 28th / 8AM CT)

All jobs load the euphy-bullet-journal skill and use the Proactive Update Templates.

**Prerequisite:** Each cron job MUST run under the `euphy` Hermes profile (`--profile euphy`) so it can access the journal file at `/root/.hermes/profiles/euphy/journal/study-schedule.md`. Running under the default profile or any other profile will fail with a permission error on `/root/`.

## Horizon System

The three cron jobs now have distinct time horizons to eliminate redundancy:

| Cron | Horizon | Purpose |
|------|---------|---------|
| Daily | Today + 3 days | Operational — immediate tasks and events |
| Weekly | Today + 14 days | Tactical — upcoming commitments and deadlines |
| Monthly | Today + 90 days | Strategic — horizon scanning, long-term deadlines, undated To-Do items |

## Date Tag Convention

Every journal entry should carry a `[due:YYYY-MM-DD]` inline tag to enable horizon filtering:

- `euphy-add` automatically appends `[due:YYYY-MM-DD]` to every entry it writes.
- Legacy entries without the tag inherit the date from their section header.
- Items in "To Do" / "Upcoming" sections without dates show up in monthly only.

## Cron Prompt Rules

Each cron prompt MUST include:
1. Read the journal file first.
2. Parse `[due:]` tags; for legacy entries, use the date header.
3. Filter by the horizon range above.
4. Use real data from the journal — never placeholders.
5. Use the appropriate update template with Euphy's tone.

## History

- 2026-05-18: Initial setup (daily 07:00, weekly 07:00 Sun, monthly 15:00 28-31)
- 2026-05-19: Daily rescheduled to 12:00 UTC
- 2026-05-20: Added cron prompt requirements section. All schedules updated to current values.
- 2026-05-28: Introduced horizon system with [due:] tag convention. Daily=3d, Weekly=14d, Monthly=90d. Updated euphy-add to auto-tag entries.
