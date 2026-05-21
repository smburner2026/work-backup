# Batch 20 — Metals & Metalloids Domain IV Error Audit

**Batch file:** `/root/work/dabt/dabt-tutor/batches/batch20.json`  
**Questions:** DABT-1169 to DABT-1218 (50 questions)  
**Topic:** Metals & Metalloids (48 Qs) + Pesticides – Insecticides (2 Qs)  
**Source bank:** 2000Q Bank (source_file_id=2, except where noted)  
**Reference texts:** Casarett & Doull Ch.23 (Metals), Ch.22 (Pesticides); Hayes Ch.19 (Metals), Ch.18 (Crop Protection)  
**Explanation output:** `/root/work/dabt/dabt-tutor/batches/batch20_done.json`

## Summary

| Metric | Count |
|--------|-------|
| Total questions | 50 |
| Source discrepancies (DB answer ≠ standard toxicology) | ~10 (20%) |
| Questions with answer E but only A–D options | 7 |
| Zero-option questions (no answer_options rows) | 2 (DABT-1169, 1170) |

## Detailed Discrepancies

### Wrong Standard Answer (DB says X, textbook says Y)

| QID | DB Answer | Textbook-Correct Answer | Issue |
|-----|-----------|------------------------|-------|
| DABT-1186 | A — liver and kidney | C — teeth and bones | Fluorosis: Casarett & Doull Ch.23 describes **dental fluorosis** (white mottling, pitting of enamel) and **skeletal fluorosis** (osteosclerosis, ligament calcification) — NOT liver and kidney. |
| DABT-1187 | A — arsenic | mercury | Acrodynia (pink disease) in children: Casarett & Doull Ch.23 line 2826 explicitly says acrodynia is caused by **inorganic mercury** from calomel in teething powders, not arsenic. DB answer contradicts the same reference chapter. |
| DABT-1188 | A — through volcanic emissions | D — all of the above | Mercury is deposited through volcanic emissions, industrial emissions, AND rainwater. DB picks a single narrow source when the comprehensive answer is correct. |
| DABT-1190 | C — germanium | D — cesium (or A — silver/argyria) | Skin/eye pigmentation from prolonged exposure: silver causes **argyria** (irreversible blue-gray skin pigmentation). Germanium is associated with renal toxicity, not pigmentation. |
| DABT-1191 | B — peripheral neuropathy | C — cardiomyopathy | Selenium deficiency: classic manifestation is **Keshan disease** (cardiomyopathy), named after the region in China with endemic Se-deficient soil. Peripheral neuropathy is not a recognized manifestation. |
| DABT-1194 | C — selenium–dandruff shampoos | Incorrect pair is actually correct | Selenium sulfide IS used in dandruff shampoos (Selsun Blue). The DB labels this as an incorrect pair when it's actually a correct commercial use. |
| DABT-1195 | E — none of the above | D — strontium | Strontium substitutes for calcium in bone (similar ionic radius, incorporates into hydroxyapatite). The DB says none of A–D work, but D (strontium) is textbook-correct. |
| DABT-1196 | B — bromine | C — boron | Boron is a true metalloid (one of Si, Ge, As, Sb, Te, Po). Bromine is a halogen, not a metalloid. |
| DABT-1202 | C — organic tin compounds can be very neurotoxic | D — inorganic compounds are better absorbed than organic | The DB lists C (a true statement) as the "except" answer, but the actually false statement is D (organic tin compounds are better absorbed than inorganic, not the reverse). |
| DABT-1204 | C — it is essential for human growth and development | (B — overdose > deficiency, but both are problematic) | Zinc IS essential for growth and development — this is a true statement, so it should not be the "except" answer. The intended exception is likely B (overdose vs deficiency: globally Zn deficiency is a major problem). |
| DABT-1206 | C — H. pylori gastritis | D — inflammatory bowel disease | Bismuth is used for H. pylori gastritis (standard quadruple therapy) — this is correct, not an exception. IBD is not a standard indication for bismuth. |
| DABT-1215 | C — serum unbound copper levels are elevated | B — serum ceruloplasmin is elevated | In Wilson's disease, serum CERULOPLASMIN is LOW (not elevated). The DB identifies C as the exception, but the actually false statement is B. |
| DABT-1216 | D — none of the above | B is factually correct | Menkes' disease IS characterized by copper deficiency in the brain (B is true). The DB says "none of the above" is correct, but option B is a true statement about Menkes' disease. |
| DABT-1217 | E — none of the above | B is the false statement | The major presentation of iron deficiency in young children is microcytic anemia, NOT seizure disorder (B). The DB says all A–D are true, but B is factually false. |
| DABT-1218 | E — none of the above | D — nausea, abdominal pain, metabolic acidosis | Acute iron overdose classic symptoms are GI distress (nausea/vomiting, abdominal pain) followed by metabolic acidosis and multisystem organ failure — option D. The DB says none of A–D are correct, but D is the textbook-correct answer. |

### Structural Patterns

#### Letter E with Only A–D Options

7 questions have correct_answer_letter = "E" but only 4 answer options (A–D). These function as "none of the above" answers. In most cases this is plausible (all listed statements are true/false), but in several instances it conflicts with standard toxicology:

| QID | A–D Options | Plausible E? | Notes |
|-----|-------------|--------------|-------|
| DABT-1171 | 4 statements about metal properties | ✅ Yes — all 4 are false | Valid "none of the above" |
| DABT-1180 | 4 alcohol–metal interaction mechanisms | ✅ Yes — all 4 are valid | Valid "none of the above" |
| DABT-1193 | 4 Hg exposure statements | ✅ Yes — all 4 are true | Valid "none of the above" |
| DABT-1195 | 4 metals as Ca substitutes | ⚠️ No — strontium IS correct | Should be D, not E |
| DABT-1208 | 4 Li toxicity manifestations | ✅ Yes — all 4 are true | Valid "none of the above" |
| DABT-1217 | 4 Fe deficiency statements | ⚠️ No — B is false | Should identify B as exception |
| DABT-1218 | 4 Fe overdose symptoms | ⚠️ No — D is correct | Should be D, not E |

#### Zero-Option Questions

DABT-1169 ("chlorothalonil") and DABT-1170 ("norbormide") have:
- `question_text` = single word (the chemical name)
- `correct_answer_letter` = C (both)
- **Zero rows** in `answer_options` table
- Topic = "Pesticides – Insecticides"

**Resolution:** Verified against Casarett & Doull Ch.22 that chlorothalonil is a fungicide and norbormide is a rodenticide — neither is an insecticide. The questions are likely classification items asking which listed compound is NOT an insecticide, with C being the correct exception.

**Detection query:**
```sql
SELECT q.id, q.question_text, q.correct_answer_letter, COUNT(a.id) as opt_count
FROM questions q
LEFT JOIN answer_options a ON q.id = a.question_id
WHERE q.source_file_id = 2
GROUP BY q.id
HAVING opt_count = 0;
```

### Two Pesticide Questions at Start of Batch

DABT-1169 and DABT-1170 belong to "Pesticides – Insecticides" topic while the remaining 48 are "Metals & Metalloids." When writing explanations for mixed-topic batches, look up the correct reference chapter (Casarett Ch.22 for pesticides, Ch.23 for metals) and don't assume the entire batch is a single topic.
