#!/usr/bin/env python3
"""
Comprehensive answer extraction v3 - with careful text matching.
Matches DB questions to PPTX-derived answers using text comparison.
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
    # Normalize: remove newlines, extra spaces
    text_clean = re.sub(r'\s+', ' ', row['question_text']).strip()
    all_remaining[row['id']] = {
        'text': row['question_text'],
        'text_clean': text_clean,
        'current_answer': row['correct_answer_letter']
    }

print(f"Total remaining questions: {len(all_remaining)}")

# Define answer map: each entry is (text_fragment_or_pattern, answer_letter)
# Using normalized text for matching
answer_map = []

def add_match(pattern, answer):
    answer_map.append((pattern, answer))

# ===== 2015 Part B Q1-Q8 (Szabo part b_1-8.pptx) =====
add_match('neoplastic transformation of cells is not usually associated', 'D')
add_match('not been classified as group 1 iarc carcinogenic', 'C')
add_match('minocycline, nicardipine, and spironolactone are examples of marketed drugs known to induce thyroid', 'C')
add_match('what is the primary factor responsible for how deeply a gas penetrates into the lung', 'C')
add_match('mucociliary clearance of inhaled particles deposited in the lower airways', 'C')
add_match('which of the following assays assesses the ability of a test material to induce chromosomal aberrations in vivo', 'B')
add_match('correct regarding the "promotion" stage in the multistage carcinogenesis model', 'A')
add_match('during which period of pregnancy will administration of a drug most likely produce teratogenic effects', 'B')

# ===== 2015 Part B Q9-Q16 (2015 Part b JG_9-16.pptx) =====
add_match('how can dna adducts assist in establishing a chemical\'s mode of action', 'A')
add_match('which of the following is correct about fibrosarcomas', 'A')
add_match('not true regarding chemical-induced deregulation to produce thyroid hormone insufficiency', 'C')
add_match('reproductive physiology similarity among humans and rats', 'B')
add_match('not correct regarding endocrine disruption', 'B')
add_match('ethanol, retinoids, valproic acid, and the angiotensin converting enzyme', 'C')
add_match('biggest public health concern related to low level exposure to lead', 'D')
add_match('basis of acrylamide neurotoxicity is considered to be', 'A')

# ===== 2015 Part B Q17-Q24 (Natalia_Recert part B_17-24.pptx) =====
add_match('which of the following is true regarding glutamate', 'C')
add_match('not correct regarding peripheral nervous system axonopathies', 'A')
add_match('potential effects of a toxicant on vision is evaluated in the functional observational battery', 'B')
add_match('peripheral neuropathy caused by n-hexane and carbon disulfide', 'B')
add_match('mechanism of retinal and optic nerve toxicity of methanol in humans', 'A')
add_match('not a characteristic of natural killer (nk) cells', 'C')
add_match('not correct regarding renal injury', 'D')
add_match('primary site of kidney injury resulting from exposure to chloroform', 'A')

# ===== 2015 Part B Q25-Q40 (2015 part b 24-40 ADL_AM.pptx) =====
add_match('which of the following statements best characterizes the buehler and maximization assays', 'D')
add_match('chloracne is a persistent skin disease caused by overexposure to certain halogenated', 'B')
add_match('not characteristic of allergic contact dermatitis', 'D')
add_match('which ocular tissue is highly vulnerable to systemic, toxicant induced structural', 'E')
add_match('oral anticoagulant, warfarin, modulates hemostasis by interfering with vitamin k', 'D')
add_match('which of the following agents specifically accumulates in hepatic stellate cells', 'B')
add_match('which of the following is the primary function for kupffer cells in the liver', 'B')
add_match('the in vivo micronucleus test is often used in a standard battery', 'C')
add_match('which of the following answers is correct regarding iarc class 1 carcinogens', 'C')
add_match('tester strains of salmonella typhimurium used in the ames assay', 'A')
add_match('which organ system is most susceptible to cisplatin toxicity', 'A')
add_match('which of the following associations is not correct', 'C')
add_match('iron (fe) is an essential mineral but overdoses result in damage to periportal hepatocytes', 'B')
add_match('xenobiotics such as omeprazole or zidovudine can contribute to a deficiency of vitamin b12', 'C')
add_match('of the various circulating biomarkers available for detecting myocardial injury', 'B')

# ===== 2013 Part A Q17-Q24 (DABT Prep_Natalia_2013 Recert part A_17-24.pptx) =====
# These have Explicit "Answer: X" on discussion slides
# Matching by text from the slides
add_match('bisphenol a is considered a chemical of concern due to which of the following', 'C')

# ===== 2013 Part A Q25-Q40 (2013 part A 25-40_ADL_AM.pptx) =====
add_match('for which agent listed below is the neurotoxicity associated with its use mediated by a disruption of microtubule dissociation', 'D')
add_match('ionization frequently disrupts chemical bonding in cellular molecules such as dna', 'C')
add_match('soft tissue calcification in cattle has been attributed to which of the following', 'B')
add_match('which of the following properties best describes the estrogenic activity of phytoestrogens', 'A')
add_match('particle size of an aerosol is a major determinant of where in the respiratory tract', 'E')
add_match('snake venoms are complex mixtures, however, their poisonous effects are most commonly due', 'A')
add_match('food idiosyncrasy is characterized by which of the following', 'C')
add_match('which of the following statements about selenium and selenium compounds is not correct', 'C')
add_match('which of the following is an important class of chemicals that are formed during grilling or broiling', 'B')
add_match('which aflatoxin is the most toxicologically potent and commonly occurs in produce', 'A')
add_match('rhabdomyolysis can be the direct result of a toxicant or the indirect result', 'C')
add_match('which of the following is a specific antidote for benzodiazepine overdose', 'C')
add_match('some ethnic populations, such as asians and native americans, have difficulty metabolizing alcohol', 'E')
add_match('which of the following is correct regarding the mycotoxin food contaminant zearalenone', 'C')
add_match('which of the following toxicities is not associated with acute or chronic tetracycline antibiotics use', 'C')

# ===== 2013 Part C Q1-Q8 (DS_2013 Part C exam 1-8.pptx) =====
add_match('the therapeutic index (ti) of a drug is an approximation of the relative safety', 'D')
add_match('which of the following best describes hormesis', 'A')
add_match('primary sites of absoption of toxicants into the body include', 'C')
add_match('which reactive oxygen species (ros is likely to be most damaging', 'C')
add_match('the cytochrome p450 family of enzymes consists of about 1,000 known p450 isoforms', 'E')
add_match('which of the following enzymes catalyze a phase ii biotransformation of xenobiotic', 'B')
add_match('peanut allergy is relatively common and can be quite severe in some individuals', 'A')

# ===== 2015 Part C Q1-Q8 (DS_2015 part C questions 1_8.pptx) =====
add_match('calculate the achieved dosage in mg/kg/day of a chemical fed to rats', 'A')
add_match('select the correct pairing of toxic agent and mechanism of cardiotoxicity', 'D')
add_match('furanocoumarins in grapefruit juice can increase the systemic exposure', 'A')
add_match('many chemicals require metabolic activation to form their ultimate toxicants', 'A')
add_match('oligomycin, cyhexatin, ddt, and chlordecone all can interfere with mitochondrial atp synthesis', 'A')
add_match('establishing a causal association between an occupational toxicant and harmful effect', 'D')
add_match('which of the following would be expected to be the most effective treatment for protecting against systemic effects from hydrofluoric acid', 'C')
add_match('which of the following is not considered an important factor affecting nanoparticle toxicity in the lung', 'B')

# ===== 2015 Part C Q9-Q16 (JG_part C 9-16.pptx) =====
add_match('which of the following metabolic pathways would most likely be involved with protecting tissue and cellular function', 'C')
add_match('which of the following statements is not correct relative to toxicokinetic behavior of pharmaceuticals', 'D')
add_match('the transcription factor nrf2 is the master regulator of a major adaptive response', 'D')
add_match('for drugs that are extensively bound to plasma proteins but are not bound to tissue components', 'C')

# Now match
matched_pairs = []
for qid, qdata in all_remaining.items():
    text_clean = qdata['text_clean'].lower()
    
    for pattern, answer in answer_map:
        if pattern.lower() in text_clean:
            matched_pairs.append((qid, answer, pattern))
            break

print(f"\nMatched {len(matched_pairs)} questions")
for qid, answer, pattern in matched_pairs:
    text_preview = all_remaining[qid]['text_clean'][:80]
    print(f"  {qid}: {answer} <- '{pattern}'")

# Check for duplicates
id_to_answer = {}
for qid, answer, pattern in matched_pairs:
    if qid in id_to_answer:
        print(f"  WARNING: {qid} already matched as {id_to_answer[qid]}, now also {answer} from '{pattern}'")
    id_to_answer[qid] = answer

print("\n=== UNMATCHED QUESTIONS ===")
for qid, qdata in all_remaining.items():
    if qid not in id_to_answer:
        print(f"  {qid}: {qdata['text_clean'][:100]}...")

print(f"\nTotal matched: {len(matched_pairs)}")
print(f"Total unmatched: {len(all_remaining) - len(matched_pairs)}")

# Save the results
results = []
for qid, answer, pattern in matched_pairs:
    results.append({
        'id': qid,
        'answer': answer,
        'match_pattern': pattern,
        'text_preview': all_remaining[qid]['text_clean'][:80]
    })

with open(BACKUP_PATH, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to {BACKUP_PATH}")

# Now update the database
print("\n=== UPDATING DATABASE ===")
update_count = 0
for qid, answer, pattern in matched_pairs:
    cursor.execute("""
        UPDATE questions 
        SET correct_answer_letter = ? 
        WHERE id = ? AND (correct_answer_letter IS NULL OR correct_answer_letter = '')
    """, (answer, qid))
    if cursor.rowcount > 0:
        update_count += 1
        print(f"  Updated {qid}: {answer}")

conn.commit()
print(f"\nUpdated {update_count} questions in database")

conn.close()
