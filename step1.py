#!/usr/bin/env python3
import sqlite3
DB = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM questions WHERE source_file_id=10")
print("COUNT before:", cur.fetchone()[0])
cur.execute("DELETE FROM answer_options WHERE question_id IN (SELECT id FROM questions WHERE source_file_id=10)")
print("DEL answer_options:", cur.rowcount)
cur.execute("DELETE FROM questions WHERE source_file_id=10")
print("DEL questions:", cur.rowcount)
cur.execute("DELETE FROM source_files WHERE id=10")
print("DEL source_files:", cur.rowcount)
conn.commit()
conn.close()
print("Deletion phase done")
