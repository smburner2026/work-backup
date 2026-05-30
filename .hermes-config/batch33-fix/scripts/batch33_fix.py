#!/usr/bin/env python3
"""
Batch33 DB Corrections - Apply fixes to dabt.db
Parses batches/batch33_done.json, extracts "Correct answer: X" from DB-corrected items,
and UPDATEs the SQLite database.
"""
import json
import re
import sqlite3
import os
import shutil
from datetime import datetime

WORKDIR = "/root/work/dabt/dabt-tutor"
DB_PATH = f"{WORKDIR}/reference/data/dabt.db"
BATCH_FILE = f"{WORKDIR}/batches/batch33_done.json"
BACKUP_PATH = f"{WORKDIR}/reference/data/dabt.db.batch33_backup"

def main():
    print(f"=== Batch33 DB Corrections ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"DB: {DB_PATH}")
    print(f"Corrections: {BATCH_FILE}")
    print()
    
    # Step 0: Verify files exist
    if not os.path.isfile(BATCH_FILE):
        print(f"ERROR: Corrections file not found at {BATCH_FILE}")
        return 1
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: Database not found at {DB_PATH}")
        return 1
    
    # Step 1: Read corrections file
    with open(BATCH_FILE) as f:
        corrections = json.load(f)
    
    print(f"Loaded {len(corrections)} items from corrections file")
    
    # Step 2: Find DB-corrected items
    db_corrected = []
    for item in corrections:
        explanation = item.get('explanation', '')
        if 'DB-corrected' in explanation:
            qid = item.get('id', 'N/A')
            # Extract correct answer letter
            match = re.search(r'Correct answer:\s*([A-Z])', explanation)
            if match:
                correct_letter = match.group(1)
                db_corrected.append({
                    'id': qid,
                    'correct_answer_letter': correct_letter,
                    'explanation': explanation
                })
            else:
                print(f"  WARNING: No 'Correct answer: X' found in {qid}: {explanation[:100]}...")
    
    print(f"\nFound {len(db_corrected)} DB-corrected items with parseable answer letters")
    
    if len(db_corrected) == 0:
        # Debug: show a few explanations to help understand the format
        print("\nDEBUG: Showing first 3 items with 'DB-corrected':")
        count = 0
        for item in corrections:
            if 'DB-corrected' in item.get('explanation', ''):
                print(f"  ID: {item.get('id')}")
                print(f"  Explanation (first 200 chars): {item.get('explanation', '')[:200]}")
                count += 1
                if count >= 3:
                    break
        # Also show count of "DB-corrected" strings
        total_db = sum(1 for i in corrections if 'DB-corrected' in i.get('explanation', ''))
        print(f"\nTotal items with 'DB-corrected' in explanation: {total_db}")
    
    # Step 3: Backup database
    if os.path.isfile(BACKUP_PATH):
        print(f"\nBackup already exists at {BACKUP_PATH}, skipping")
    else:
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print(f"\nBackup created at {BACKUP_PATH}")
    
    # Step 4: Connect and apply updates
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check current values before update
    print(f"\n{'='*60}")
    print(f"Applying {len(db_corrected)} corrections...")
    print(f"{'='*60}")
    
    successes = 0
    errors = []
    
    for item in db_corrected:
        qid = item['id']
        correct_letter = item['correct_answer_letter']
        explanation = item['explanation']
        
        try:
            # Get current value
            cursor.execute(
                "SELECT correct_answer_letter FROM questions WHERE id = ?",
                (qid,)
            )
            row = cursor.fetchone()
            if row is None:
                errors.append(f"{qid}: Not found in database")
                continue
            
            old_letter = row[0]
            
            # Update both answer letter and explanation
            cursor.execute(
                "UPDATE questions SET correct_answer_letter = ?, explanation = ? WHERE id = ?",
                (correct_letter, explanation, qid)
            )
            if cursor.rowcount > 0:
                successes += 1
                arrow = "<-- CHANGED" if old_letter != correct_letter else "(same)"
                print(f"  {qid}: {old_letter} -> {correct_letter} {arrow}")
            else:
                errors.append(f"{qid}: No rows updated")
        except Exception as e:
            errors.append(f"{qid}: {str(e)}")
    
    conn.commit()
    conn.close()
    
    # Step 5: Report
    print(f"\n{'='*60}")
    print(f"CORRECTIONS COMPLETE")
    print(f"  Total DB-corrected items: {len(db_corrected)}")
    print(f"  Successfully updated:     {successes}")
    print(f"  Errors:                   {len(errors)}")
    print(f"{'='*60}")
    
    if errors:
        print(f"\nErrors:")
        for e in errors:
            print(f"  {e}")
    
    # Step 6: Verify key items
    print(f"\n{'='*60}")
    print(f"VERIFICATION")
    print(f"{'='*60}")
    
    verify_ids = ['DABT-1820', 'DABT-1827', 'DABT-1819']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for vid in verify_ids:
        cursor.execute(
            "SELECT id, correct_answer_letter FROM questions WHERE id = ?",
            (vid,)
        )
        row = cursor.fetchone()
        if row:
            status = "CORRECT" if row[1] == 'A' else f"WRONG (got {row[1]})"
            print(f"  {row[0]}: correct_answer_letter={row[1]} {status}")
        else:
            print(f"  {vid}: NOT FOUND")
    
    conn.close()
    
    return 0

if __name__ == "__main__":
    exit(main())
