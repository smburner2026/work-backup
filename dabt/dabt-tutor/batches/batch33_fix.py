#!/usr/bin/env python3
"""
batch33_fix.py — Apply batch33 DB corrections to dabt.db.

Reads batches/batch33_done.json, extracts DB-corrected answer corrections,
and UPDATEs the live dabt.db. Run with working directory = /root/work/dabt/dabt-tutor/
"""

import json, re, sqlite3, shutil, os, sys

DB = "reference/data/dabt.db"
BATCH = "batches/batch33_done.json"

if not os.path.isfile(BATCH):
    print(f"ERROR: {BATCH} not found. Run from /root/work/dabt/dabt-tutor/")
    sys.exit(1)

with open(BATCH) as f:
    data = json.load(f)

fixes = []
for item in data:
    exp = item.get("explanation", "")
    if "DB-corrected" in exp:
        m = re.search(r"Correct answer:\s*([A-Z])", exp)
        if m:
            fixes.append((item["id"], m.group(1), exp))
        else:
            print(f"WARNING: {item['id']}: has DB-corrected but no 'Correct answer: X' found")

print(f"Found {len(fixes)} corrections to apply from {len(data)} total questions")

# Backup
bak = f"{DB}.batch33_backup"
shutil.copy2(DB, bak)
print(f"Backup saved to {bak}")

conn = sqlite3.connect(DB)
c = conn.cursor()

applied = 0
skipped = 0
for qid, letter, exp in fixes:
    c.execute("SELECT correct_answer_letter FROM questions WHERE id=?", (qid,))
    row = c.fetchone()
    if not row:
        print(f"  SKIP {qid}: not found in questions table (maybe in quarantine?)")
        skipped += 1
        continue
    old = row[0]
    c.execute("UPDATE questions SET correct_answer_letter=?, explanation=? WHERE id=?", (letter, exp, qid))
    changed = " <-- CHANGED" if old != letter else " (already correct)"
    print(f"  {qid}: {old} -> {letter}{changed}")
    applied += 1

conn.commit()
conn.close()
print(f"\nApplied: {applied} corrections. Skipped: {skipped}")

# Verify key corrections
print("\n=== Verification ===")
r = os.popen(f'sqlite3 "{DB}" "SELECT id, correct_answer_letter FROM questions WHERE id IN (\'DABT-1820\',\'DABT-1827\',\'DABT-1819\',\'DABT-1867\')"').read()
print(r)
