---
name: vault-maintenance-cron
description: Class-level cron patterns for keeping a study vault healthy. No-LLM, no_agent shell scripts that surface coverage gaps and recurring weak areas on a schedule. Applies to DABT, USMLE, CFA, bar prep — any structured-vault study workflow.
---

# Vault Maintenance Cron Patterns

A populated study vault needs two cheap, recurring checks to stay useful: (1) coverage audit — which concepts have no incoming links, (2) weak-area surfacing — which concepts show up most in miss entries. Both are pure shell + `grep` — no LLM cost, safe to run nightly or every few days.

This pattern is class-level: it works for any study project vault (DABT, USMLE, CFA, bar prep) once you have a `wiki/concepts/` directory and a `wiki/miss-journal/` directory.

## Pattern 1 — Orphan audit (weekly)

**Purpose:** surface concept notes with zero incoming `[[wikilinks]]` from anywhere in the vault or reference library. These are the "orphans" — the user's pull-target list for the next study session.

**Cost:** ~0 tokens. Pure `find` + `grep`. Safe to run daily; weekly is enough.

**Script template (`~/.hermes/scripts/<project>-vault-orphan-audit.sh`):**

```bash
#!/bin/bash
# <Project> vault orphan-concepts audit
# Reports concept notes with no incoming [[wikilinks]] anywhere.
set -uo pipefail

WORKDIR="/path/to/<project>"
CONCEPTS_DIR="$WORKDIR/wiki/concepts"

if [ ! -d "$CONCEPTS_DIR" ]; then
    echo "ERROR: concepts dir not found at $CONCEPTS_DIR"
    exit 1
fi

# Build list of concept slugs (file stems, excluding MOCs)
mapfile -t SLUGS < <(find "$CONCEPTS_DIR" -maxdepth 1 -name "*.md" -type f ! -name "moc-*" -exec basename {} .md \; | sort)

orphans=()
referenced=()
for slug in "${SLUGS[@]}"; do
    # Count files containing [[slug]] anywhere in vault + reference
    count=$(grep -rIl "\[\[$slug\]\]" "$WORKDIR/wiki/" "$WORKDIR/reference/" 2>/dev/null | wc -l)
    if [ "$count" -eq 0 ]; then
        orphans+=("$slug")
    else
        referenced+=("$slug ($count refs)")
    fi
done

echo "=== <Project> vault orphan audit $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "Total concept notes: ${#SLUGS[@]}"
echo "With at least 1 incoming link: ${#referenced[@]}"
echo "Orphans (no incoming links): ${#orphans[@]}"

if [ "${#orphans[@]}" -gt 0 ]; then
    echo "Top 20 orphan concepts (highest-priority to populate):"
    printf '  - %s\n' "${orphans[@]}" | head -20
fi
```

**Cron schedule:** weekly, e.g. Sunday 04:00 UTC. Use `no_agent: true` so the script's stdout is delivered verbatim as the message.

**Hermes cron registration:**

```python
cronjob(action="create",
        name="<Project> vault orphan audit",
        schedule="0 4 * * 0",
        script="<project>-vault-orphan-audit.sh",   # relative to ~/.hermes/scripts/
        no_agent=True,
        deliver="origin")
```

**Concrete example (DABT, 2026-06-05):** `dabt-vault-orphan-audit.sh` → 82 concept notes, 71 linked, 11 orphans (the orphans were the Domain II (Mechanism) and Domain IV (Applied) stubs that didn't have a chapter explicitly mapped — clear signal to expand those next).

## Pattern 2 — Weak areas summary (every few days)

**Purpose:** scan the last N days of miss journal entries, surface the most-referenced concept names. The "your top 5 weak areas this week" view, automated.

**Cost:** ~0 tokens. Pure `find` + `grep` + `sort | uniq -c`.

**Script template (`~/.hermes/scripts/<project>-weak-areas-summary.sh`):**

```bash
#!/bin/bash
# <Project> weak-areas summary
# Reads the miss journal and surfaces most-referenced concept names.
set -uo pipefail

WORKDIR="/path/to/<project>"
MISS_DIR="$WORKDIR/wiki/miss-journal"
WINDOW_DAYS=7

if [ ! -d "$MISS_DIR" ]; then
    echo "ERROR: miss journal not found at $MISS_DIR"
    exit 1
fi

echo "=== <Project> weak areas — last $WINDOW_DAYS days ==="
echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

recent_files=$(find "$MISS_DIR" -maxdepth 1 -name "*.md" -type f -mtime -"$WINDOW_DAYS" 2>/dev/null)
if [ -z "$recent_files" ]; then
    echo "No miss journal entries in the last $WINDOW_DAYS days."
    exit 0
fi

echo "Most-referenced concepts (recurring weak areas):"
for f in $recent_files; do
    grep -oE '\[\[[a-z0-9-]+\]\]' "$f" 2>/dev/null
done | sort | uniq -c | sort -rn | head -10
```

**Cron schedule:** every 3 days at 09:00 UTC is a good default. Adjust the window to 7 days.

## Why these two patterns

- **Coverage audit** tells you "where am I empty?" — directs expansion work
- **Weak areas** tells you "where am I losing marks?" — directs study focus

Together they close the loop: study → miss → wikilink → coverage grows; coverage audit tells you which concepts to expand; weak areas tells you which concepts to drill next. No LLM, no database, no fragile stack.

## When NOT to add more cron jobs

The user said "a couple" — stop at 2. More than that and the noise ratio goes up. If you have a third idea, ask first; do not silently schedule a 3rd job.

## Pitfall — script path resolution

The Hermes cron tool requires `script` to be **relative to `~/.hermes/scripts/`**, not absolute. Pass `script="<project>-vault-orphan-audit.sh"`, not `script="/root/.hermes/scripts/<project>-vault-orphan-audit.sh"`. The latter is silently rejected.

## Pitfall — orphaned wikilink targets

The orphan audit flags concepts with no incoming links, but a concept with a single self-referential link (e.g., its own back-link section) will count as linked. Don't game it by adding self-references; the goal is genuine cross-references from miss entries, source chapters, and other concepts.
