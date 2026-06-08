# Recovery Findings — 2026-06-08

## What was recovered

- **Backup archives**: `/root/.hermes/backups/` (39M compressed old-sessions, mnemosyne DB, request dump)
- **WSL sessions**: `/root/.hermes/sessions/sessions-wsl.json` (851 lines, May 21+)
- **Session .jsonl files**: `/root/.hermes/sessions/` (303M, dates 2026-05-16 through present)

## What the user expected

- Sessions from May 20 and older should appear in `session_search` after recovery.
- Recovery via backup → auto-populate live DB.

## What actually happened

- Recovery preserves files but does NOT auto-merge into `session_search`.
- Live DB only returns post-hygiene cluster (May 30+).
- WSL history exists in `sessions-wsl.json` but is not indexed by `session_search`.

## Disk hygiene actions taken

- Old session `.json.gz` collection bundled into:
  - `/root/.hermes/backups/2026-06-07_old-sessions.tar.zst` (36M)
  - `/root/.hermes/backups/2026-06-07_archive.tar.zst` (37M)
- Removed loose directories under `/root/.hermes/backups/archive/`
- Left only `${backup}.db` and `${backup}.db.backup-YYYY-MM-DD` files

## Open action

- Merge WSL sessions into main session_search index, or document them so they remain recoverable.
- Address output truncation issue in delivered responses.
