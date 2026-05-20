#!/usr/bin/env python3
"""
Extract correct answer letters from Kristen Topic Tests "with answers" docx files
and update the DABT database.

Strategy:
- 4 docx files each contain a topic test with answers in bold
- Each file has its own internal question numbering (Q1, Q2, ...)
- Map internal numbering to DB's question_number_in_source for each topic
- Update the database
- Save a backup JSON
"""

import json
import re
import sqlite3
import sys
from docx import Document

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
SOURCE_DIR = "/root/dabt-curated/Practice_Tests_by_Topic/Kristen_Topic_Tests"

# Mapping: source file -> topic in DB
FILES_MAP = [
    {
        "filename": "Ecotox exam with answers 28 July 2017.docx",
        "topic": "General Toxicology",
    },
    {
        "filename": "Forensic-analytical-clinical exam with answers 28 July 2017.docx",
        "topic": "Drugs & Therapeutics – Toxicology",
    },
    {
        "filename": "Pesticides examination with answers 08 June 2017.docx",
        "topic": "Pesticides – Insecticides",
    },
    {
        "filename": "Risk Assessement Overview examination with answers 05 August 2017.docx",
        "topic": "Risk Assessment & Regulatory",
    },
]


def extract_answers_from_docx(filepath):
    """
    Extract question_number -> answer_letter from a "with answers" docx file.
    
    The answer is indicated by bold formatting on the correct option letter
    (e.g., "A.", "B." etc.). Answers can be:
    - Inline in the question paragraph (same paragraph as question number)
    - In separate paragraphs (one option per paragraph)
    
    Returns: dict of {question_number: answer_letter}
    """
    doc = Document(filepath)
    answers = {}
    
    current_qnum = None
    
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        
        # Check if this paragraph starts a new question
        m = re.match(r'^(\d+)\.\s', text)
        if m:
            current_qnum = int(m.group(1))
            
            # Check for bold answer letter IN the question paragraph itself
            # (some files have the answer inline in the same paragraph)
            for r in p.runs:
                if r.bold and r.text.strip():
                    bold_text = r.text.strip()
                    # Match letter pattern like "A.", "B.", etc.
                    am = re.match(r'^([A-H])\.?\s*$', bold_text)
                    if am:
                        answers[current_qnum] = am.group(1)
                        break
                    # Also check: "A. some text" where the whole thing is bold
                    am2 = re.match(r'^([A-H])\.\s', bold_text)
                    if am2:
                        answers[current_qnum] = am2.group(1)
                        break
            continue
        
        # For paragraphs that are answer options (e.g., "A. text", "B. text")
        # check if they have bold formatting on the letter
        if current_qnum is not None:
            am = re.match(r'^([A-H])\.\s', text)
            if am:
                letter = am.group(1)
                for r in p.runs:
                    if r.bold and r.text.strip():
                        bold_text = r.text.strip()
                        # Check if the bold text starts with the letter
                        bm = re.match(r'^([A-H])\.?\s*', bold_text)
                        if bm and bm.group(1) == letter:
                            # Found it - this option is the correct answer
                            answers[current_qnum] = letter
                            break
                
                # Also handle case where a line has multiple options separated by \n
                # e.g., "A. text\nB. text" - check all runs
                if len(p.runs) > 1:
                    for r in p.runs:
                        if r.bold and r.text.strip():
                            bold_text = r.text.strip()
                            bm = re.match(r'^([A-H])\.?\s*', bold_text)
                            if bm:
                                answers[current_qnum] = bm.group(1)
                                break
    
    return answers


def get_db_questions_for_topic(topic):
    """Get questions from DB for a given topic."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT q.id, q.question_number_in_source, q.correct_answer_letter
        FROM questions q
        JOIN question_topics qt ON q.id = qt.question_id
        WHERE q.source_file_id = 5 AND qt.topic = ?
        ORDER BY q.question_number_in_source
    """, (topic,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_db(updates):
    """
    Update the database with extracted answers.
    updates: list of (db_question_id, answer_letter)
    Returns: number of rows updated
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for qid, answer_letter in updates:
        old_answer = cursor.execute(
            "SELECT correct_answer_letter FROM questions WHERE id = ?", (qid,)
        ).fetchone()
        
        if old_answer:
            old = old_answer[0] or ''
            cursor.execute(
                "UPDATE questions SET correct_answer_letter = ? WHERE id = ?",
                (answer_letter, qid)
            )
            if cursor.rowcount > 0:
                changed = " (was: '{}')".format(old) if old and old != answer_letter else ""
                print(f"  {qid}: '{answer_letter}'{changed}")
                count += 1
    
    conn.commit()
    conn.close()
    return count


def main():
    all_answers = {}  # Mapping file -> {qnum: letter}
    all_updates = []  # List of (question_id, answer_letter, file_qnum, topic)
    
    for file_info in FILES_MAP:
        filepath = f"{SOURCE_DIR}/{file_info['filename']}"
        topic = file_info['topic']
        
        print(f"\n{'='*60}")
        print(f"File: {file_info['filename']}")
        print(f"Topic: {topic}")
        
        # Extract answers from docx
        answers = extract_answers_from_docx(filepath)
        all_answers[file_info['filename']] = answers
        print(f"Extracted {len(answers)} answers from file")
        
        # Get DB questions for this topic
        db_questions = get_db_questions_for_topic(topic)
        print(f"Found {len(db_questions)} questions in DB for this topic")
        
        # Map file question numbers to DB question IDs
        # The file's internal numbering maps directly to question_number_in_source
        for qid, qnum_in_source, current_answer in db_questions:
            if qnum_in_source in answers:
                extracted_letter = answers[qnum_in_source]
                
                # Skip if already correct
                if current_answer == extracted_letter:
                    continue
                
                all_updates.append((qid, extracted_letter, qnum_in_source, topic, current_answer))
            else:
                print(f"  WARNING: Q{qnum_in_source} ({qid}) not found in extracted answers")
        
        # Also check for answers in file that don't have matching DB entries
        for qnum in sorted(answers.keys()):
            found = any(qnum_in_source == qnum for _, qnum_in_source, _ in db_questions)
            if not found:
                print(f"  NOTE: Q{qnum} answer '{answers[qnum]}' found in file but no matching DB question")
    
    print(f"\n{'='*60}")
    print(f"Total updates to make: {len(all_updates)}")
    
    for qid, letter, qnum, topic, old in all_updates:
        old_str = f" (was: '{old}')" if old else " (was: empty)"
        print(f"  {qid} (topic={topic}, Q{qnum}): '{letter}'{old_str}")
    
    # Ask for confirmation
    print(f"\n{'='*60}")
    print("Proceeding with database update...")
    
    # Update DB
    updates_for_db = [(qid, letter) for qid, letter, _, _, _ in all_updates]
    count = update_db(updates_for_db)
    
    print(f"\nUpdated {count} rows in database")
    
    # Save backup mapping
    backup = {
        "source": "Kristen Topic Tests (docx with answers)",
        "source_file_id": 5,
        "db_path": DB_PATH,
        "mapping": {}
    }
    
    for qid, letter, qnum, topic, old in all_updates:
        backup["mapping"][qid] = {
            "question_number": qnum,
            "topic": topic,
            "answer_letter": letter,
            "previous_answer": old or None
        }
    
    # Also add answers that were already correct (unchanged)
    for file_info in FILES_MAP:
        topic = file_info['topic']
        db_questions = get_db_questions_for_topic(topic)
        for qid, qnum_in_source, current_answer in db_questions:
            if current_answer and qid not in backup["mapping"]:
                backup["mapping"][qid] = {
                    "question_number": qnum_in_source,
                    "topic": topic,
                    "answer_letter": current_answer,
                    "previous_answer": current_answer,
                    "status": "unchanged"
                }
    
    backup_path = "/root/work/dabt/kristen_topic_answers.json"
    with open(backup_path, "w") as f:
        json.dump(backup, f, indent=2)
    
    print(f"Backup mapping saved to {backup_path}")
    
    return all_updates


if __name__ == "__main__":
    main()
