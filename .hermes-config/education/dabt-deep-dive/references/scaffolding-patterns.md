# Scaffolding Patterns & Protocols

## Journey/Narrative Pattern
For sequential/chain-of-events topics where order matters (ADME, AOP, carcinogenesis initiation→promotion→progression, MOA). Unlike the Terminology Ladder (hierarchical) or Methodology/Toolkit (decision-tree), this pattern traces ONE concrete entity through a system.

### When to use
- Learner says "too high-level" or "sparse" — this is the signal to RESTART at a lower narrative frame, NOT to add more facts to the current frame
- Topic is a sequence with branching or gatekeeping steps (first-pass is a gate; BBB is a gate; Phase I→Phase II is a pipeline)
- The parameters (Vd, CL, t½, F) serve the story rather than the story serving the parameters

### Build steps

1. **Pick one molecule** — a real toxicant the learner knows. For ADME: ethanol (simple), acetaminophen (bioactivation), TCDD (massive Vd, extreme t½), or a hypothetical Chemical X with defined properties (lipophilicity, pKa, MW, CYP substrate).

2. **Trace the journey step by step.** At each stage, ask before telling:
   - "It's in the stomach. Can it cross?" (ionization, pKa vs pH)
   - "It crossed into the enterocyte. Does it all go to the liver?" (transporters, P-gp efflux)
   - "It's in the portal vein. What happens in the liver?" (first-pass metabolism, saturation)
   - "Some escaped the liver. Where does it go next?" (systemic circulation, protein binding)
   - "Is it all in the blood or does it go into tissues?" (Vd, lipophilicity, tissue binding)
   - "Can it get into the brain? The fetus?" (BBB, placental transporters)
   - "Now it's been metabolized. How does it leave?" (renal, biliary, pulmonary excretion)

3. **The "reveal" question** — Position a question that forces the learner to discover a non-obvious principle. The canonical example for ADME:
   > At low dose, F = 15% (85% of oral dose never reaches systemic circulation). At high dose, AUC is 8× what linear scaling predicts. Where did that 85% go?
   > → The learner discovers first-pass saturation as a variable, not a fact to memorize.

4. **Connect parameters to the story** — Don't define Vd, CL, t½ until the journey has made the question "why?" meaningful:
   - After showing TCDD distributes into fat and stays there: "We need a way to describe 'how much of the body does this fill.' That's Vd. For TCDD, Vd >> total body water — because it's not in the water, it's in the fat."
   - After showing slow redistribution from fat: "The time it takes for half to leave is t½. For TCDD: 7-8 years. Now you know why."

5. **MCQ at the journey end** — Test the integrated understanding, not the isolated definition. The 8× AUC question from the ADME deep dive is the model: it requires the learner to connect bioavailability, first-pass, and saturation — not just recall a term.

### Depth calibration: the "sparse" signal
When the learner says "too high-level" or "I need to go back to basics":
- **WRONG response:** Add more facts to the current frame. Dense reference tables (Phase I vs Phase II, routes of excretion, etc.) without narrative scaffolding feel like a study guide, not teaching.
- **RIGHT response:** Restart at a lower narrative frame. Pick a simpler molecule. Ask "What happens first? What happens next?" at every step. Let the learner's answers determine pace. The narrative IS the structure — the definitions hang on it like ornaments on a tree rather than being scattered on the ground.

### When NOT to use
- Comparative topics (metals, solvents) → Six-Axis Framework
- Hierarchical definition chains (NOAEL→BMD→UF→RfD→CSF) → Terminology Ladder
- Decision-tree/tool-selection topics (statistics, study design, dose selection) → Methodology/Toolkit
- Regulatory/process frameworks (GLP, quality systems) → Three-Layer Architecture
- Drill-mode review → just present cards

## Methodology/Toolkit Pattern
For decision-tree/tool-selection topics where the content is a set of tools that must be selected based on situational rules. Applies to: statistics (t-test vs ANOVA vs χ² vs trend tests), study design selection (acute vs subchronic vs chronic), dose selection strategy, multiplicity correction choice.

### Contrast to the other patterns
- **Not a journey** — there's no single path through a system. The learner needs to choose between branches.
- **Not a ladder** — the concepts aren't hierarchical definitions building on each other. They're parallel alternatives with different applicability conditions.
- **Not a comparison matrix** — the decision is conditional ("if X then Y"), not a flat head-to-head.

### When to use
- Learner asks "which one do I use and why?" or says "break down the situations"
- Topic involves selecting between tools/methods based on data type, study design, or question
- Each tool has a clear trigger condition and an exam-trap confusable pair

### Build steps

1. **Open with a decision framework** — Present the branching logic visually as a decision tree or flowchart BEFORE definitions. The framework gives the learner a map before they navigate each branch. For statistics:
   ```
   Data type?
   ├── Continuous → Parametric? → 2 groups (t-test) vs ≥3 groups (ANOVA + post-hoc)
   │                       → Non-parametric? → 2 groups (Mann-Whitney) vs ≥3 groups (Kruskal-Wallis)
   └── Categorical → Proportions (χ²) vs Trend (Cochran-Armitage)
   ```

2. **Walk each branch individually** — One tool per sub-block. For each:
   - **Trigger condition:** concrete statement of when this tool applies ("two groups, independent, continuous, normal")
   - **Concrete toxicology example:** a real or realistic study design where this tool is the right choice
   - **The confusable pair:** name the tool it's most commonly mistaken for, and why
   - **Focused MCQ:** tests one decision — given this study design, which tool?

3. **One check-in per tool** — Each tool gets its own MCQ before moving to the next. Do NOT compress multiple tool selections into one complex MCQ until the learner has demonstrated each individually.

4. **The layered MCQ (only after all branches covered)** — Only once each tool has been individually tested, present a study design with multiple endpoints that requires selecting different tools for different endpoints. This tests the learner's ability to branch correctly within a single study context.

### Sub-block structure for statistics (worked example)

```
Sub-block 1: Central tendency vs dispersion + SD vs SE
  - Trigger: report mean/SD vs mean/SE; which describes animal variability?
  - MCQ: data with outlier, SE reported → identify the misrepresentation

Sub-block 2: 2-sample t-test vs paired t-test
  - Trigger: independent groups vs same-subjects pre/post
  - MCQ: given a crossover design, pick the test

Sub-block 3: ANOVA + Dunnett
  - Trigger: ≥3 groups, all vs a common control
  - MCQ: 4-dose study, identify correct post-hoc

Sub-block 4: χ² test
  - Trigger: categorical/proportional data (incidence, mortality)
  - MCQ: tumor incidence across groups → pick the test

Sub-block 5: Multiplicity correction
  - Trigger: multiple comparisons, FWER control
  - MCQ: Bonferroni vs Dunnett vs Williams — pick for correlated dose endpoints

Sub-block 6: Trend tests (Cochran-Armitage, Williams')
  - Trigger: ordered dose groups, monotonic trend hypothesis
  - MCQ: carcinogenicity bioassay with monotonic tumor incidence → pick trend test

Sub-block 7: Integrated layered MCQ
  - One study design (e.g., subchronic tox with 4 endpoints)
  - Learner must pick the right test for EACH endpoint
```

### Key protocols

- **Decision-tree-first:** Open every tool-selection topic with the framework, not definitions. The framework IS the scaffold — definitions hang on its branches.
- **One branch at a time:** If the learner says "we need to go through this one by one" after you opened with a layered MCQ, the correction is the same: retreat to individual tool sub-blocks and only re-attempt the layered MCQ after all are covered individually.
- **Confusable pairs first:** For each tool, surface the confusable pair proactively. "This is when you use a paired t-test. The trap is using a 2-sample t-test on paired data — you lose power."
- **User-preference embedding:** This learner (TempMoon) prefers decision-tree framing for tool-selection topics. Open with the tree, not with definitions. Each sub-block should test one decision before layering.

## Six-Axis Metals Framework
Fixed-order comparison frame for metals deep dives:
1. **Valence/form** — toxic vs essential form; why valence determines entry/binding
2. **Half-life/accumulation** — acute vs chronic vs cumulative; temporal profile
3. **Target organs** — route-of-exposure distribution; pathognomonic targets
4. **Biomarkers** — matrix (urine/blood/hair/nails), assay measure, interpretation nuance
5. **Chelator availability** — effective chelators per metal and mechanistic reason
6. **Carcinogenic mechanism** — direct vs indirect genotoxic vs epigenetic; IARC class

Forces head-to-head comparison on every dimension. Validated 2026-05-19 As/Cd/Cr deep dive.

## Three-Layer Architecture Pattern
For teaching process-oriented regulatory content (GLP/OECD, quality systems, compliance frameworks) where the material naturally divides into people, procedures, and outputs.

### When to use
- Topic is a regulatory framework (GLP, GMP, ICH guidelines, quality management systems)
- The content has clear "who does what," "how it's done," and "what survives" dimensions
- The exam tests role responsibility questions (Who signs the report? Who audits? Who provides resources?)

### When NOT to use
- Mechanism-based topics (MOA, AOP) → Journey/Narrative
- Decision-tree topics (study design selection, statistics) → Methodology/Toolkit
- Comparative topics (metals) → Six-Axis Framework

### Build steps

1. **Open with the Why** — Lead with the historical catalyst (e.g., IBT scandal for GLP) or the problem the framework was designed to solve. Ask the learner: "If you were the regulator, what would you require?" This engages them in first-principles thinking before the formal structure is revealed.

2. **Present the three-layer architecture** — After establishing the Why, present the structure as three natural layers:

   **Layer 1 — Who (roles and responsibilities)**
   Who runs it? Who audits it? Who funds it? Who owns the output?
   - Single point of accountability (Study Director)
   - Independent oversight (QAU)
   - Support structure (Management)

   **Layer 2 — How (procedures and rules)**
   How is work standardized? How are changes documented? What governs daily operations?
   - Standard Operating Procedures (SOPs)
   - Protocols and amendments
   - Equipment qualification and calibration

   **Layer 3 — What survives (data and artifacts)**
   What records must exist? What are the rules for creating, correcting, and keeping them?
   - Raw data rules (contemporaneous, indelible, attributable)
   - Final reports (who signs, what they contain)
   - Archiving (what goes in, how long, who controls access)

3. **One exam-relevant check-in per layer** — The exam tests role distinctions (Layer 1: SD vs QAU) more than procedural detail. For Layer 1, a question testing independence and accountability is ideal. For Layer 3, a raw-data correction scenario is the typical exam format.

4. **Proceed signal applies** — If the learner responds well to the Why opener and says "continue," present all three layers as structured content. Do not Socratic-discover every sub-point across all three layers — the structure itself is the scaffold.

### Example: GLP/OECD (validated May 30 session)
Opener: IBT scandal → "What would you require?" → Learner says "regs for documentation and auditability" → "Continue" signal → Present 3 layers:
- Layer 1: Study Director (owns study), QAU (audits independently), Management (resources, no interference)
- Layer 2: SOPs (every routine procedure), Protocol (approved before work, amendments for changes)
- Layer 3: Raw data (no erasures, strike+initial+date+reason), Final report (SD signs, QAU attaches statement), Archive (10-15yr retention)

### Extends to other regulatory content
- **ICH Q1 (Stability):** Layer 1 = Stability Study Director, QA, Management. Layer 2 = Stability protocols, storage conditions, testing schedule, pull points. Layer 3 = Stability data, chromatograms, trend reports, retest/expiry dates.
- **GCP:** Layer 1 = Principal Investigator, Sponsor, IRB/IEC. Layer 2 = Case report forms, informed consent, monitoring plan. Layer 3 = Source documents, audit trail, regulatory filing.
- **21 CFR Part 11 (Electronic Records):** Layer 1 = System owner, users, administrator. Layer 2 = Access controls, audit trails, backup procedures. Layer 3 = Electronic signatures, audit logs, archived records.

## Terminology Ladder Pattern
For chains of related terms (NOAEL→BMD→UF→RfD→CSF). Per-rung:
1. Context + prompt → learner articulates *before* you define
2. Probe edges, don't correct immediately
3. Only after exhausted reasoning → formal definition (ABT-handbook precise)
4. MCQ with full distractor breakdown
5. Name the classic exam confusion for this term

Exit: learner correctly reasons through final-rung MCQ without help.

## Think-Out-Loud Protocol
Say "Think out loud" before revealing answer. Let learner talk through reasoning fully. When wrong → probe edges ("What if X changed?"). Only provide answer after reasoning exhausted or explicitly requested.

## Answer-Change Probing
When learner changes answer, probe why. The change itself is diagnostic (did they realize something or switch to new wrong intuition?). Validate correct answer only after they articulate the reasoning chain.

## Distractor-Targeting Protocol
Every MCQ → option-by-option breakdown:
- What reasoning error each distractor targets
- Why it's wrong in concrete, mechanistic terms
- Which exam trap it maps to (statistical-significance vs adversity, endpoint cherry-picking, study-type confusion, etc.)

Required per TempMoon directive — do not skip.

## Stuck-on-Rung Protocol
When learner can't proceed: pause ladder. Offer concrete analogy from different domain. Walk through concept in simpler terms. Ask "Which part doesn't click?" Only resume when learner confirms readiness. If still stuck, save position to memory and flag for next session.

## Summary Artifact Template
Save to `deep-dives/YYYY-MM-DD-<topic>-dive.md`:
```markdown
# Deep Dive: [Topic]
**Date:** YYYY-MM-DD
**Domain:** [I-IV].[Sub-domain].Task [N]
**Prior Gap:** [Where mental model was breaking]
**Corrected Mental Model:**
- [Key point]
**Key Mechanisms / Definitions:**
- [mechanism]
**Integration Points:**
- Connects to [domain/topic] via [link]
**Retention Drill Questions:** (5-10 questions)
**Primary Sources:**
- Casarett Ch.[N], [section]
- [Guideline/Handbook]
```
