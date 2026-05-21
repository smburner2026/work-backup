# Data-Mining Commands — Deep Dive Pre-Work

These extract the specific gap pattern from drill data before the diagnostic opening.

## 1. Check topic-level stats from state.json

```bash
python3 -c "import json; s=json.load(open('progress/state.json')); print(json.dumps(s.get('by_topic',{}), indent=2))"
```

Filter for the target topic:
```python
topic = "Metals & Metalloids"
s = json.load(open('progress/state.json'))
stats = s.get('by_topic',{}).get(topic, {})
print(f"{stats.get('correct',0)}/{stats.get('total',0)}")
```

## 2. Pull weak_intersections from state.json

```python
s = json.load(open('progress/state.json'))
for wi in s.get('weak_intersections', []):
    if 'metal' in wi.get('topic','').lower():
        print(wi)
```

## 3. Find the drill session transcript

```python
# Use session_search or check progress/ directory
from pathlib import Path
for f in sorted(Path('progress').glob('*.json')):
    print(f.name)
```

Recent drill snapshots contain `asked_question_ids` and per-question records.

## 4. Extract specific questions from the Excel database

```python
import openpyxl
wb = openpyxl.load_workbook('reference/data/DABT_Practice_Questions_Database.xlsx', read_only=True)
ws = wb['Questions']
headers = [cell.value for cell in next(ws.rows)]

# Get a specific question by ID
target_id = 'DABT-0273'
for row in ws.rows:
    vals = [cell.value for cell in row]
    if vals[0] == target_id:
        print(f"Q: {vals[3]}")
        print(f"A: {vals[4]}")
        print(f"B: {vals[5]}")
        print(f"C: {vals[6]}")
        print(f"D: {vals[7]}")
        print(f"Correct: {vals[12]} - {vals[13]}")
        print(f"Explanation: {str(vals[14])[:400]}")
        print(f"All Topics: {vals[16]}")
        break
```

## 5. Get all questions for a topic (pattern matching)

```python
import openpyxl
wb = openpyxl.load_workbook('reference/data/DABT_Practice_Questions_Database.xlsx', read_only=True)
ws = wb['Questions']
headers = [cell.value for cell in next(ws.rows)]

topic_qs = []
for row in ws.rows:
    vals = [cell.value for cell in row]
    if vals[0] and str(vals[0]).startswith('DABT') and vals[15] == target_topic:
        topic_qs.append(dict(zip(headers, vals)))
```

## 6. Classify missed-question patterns

Group by error type:
- **Regulatory threshold error**: user chose pediatric/adult flip, wrong cutoff
- **Chelator pairing error**: wrong chelator-metal match
- **Clinical reasoning error**: wrong target organ/syndrome
- **Kinetic mechanism error**: wrong ADME or transport

This classification comes from reading the question + explanation + user's wrong answer together.
