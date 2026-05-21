# DABT Material Batch Onboarding

When the user acquires a new batch of exam materials (ZIP of study guides, recert
exams, lecture notes, textbook PDFs), use this pipeline to evaluate, dedup, and
integrate what's novel.

## Value Tiers

| Tier | Category | Priority | Action |
|------|----------|----------|--------|
| HIGH | Recert exam questions | Digest first | Dedup against existing 446-question Mini-ABT bank; merge novel questions into the database |
| MEDIUM | Lecture notes (ACT, MAT, etc.) | Digest second | Distill key exam-relevant concepts into wiki notebook pages |
| LOW | Textbook PDFs / regs | Check, then skip unless novel | Redundant if we already have Casarett 9e + Hayes 7e + 29 regulatory docs extracted |
| SKIP | Duplicates, self-study flashcards, course syllabi | Flag for deletion | No integration value |

## Pipeline

### Phase 1 — Tree & Dedup Scan

1. Unpack the ZIP to a working directory (`/tmp/material-audit/`)
2. Run a file tree: `find` by type (`.pdf`, `.docx`, `.pptx`, `.txt`, `.xlsx`)
3. Check for textbook PDFs against existing reference library at
   `/root/work/dabt/dabt-tutor/reference/extracted/`:
   - Match by title keywords (Casarett, Hayes, Klaassen, Hodgson, etc.)
   - If the same edition → redundant, skip
   - If a different text or newer edition → flag as potentially novel
4. Identify recert exam files: look for question-answer patterns, exam numbers,
   "Mini-ABT", "recert", "practice exam" in filenames
5. Separate lecture notes into their own directory for Phase 3

### Phase 2 — Recert Exam Integration (HIGHEST value)

For each exam file found:

1. Extract questions programmatically:
   - PDF: attempt `python-docx` or `pdftotext` extraction; if image-based, use OCR
   - DOCX: parse with `python-docx`, look for numbered-question patterns
2. **Always check the docx files for embedded answer keys** before relying on standalone answer PDFs. Many 2000Q-style question banks have an answer section at the bottom of the same docx (e.g., "CHAPTER XX ANSWERS (REFERENCES)"). These are authoritative — they come with the questions in the same document — and may differ from standalone answer PDFs which can have errors or be incomplete.
3. **Cross-reference multiple answer sources when both exist.** In the 2000Q bank, the standalone Tox 2000 Answers.pdf had 9 wrong answers (Q1476–Q1484) compared to the embedded docx answer sections. The embedded docx answers are authoritative. When they conflict, verify against the question content — the embedded answers were correct in every case checked.
4. **Check coverage completeness.** A standalone answer PDF may only cover a subset of question IDs. The Tox 2000 Answers.pdf covered Q1–Q1484, but the question bank continues to Q1999. The remaining Q1485–Q1999 all had embedded answers in the docx files. Always verify: count max question ID in answers vs max question ID in source files.
5. **Watch for misspelled answer key filenames.** Some answer files use "explainations" (misspelled) instead of "explanations" — find patterns like `*explain*` or `*answer*` rather than exact names to catch these.

Compare against the existing database at
   `/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx`:
   - Match by question text similarity (fuzzy match on first 80 chars)
   - Match by answer option content where question text differs
3. **Novel questions** → append to a backup copy of the database, then propose
   merging to the user. Tag with source = "recert-YY" or "batch-YYYY-MM-DD".
4. **Likely duplicates** → report count with confidence level

### Phase 3 — Lecture Notes → Wiki Notebook

For lecture notes (ACT course, Mid-American Toxicology, etc.):

1. Identify distinct topic areas (metals, pesticides, kinetics, etc.)
2. For each topic with a substantial treatment not already deep-dived:
   - Extract key exam-relevant points (thresholds, chelators, mechanisms)
   - Cross-reference against existing wiki pages in `/root/work/dabt/dabt-tutor/wiki/concepts/`
   - Offer to create or update a page with the synthesis
3. Low-signal content (course outlines, repeated slides) → discard

### Phase 4 — Textbook/Reg Novelty Check

For any textbook PDF not already in the reference library:

1. Extract the table of contents (first 10-20 pages)
2. Compare chapter titles / edition number against existing references
3. If novel source or newer edition: flag for full extraction pipeline
   (see `references/reference-setup.md` for the extraction procedure)
4. If same source + same/older edition: flag as redundant, propose deletion

### Phase 5 — Report

Deliver a structured summary:

```
Batch: [file name] | [size]
────────────────────────────────
Recert exams:   N files → N novel questions found, N duplicates
Lecture notes:  N files → N topics suitable for notebook
Textbooks:      N files → [N novel / N redundant / N unknown]
Regs:           N files → [N novel / N redundant]

Disk saved by dedup: ~X MB
Questions for user: [e.g., "Merge N novel recert questions into database?"]
```

## Pitfalls

- **Don't trust OCR for high-stakes dedup** — always do a manual spot-check on
  a sample before bulk-merging questions into the production database
- **Don't delete source files** — move to `/tmp/material-audit/redundant/`
  instead, in case the user wants to verify before permanent deletion
- **Lecture notes can contain exam answer keys** — if the notes include
  question-answer pairs, treat as potential recert exam material, not just notes
- **File size ≠ value** — a 5 MB PDF of redundant textbook pages is worthless;
  a 200 KB DOCX of 20 recert questions is high value
- **Watch for mixed-content PDFs** — some files combine lecture slides with
  embedded practice questions. Split before processing.
- **Docx files may have embedded answer sections at the end** — always extract the full docx text before concluding no answer key exists. Files like "2000Q MEDICAL TOXICOLOGY.docx" embed "CHAPTER XX ANSWERS (REFERENCES)" sections after the last question.
- **Standalone answer PDFs can be incomplete** — verify by checking max answer ID vs max question ID. Tox 2000 Answers.pdf covered Q1-Q1484 but not Q1485-Q1999 (found embedded in docx files).
- **Don't trust a single answer source when multiple exist** — standalone PDFs and embedded docx answers may disagree (9 confirmed errors in PDF vs embedded). The embedded answer (same document) is authoritative.
- **Exam sets may have 100% overlap under different naming** — "Mini-ABT Exams 1-11" and "Kristen's Mini Exams" had the same content. Run pairwise question-text comparison across directories.
- **Catch misspelled answer key filenames** — "with explainations" instead of "explanations". Use broad patterns like `*explain*` or `*answer*`.
- **Parallel subagent extraction for large collections** — 100+ files: spin up subagents per category in parallel. Each extracts text, counts questions, identifies formats, outputs structured report. Orchestrator cross-references.
- **Inline answer formatting** — in some exam sets, answers are marked with `*` or descriptive text in option lines, not as a separate answer key section.
