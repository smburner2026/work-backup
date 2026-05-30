# Quarantine Campaign (2026-05-20)

1,048 low-quality/broken questions moved to `quarantine` and `quarantine_answer_options` tables.

**Group A (626):** No answer letter, no options, answer letter mismatches options, or non-standard letters (I–Q). Un-drillable.

**Group B (422):** Option counts not 4–5. Potentially salvageable but incompatible with standard drill pipeline.

**Past ABT PDFs (273):** Real exam questions without published answer keys. Placed in quarantine rather than left as NULL. Needs SME review.

All original data preserved (question_text, options, explanations) with `q_issue` documenting the defect. Restore: `INSERT INTO questions SELECT * FROM quarantine WHERE id = ?` and migrate options.
