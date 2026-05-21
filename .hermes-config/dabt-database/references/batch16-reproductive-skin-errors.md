# Batch 16 Reproductive & Skin Toxicology DB Answer Discrepancies

Batch: DABT-0969 through DABT-1018 (50 questions)
Source: 2000Q Bank (source_file_id=2)
Domain: All Domain IV — Applied Toxicology
Topics:
- Skin / Dermatotoxicity: DABT-0969 to DABT-0994 (26 questions)
- Reproductive & Developmental Toxicity: DABT-0995 to DABT-1018 (24 questions)
Date processed: 2026-05-20

## Summary

**Total DB errors/discrepancies: 24 out of 50 questions (48%)**
- Skin / Dermatotoxicity: **13 errors in 26 questions (50%)**
- Reproductive & Developmental Toxicity: **11 errors in 24 questions (46%)**

This batch is among the most error-prone encountered across all source banks. Of the 24 errors:
- 7 are **answer-letter-E** issues (correct_answer_letter='E' but only A–D options stored — import corruption)
- 12 are **wrong-standard-answer** (the stored answer contradicts established toxicology in Casarett & Doull)
- 4 are **matching-item wrong pairings** (single-option matching items with toxicologically incorrect associations)
- 1 is a **text corruption** ("Matching Test" appended into option_text)

---

## PART 1: SKIN / DERMATOTOXICITY ERRORS (DABT-0969 to DABT-0994)

### Category 1: Answer Letter E Issues (corrupt import — E with no corresponding option)

| QID | Question | DB ans | Real answer | Rationale |
|-----|----------|--------|-------------|-----------|
| DABT-0981 | Incidents in Seveso, Italy, and Taiwan produced outbreaks of _____. | **E** (no option stored) | **A** (chloracne) | Seveso (1976, TCDD/dioxin release) and Taiwan Yu-Cheng (1979, PCB/PCDF-contaminated rice oil) both caused epidemic chloracne — a hallmark AhR-mediated keratinocyte differentiation defect. Options: A=chloracne, B=malignant melanoma, C=urticaria, D=phototoxic dermatitis. |
| DABT-0983 | Drug-induced life-threatening skin reaction from apoptosis via death receptors is _____. | **E** (no option stored) | **C** (toxic epidermal necrolysis) | TEN involves Fas/CD95 + TNF-alpha death receptor cascade -> massive keratinocyte apoptosis and epidermal detachment. Options: A=anaphylaxis, B=psoriasis, C=TEN, D=xeroderma pigmentosum. |

### Category 2: Wrong Standard Answer (schema contradicts Casarett & Doull)

| QID | Question | DB Answer | Tox. Correct | Rationale |
|-----|----------|-----------|-------------|-----------|
| DABT-0973 | All phototoxic drugs/chemicals EXCEPT _____. | **B** (tetracycline) | **A** (ampicillin) | Tetracyclines (doxycycline, demeclocycline) are among the BEST documented phototoxic drugs clinically. Ampicillin is not typically associated with phototoxicity. Options: A=ampicillin, B=tetracycline (DB says exception but it IS phototoxic), C=anthracene, D=8-methoxypsoralen. |
| DABT-0982 | Direct histamine release without antibodies can be caused by _____. | **A** (thiazide diuretics) | **B** (opiate analgesics) | Opiates (morphine, codeine) cause direct mast cell degranulation via MRGPRX2 — the classic pharmacologic non-immunologic histamine release. Thiazides not associated. Options: A=thiazides, B=opiates, C=tetracycline, D=tricyclics. |
| DABT-0984 | Psoralens are associated with _____. | **A** (acne) | **C** (phototoxic dermatitis) | Psoralens are photoactive furocoumarins causing phototoxic dermatitis via DNA adducts upon UVA. No known association with acne. |
| DABT-0985 | Arsenic is associated with _____. | **D** (photoallergic dermatitis) | **B** (skin carcinoma) | Chronic arsenic causes Bowen's disease, BCC, SCC plus hyperkeratosis/hyperpigmentation. NOT associated with photoallergic dermatitis. |
| DABT-0988 | Sulfonamides cross-react in allergic-contact sensitization with _____. | **D** (tetracycline) | **A** (para-aminobenzoic acid / PABA) | Classic cross-reactivity: sulfonamides <-> PABA (shared para-aminophenyl group). Also with benzocaine, procaine, sulfa dyes. |
| DABT-0990 | All TRUE of skin EXCEPT _____. | **D** (SC cells lost nucleus) | **C** (active transport in SC) | SC is dead corneocytes — no active transport possible. Option D IS true (anucleate). **Corruption:** D text has "Matching Test" appended. |

### Category 3: Matching Items — Wrong Pairings (all 4)

| QID | Term | Stored Match | Should Be | Rationale |
|-----|------|-------------|-----------|-----------|
| DABT-0991 | **androgens** | contact dermatitis (B) | **acne** | Androgens (DHT) stimulate sebaceous glands -> acne. Contact dermatitis is type IV hypersensitivity. |
| DABT-0992 | **selenium** | fixed drug eruption (A) | **alopecia** | Selenosis causes alopecia, nail loss, garlic odor. Not fixed drug eruption. |
| DABT-0993 | **neomycin sulfate** | alopecia (E) | **contact dermatitis** | Neomycin is a classic type IV contact sensitizer (topical antibiotic allergen). Not alopecia. |
| DABT-0994 | **tetracycline** | causes acne (E) | **phototoxic dermatitis** | Tetracyclines TREAT acne (anti-C. acnes + anti-inflammatory). Phototoxic dermatitis is the toxicologically correct association. |

**Correct mapping:** androgens -> acne; selenium -> alopecia; neomycin -> contact dermatitis; tetracycline -> phototoxic dermatitis

---

## PART 2: REPRODUCTIVE & DEVELOPMENTAL TOXICITY ERRORS (DABT-0995 to DABT-1018)

### Category 1: Answer Letter E Issues

| QID | Question | DB ans | Real ans | Rationale |
|-----|----------|--------|----------|-----------|
| DABT-0995 | Sexual differentiation begins at gestation week _____. | **E** | **C** (7) | Week 7: SRY directs bipotential gonad -> testis. Options: 2, 3, 7, 10. |
| DABT-1011 | Most important hormone in milk production is _____. | **E** | **C** (prolactin) | Prolactin drives lactogenesis. Oxytocin = milk ejection. Options: serotonin, oxytocin, prolactin, norepinephrine. |
| DABT-1012 | In humans, corpus luteum maintenance depends on _____. | **E** | **D** (hCG) | hCG from syncytiotrophoblast is critical luteotrophic signal in humans. Options: pituitary hormones, estrogen, prolactin, hCG. |
| DABT-1013 | 50% progesterone reduction at midpregnancy in rat causes _____. | **E** | **D** (no effect) | Rat has ovarian reserve + placental compensatory capacity. Options: ambiguous genitalia, litter loss, breast cancer, no effect. |
| DABT-1015 | Miroestrol is _____. | **E** | **D** (a phytoestrogen) | From *Pueraria mirifica* (kwao krua), Thai traditional medicine. Options: DES metabolite, fungal product, marine product, phytoestrogen. |

### Category 2: Wrong Standard Answer

| QID | Question | DB Answer | Tox. Correct | Rationale |
|-----|----------|-----------|-------------|-----------|
| DABT-0999 | Puberty stages determined by _____. | **C** (serum cortisol) | **D** (Tanner stages) | Tanner staging (SMR 1-5) is THE universal standard. Cortisol is a stress hormone unrelated to pubertal staging. |
| DABT-1003 | All potential EDCs EXCEPT _____. | **A** (TCDD) | **B** (acetone) | TCDD IS a potent EDC via AhR (listed by WHO/UNEP). Acetone is a simple solvent with zero EDC activity. |
| DABT-1007 | All true of rat uterine weight EXCEPT _____. | **C** (varies with estrus) | **D** (not measured) | Uterine weight DOES vary with cycle (proestrus peak). It IS a standard endpoint in uterotrophic assay and reproductive studies. |
| DABT-1010 | Drug class that could cause ED is _____. | **A** (NSAIDs) | **B** (autonomic NS drugs) | ANS drugs (anticholinergics, sympatholytics) are well-established ED causes. PDE5 inhibitors TREAT ED. |
| DABT-1017 | The herbicide linuron is _____. | **D** (estrogen antagonist) | **B** (androgen antagonist) | Linuron is a well-documented antiandrogen (AR antagonist: reduced AGD, retained nipples). NOT an estrogen antagonist. |
| DABT-1018 | All environmental antiandrogens EXCEPT _____. | **C** (p,p'-DDE) | **D** (nandrolone) | p,p'-DDE IS an antiandrogen (AR antagonist). Nandrolone is an AR agonist (anabolic steroid) — correct exception. |

---

## Error Statistics

| Category | Skin (/26) | Repro (/24) | Total (/50) |
|----------|-----------|-------------|-------------|
| Answer Letter E (import corruption) | 2 (7.7%) | 5 (20.8%) | 7 (14%) |
| Wrong Standard Answer | 6 (23.1%) | 6 (25.0%) | 12 (24%) |
| Matching Wrong Pairing | 4 (15.4%) | 0 (0%) | 4 (8%) |
| Text Corruption | 1 (3.8%) | 0 (0%) | 1 (2%) |
| **Total** | **13 (50.0%)** | **11 (45.8%)** | **24 (48.0%)** |

## Reference Chapters for Verification

| Topic | Reference | Notes |
|-------|-----------|-------|
| Skin / Dermatotoxicity | Casarett & Doull Ch.19 | ICD vs ACD, phototoxicity, chloracne, chemical burns, skin penetration |
| Male Reproductive | Casarett & Doull Ch.20; Hayes Ch.18 | Sexual diff., TDS, spermatogenesis, androgens |
| Female Reproductive | Casarett & Doull Ch.20; Hayes Ch.19 | Ovarian function, estrus cycle, puberty, lactogenesis, uterotrophic assay |
| Endocrine Disruption | Casarett & Doull Ch.20 | EDC mechanisms, antiandrogens, phytoestrogens, pulp mill effluents |

## Lessons for Future Batches

1. **Reproductive & Developmental Toxicity is HIGHLY error-prone (46%)** — cross-check every answer against Casarett & Doull Ch.20. Especially unreliable: puberty staging (DABT-0999), EDC classification (DABT-1003, DABT-1018), herbicide MOA (DABT-1017).

2. **Letter-E corruption extends to reproductive toxicity** — 5 of 24 repro questions have ans='E' with only A-D options. Map to correct answer via the explanation field and available options.

3. **Skin matching items are scrambled** — all 4 items (DABT-0991–0994) are wrong. Do not trust single-option skin matching items from the 2000Q Bank.

4. **"EXCEPT" questions are systematically unreliable** — DABT-0973, DABT-0990, DABT-1003, DABT-1007 all misidentify the exception. Same pattern seen in immunotoxicology (data-quality-audit.md).
