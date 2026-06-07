# Phantom Completion Prevention

## Incident: 2026-06-02 — Synthetic Question Generation

### What Happened
- Kanban tasks t_6732e04c, t_cbcb1ceb (Domain I, 1,600 Qs) and t_7befa634, t_f9228efb (Domain III, 600 Qs) were marked DONE
- The dabt-database skill description was updated to claim "1,600 synthetic Domain I Qs and 600 synthetic Domain III Qs generated"
- The task-roadmap.md was updated to list these as completed
- **BUT: the questions were never imported into the database.** Source_files table has no synthetic bank. Total Q count (5,368) exactly matches the 10 existing banks. Domain I still at 1,125, Domain III still at 287.

### Root Cause Chain
1. Subagents were delegated to generate + import questions
2. Subagents may have generated questions to stdout/file but timed out before DB import
3. The orchestrator marked tasks "done" based on subagent self-reports
4. No post-import verification was run
5. Skill description and task-roadmap were updated based on task status, not DB state
6. Truth audits flagged Domain III still at 287 — but as a "coverage gap," not a "failed import"

### What Failed
- **No verification step** existed in the workflow for DB-write operations
- **Self-report trusted as proof** — subagent "done" was taken at face value
- **Documentation updated prematurely** — skill description and task-roadmap were patched before DB verification
- **Audit didn't catch it** — truth audits check current state, not task completion history

### Prevention (now encoded in dabt-project-workflow)

1. **Post-import verification is mandatory** for any DB-write kanban task
2. **Orchestrator must run verification queries independently** before marking done
3. **Phantom completion detection** — if a task claims N records but DB shows no delta, flag as BLOCKED
4. **Documentation update gating** — skill description and task-roadmap updates require DB verification to pass first
5. **File-based intermediate step** — generate to JSON file first, verify file, then import to DB

### Verification Template

```python
import sqlite3

def verify_import(db_path, source_file_id, expected_count, expected_domains):
    """Run after any batch import to confirm data landed."""
    conn = sqlite3.connect(db_path)
    
    # Count check
    actual = conn.execute(
        "SELECT COUNT(*) FROM questions WHERE source_file_id=?", 
        (source_file_id,)
    ).fetchone()[0]
    
    if actual != expected_count:
        return f"FAIL: expected {expected_count} Qs, got {actual}"
    
    # Domain distribution check
    actual_domains = dict(conn.execute(
        """SELECT d.domain, COUNT(*) FROM questions q 
           JOIN question_domains d ON q.id=d.question_id 
           WHERE q.source_file_id=? GROUP BY d.domain""",
        (source_file_id,)
    ).fetchall())
    
    for domain, expected_n in expected_domains.items():
        got = actual_domains.get(domain, 0)
        if got != expected_n:
            return f"FAIL: {domain} expected {expected_n}, got {got}"
    
    conn.close()
    return f"PASS: {actual} Qs imported, domains verified"
```

### Lesson Learned
The kanban system's "done" status is a **claim**, not a **fact**. Any operation with side effects (DB writes, file moves, API calls) requires independent verification before the claim can be trusted. This is especially critical for batch operations delegated to subagents, where the subagent's context window may close before the final verification step.
