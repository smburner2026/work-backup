#!/usr/bin/env python3
"""Scan recent Hermes session transcripts for hallucination patterns.

Runs as a cron script (no_agent=True). Reads the session SQLite DB,
scans messages from the last N hours, logs new pattern matches to
the Obsidian vault. Silently exits if nothing found.

Usage:
    python3 scan_sessions.py [--hours 6] [--vault /root/obsidian-vault]
"""

import argparse
import hashlib
import os
import re
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- Patterns (same as log_pattern.py) ---
PATTERNS = {
    "knowledge_cutoff": {
        "regex": r"(?i)as of my (?:last |knowledge )?cut.?off",
        "risk": "Medium",
        "description": "Knowledge cutoff reference",
    },
    "capability_denial": {
        "regex": r"(?i)I (?:don't|cannot|can't) (?:access|browse|search)",
        "risk": "High",
        "description": "Capability denial while giving specifics",
    },
    "specific_date": {
        "regex": r"(?i)(?:January|February|March|April|May) 20[0-9]{2}",
        "risk": "Medium",
        "description": "Specific date claim — verify",
    },
    "version_number": {
        "regex": r"(?i)version \d+\.\d+\.\d+",
        "risk": "High",
        "description": "Specific version number — verify",
    },
    "vague_authority": {
        "regex": r"(?i)according to (?:the|a) (?:official|latest)",
        "risk": "Medium",
        "description": "Vague authority claim",
    },
    "weasel_words": {
        "regex": r"(?i)it is (?:widely|generally|commonly) (?:known|accepted|believed)",
        "risk": "Low",
        "description": "Weasel words — appeals to consensus",
    },
}

LOG_NOTE = "04-Reference/hallucination-log.md"
DEDUP_FILE = ".hallucination-dedup"
HEADER = """# Hallucination Log

Accumulated pattern matches from AI output validation. Each entry is a signal to verify, not proof of error.

See also: [[hallucination-patterns]] — the pattern reference skill.

---
"""

# --- Session DB locations (Hermes stores messages in SQLite) ---
HERMES_HOME = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))


def find_session_dbs():
    """Find all Hermes session/message SQLite databases."""
    dbs = []
    # LCM database (primary message store)
    lcm_db = HERMES_HOME / "lcm.db"
    if lcm_db.exists():
        dbs.append(lcm_db)
    # Response store
    resp_db = HERMES_HOME / "response_store.db"
    if resp_db.exists():
        dbs.append(resp_db)
    # Legacy session DB
    legacy_db = HERMES_HOME / "data" / "sessions.db"
    if legacy_db.exists():
        dbs.append(legacy_db)
    # Profile-specific DBs
    profiles_dir = HERMES_HOME / "profiles"
    if profiles_dir.exists():
        for profile_dir in profiles_dir.iterdir():
            if profile_dir.is_dir():
                for name in ["lcm.db", "sessions.db"]:
                    pdb = profile_dir / name
                    if pdb.exists():
                        dbs.append(pdb)
    return dbs


def load_dedup(vault_path: Path):
    """Load set of already-logged content hashes."""
    dedup_path = vault_path / DEDUP_FILE
    if not dedup_path.exists():
        return set()
    return set(dedup_path.read_text().strip().split("\n"))


def save_dedup(vault_path: Path, hashes: set):
    """Save dedup hashes, keeping last 5000."""
    dedup_path = vault_path / DEDUP_FILE
    # Keep only last 5000 to prevent unbounded growth
    recent = sorted(hashes)[-5000:]
    dedup_path.write_text("\n".join(recent) + "\n")


def content_hash(text: str, pattern: str) -> str:
    """Hash of (truncated text + pattern) for dedup."""
    key = f"{text[:200]}::{pattern}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def scan_messages(db_path: Path, hours: int):
    """Scan assistant messages from the last N hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    cutoff_ts = cutoff.timestamp()

    matches = []
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Find the messages table — Hermes uses different schemas
        # Try the standard schema first
        tables = [row[0] for row in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()]

        msg_table = None
        for t in ["messages", "message", "conversation_messages"]:
            if t in tables:
                msg_table = t
                break

        if not msg_table:
            conn.close()
            return matches

        # Get column names
        cols = [row[1] for row in cursor.execute(f"PRAGMA table_info({msg_table})").fetchall()]
        col_names = [c[1] for c in cursor.execute(f"PRAGMA table_info({msg_table})").fetchall()]

        # Build query — we want assistant messages from the last N hours
        # Try common timestamp column names
        ts_col = None
        for candidate in ["created_at", "timestamp", "ts", "time", "created"]:
            if candidate in col_names:
                ts_col = candidate
                break

        # Try common role/content column names
        role_col = None
        for candidate in ["role", "type", "sender"]:
            if candidate in col_names:
                role_col = candidate
                break

        content_col = None
        for candidate in ["content", "text", "message", "body"]:
            if candidate in col_names:
                content_col = candidate
                break

        if not all([ts_col, role_col, content_col]):
            conn.close()
            return matches

        # Query assistant messages from last N hours
        query = f"""
            SELECT {content_col}, {ts_col}
            FROM {msg_table}
            WHERE {role_col} = 'assistant'
            AND {ts_col} > ?
            ORDER BY {ts_col} DESC
            LIMIT 500
        """

        rows = cursor.execute(query, (cutoff_ts,)).fetchall()
        conn.close()

        for content, ts in rows:
            if not content or len(str(content)) < 20:
                continue
            # Run patterns
            for pname, info in PATTERNS.items():
                for m in re.finditer(info["regex"], str(content)):
                    matches.append({
                        "pattern": pname,
                        "description": info["description"],
                        "risk": info["risk"],
                        "match": m.group(),
                        "context": str(content)[:300],
                        "hash": content_hash(str(content), pname),
                    })

    except Exception as e:
        # Silently skip broken DBs
        pass

    return matches


def log_to_vault(vault_path: Path, matches: list, dedup: set):
    """Log new matches to the vault note."""
    log_file = vault_path / LOG_NOTE

    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.write_text(HEADER)

    new_matches = [m for m in matches if m["hash"] not in dedup]
    if not new_matches:
        return 0

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    entries = []
    for m in new_matches:
        entry = f"""
### [{now}] Pattern: {m['pattern']}
- **Risk:** {m['risk']}
- **Matched:** `{m['match']}`
- **Context:** _{m['context'][:200]}..._
- **Action taken:** _auto-logged by cron scanner_
"""
        entries.append(entry)
        dedup.add(m["hash"])

    with open(log_file, "a") as f:
        f.write("\n".join(entries))

    return len(new_matches)


def main():
    parser = argparse.ArgumentParser(description="Scan sessions for hallucination patterns")
    parser.add_argument("--hours", type=int, default=6, help="Scan last N hours (default: 6)")
    parser.add_argument("--vault", default=os.environ.get("OBSIDIAN_VAULT_PATH", "/root/obsidian-vault"),
                        help="Obsidian vault path")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.exists():
        print(f"Vault not found: {vault}")
        return

    dedup = load_dedup(vault)
    total_new = 0

    for db_path in find_session_dbs():
        matches = scan_messages(db_path, args.hours)
        if matches:
            new = log_to_vault(vault, matches, dedup)
            total_new += new

    if total_new > 0:
        save_dedup(vault, dedup)
        print(f"Logged {total_new} new hallucination pattern match(es) to {vault / LOG_NOTE}")
    # Silent if nothing found — cron job stays quiet


if __name__ == "__main__":
    main()
