---
name: dabt-weekly-maintenance
description: "Weekly DABT maintenance cron job — truth audit, weak areas summary, vault orphan audit, flashcard briefing, and artifact scanning."
category: education
---

# DABT Weekly Maintenance

## Trigger
Load when: weekly cron job fires (Sunday 04:00 UTC) | user says "run maintenance" | "weekly audit" | "DABT health check".

## Procedure

### 1. Database Truth Audit
Run via `terminal` (NOT `execute_code` — blocked in cron mode):

```bash
cd /root/work/dabt/dabt-tutor && python3 -c "
import sqlite3
conn = sqlite3.connect('reference/data/dabt.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
# ... (query as needed)
"
```

**Key metrics to report:**
- Total Qs, answer key coverage, explanation coverage, Bloom level coverage
- Domain distribution vs exam blueprint (Domain I: 36%, II: 13%, III: 38%, IV: 13%)
- Missing explanations by domain
- Zero-option Qs by domain
- Low-confidence classifications

**Pitfall:** `execute_code` is blocked in cron mode. Use `terminal` for all Python analysis.
**Pitfall:** Pipe-to-interpreter (`python3 | python3`) is blocked in cron mode. Run single commands only.

### 2. Weak Areas Summary
Cross-reference DB metrics against exam blueprint:
- Domain III (Risk Assessment) is chronically underweight — flag if <15% of DB
- Domain IV (Applied) is typically overweight — flag if >30% of DB
- Missing explanations: prioritize Domain II (highest rate) and Domain IV (highest count)
- State.json staleness: check `progress/state.json` last drill date

### 3. Vault Orphan Audit
```bash
cd /root/work/dabt/dabt-tutor
# Get concept slugs (exclude MOCs)
find wiki/concepts/ -maxdepth 1 -name "*.md" ! -name "moc-*" -exec basename {} .md \; | sort

# For each slug, count backlinks
grep -rl "\[\[$slug\]\]" wiki/ reference/extracted/ 2>/dev/null | wc -l
```

**MOC naming convention:** MOC files use `moc-i-conduct-of-studies.md` format (NOT `moc-domain-i.md`). All 5 MOCs should be present:
- `moc-i-conduct-of-studies.md`
- `moc-ii-mechanistic-tox.md`
- `moc-iii-risk-assessment.md`
- `moc-iv-applied-tox.md`
- `moc-organ-systems.md`

**Pitfall:** Do NOT check for `moc-domain-i.md` — wrong naming convention.

### 4. Daily Flashcard Reminder Briefing
```bash
python3 ~/.hermes/scripts/daily-flashcard-reminder.py
```

**Pitfall:** The reminder script may crash with "Expecting value: line 1 column 1" if `run_cmd()` doesn't check for empty subprocess output. See `memento-flashcards` skill's `references/daily-reminder-fix.md` for the fix. If the script fails, manually compile the briefing from:
```bash
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py stats
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due --collection "DABT - Risk Assessment"
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due --collection "DABT - Conduct of Studies"
python3 ~/.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py due --collection "DABT - Metal Tox"
```

### 5. New Artifacts Scan
```bash
cd /root/work/dabt/dabt-tutor
# Find files newer than last audit
find . -newer wiki/skills-vault-audit-2026-06-05.md -name "*.md" -o -name "*.json" | grep -v __pycache__
```

For each new artifact, create L1 summary (and L2 where appropriate) with full provenance.

**Note:** The `artifact-pyramids` referenced in the original cron spec does not exist as a standalone skill. The pyramid step is handled directly in this maintenance workflow.

## Output Format
Produce a single structured report with sections for each task, metrics, and actions taken. Use the report template in `references/maintenance-report-template.md`.

## Cron Schedule
- **Sunday 04:00 UTC** — Full weekly maintenance (all 5 tasks)
- **Every 3 days 09:00 UTC** — Weak areas summary only (abbreviated)
