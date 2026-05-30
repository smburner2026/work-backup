#!/usr/bin/env python3
"""Daily flashcard reminder — checks Memento due cards and prints a briefing."""
import json
import subprocess
import sys
from pathlib import Path

MEMENTO = Path.home() / '.hermes/skills/productivity/memento-flashcards/scripts/memento_cards.py'

def run_cmd(*args):
    result = subprocess.run(
        [sys.executable, str(MEMENTO), *args],
        capture_output=True, text=True, timeout=30
    )
    return json.loads(result.stdout)

try:
    stats = run_cmd('stats')
    total = stats['total']
    due = stats['due_now']
    cols = stats.get('collections', {})

    per_col = {}
    for col_name in cols:
        try:
            col_due = run_cmd('due', '--collection', col_name)
            per_col[col_name] = col_due['count']
        except Exception:
            per_col[col_name] = '?'

    lines = []
    lines.append("**🧠 Daily Flashcard Reminder**")
    lines.append("")
    if due == 0:
        lines.append("No cards due today — you're caught up! :tada:")
        lines.append(f"Total: {total} cards across {len(cols)} collections.")
    else:
        lines.append(f"You have **{due} cards due** out of {total} total.")
        lines.append("")
        for col_name in sorted(per_col.keys()):
            due_count = per_col[col_name]
            total_count = cols[col_name]
            bar = "■" * min(due_count, 10) + "□" * max(0, 10 - min(due_count, 10))
            lines.append(f"{bar} **{col_name}**: {due_count} due / {total_count} total")
        lines.append("")
        lines.append("→ Reply **`review`** to start a session")
        lines.append("→ Or **`review [topic]`** for a specific collection")
    print("\n".join(lines))

except Exception as e:
    print(f"**Flashcard Briefing Error**\n\nCould not check cards: {e}")
