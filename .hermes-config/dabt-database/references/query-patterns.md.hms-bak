# Query Patterns

All queries use `dabt-config.json` for paths and weights.

## Load Database
```python
import sqlite3, pandas as pd
conn = sqlite3.connect('/root/work/dabt/dabt-tutor/reference/data/dabt.db')

# All questions with topics and domains
df = pd.read_sql("""
    SELECT q.*, t.topic, d.domain, d.sub_domain, d.task
    FROM questions q
    LEFT JOIN question_topics t ON q.id = t.question_id
    LEFT JOIN question_domains d ON q.id = d.question_id
""", conn)

# Flat with options
df_full = pd.read_sql("""
    SELECT q.id, q.question_text, q.correct_answer_letter,
           a.option_letter, a.option_text
    FROM questions q
    JOIN answer_options a ON q.id = a.question_id
""", conn)
```

## Filter by Topic
```python
topic_df = pd.read_sql("""
    SELECT q.* FROM questions q
    JOIN question_topics t ON q.id = t.question_id
    WHERE t.topic = 'Metals & Metalloids'
""", conn)
```

## Blueprint-Weighted Sampling (preferred)
```python
import json, sqlite3, random
with open('/root/work/dabt/dabt-tutor/dabt-config.json') as f:
    CONFIG = json.load(f)
WORKDIR = CONFIG['project']['workdir']
DB_PATH = f"{WORKDIR}/{CONFIG['database']['primary']['path']}"
conn = sqlite3.connect(DB_PATH)

TARGET = CONFIG['drill_config']['target_distribution_per_10']
state = json.load(open(f"{WORKDIR}/{CONFIG['progress']['state_path']}"))
asked = set(state.get('asked_question_ids', []))

def sample_by_exam_weight(n=5, asked_ids=set()):
    weights = {'Domain III': max(1, int(n * 0.38)),
               'Domain I': max(1, int(n * 0.36)),
               'Domain II': max(0, int(n * 0.13)),
               'Domain IV': max(0, int(n * 0.13))}
    result = []
    for domain, count in weights.items():
        if count == 0: continue
        placeholders = ','.join('?' * len(asked_ids)) if asked_ids else 'NULL'
        query = f"""
            SELECT q.*, COALESCE(d.sub_domain, ''), COALESCE(d.task, '')
            FROM questions q
            JOIN question_domains d ON q.id = d.question_id
            WHERE d.domain = ? AND q.id NOT IN ({placeholders})
            ORDER BY RANDOM() LIMIT ?
        """
        rows = conn.execute(query, [domain] + list(asked_ids) + [count]).fetchall()
        result.extend(rows)
    return result

def sample_from_domain(domain, n, asked_ids, exclude_sources=None):
    placeholders = ','.join('?' * len(asked_ids)) if asked_ids else 'NULL'
    source_filter = ""
    if exclude_sources:
        source_filter = "AND q.source_file_id NOT IN (" + ','.join(map(str, exclude_sources)) + ")"
    query = f"""
        SELECT q.* FROM questions q
        JOIN question_domains d ON q.id = d.question_id
        WHERE d.domain = ? AND q.id NOT IN ({placeholders}) {source_filter}
        ORDER BY RANDOM() LIMIT ?
    """
    return conn.execute(query, [domain] + list(asked_ids) + [n]).fetchall()

def domain_iii_depletion_check():
    threshold = CONFIG['drill_config']['domain_iii_conservation']['warning_threshold']
    state = json.load(open(f"{WORKDIR}/{CONFIG['progress']['state_path']}"))
    asked = set(state.get('asked_question_ids', []))
    placeholders = ','.join('?' * len(asked)) if asked else 'NULL'
    remaining = conn.execute(f"""
        SELECT COUNT(*) FROM questions q
        JOIN question_domains d ON q.id = d.question_id
        WHERE d.domain = 'Domain III' AND q.id NOT IN ({placeholders})
    """).fetchone()[0]
    return {'remaining': remaining, 'threshold': threshold, 'depleted': remaining <= threshold}
```
