# DABT Database Audit Report

**Database:** `/root/work/dabt/dabt-tutor/reference/data/dabt.db`
**Audit date:** 2026-05-20 01:59:17

---
## Baseline Statistics

- Total questions: **4841**
- Total answer options: **21063** (avg 4.4/Q)
- Total match_pairs: 205
- Source files: 7
  - [1] `DABT_Practice_Questions_Database.xlsx` — 446 questions
  - [2] `dabt_extract_2000q.csv` — 1801 questions
  - [3] `dabt_extract_chapter.csv` — 1119 questions
  - [4] `dabt_extract_mini.csv` — 208 questions
  - [5] `dabt_extract_topic.csv` — 145 questions
  - [6] `2008-2014_Compiled_Recert_Exams.xlsx` — 767 questions
  - [7] `various PDFs` — 355 questions

---
## Phase 1 — Structural Integrity

### 1.1 Questions with NULL/empty question_text
- PASS: No questions with NULL/empty question_text (0)

### 1.2 Questions with correct_answer_letter but NO answer_options
- 94 questions with correct_answer_letter but no answer_options
  - QDABT-0461: answer_letter='D', has_match_pairs=0, src=2
  - QDABT-0507: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0508: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0509: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-0510: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0511: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0512: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0513: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0514: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0523: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-0524: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0525: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0526: answer_letter='O', has_match_pairs=1, src=2
  - QDABT-0527: answer_letter='M', has_match_pairs=1, src=2
  - QDABT-0528: answer_letter='G', has_match_pairs=1, src=2
  - QDABT-0529: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-0530: answer_letter='J', has_match_pairs=1, src=2
  - QDABT-0581: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-0582: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0701: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0702: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-0703: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-0704: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-0705: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-0706: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0707: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-0708: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-0709: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0710: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-0814: answer_letter='B', has_match_pairs=0, src=2
  - QDABT-0962: answer_letter='B', has_match_pairs=0, src=2
  - QDABT-1040: answer_letter='C', has_match_pairs=0, src=2
  - QDABT-1092: answer_letter='B', has_match_pairs=0, src=2
  - QDABT-1167: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-1168: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-1169: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-1170: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-1249: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-1250: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1251: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1252: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1253: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1324: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-1348: answer_letter='D', has_match_pairs=0, src=2
  - QDABT-1432: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-1508: answer_letter='D', has_match_pairs=0, src=2
  - QDABT-1600: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1601: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-1602: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1603: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1604: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1605: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1606: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1607: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-1665: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1730: answer_letter='O', has_match_pairs=1, src=2
  - QDABT-1731: answer_letter='K', has_match_pairs=1, src=2
  - QDABT-1732: answer_letter='Q', has_match_pairs=1, src=2
  - QDABT-1733: answer_letter='J', has_match_pairs=1, src=2
  - QDABT-1734: answer_letter='H', has_match_pairs=1, src=2
  - QDABT-1735: answer_letter='I', has_match_pairs=1, src=2
  - QDABT-1736: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-1792: answer_letter='B', has_match_pairs=0, src=2
  - QDABT-1879: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1880: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1881: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1882: answer_letter='C', has_match_pairs=1, src=2
  - QDABT-1883: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1884: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1885: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-1886: answer_letter='A', has_match_pairs=1, src=2
  - QDABT-1887: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-1888: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1889: answer_letter='D', has_match_pairs=1, src=2
  - QDABT-1890: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-1891: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-1910: answer_letter='E', has_match_pairs=1, src=2
  - QDABT-1972: answer_letter='B', has_match_pairs=1, src=2
  - QDABT-2105: answer_letter='B', has_match_pairs=0, src=2
  - QDABT-2232: answer_letter='C', has_match_pairs=0, src=2
  - QDABT-2233: answer_letter='J', has_match_pairs=0, src=2
  - QDABT-2234: answer_letter='M', has_match_pairs=1, src=2
  - QDABT-2235: answer_letter='G', has_match_pairs=1, src=2
  - QDABT-2236: answer_letter='N', has_match_pairs=1, src=2
  - QDABT-2238: answer_letter='B', has_match_pairs=0, src=2
  - QDABT-2239: answer_letter='P', has_match_pairs=1, src=2
  - QDABT-2240: answer_letter='O', has_match_pairs=0, src=2
  - QDABT-2241: answer_letter='C', has_match_pairs=0, src=2
  - QDABT-2242: answer_letter='D', has_match_pairs=0, src=2
  - QDABT-2243: answer_letter='E', has_match_pairs=0, src=2
  - QDABT-2244: answer_letter='F', has_match_pairs=1, src=2
  - QDABT-2245: answer_letter='H', has_match_pairs=1, src=2
  - QDABT-2246: answer_letter='I', has_match_pairs=0, src=2
  - QDABT-2247: answer_letter='K', has_match_pairs=0, src=2
  - Of these: 76 have match_pairs, 18 have neither options nor match_pairs

### 1.3 Answer options with empty/NULL option_text
- FAIL: 2 answer options with empty/NULL option_text
  - AO#17129: QDABT-4051, letter=D, text='NULL'
  - AO#17130: QDABT-4051, letter=E, text='NULL'

### 1.4 Questions with NO domain assignment
- 127 questions with no domain assignment
  - QDABT-3750: source=2008-2014_Compiled_Recert_Exams.xlsx, text='Sodium saccharin has been shown to induce bladder tumors'
  - QDABT-3761: source=2008-2014_Compiled_Recert_Exams.xlsx, text='Which of the following is TRUE regarding retinoblastoma?'
  - QDABT-3776: source=2008-2014_Compiled_Recert_Exams.xlsx, text='Screening batteries to further evaluate neurobehavioral toxicity currently inclu'
  - QDABT-3779: source=2008-2014_Compiled_Recert_Exams.xlsx, text='Which of the following is associated with spina bifida in offspring of epileptic'
  - QDABT-3805: source=2008-2014_Compiled_Recert_Exams.xlsx, text='About 2% of Caucasians are deficient in the normal form of serum carboxylesteras'
  - QDABT-3814: source=2008-2014_Compiled_Recert_Exams.xlsx, text='All of the following are correctly paired as xenobiotic and toxic metabolite EXC'
  - QDABT-3834: source=2008-2014_Compiled_Recert_Exams.xlsx, text='As a first order process, after how many half-lives will 99% of a chemical be el'
  - QDABT-3846: source=2008-2014_Compiled_Recert_Exams.xlsx, text='Which of the following is the primary reason for using oximes (e.g., 2-PAM) to t'
  - QDABT-3874: source=2008-2014_Compiled_Recert_Exams.xlsx, text='The experimental unit in a Segment II teratology study for the purpose of statis'
  - QDABT-3897: source=2008-2014_Compiled_Recert_Exams.xlsx, text='Information from short-term studies useful in the design of subchronic toxicity '
  - **Investigation:**
    - `various PDFs`: 79 questions without domain
    - `2008-2014_Compiled_Recert_Exams.xlsx`: 48 questions without domain

### 1.5 Source file reference integrity
- PASS: All source_file_id values resolve to valid source_files

### 1.6 Orphan answer_options
- PASS: No orphan answer_options

### 1.7 Domain assignments completeness
- question_domains schema sample: {'id': 1, 'question_id': 'DABT-0001', 'domain': 'Domain IV', 'sub_domain': 'Applied', 'task': 'T11', 'confidence': 'medium'} | domain=Domain IV

- Domain distribution:
  - **Domain IV**: 2850 questions
  - **Domain I**: 981 questions
  - **Domain II**: 673 questions
  - **Domain III**: 210 questions

### 1.8 Topic distribution
- Topic distribution:
  - `General Principles & Concepts`: 447
  - `Drugs & Therapeutics – Toxicology`: 363
  - `General Toxicology`: 325
  - `Biotransformation / Metabolism`: 257
  - `Mechanisms of Toxicity`: 253
  - `Liver / Hepatotoxicity`: 233
  - `Comprehensive`: 208
  - `Metals & Metalloids`: 207
  - `Lung / Pulmonary Toxicity`: 204
  - `Immunotoxicology / Allergy`: 199
  - `Pesticides – Insecticides`: 197
  - `Nervous System / Neurotoxicity`: 194
  - `Kidney / Nephrotoxicity`: 174
  - `Carcinogenesis & Mutagenesis`: 168
  - `Reproductive & Developmental Toxicity`: 162
  - `Solvents & Hydrocarbons`: 155
  - `Hematology & Blood Toxicity`: 147
  - `Plant Toxins`: 145
  - `Risk Assessment & Regulatory`: 145
  - `Cardiovascular Toxicity`: 136
  - `Skin / Dermatotoxicity`: 136
  - `Toxicokinetics / ADME`: 125
  - `Eye / Ocular Toxicity`: 110
  - `Air Pollution & Particulates`: 100
  - `Endocrine Toxicology`: 95
  - `Cosmetics & GRAS`: 70
  - `Food Additives`: 70
  - `Food Additives, Cosmetics & GRAS`: 69
  - `Alcohols & Methanol/Ethanol`: 65
  - `Genotoxicity / DNA Damage`: 59
  - `Animal & Microbial Venoms / Toxins`: 43
  - `Gases – Asphyxiants & Irritants`: 37
  - `Radiation / UV / Ionizing`: 35
  - `Pesticides – Herbicides`: 11
  - `Mycotoxins`: 10
  - `Pesticides – Rodenticides`: 9
  - `Pesticides – Fumigants`: 6
  - `Pesticides – Fungicides`: 1

### 1.9 Questions without topic assignment
- 285 questions with no topic assignment
  - QDABT-3722: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3723: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3726: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3727: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3736: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3738: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3740: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3742: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3748: source=2008-2014_Compiled_Recert_Exams.xlsx
  - QDABT-3750: source=2008-2014_Compiled_Recert_Exams.xlsx

### 1.10 Additional structural findings

- Questions with NULL/empty correct_answer_letter: **1749** (36%)
- Questions with both options AND answer_letter: 2998 (62%)
- Questions with explanations: 1454

### 1.11 Option text truncation check

  - AO#72 QDABT-0015 B: 'the Delaney clause bans known carcinogens and mutagens as food additives...' (len=72)
  - AO#76 QDABT-0016 A: 'prohibited interstate commerce of misbranded and adulterated foods, drinks and d...' (len=84)
  - AO#102 QDABT-0021 B: 'has been incriminated as the causative agent in “beer drinkers” myopathy...' (len=72)
  - AO#131 QDABT-0027 A: 'formation of nitrosamine in the stomach from reaction of nitrite with amines...' (len=76)
  - AO#132 QDABT-0027 B: 'production of nitrogen dioxide in the lower bowel by bacterial oxidation of nitr...' (len=83)
- Options possibly truncated (end mid-word at ~80 char boundary): **at least 549**
  - The truncation appears to be a CSV field length limit during extraction

### 1.12 Answer letter distribution (non-standard)

  - `F`: 21 questions (matching test answer keys)
  - `G`: 13 questions (matching test answer keys)
  - `H`: 11 questions (matching test answer keys)
  - `J`: 4 questions (matching test answer keys)
  - `O`: 3 questions (matching test answer keys)
  - `N`: 3 questions (matching test answer keys)
  - `M`: 3 questions (matching test answer keys)
  - `K`: 3 questions (matching test answer keys)
  - `I`: 3 questions (matching test answer keys)
  - `Q`: 2 questions (matching test answer keys)
  - `P`: 2 questions (matching test answer keys)
  - `L`: 1 questions (matching test answer keys)
  - These non-standard letters (F,G,H,I,J,K,L,M,N,O,P,Q) are answer keys for matching/pairing questions


---
## Phase 2 — Answer Integrity Spot-Check

### 2.1 Random Sample Verification (30 questions)

  - **QDABT-1758** [dabt_extract_2000q.csv]: correct_answer='E' not in options ['A', 'B', 'C', 'D']
    Text: 'Aqueous pores are primarily involved in the transport of _____....'
    Options: A: 'small hydrophobic molecules', B: 'large hydrophobic molecules', C: 'small hydrophilic molecules', D: 'large hydrophilic molecules'
    Correct: E
  - **QDABT-0551** [dabt_extract_2000q.csv]: correct_answer='E' not in options ['A', 'B', 'C', 'D']
    Text: 'Hereditary differences in a single gene that occur in more than 1 % of the population are referred to as _____....'
    Options: A: 'significant mutations', B: 'dominant mutations', C: 'genetic polymorphisms', D: 'sister chromatid exchanges'
    Correct: E
  - **QDABT-0344** [DABT_Practice_Questions_Database.xlsx]: possibly truncated
    Text: 'Elevations of acid phosphatase are associated with tumors of:...'
    Options: A: 'chromaffin tissue', B: 'breast', C: 'testis', D: 'bladder', E: 'prostate'
    Correct: E
  - **QDABT-0356** [DABT_Practice_Questions_Database.xlsx]: possibly truncated
    Text: 'Single base pair transformations in the genome coding for a specific protein:...'
    Options: A: 'may alter protein structure', B: 'may not alter protein structure', C: 'may alter protein structure without altering funct', D: 'choices A and B are correct', E: 'all of the above are correct'
    Correct: E
  - **QDABT-0081** [DABT_Practice_Questions_Database.xlsx]: possibly truncated
    Text: 'All of the following are true in solvent abuse except:...'
    Options: A: 'The blood-brain barrier causes a significant delay', B: 'Almost 20% of eighth graders admit to abusing inha', C: 'There is a potential for dependence', D: 'Death can occur by cardiac arrhythmia'
    Correct: A
  - **QDABT-0304** [DABT_Practice_Questions_Database.xlsx]: possibly truncated
    Text: 'The primary type of tumor observed in workers occupationally exposed to vinyl chloride was:...'
    Options: A: 'squamous cell carcinoma of the bladder', B: 'hepatocellular carcinoma', C: 'neuroglioma', D: 'angiocarcinoma of the liver', E: 'carcinoma of the lung'
    Correct: D
  - **QDABT-1299** [dabt_extract_2000q.csv]: correct_answer='E' not in options ['A', 'B', 'C', 'D']
    Text: 'Hydrofluoroic acid exposure has been associated with _____....'
    Options: A: 'osteosarcoma', B: 'osteosclerosis', C: 'hepatitis', D: 'anemia'
    Correct: E
- WARN: 7/30 questions have issues

### 2.2 Past ABT Exams — Explanation/Answer verification (10 questions)

- Sampled 10 questions with explanations:

  - **QDABT-3301** [dabt_extract_chapter.csv]:
    Q: 'Which of the following statements about tick paralysis is correct?...'
    Options: A: Improvement often occurs rapidly after the entire tick is re, B: The tick must be on the skin for 2- 3 hours before disease w, C: Absent deep tendon reflexes at 6 hours after envenomation is, D: Calcium gluconate will effectively reverse muscle weakness, E: Boys get tick paralysis more commonly than girls
    Correct answer: A
    Explanation (first 200 chars): 'Improvement in paralysis often occurs after the entire tick is removed from the skin. The tick must remain on the person for 5-8 days before symptoms occur. Young girls are reported to develop tick pa...'
    OK: Explanation justifies answer

  - **QDABT-3884** [2008-2014_Compiled_Recert_Exams.xlsx]:
    Q: 'A gender-related susceptibility to nephrotoxicity is NOT characteristic of which of the following
ag...'
    Options: A: cyclosporin A, B: acetaminophen (paracetamol), C: chloroform, D: d-limonene, E: hexachlorobutadiene
    Correct answer: E
    Explanation (first 200 chars): 'Cyclosporin A (Sandimmune, CsA) is a cyclic undecapeptide isolated from fungal organisms found in the soil. Important to its use as an immunosuppressant is the relative lack of secondary toxicity (e.g...'
    OK: Explanation justifies answer

  - **QDABT-4449** [2008-2014_Compiled_Recert_Exams.xlsx]:
    Q: 'Reticulocytosis following high therapeutic daily doses of a drug would MOST likely be due to which
o...'
    Options: A: a drug-induced normal physiologic response, B: drug-induced polycythemia, C: drug-induced red blood cell loss, D: drug-induced aplastic anemia, E: drug induced edema
    Correct answer: None
    Explanation (first 200 chars): 'C...'
    WARN: Explanation may NOT directly justify 'None'

  - **QDABT-0199** [DABT_Practice_Questions_Database.xlsx]:
    Q: 'During a thirteen-week repeated dose study in rats with an E. coli derived recombinant protein, the ...'
    Options: A: elicitation of type III hypersensitivity, B: IgE mediated anaphylaxis, C: inactivation of the protein by a non-specific peptidase, D: formation of autoantibodies, E: formation of neutralizing antibodies
    Correct answer: E
    Explanation (first 200 chars): '*A Neutralizing antibody, or NAb is an antibody which defends a cell from an antigen or infectious body by inhibiting or neutralizing any effect it has biologically. An example of a neutralizing antib...'
    OK: Explanation justifies answer

  - **QDABT-2530** [dabt_extract_chapter.csv]:
    Q: 'Metallic and inorganic forms of compound “X” are relatively nontoxic. Inorganic forms of compound X ...'
    Options: A: methyl mercury, B: trimethyltin, C: dimethyl arsenic acid, D: trimethyl arsenic oxide
    Correct answer: D
    Explanation (first 200 chars): 'Ingestion of food items contaminated with high levels of inorganic tins may cause acute gastroenteritis, while chronic inhalation of inorganic tins (e.g., stannic oxide dust or fumes) may lead to beni...'
    OK: Explanation justifies answer

  - **QDABT-2614** [dabt_extract_chapter.csv]:
    Q: 'Which of the following characteristically causes vertical nystagmus?...'
    Options: A: Carbamazepine, B: Phenytoin, C: Phencyclidine, D: Ethanol, E: Diazepam
    Correct answer: C
    Explanation (first 200 chars): 'Each of the others causes nystagmus, which is almost always horizontal in character. Among them, however, only phencyclidine is typically associated with vertical nystagmus....'
    OK: Explanation justifies answer

  - **QDABT-2763** [dabt_extract_chapter.csv]:
    Q: 'Vitamin D from the diet or dermal synthesis from sunlight is biologically inactive; activation requi...'
    Options: A: cholecalciferol/calcidiol, B: calcitriol/calcidiol, C: calcidiol/calcitriol, D: calcidiol/cholecalciferol
    Correct answer: A
    Explanation (first 200 chars): 'Cholecalciferol (vitamin D3) is one of the five forms of vitamin D. It is a secosteroid, that is, a steroid molecule with one ring open. Cholecalciferol is inactive: it is converted to its active form...'
    OK: Explanation justifies answer

  - **QDABT-3880** [2008-2014_Compiled_Recert_Exams.xlsx]:
    Q: 'In a rat reproduction study, treatment-related findings were limited to significantly reduced body w...'
    Options: A: estrogen agonism, B: androgen agonism, C: inhibition of 5-alpha-reductase, D: delayed growth in both sexes, E: disruption of negative feedback to the hypothalamus and pitu
    Correct answer: D
    Explanation (first 200 chars): 'estrogen agonism (would affect vaginal opening only)
B) androgen agonism (would affect preputial separation only)
C) inhibition of 5 alpha-reductase (would affect preputial separation only; 5α-reducta...'
    OK: Explanation justifies answer

  - **QDABT-2444** [dabt_extract_chapter.csv]:
    Q: 'The proximal tubule is the most common site of toxicant-induced renal injury. The reasons for this r...'
    Options: A: 2,4,4-trimethylpentane, B: d-limonene, C: cisplatin, D: ochratoxin, E: all of the above, F: A, B, and C, G: B, C, and D
    Correct answer: D
    Explanation (first 200 chars): 'Ochratoxin damages the proximal tubule, but it is classified as a toxin, not a toxicant....'
    OK: Explanation justifies answer

  - **QDABT-0172** [DABT_Practice_Questions_Database.xlsx]:
    Q: 'Which of the following agents exerts its primary nephrotoxic effects on the glomerulus?...'
    Options: A: phenacetin, B: amphotericin B, C: cyclosporine, D: mercuric chloride, E: potassium bichromate
    Correct answer: C
    Explanation (first 200 chars): 'Other notes — E: The glomerulus is the primary site for immune complexes. (p. 593) Chemically induced glomerular injury may also be mediated by extrarenal factors. Circulating immune complexes may be ...'
    OK: Explanation justifies answer

### 2.3 PDF-Extracted Questions — Parsing Quality Check

  Sampling 20 PDF-extracted questions (source ID 7 = various PDFs):
  - QDABT-4711 [PDF]: OK
  - QDABT-4661 [PDF]: OK
  - QDABT-4680 [PDF]: OK
  - QDABT-4660 [PDF]: OK
  - QDABT-4828 [PDF]: OK
  - QDABT-4584 [PDF]: OK
  - QDABT-4655 [PDF]: OK
  - QDABT-4740 [PDF]: OK
  - QDABT-4812 [PDF]: OK
  - QDABT-4763 [PDF]: OK
  - QDABT-4762 [PDF]: OK
  - QDABT-4806 [PDF]: OK
  - QDABT-4595 [PDF]: OK
  - QDABT-4535 [PDF]: OK
  - QDABT-4506 [PDF]: OK
  - QDABT-4508 [PDF]: OK
  - QDABT-4533 [PDF]: OK
  - QDABT-4781 [PDF]: OK
  - QDABT-4718 [PDF]: OK
  - QDABT-4811 [PDF]: OK
  - PDF parsing issues: 0/20

---
## Phase 3 — Matching Tests

- Total match_pairs entries: 205
- Questions with match_pairs: 205
- Questions with NEITHER options NOR match_pairs (BROKEN): **43**
  - Listing broken questions:
    - QDABT-0461 [dabt_extract_2000q.csv]: answer='D' text='In a decomposed or embalmed body, the specimen to use to measure an alcohol level that would best co'
    - QDABT-0814 [dabt_extract_2000q.csv]: answer='B' text='Which of the following is the correct toxicant-target organ pair?'
    - QDABT-0962 [dabt_extract_2000q.csv]: answer='B' text='Styrene has been associated with _____.'
    - QDABT-1040 [dabt_extract_2000q.csv]: answer='C' text='The phthalate syndrome in rats includes all of the following except _____.'
    - QDABT-1092 [dabt_extract_2000q.csv]: answer='B' text='All of the following are true of raloxifene except _____.'
    - QDABT-1348 [dabt_extract_2000q.csv]: answer='D' text='The term-effective dose of ionizing radiation _____.'
    - QDABT-1508 [dabt_extract_2000q.csv]: answer='D' text='The microgram mass of a toxin in an organism per kilogram of lipid divided by the microgram mass of '
    - QDABT-1792 [dabt_extract_2000q.csv]: answer='B' text='Which one of the following statements is true with respect to absorption of a toxicant through the s'
    - QDABT-2105 [dabt_extract_2000q.csv]: answer='B' text='A threshold for toxicity is assumed for all of the following toxicants except _____.'
    - QDABT-2232 [dabt_extract_2000q.csv]: answer='C' text='Patients with significant caustic ingestion are at an increased risk of all of the following except '
    - QDABT-2233 [dabt_extract_2000q.csv]: answer='J' text='sulfanilamide disaster 1937 A. hydrogen sulfide'
    - QDABT-2238 [dabt_extract_2000q.csv]: answer='B' text='Turkey, 1956 F. L-tryptophan eosinophilia- myalgia syndrome'
    - QDABT-2240 [dabt_extract_2000q.csv]: answer='O' text='Minamata Bay, Japan, 1950s H. thalidomide'
    - QDABT-2241 [dabt_extract_2000q.csv]: answer='C' text='Japan, 1968 I. China white epidemic'
    - QDABT-2242 [dabt_extract_2000q.csv]: answer='D' text='Chicago, United States, 1982 J. ethylene glycol'
    - QDABT-2243 [dabt_extract_2000q.csv]: answer='E' text='Chernobyl, Ukrane, 1986 K. Ginger Jake paralysis'
    - QDABT-2246 [dabt_extract_2000q.csv]: answer='I' text='Pittsburgh, United States, 1988 N. dioxin'
    - QDABT-2247 [dabt_extract_2000q.csv]: answer='K' text='United States, 1930-1931 O. methylmercury 2000. San Jose, United States,'
    - QDABT-3020 [dabt_extract_chapter.csv]: answer='None' text='The biotransformation of xenobiotics is catalyzed by various enzyme systems that can be divided into'
    - QDABT-3575 [dabt_extract_topic.csv]: answer='None' text='Birds are uniquely at high risk of lead poisoning because'

- Questions without correct_answer_letter but WITH answer_options: 1724
- Questions without answer_letter but WITH match_pairs: 0
- Questions without answer_letter, no options, no match_pairs: **25**

### Match Pairs Integrity Check

- Orphan match_pairs (referencing non-existent questions): 0
- Sample match_pairs (10 random):
  - QDABT-1969: term='mercury' match='D'
    Context: 'mercury'
  - QDABT-0526: term='flumazenil' match='O'
    Context: 'flumazenil'
  - QDABT-0578: term='STEPS' match='B'
    Context: 'STEPS'
  - QDABT-1425: term='water hemlock' match='A'
    Context: 'water hemlock'
  - QDABT-1970: term='particulate matter' match='C'
    Context: 'particulate matter'
  - QDABT-1971: term='arsenic' match='A'
    Context: 'arsenic'
  - QDABT-0869: term='oxides of nitrogen' match='B'
    Context: 'oxides of nitrogen'
  - QDABT-0767: term='gamma glutamyl transpeptidase' match='B'
    Context: 'gamma glutamyl transpeptidase'
  - QDABT-1320: term='chromic acid' match='D'
    Context: 'chromic acid'
  - QDABT-1729: term='arsine' match='A'
    Context: 'arsine'

---
## Phase 4 — Domain III (Risk Assessment) Deep-Dive

- Total questions classified as Domain III: 210
- Domain III name variants used:
  - 'Domain III': 210 questions

### Sampling 20 Domain III questions for verification

  - **QDABT-4254** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Genomic biomarkers can play an important role in identifying responders and non-responders, avoiding toxicity and adjust...'
    Correct: None | Options: OK
    Risk keywords found: population, risk, assessment

  - **QDABT-0403** [DABT_Practice_Questions_Database.xlsx]
    Domain: Domain III | Topic: Biotransformation / Metabolism
    Q: 'Biological activity of the methylenedioxyphenyl class of insecticide synergists (piperonyl butoxide):...'
    Correct: D | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-4059** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: N/A
    Q: 'Which of the following is MOST commonly used in the treatment of anticholinesterase poisoning?...'
    Correct: E | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-3711** [dabt_extract_topic.csv]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Which of the following are used by the World Health Organization for pesticides and food additives to define “the daily ...'
    Correct: A | Options: OK
    Risk keywords found: RfD, TDI

  - **QDABT-4758** [various PDFs]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Which of the following should be considered as a
first choice for controlling workplace hazards?...'
    Correct: None | Options: OK
    Risk keywords found: hazard

  - **QDABT-3907** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Occupational exposure to nerve agents can cause all of the following EXCEPT...'
    Correct: None | Options: OK
    Risk keywords found: exposure

  - **QDABT-0137** [DABT_Practice_Questions_Database.xlsx]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Which of the following steps is NOT deemed critical to the process of risk assessment?...'
    Correct: E | Options: OK
    Risk keywords found: risk management, characterization, dose-response, assessment, exposure

  - **QDABT-4643** [various PDFs]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'A risk quotient (RQ) is a deterministic approach
for evaluating a point estimate of exposure with a
point estimate of ef...'
    Correct: None | Options: OK
    Risk keywords found: RfD, risk, exposure

  - **QDABT-4083** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: N/A
    Q: '39. The greatest food-borne risk facing consumers in most of the world is...'
    Correct: B | Options: OK
    Risk keywords found: risk

  - **QDABT-0434** [DABT_Practice_Questions_Database.xlsx]
    Domain: Domain III | Topic: Mycotoxins
    Q: 'Chemically induced glomerular injury may also be mediated by extrarenal factors.  Circulating immune complexes may be tr...'
    Correct: A | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-3828** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: N/A
    Q: 'Which of the following is NOT CORRECT regarding epidemiological studies?...'
    Correct: B | Options: OK
    Risk keywords found: population, hazard, risk

  - **QDABT-4363** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: N/A
    Q: 'Which of the following would be expected to be the most effective treatment for protecting against
systemic effects from...'
    Correct: C | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-2102** [dabt_extract_2000q.csv]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'On a dose-response curve, the lowest dose tested with a statistically significant effect is _____....'
    Correct: A | Options: OK
    Risk keywords found: dose-response, reference dose, NOAEL, LOAEL

  - **QDABT-4331** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Which of the following BEST characterizes the findings of toxic response to in utero exposure to
ethanol?...'
    Correct: C | Options: OK
    Risk keywords found: exposure

  - **QDABT-3928** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Acrodynia (pink disease), characterized by erythema of the extremities, chest and face with photophobia, diaphoresis, an...'
    Correct: None | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-0311** [DABT_Practice_Questions_Database.xlsx]
    Domain: Domain III | Topic: Pesticides – Herbicides
    Q: 'All of the following are capable of accepting electrons from reductases and forming radicals except ___·...'
    Correct: C | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-0234** [DABT_Practice_Questions_Database.xlsx]
    Domain: Domain III | Topic: Immunotoxicology / Allergy
    Q: 'Dermal delayed hypersensitivity reactions are mediated by:...'
    Correct: C | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-2092** [dabt_extract_2000q.csv]
    Domain: Domain III | Topic: Risk Assessment & Regulatory
    Q: 'Body weights of a 21-year-old male will follow a __________ distribution....'
    Correct: A | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-0383** [DABT_Practice_Questions_Database.xlsx]
    Domain: Domain III | Topic: Immunotoxicology / Allergy
    Q: 'Type III hypersensitivity reactions are mediated by...'
    Correct: D | Options: OK
    **WARNING**: No risk-related keywords detected -- possible miscategorization

  - **QDABT-3817** [2008-2014_Compiled_Recert_Exams.xlsx]
    Domain: Domain III | Topic: N/A
    Q: 'A prominent application of structure-activity relationships for assessment of risks associated with 2,3,7,8-tetrachlorod...'
    Correct: A | Options: OK
    Risk keywords found: risk, assessment

- Domain III Spot-Check Summary:
  - Questions sampled: 20
  - Issues found: 0

---
## Phase 5 — Topic Distribution Analysis

### 5.1 Topic Count Summary
- Total topic assignments: 5370
- Unique topics: 38
- Average Qs per topic: 141.3

### 5.2 Topics with very few questions (<=3)
  - `Pesticides – Fungicides`: 1 questions

### 5.3 Potential catch-all topics
  - `General Principles & Concepts`: 447 questions (8.3% of total)
  - `General Toxicology`: 325 questions (6.1% of total)

### 5.4 Key DABT exam topics presence check

  - `Carcinogenesis & Mutagenesis`: 168 questions OK
  - `Carcinogenesis & Mutagenesis`: 168 questions OK
  - `genetic toxicology`: **0** questions -- possible gap
  - `developmental toxicology`: **0** questions -- possible gap
  - `reproductive toxicology`: **0** questions -- possible gap
  - `neurotoxicology`: **0** questions -- possible gap
  - `Immunotoxicology / Allergy`: 199 questions OK
  - `Toxicokinetics / ADME`: 125 questions OK
  - `biostatistics`: **0** questions -- possible gap
  - `ecotoxicology`: **0** questions -- possible gap
  - `forensic toxicology`: **0** questions -- possible gap
  - `clinical toxicology`: **0** questions -- possible gap
  - `regulatory toxicology`: **0** questions -- possible gap
  - `Metals & Metalloids`: 207 questions OK
  - `Pesticides – Insecticides`: 197 questions OK
  - `Solvents & Hydrocarbons`: 155 questions OK
  - `nanotoxicology`: **0** questions -- possible gap
  - `food toxicology`: **0** questions -- possible gap
  - `in vitro`: **0** questions -- possible gap
  - `alternative methods`: **0** questions -- possible gap
  - `Toxicokinetics / ADME`: 125 questions OK
  - `pharmacokinetics`: **0** questions -- possible gap
  - `Biotransformation / Metabolism`: 257 questions OK
  - `Risk Assessment & Regulatory`: 145 questions OK
  - `exposure assessment`: **0** questions -- possible gap
  - `dose-response`: **0** questions -- possible gap
  - `hazard identification`: **0** questions -- possible gap
  - `dermal toxicology`: **0** questions -- possible gap
  - `inhalation toxicology`: **0** questions -- possible gap
  - `target organ`: **0** questions -- possible gap
  - `Liver / Hepatotoxicity`: 233 questions OK
  - `Kidney / Nephrotoxicity`: 174 questions OK

---
## Audit Summary

| Phase | Result | Notes |
|-------|--------|-------|
| Phase 1 -- Structural Integrity | **WARN** | 1749 Qs no answer_letter; 21063 K answer options; 549 opt truncation; 43 broken Qs; 2 empty options; 127 Qs without domain |
| Phase 2 -- Answer Integrity | **FAIL** | 7/30 sample issues |
| Phase 3 -- Matching Tests | **FAIL** | 205 pairs, 205 linked Qs; 43 broken Qs |
| Phase 4 -- Domain III | **PASS** | 210 D3 Qs, 0 issues in 20 sampled |
| Phase 5 -- Topic Distribution | **WARN** | 38 unique topics; 1 topics with <=3 Qs; 20 key exam topics missing |

---
## Recommended Fixes

1. **Fix 43 broken questions** -- add answer_options or match_pairs entries, or delete these records
   - Broken question IDs: DABT-0461, DABT-0814, DABT-0962, DABT-1040, DABT-1092, DABT-1348, DABT-1508, DABT-1792, DABT-2105, DABT-2232, DABT-2233, DABT-2238, DABT-2240, DABT-2241, DABT-2242, DABT-2243, DABT-2246, DABT-2247, DABT-3020, DABT-3575, DABT-3576, DABT-3577, DABT-3578, DABT-3579, DABT-3580, DABT-3581, DABT-3582, DABT-3583, DABT-3584, DABT-3585, DABT-3586, DABT-3587, DABT-3588, DABT-3589, DABT-3590, DABT-3591, DABT-3592, DABT-3593, DABT-3594, DABT-3595, DABT-3596, DABT-3597, DABT-3934

2. **Assign domains to 127 unclassified questions** -- priority since domain distribution affects exam prep
   - Unclassified question IDs (first 50): DABT-3750, DABT-3761, DABT-3776, DABT-3779, DABT-3805, DABT-3814, DABT-3834, DABT-3846, DABT-3874, DABT-3897, DABT-3911, DABT-3921, DABT-3960, DABT-4010, DABT-4012, DABT-4025, DABT-4027, DABT-4037, DABT-4041, DABT-4042, DABT-4043, DABT-4049, DABT-4084, DABT-4089, DABT-4091, DABT-4113, DABT-4148, DABT-4151, DABT-4177, DABT-4264, DABT-4290, DABT-4315, DABT-4338, DABT-4346, DABT-4357, DABT-4378, DABT-4379, DABT-4394, DABT-4404, DABT-4419, DABT-4420, DABT-4438, DABT-4444, DABT-4455, DABT-4469, DABT-4473, DABT-4475, DABT-4476, DABT-4489, DABT-4491

3. **Populate 2 empty answer options** -- or delete them if they're placeholders

5. **Expand thin topics** -- the following topics have very few questions:
   - `Pesticides – Fungicides`: only 1 question(s)

6. **Fill content gaps** -- missing key exam topics:
   - `genetic toxicology`
   - `developmental toxicology`
   - `reproductive toxicology`
   - `neurotoxicology`
   - `biostatistics`
   - `ecotoxicology`
   - `forensic toxicology`
   - `clinical toxicology`
   - `regulatory toxicology`
   - `nanotoxicology`
   - `food toxicology`
   - `in vitro`
   - `alternative methods`
   - `pharmacokinetics`
   - `exposure assessment`
   - `dose-response`
   - `hazard identification`
   - `dermal toxicology`
   - `inhalation toxicology`
   - `target organ`

---
## Questions Needing Human Review

- **QDABT-0461**: Broken: no options, no match_pairs
  Text: 'In a decomposed or embalmed body, the specimen to use to measure an alcohol level that would best co...'
- **QDABT-0814**: Broken: no options, no match_pairs
  Text: 'Which of the following is the correct toxicant-target organ pair?...'
- **QDABT-0962**: Broken: no options, no match_pairs
  Text: 'Styrene has been associated with _____....'
- **QDABT-1040**: Broken: no options, no match_pairs
  Text: 'The phthalate syndrome in rats includes all of the following except _____....'
- **QDABT-1092**: Broken: no options, no match_pairs
  Text: 'All of the following are true of raloxifene except _____....'
- **QDABT-1348**: Broken: no options, no match_pairs
  Text: 'The term-effective dose of ionizing radiation _____....'
- **QDABT-1508**: Broken: no options, no match_pairs
  Text: 'The microgram mass of a toxin in an organism per kilogram of lipid divided by the microgram mass of ...'
- **QDABT-1792**: Broken: no options, no match_pairs
  Text: 'Which one of the following statements is true with respect to absorption of a toxicant through the s...'
- **QDABT-2105**: Broken: no options, no match_pairs
  Text: 'A threshold for toxicity is assumed for all of the following toxicants except _____....'
- **QDABT-2232**: Broken: no options, no match_pairs
  Text: 'Patients with significant caustic ingestion are at an increased risk of all of the following except ...'
- **QDABT-2233**: Broken: no options, no match_pairs
  Text: 'sulfanilamide disaster 1937 A. hydrogen sulfide...'
- **QDABT-2238**: Broken: no options, no match_pairs
  Text: 'Turkey, 1956 F. L-tryptophan eosinophilia- myalgia syndrome...'
- **QDABT-2240**: Broken: no options, no match_pairs
  Text: 'Minamata Bay, Japan, 1950s H. thalidomide...'
- **QDABT-2241**: Broken: no options, no match_pairs
  Text: 'Japan, 1968 I. China white epidemic...'
- **QDABT-2242**: Broken: no options, no match_pairs
  Text: 'Chicago, United States, 1982 J. ethylene glycol...'
- **QDABT-2243**: Broken: no options, no match_pairs
  Text: 'Chernobyl, Ukrane, 1986 K. Ginger Jake paralysis...'
- **QDABT-2246**: Broken: no options, no match_pairs
  Text: 'Pittsburgh, United States, 1988 N. dioxin...'
- **QDABT-2247**: Broken: no options, no match_pairs
  Text: 'United States, 1930-1931 O. methylmercury 2000. San Jose, United States,...'
- **QDABT-3020**: Broken: no options, no match_pairs
  Text: 'The biotransformation of xenobiotics is catalyzed by various enzyme systems that can be divided into...'
- **QDABT-3575**: Broken: no options, no match_pairs
  Text: 'Birds are uniquely at high risk of lead poisoning because...'
- **QDABT-3576**: Broken: no options, no match_pairs
  Text: 'The free ion activity model (FIAM) states that...'
- **QDABT-3577**: Broken: no options, no match_pairs
  Text: 'Movement of NON-IONIC organic compounds across gut or gills is strongly influenced by...'
- **QDABT-3578**: Broken: no options, no match_pairs
  Text: 'Policies and regulations surrounding chemical effects in natural ecosystems are designed to...'
- **QDABT-3579**: Broken: no options, no match_pairs
  Text: 'Ligands of this receptor(s) have been extensively studied in the context of ecotoxicology because of...'
- **QDABT-3580**: Broken: no options, no match_pairs
  Text: 'Movement of IONIC organic compounds across gut or gills is strongly influenced by...'
- **QDABT-3581**: Broken: no options, no match_pairs
  Text: 'Ligands of this receptor upregulate many enzymes involved in metabolism of lipophilic xenobiotics an...'
- **QDABT-3582**: Broken: no options, no match_pairs
  Text: 'Granular formulations of these chemicals may be ingested by birds mistaking them for seed or grit...'
- **QDABT-3583**: Broken: no options, no match_pairs
  Text: 'Not an environmental ligand of the aryl hydrocarbon receptor...'
- **QDABT-3584**: Broken: no options, no match_pairs
  Text: 'Determines bioavailability of metal dissolved in surface waters...'
- **QDABT-3585**: Broken: no options, no match_pairs
  Text: 'Aquatic animals are especially sensitive to this toxicant/sources...'
- **QDABT-3586**: Broken: no options, no match_pairs
  Text: 'Not a mechanism by which environmental chemicals enhance reactive oxygen species production...'
- **QDABT-3587**: Broken: no options, no match_pairs
  Text: 'Not a redox cycling environmental contaminant...'
- **QDABT-3588**: Broken: no options, no match_pairs
  Text: 'The most widely studied form of cancer-causing mechanism studied in ecotoxicology...'
- **QDABT-3589**: Broken: no options, no match_pairs
  Text: 'Not true about cellular or organ targets in ecotoxicology...'
- **QDABT-3590**: Broken: no options, no match_pairs
  Text: 'Elevated micronuclei number has been observed in these after exposure to environmental contaminants...'
- **QDABT-3591**: Broken: no options, no match_pairs
  Text: 'Hydrocarbons associated with all of these sources affect fish development, except...'
- **QDABT-3592**: Broken: no options, no match_pairs
  Text: 'Not true about "blue sac disease"...'
- **QDABT-3593**: Broken: no options, no match_pairs
  Text: 'Wrong pairing of chemical that impacts the immune system of animals in lab experiments...'
- **QDABT-3594**: Broken: no options, no match_pairs
  Text: 'Not true about the effects of toxicants on fish behavior...'
- **QDABT-3595**: Broken: no options, no match_pairs
  Text: 'Exposure to this leads to loss of neurons in the peripheral mechanosensory system of zebrafish and a...'
- **QDABT-3596**: Broken: no options, no match_pairs
  Text: 'Since cancer occurs largely in older animals, it is likely to impact population dynamics and ecologi...'
- **QDABT-3597**: Broken: no options, no match_pairs
  Text: 'The following benthic fish exhibit the highest cancer rates in polluted systems EXCEPT...'
- **QDABT-3750**: No domain assigned
  Text: 'Sodium saccharin has been shown to induce bladder tumors...'
- **QDABT-3761**: No domain assigned
  Text: 'Which of the following is TRUE regarding retinoblastoma?...'
- **QDABT-3776**: No domain assigned
  Text: 'Screening batteries to further evaluate neurobehavioral toxicity currently include...'
- **QDABT-3779**: No domain assigned
  Text: 'Which of the following is associated with spina bifida in offspring of epileptic women?...'
- **QDABT-3805**: No domain assigned
  Text: 'About 2% of Caucasians are deficient in the normal form of serum carboxylesterase. This is an
import...'
- **QDABT-3814**: No domain assigned
  Text: 'All of the following are correctly paired as xenobiotic and toxic metabolite EXCEPT...'
- **QDABT-3834**: No domain assigned
  Text: 'As a first order process, after how many half-lives will 99% of a chemical be eliminated?...'
- **QDABT-3846**: No domain assigned
  Text: 'Which of the following is the primary reason for using oximes (e.g., 2-PAM) to treat anticholinester...'
- **QDABT-3874**: No domain assigned
  Text: 'The experimental unit in a Segment II teratology study for the purpose of statistical analysis is...'
- **QDABT-3897**: No domain assigned
  Text: 'Information from short-term studies useful in the design of subchronic toxicity studies does NOT inc...'
- **QDABT-3911**: No domain assigned
  Text: 'Which of the following is CORRECT regarding Good Iaboratory Practices?...'
- **QDABT-3921**: No domain assigned
  Text: 'Which for the following statements is CORRECT regarding the coefficient of variation (CV)?...'
- **QDABT-3934**: Broken: no options, no match_pairs
  Text: 'Itai Itai disease- Osteomalacia and osteoporesis in japanese women fed with Cadmium contaminated ric...'
- **QDABT-3960**: No domain assigned
  Text: 'The characteristic best attributable to ultrafine (less than 0.1 micron) particles as compared to fi...'
- **QDABT-4010**: No domain assigned
  Text: 'The two-compartment pharmacokinetic model is ideally suited for chemicals that...'
- **QDABT-4012**: No domain assigned
  Text: 'Which of the following is NOT CORRECT regarding the indirect acting sympathomimetic tyramine...'
- **QDABT-4025**: No domain assigned
  Text: 'Which of the following statements BEST characterizes the environmental behavior of a substance?...'
- **QDABT-4027**: No domain assigned
  Text: 'Which of the following best describes prevalence of a disease?...'
- **QDABT-4037**: No domain assigned
  Text: 'The duty of an "expert" in a court of law might include...'
- **QDABT-4041**: No domain assigned
  Text: 'Which of the following is CORRECT regarding the maximum tolerated dose used in chronic toxicity stud...'
- **QDABT-4042**: No domain assigned
  Text: 'Epigenetics can be described as...'
- **QDABT-4043**: No domain assigned
  Text: 'Which of the following is CORRECT regarding genomic and proteomic approaches to identify the genes i...'
- **QDABT-4049**: No domain assigned
  Text: 'Which of the following sets of elements are essential nutrients?...'
- **QDABT-4084**: No domain assigned
  Text: 'Which of the following is the primary psychoactive analyte of marijuana?...'
- **QDABT-4089**: No domain assigned
  Text: 'Which of the following endpoints are measured in the dominant lethal assay?...'
- **QDABT-4091**: No domain assigned
  Text: 'Reduced litter size can result from which of the following?...'
- **QDABT-4113**: No domain assigned
  Text: 'Kupffer cells and microglia cells are cellular components of the body's innate immunity. These cells...'
- **QDABT-4148**: No domain assigned
  Text: 'In the United States, National Ambient Air Quality Standards (NAAQS) have been set for all of the fo...'
- **QDABT-4151**: No domain assigned
  Text: 'The dose received by a worker exposed to a chemical handled in the workplace depends on all of
the f...'
- **QDABT-4177**: No domain assigned
  Text: 'Metam sodium is a soil fumigant whose toxic action toward soil nematodes, fungi and weed seeds is du...'
- **QDABT-4264**: No domain assigned
  Text: 'Which of the following is NOT CORRECT regarding epidemiologic studies of human cancer?...'
- **QDABT-4290**: No domain assigned
  Text: 'Which of the following is CORRECT regarding insect-resistant corn?...'
- **QDABT-4315**: No domain assigned
  Text: 'Which of the following is a specific antidote for benzodiazepine overdose?...'
- **QDABT-4338**: No domain assigned
  Text: 'Phagocytic cells that are part of the innate immune system of mammals include which of the following...'
- **QDABT-4346**: No domain assigned
  Text: 'The murine local lymph node assay is BEST described by which of the following?...'
- **QDABT-4357**: No domain assigned
  Text: 'Calculate the achieved dosage in mg/kg/day of a chemical fed to rats at a concentration of 0.5% (500...'
- **QDABT-4378**: No domain assigned
  Text: 'According to Good Laboratory Practices (21 CFR 58) reagents must be labeled with which of the
follow...'
- **QDABT-4379**: No domain assigned
  Text: 'In vitro assays for photoreactivity (e.g. reactive oxygen species, ROS) and phototoxicity (e.g. Neut...'
- **QDABT-4394**: No domain assigned
  Text: 'Which of the following associations (toxic syndromes -classic clinical features) is NOT correct?...'
- **QDABT-4404**: No domain assigned
  Text: 'Which of the following compounds has the highest potential for biomagnification?...'
- **QDABT-4419**: No domain assigned
  Text: 'Which of the following is NOT TRUE of an adverse reaction to food or food ingredients?...'
- **QDABT-4420**: No domain assigned
  Text: 'Which of the following is NOT correctly matched with its commonly observed idosyncratic food
reactio...'
- **QDABT-4438**: No domain assigned
  Text: 'Which of the following is NOT CORREC regarding hormesis?...'
- **QDABT-4444**: No domain assigned
  Text: 'An increase in abnormal sperm morphology indicates that a toxic agent has gained access to which
of ...'
- **QDABT-4455**: No domain assigned
  Text: 'Which of the following is the Comet Assay used for?...'
- **QDABT-4469**: No domain assigned
  Text: 'Which of the following is NOT CORRECT as per as necrossis is concerned?...'
- **QDABT-4473**: No domain assigned
  Text: 'Administration of a substance to rats produces the following clinical signs: salivation, miosis,
chr...'
- **QDABT-4475**: No domain assigned
  Text: 'Registration, Evaluation and Authorisation of Chemicals (REACH) is a chemical registration
programme...'
- **QDABT-4476**: No domain assigned
  Text: 'Which of the following combinations of gene promoter and tissue type would be appropriate to
create ...'
- **QDABT-4489**: No domain assigned
  Text: 'Which of the following is indicated to further evaluate the etiology of his mild transaminitis?...'
- **QDABT-4491**: No domain assigned
  Text: 'Which of the following is not considered a part of the metabolic syndrome?...'
- **QDABT-4494**: No domain assigned
  Text: 'You recommend exercise and weight loss for your patient; however,
he is interested in pharmacotherap...'
- **QDABT-4495**: No domain assigned
  Text: 'Your patient asks you about the natural history of NAFLD. Which of the
following statements is Answe...'
- **QDABT-4496**: No domain assigned
  Text: 'Bisphenol A is considered a chemical of concern
due to which of the following?...'
- **QDABT-4497**: No domain assigned
  Text: 'reagents must be labeled with which of the
following?...'
- **QDABT-4512**: No domain assigned
  Text: 'Which of the following chemicals bind
acetylcholinesterase in a rapidly reversible manner?...'
- **QDABT-4518**: No domain assigned
  Text: 'All of the following characteristics are factors in
the toxicity of inhaled nanoparticles relative t...'
- **QDABT-4521**: No domain assigned
  Text: 'What range BEST defines the size constituting
the definition of a nanoparticle?...'
- **QDABT-4522**: No domain assigned
  Text: 'It is difficult to predict the toxicity of engineered
nanomaterials based on their composition becau...'
- **QDABT-4524**: No domain assigned
  Text: 'Eating the leaves from foxglove plant can cause
which of the following?...'
- **QDABT-4530**: No domain assigned
  Text: 'Acrylamide has been used in a variety of foods
and beverages (e,g., baked goods and coffee, among
ot...'
- **QDABT-4537**: No domain assigned
  Text: 'Neoplastic transformation of cells is NOT usually
associated which of the following?...'
- **QDABT-4546**: No domain assigned
  Text: 'Which of the following is CORRECT about
fibrosarcomas?...'
- **QDABT-4554**: No domain assigned
  Text: 'Which of the following is TRUE regarding
glutamate?...'
- **QDABT-4559**: No domain assigned
  Text: 'Which of the following is NOT a characteristic of
Natural Killer (NK) cells?...'
- **QDABT-4562**: No domain assigned
  Text: 'Which of the following statements BEST
characterizes the Buehler and Maximization assays?...'
- **QDABT-4571**: No domain assigned
  Text: 'Which of the following associations is NOT
CORRECT?...'
- **QDABT-4581**: No domain assigned
  Text: 'The transcription factor Nrf2 is the master
regulator of a major adaptive response to cellular
stres...'
- **QDABT-4583**: No domain assigned
  Text: 'There is a growing interest in nanoparticles that
may be useful in a variety of chemical and biologi...'
- **QDABT-4586**: No domain assigned
  Text: 'The key measures of validity in epidemiologic
studies are sensitivity and specificity.  Which of the...'
- **QDABT-4587**: No domain assigned
  Text: 'The primary physiochemical property used in
quantitative structure-activity relationship (QSAR)
mode...'
- **QDABT-4601**: No domain assigned
  Text: 'Which of the following BEST describes the
purpose of the local lymph node assay?...'
- **QDABT-4605**: No domain assigned
  Text: 'Which of the following types of uteri occurs in
the rat?...'
- **QDABT-4612**: No domain assigned
  Text: 'Statistical tests used in epidemiological studies
consider the influence of both type I and type II
...'
- **QDABT-4615**: No domain assigned
  Text: 'Which of the following is/are true regarding
chemical injury to the cornea?...'
- **QDABT-4619**: No domain assigned
  Text: 'All of the following can inhibit opening of the
mitochondrial permeability transition pore (mPT)
exc...'
- **QDABT-4620**: No domain assigned
  Text: 'Which of the following rodenticides acts
principally by blocking the enzyme aconitase in the
Krebs (...'
- **QDABT-4623**: No domain assigned
  Text: 'All of the following are true of trichloroethylene
except:...'
- **QDABT-4631**: No domain assigned
  Text: 'All of the following statements are true of volatile
organic compounds (VOC) except:...'
- **QDABT-4633**: No domain assigned
  Text: 'Which of the following statements is not true for
the data shown in this figure?...'
- **QDABT-4635**: No domain assigned
  Text: 'The data shown in this graph indicate that:...'
- **QDABT-4637**: No domain assigned
  Text: 'The slope of a probit plot is:...'
- **QDABT-4641**: No domain assigned
  Text: 'Which of the following is NOT a goal of the 1996
Food Quality Protection Act?...'
- **QDABT-4642**: No domain assigned
  Text: 'Which of the following refers to a risk evaluation
involving the calculation and expression of risk ...'
- **QDABT-4647**: No domain assigned
  Text: 'Which of the following personal care products
produces the highest total number of reactions among
a...'
- **QDABT-4648**: No domain assigned
  Text: 'A temperature inversion in a densely populated
area is characterized by:...'
- **QDABT-4649**: No domain assigned
  Text: 'Eutrophication:...'
- **QDABT-4657**: No domain assigned
  Text: 'Signs of advanced chloroquine-induced
retinopathy may include:...'
- **QDABT-4664**: No domain assigned
  Text: 'Hereditary hemochromatosis causes ____....'
- **QDABT-4665**: No domain assigned
  Text: 'Which of the following can cause vaginal
adenocarcinoma:...'
- **QDABT-4678**: No domain assigned
  Text: 'Garlic breath is associated with all of the
following except ____....'
- **QDABT-4679**: No domain assigned
  Text: 'The primary toxicity of lindane
(hexachlorocyclohexane) is manifested as which of
the following?...'
- **QDABT-4681**: No domain assigned
  Text: 'Zinc phosphide is an inexpensive and effective
rodenticide. Symptoms of accidental ingestion
include...'
- **QDABT-4682**: No domain assigned
  Text: 'Which of the following is/are true concerning
Aroclor 1254?...'
- **QDABT-4686**: No domain assigned
  Text: 'Which of the following signs is NOT diagnostic
of acute opioid overdose?...'
- **QDABT-4687**: No domain assigned
  Text: 'A proposed 28-day study in rats involves oral
dosing a novel pharmaceutical to groups of 10 male
and...'
- **QDABT-4694**: No domain assigned
  Text: 'All of the following are true in Wilson's disease
except ____....'
- **QDABT-4696**: No domain assigned
  Text: 'Benzodiazepines at high doses can cause which
of the following peripheral effects?...'
- **QDABT-4700**: No domain assigned
  Text: 'Menkes' disease is characterized by ____....'
- **QDABT-4704**: No domain assigned
  Text: 'Which of the following is a major weakness of
cross-sectional epidemiological studies?...'
- **QDABT-4706**: No domain assigned
  Text: 'Which of the following statements is NOT true:...'

---
*End of audit report -- generated 2026-05-20 01:59:37*