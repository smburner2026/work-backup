#!/usr/bin/env python3
import pandas as pd
import json, random

DB_PATH = "/home/vthen/work/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx"
CLS_PATH = "/home/vthen/work/dabt-tutor/reference/data/question_classifications.csv"
STATE_PATH = "/home/vthen/work/dabt-tutor/progress/state.json"

# Update state with session results
asked_ids = ["DABT-0234", "DABT-0273", "DABT-0111", "DABT-0157", "DABT-0427"]

# Question metadata for state update
q_data = {
    "DABT-0234": {"domain": "Domain III", "bloom": "Remember/Understand", "topic": "Hematology & Blood Toxicity", "correct": False},
    "DABT-0273": {"domain": "Domain III", "bloom": "Apply", "topic": "Metals & Metalloids", "correct": False},
    "DABT-0111": {"domain": "Domain I", "bloom": "Remember/Understand", "topic": "Liver / Hepatotoxicity", "correct": False},
    "DABT-0157": {"domain": "Domain I", "bloom": "Remember/Understand", "topic": "Toxicokinetics / ADME", "correct": False},
    "DABT-0427": {"domain": "Domain II", "bloom": "Apply", "topic": "Carcinogenesis & Mutagenesis", "correct": False}
}

state = json.load(open(STATE_PATH))

# Update session
state["session"]["number"] = 2
state["session"]["date"] = "2025-05-14"  # or whatever today is... let me be approximate
state["session"]["mode"] = "drill"
state["session"]["questions_drilled"] = state["session"].get("questions_drilled", 5) + 5
state["session"]["questions_correct"] = state["session"].get("questions_correct", 3) + 0

# Update cumulative
domain_map = {"Domain I": "domain-i-conduct-of-studies", "Domain II": "domain-ii-mechanistic-tox",
              "Domain III": "domain-iii-risk-assessment", "Domain IV": "domain-iv-applied-tox"}
bloom_map = {"Remember/Understand": "remember-understand", "Apply": "apply", "Analyze": "analyze"}

for qid, meta in q_data.items():
    dk = domain_map[meta["domain"]]
    bk = bloom_map[meta["bloom"]]
    tk = meta["topic"]
    
    # By domain
    d = state["cumulative"]["by_domain"].setdefault(dk, {"correct": 0, "total": 0})
    d["total"] += 1
    if meta["correct"]:
        d["correct"] += 1
    
    # By bloom
    b = state["cumulative"]["by_bloom"].setdefault(bk, {"correct": 0, "total": 0})
    b["total"] += 1
    if meta["correct"]:
        b["correct"] += 1
    
    # By topic
    t = state["cumulative"]["by_topic"].setdefault(tk, {"correct": 0, "total": 0})
    t["total"] += 1
    if meta["correct"]:
        t["correct"] += 1

# Append asked IDs
state["asked_question_ids"].extend(asked_ids)

# Update weak intersections - add misses
for qid, meta in q_data.items():
    if not meta["correct"]:
        dk = domain_map[meta["domain"]]
        bk = bloom_map[meta["bloom"]]
        # Find existing or create new
        found = False
        for w in state["weak_intersections"]:
            if w["domain"] == dk and w["bloom"] == bk and w["topic"] == meta["topic"]:
                w["misses"] += 1
                found = True
                break
        if not found:
            state["weak_intersections"].append({
                "domain": dk, "bloom": bk, "topic": meta["topic"], "misses": 1
            })

# Sort weak intersections by misses descending
state["weak_intersections"].sort(key=lambda x: x["misses"], reverse=True)

# Now sample next set (switch odd to Applied this time)
df = pd.read_excel(DB_PATH, sheet_name="Questions")
cls = pd.read_csv(CLS_PATH)
df = df.merge(cls[["ID", "Domain", "Sub-Domain", "Task", "Bloom Level"]], on="ID", how="left")
asked_set = set(state["asked_question_ids"])
available = df[~df["ID"].isin(asked_set)]

ra_pool = available[available["Domain"] == "Domain III"]
conduct_pool = available[available["Domain"] == "Domain I"]
applied_pool = available[available["Domain"] == "Domain IV"]

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
applied_qs = sample_n(applied_pool, 1, source_used)
set_df = pd.concat([ra_qs, conduct_qs, applied_qs])

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
    "updated_state": state,
    "new_questions": result,
    "source_exams": [int(s) for s in source_used]
}

# Update state file
json.dump(state, open(STATE_PATH, "w"), indent=2)

print(json.dumps(output, indent=2))
