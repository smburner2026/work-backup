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

## Verification step
After cleanup, run a quick file count + total size check:
```bash
find <project_root> -type f | wc -l
du -sh <project_root>
```

Report: "Cleanup complete. X files deleted, Y MB freed. Z core files remaining."
