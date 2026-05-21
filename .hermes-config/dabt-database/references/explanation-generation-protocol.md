# Explanation Generation Protocol

Generated 901 exam-quality explanations across all DABT source banks in a single pass using parallel subagents.

## User-Approved Template (2026-05-20)

```
**Answer: X** — [1 sentence: mechanism/rationale for why correct]
**Why not the others:** [1-2 sentences on the most seductive distractor and what makes it wrong. Only flag traps, not every option.]
**Exam tip:** [Optional — 1 sentence: memorisation hook, common confusion, or "the exam will try to trick you by…"]
**Source:** [Textbook.chapter]
```

### Rules
- 3-4 lines max per explanation
- **Mechanism-anchored**: explain WHY the right answer works, not just WHAT it is
- **Distractor trap**: explain the reasoning error someone would make (not every option — just the most seductive one)
- **Exam tip**: only when there's a genuine trick, memory hook, or common confusion worth calling out
- **Sources**: use standard abbreviations — Casarett & Doull (C&D), Hayes, EPA, ICH, OECD, Goldfrank's
- **Accuracy**: every factual assertion must be traceable to a reference — do NOT invent mechanisms

### Examples

**Good (approved):**
> **Answer: B** — bone marrow/spleen — The bone marrow is the primary site of hematopoiesis in mammals, while the spleen serves as a secondary lymphoid organ for clearance of senescent erythrocytes and host defense.
> **Why not the others:** Choice D (thymus/bone marrow) confuses secondary lymphoid function with primary hematopoiesis; the liver and kidney play roles in erythrocyte clearance and erythropoietin production, but the bone marrow is the principal hematopoietic site.
> **Source:** Hematotoxicology (C&D Ch. 10)

**Good (with exam tip):**
> **Answer: C** — Water solubility (blood:gas partition coefficient) is the primary factor determining a gas's penetration depth into the respiratory tract. Highly water-soluble gases (e.g., ammonia, formaldehyde, SO₂) are scrubbed by the nasal mucosa. Poorly soluble gases (e.g., phosgene, NO₂, ozone) penetrate to the alveolar region.
> **Why not the others:** Vapor pressure affects volatility/concentration. Respiratory rate affects total inhaled dose. Vapor density and molecular weight have relatively minor impacts.
> **Exam tip:** Solubility determines site of action: high solubility = upper respiratory (nose/throat), low solubility = lower respiratory (alveoli). Classic example: formaldehyde (high) → nasal cancer; phosgene (low) → pulmonary edema.
> **Source:** C&D 8th ed., Ch. 14

## Parallel Generation Workflow

### Strategy: Source-Based Slicing

Split the 901 questions by source bank, then dispatch each slice as a `delegate_task` subagent. Each subagent:
1. Reads its question slice from a JSON file (pre-exported from the DB with question_text, options, correct_answer_letter)
2. Processes questions in batches of 20-30
3. For each batch: reads data, generates all explanations using its own reasoning, writes UPDATE queries to the DB
4. Commits after each batch
5. Saves incremental progress to a JSON file as backup

### Slice Sizing

| Slice | Source | Questions | Subagent API Calls | Duration |
|-------|--------|-----------|-------------------|----------|
| 1 | Chapter Tests | 576 | ~30 (timed out but partial) | 600s |
| 2 | Kristen Mini + Topic | 237 | 22 | 596s |
| 3 | Past ABT PDFs + 2008-2014 | 88 | ~38 (timed out but partial) | 600s |

Even timed-out subagents usually saved progress to their backup JSON, making recovery straightforward.

### Execution

```bash
# 1. Pre-export questions needing explanations
python3 prep_explain_slices.py  # outputs slice1.json, slice2.json, slice3.json

# 2. Launch parallel subagents (from the agent, not shell)
delegate_task(goal="Generate explanations for slice N", ...)

# 3. After all subagents complete, verify coverage
sqlite3 dabt.db "SELECT COUNT(*) FROM questions WHERE explanation IS NULL OR explanation = ''"

# 4. Fix any corrupt/trivial explanations (single letters, page refs)
# These come from source 6 where the xlsx imported page numbers as "explanations"
python3 fix_corrupt_explanations.py  # or delegate to subagent
```

### Post-Generation Quality Check

```sql
-- Check for missing explanations
SELECT COUNT(*) FROM questions WHERE explanation IS NULL OR explanation = '';

-- Check for trivial/short explanations (likely corrupt)
SELECT id, explanation FROM questions WHERE length(explanation) < 10 AND explanation != '';

-- Check for explanations matching the new template
SELECT COUNT(*) FROM questions WHERE explanation LIKE '**Answer:%';

-- Verify by source
SELECT s.bank_name, 
  SUM(CASE WHEN q.explanation IS NULL OR q.explanation = '' THEN 1 ELSE 0 END) as missing
FROM questions q JOIN source_files s ON q.source_file_id = s.id
GROUP BY s.id ORDER BY missing DESC;
```

### Pitfalls

1. **Corrupt pre-existing explanations**: Source 6 (2008-2014 Past ABT) had 68 questions where the "explanation" was just a single letter ("A", "D.") or a page reference ("pg 832", "p603"). These came from the original xlsx import where answer key data was written into the explanation field. Fix them by exporting the corrupt set to JSON and dispatching a fresh generation subagent.

2. **Subagent timeout**: Subagents have a 600s timeout. For large slices (500+ questions), they may time out before finishing. Mitigation: save progress to a JSON file after every batch, and verify coverage after all subagents return. The backup file lists completed IDs so you can resubmit the remainder.

3. **Template drift**: Without explicit template instructions, subagents may drift toward longer, more verbose explanations. The template must be included in the `context` parameter of each `delegate_task` call.

4. **Source references**: Chapter Test and Kristen questions can reference C&D chapters. Past ABT PDF exam questions may not have clean source references — use the most likely C&D chapter based on topic, or omit the source line.
