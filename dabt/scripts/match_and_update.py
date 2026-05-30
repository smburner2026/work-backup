#!/usr/bin/env python3
"""
Final comprehensive answer extraction and DB update.
Maps exam question numbers to DABT IDs based on question text matching.
"""
import sqlite3
import json
import re
import os

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
BACKUP_PATH = "/root/work/dabt/source7_additional_answers.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all remaining source 7 questions with full text
cursor.execute("""
    SELECT id, question_text, correct_answer_letter
    FROM questions 
    WHERE source_file_id=7 
    AND (correct_answer_letter IS NULL OR correct_answer_letter = '')
    ORDER BY id
""")

all_remaining = {}
for row in cursor.fetchall():
    all_remaining[row['id']] = {
        'text': row['question_text'],
        'current_answer': row['correct_answer_letter']
    }

print(f"Total remaining questions: {len(all_remaining)}")

# =======================================================
# MANUALLY DERIVED ANSWER MAP FROM PPTX ANALYSIS
# Based on careful reading of all 15 PPTX discussion files
# =======================================================

# Each map: key = DABT-ID or question text fragment, value = answer letter

# --- 2015 Part B Q1-Q8 (Szabo part b_1-8.pptx) ---
# Q1: "Neoplastic transformation of cells is NOT usually associated which of the following?"
#   Answer: D (release of growth factors that suppress cell proliferation - NOT associated)
# Q2: "Which of the following molecules has NOT been classified as group 1 IARC carcinogenic agents?"
#   Answer: C (IARC 4 - the others are IARC 1)
# Q3: "Minocycline, nicardipine, and spironolactone..."
#   Answer: C (induction of hepatic microsomal enzymes - per reference)
# Q4: "What is the primary factor responsible for how deeply a gas penetrates into the lung?"
#   Answer: C (water solubility)
# Q5: "In healthy individuals, mucociliary clearance..."
#   Answer: C (24-48 hours)
# Q6: "Which of the following assays assesses the ability of a test material to induce chromosomal aberrations in vivo?"
#   Answer: B (mouse micronucleus test - in vivo)
# Q7: "Which of the following is CORRECT regarding the 'promotion' stage..."
#   Answer: A (True p. 398)
# Q8: "During which period of pregnancy will administration of a drug most likely produce teratogenic effects..."
#   Answer: B (First Trimester, organogenesis period)

# Match by question text
def find_q_by_text_fragment(text_fragment, all_qs):
    """Find matching question IDs by text fragment."""
    matches = []
    fragment_lower = text_fragment.lower().strip()
    for qid, qdata in all_qs.items():
        if fragment_lower in qdata['text'].lower():
            matches.append(qid)
    return matches

# Build the answer map based on my analysis
answer_map = {}

# ===== 2015 Part B Q1-Q8 =====
answer_map['Neoplastic transformation of cells is NOT usually'] = 'D'
answer_map['NOT been classified as group 1 IARC'] = 'C'
answer_map['Minocycline, nicardipine, and spironolactone'] = 'C'
answer_map['primary factor responsible for how deeply a gas penetrates'] = 'C'
answer_map['mucociliary clearance of inhaled particles deposited in the lower airways'] = 'C'
answer_map['assays assesses the ability of a test material to induce chromosomal aberrations in vivo'] = 'B'
answer_map['CORRECT regarding the "promotion" stage in the multistage carcinogenesis'] = 'A'
answer_map['period of pregnancy will administration of a drug most likely produce teratogenic effects'] = 'B'

# ===== 2015 Part B Q9-Q16 =====
answer_map['How can DNA adducts assist in establishing'] = 'A'  # Best answer p.137
answer_map['Which of the following is CORRECT about fibrosarcomas'] = 'A'  # best answer: malignant mesenchymal tumor
answer_map['NOT TRUE regarding chemical-induced deregulation to produce thyroid'] = 'C'  # C is False
answer_map['reproductive physiology similarity among humans and rats'] = 'B'  # B) Correct
answer_map['NOT CORRECT regarding endocrine disruption'] = 'B'  # B is false
answer_map['Ethanol, retinoids, valproic acid, and the angiotensin converting enzyme'] = 'C'  # C is correct answer
answer_map['biggest public health concern related to low level exposure to lead'] = 'D'  # D is correct
answer_map['basis of acrylamide neurotoxicity'] = 'A'  # A) Best answer

# ===== 2015 Part B Q17-Q24 (Natalia_Recert part B_17-24.pptx) =====
answer_map['Which of the following is TRUE regarding glutamate'] = 'C'   # Q17: Answer C
answer_map['NOT CORRECT regarding peripheral nervous system axonopathies'] = 'A'  # Q18: Answer A
answer_map['potential effects of a toxicant on vision is evaluated in the Functional Observational Battery'] = 'B'  # Q19: Answer B
answer_map['peripheral neuropathy caused by n-hexane'] = 'B'  # Q20: Answer B
answer_map['mechanism of retinal and optic nerve toxicity of methanol'] = 'A'  # Q21: Answer A
answer_map['Which of the following is NOT a characteristic of Natural Killer'] = 'C'  # Q22: Answer C
answer_map['NOT CORRECT regarding renal injury'] = 'D'  # Q23: Answer D
answer_map['primary site of kidney injury resulting from exposure to chloroform'] = 'E'  # Q24: Answer E

# ===== 2015 Part B Q25-Q40 (2015 part b 24-40 ADL_AM.pptx) =====
answer_map['primary site of kidney injury resulting from exposure to chloroform'] = 'A'  # Q25: proximal tubule
answer_map['Which of the following statements BEST characterizes the Buehler and Maximization'] = 'D'  # Q26: delayed-contact hypersensitivity
answer_map['Chloracne is a persistent skin disease caused by overexposure'] = 'B'  # Q27: sebaceous glands
answer_map['Which of the following is NOT characteristic of allergic contact dermatitis'] = 'D'  # Q28: intensity proportional to dose
answer_map['Which ocular tissue is highly vulnerable to systemic'] = 'E'  # Q29: retina
answer_map['oral anticoagulant, warfarin, modulates hemostasis by interfering with vitamin K'] = 'D'  # Q30: decreased clotting factors IX and X
answer_map['Which of the following agents specifically accumulates in hepatic stellate cells'] = 'B'  # Q31: vitamin A
answer_map['Which of the following is the primary function for Kupffer cells in the liver'] = 'B'  # Q32: macrophages
answer_map['The in vivo micronucleus test is often used'] = 'C'  # Q33: membrane-bounded structures
answer_map['Which of the following answers is CORRECT regarding IARC Class 1 carcinogens'] = 'C'  # Q34: benzene, aflatoxin, vinyl chloride
answer_map['The tester strains of Salmonella typhimurium used in the Ames Assay'] = 'A'  # Q35: TA 1535, TA 100, TA 1538, TA 98
answer_map['Which organ system is most susceptible to cisplatin toxicity'] = 'A'  # Q36: kidney
answer_map['Which of the following associations is NOT CORRECT'] = 'C'  # Q37: unleaded gasoline: alpha2u-globulin in humans
answer_map['Iron (Fe) is an essential mineral but overdoses result in damage to periportal hepatocytes'] = 'B'  # Q38: electron donor for ROS
answer_map['Xenobiotics such as omeprazole or zidovudine can contribute to a deficiency of vitamin B12'] = 'C'  # Q39: megaloblastic anemia
answer_map['Of the various circulating biomarkers available for detecting myocardial injury'] = 'B'  # Q40: cardiac troponins T and I

# ===== 2013 Part A Q17-Q24 (DABT Prep_Natalia_2013 Recert part A_17-24.pptx) =====
# Q17: 'D', Q18: 'D', Q19: 'A', Q20: 'D', Q21: 'C', Q22: 'A', Q23: 'B', Q24: 'B'
# These need to be matched by question text

# ===== 2013 Part A Q25-Q40 (2013 part A 25-40_ADL_AM.pptx) =====
answer_map['Which aflatoxin is the most toxicologically potent'] = 'A'  # Q35: Aflatoxin B1
answer_map['Which of the following is a specific antidote for benzodiazepine overdose'] = 'C'  # Q37: flumazenil
answer_map['Some ethnic populations, such as Asians and Native Americans, have difficulty metabolizing alcohol'] = 'E'  # Q38: acetaldehyde dehydrogenase
answer_map['Which of the following is CORRECT regarding the mycotoxin food contaminant zearalenone'] = 'C'  # Q39: decreases reproductive potential
answer_map['Which of the following toxicities is NOT associated with acute or chronic tetracycline'] = 'C'  # Q40: cardio-pulmonary effects

# More 2013 Part A Q25-Q40
answer_map['For which agent listed below is the neurotoxicity associated with its use mediated by a disruption of microtubule dissociation'] = 'D'  # Q25: paclitaxel
answer_map['Ionization frequently disrupts chemical bonding in cellular molecules such as DNA'] = 'C'  # Q26: single-strand breaks
answer_map['Soft tissue calcification in cattle has been attributed'] = 'B'  # Q27: Vitamin D-like glycosides
answer_map['Which of the following properties best describes the estrogenic activity of phytoestrogens'] = 'A'  # Q28: antigonadotropic effects
answer_map['The particle size of an aerosol is a major determinant of where in the respiratory tract'] = 'E'  # Q29: sigmag=2.0 is monodisperse (NOT CORRECT)
answer_map['Snake venoms are complex mixtures, however, their poisonous effects are most commonly due'] = 'A'  # Q30: enzymes and polypeptides
answer_map['Food idiosyncrasy is characterized by which of the following'] = 'C'  # Q31: genetically predisposed individuals
answer_map['Bisphenol A is considered a chemical of concern'] = 'C'  # Q32: extensive use in plastic, weak estrogen receptor binding
answer_map['Which of the following statements about selenium and selenium compounds is NOT CORRECT'] = 'C'  # Q33: enhances methylmercury toxicity
answer_map['Which of the following is an important class of chemicals that are formed during grilling or broiling'] = 'B'  # Q34: heterocyclic amines
answer_map['Rhabdomyolysis can be the direct result of a toxicant'] = 'C'  # Q36: NOT CORRECT - red colored urine

# ===== 2013 Part C Q2-Q8 (DS_2013 Part C exam 1-8.pptx) =====
answer_map['The therapeutic Index (TI) of a drug is an approximation of the relative safety'] = 'D'  # Q2: ED50
answer_map['Which of the following best describes hormesis'] = 'A'  # Q3: beneficial low, adverse high
answer_map['Primary sites of absoption of toxicants into the body'] = 'C'  # Q4: skin, GI, lung
answer_map['Which reactive oxygen species (ROS is likely to be most damaging'] = 'C'  # Q5: hydroxyl radical
answer_map['The cytochrome P450 family of enzymes consists of about 1,000 known P450 isoforms'] = 'E'  # Q6: conjugating enzymes
answer_map['Which of the following enzymes catalyze a phase II biotransformation'] = 'B'  # Q7: glutathione S-transferase
answer_map['Peanut allergy is relatively common and can be quite severe'] = 'A'  # Q8: Type 1 hypersensitivity

# ===== 2015 Part C Q1-Q8 (DS_2015 part C questions 1_8.pptx) =====
answer_map['Calculate the achieved dosage in mg/kg/day of a chemical fed to rats'] = 'A'  # Q1: 600
answer_map['Select the correct pairing of toxic agent and mechanism of cardiotoxicity'] = 'D'  # Q2: cobalt altered calcium homeostasis
answer_map['Furanocoumarins in grapefruit juice can increase the systemic exposure'] = 'A'  # Q3: inhibition of intestinal CYP3A4
answer_map['Many chemicals require metabolic activation to form their ultimate toxicants'] = 'A'  # Q4: fluoroacetate forms fluoronitrate (should be fluorocitrate)
answer_map['Oligomycin, cyhexatin, DDT, and chlordecone all can interfere with mitochondrial ATP synthesis'] = 'A'  # Q5: inhibit ADP phosphorylation on ATP synthase
answer_map['Establishing a causal association between an occupational toxicant and harmful effect'] = 'D'  # Q6: relationships between metabolic pathways can be derived
answer_map['Which of the following would be expected to be the most effective treatment for protecting against systemic effects from hydrofluoric acid'] = 'C'  # Q7: calcium gluconate
answer_map['Which of the following is NOT considered an important factor affecting nanoparticle toxicity in the lung'] = 'B'  # Q8: glucuronidation of nanoparticulates

# ===== 2015 Part C Q9-Q16 (JG_part C 9-16.pptx) =====
answer_map['Which of the following metabolic pathways would most likely be involved with protecting tissue'] = 'C'  # Q9: Correct - Ch. 3
answer_map['Which of the following statements is NOT CORRECT relative to toxicokinetic'] = 'D'  # Q11: D is False (NOT TRUE)
answer_map['The transcription factor Nrf2 is the master regulator of a major adaptive response'] = 'D'  # Q15: D) Correct - KEAP1 sequesters NRF2

# ===== 2013 Part A Q9-Q16 (JG 2013recert part A questions9_16.pptx) =====
# Q12: 'C' (Bt corn - true, ~80% of market)
# Q13: 'D' (Correct - Solvent elimination engineering controls)
# Q15: 'D' (Correct - atropine cornerstone of treatment)

# Let's also check: DABT-4487 to DABT-4495 are liver/NAFLD questions - NOT from recert discussion slides
# DABT-4496 Bisphenol A - already matched (2013 Part A Q32)
# DABT-4497-4498 are forensic tox questions - NOT from recert discussion slides

# Now let's do the matching
matched_pairs = []

for qid, qdata in all_remaining.items():
    text = qdata['text']
    
    for fragment, answer in answer_map.items():
        if fragment.lower() in text.lower():
            matched_pairs.append((qid, answer, fragment))
            break

print(f"\nMatched {len(matched_pairs)} questions using text fragments")
for qid, answer, fragment in matched_pairs:
    print(f"  {qid}: {answer} (matched: '{fragment}')")

# Check for duplicates (same question matched by multiple fragments)
# Also check for conflicts with existing answers
print("\n=== UNMATCHED QUESTIONS ===")
matched_ids = set(m[0] for m in matched_pairs)
for qid, qdata in all_remaining.items():
    if qid not in matched_ids:
        text_preview = qdata['text'][:80]
        print(f"  {qid}: {text_preview}...")

conn.close()
