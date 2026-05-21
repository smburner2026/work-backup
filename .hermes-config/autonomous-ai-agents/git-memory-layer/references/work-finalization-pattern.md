# Work Finalization Pattern — Artifact Archival After Major Work

When a major work block completes (complex task, pipeline run, multi-session analysis, data enrichment campaign), the artifacts span more than just the work directory. This pattern covers the full finalization sweep.

## What "major work" triggers this

- Data pipeline run (batch enrichment, DB migration, classification)
- Analysis that produces referenceable artifacts (error audits, truth audits)
- Configuration that affects how Hermes operates (cron jobs, skills, profiles)
- Multi-session campaign with accumulating state

## Finalization checklist

### 1. Commit material work

`cd /root/work && git add -A && git commit -m "cat: description" && git push`

Covers all changed files in the work directory. The auto-backup cron (weekly) will eventually catch missed pushes, but push immediately for important work.

**What goes in:** Scripts, data files, config, analysis output, AGENTS.md, deep dives, reference extraction, batch output.

**What stays out:** Chat dialogue, session transcripts, Hermes internal state, credentials.

### 2. Save skill snapshots

Skills live in `~/.hermes/skills/` — outside the work directory, outside git backup. For important work, snapshot the relevant skills into the work directory:

```
cp ~/.hermes/skills/<category>/<skill>/SKILL.md /root/work/.../.hermes-snapshots/skills/<skill>.md
cp ~/.hermes/skills/<skill>/references/<file>.md /root/work/.../.hermes-snapshots/skills/
```

Include any reference files that document the work (audit reports, error analyses, config schemas).

### 3. Document cron job definitions

Cron jobs are defined in Hermes's internal cron system — they survive restarts but aren't backed up as files. For any cron job created during the work:

```
cronjob(action='list') → get job_id, schedule, skills, prompt
write_file → /root/work/.../.hermes-snapshots/cron/<job-name>.md
```

The documentation file should include: schedule, skills loaded, toolsets enabled, full prompt text, workdir, and rationale/context for the job.

### 4. Compress profile memory files (and check soul files)

Memory files (MEMORY.md, USER.md) accumulate facts during heavy work sessions and approach capacity. After each major work block, check and compress:

- **MEMORY.md** was 90%+? Compress with token packing: merge related entries, drop redundant detail, use `→`/`/`/`+` notation, group by domain label (DABT, GIT, VPS, etc.)
- **USER.md** was 85%+? Compress: drop parenthetical examples (retrievable via session_search), tighten clauses, collapse long explanations into one-liners
- **Soul files** were not compressed in this session? Check if any have prose sections that could become DSL

Memory files (MEMORY.md, USER.md) accumulate facts during heavy work sessions and approach capacity. After each major work block, check and compress:

- **MEMORY.md** was 90%+? Compress with token packing: merge related entries, drop redundant detail, use `→`/`/`/`+` notation, group by domain label (DABT, GIT, VPS, etc.)
- **USER.md** was 85%+? Compress: drop parenthetical examples (retrievable via session_search), tighten clauses, collapse long explanations into one-liners
- **Soul files** were not compressed in this session? Check if any have prose sections that could become DSL

Compression targets: MEMORY.md → ≤80% cap, USER.md → ≤70% cap.

Expected savings: 15–25% per file using DSL packing.

### 5. Push everything

```
cd /root/work && git commit -m "Work finalization: [summary]" && git push
```

Commit message should list what was saved and what compression was achieved.

## In-scope snapshot locations

For the DABT tutor project, snapshots go to:
`/root/work/dabt/dabt-tutor/.hermes-snapshots/skills/` (skill snapshots + compressed profiles)
`/root/work/dabt/dabt-tutor/.hermes-snapshots/cron/` (cron job documentation)

## Automated backup safety net

The cron job `work-backup` (script `~/.hermes/scripts/work-backup.sh`, scheduled `0 6 * * 0`) automatically commits and pushes all changes in `/root/work/` weekly. This catches anything missed during manual finalization, but push important work immediately — don't rely on the weekly safety net for high-value artifacts.
