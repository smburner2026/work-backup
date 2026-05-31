#!/usr/bin/env python3
"""
apply_batch_corrections.py — Apply DB corrections from a batchN_done.json file.

Usage: python3 apply_batch_corrections.py <batch_number>

Parses batches/batch{N}_done.json for items whose explanation contains "DB-corrected",
extracts "Correct answer: X", and UPDATEs the dabt.db questions table.

Edit DB_PATH and WORKDIR at the top of this file before running in your environment.
"""
import json, re, sqlite3, shutil, sys, os

# ---- CONFIG ----
WORKDIR = "/root/work/dabt/dabt-tutor"
DB_PATH = f"{WORKDIR}/reference/data/dabt.db"
# ---- END CONFIG ----

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <batch_number>")
        print(f"  Reads batches/batch{{N}}_done.json and applies corrections to dabt.db")
        sys.exit(1)

    batch_n = sys.argv[1]
    batch_file = f"{WORKDIR}/batches/batch{batch_n}_done.json"

    if not os.path.isfile(batch_file):
        print(f"ERROR: {batch_file} not found"); sys.exit(1)
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: {DB_PATH} not found"); sys.exit(1)

    with open(batch_file) as f:
        corrections = json.load(f)
    print(f"Loaded {len(corrections)} items from batch{batch_n}_done.json")

    # Find DB-corrected items
    to_fix = []
    for item in corrections:
        exp = item.get('explanation', '')
        if 'DB-corrected' not in exp:
            continue
        qid = item.get('id', 'N/A')
        m = re.search(r'Correct answer:\s*([A-Z])', exp)
        if m:
            to_fix.append({'id': qid, 'ans': m.group(1), 'exp': exp})
        else:
            print(f"  WARNING: {qid}: 'DB-corrected' but no 'Correct answer: X' found")

    if not to_fix:
        print("No DB-corrected items found. Nothing to do.")
        sys.exit(0)

    print(f"Found {len(to_fix)} items to fix")

    # Backup
    backup = f"{DB_PATH}.batch{batch_n}_backup"
    if not os.path.isfile(backup):
        shutil.copy2(DB_PATH, backup)
        print(f"Backup saved: {backup}")
    else:
        print(f"Backup exists: {backup} (skipping)")

    # Apply corrections
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ok, skipped, errors = 0, 0, []

    for item in to_fix:
        c.execute("SELECT correct_answer_letter FROM questions WHERE id=?", (item['id'],))
        row = c.fetchone()
        if not row:
            # May be in quarantine
            c.execute("SELECT 1 FROM quarantine WHERE id=?", (item['id'],))
            in_quar = c.fetchone()
            if in_quar:
                print(f"  SKIP (quarantine): {item['id']} -> {item['ans']}")
                skipped += 1
            else:
                errors.append(f"{item['id']}: not in questions or quarantine table")
            continue
        old = row[0]
        c.execute("UPDATE questions SET correct_answer_letter=?, explanation=? WHERE id=?",
                  (item['ans'], item['exp'], item['id']))
        ok += 1
        ch = " <-- CHANGED" if old != item['ans'] else " (unchanged)"
        print(f"  {item['id']}: {old} -> {item['ans']}{ch}")

    conn.commit()
    conn.close()

    # Summary
    print(f"\n{'='*50}")
    print(f"Batch {batch_n} corrections applied: {ok}")
    print(f"Skipped (quarantine): {skipped}")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  ERROR: {e}")

    # Verification query for key items
    if ok > 0:
        print(f"\n=== VERIFICATION ===")
        verify_ids = [item['id'] for item in to_fix[:10]]
        if verify_ids:
            conn = sqlite3.connect(DB_PATH)
            placeholders = ','.join('?' * len(verify_ids))
            rows = conn.execute(
                f"SELECT id, correct_answer_letter FROM questions WHERE id IN ({placeholders}) ORDER BY id",
                verify_ids
            ).fetchall()
            for r in rows:
                print(f"  {r[0]}: {r[1]}")
            conn.close()

if __name__ == "__main__":
    main()
