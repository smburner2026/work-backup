# Batch7 DB Errors and Fixes (DABT-0568 to DABT-0618)

Generated 2026-05-20. Source bank: 2000Q Bank (source_file_id=2).

## Matching Test Scrambles (DABT-0573 to DABT-0582)

The DB has both `correct_answer_letter` AND `correct_answer_text` scrambled for the General Principles matching test. The import process misaligned the entire column B to column A mapping.

### Correct Mappings

| DB ID | Term | Correct | DB Had | Source |
|-------|------|---------|--------|--------|
| DABT-0573 | antagonism | B: 4 + 0 = 1 | C: program to prevent birth defects | Casarett Ch.2 |
| DABT-0574 | TOCP | C: delayed neurotoxicity | E: performs human risk assessment | Casarett Ch.22 |
| DABT-0575 | probit unit | D: normal equivalent deviation plus 5 | E: idiosyncratic-prolonged apnea | Casarett Ch.2 |
| DABT-0576 | synergy | E: 2 + 3 = 10 | C: delayed neurotoxicity | Casarett Ch.2 |
| DABT-0577 | succinylcholine | E: idiosyncratic-prolonged apnea | D: normal equivalent deviation plus 5 | Casarett Ch.4 |
| DABT-0578 | STEPS | C: program to prevent birth defects | B: 4 + 0 = 1 | Casarett Ch.10 |
| DABT-0579 | Superfund Act | C: toxicology and the law | (correct) | Casarett Ch.35 |
| DABT-0580 | descriptive toxicologist | E: conducts/designs toxicity tests | E: 2 + 3 = 10 | Casarett Ch.1 |
| DABT-0581 | regulatory toxicologist | E: performs human risk assessment | (no option stored) | Casarett Ch.35 |

### How the Fix Works (in generate_batch7.py)

```python
OVERRIDES = {
    'DABT-0573': ('B', '4 + 0 = 1', 'Domain I'),
    'DABT-0574': ('C', 'delayed neurotoxicity', 'Domain I'),
    # ... each overridden with (correct_letter, correct_text, domain)
}
```

## Hematology DB Errors (DABT-0583 to DABT-0618)

Most hematology answers are correct (verified against Casarett Ch.11). Three exceptions:

### DABT-0584: Megaloblastic Anemia Features

- **Question:** "All of the following could be features of megaloblastic anemia except _____"
- **Options:** A. low serum B12 or folate, B. microcytosis (decreased MCV), C. pancytopenia, D. hypersegmented neutrophils
- **DB says:** A (low serum B12 or folate) — **WRONG**
- **Correct:** B (microcytosis)
- **Reasoning:** Megaloblastic anemia = macrocytic (increased MCV). Low B12/folate is the CAUSE not a morphologic feature, but it IS a laboratory finding. Microcytosis is definitively NOT a feature. Casarett Ch.11 Table 11-2 lists: macrocytic RBCs, hypersegmented neutrophils, pancytopenia — never microcytosis.

### DABT-0592: Ferric Heme + Chloride Complex

- **Question:** "During oxidative hemolysis of red blood cells, the ferric iron in heme can react with chloride to form a complex called _____"
- **Options:** A. Heinz bodies, B. hemin, C. hemosiderin, D. beta 2 microglobulin
- **DB says:** D (beta 2 microglobulin) — **WRONG**
- **Correct:** B (hemin)
- **Reasoning:** Ferric protoporphyrin IX + chloride = hemin (iron protoporphyrin IX chloride). This is basic biochemistry — hemin forms brown rhomboid crystals and is a biomarker of intravascular hemolysis. B2M is an MHC class I component, unrelated to heme chemistry.

### DABT-0616: Lupus Anticoagulants

- **Question:** "All of the following are true of lupus anticoagulants except _____"
- **Options:** A. antibodies that interfere with PL-dependent coagulation, B. potentiate procoagulant mechanisms, C. can cause severe bleeding, D. induced by procainamide/hydralazine
- **DB says:** A — **CONTROVERSIAL (likely wrong)**
- **Likely correct:** C
- **Reasoning:** LAs DO interfere with PL-dependent coagulation tests (A is true). They ARE prothrombotic in vivo (B is true). LAs don't typically cause severe bleeding (C is false — paradox: in vitro anticoagulant, in vivo procoagulant). Procainamide/hydralazine CAN induce LAs (D is true). So C should be the exception. However, the DB answer A is what the source key says.

## Domain Assignment

All hematology questions (DABT-0583 to DABT-0618) are classified "Domain IV" (Applied Toxicology). The General Principles questions (DABT-0568 to DABT-0582) are "Domain I" (Conduct of Studies). This matches the exam blueprint — blood toxicity falls under target organ toxicology in Domain IV.

## Reference Used

Primary: Casarett & Doull Ch.11 "Toxic Responses of the Blood" (5,150 lines, pp.612-651)
Secondary: Casarett Ch.2 (General Principles), Hayes Ch.33 (Renal + blood discussion scattered)
