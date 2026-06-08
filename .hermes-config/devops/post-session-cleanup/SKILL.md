---
name: post-session-cleanup
description: Automatic cleanup after heavy work sessions. Delete intermediate artifacts, consolidate redundant files, update working indexes. Runs without user prompt after research sprints, source acquisition, or multi-file operations.
version: 1
status: active
tags: [cleanup, workflow, housekeeping, automation]
---

# Post-Session Cleanup

## Trigger
Run automatically after heavy work sessions (5+ tool calls, multiple file operations, research sprints, source acquisition). No user prompt needed.

## Session closeout directive
If the user says anything like "close out all sessions except this one", act on ALL non-current Hermes sessions — including kanban task sessions, cron sessions, and system/non-interactive sessions. Do not preserve kanban task sessions as a special category. The user already has Kanban as a source of truth; orphaned kanban session records should be removed too.

Protection boundary: only the active/current session ID is exempt. Do not archive away the active chat unless the user explicitly says to resume or rename it.

## What to clean

### 1. Intermediate artifacts
Delete files that served a purpose during the session but aren't deliverables:
- HTML page dumps (`.html`)
- PNG screenshots from browser work (`.png`)
- JSON API/scrape results (`.json`)
- Binary test files (`.bin`)
- Search result pages (Libgen, Google Scholar, etc.)
- Failed download attempts
- Dead-end extraction attempts

### 2. Duplicate/redundant files
When multiple versions of the same content exist (e.g., 6 extracted versions of the same chapter), keep the most complete/clean version and delete the rest.

### 3. Stale working files
Files that served a transient purpose during the session:
- Cloud storage strategy drafts (when the project moved on)
- Temporary analysis files superseded by final versions
- Status/progress notes that are now outdated

### 4. Project index update
After cleanup, update the project's `INDEX.md` (or equivalent) to reflect the current state:
- Update file counts and sizes
- Mark any new deliverables
- Remove references to deleted files
- Update "Last updated" timestamp

## What NOT to delete
- Source PDFs (always keep)
- OCR'd source text (`.txt` from pdftotext/OCR)
- Deliverable extract files (method extracts, lens foundations)
- Translation files and glossaries
- Charter, strategies, and methodology documents
- Skills and verified primary source extracts

## WSL session recovery

When the main Hermes session DB has been cleared or deleted, WSL copies may exist at `~/.hermes/sessions/` on the local machine. Recover by:

1. **Confirm SSH path works**: `ssh local-machine 'hostname && find ~/.hermes/sessions -maxdepth 1 -type f | wc -l'`
2. **Pull WSL sessions**: `rsync -av --ignore-existing local-machine:~/.hermes/sessions/ /tmp/ws-sessions/ && cp /tmp/ws-sessions/* /root/.hermes/sessions/`
3. **Validate**: spot-check restored content with `session_search` or `hermes sessions list` using a known ID/topic.
4. **Merge, don't overwrite**: copy WSL's `sessions.json` to `~/.hermes/sessions/sessions-wsl.json` for reference; do not replace the active VPS `sessions.json`.

## Mnemosyne backup inclusion

The weekly backup cron must snapshot Mnemosyne on both machines:

- VPS: `cp ~/.hermes/mnemosyne/data/mnemosyne.db ~/.hermes/backups/mnemosyne-<timestamp>.db`
- WSL: `scp local-machine:~/.hermes/mnemosyne/data/mnemosyne.db.backup-YYYYMMDD-HHMMSS ~/.hermes/backups/mnemosyne-wsl-<timestamp>.db`

If the live VPS Mnemosyne DB is smaller than a recent WSL backup, prefer the WSL snapshot as the more complete restore source.

## Artifact governance pattern (Hermes sessions)

When cleanup touches Hermes session data (e.g. `~/.hermes/sessions`), apply a retention policy rather than flat deletion:

1. **Keep protected state files**: `sessions.json`, `sessions.db`, and any active session IDs the user still references must never be removed.
2. **Compress + archive old session JSONs**: files older than the cutoff are gzip-compressed into `~/backups/archive/old-sessions/*.gz`, preserving the original mtime so deduplication works on repeated runs.
3. **Rotate config backups**: keep the most recent `config.yaml.bak*`, archive older ones to `~/backups/archive/old-configs/`.
4. **Verify with size + count**: report bytes freed, files compressed, and any errors.

## Verification step
After cleanup, run a quick file count + total size check:
```bash
find <project_root> -type f | wc -l
du -sh <project_root>
```

Report: "Cleanup complete. X files deleted, Y MB freed. Z core files remaining."
