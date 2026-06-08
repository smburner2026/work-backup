#!/usr/bin/env python3
"""
Import archived session files from backup into LCM database.
Run after extracting 2026-06-07_old-sessions.tar.zst to a temp directory.
"""

import json
import sqlite3
import gzip
import os
from pathlib import Path

ARCHIVE_DIR = Path(os.environ.get('ARCHIVE_DIR', '/tmp'))
DB_PATH = "/root/.hermes/lcm.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT session_id FROM messages")
    existing = {row[0] for row in cursor.fetchall()}
    print(f"Existing sessions in DB: {len(existing)}")

    imported_count = 0
    skipped_count = 0
    errors = 0

    for gz_file in sorted(ARCHIVE_DIR.glob("session_*.json.gz")):
        try:
            with gzip.open(gz_file, 'rt') as f:
                data = json.load(f)
            session_id = data['session_id']
            if session_id in existing:
                skipped_count += 1
                continue
            platform = data.get('platform', 'unknown')
            source = platform
            for msg in data['messages']:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                tool_call_id = msg.get('tool_call_id', '')
                tool_calls = json.dumps(msg.get('tool_calls', [])) if msg.get('tool_calls') else ''
                tool_name = msg.get('tool_name', '')
                timestamp = data.get('session_start', 0)
                cursor.execute("""
                    INSERT INTO messages (session_id, source, role, content, tool_call_id, tool_calls, tool_name, timestamp, token_estimate)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (session_id, source, role, content, tool_call_id, tool_calls, tool_name, timestamp, len(content)//4))
            imported_count += 1
            if imported_count % 50 == 0:
                conn.commit()
                print(f"  Imported {imported_count} sessions...")
        except Exception as e:
            errors += 1
            print(f"Error importing {gz_file}: {e}")

    conn.commit()
    cursor.execute("SELECT COUNT(DISTINCT session_id) FROM messages")
    total_sessions = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    print(f"\nDone.")
    print(f"  Imported: {imported_count}")
    print(f"  Skipped (duplicates): {skipped_count}")
    print(f"  Errors: {errors}")
    print(f"  Total sessions now: {total_sessions}")
    print(f"  Total messages now: {total_messages}")
    conn.close()

if __name__ == "__main__":
    main()