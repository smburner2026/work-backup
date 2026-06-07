# DABT Tutor — Task Roadmap

Updated 2026-06-02 (post-phantom-completion audit).

## Current DB State

- **5,368 questions** across 10 source banks
- **4,698** with answer letters (35 truly lack answer keys)
- **4,546** with explanations
- **5,368** domain-classified (100%)
- **2** quarantine items remaining
- **0 synthetic questions** in DB (generation tasks failed — see phantom completion incident)

## Completed Work (verified ✅)

| Task | Card | Verification | What was achieved |
|------|------|-------------|-------------------|
| Truth audit | t_07d66662 | DB query | 10-checks audit: 6 PASS, 2 PARTIAL, 2 FAIL → spawned 4 follow-ups |
| Classify 466 domain-less Qs | t_3dedb8df | `SELECT COUNT(*) FROM question_domains` | Sources 7+9 classified; 8 stragglers only |
| Import 2015 recert exam | t_cfd11e62 | `SELECT COUNT(*) FROM questions WHERE source_file_id=10` | 40 Qs re-extracted and imported |
| Refresh dabt-config.json | t_c835eebd | Config file updated | Config updated to 5,368 count with all sources |
| Backfill 25 NULL answer_letters | t_99f99a13 | `SELECT COUNT(*) FROM questions WHERE correct_answer_letter='E'` | 25 "answer=E" implied-option items fixed |
| Execute recert SQL import | t_fbf97a68 | `SELECT COUNT(*) FROM questions WHERE source_file_id=10` | 2013+2015 recert Qs imported |
| Verify recert SQL results | t_0ad34e4a | Verification query | Import verified correct |
| Fix 149 Group B Qs | t_f4e9b35d | Manual spot-check | Non-standard option formats normalized |
| Recover 626 Group A Qs | t_321fa0c0 | `SELECT COUNT(*) FROM questions` increased by 626 | Corrupted answer keys recovered from quarantine |
| Fill 1,725 null answer_texts | t_20dc666f | `SELECT COUNT(*) FROM questions WHERE correct_answer_text IS NOT NULL` | Bulk-fill from answer_options |
| Recover 273 Past ABT PDF Qs | t_1f487ac4 | `SELECT COUNT(*) FROM questions WHERE source_file_id=7` | Educated-guess answers for real exam Qs |
| Audit + fix batch33 errors | t_235e8911 et al. | Casarett Ch.6 cross-verification | 34+ corrections verified |
| Classify 62 domain-less Qs | t_1b8101c5 | `SELECT COUNT(*) FROM question_domains` | Source 6 Past ABT Exams classified |
| Audit 502 EXCEPT/NOT Qs | t_bb28e906 | Manual review | Reversal-prone questions reviewed |
| Systems integrity audit | t_ae24e2ca | Multi-system check | Skills, LCM, Mnemosyne, DB verified |

## ⚠️ Phantom Completion Incidents (NOT completed)

| Task | Claimed | Actual | Root Cause |
|------|---------|--------|------------|
| Synthetic Domain I (1,600 Qs) | t_6732e04c + t_cbcb1ceb marked DONE | **0 questions in DB** — no source_file_id, no synthetic bank | Subagent generated but never imported; orchestrator marked done without verification |
| Synthetic Domain III (600 Qs) | t_7befa634 + t_f9228efb marked DONE | **0 questions in DB** — same issue | Same root cause |
| Web audit synthetic Qs (20%) | t_492c8817 marked DONE | **Audit was of non-existent data** | Depended on phantom completions above |

**Impact:** Domain I remains at 1,125 Qs (21% of bank vs 36% exam weight). Domain III remains at 287 Qs (5.3% of bank vs 38% exam weight). These are the two highest-weight exam domains and the DB is critically underweight for both.

**See:** `references/phantom-completion-prevention.md` for the full incident report and prevention protocol.

## Remaining Work Items

### 1. Synthetic Question Generation (REQUIRES RE-EXECUTION)
- **Domain III**: 600 synthetic Qs needed (287 current → 887 target)
- **Domain I**: 1,600 synthetic Qs needed (1,125 current → 2,725 target)
- **Must follow the updated workflow**: generate to JSON → verify JSON → import to DB → verify DB → mark done
- See `dabt-database` skill → "Synthetic Question Generation — Protocol" for the updated workflow

### 2. No-Answer-Key Question Answers (35 Qs)
- 35 Qs across 2 sources with `no_answer_key=1`
- Option: educated-guess generation (like t_1f487ac4 methodology)
- Risk: wrong answers propagate as "correct" and train exam failure
- Needs decision: generate with confidence flagging or leave as discussion prompts

### 3. Full 2015 recert extraction (Parts A-D)
- Current: only 40 Part A Qs imported (t_cfd11e62)
- Remaining: Parts B-D not extracted
- Materials at reference/exam-materials/practice-exams/abt-2015-recert/
- Known no-answer-key (no official key published)

### 4. Domain II mechanistic depth
- 926 Qs (17.2% of bank vs 13% exam weight) — slightly over-represented
- But mechanistic depth is sparse — many batch explanations revealed 25-58% error rates
- Option: synthetic Domain II generation if mechanistic tutoring reveals gaps

### 5. Domain III explanation gap
- 95/287 Domain III questions (33%) lack explanations
- Mostly risk assessment topics (dose-response, hazard ID, risk characterization)
- Enrichment requires Casarett Ch.4, Hayes Ch.3/10, EPA guidelines
