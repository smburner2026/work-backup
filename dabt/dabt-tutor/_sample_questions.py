#!/usr/bin/env python3
import pandas as pd
import json, random

DB_PATH = "/home/vthen/work/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx"
CLS_PATH = "/home/vthen/work/dabt-tutor/reference/data/question_classifications.csv"
STATE_PATH = "/home/vthen/work/dabt-tutor/progress/state.json"

df = pd.read_excel(DB_PATH, sheet_name="Questions")
cls = pd.read_csv(CLS_PATH)
df = df.merge(cls[["ID", "Domain", "Sub-Domain", "Task", "Bloom Level"]], on="ID", how="left")

state = json.load(open(STATE_PATH))
asked = set(state.get("asked_question_ids", []))
available = df[~df["ID"].isin(asked)]

ra_pool = available[available["Domain"] == "Domain III"]
conduct_pool = available[available["Domain"] == "Domain I"]
mech_pool = available[available["Domain"] == "Domain II"]

def sample_n(pool, n, source_used):
    avail = pool[~pool["ID"].isin(asked)]
    if len(avail) == 0:
        return pd.DataFrame()
    avail_no_cluster = avail[~avail["Source Exam"].isin(source_used)]
    if len(avail_no_cluster) >= n:
        chosen = avail_no_cluster.sample(n, random_state=random.randint(0, 10000))
    else:
        chosen = avail.sample(min(n, len(avail)), random_state=random.randint(0, 10000))
    source_used.update(chosen["Source Exam"].values)
    return chosen

source_used = set()
ra_qs = sample_n(ra_pool, 2, source_used)
conduct_qs = sample_n(conduct_pool, 2, source_used)
mech_qs = sample_n(mech_pool, 1, source_used)
set_df = pd.concat([ra_qs, conduct_qs, mech_qs])

result = []
for i, (_, row) in enumerate(set_df.iterrows(), 1):
    q = {
        "num": i,
        "question": row["Question"],
        "options": {},
        "id": row["ID"],
        "exam": int(row["Source Exam"]),
        "domain": row["Domain"],
        "bloom": str(row.get("Bloom Level", "N/A")),
        "correct_answer": row["Correct Answer"],
        "correct_text": str(row["Correct Answer Text"]),
        "topic": str(row.get("Topic (Primary)", ""))
    }
    for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        if col in row and pd.notna(row[col]):
            q["options"][col] = str(row[col])
    result.append(q)

print(json.dumps({"questions": result, "source_exams": [int(s) for s in source_used]}, indent=2))
