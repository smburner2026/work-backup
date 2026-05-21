# Cross-Verification Workflow — Flashcard/Database/Reference Accuracy

## When to Use

- A flashcard's factual claim needs confirmation (half-life, transporter, threshold, chelator pairing)
- A database answer needs verification against primary toxicology references
- You want to run a periodic health check on study system content
- The user asks "is that right?" about any stored study material

## Workflow: Three-Layer Verification

### Layer 1 — Flashcard → Database

Search the 446-question DABT database for a matching question on the same topic:

```python
import pandas as pd
df = pd.read_excel(
    '/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx',
    sheet_name='Questions'
)

# Search for topic terms in question text, answer options, and correct answer text
term = 'antimony'
mask = (df['Question'].str.contains(term, na=False, case=False) |
        df['Correct Answer Text'].str.contains(term, na=False, case=False))
matches = df[mask][['ID', 'Question', 'Correct Answer', 'Correct Answer Text']]
```

If a matching question exists, the flashcard's answer should match the database's
`Correct Answer Text` exactly. The flashcard can add explanatory context (e.g.,
"EDTA chelates lead but NOT mercury") but the core fact must agree.

### Layer 2 — Database Answer → Reference Text

For mechanistic claims, thresholds, half-lives, and regulatory values, verify
against primary toxicology references using the `dabt-reference` three-pass search:

1. **Pass 1 (files-only search)**: Identify which reference source covers the topic
   - Metals, chelation, half-lives → Casarett Ch.23 or Hayes Ch.19
   - Pesticides → Casarett Ch.22 or Hayes Ch.18
   - Risk assessment, BMD → Casarett Ch.4 or Hayes Ch.3
   - Regulations → respective ICH/OECD/EPA/FDA documents

2. **Pass 2 (content search with context)**: Find the exact passage

3. **Pass 3 (read full section)**: Load surrounding context for accuracy

Document every verified claim with its source citation:

```
[Claim] Cd half-life >26 years
[Source] Casarett Ch.23 "Toxic Effects of Metals" pp.1126-1181
[Passage] "The half-life of cadmium in humans is estimated to be more than 26 years"
[Verdict] ✅ CONFIRMED
```

### Layer 3 — Flashcard → Reference Text (direct, no database mediation)

For general-principle flashcards that don't correspond to a specific database
question (e.g., "What property should an ideal chelating agent have?"), skip
Layer 1 and go directly to reference texts. Use chapter-index heuristics:

| General topic | Likely source |
|--------------|---------------|
| Chelation chemistry / HSAB | Casarett Ch.23 introduction |
| Ideal chelator properties | Casarett Ch.23 "General Principles" |
| Metal transport / mimicry | Casarett Ch.23 "Transport" section |
| Biomarker time windows | Casarett Ch.23 "Biomarkers" section |

## Recording Results

After completing all three layers for a flashcard set, record the verification
status. Options:

1. **Inline in the flashcard answer** — append `[Verified: Casarett Ch.23]` to
   the card's answer text. Only if you're editing the card.
2. **Reference file** — maintain a running verification log under
   `dabt-database/references/truth-audit-YYYY-MM-DD.md` for periodic audits.
3. **Done — no record needed** — for single-card spot-checks during a drill
   session where the answer is confirmed mid-conversation.

## Common Pitfalls

- **Database answer ≠ reference truth.** The database may have errors (none
  found in 2026-05-19 audit, but always check). The reference text is the
  ground truth.
- **Regulatory thresholds change.** OSHA PELs, CDC action levels, and EPA
  guidelines are updated. The database and flashcards reflect values at time
  of encoding — verify against current ATSDR/EPA/OSHA documents for
  regulatory questions.
- **Distinguish "treatment threshold" from "regulatory threshold."** Casarett
  says lead chelation at BLL >60 µg/dL, but the OSHA standard is <40 µg/dL.
  Both are correct — they answer different questions (clinical vs regulatory).
- **Bloom level in classification is heuristic (medium confidence).** The
  Remember/Understand vs Apply split was keyword-based; don't treat it as
  authoritative.
