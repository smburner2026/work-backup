#!/usr/bin/env python3
import pandas as pd, json, random

DB_PATH = "/home/vthen/work/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx"
CLS_PATH = "/home/vthen/work/dabt-tutor/reference/data/question_classifications.csv"
STATE_PATH = "/home/vthen/work/dabt-tutor/progress/state.json"

# Set 2 results
set2 = {
    "DABT-0294": {"domain": "Domain III", "bloom": "Apply", "topic": "Immunotoxicology / Allergy", "correct": False},
    "DABT-0403": {"domain": "Domain III", "bloom": "Remember/Understand", "topic": "Pesticides – Insecticides", "correct": False},
    "DABT-0258": {"domain": "Domain I", "bloom": "Remember/Understand", "topic": "Immunotoxicology / Allergy", "correct": False},
    "DABT-0036": {"domain": "Domain I", "bloom": "Remember/Understand", "topic": "Nervous System / Neurotoxicity", "correct": False},
    "DABT-0369": {"domain": "Domain IV", "bloom": "Apply", "topic": "Metals & Metalloids", "correct": True}
}

state = json.load(open(STATE_PATH))

domain_map = {"Domain I": "domain-i-conduct-of-studies", "Domain II": "domain-ii-mechanistic-tox",
              "Domain III": "domain-iii-risk-assessment", "Domain IV": "domain-iv-applied-tox"}
bloom_map = {"Remember/Understand": "remember-understand", "Apply": "apply", "Analyze": "analyze"}

asked_new = list(set2.keys())
state["asked_question_ids"].extend(asked_new)
state["session"]["questions_drilled"] += 5
state["session"]["questions_correct"] += 1

for qid, meta in set2.items():
    dk = domain_map[meta["domain"]]
    bk = bloom_map[meta["bloom"]]
    tk = meta["topic"]
    d = state["cumulative"]["by_domain"].setdefault(dk, {"correct": 0, "total": 0})
    d["total"] += 1
    if meta["correct"]: d["correct"] += 1
    b = state["cumulative"]["by_bloom"].setdefault(bk, {"correct": 0, "total": 0})
    b["total"] += 1
    if meta["correct"]: b["correct"] += 1
    t = state["cumulative"]["by_topic"].setdefault(tk, {"correct": 0, "total": 0})
    t["total"] += 1
    if meta["correct"]: t["correct"] += 1
    if not meta["correct"]:
        found = False
        for w in state["weak_intersections"]:
            if w["domain"] == dk and w["bloom"] == bk and w["topic"] == tk:
                w["misses"] += 1
                found = True
                break
        if not found:
            state["weak_intersections"].append({"domain": dk, "bloom": bk, "topic": tk, "misses": 1})

state["weak_intersections"].sort(key=lambda x: x["misses"], reverse=True)

# Sample set 3 — odd goes to Mechanistic this round
df = pd.read_excel(DB_PATH, sheet_name="Questions")
cls = pd.read_csv(CLS_PATH)
df = df.merge(cls[["ID", "Domain", "Sub-Domain", "Task", "Bloom Level"]], on="ID", how="left")
asked_set = set(state["asked_question_ids"])
available = df[~df["ID"].isin(asked_set)]

print(f"Available total: {len(available)}")

ra_pool = available[available["Domain"] == "Domain III"]
conduct_pool = available[available["Domain"] == "Domain I"]
mech_pool = available[available["Domain"] == "Domain II"]

print(f"RA: {len(ra_pool)}, Conduct: {len(conduct_pool)}, Mech: {len(mech_pool)}")

def sample_n(pool, n, source_used):
    avail = pool[~pool["ID"].isin(asked_set)]
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

output = {
    "state": state,
    "questions": result,
    "source_exams": [int(s) for s in source_used]
}

json.dump(state, open(STATE_PATH, "w"), indent=2)
# Also write output to a temp file for reading
json.dump(result, open("/tmp/last_set_output.json", "w"), indent=2)
print(json.dumps(output, indent=2))
