# Question Classification Methodology

## Source

4,841 questions from the SQLite database (`dabt.db`, 7 source banks). 

> **NOTE:** This document covers the DOMAIN classification (topic-to-domain mapping)
> used during the initial DB build. For the BLOOM LEVEL classification (cognitive
> demand: Remember/Apply/Analyze), see `references/bloom-classification-methodology.md`
> — that was done in a separate pass on the full 4,841-question database on 2026-05-20.

Legacy xlsx (446 Qs) available for backward compat.

## Classification Pipeline

### Step 1: Topic-to-Domain Mapping

A deterministic lookup table maps each `Topic (Primary)` value to a Handbook domain, sub-domain, and task. Confidence levels:

- **high**: topic uniquely maps to one domain (e.g., "Carcinogenesis & Mutagenesis" → Domain II)
- **medium**: reasonable but could cross domains (e.g., "General Toxicology" → Domain I.C)
- **low**: override applied; needs review

#### Full Mapping Table

| Topic (Primary) | Domain | Sub-Domain | Task | Confidence |
|---|---|---|---|---|
| General Principles & Concepts | I | A.Design | T1 | high |
| General Toxicology | I | C.Interpret | T1 | medium |
| Toxicokinetics / ADME | I | B.Execute | T2 | medium |
| Biotransformation / Metabolism | I | C.Interpret | T4 | medium |
| Mechanisms of Toxicity | II | Mechanistic | T1 | high |
| Carcinogenesis & Mutagenesis | II | Mechanistic | T4 | high |
| Genotoxicity / DNA Damage | II | Mechanistic | T1 | high |
| Risk Assessment & Regulatory | III | D.RiskChar&Mgmt | T1 | medium |
| Metals & Metalloids | IV | Applied | T11 | medium |
| Solvents & Hydrocarbons | IV | Applied | T11 | medium |
| Pesticides – Insecticides | IV | Applied | T11 | medium |
| Pesticides – Herbicides | IV | Applied | T11 | medium |
| Pesticides – Rodenticides | IV | Applied | T11 | medium |
| Pesticides – Fumigants | IV | Applied | T11 | medium |
| Gases – Asphyxiants & Irritants | IV | Applied | T11 | medium |
| Air Pollution & Particulates | IV | Applied | T3 | medium |
| Drugs & Therapeutics – Toxicology | IV | Applied | T8 | high |
| Plant Toxins | IV | Applied | T11 | medium |
| Animal & Microbial Venoms / Toxins | IV | Applied | T11 | medium |
| Mycotoxins | IV | Applied | T1 | medium |
| Food Additives, Cosmetics & GRAS | IV | Applied | T7 | medium |
| Alcohols & Methanol/Ethanol | IV | Applied | T11 | medium |
| Radiation / UV / Ionizing | IV | Applied | T1 | high |
| Liver / Hepatotoxicity | I | C.Interpret | T2 | medium |
| Kidney / Nephrotoxicity | I | C.Interpret | T2 | medium |
| Lung / Pulmonary Toxicity | I | C.Interpret | T2 | medium |
| Nervous System / Neurotoxicity | I | C.Interpret | T2 | medium |
| Skin / Dermatotoxicity | I | C.Interpret | T2 | medium |
| Eye / Ocular Toxicity | I | C.Interpret | T2 | medium |
| Cardiovascular Toxicity | I | C.Interpret | T2 | medium |
| Hematology & Blood Toxicity | I | C.Interpret | T2 | medium |
| Immunotoxicology / Allergy | I | C.Interpret | T2 | medium |
| Endocrine Toxicology | I | C.Interpret | T2 | medium |
| Reproductive & Developmental Toxicity | I | C.Interpret | T2 | medium |

### Step 2: Domain III Keyword Override

Questions in Domain I or IV that contain Risk Assessment keywords get reclassified to Domain III. This catches dose-response, exposure assessment, and risk characterization questions that use topic tags from other domains.

Keyword categories (60+ terms):
- **Dose-response**: NOAEL, LOAEL, BMD, RfD, RfC, LD50, ED50, therapeutic index, POD, hormesis, dose-response curve
- **Exposure assessment**: margin of exposure, hazard quotient, TLV, PEL, TWA, biomonitoring, exposure route, body weight, inhalation rate
- **Hazard identification**: weight of evidence, IARC, cancer classification, Group 1/2A/2B, known/probable human carcinogen
- **Risk characterization/management**: risk assessment, risk characterization, OSHA standard, EPA guideline, FIFRA, REACH, cleanup, remediation
- **Uncertainty/extrapolation**: interspecies, intraspecies, safety factor, allometric scaling, DDEF, CSAF, non-threshold
- **Mode of action/AOP**: mode of action, adverse outcome pathway, key event
- **Sentinel**: "for risk assessment", "estimated daily intake", EDI

Threshold: ra_score >= 1 triggers Domain III reclassification. Confidence set to 'medium' if ra_score >= 3, 'low' otherwise.

### Step 3: Bloom Level Classification

**DEPRECATED — this section describes the v1 classification on the legacy 446-Q xlsx.
For the current 4,841-question bloom classification, see
`references/bloom-classification-methodology.md`.**

Heuristic-based keyword scan of question text.

- **Analyze**: 2+ indicators (mechanism, explain, compare, distinguish, rationale, why, due to, best explains...) → Only 3 questions classified as Analyze
- **Apply**: 1+ analyze indicator OR 1+ apply indicator (which of the following, most appropriate, best, select, patient, worker, exposed, scenario, management, treatment, most likely...) → 224 questions
- **Remember/Understand**: default fallback → 219 questions

Bloom confidence is 'medium' for all.

## Results

| Domain | Count | % |
|---|---|---|
| Domain IV (Applied Toxicology) | 191 | 42.8% |
| Domain I (Conduct of Studies) | 151 | 33.9% |
| Domain II (Mechanistic Tox) | 66 | 14.8% |
| Domain III (Risk Assessment) | 38 | 8.5% |

| Bloom | Count | % |
|---|---|---|
| Apply | 224 | 50.2% |
| Remember/Understand | 219 | 49.1% |
| Analyze | 3 | 0.7% |

| Confidence | Count |
|---|---|
| medium | 332 |
| high | 81 |
| low | 33 |

## Known Limitations

### Domain III Undercount

Expected ~38% (per exam blueprint), actual ~9%. Root causes:

1. **General language**: Many dose-response/exposure/risk questions use terms like "dose", "effect", "toxicity" rather than specific Risk Assessment jargon (RfD, BMD, MOE, POD). These get classified under their Topic (Primary) domain.

2. **Organ system cross-cutting**: Liver, Kidney, Nervous System, etc. questions are assigned to Domain I (Interpret — target organ identification), but many have Risk Assessment context (e.g., "What is the POD for cadmium nephrotoxicity?").

3. **Toxicant class overlap**: Domain IV questions about specific agents (metals, pesticides, solvents) often have risk assessment framing (exposure limits, regulatory standards, safety margins). The keyword override catches some but not all.

4. **Ambiguous boundaries**: The Handbook tasks themselves overlap across domains. A question about interpreting a dose-response curve is Domain I.C (Interpret) when framed as study interpretation, or Domain III.C (Dose-Response) when framed as risk assessment.

### Refinement Strategy

- **Low-confidence items first**: Review the 33 'low' confidence questions (Domain III keyword overrides) — verify or correct.
- **Organ system questions**: Manually review the 169 Domain I questions tagged as C.Interpret; reclassify those with clear dose-response/risk framing to Domain III.
- **Spot-check Domain IV**: Sample from Metals, Solvents, Pesticides questions — many likely have risk assessment framing.
- **Iterate keyword list**: Add terms discovered during manual review.
- **Bloom level calibration**: The 3 Analyze vs 224 Apply split may need recalibration. DABT exam likely has more Analyze-level questions than 0.7%.

## Usage

Load alongside main database:

```python
import pandas as pd

db = pd.read_excel('/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx', sheet_name='Questions')
cls = pd.read_csv('/root/work/dabt/dabt-tutor/reference/data/question_classifications.csv')
db = db.merge(cls[['ID', 'Domain', 'Sub-Domain', 'Task', 'Bloom Level']], on='ID', how='left')

# Filter by domain
domain_iii = db[db['Domain'] == 'Domain III']

# Filter low-confidence items for review
needs_review = cls[cls['Domain Confidence'] == 'low']
```

## Script

The classification script lives at `scripts/classify_questions.py` in the project root. Re-run to regenerate the CSV/JSON after updating topic mappings or keyword lists:

```bash
cd /root/work/dabt/dabt-tutor
python3 scripts/classify_questions.py
```

Output: `reference/data/question_classifications.csv` and `reference/data/question_classifications.json`.
