#!/usr/bin/env python3
"""
Extract ALL questions from 2000Q Question Bank docx files into standardized CSV
matching the DABT database schema.

Output: /tmp/dabt_extract_2000q.csv
"""

import os, re, csv, sys
from collections import OrderedDict, defaultdict
from docx import Document

BASE_DIR = "/root/dabt-curated/2000Q_Question_Bank"
ANSWER_KEY_CSV = os.path.join(BASE_DIR, "2000Q_ANSWER_KEY.csv")
OUTPUT_CSV = "/tmp/dabt_extract_2000q.csv"

# All non-duplicate 2000Q docx files (skip _DUPLICATE_ prefix)
DOCX_FILES = sorted([
    f for f in os.listdir(BASE_DIR)
    if f.endswith('.docx') and f.startswith('2000Q') and not f.startswith('_DUPLICATE')
])

# Source Exam names (human-readable, short)
def source_exam_name(filename):
    """Derive a short human-readable source exam name from filename."""
    name = filename.replace('2000Q ', '').replace('.docx', '')
    # Clean up common patterns
    name = name.replace('Ch1 General', 'Ch1 General')
    name = name.replace('Ch3 Mechanisms of Toxicity', 'Ch3 Mechanisms')
    name = name.replace('Ch5 ADE', 'Ch5 ADE')
    name = name.replace('Ch6 Metabolism', 'Ch6 Metabolism')
    name = name.replace('Ch7 TK', 'Ch7 TK')
    name = name.replace('Ch8 Cardiovascular Tox', 'Ch8 Cardiovascular')
    name = name.replace('Ch11 Blood', 'Ch11 Blood')
    name = name.replace('Ch12 Immunology', 'Ch12 Immunology')
    name = name.replace('Ch13 Hepatic Tox', 'Ch13 Hepatic')
    name = name.replace('Ch14 Renal Tox', 'Ch14 Renal')
    name = name.replace('Ch15 RESPIRATORY TOXICOLOGY', 'Ch15 Respiratory')
    name = name.replace('Ch16 NEUROTOXICOLOGY', 'Ch16 Neurotoxicology')
    name = name.replace('Ch17 OCULAR TOXICOLOGY', 'Ch17 Ocular')
    name = name.replace('Ch19 Dermal Tox', 'Ch19 Dermal')
    name = name.replace('Ch20 REPRODUCTIVE TOXICOLOGY', 'Ch20 Reproductive')
    name = name.replace('Ch21 ENDOCRINE TOXICOLOGY', 'Ch21 Endocrine')
    name = name.replace('Ch22 PESTICIDES', 'Ch22 Pesticides')
    name = name.replace('Ch23 METAL TOXICOLOGY', 'Ch23 Metal')
    name = name.replace('Ch24 CHEMICAL AND SOLVENT TOXICOLOGY', 'Ch24 Chemical & Solvent')
    name = name.replace('Ch25 RADIATION TOXICOLOGY', 'Ch25 Radiation')
    name = name.replace('Ch27 TOXICOLOGY OF PLANTS', 'Ch27 Plant Toxins')
    name = name.replace('Ch28 AIR AND WATER POLLUTION', 'Ch28 Air & Water')
    name = name.replace('Ch29 ENVIRONMENTAL TOXICOLOGY', 'Ch29 Environmental')
    name = name.replace('Ch30 FOOD TOXICOLOGY', 'Ch30 Food')
    name = name.replace('Ch31 ANALYTICAL TOXICOLOGY', 'Ch31 Analytical')
    name = name.replace('Ch33 OCCUPATIONAL TOXICOLOGY', 'Ch33 Occupational')
    name = name.replace('TOXICOLOGIC DISASTERS', 'Toxicologic Disasters')
    name = name.replace('EPIDEMIOLOGY', 'Epidemiology')
    name = name.replace('MEDICAL TOXICOLOGY', 'Medical Toxicology')
    name = name.replace('DRUG ABUSE TOXICOLOGY', 'Drug Abuse')
    name = name.replace('ANTIDOTES Matching Test', 'Antidotes')
    name = name.replace('ANIMAL TOXICOLOGY', 'Animal Toxicology')
    name = name.replace('ALCOHOL TOXICOLOGY', 'Alcohol Toxicology')
    return name.strip()

# Topic mapping
TOPIC_MAP = {
    'Ch1 General': 'General Principles & Concepts',
    'Ch3 Mechanisms': 'Mechanisms of Toxicity',
    'Ch5 ADE': 'General Toxicology',
    'Ch6 Metabolism': 'Biotransformation / Metabolism',
    'Ch7 TK': 'Toxicokinetics / ADME',
    'Ch8 Cardiovascular': 'Cardiovascular Toxicity',
    'Ch11 Blood': 'Hematology & Blood Toxicity',
    'Ch12 Immunology': 'Immunotoxicology / Allergy',
    'Ch13 Hepatic': 'Liver / Hepatotoxicity',
    'Ch14 Renal': 'Kidney / Nephrotoxicity',
    'Ch15 Respiratory': 'Lung / Pulmonary Toxicity',
    'Ch16 Neurotoxicology': 'Nervous System / Neurotoxicity',
    'Ch17 Ocular': 'Eye / Ocular Toxicity',
    'Ch19 Dermal': 'Skin / Dermatotoxicity',
    'Ch20 Reproductive': 'Reproductive & Developmental Toxicity',
    'Ch21 Endocrine': 'Endocrine Toxicology',
    'Ch22 Pesticides': 'Pesticides – Insecticides',
    'Ch23 Metal': 'Metals & Metalloids',
    'Ch24 Chemical & Solvent': 'Solvents & Hydrocarbons',
    'Ch25 Radiation': 'Radiation / UV / Ionizing',
    'Ch27 Plant Toxins': 'Plant Toxins',
    'Ch28 Air & Water': 'Air Pollution & Particulates',
    'Ch29 Environmental': 'General Toxicology',
    'Ch30 Food': 'Food Additives, Cosmetics & GRAS',
    'Ch31 Analytical': 'General Toxicology',
    'Ch33 Occupational': 'General Toxicology',
    'Alcohol Toxicology': 'Alcohols & Methanol/Ethanol',
    'Animal Toxicology': 'General Toxicology',
    'Antidotes': 'Drugs & Therapeutics – Toxicology',
    'Drug Abuse': 'Drugs & Therapeutics – Toxicology',
    'Epidemiology': 'Risk Assessment & Regulatory',
    'Medical Toxicology': 'Drugs & Therapeutics – Toxicology',
    'Toxicologic Disasters': 'General Toxicology',
}

def get_topic(source_name):
    for key, topic in TOPIC_MAP.items():
        if key.lower() in source_name.lower():
            return topic
    return 'General Toxicology'

# Step 1: Load answer key (question_id -> {file, answer_letter})
print("Loading answer key...")
answer_key = {}  # global_qid -> {file, answer}
with open(ANSWER_KEY_CSV, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        qid = int(row['QuestionID'])
        answer_key[qid] = {
            'file': row.get('File', '').strip(),
            'answer': row.get('AnswerLetter', '').strip(),
        }
print(f"  Loaded {len(answer_key)} answer entries")

# Step 2: Build question-to-file mapping from answer key
qid_to_file = {}  # global_qid -> filename
for qid, info in answer_key.items():
    if info['file']:
        qid_to_file[qid] = info['file']

# Step 3: For each file, find the range of global question IDs that belong to it
file_question_ranges = defaultdict(list)
for qid in sorted(qid_to_file.keys()):
    fname = qid_to_file[qid]
    file_question_ranges[fname].append(qid)

print(f"  Files with question mappings: {len(file_question_ranges)}")
for fname in sorted(file_question_ranges.keys()):
    qids = file_question_ranges[fname]
    print(f"    {fname}: Q{qids[0]}-Q{qids[-1]} ({len(qids)} questions)")

# Step 4: Parse each docx file to extract questions and answer options
def extract_questions_from_docx(filepath, known_qids):
    """
    Extract question text and answer options from a docx file.
    Returns dict: global_qid -> {question_text, options_dict, option_letters}
    """
    doc = Document(filepath)
    results = {}
    
    # Collect all paragraph texts
    all_texts = []
    for para in doc.paragraphs:
        all_texts.append(para.text)
    
    # Strategy: Walk through paragraphs, identify question starts and answer option blocks
    # Question pattern: "NUM. " or "NUM\t" at start of line
    # Answer option pattern: "LETTER. text" (A., B., C., etc.)
    
    current_qid = None
    current_question_lines = []
    current_options = {}  # letter -> text
    found_options_order = []
    
    # Regular expressions
    q_start = re.compile(r'^(\d{1,4})[\.\s]\s*(.*)')
    opt_pattern = re.compile(r'^([A-H])[\.\)]\s*(.*)')
    # For matching tests: "NUM. term \t\t LETTER. definition"
    match_pattern = re.compile(r'^(\d{1,4})[\.\s]\s*(.*?)\s+([A-H])[\.\)]\s*(.*)')
    # Also: "NUM. term \t\t\tLETTER. definition" (tab-based)
    match_tab_pattern = re.compile(r'^(\d{1,4})[\.\s]\s*(.+?)\t+([A-H])[\.\)]?\s*(.*)')
    
    def flush_question():
        nonlocal current_qid, current_question_lines, current_options, found_options_order
        if current_qid is not None and current_qid in known_qids:
            # Clean question text
            qtext = ' '.join(current_question_lines).strip()
            qtext = re.sub(r'\s+', ' ', qtext)
            
            results[current_qid] = {
                'question': qtext,
                'options': dict(current_options),
                'option_order': list(found_options_order),
            }
        current_qid = None
        current_question_lines = []
        current_options = {}
        found_options_order = []
    
    for text in all_texts:
        stripped = text.strip()
        if not stripped:
            # Empty line - could be separator, keep current context
            continue
        
        # Check if this is the start of an answer key section
        if 'ANSWER' in stripped.upper() and ('REFERENCE' in stripped.upper() or stripped.startswith('CHAPTER')):
            # We've reached the answer key - stop extracting questions
            flush_question()
            break
        
        # Try matching test format first: "NUM. term \t LETTER. definition"
        # This has the answer option embedded in the same line
        m_match = match_tab_pattern.match(stripped)
        if not m_match:
            # Try non-tab matching
            m_match = match_pattern.match(stripped)
        
        if m_match:
            qnum = int(m_match.group(1))
            term = m_match.group(2).strip()
            opt_letter = m_match.group(3).strip()
            opt_text = m_match.group(4).strip()
            
            # Flush previous question
            flush_question()
            
            current_qid = qnum
            current_question_lines = [term]
            current_options = {}
            found_options_order = []
            
            # The answer option is on the same line
            # But this may be part of a matching test where options span many lines
            # For matching tests, each question has its own answer option embedded
            current_options[opt_letter] = opt_text
            found_options_order.append(opt_letter)
            
            flush_question()
            continue
        
        # Check if line starts with a question number
        m_q = q_start.match(stripped)
        if m_q:
            qnum = int(m_q.group(1))
            rest = m_q.group(2).strip()
            
            # Check if the rest contains answer options (e.g., "text A. opt B. opt")
            # This happens when options are on the same line as question
            # First check if there's just text with no options
            has_inline_options = bool(re.search(r'\s+([A-H])[\.\)]\s', rest))
            
            # Flush previous question
            flush_question()
            
            current_qid = qnum
            # Remove any trailing "Matching Test" text
            if rest.endswith('Matching Test') or rest.endswith('Matching'):
                current_question_lines = [rest.replace('Matching Test', '').replace('Matching', '').strip()]
            else:
                current_question_lines = [rest]
            current_options = {}
            found_options_order = []
            
            # Check for inline options on the same line as the question number
            # Format: "NUM. text A. option B. option C. option D. option"
            # This happens when the question text is very short
            remaining = rest
            inline_opts_found = False
            while True:
                m_opt = re.search(r'\s+([A-H])[\.\)]\s+(.*)', remaining)
                if m_opt:
                    letter = m_opt.group(1)
                    opt_text = m_opt.group(2).strip()
                    # Only consider it an option if the remaining text after stripping
                    # the question part is mostly options
                    current_options[letter] = opt_text
                    found_options_order.append(letter)
                    remaining = ''
                    inline_opts_found = True
                    break
                else:
                    break
            
            if inline_opts_found:
                # Clean the question text - remove the inline options
                # The question text is what came before the first option
                # Re-extract: first part is question, then options
                qtext_parts = rest.split(maxsplit=1)
                if len(qtext_parts) > 1:
                    pass  # keep as is, the options were already parsed
                flush_question()
                continue
        
        # Check if line is an answer option (A. ... or A) ...)
        m_opt = opt_pattern.match(stripped)
        if m_opt:
            letter = m_opt.group(1)
            opt_text = m_opt.group(2).strip()
            
            if current_qid is not None:
                current_options[letter] = opt_text
                if letter not in found_options_order:
                    found_options_order.append(letter)
            continue
        
        # Otherwise, it could be continuation of question text
        if current_qid is not None:
            # Check if this looks like it could be a standalone answer option without the letter prefix
            # But only add if it doesn't look like a new question
            current_question_lines.append(stripped)
    
    # Flush last question
    flush_question()
    
    # Post-processing: For questions where we couldn't find options,
    # try a different approach - scan backwards from the question to find options
    # This handles cases where options appear AFTER the question text
    
    return results


def extract_questions_v2(filepath, known_qids):
    """
    More robust extraction: process the docx paragraph by paragraph,
    handling multi-line questions and answer options that appear after questions.
    """
    doc = Document(filepath)
    results = {}
    
    # Get all non-empty paragraphs
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append(text)
    
    # Find where the answer key section starts
    answer_key_start = len(paragraphs)
    for i, text in enumerate(paragraphs):
        if 'ANSWER' in text.upper() and ('REFERENCE' in text.upper() or 'CHAPTER' in text.upper()):
            answer_key_start = i
            break
    
    # Only process paragraphs before the answer key
    content_paragraphs = paragraphs[:answer_key_start]
    
    # Pattern for detecting question starts
    qnum_pattern = re.compile(r'^(\d{1,4})[\.\s]\s*(.*)')
    # Pattern for answer options: "A. text" or "A) text"
    opt_pattern = re.compile(r'^([A-H])[\.\)]\s*(.*)')
    # Pattern for matching test: "NUM. term \t LETTER. definition" or "NUM. term LETTER. definition"
    match_inline = re.compile(r'^(\d{1,4})[\.\s]\s*(.+?)\s+([A-H])[\.\)]\s*(.*)')
    
    # State machine
    questions = OrderedDict()  # qid -> {'question': ..., 'options': {letter: text, ...}, 'option_order': [...]}
    
    # We'll process paragraph by paragraph
    # A question starts with a number, then optionally has answer options
    # Answer options can be on the same paragraph, or on subsequent paragraphs
    
    current_qid = None
    current_question = []
    current_options = OrderedDict()
    in_question = False
    
    def save_question():
        nonlocal current_qid, current_question, current_options, in_question
        if current_qid is not None and current_qid in known_qids:
            qtext = ' '.join(current_question).strip()
            qtext = re.sub(r'\s+', ' ', qtext)
            if qtext:
                questions[current_qid] = {
                    'question': qtext,
                    'options': dict(current_options),
                    'option_order': list(current_options.keys()),
                }
        current_qid = None
        current_question = []
        current_options = OrderedDict()
        in_question = False
    
    i = 0
    while i < len(content_paragraphs):
        text = content_paragraphs[i]
        
        # Check for matching test format: "NUM. term LETTER. definition" (all in one line)
        m_match = re.match(r'^(\d{1,4})[\.\s]\s*(.+?)\s+([A-H])[\.\)]\s*(.*)', text)
        if m_match:
            qnum = int(m_match.group(1))
            term = m_match.group(2).strip()
            opt_letter = m_match.group(3).strip()
            opt_text = m_match.group(4).strip()
            
            if qnum in known_qids:
                save_question()
                current_qid = qnum
                current_question = [term]
                current_options = OrderedDict()
                current_options[opt_letter] = opt_text
                save_question()
            i += 1
            continue
        
        # Check if line starts with a question number
        m_q = qnum_pattern.match(text)
        if m_q:
            qnum = int(m_q.group(1))
            rest = m_q.group(2).strip()
            
            # Save any previous question
            save_question()
            
            if qnum not in known_qids:
                i += 1
                continue
            
            current_qid = qnum
            in_question = True
            
            # Check if rest contains inline answer options like "A. text B. text C. text D. text"
            # Pattern: after some text, we see "A." or "A)" followed by text, then "B." etc.
            # First extract the question text (before the first option)
            opt_match = re.search(r'\s+([A-H])[\.\)]\s+', rest)
            if opt_match:
                # Find where the question text ends and options begin
                # The question text is everything before the first letter option pattern
                first_opt_pos = opt_match.start()
                qtext = rest[:first_opt_pos].strip()
                current_question = [qtext] if qtext else []
                
                # Now extract all inline options
                opt_rest = rest[first_opt_pos:].strip()
                # Parse: "A. text B. text C. text D. text" etc.
                opt_parts = re.findall(r'([A-H])[\.\)]\s*([^A-H]*(?:\([^)]*\)[^A-H]*)*)', opt_rest)
                for letter, opt_text in opt_parts:
                    opt_text = opt_text.strip()
                    if opt_text and letter not in current_options:
                        current_options[letter] = opt_text
                
                save_question()
                i += 1
                continue
            else:
                # Just the question text on this line
                current_question = [rest]
                i += 1
                continue
        
        # If we're in a question, check for answer options
        if in_question and current_qid is not None:
            m_opt = opt_pattern.match(text)
            if m_opt:
                letter = m_opt.group(1)
                opt_text = m_opt.group(2).strip()
                if letter not in current_options:
                    current_options[letter] = opt_text
                i += 1
                continue
            else:
                # Continuation of question text
                current_question.append(text)
                i += 1
                continue
        
        i += 1
    
    # Save last question
    save_question()
    
    return questions


# Step 5: Process each file
print("\nProcessing docx files...")
all_questions = []  # list of dicts with all fields

# We need to process files in order and track the question number within each file
# First, build a mapping of file -> sorted list of global qids
file_qids = defaultdict(list)
for qid in sorted(qid_to_file.keys()):
    fname = qid_to_file[qid]
    file_qids[fname].append(qid)

# Process files in alphabetical order (same order as DOCX_FILES)
next_id_num = 447  # DABT-0447 is the first ID
output_rows = []

for fname in DOCX_FILES:
    filepath = os.path.join(BASE_DIR, fname)
    if not os.path.exists(filepath):
        print(f"  SKIP: {fname} not found")
        continue
    
    expected_qids = file_qids.get(fname, [])
    if not expected_qids:
        print(f"  SKIP: {fname} - no question mapping in answer key")
        continue
    
    print(f"\n  Processing: {fname} ({len(expected_qids)} questions, Q{expected_qids[0]}-Q{expected_qids[-1]})")
    
    # Extract questions
    extracted = extract_questions_v2(filepath, set(expected_qids))
    print(f"    Extracted {len(extracted)} questions")
    
    source_name = source_exam_name(fname)
    topic = get_topic(source_name)
    
    # Sort extracted questions by their global ID
    for qnum_in_file, global_qid in enumerate(sorted(expected_qids), 1):
        qinfo = extracted.get(global_qid, {})
        question_text = qinfo.get('question', '')
        options = qinfo.get('options', {})
        option_order = qinfo.get('option_order', [])
        
        if not question_text:
            print(f"    WARNING: Q{global_qid} - no question text extracted")
        
        # Get correct answer
        correct_letter = answer_key.get(global_qid, {}).get('answer', '')
        correct_text = options.get(correct_letter, '')
        
        # Build the row
        dabt_id = f"DABT-{next_id_num:04d}"
        next_id_num += 1
        
        row = OrderedDict()
        row['ID'] = dabt_id
        row['Source Exam'] = source_name
        row['Question #'] = qnum_in_file
        row['Question'] = question_text
        row['A'] = options.get('A', '')
        row['B'] = options.get('B', '')
        row['C'] = options.get('C', '')
        row['D'] = options.get('D', '')
        row['E'] = options.get('E', '')
        row['F'] = options.get('F', '')
        row['G'] = options.get('G', '')
        row['H'] = options.get('H', '')
        row['Correct Answer'] = correct_letter
        row['Correct Answer Text'] = correct_text
        row['Explanation'] = ''
        row['Topic (Primary)'] = topic
        row['All Topics'] = topic
        row['Source File'] = fname
        
        output_rows.append(row)
    
    # Report extraction quality
    missing = set(expected_qids) - set(extracted.keys())
    if missing:
        print(f"    MISSING: {len(missing)} questions not extracted: Q{min(missing)}-Q{max(missing)}")
    
    # Check which extracted questions have no text
    no_text = [qid for qid, q in extracted.items() if not q['question']]
    if no_text:
        print(f"    NO TEXT: {len(no_text)} questions with empty text")
    
    # Check which extracted questions have no options
    no_opts = [qid for qid, q in extracted.items() if not q['options']]
    if no_opts:
        print(f"    NO OPTIONS: {len(no_opts)} questions with no options extracted")

# Step 6: Write CSV
print(f"\n\nWriting CSV to {OUTPUT_CSV}...")
fieldnames = list(output_rows[0].keys()) if output_rows else []
with open(OUTPUT_CSV, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in output_rows:
        writer.writerow(row)

print(f"  Written {len(output_rows)} questions")
print(f"  ID range: {output_rows[0]['ID']} to {output_rows[-1]['ID']}")
print(f"  Files processed: {len(DOCX_FILES)}")
print("\nDONE!")
