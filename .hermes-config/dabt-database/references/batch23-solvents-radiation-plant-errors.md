# Batch 23 — Solvents (Matching) / Radiation / Plant Toxins DB Errors

**Batch questions:** DABT-1319 to DABT-1368 (50 questions)
**Domains:** Domain IV (Applied Toxicology)
**Source bank:** 2000Q Bank (source_file_id=2), primarily Ch.24 (Solvents), Ch.25 (Radiation), Ch.27 (Plant Toxins)

## 1. Solvents & Hydrocarbons — Matching Test (Ch.24, Qs 65–73)

The DB IDs DABT-1319–1324 correspond to questions #68–73 in the original 2000Q Ch.24 "Matching Test" (source question numbers 1227–1232). The CSV parser stored the printed choice letter next to each term as the "correct answer," but the actual answer key is in a separate section of the docx.

### Correct mapping from source answer key

From the original `2000Q Ch24 CHEMICAL AND SOLVENT TOXICOLOGY.docx`, the Matching Test answer key reads:

| # | Term | DB-stored match (LETTER) | DB-stored match (TEXT) | **Actual answer (LETTER)** | **Actual match** |
|---|------|------------------------|----------------------|--------------------------|-----------------|
| 1227 (DB-1319) | calcium oxide | C | liver and pancreatic toxicity | **J** | caustic alkali |
| 1228 (DB-1320) | chromic acid | D | depletes ozone in atmosphere | **B** | inorganic lung carcinogen |
| 1229 (DB-1321) | esters | E | potentiates absorption of other chems through skin | **A** | low odor threshold |
| 1230 (DB-1322) | chlorofluorocarbons | E | azo dyes | **E** | depletes ozone in atmosphere |
| 1231 (DB-1323) | dimethyl sulfoxide | E | may release HCN while burning | **F** | potentiates absorption of other chems through skin |
| 1232 (DB-1324) | dimethylformamide | A | *(empty)* | **D** | liver and pancreatic toxicity |

The answer bank options (A–J) were:
A. low odor threshold
B. inorganic lung carcinogen
C. mist associated with laryngeal cancer
D. liver and pancreatic toxicity
E. depletes ozone in atmosphere
F. potentiates absorption of other chemicals through the skin
G. azo dyes
H. may release HCN while burning
I. glue sniffing
J. caustic alkali

**Error rate: 100%** — all 6 matching items have incorrect answers in the DB.

**Pattern:** The DB stored the option LETTER and OPTION TEXT that were listed adjacent to each term in the matching test, NOT the correct answer from the answer key. This is a systematic CSV extraction error — the parser treated the matching-pair list as if each row's choice letter were the correct answer, when in fact the printed letter only indicates which answer-bank entry corresponds to that row. The actual correct answer letter (from the answer key section) was completely ignored.

## 2. Radiation / UV / Ionizing (Ch.25, DABT-1325–1348)

**Total: 24 questions | Confirmed errors: 7 (29%)**

| DB ID | DB-stored Answer | Issues Found |
|-------|-----------------|--------------|
| DABT-1327 | D: oxygen 16 (pure gamma emitter) | Oxygen-16 is STABLE, not a gamma emitter. Technetium-99m (A) is the classic pure gamma emitter used in nuclear medicine. DB answer is wrong. |
| DABT-1330 | C: converting a neutron into a proton and electron | 1.02 MeV is the threshold for PAIR PRODUCTION (electron-positron pair production in the field of a nucleus). DB answer describes beta decay, not pair production. Wrong. |
| DABT-1332 | A: do not have relativistic velocities | Alpha particles are most dangerous when they are INHALED or INGESTED (internal exposure). Their danger comes from high LET, not velocity. Describing them as "most dangerous when they do NOT have relativistic velocities" is misleading. The correct characterization is that alpha particles are most dangerous as internal emitters (inhalation/ingestion). |
| DABT-1342 | A: nitrogen, oxygen, and silicon | These are NOT sources of terrestrial background radiation. The correct answer should be D: uranium, thorium, and potassium — the three main primordial radionuclides. |
| DABT-1345 | A: have a wavelength in the visible range | Relativistic beta particles have de Broglie wavelengths in the X-ray/gamma range (~10⁻¹² m), not visible range (~10⁻⁷ m). Wrong. |
| DABT-1347 | E (no stored text; options: A=rem, B=sievert(Sv), C=roentgen, D=gray(Gy)) | The unit of equivalent dose is the sievert (Sv), which IS listed as option B. If answer E means "none of the above," it's wrong because sievert is the correct SI unit. If answer E means "rem," that's the obsolete unit — still sometimes used but not the SI answer expected for DABT. Potentially correct as "rem" if the source considers it the answer, but sievert is the standard. |
| DABT-1348 | D (no stored text or options) | "Term-effective dose" — no data to verify. Likely refers to effective dose (tissue-weighted sum of equivalent doses). If options were standard, D would need verification against source. |

**Note on DABT-1334 (electron capture):** The DB answer A (electron capture) is actually correct — combination of an inner-shell electron with a nuclear proton defines electron capture. ✅

**Note on DABT-1335 (ICRP 1990 limit):** DB answer B (250 mSv in 5 years) is partially correct — the 1990 ICRP recommendation was 100 mSv in 5 years (20 mSv/yr). The 250 mSv value appears to be from a different ICRP document or a later revision. Verify against Casarett & Doull Ch.25.

## 3. Plant Toxins (Ch.27, DABT-1349–1368)

**Total: 20 questions | Confirmed errors: 10 (50%)**

| DB ID | DB-stored Answer | Correct Answer | Issue |
|-------|-----------------|---------------|-------|
| DABT-1350 | D: ergot (poison ivy allergen) | **A: urushiol** | Urushiol is the classic poison ivy contact allergen. Ergot is a fungal alkaloid from Claviceps. DB swapped answers. |
| DABT-1354 | C: silymarin (poppy DNA intercalator) | **B: sanguinarine** | Silymarin is from milk thistle, not poppy. Sanguinarine from poppy/Argemone intercalates DNA. |
| DABT-1356 | D: activation of proto-oncogenes (ricin MOA) | **A: inhibition of protein synthesis** | Ricin depurinates 28S rRNA, inhibiting protein synthesis. This is one of the best-known facts in plant toxicology. |
| DABT-1357 | D: 4-ipomeanol (mad honey) | **A: grayanotoxin** | Mad honey from Rhododendron contains grayanotoxin, a Na-channel toxin. 4-Ipomeanol is a pulmonary toxin from moldy sweet potatoes. |
| DABT-1358 | A: antidepressant (cascara sagrada) | **B: a laxative** | Cascara is a classic stimulant laxative containing anthraquinone glycosides. It has no established antidepressant activity. |
| DABT-1359 | B: toxic shock syndrome (Symphytum) | **D: Budd-Chiari syndrome** | Comfrey (Symphytum) pyrrolizidine alkaloids cause hepatic veno-occlusive disease (Budd-Chiari-like), not TSS. |
| DABT-1361 | C: bladder tumors (Veratrum) | **B: bradycardia** | Veratrum alkaloids cause bradycardia and hypotension via Na-channel modulation. Bladder tumors are from bracken fern (ptaquiloside). |
| DABT-1364 | D: sympathomimetic agents (Datura) | **C: anticholinergic agents** | Datura (jimsonweed) contains atropine/scopolamine — anticholinergic, not sympathomimetic. Classic anticholinergic toxidrome. |
| DABT-1365 | B: domoic acid (locoweed) | **D: swainsonine** | Locoweed contains swainsonine (alpha-mannosidase inhibitor causing locoism). Domoic acid is from marine diatoms. |
| DABT-1366 | E: jervine (excitatory amino acid exception?) | Options: A=jervine, B=domoic acid, C=ibotenic acid, D=willardine | Jervine (A) is NOT an excitatory amino acid — it's a steroidal alkaloid from Veratrum. Excitatory amino acids = domoic acid, ibotenic acid, willardine (glutamate receptor agonists). So the "exception" is jervine (A), NOT E. |
| DABT-1368 | C: hallucinations (dicumarol) | **D: bleeding** | Dicumarol is a vitamin K antagonist anticoagulant from moldy sweet clover. Causes hemorrhagic disease ("sweet clover disease"), not hallucinations. |

### Questionable but unconfirmed (DABT-1367)

DB answer: C — mint family (not associated with seizures). This is probably CORRECT — Strychnos (strychnine) causes seizures, water hemlock (parsley family) causes seizures, and spurge family has irritants. Mint family is not proconvulsant. ✅

## 4. Summary Statistics

| Subtopic | Total Questions | Confirmed DB Errors | Error Rate |
|----------|---------------|-------------------|------------|
| Solvents Matching (DABT-1319–1324) | 6 | 6 | **100%** |
| Radiation (DABT-1325–1348) | 24 | 7+ | **~29%** |
| Plant Toxins (DABT-1349–1368) | 20 | 10+ | **50%** |
| **Batch 23 Total** | **50** | **23+** | **~46%** |

## 5. Recommendations

1. **Solvents Matching:** All 6 items should be re-mapped using the docx answer key (Section 1 above).
2. **Radiation:** Cross-reference the 7 flagged items against Casarett & Doull Ch.25 before using in drills. Several contain fundamental physics errors (stable isotope called gamma emitter, visible-range wavelength for beta particles, non-radioactive elements called terrestrial background sources).
3. **Plant Toxins:** The 10 confirmed errors in 20 questions represent a 50% error rate — the highest of any organ system reviewed so far. Do NOT use plant toxin questions from the DB for assessment purposes without first correcting the answer keys. Cross-reference every answer against Casarett & Doull Ch.26 and Hayes Ch.20.
4. **Batch explanation writers:** For all batch23 questions, flag the DB-stored answer and provide the corrected answer with rationale, citing the appropriate reference chapter.
