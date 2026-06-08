[RECOVERY] Corrupt DB data IS recoverable: dump to SQL→rebuild clean DB→Python merge. sqlite3 ATTACH fails on WAL-corrupt DBs; use Python sqlite3 instead. Check `.corrupt` files before assuming data loss.
[MNEMOSYNE] Installed May 18 2026 (not June 7). Pre-June-7 data recovered from corrupt backups (3,898 working memories + 1,771 facts merged). Full coverage: May 18→present (~5,361 working memories).
[BACKUP] combined-backup.sh Sundays 06:00 UTC: git push → session archive → Mnemosyne (7 daily) → LCM (4 weekly) → other DBs (2 weekly). Cloud (B2) NOT set up yet.
[LCM] 472 sessions, 68K messages, May 18→June 8. Timestamps = session_start (archive lacks per-message). FTS5 text search OK.
§
[2026-06-08] Skill updates: disk-full-mnemosyne-recovery patched with Python cross-schema merge technique + .corrupt file recovery path. hermes-session-recovery patched with cross-store verification checklist + reference file. Key learning: sqlite3 ATTACH fails silently across different schema versions; Python executemany with explicit column lists is the reliable merge strategy.
§
User needs guidance to create Backblaze B2 account and bucket for Hermes backup. Provide step-by-step instructions.