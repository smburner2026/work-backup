# Parallel Enrichment Pattern — Batch Processing with delegate_task

## Problem

The DABT project regularly needs bulk data enrichment tasks too large for sequential processing:
- Writing explanations for 2,000+ questions
- Classifying bloom levels for 4,841 questions
- Answer recovery from source files for 1,749 questions

Each question is independent — these are embarrassingly parallel workloads.

## Solution: 3-Way Parallel Fan-Out

Use `delegate_task` with 3 concurrent subagents, each with a batch of ~50 IDs.

### Task Design

Each subagent receives: a batch file path, DB connection info, an explicit output path, and the required output format:

```json
{
  "tasks": [
    {"goal": "Write explanations for batch1.json. Save to batch1_done.json as JSON array of {id, explanation, domain}.", "context": "..."},
    {"goal": "Write explanations for batch2.json. Save to batch2_done.json...", "context": "..."},
    {"goal": "Write explanations for batch3.json. Save to batch3_done.json...", "context": "..."}
  ]
}
```

### Batch Size

- **50 Qs/batch** for explanation writing (~3-5 min per subagent)
- **100-200 Qs/batch** for simple classification (bloom levels, topic tagging)
- **20-30 Qs/batch** for complex questions (detailed vignettes, matching tests)

### Output Format Standardization

Subagents vary in output format. Normalize before bulk-committing:

```python
if isinstance(data, list):
    entries = [(e["id"], e["explanation"]) for e in data]  # Preferred
elif isinstance(data, dict):
    if all(isinstance(v, str) for v in data.values()):
        entries = list(data.items())  # Dict of strings
    else:
        entries = [(k, v["explanation"]) for k, v in data.items()]  # Dict of dicts
```

## Self-Review Requirement

Every subagent batch MUST verify before returning:
- All QIDs present and match input
- Each entry has source citation
- Correct answer letter mentioned in explanation
- No hallucinated facts (cross-checked against reference texts)
- JSON is valid

## Edge Cases

### Subagent Timeout (600s limit)
Check for partial output on timeout:
```python
import os
for path in ["/root/work/dabt/dabt-tutor/batches/batchN_done.json", "/root/work/batchN_done.json"]:
    if os.path.exists(path):
        data = json.load(open(path))
```

### Wrong Output Path
Subagents sometimes save to /root/work/ instead of /root/work/dabt/dabt-tutor/batches/.
Check multiple locations when a file isn't found.

### DB Answer Corrections
Subagents often discover DB errors while writing explanations. Some patch the DB directly.
Track what changed: `SELECT id, correct_answer_letter FROM questions WHERE id IN (...)`.

## Performance

| Batch Size | Subagents | Wall Time | Questions/Round |
|------------|-----------|-----------|-----------------|
| 50 Qs | 3 | ~3-5 min | 150 |
| 100 Qs | 3 | ~6-8 min | 300 |

At 150 Qs/round, ~4,841 questions complete in ~30 rounds = ~2-3 hours wall time.

## Scaling Limitation

- Max 3 concurrent subagents (delegation.max_concurrent_children)
- Subagents cannot delegate further (max_spawn_depth=1)
- Fresh terminal session per subagent
- No execute_code/clarify/memory tools in leaf subagents
