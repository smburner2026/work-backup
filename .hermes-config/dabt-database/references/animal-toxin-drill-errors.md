# Animal & Venom Toxin DB Errors Found During Drilling

Error discovered 2026-05-26 during Session 3 mixed blueprint drill (TempMoon).

## DABT-0494 — Gila Monster Venom (source_file_id=1, Mini-ABT 1-11)

**Source:** Mini-ABT 1-11 (legacy xlsx → SQLite, source_file_id=1)
**Domain assigned:** Domain I (Conduct of Studies) — topic "General Toxicology"
**Question:** "The venom from the Gila monster _____."

### The Four Options

| Option | Text | Verdict |
|--------|------|---------|
| A | does not have a commercially available antivenom | **✅ CORRECT per reference** |
| B | is similar to the coral snake | ❌ DB stored answer — not supported by reference |
| C | is a frequent cause of death | ❌ False — "far less dangerous than is generally believed" |
| D | is used in cancer treatments | ❌ False — exenatide is for type 2 diabetes |

### Reference Citations (Casarett & Doull 9e, Ch.26)

**Option A — No antivenom commercially available:**
> "No antivenin is commercially available. Treatment is supportive." (lines 2636-2637)

**Option D — Not cancer treatment:**
> "exenatide from Gila monster venom is used in type 2 diabetes treatment" (lines 3591-3592)

**Option B — Coral snake similarity not supported:**
Casarett lists the venom composition as: serotonin, amine oxidase, phospholipase A, bradykinin-releasing substance, helodermin, gilatoxin, high hyaluronidase activity, low proteolytic activity. Notably **lacks** acetylcholinesterase, nucleotidase, ATPase, and the α-neurotoxins that define elapid (coral snake) venom. The venom is structurally distinct from coral snake venom.

**Option C — Not a frequent cause of death:**
> "far less dangerous than is generally believed" (line 2527)

### Significance

This is the **first documented non-2000Q-Bank error** (source_file_id=1) in the error tracking system. All prior documented errors (batch7 through batch38) are from source_file_id=2 (2000Q Question Bank). This finding proves that answer key errors exist across ALL source banks, not just the 2000Q Bank. Treat all Mini-ABT, Chapter Test, and Kristen questions with the same suspicion as 2000Q Bank questions during drill review.
