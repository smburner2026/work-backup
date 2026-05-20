---
name: batch-data-enrichment
description: "Parallel batch enrichment of existing datasets using delegate_task with self-review loops. Pattern for enriching SQLite datasets with LLM-generated content (explanations, classifications, corrections) at scale — 1000+ records per hour via parallel subagents."
version: 1.0.0
category: data-science
---

# Batch Data Enrichment — Parallel Subagent Pattern

## When to Use

Load this skill when you need to:
- Enrich a large SQLite dataset with LLM-generated content
- Apply a transformation to 1000+ independent records
- Perform a truth audit against reference sources
- Add structured metadata (categories, quality scores) to every record
- Any task where each record is independent and the operation is LLM-reasoning-heavy

Do NOT use for: mechanical transformations (regex etc.), cross-record reasoning, or tasks needing user interaction per item.

## Architecture

```
Source Data (SQLite)
    │
    ├──→ Reconnaissance → shape, quality, distribution
    ├──→ Config → schema, output format, quality criteria
    ├──→ Split → balanced batches of 50
    ├──→ Delegate → 3 subagents in parallel
    │    ├── Read batch file
    │    ├── Query source DB
    │    ├── Reference lookup
    │    ├── Generate enrichment
    │    ├── Self-review
    │    └── Save output file
    ├──→ Normalize → reconcile format differences
    ├──→ Commit → write to DB, update config
    └──→ Loop → next 3 batches until done
```

## Procedure

### 0. Reconnaissance

```python
import sqlite3
db = sqlite3.connect("data.db")
db.row_factory = sqlite3.Row
total = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
needed = db.execute("SELECT COUNT(*) FROM items WHERE enrichment IS NULL").fetchone()[0]
print(f"Total: {total}, Need enrichment: {needed}")
cats = db.execute("SELECT category, COUNT(*) FROM items GROUP BY category").fetchall()
print(f"Categories: {[(c[0],c[1]) for c in cats]}")
samples = db.execute("SELECT * FROM items LIMIT 5").fetchall()
db.close()
```

**Questions to answer:**
1. Are records independent? (Yes → parallel. No → rethink.)
2. What enrichment per record? (One field? Multiple?)
3. What quality criteria define "done"?
4. Are reference sources available for grounding?
5. What's the distribution across categories? (Need balanced batches?)

### 1. Config

Create a project-level JSON config with: DB path, batch size (50), parallel workers (3), output directory, enrichment criteria, quality thresholds.

### 2. Split Into Batches

Interleave categories for balanced batches. 50 items per batch. Save each as `batches/batchN.json`.

### 3. Delegate (Core Loop)

Per iteration: prepare 3 batches → delegate 3 subagents in parallel → collect outputs → normalize → commit → report.

**Subagent task template:**

```python
delegate_task(tasks=[
    {
        "goal": "Enrich batch N. Read IDs from /path/batches/batchN.json. "
                "For each ID, query DB at /path/db. "
                "Generate enrichment per criteria. "
                "SAVE output to /path/batches/batchN_done.json as JSON array. "
                "SELF-REVIEW before finishing.",
        "context": (
            "DB query: python3 -c \"import sqlite3,json; "
            "db=sqlite3.connect('/path/db'); db.row_factory=sqlite3.Row; "
            "row=db.execute('SELECT * FROM items WHERE id=?',(qid,)).fetchone(); "
            "print(json.dumps(dict(row)))\"\n\n"
            "Output format: [{\"id\": \"X\", \"enrichment\": \"...\", \"category\": \"...\"}]"
        )
    },
    # batch N+1, N+2
])
```

**4 design rules:**
1. **Explicit output path** — `SAVE to /path/batches/batchN_done.json` in goal. Subagents will output to stdout otherwise.
2. **Exact output format** — show the exact JSON schema.
3. **Self-review** — always include `SELF-REVIEW before finishing`.
4. **Query pattern** — provide a working command they can copy-paste.

### 4. Normalize + Commit

Subagents produce JSON in different formats. Handle the three common variants:
- `list` of dicts with id and enrichment keys
- `dict` keyed by ID with enrichment sub-dict
- `dict` keyed by ID with string value directly

Use a normalization step before writing to DB.

### 5. Track Progress

Update a status config after each commit cycle. Report: total done/total, remaining, per-category progress. Loop until remaining = 0.

## The Truth Audit Dividend

When subagents enrich data, they naturally verify it against their knowledge. Capture these findings:

- Extraction errors: "DB says answer E but only options A-D exist"
- Factual errors: "DB says liver not target for cadmium — Casarett says kidney is primary"
- Systematic issues: pattern of errors across batches (e.g., "all matching tests have shifted answer keys")

Record these findings in a reference document for the project. They represent a free truth audit.

## Rules

- **Batch size 50** — large enough for efficiency, small enough for context windows
- **3 parallel workers** — balances throughput against quality per worker
- **ID-order preserves topic clustering** — if source data is chapter/topic ordered
- **Balanced batches** — interleave categories so each batch has representative mix
- **Self-review is mandatory** — every subagent must verify its own output before saving
- **Normalize before commit** — never assume consistent output format
- **Update config after each round** — prevents lost progress on crash

## Pitfalls

- **Subagents lose files without explicit paths** — always include `SAVE TO /absolute/path` in the goal
- **Different output formats** — normalize across all variants before committing
- **Timed-out subagents** — partial output may exist if timeout occurs after file write; check before re-delegating
- **Subagents may patch source DB directly** — this is usually good (they fix errors) but creates implicit changes; audit their patches
- **Token costs are substantial** — each 50-item batch costs ~40K input tokens per subagent; plan accordingly
- **Quality varies by model** — the subagent model must be capable of the reasoning required
