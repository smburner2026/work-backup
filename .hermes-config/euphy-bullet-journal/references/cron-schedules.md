# Euphy Bullet Journal - Cron Schedules

Configured schedules (as of 2026-05-20):

- Daily: 0 12 * * * (12:00 UTC / 7AM CT)
- Weekly: 0 12 * * 0 (12:00 UTC Sunday / 7AM CT Sunday)
- Monthly: 0 20 28 * * (20:00 UTC on the 28th / 3PM CT)

All jobs load the euphy-bullet-journal skill and use the Proactive Update Templates.

## Cron Prompt Requirements

The daily/weekly cron prompt MUST follow these rules:
1. **Always read the journal file** first (~/.hermes/profiles/euphy/journal/study-schedule.md).
2. Check today's date and report items actually recorded — never use placeholder text.
3. Do NOT assume "no tasks" — verify by reading the file.
4. Use the Daily/Weekly/Monthly update templates but populate them from real data.

## History

- 2026-05-18: Initial setup (daily 07:00, weekly 07:00 Sun, monthly 15:00 28-31)
- 2026-05-19: Daily rescheduled to 12:00 UTC
- 2026-05-20: Added cron prompt requirements section. All schedules updated to current values.
