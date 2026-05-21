# Post-Review Performance Assessment — Worked Examples

## Case 1: First-Pass Learning (what happened this session)

**Situation:** 40 cards created < 6 hours ago. User says "I studied this a couple days ago and still missed everything."

**Analysis:** Cards were brand new. The user confused "studied the topic a couple days ago" (read the arsenic deepdive transcript) with "rehearsed these specific flashcards." Two different things — reading comprehension generates familiarity, recall generates retention. The cards were never seen before, so every card was a cold retrieval attempt.

**Fix:** Rate all `hard` → 24h spacing. Next session is a genuine second pass. Also: create study cards 24h before a planned review, not during the same session.

---

## Case 2: Confusable Cluster — Cadmium Renal Biomarkers

**Cards involved:**
- "What urinary biomarker reflects Cd-induced renal tubular damage?" → β₂-MG
- "What urinary enzyme is a sensitive biomarker for early Cd nephrotoxicity?" → NAG
- "What is the most important Cd-binding protein and why is it relevant as a biomarker?" → Metallothionein

**Why they collapse:** All three answer "something urinary from the kidney related to cadmium." Without a mechanism anchor, the brain stores them as a single slot → picks randomly on retrieval.

**Anchor fix (create these cards first):**
1. "Why does β₂-MG appear in urine during Cd nephrotoxicity?" → "Low-molecular-weight protein, freely filtered at glomerulus, normally reabsorbed by proximal tubule. Cd damages proximal tubule cells → β₂-MG spills un-reabsorbed into urine."
2. "Why does NAG appear in urine during Cd nephrotoxicity?" → "NAG is a lysosomal enzyme. When Cd kills proximal tubular cells, lysosomes rupture → NAG released into urine. It's an enzyme, not a filtered protein — mechanism differs from β₂-MG."
3. "Why is metallothionein elevated in urine after Cd exposure?" → "MT is induced by Cd binding. Cd-MT complex accumulates in kidney. When tubular cells are damaged, the Cd-MT complex itself spills into urine — it's a direct measure of renal Cd burden, not tubular injury per se."

**Mnemonic chain:** β₂-MG = filtered then not reabsorbed → tubular function. NAG = released from dead cells → tubular damage. MT = Cd storage protein → Cd body burden.

---

## Case 3: Compound Card — Dual Retrieval

**Card:** "What is the approximate half-life of cadmium in the human body and its biomarker implication?"

**Why it fails:** The user must retrieve two disconnected facts: a number (>26 yr) AND a conceptual inference (cumulative poison, urine reflects lifetime burden). If they remember the number but stall on the implication, the card is "wrong" despite having the number right. But the rating tool only records one answer, so you can't tell which part they knew.

**Split into:**
- Card A: "What is the approximate half-life of cadmium in the human body?" → ">26 years"
- Card B: "Why is cadmium considered a cumulative poison in biomarker terms?" → "26 yr half-life + high MT binding affinity + very slow renal elimination → urine Cd reflects lifetime body burden, not recent exposure"

**Now each card tests one retrieval. If the user gets A but misses B, you know exactly where the gap is.**

---

## Case 4: Blocked Practice Fatigue

**Situation:** 8 consecutive cadmium cards, user misses #5-#8 after getting #1-#4 correct. Says "I knew this 10 minutes ago, now it's gone."

**Analysis:** After 4-5 cards on the same sub-topic, the brain switches from retrieval to pattern-matching. The user is guessing from context rather than recalling. The last cards in a block look harder than they are because the retrieval mechanism is exhausted.

**Fix:** Interleave collections. Alternate between Pb → Cd → As → Hg rather than all-Cd-block. The memento `due` command returns cards ordered by `next_review_at` within a collection — if multiple collections are due, present them round-robin.

---

## Case 5: Gist Learning, Not Specific Recall

**Card:** "What is the OSHA blood lead threshold for medical removal?"

**User answer:** "Like, 40-something."

**Analysis:** The user absorbed the general magnitude but not the precise number. This is the most common failure mode in exam prep — the brain remembers "around 40" but not "≥40 µg/dL" or the context (medical removal vs action level vs reference value).

**Fix options:**
1. Shrink the answer to the minimal exam-worthy string: "≥40 µg/dL"
2. Add a precision-marker card: "OSHA medical removal BLL: ≥40 or >40?" → "≥40 (action level is 40, removal triggers at or above)"
3. Add a comparison card: "What distinguishes OSHA blood lead action level from medical removal level?" → "Action level = 40 µg/dL leads to monitoring. Medical removal = ≥40 µg/dL with confirmed exposure."
