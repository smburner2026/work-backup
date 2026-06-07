#!/usr/bin/env python3
"""Log a hallucination pattern match to the Obsidian vault.

Usage:
    python3 log_pattern.py --pattern "version_number" \
        --text "the matched excerpt" \
        --model "model-name" \
        --context "what was being asked" \
        [--vault /root/obsidian-vault]
"""

import argparse
import os
import re
from datetime import datetime, timezone
from pathlib import Path

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
HEADER = """# Hallucination Log

Accumulated pattern matches from AI output validation. Each entry is a signal to verify, not proof of error.

See also: [[hallucination-patterns]] — the pattern reference skill.

---
"""


def scan_text(text: str) -> list[dict]:
    """Scan text against all patterns, return matches."""
    matches = []
    for name, info in PATTERNS.items():
        for m in re.finditer(info["regex"], text):
            matches.append({
                "pattern": name,
                "description": info["description"],
                "risk": info["risk"],
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            })
    return matches


def log_entry(vault_path: Path, pattern: str, text: str, model: str, context: str):
    """Append a log entry to the Obsidian note."""
    log_file = vault_path / LOG_NOTE

    # Create note with header if it doesn't exist
    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.write_text(HEADER)

    # Get pattern info
    info = PATTERNS.get(pattern, {"risk": "Unknown", "description": pattern})

    # Build entry
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    entry = f"""
### [{now}] Pattern: {pattern}
- **Model:** {model}
- **Context:** {context}
- **Matched:** `{text[:500]}`
- **Risk:** {info['risk']}
- **Action taken:** _pending review_
"""

    # Append
    with open(log_file, "a") as f:
        f.write(entry)

    print(f"Logged: {pattern} ({info['risk']}) → {log_file}")


def main():
    parser = argparse.ArgumentParser(description="Log hallucination pattern to Obsidian vault")
    parser.add_argument("--pattern", default=None, help="Pattern name (knowledge_cutoff, capability_denial, etc.)")
    parser.add_argument("--text", default=None, help="Text that matched")
    parser.add_argument("--model", default="unknown", help="Model that produced the text")
    parser.add_argument("--context", default="", help="What was being asked/produced")
    parser.add_argument("--vault", default=os.environ.get("OBSIDIAN_VAULT_PATH", "/root/obsidian-vault"),
                        help="Obsidian vault path")
    parser.add_argument("--scan", help="Scan text for all patterns instead of logging a specific one")
    args = parser.parse_args()

    vault = Path(args.vault)

    if args.scan:
        matches = scan_text(args.scan)
        if matches:
            print(f"Found {len(matches)} pattern match(es):")
            for m in matches:
                print(f"  [{m['risk']}] {m['pattern']}: {m['match']!r}")
        else:
            print("No patterns matched.")
        return

    if not args.pattern or not args.text:
        parser.error("--pattern and --text are required when not using --scan")

    log_entry(vault, args.pattern, args.text, args.model, args.context)


if __name__ == "__main__":
    main()
