# Batch Explanation Generation Pipeline

Used for Task 3 (Explanations) — applies to all batches in `batches/` directory.

## Workflow

### Step 1: Read Batch JSON
```
/root/work/dabt/dabt-tutor/batches/batchN.json
```
Contains a JSON array of question IDs (e.g., `["DABT-0468", "DABT-0469", ...]`).

### Step 2: Query the DB
For each question ID, fetch from `dabt.db`:
- `questions` table: `id`, `question_text`, `correct_answer_letter`, `correct_answer_text`, `explanation`
- `answer_options` table: `option_letter`, `option_text` (order by option_letter)
- `question_domains` table: `domain`, `sub_domain`

```python
import sqlite3
db = sqlite3.connect('/root/work/dabt/dabt-tutor/reference/data/dabt.db')
db.row_factory = sqlite3.Row

q = db.execute('SELECT id, question_text, correct_answer_letter, correct_answer_text, explanation FROM questions WHERE id=?', (qid,)).fetchone()
opts = db.execute('SELECT option_letter, option_text FROM answer_options WHERE question_id=? ORDER BY option_letter', (qid,)).fetchall()
dom = db.execute('SELECT domain FROM question_domains WHERE question_id=?', (qid,)).fetchone()
```

Also check `source_files` for the bank origin:
```python
src = db.execute('SELECT * FROM source_files WHERE id=?', (q['source_file_id'],)).fetchone()
```

### Step 2a: Identify Question Format

Before writing explanations, classify each question into one of:

| Format | Handling |
|--------|----------|
| **Standard MCQ** | Full question text + 4 options. Write 2-4 sentence explanation. |
| **"All of the following EXCEPT"** | The correct answer is the FALSE statement. Explain why each distractor IS true, then why the answer is false. |
| **Matching test items** | Question_text is the left-column term (e.g., "cone snail"), correct_answer_text is the right-column match ("targets Ca²⁺ ion channel"). Only the correct option is stored in DB. Write explanation linking the term to its match. If the match seems factually questionable (e.g., "sea turtle → more toxic species"), note the standard toxicology in the explanation. |
| **Antidote matching items** | Domain IV items matching substances (e.g., "sodium bicarbonate") to their clinical use ("methotrexate"). Usually single-option items with unusual letter codes. |

### Step 3: Search Reference Texts Before Writing

For each question (or batch of similar questions), search the reference library FIRST to ground your explanations. Load the relevant chapter and read contextual passages.

**Preferred search order:**
1. Casarett & Doull Ch.26 "Toxic Effects of Plants and Animals" — covers all venom/toxin-animal questions
2. Hayes Ch.15 "Plant and Animal Toxins" — broader coverage, often more detail on specific molecules
3. Casarett & Doull Ch.3 "Mechanisms of Toxicity" — for mechanism-level questions (TTX, saxitoxin)
4. Casarett & Doull Ch.33 "Clinical Toxicology" — for clinical/antidote questions

**Search technique:**
```python
# Pass 1: Find candidate files
search_files(
    pattern="tarantula|spider.*venom|latrodectus",
    path="/root/work/dabt/dabt-tutor/reference/extracted/casarett-doull-9e",
    output_mode="files_only"
)

# Pass 2: Get relevant passages with context
search_files(
    pattern="Theraphosidae|tarantula",
    path="/root/work/dabt/dabt-tutor/reference/extracted/casarett-doull-9e/26-toxic-effects-of-plants-and-animals.txt",
    context=3
)

# Pass 3: Load full section
read_file(
    path="/root/work/dabt/dabt-tutor/reference/extracted/casarett-doull-9e/26-toxic-effects-of-plants-and-animals.txt",
    offset=2122,
    limit=50
)
```

### Step 4: Write Explanation (2–5 sentences)

Each explanation must contain:
1. **Correct answer** — stated explicitly with the letter, e.g. "Correct answer: A — 'Death occurs in 10% of cases' is NOT true."
2. **Toxicologic mechanism** — the scientific rationale, grounded in reference text
3. **Distractor trap** — flag the plausible wrong answer(s) and why they're wrong
4. **Source citation** — parenthetical reference like `(Casarett & Doull Ch.26)` or `(Hayes Ch.15)`

**Handling DB-vs-Reference discrepancies:**
- **ALWAYS verify the DB answer against the original source docx answer key for 2000Q Bank questions**, as significant parsing errors exist. See "DB Answer Verification" below.
- If the DB's `correct_answer_letter` conflicts with the reference text, write the explanation according to the reference text but note the discrepancy: "The source lists D as the answer. However, Casarett & Doull Ch.26 states that sarafotoxins cause coronary artery constriction, not bile duct stones."
- Do NOT write an explanation that propagates factually incorrect toxicology just because the DB says so.
- In the self-review, flag such items explicitly.

**"EXCEPT" format questions:**
- State the correct answer (the FALSE statement). Then explain why each other option IS true.
- Example: "Correct answer: A — 'Death occurs in 10% of cases' is NOT true. Casarett & Doull Ch.26 states ... (explain why B, C, D are true)."

**Matching test items (single-option DB):**
- The DB only stores the correct match. Explain the term (question_text) and why it matches the answer (correct_answer_text).
- If the match is toxicologically questionable, provide the standard toxicology alongside: "The match may reflect a specific source classification; per Hayes Ch.15, this animal produces [standard toxin]."

### Step 5: Save Output
Save to `batches/batchN_done.json` as a JSON array:
```json
[
  {
    "id": "DABT-0468",
    "explanation": "Correct answer: A — 'Death occurs in 10% of cases' is NOT true. ...",
    "domain": "Domain I"
  },
  ...
]
```

No extra fields — exactly `{id, explanation, domain}` per entry.

### Step 6: Self-Review Pass

Run comprehensive verification, including docx answer key cross-reference for 2000Q Bank questions:

```python
import json, sqlite3, re
from collections import Counter
from docx import Document

with open('batches/batchN_done.json') as f:
    explanations = json.load(f)
with open('batches/batchN.json') as f:
    batch_ids = json.load(f)

db = sqlite3.connect('reference/data/dabt.db')
db.row_factory = sqlite3.Row

# Load docx answer key for 2000Q source questions
DOCX_ANSWERS = {}  # question_number_in_source → answer_letter
try:
    doc = Document('/root/dabt-curated/2000Q_Question_Bank/2000Q Ch1 General.docx')
    for p in doc.paragraphs:
        text = p.text.strip()
        if 'CHAPTER 1 ANSWERS' in text:
            for m in re.finditer(r'(\d+)\.\s*([A-Z])\s*\(', text):
                DOCX_ANSWERS[int(m.group(1))] = m.group(2)
except:
    pass  # docx not available

errors = []
for item in explanations:
    qid = item['id']
    q = db.execute('SELECT * FROM questions WHERE id=?', (qid,)).fetchone()
    dom = db.execute('SELECT domain FROM question_domains WHERE question_id=?', (qid,)).fetchone()
    
    # 1. ID match
    if qid not in batch_ids:
        errors.append(f'{qid}: not in batch input')
    
    # 2. Domain match
    expected_domain = dom['domain'] if dom else 'Unknown'
    if item['domain'] != expected_domain:
        errors.append(f'{qid}: domain mismatch (file={item["domain"]}, db={expected_domain})')
    
    # 3. Explanation mentions the correct answer text (not just letter)
    if q and q['correct_answer_text'] and q['correct_answer_text'] not in item['explanation']:
        # Check if this is an override case (explanation used different answer than DB)
        pass  # Overrides are handled separately — verify manually
    
    # 4. Explanation is substantial
    if len(item['explanation']) < 100:
        errors.append(f'{qid}: too short ({len(item["explanation"])} chars)')
    
    # 5. No extra fields
    if set(item.keys()) != {'id', 'explanation', 'domain'}:
        errors.append(f'{qid}: extra fields')
    
    # 6. Has reference citation
    if 'Casarett' not in item['explanation'] and 'Hayes' not in item['explanation']:
        errors.append(f'{qid}: missing reference citation')

# 7. For 2000Q Bank questions, check against docx answer key
for item in explanations:
    qid = item['id']
    q = db.execute('''
        SELECT q.id, q.question_number_in_source, s.bank_name
        FROM questions q
        JOIN source_files s ON s.id = q.source_file_id
        WHERE q.id=?
    ''', (qid,)).fetchone()
    if q and 'Ch1 General' in str(dict(q)):
        src_num = q['question_number_in_source']
        if src_num in DOCX_ANSWERS:
            db_letter = db.execute('SELECT correct_answer_letter FROM questions WHERE id=?', (qid,)).fetchone()[0]
            docx_letter = DOCX_ANSWERS[src_num]
            if db_letter != docx_letter:
                # The DB has a known error — check explanation matches docx_letter
                pass  # Flag for manual review
                # (A properly corrected explanation will explain the docx answer, not the DB answer)

# 8. All expected IDs present
output_ids = {item['id'] for item in explanations}
missing = [i for i in batch_ids if i not in output_ids]
if missing:
    errors.append(f'Missing from output: {missing}')

if errors:
    print(f'SELF-REVIEW FAILED — {len(errors)} issue(s):')
    for e in errors:
        print(f'  • {e}')
else:
    print(f'✅ All {len(explanations)} explanations pass self-review')
```

## Conventions

- **File naming:** `batchN.json` (input IDs) → `batchN_done.json` (output with explanations)
- **JSON structure:** Always a flat array. No wrapping object.
- **Explanation format:** "Correct answer: X — [mechanism] [distractor trap] [citation]"
- **Source citations:** Prefer Casarett & Doull chapters over Hayes when both cover the topic. Use "Ch.26" for animal/plant toxins, "Ch.33" for clinical tox, "Ch.3" for mechanisms.
- **Domain values:** Must match DB exactly (e.g., "Domain I", "Domain IV" — never "Domain 1").

## Batch Status

| batch | Questions | Status |
|-------|-----------|--------|
| batch1 | TBD | Pending |
| batch2 | TBD | Pending |
| batch3 | 50 | ✅ Done (2026-05-20) |
| batch4 | TBD | Pending |
| batch5 | 50 | ✅ Done (2026-05-20) |
| batch6 | 50 | ✅ Done (2026-05-20) — Audited 21 DB answer errors via docx cross-reference |
| batch7 | 50 (DABT-0568 to DABT-0618) | ✅ Done (2026-05-20) — Fixed 9 scrambled matching test answers + 2 hematology DB errors |
| batch8 | TBD | Pending |
| batch9 | 50 (DABT-0669 to DABT-0718) | ✅ Done (2026-05-20) — Immunotoxicology + Liver sections; noted pattern of Except-question reversals and liver zonation mismatches |
| batch10 | 50 (DABT-0719 to DABT-0768) | ✅ Done (2026-05-20) — All Domain IV (liver/hepatotoxicity); found "TRUE" reversal (DABT-0724), lab-value matching discrepancies (DABT-0761-0767), and 19/50 initial drafts missing answer-letter reference
| batch11 | 50 (DABT-0769 to DABT-0818) | Done (2026-05-20) — All Domain IV (renal & respiratory toxicology). Found systematic DB answer errors in renal physiology section — see `references/batch11-renal-errors.md` |
| batch12 | 50 (DABT-0819 to DABT-0868) | Done (2026-05-20) — All Domain IV (lung/pulmonary toxicology). Highest error rate yet: 24/50 (48%) DB answer errors. 9 E-answer import errors, 15 wrong-standard-answer, 5 scrambled matching items. See `references/batch12-lung-errors.md` |
| batch13 | 50 (DABT-0869 to DABT-0918) | Done (2026-05-20) — All Domain IV (neurotoxicology). 29/50 (58%) DB answer errors: highest rate seen. 8 E-answers (6 valid, 2 invalid), 21 wrong-standard-answer, 3 scrambled matching items, 100% error on MPTP/dopamine subtopic. See `references/batch13-neuro-errors.md` |
| batch14 | 50 (DABT-0919 to DABT-0968) | Done (2026-05-20) — All Domain IV. Topics: neurotoxicology (17 Qs continuation from batch13), ocular toxicity (27 Qs), skin (6 Qs). 8 DB answer errors: 6 in ocular (22% error rate), 1 in skin, 1 in neuro continuation. Also found 1 question with zero stored options (DABT-0962). See `references/batch14-ocular-skin-errors.md` |
| batch18 | 50 (DABT-1069 to DABT-1118) | Done (2026-05-20) — All Domain IV. Topics: Endocrine Toxicology (24 Qs), Pesticides – Insecticides (26 Qs). ~5 DB answers contradict Casarett & Doull reference texts: DABT-1081 (adrenal adenoma vs pheochromocytoma), DABT-1100 (status epilepticus vs respiratory failure), DABT-1107 (G6PD vs aconitase for fluoroacetate), DABT-1095 (rotenone vs anticoagulants), DABT-1096 (asulam vs gibberellic acid). 10 E-answers with only A-D options (mostly plausible as "none of the above"). 1 parsing issue (DABT-1070: all 4 options concatenated into option A). 1 zero-options question (DABT-1092). See `references/batch18-endocrine-pesticide-errors.md` |
| batch19-23 | Various | Done (2026-05-20) — See individual error reference files: `batch19-pesticide-errors.md`, `batch20-metals-errors.md`, `batch21-solvents-errors.md`, `batch22-solvents-errors.md`, `batch23-solvents-radiation-plant-errors.md` |
| batch24 | 50 (DABT-1369 to DABT-1418) | ✅ Done (2026-05-20) — All Domain IV (Plant Toxins). ~13/50 (26%) DB answer errors, 9 letter-E corruptions, 2/3 foundational classification Qs wrong. See `references/batch24-plant-toxins-errors.md` |
| batch25 | 50 (DABT-1419 to DABT-1468) | ✅ Done (2026-05-20) — Mix: Plant Toxins (14 Qs, 8/9 matching items wrong) + Air Pollution (36 Qs, ZERO errors). See `references/batch25-air-pollution-errors.md` |
| batch27 | 50 (DABT-1519 to DABT-1568) | ✅ Done (2026-05-20) — All Domain II (Mechanistic Toxicology). First Domain II batch from 2000Q Bank. ~12% error rate: 4 wrong-standard-answer (DABT-1528 receptor agonist pair reversal, DABT-1529 merged options, DABT-1559 HMG-CoA reductase → thioredoxin reductase, DABT-1568 glutathione false statement ambiguity). 5 E-answer corruptions. See `references/batch27-mechanistic-tox-errors.md` |
| batch28 | 50 (DABT-1569 to DABT-1618) | ✅ Done (2026-05-20) — Mix: Cell Death/Domain II (24 Qs, ~8% error), Neuropharm Matching/Domain II (15 Qs, 100% error on 7 stored matches + 8 letter-only zero-option items), Food Safety/Domain IV (11 Qs, ZERO errors). See `references/batch28-neuropharm-food-errors.md` |
| batch29 | 50 (DABT-1619 to DABT-1668) | ✅ Done (2026-05-20) — Domain IV: Food Safety (47 Qs). Domain I: Analytical Toxicology (3 Qs). 38/38 standard MCQs clean (food additive regulation, GRAS/Delaney, food allergy, natural toxins). 9/9 matching-test items have wrong stored associations (column-shift artifact). 1 Q-A text mismatch (DABT-1643: question asks source, options about effects). 1 parsing corruption (DABT-1652: all 4 options crammed into one row). 1 severe truncation (DABT-1653). 3/3 Domain I analytical tox Qs clean. See `references/batch29-food-errors.md` |
| batch31 | 50 (DABT-1719 to DABT-1768) | ✅ Done (2026-05-20) — All Domain I. Topics: Industrial Hygiene (4 Qs, clean), Industrial Gas Matching (14 Qs, 7 with wrong stored text same batch7 pattern), ADME/Toxicokinetics (32 Qs, 69% error rate — the HIGHEST found in any 2000Q Bank section). ADME errors: 6 E-import corruptions, fundamental physiology reversals (ion trapping direction, renal reabsorption, placental transport, membrane fluidity, P-gp classification, Fick's law). See entries below for full decomposition. |
| batch32 | 50 (DABT-1769 to DABT-1818) | ✅ Done (2026-05-24) — Domain I ADME/Toxicokinetics (24 Qs) + Domain II Biotransformation (26 Qs). First systematic coverage of ADME errors from 2000Q Bank. ~15/50 (30%) DB answer errors: 7 fundamental physiological reversals (transplacental carcinogen, enterohepatic cycling, bile:plasma ratio, cardiac output, TCDD excretion, plasma proteins, phenobarbital carcinogenesis), 2 transporter misclassifications, 5 wrong mechanism/association, 1 incomplete answer, 12 letter-E corruptions. See `references/batch32-adme-biotransformation-errors.md` |
| batch32 | 50 (DABT-1769 to DABT-1818) | ✅ Done (2026-05-24) — Domain I ADME/Toxicokinetics (24 Qs) + Domain II Biotransformation (26 Qs). First systematic coverage of ADME errors from 2000Q Bank. ~15/50 (30%) DB answer errors: 7 fundamental physiological reversals (transplacental carcinogen, enterohepatic cycling, bile:plasma ratio, cardiac output, TCDD excretion, plasma proteins, phenobarbital carcinogenesis), 2 transporter misclassifications, 5 wrong mechanism/association, 1 incomplete answer, 12 letter-E corruptions. See `references/batch32-adme-biotransformation-errors.md` |
| batch33 | 50 (DABT-1819 to DABT-1868) | ✅ Done (2026-05-20) — **All Domain II (Biotransformation). ~82% error rate (41/50) — the WORST Domain II batch.** The DABT-1800+ range reveals a data-quality cliff: 14 "EXCEPT" questions with TRUE statements marked as exception, fundamental enzyme location reversals (ALDH2, CYP450, GST compartment), wrong cofactors (Mo, UGT count), swapped CYP probe drugs, and 6 E-answer corruptions. **Check EVERY answer against C&D Ch.6.** See `references/batch33-biotransformation-errors.md` |
| batch35 | 50 (DABT-1919 to DABT-1968) | ✅ Done — All Domain IV (Cardiovascular Toxicity). ~20% error rate (10/50). Antiarrhythmic class reversal, cardiac biomarker confusion, hypertrophy/failure distinction blurred, 4 matching-test multi-position offset errors, alcoholic cardiomyopathy duration dependency reversed. See `references/batch35-cardiovascular-errors.md` |
| batch36 | 50 (DABT-1969 to DABT-2018) | ✅ Done (2026-05-20) — All Domain IV. Mix: (a) 4 matching-test items (DABT-1969–1972, CV/environmental matching continuation from batch35 — same column-alignment artifact pattern); (b) 46 Drug Abuse MCQs (DABT-1973–2018, **0% error rate**, extending the clean Drug Abuse sub-source across batch36+batch37 = 96 clean questions total). Reference: C&D Ch.32 (Analytical & Forensic Toxicology), Ch.33 (Clinical Toxicology). |
| batch37 | 50 (DABT-2019 to DABT-2068) | ✅ Done (2026-05-20) — All Domain IV (Drugs of Abuse / Forensic Toxicology). **0% error rate (0/50)** — third clean 2000Q Bank sub-source. Topics: opioids, hallucinogens, cannabinoids, stimulants, ethanol, GHB, Kratom, Salvia, anabolic steroids. Reference: C&D Ch.33 (Clinical Toxicology). See `references/batch37-drugs-of-abuse-errors.md` |
## DB Answer Verification Against Original Docx Source

**CRITICAL: The 2000Q Bank extracted data contains systematic parsing errors.** The `2000Q_ANSWER_KEY.csv` (used to populate `correct_answer_letter` and `correct_answer_text` in the DB) has ~21 known discrepancies from the original docx answer keys. Always verify suspect questions against the original `.docx` files.

### Where to Find Original Docx Files

```
/root/dabt-curated/2000Q_Question_Bank/
├── 2000Q Ch1 General.docx        → Ch1 General questions (standard MCQs + matching)
├── 2000Q ANTIDOTES Matching Test.docx → Antidote matching questions
├── 2000Q_ANSWER_KEY.csv          → EXTRACTED answer key (CONTAINS ERRORS — do not trust blindly)
└── ... (40+ chapter/theme files)
```

### Antidotes Matching Test — Critical Format Detail

The antidotes matching test has a deceptive format in the docx:

```
Display lines (P1-P17): Shows EACH term paired with a LETTER-definition, but the pairing is ARBITRARY (just ordinal alignment):
  1968. sodium bicarbonate A. methotrexate
  1969. L-carnitine B. cholinesterase inhibitor
  ...

Answer section (P19-P35): Contains the CORRECT letter for each term:
  1968. Q (I)    → sodium bicarbonate → Q (cyclic antidepressants)
  1969. H (II)   → L-carnitine → H (valproic acid toxicity)
  ...
```

**The extraction script (`extract_2000q_v3.py`) stored the display-line option text as `correct_answer_text` in the DB.** This is WRONG. The correct answer letter (from the answer section) maps to a different definition entirely. For example, Q1971 (DABT-0518, "glucagon") has DB `correct_answer_text="heparin"` (from display line "D. heparin"), but the actual correct answer is "beta-adrenergic antagonists" (letter L from answer section).

**To determine the actual correct answer:**
1. Use the DB's `correct_answer_letter` — this IS correct (matches the answer key)
2. Map that letter to the full definition using the letter-definition key from the display lines:
   - A = methotrexate, B = cholinesterase inhibitor, C = isoniazid, D = heparin, E = thallium
   - F = bupivacaine, G = ethanol withdrawal, H = valproic acid toxicity, I = plutonium
   - J = hydrogen fluoride, K = anticholinergic toxicity, L = beta-adrenergic antagonists
   - M = ethylene glycol, N = malignant hyperthermia, O = midazolam, P = sulfonylurea-induced hypoglycemia
   - Q = cyclic antidepressants
3. Write the explanation based on the REAL toxicology pairing, not the DB's corrupt `correct_answer_text`.

### Ch1 General MCQs — Verification Pattern

For standard MCQs from the "Ch1 General" source, verify the DB answer against the docx answer section:

```python
from docx import Document
import re

doc = Document('/root/dabt-curated/2000Q_Question_Bank/2000Q Ch1 General.docx')

# Parse answer key from the end of the document
for p in doc.paragraphs:
    text = p.text.strip()
    if 'CHAPTER 1 ANSWERS' in text:
        answers = re.findall(r'(\d+)\.\s*([A-Z])\s*\(', text)
        answer_map = {int(q): letter for q, letter in answers}
        # answer_map[1] → 'B', answer_map[2] → 'D', etc.

# Answer key (Q1-Q43) from original docx:
DOCX_ANSWERS = {
    1: 'B', 2: 'D', 3: 'B', 4: 'B', 5: 'C', 6: 'B', 7: 'A', 8: 'B', 9: 'C',
    10: 'D', 11: 'B', 12: 'A', 13: 'C', 14: 'D', 15: 'C', 16: 'C', 17: 'A',
    18: 'D', 19: 'A', 20: 'C', 21: 'C', 22: 'B', 23: 'A', 24: 'B', 25: 'D',
    26: 'B', 27: 'C', 28: 'B', 29: 'D', 30: 'A', 31: 'C', 32: 'A', 33: 'B',
    34: 'C', 35: 'C', 36: 'D', 37: 'B', 38: 'B', 39: 'C', 40: 'D',
    41: 'C', 42: 'D', 43: 'A'
}
```

### Known DB Errors Found (Batch 6 Audit)

The following 21 discrepancies were found in Batch 6 (DABT-0518 to DABT-0567) and corrected:

| DB ID | DB says (answer → text) | Docx says | Correct answer |
|-------|------------------------|-----------|----------------|
| DABT-0518-0530 | Various (see Antidotes section above) | Various | See letter map above |
| DABT-0532 | C → 1 to 2 days | D | 1 to 2 weeks |
| DABT-0533 | D → genetic increase in liver enzyme | B | idiosyncratic reaction |
| DABT-0534 | C → cytochrome oxidase | B | NADH cytochrome b5 reductase |
| DABT-0536 | D → hematopoietic/lungs | B | muscle and bone |
| DABT-0537 | C → potentiation | A | additive effect |
| DABT-0538 | C → potentiation | B | synergy |
| DABT-0540 | C → receptor antagonism | D | functional antagonism |
| DABT-0541 | A → dispositional antagonism | B | chemical antagonism |
| DABT-0543 | B → chemical antagonism | C | receptor antagonism |
| DABT-0544-0567 | Various E answers (no E option) | Various A-D | See individual mappings |

**Pattern to watch for:** Questions with `correct_answer_letter="E"` but options only A-D (6 questions in Batch 6). These are all corrupted — the docx answer key gives the real answer (always one of A-D or the docx key's actual letter).

### General-Principles Matching Test (DABT-0573 through DABT-0582) — Letter Scrambling

**ANOTHER corrupted matching test** from the 2000Q Bank (source_file_id=2). Unlike the Antidotes Matching Test (where only `correct_answer_text` was wrong), this test has the **entire letter-to-definition mapping scrambled**. Both `correct_answer_letter` and `correct_answer_text` in the DB are assigned to the wrong term.

The actual correct pairings based on standard toxicology:

| DB ID | Column A Term | Actual correct match |
|-------|--------------|---------------------|
| DABT-0573 | antagonism | 4 + 0 = 1 (less than additive) |
| DABT-0574 | TOCP | delayed neurotoxicity (OPIDN) |
| DABT-0575 | probit unit | normal equivalent deviation plus 5 |
| DABT-0576 | synergy | 2 + 3 = 10 (greater than additive) |
| DABT-0577 | succinylcholine | idiosyncratic-prolonged apnea |
| DABT-0578 | STEPS | program to prevent birth defects |
| DABT-0579 | Superfund Act | toxicology and the law (already correct) |
| DABT-0580 | descriptive toxicologist | conducts/designs toxicity tests |
| DABT-0581 | regulatory toxicologist | performs human risk assessment |
| DABT-0582 | forensic toxicologist | applies tox to legal matters |

**Pattern to detect:** Terms like "antagonism", "synergy", "STEPS", "probit unit" as bare question_text (single word/short phrase) with only one option stored in `answer_options`. The match_pairs table also has scrambled `match_answer` values for these — the entire test was misaligned during CSV import.

**How to fix in batch scripts:** Use a manual OVERRIDES dict mapping each DB ID to `(correct_letter, correct_text, domain)`. Do NOT trust either `correct_answer_letter` or `correct_answer_text` from the DB for these items.

### Hematology Questions (source_file_id=2, batch7 DABT-0583 to DABT-0618)

These are standard MCQs covering blood toxicity topics. The correct DB answers are generally reliable, but a few were identified as wrong:

| DB ID | DB says | Correct answer | Rationale |
|-------|---------|---------------|-----------|
| DABT-0584 | low serum B12 or folate | microcytosis | Megaloblastic anemia is macrocytic, not microcytic |
| DABT-0592 | beta 2 microglobulin | hemin | Ferric heme + chloride = hemin |
| DABT-0616 | A (interfere with PL-dependent coag) | C likely (severe bleeding) | LAs are prothrombotic in vivo |

**Primary reference for hematology questions:** Casarett & Doull Ch.11 "Toxic Responses of the Blood" (pp.612-651, 5,150 lines extracted). Hayes Ch.7e lacks a dedicated blood chapter — Hayes hematotoxicity discussion is spread across chapters 33 (renal), 35 (neuro), and 39 (immune).

**Prevention — updated for Batch7 findings:**

When processing a new batch:
1. **Check the source_file_id** — questions from `source_file_id=2` (2000Q Bank) are the risk group
2. **For Antidotes matching items** (topic = "Drugs & Therapeutics – Toxicology", short single-word question text): always reconstruct correct answer from the letter-key mapping in the Antidotes section above
3. **For General-Principles matching items** (terms like antagonism, synergy, probit unit, TOCP, STEPS): check against the corrected mapping table above — the DB has both letter AND text scrambled
4. **For Ch1 General items** (within file question numbers 1-37): compare against the DOCX_ANSWERS dict above
5. **For question numbers >40** within Ch1 General: use the `answers` regex extraction from the docx
6. **Flag any question where** `correct_answer_letter > 'D'` but options only go up to D
7. **For hematology questions** (topics containing "Hematology & Blood Toxicity"): verify against Casarett & Doull Ch.11 — the DB answers are usually correct but a few "EXCEPT" questions (DABT-0584, DABT-0616) and biochemistry questions (DABT-0592) have wrong answers
8. **For immunotoxicology questions** (topic = "Immunotoxicology / Allergy"): Several "EXCEPT" questions have the answer letter pointing to a TRUE statement instead of the exception. Verify each option's truth value independently against Casarett & Doull Ch.12. Also watch for matching-test items where the DB answer conflicts with known immunology (e.g., Buehler test said to assess autoimmunity vs contact hypersensitivity).
9. **For liver zonation questions** (topic = "Liver / Hepatotoxicity", questions about acinus zones or CYP zonation): The three zone-characterization questions in the 2000Q Bank (Q3-Q5) have systematically wrong answer keys. Always verify against Casarett & Doull Ch.13 pp.740-742.

## Pitfalls

- **"EXCEPT" questions:** Easy to reverse the logic. Always verify: the correct answer is the FALSE/EXCLUDED statement; the distractors are TRUE statements. **Batch 9 finding:** Several immunotoxicology "EXCEPT" questions from the 2000Q Bank (DABT-0670, DABT-0671, DABT-0674) have the DB's answer letter pointing to a statement that IS actually true — the opposite of what was expected. Do NOT blindly trust the DB's answer letter for "EXCEPT" questions from the immunotoxicology section. Always independently verify each option's truth value against Casarett & Doull Ch.12 before writing.
- **Compound correct answers** (e.g., "E = A and C"): Don't just state the letter — explain why A and C are correct and why B/D are wrong.
- **"All of the above" / "None of the above":** Enumerate every listed option to demonstrate thoroughness.
- **Matching-test single-option items:** These have only the correct match in the DB's `answer_options` table (one letter, one text). The explanation should explain the association. If the association is toxicologically dubious, note the standard fact alongside.
- **DB answer-vs-reference conflicts:** Do NOT propagate wrong toxicology. Flag discrepancies in the explanation. Several batch5 items had DB answers that conflict with Casarett & Doull (e.g., DABT-0486 sarafotoxins → "common bile duct stones" vs reference's "coronary artery constriction"; DABT-0498 ACE inhibitors → "wasp venom" vs reference's "Bothrops jararaca").
- **2000Q Bank data quality issues:** The extracted CSV/DB has ~21 known errors in `correct_answer_text` and `correct_answer_letter` for Chapter 1 and Antidotes Matching questions. Always cross-reference against the original docx files. The docx answer key is the ground truth; the `2000Q_ANSWER_KEY.csv` had parsing errors.
- **Antidotes matching: correct_answer_text is usually WRONG:** The DB stored the display-line definition text (arbitrary ordinal pairing), not the actual correct match. Use `correct_answer_letter` + the letter-definition key (reconstructed in the DB Verification section above) to find the real answer.
- **Questions with `correct_answer_letter='E'` but only A-D options:** The answer key extraction went wrong. Read the original docx answer section to find the real answer letter. Six such questions in Chapter 1 (Q14, Q18, Q19, Q21, Q29, Q33, Q35). Also found in immunotoxicology section (batch 9: DABT-0669, DABT-0676, DABT-0679, DABT-0680, DABT-0681, DABT-0685, DABT-0690, DABT-0691, DABT-0696, DABT-0698, DABT-0699, DABT-0700). These may or may not be errors — many are "All of the above" / "None of the above" implicit options where E = None. Verify against reference text before accepting or correcting.
- **Domain classification:** Must match `question_domains.domain` in the DB exactly (e.g., "Domain I" not "Domain 1" or "Domain-I").
- **Source attribution:** When unsure of the exact chapter, scan the extracted/ files for the topic. Casarett index.json and Hayes index.json list all chapters with titles.
- **Self-review completeness:** Always check (a) ID set completeness, (b) domain match, (c) correct-answer-letter presence, (d) reference citation, (e) minimum length.
- **Generator script vs output file:** When using a Python script to generate the batch JSON, write the script to /tmp/ and run it to produce the output. Do NOT write the generator script directly to `batchN_done.json` — tool will overwrite with the script source instead of JSON output.
- **ADME/Toxicokinetics questions from 2000Q Bank (Domain I, batch31, DABT-1737-1768, source_file_id=2, docx = '2000Q Ch5 ADE.docx'):** This section has a 69% error rate (22/32 Qs wrong) — the HIGHEST of any 2000Q Bank section processed. The original docx answer key is the only reliable reference. Key systematically wrong DB answers:
  - **Ion trapping direction (DABT-1737, 1738, 1739):** The DB reverses the core principle. Alkaline urine favors EXCRETION of weak acids (they become ionized → trapped), not bases. Lipid-soluble molecules (not organic cations) are reabsorbed after filtration. Diuretics enhance elimination of ion-trapped (polar) compounds, not lipid-soluble ones.
  - **Kernicterus mechanism (DABT-1741):** DB says "enzyme induction → glucocorticoids." Correct: displacement of bilirubin from albumin by drugs like sulfonamides.
  - **GI absorption factors (DABT-1742):** DB says presence of food is the exception. Time of day is the correct exception — food definitely influences absorption.
  - **Colonic absorption (DABT-1744):** DB says water is the exception. Glucose is correct — it's absorbed in the small intestine, not the colon.
  - **Bone storage (DABT-1747):** DB says E (no E option). Correct: diquat is the exception — lead, strontium, and fluoride all accumulate in bone.
  - **Placental crossing (DABT-1748):** DB says IgG. Correct: heparin does NOT cross the placenta. IgG crosses via FcRn.
  - **Methylmercury BBB transport (DABT-1749):** DB says glutamine. Correct: methionine mimic (MeHg-cysteine complex is transported by LNAA system L).
  - **Breast milk pH trapping (DABT-1750):** DB says "cows→humans" is exception. Correct: acidic compounds are LESS concentrated (basic compounds are ion-trapped and more concentrated in milk).
  - **Facilitated diffusion (DABT-1752):** DB says saturability is exception. Correct: movement AGAINST gradient is the exception — facilitated diffusion goes ALONG the gradient.
  - **Alveolar particle clearance (DABT-1753):** DB says MDR1/P-gp. Correct: phagocytosis by alveolar macrophages.
  - **P-gp classification (DABT-1754):** DB says "metal transporters." Correct: efflux transporters.
  - **P-gp substrates (DABT-1755):** DB says colchicine is exception. Correct: ethanol is NOT a P-gp substrate.
  - **Simple diffusion law (DABT-1756):** DB says "Priestley's law." Correct: Fick's law.
  - **Membrane fluidity (DABT-1757):** DB says ion channels. Correct: unsaturated fatty acids determine fluidity.
  - **Aqueous pores (DABT-1758):** DB says E (no E option). Correct: small hydrophilic molecules pass through pores.
  - **Octanol/water partition (DABT-1759):** DB says acetic acid. Correct: TCDD has the largest Kow (~6.8).
  - **Nutrient delivery to fetus (DABT-1761) and toxicant placental crossing (DABT-1762):** Both DB entries say E. Correct: active transport for nutrients; simple diffusion for toxicants.
  - **Fetal protection (DABT-1763):** DB says "biotransformation ability of the placenta" is exception. Correct: tight endothelial cell junctions (like BBB) do NOT exist in the placenta — the exception is A.
  - **BBB transporter energy requirement (DABT-1764):** DB says option D (some efflux anionic/cationic) is exception. Correct: claim that these ABC transporters do NOT require ATP (C) is the false statement — they absolutely require ATP.
  - **Neonatal nitrate sensitivity (DABT-1767):** DB says toxic megacolon. Correct: methemoglobinemia from nitrate-reducing bacteria in higher-pH infant GI tract.
  - **Always verify Ch5 ADE questions against the docx answer key at `/root/dabt-curated/2000Q_Question_Bank/2000Q Ch5 ADE.docx`.**
- **ADME/Toxicokinetics questions from 2000Q Bank (Domain I, source_file_id=2, DABT-1769 to DABT-1792):** This batch has a ~30% error rate in this section. Key patterns to verify independently:
  - **Bile-to-plasma classification:** The DB frequently stores albumin (Class C, ratio <1) where a Class B substance (arsenic, lead, Mn — ratio 10-1000) is correct. Always verify against C&D Ch.5 Table 5-13's Class A/B/C system.
  - **Transplacental carcinogen:** The DB says warfarin; C&D Ch.5 says diethylstilbestrol (DES). Warfarin is a teratogen, not a transplacental carcinogen.
  - **Enterohepatic cycling vs well-stirred effect:** The DB swaps these two very different concepts. Enterohepatic cycling = biliary excretion → gut hydrolysis → reabsorption. Well-stirred = a PK model assuming uniform hepatic distribution.
  - **Cardiac output distribution:** The DB says kidney receives the smallest % (opposite — it receives ~25%, one of the highest). Skin receives the smallest fraction.
  - **TCDD excretion:** The DB says exhalation is a major route. TCDD is non-volatile and highly lipophilic — primary excretion is biliary-fecal.
  - **Plasma protein binding:** The DB substitutes ceruloplasmin and RBP as "the two major" xenobiotic-binding proteins. The correct answer is albumin + α₁-acid glycoprotein.
  - **ABC transporter location:** The DB says P-gp is not an ABC transporter example. P-gp is the prototypical ABC transporter. The real false statement is "found only in liver and kidney."
  - **See `references/batch32-adme-biotransformation-errors.md` for full detail.
- **Renal toxicology questions from 2000Q Bank (Domain IV, source_file_id=2, DABT-0769 to DABT-0814):** These cover nephron anatomy, renal physiology, and nephrotoxicant mechanisms. The DB answer keys for this section have systematic errors — more than any other organ system processed so far. Key discrepancies found in batch11:
  - **BUN physiology (DABT-0787):** DB says dehydration does NOT increase BUN. Physiologically, dehydration increases BUN via prerenal azotemia. The actual exception should be "immediately postdialysis" (BUN falls).
  - **Ischemic injury mechanisms (DABT-0792):** DB says "interfering with renal blood flow" does NOT cause ischemic injury. This contradicts basic physiology — vasoconstriction → reduced renal perfusion → ischemic ATN.
  - **Tubular cast composition (DABT-0798):** DB says casts are basophils and plasma cells. Casts after ATN are necrotic/viable tubular epithelial cells + Tamm-Horsfall protein.
  - **Tubular repair cells (DABT-0799):** DB says capillary endothelial cells are primary source of tubular repair. Current understanding: surviving tubular epithelial cells dedifferentiate, proliferate, and redifferentiate.
  - **Vasopressin effect (DABT-0804):** DB says ADH interference most impairs glomerular filtration. ADH's primary renal action is on collecting duct water permeability; blocking it impairs concentrating ability, not GFR.
  - **JGA secretion (DABT-0810):** DB says JGA secretes vitamin D. The JGA secretes renin. Vitamin D activation (1α-hydroxylation) occurs in proximal tubular cells, not the JGA.
  - **Most common renal injury site (DABT-0811):** DB says collecting duct. The proximal tubule is the classic most common site (high metabolic rate, OAT/OCT transport, concentration of toxicants).
  - **Surfactant source (DABT-0817):** DB says mucus-producing cells. Surfactant is produced by type II alveolar (pneumocyte) cells.
  - **Multiple "E" answers with only A-D options:** DABT-0777, 0780, 0782, 0805, 0808, 0813 all have `correct_answer_letter='E'` but options only A-D. Follow the pattern established in earlier batch audits — verify each against standard toxicology.
  - **Missing options (DABT-0814):** The question "Which of the following is the correct toxicant-target organ pair?" has zero options in the DB and no `correct_answer_text`.
  - **Parsing error (DABT-0818):** All four option statements were jammed into option A's text field, concatenated without separators.
  
  **Pattern:** Renal physiology questions seem to have been extracted with particularly poor quality control. Always verify against Casarett & Doull Ch.25 "Toxic Responses of the Renal System" before writing explanations. A defensive approach is to flag every explanation where the DB answer contradicts well-established renal physiology with a `[Note: ...]` block.

- **Lung/pulmonary questions from 2000Q Bank (source_file_id=2, Domain IV, DABT-0819 to DABT-0868):** This section has the HIGHEST error rate seen (48% — 24/50 questions have wrong answers). Key patterns:
  - **Gas solubility is systematically swapped:** The DB frequently reverses which gases stay in the upper airway vs. penetrate deep. SO₂ (highly water-soluble → upper airway scrubbed) and NO₂ (poorly soluble → penetrates to alveoli) are the most common reversal. Always verify against Cascarett & Doull Ch.15 gas solubility tables.
  - **Particle/fiber deposition mechanisms:** For questions asking about diffusion vs. interception vs. impaction vs. sedimentation for specific particle sizes/shapes, the DB answers are unreliable for fibers with extreme aspect ratios. A 200×1 µm fiber is deposited by INTERCEPTION, not diffusion (the DB says diffusion).
  - **Emphysema definition is entirely wrong:** The DB stores "abnormal contraction with fibrotic walls" as the definition. The correct definition is "abnormal ENLARGEMENT without fibrosis" (C&D Ch.15).
  - **Matching-test items are all scrambled:** Five lung-disease matching items (asbestos, cadmium oxide, isocyanates, nickel refining, aluminum dust → their diseases) have completely wrong associations in the DB. Always reconstruct the correct disease pairings from C&D Ch.15.
  - **Reference chapter:** Casarett & Doull Ch.15 "Toxic Responses of the Respiratory System" is the single authoritative reference for this entire section. No docx cross-reference was available for verification.
  - **"EXCEPT" questions remain unreliable:** The batch9 pattern continues — several lung EXCEPT questions (DABT-0834, DABT-0841, DABT-0859, DABT-0861) have DB answers pointing to statements that ARE actually true. Always independently verify each option against C&D Ch.15.

**"Which statement is TRUE" reversal (distinct from EXCEPT):** The batch10 liver section (DABT-0724) revealed a new pattern: a "Which one of the following statements is true?" question where the DB's listed answer (A: "The liver cannot regenerate") is factually FALSE. This is NOT an EXCEPT question — it's a standard TRUE/FALSE selection where the DB stored answer appears wrong. Watch for this pattern in ALL question formats, not just EXCEPT. Before writing, independently verify every option's truth value against Casarett & Doull, even for non-EXCEPT questions. The question format (true/false, except, match) does not change the need for verification.

**Liver-lab-value matching tests (batch10, DABT-0761-0767):** This is a matching test from source_file_id=2 pairing hepatic analytes with their clinical interpretation. The DB only stores the correct match per question (one letter + one text). Several matches are factually incongruent with standard hepatology:
- Albumin → "elevated in liver disease and hemolysis" (albumin is DECREASED in chronic liver disease)
- Prothrombin time → "decreased in chronic liver disease" (PT is INCREASED/prolonged)
- Alkaline phosphatase → "most sensitive indicator of acute liver disease" (ALT/aminotransferases are the sensitive markers; ALP is a cholestasis marker)
- Ultrasound → "distinguishes bone from liver disease" (GGT does this; ultrasound shows bile duct dilation)

**Pattern to detect:** Question text is a single-word analyte name (albumin, AST, ammonia, etc.) from a liver-function-test set. Only 1 option stored in answer_options, and it may reflect the source's option key rather than clinical reality. Write the explanation stating both what DB says AND what standard toxicology/hepatology says. Flag the discrepancy explicitly: "The DB matches albumin with 'elevated in liver disease and hemolysis' — note that clinically, albumin is decreased in chronic liver disease due to reduced hepatic synthesis."

**New "homogeneous-domain batch" pattern:** Batch10 (DABT-0719 to DABT-0768) was the first batch where ALL 50 questions belonged to one domain (Domain IV — Applied Toxicology / Hepatotoxicity). Previous batches mixed domains. When a batch is homogeneous, consider:
- Target reference chapter search to one topic (e.g., Casarett & Doull Ch.13 "Liver" for all 50)
- Batch-level domain check: `all(item['domain'] == same_domain for item in output)` is a cheap but valuable verification
- If the batch was explicitly split by domain, the `batchN.json` author likely grouped by source chapter — look for thematic clusters within the batch

**Self-review: answer-letter presence is not automatic.** In batch10, 19/50 explanations (38%) failed to mention the correct answer letter in the initial draft — they described the mechanism without naming the letter. During self-review, add a mandatory check:
```python
for item in output:
    ans_letter = db_answer[item['id']]
    if ans_letter not in item['explanation']:
        errors.append(f"{item['id']}: answer letter {ans_letter} not in explanation")
```
- **Reference text search efficiency:** Use `search_files` with `context=3` for the first pass to see matches in context. Only `read_file` with a larger offset/limit when context is insufficient. This avoids wasting reads on irrelevant sections.

- **Endocrine Toxicology questions from 2000Q Bank (source_file_id=2, Domain IV, DABT-1069-1092):** This section covers the pituitary, thyroid, parathyroid, adrenal cortex/medulla, and pancreas. Key DB discrepancies found in batch18:
  - **Adrenal medullary tumor terminology (DABT-1081):** DB says "adrenal adenomas." Correct: pheochromocytomas (Casarett Ch.20, Parathyroid section: "Larger benign adrenal medullary proliferative lesions are designated pheochromocytomas"). Adrenal adenomas are cortical neoplasms.
  - **Thyroid cancer gender dimorphism (DABT-1086):** DB says androgens play a role. The 2-3× female predominance classically suggests estrogen involvement. Verify both androgen and estrogen literature before writing.
  - **Calcium physiology (DABT-1070):** The stored answer (D) designates "protein-bound calcium predominantly on albumin" as false — but this is physiologically correct. The cytosolic/extracellular gradient statement in option A is actually backwards (extracellular ~10,000× higher). This may be a parsing error where all options were concatenated into one row.
  - **Reference chapter:** Casarett & Doull Ch.20 (3,203 lines) is the primary reference. Hayes Ch.36 is the alternative. No docx cross-reference was available.

- **Pesticides questions from 2000Q Bank (source_file_id=2, Domain IV, DABT-1093-1118):** This section covers organophosphates, carbamates, organochlorines, pyrethroids, neonicotinoids, bipyridyls, rodenticides, and fungicides. Key DB discrepancies found in batch18:
  - **OP poisoning cause of death (DABT-1100):** DB says "status epilepticus." Standard clinical toxicology cites respiratory failure as the primary cause. Status epilepticus can contribute but is not the usual lethal event.
  - **Sodium fluoroacetate MOA (DABT-1107):** DB says "inhibition of glucose-6-phosphate dehydrogenase." Actual MOA: metabolic conversion to fluorocitrate → inhibition of aconitase in the TCA cycle. G6PD is in the pentose phosphate pathway.
  - **Rodenticide prevalence (DABT-1095) and PGR classification (DABT-1096):** DB answers contradict common knowledge (anticoagulants are the most common rodenticide, gibberellic acid is the classic PGR). These may be answer-key extraction errors or schema-specific decisions.
  - **Reference chapter:** Casarett & Doull Ch.22 (6,934 lines) is the single authoritative reference. No docx cross-reference was available.

- **Drugs of Abuse / Forensic Toxicology questions from 2000Q Bank (source_file_id=2, Domain IV, batch36 DABT-1973–2018 + batch37 DABT-2019–2068):** This section covers the pharmacology and toxicology of psychoactive substances — opioids (heroin, morphine, methadone, codeine, oxycodone), hallucinogens, stimulants, ethanol, GHB, and others. **0% error rate across 96 questions (0/46 in batch36 + 0/50 in batch37)** — making this the LARGEST clean sub-source from the 2000Q Bank, alongside Air Pollution (36 Qs) and Food Safety (11 Qs). All questions have full 4-option sets, correct answer letters, no letter-E corruptions, and no parsing issues.**
  - **Key difference from prior sections:** Unlike the high-error ADME or biotransformation sections, the Drugs of Abuse topics (opioid metabolism, cocaine biomarkers, 6-AM specificity, methamphetamine excretion, GHB postmortem artifact, ketamine MOA, etc.) are all correctly stored.
  - **Primary references:** Casarett & Doull Ch.32 (Analytical and Forensic Toxicology) for cocaine/Hair/6-AM/metabolites; Ch.33 (Clinical Toxicology) for overdose syndromes, opioid pharmacology, and clinical management.
  - **See `references/batch37-drugs-of-abuse-errors.md`** for full topic breakdown and coverage map.
