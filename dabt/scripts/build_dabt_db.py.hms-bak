#!/usr/bin/env python3
"""
Build comprehensive DABT SQLite database from all source files.
"""
import sqlite3
import csv
import openpyxl
import os
import sys
import re
import hashlib
from datetime import datetime

# === Configuration ===
DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
LOG_PATH = "/root/dabt_import_log.txt"
STATS_PATH = "/root/dabt_db_stats.txt"
EXISTING_XLSX = "/root/work/dabt/dabt-tutor/reference/data/DABT_Practice_Questions_Database.xlsx"
CLASSIFICATION_CSV = "/root/work/dabt/dabt-tutor/reference/data/question_classifications.csv"
CSV_2000Q = "/tmp/dabt_extract_2000q.csv"
CSV_CHAPTER = "/tmp/dabt_extract_chapter.csv"
CSV_MINI = "/tmp/dabt_extract_mini.csv"
CSV_TOPIC = "/tmp/dabt_extract_topic.csv"
PAST_ABT_XLSX = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams/2008-2014_Compiled_Recert_Exams.xlsx"
PAST_ABT_DIR = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams"

# Domain by topic mapping
DOMAIN_BY_TOPIC = {
    "General Principles & Concepts": "Domain I",
    "General Toxicology": "Domain I",
    "Toxicokinetics / ADME": "Domain I",
    "Biotransformation / Metabolism": "Domain II",
    "Mechanisms of Toxicity": "Domain II",
    "Carcinogenesis & Mutagenesis": "Domain II",
    "Genotoxicity / DNA Damage": "Domain II",
    "Risk Assessment & Regulatory": "Domain III",
    "Liver / Hepatotoxicity": "Domain IV",
    "Kidney / Nephrotoxicity": "Domain IV",
    "Hematology & Blood Toxicity": "Domain IV",
    "Immunotoxicology / Allergy": "Domain IV",
    "Lung / Pulmonary Toxicity": "Domain IV",
    "Nervous System / Neurotoxicity": "Domain IV",
    "Eye / Ocular Toxicity": "Domain IV",
    "Cardiovascular Toxicity": "Domain IV",
    "Skin / Dermatotoxicity": "Domain IV",
    "Endocrine Toxicology": "Domain IV",
    "Reproductive & Developmental Toxicity": "Domain IV",
    "Metals & Metalloids": "Domain IV",
    "Solvents & Hydrocarbons": "Domain IV",
    "Pesticides – Insecticides": "Domain IV",
    "Air Pollution & Particulates": "Domain IV",
    "Plant Toxins": "Domain IV",
    "Food Additives, Cosmetics & GRAS": "Domain IV",
    "Drugs & Therapeutics – Toxicology": "Domain IV",
    "Alcohols & Methanol/Ethanol": "Domain IV",
    "Radiation / UV / Ionizing": "Domain IV",
    "Animal & Microbial Venoms / Toxins": "Domain IV",
    "Mycotoxins": "Domain IV",
    "Gases – Asphyxiants & Irritants": "Domain IV",
}

log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

def text_or_none(val):
    """Return stripped string or None for empty/None values."""
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None

def text_or_empty(val):
    """Return stripped string or empty string."""
    if val is None:
        return ""
    return str(val).strip()

def create_tables(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS source_files (
        id INTEGER PRIMARY KEY,
        bank_name TEXT NOT NULL,
        filename TEXT NOT NULL,
        format_type TEXT,
        year TEXT,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        question_text TEXT NOT NULL,
        correct_answer_letter TEXT,
        correct_answer_text TEXT,
        explanation TEXT,
        source_file_id INTEGER,
        question_number_in_source INTEGER,
        bloom_level TEXT,
        FOREIGN KEY (source_file_id) REFERENCES source_files(id)
    );

    CREATE TABLE IF NOT EXISTS answer_options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id TEXT NOT NULL,
        option_letter TEXT NOT NULL,
        option_text TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions(id)
    );

    CREATE TABLE IF NOT EXISTS question_topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions(id)
    );

    CREATE TABLE IF NOT EXISTS question_domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id TEXT NOT NULL,
        domain TEXT NOT NULL,
        sub_domain TEXT,
        task TEXT,
        confidence TEXT,
        FOREIGN KEY (question_id) REFERENCES questions(id)
    );

    CREATE TABLE IF NOT EXISTS match_pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id TEXT NOT NULL,
        term TEXT NOT NULL,
        match_answer TEXT NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions(id)
    );

    CREATE INDEX IF NOT EXISTS idx_q_domain ON question_domains(domain);
    CREATE INDEX IF NOT EXISTS idx_q_topic ON question_topics(topic);
    CREATE INDEX IF NOT EXISTS idx_q_source ON questions(source_file_id);
    """)
    conn.commit()

def parse_options(row, question_id, conn):
    """Parse A through H columns into answer_options table."""
    option_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cursor = conn.cursor()
    for letter in option_letters:
        val = text_or_none(row.get(letter))
        if val:
            cursor.execute(
                "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                (question_id, letter, val)
            )

def parse_topics(row, question_id, conn):
    """Parse Topic (Primary) and All Topics into question_topics table."""
    cursor = conn.cursor()
    primary = text_or_none(row.get('Topic (Primary)'))
    all_topics = text_or_none(row.get('All Topics'))
    
    seen = set()
    if primary and primary not in seen:
        cursor.execute("INSERT INTO question_topics (question_id, topic) VALUES (?, ?)",
                      (question_id, primary))
        seen.add(primary)
    
    if all_topics:
        # Split by comma, semicolon, or pipe
        for t in re.split(r'[;,|]', all_topics):
            t = t.strip()
            if t and t not in seen:
                cursor.execute("INSERT INTO question_topics (question_id, topic) VALUES (?, ?)",
                              (question_id, t))
                seen.add(t)

def load_classifications():
    """Load classification CSV and return dict mapping ID -> classification data."""
    classifications = {}
    if not os.path.exists(CLASSIFICATION_CSV):
        log(f"WARNING: Classification CSV not found at {CLASSIFICATION_CSV}")
        return classifications
    
    with open(CLASSIFICATION_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row.get('ID', '').strip()
            if qid:
                classifications[qid] = {
                    'domain': text_or_none(row.get('Domain')),
                    'sub_domain': text_or_none(row.get('Sub-Domain')),
                    'task': text_or_none(row.get('Task')),
                    'bloom_level': text_or_none(row.get('Bloom Level')),
                    'domain_confidence': text_or_none(row.get('Domain Confidence')),
                    'bloom_confidence': text_or_none(row.get('Bloom Confidence')),
                }
    log(f"Loaded {len(classifications)} classifications from CSV")
    return classifications

def assign_domains(conn, classifications):
    """Assign domains to questions based on classifications or topic mapping."""
    cursor = conn.cursor()
    
    # Get all questions
    cursor.execute("SELECT id FROM questions")
    all_questions = [row[0] for row in cursor.fetchall()]
    
    assigned_count = 0
    topic_mapped_count = 0
    
    for qid in all_questions:
        # Check if domain already assigned via classification
        if qid in classifications:
            cls = classifications[qid]
            if cls['domain']:
                cursor.execute(
                    "INSERT INTO question_domains (question_id, domain, sub_domain, task, confidence) VALUES (?, ?, ?, ?, ?)",
                    (qid, cls['domain'], cls['sub_domain'], cls['task'], cls['domain_confidence'])
                )
                assigned_count += 1
                continue
        
        # Try to assign from topic mapping
        cursor.execute("SELECT topic FROM question_topics WHERE question_id = ?", (qid,))
        topics = [row[0] for row in cursor.fetchall()]
        
        for topic in topics:
            # Try exact match first
            domain = DOMAIN_BY_TOPIC.get(topic)
            if not domain:
                # Try case-insensitive match
                for k, v in DOMAIN_BY_TOPIC.items():
                    if k.lower() == topic.lower():
                        domain = v
                        break
            if not domain:
                # Try partial match
                for k, v in DOMAIN_BY_TOPIC.items():
                    if k.split('/')[0].strip().lower() == topic.lower():
                        domain = v
                        break
            
            if domain:
                cursor.execute(
                    "INSERT OR IGNORE INTO question_domains (question_id, domain, sub_domain, task, confidence) VALUES (?, ?, ?, ?, ?)",
                    (qid, domain, None, None, 'medium')
                )
                topic_mapped_count += 1
                break
    
    conn.commit()
    log(f"Domain assignment: {assigned_count} from classification, {topic_mapped_count} from topic mapping")

def get_question_text_hash(question_text):
    """Create a normalized hash for dedup comparison."""
    # Normalize whitespace, lowercase for comparison
    normalized = ' '.join(question_text.lower().split())
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()

def check_exact_duplicate(question_text, existing_hashes, cursor):
    """Check if question text matches an existing one."""
    qhash = get_question_text_hash(question_text)
    if qhash in existing_hashes:
        return existing_hashes[qhash]
    return None

def load_csv_data(filepath, conn, source_file_id, start_id_num, existing_hashes=None, dedup_field=False):
    """
    Load questions from a CSV file.
    Returns (next_id_num, inserted_count, skipped_count, new_hashes_dict)
    """
    cursor = conn.cursor()
    inserted = 0
    skipped = 0
    new_hashes = {}
    
    if not os.path.exists(filepath):
        log(f"WARNING: File not found: {filepath}")
        return start_id_num, 0, 0, {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_text = text_or_none(row.get('Question'))
            if not question_text:
                skipped += 1
                continue
            
            # Dedup check if needed
            if dedup_field and existing_hashes is not None:
                dup_id = check_exact_duplicate(question_text, existing_hashes, cursor)
                if dup_id:
                    skipped += 1
                    continue
            
            qid = f"DABT-{start_id_num:04d}"
            start_id_num += 1
            
            correct_letter = text_or_none(row.get('Correct Answer'))
            correct_text = text_or_none(row.get('Correct Answer Text'))
            explanation = text_or_none(row.get('Explanation'))
            qnum = text_or_none(row.get('Question #'))
            
            cursor.execute(
                "INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, question_number_in_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (qid, question_text, correct_letter, correct_text, explanation, source_file_id, qnum)
            )
            
            # Parse answer options
            option_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            for letter in option_letters:
                val = text_or_none(row.get(letter))
                if val:
                    cursor.execute(
                        "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                        (qid, letter, val)
                    )
            
            # Parse topics
            parse_topics(row, qid, conn)
            
            inserted += 1
            
            # Track hash for dedup
            qhash = get_question_text_hash(question_text)
            new_hashes[qhash] = qid
            
            # Commit in batches
            if inserted % 100 == 0:
                conn.commit()
    
    conn.commit()
    return start_id_num, inserted, skipped, new_hashes

def load_existing_xlsx(conn, source_file_id):
    """Load the existing 446 questions from the xlsx file."""
    cursor = conn.cursor()
    
    wb = openpyxl.load_workbook(EXISTING_XLSX)
    ws = wb['Questions']
    
    # Get header row
    headers = [ws.cell(1, c).value for c in range(1, 19)]
    
    inserted = 0
    existing_hashes = {}
    
    for r in range(2, ws.max_row + 1):
        row_data = {}
        for c in range(1, 19):
            row_data[headers[c-1]] = ws.cell(r, c).value
        
        qid = text_or_none(row_data.get('ID'))
        if not qid:
            continue
        
        question_text = text_or_none(row_data.get('Question'))
        if not question_text:
            continue
        
        correct_letter = text_or_none(row_data.get('Correct Answer'))
        correct_text = text_or_none(row_data.get('Correct Answer Text'))
        explanation = text_or_none(row_data.get('Explanation'))
        qnum = text_or_none(row_data.get('Question #'))
        
        cursor.execute(
            "INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, question_number_in_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (qid, question_text, correct_letter, correct_text, explanation, source_file_id, qnum)
        )
        
        # Parse answer options
        option_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for letter in option_letters:
            val = text_or_none(row_data.get(letter))
            if val:
                cursor.execute(
                    "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                    (qid, letter, val)
                )
        
        # Parse topics
        parse_topics(row_data, qid, conn)
        
        # Track hash
        qhash = get_question_text_hash(question_text)
        existing_hashes[qhash] = qid
        
        inserted += 1
        
        if inserted % 100 == 0:
            conn.commit()
    
    # Also load bloom_level from classifications if available
    # (will be handled by assign_domains later)
    
    conn.commit()
    log(f"Loaded {inserted} questions from existing xlsx")
    return existing_hashes


def parse_past_abt_exams(conn, source_file_id, start_id_num, existing_hashes):
    """Parse the Past ABT Exams xlsx file with embedded question/answer format."""
    cursor = conn.cursor()
    inserted = 0
    skipped = 0
    
    wb = openpyxl.load_workbook(PAST_ABT_XLSX)
    ws = wb['Sheet1']
    
    for r in range(1, ws.max_row + 1):
        col_a = text_or_empty(ws.cell(r, 1).value)
        col_b = text_or_empty(ws.cell(r, 2).value)
        
        if not col_a:
            continue
        
        # Parse question and options from Col A
        # Format: "Question text...\nA) option1\nB) option2\nC) option3\nD) option4\nE) option5"
        lines = col_a.split('\n')
        
        # Find where options start (A) or A. or A: or A)
        option_start = None
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if re.match(r'^[A-H][\).:]\s', line_stripped) or re.match(r'^[A-H]\)', line_stripped):
                option_start = i
                break
        
        if option_start is None:
            # Maybe it's a matching or other format - try to parse anyway
            # Use entire text as question with no options
            question_text = col_a
            options = {}
        else:
            question_text = '\n'.join(lines[:option_start]).strip()
            # Parse options
            options = {}
            for line in lines[option_start:]:
                line = line.strip()
                m = re.match(r'^([A-H])[\).:]\s*(.*)', line)
                if m:
                    options[m.group(1)] = m.group(2).strip()
        
        # Parse answer and explanation from Col B
        # Format: "Correct Answer = A\n\nDetailed explanation..."
        # or "Answer is D. Explanation..."
        # or "Answer = A\n..."
        correct_letter = None
        explanation = None
        
        if col_b:
            col_b = col_b.strip()
            
            # Try various patterns
            # Pattern 1: "Correct Answer = X" or "Correct Answer: X" or "Answer = X" or "Answer is X."
            m = re.match(r'(?:Correct\s*Answer|Answer)\s*[=:]\s*([A-H])', col_b, re.IGNORECASE)
            if m:
                correct_letter = m.group(1)
            else:
                m = re.match(r'Answer\s+is\s+([A-H])[\.\s]', col_b, re.IGNORECASE)
                if m:
                    correct_letter = m.group(1)
                else:
                    m = re.match(r'^([A-H])[\.\)]\s', col_b)
                    if m:
                        correct_letter = m.group(1)
            
            # Extract explanation - everything after the answer statement
            explanation = col_b
            # Clean up the answer prefix from explanation
            explanation = re.sub(r'^(?:Correct\s*Answer|Answer)\s*[=:]\s*[A-H]\s*\n?\s*', '', explanation, flags=re.IGNORECASE)
            explanation = re.sub(r'^Answer\s+is\s+[A-H][\.\s]*', '', explanation, flags=re.IGNORECASE)
            explanation = re.sub(r'^[A-H][\.\)]\s+', '', explanation)
            explanation = explanation.strip()
        
        if not question_text:
            skipped += 1
            continue
        
        # Dedup check
        qhash = get_question_text_hash(question_text)
        if qhash in existing_hashes:
            skipped += 1
            continue
        
        qid = f"DABT-{start_id_num:04d}"
        start_id_num += 1
        
        cursor.execute(
            "INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, question_number_in_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (qid, question_text, correct_letter, None, explanation, source_file_id, r)
        )
        
        # Insert options
        for letter in sorted(options.keys()):
            cursor.execute(
                "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                (qid, letter, options[letter])
            )
        
        # Try to infer topic from question text for Past ABT exams
        # We'll leave topics empty for these - they'll be inferred from domain mapping
        # or we can do keyword matching
        infer_topic_from_text(question_text, qid, conn)
        
        existing_hashes[qhash] = qid
        inserted += 1
        
        if inserted % 50 == 0:
            conn.commit()
    
    conn.commit()
    log(f"Past ABT Exams: loaded {inserted}, skipped {skipped} (dedup or empty)")
    return start_id_num


def infer_topic_from_text(question_text, qid, conn):
    """Try to infer topic from question text using keyword matching."""
    cursor = conn.cursor()
    
    keyword_topics = {
        "mercury|methylmercury|lead|cadmium|arsenic|chromium|nickel|chelating|chelation": "Metals & Metalloids",
        "carcinogen|mutagen|genotox|dna damage|ames test|micronucleus|sister chromatid": "Carcinogenesis & Mutagenesis",
        "liver|hepatotox|hepatic|biliary|cholestasis|hepatocyte": "Liver / Hepatotoxicity",
        "kidney|renal|nephrotox|glomerular|tubular|nephron": "Kidney / Nephrotoxicity",
        "neurotox|nervous|brain|neuron|synapse|neuropathy|axon|myelin": "Nervous System / Neurotoxicity",
        "skin|dermatotox|dermal|epidermis|contact dermatitis": "Skin / Dermatotoxicity",
        "lung|pulmonary|respirat|inhalation|asthma|bronch|alveoli": "Lung / Pulmonary Toxicity",
        "heart|cardio|cardiovascular|cardiotox|arrhythmia|myocardial": "Cardiovascular Toxicity",
        "reproduc|develop|teratogen|fetotox|embryotox|fertility|placenta": "Reproductive & Developmental Toxicity",
        "endocrine|hormone|thyroid|estrogen|androgen|steroid|adrenal": "Endocrine Toxicology",
        "immunotox|allerg|hypersensitivity|autoimmune|lymphocyte|antibody": "Immunotoxicology / Allergy",
        "blood|hematol|erythrocyte|hemoglobin|anemia|methemoglobin|coagulation": "Hematology & Blood Toxicity",
        "eye|ocular|retina|cataract|corneal|vision|ophthalmic": "Eye / Ocular Toxicity",
        "pesticide|insecticide|herbicide|organophosphate|carbamate|pyrethroid": "Pesticides – Insecticides",
        "solvent|hydrocarbon|benzene|toluene|xylene|acetone|chloroform|methylene": "Solvents & Hydrocarbons",
        "risk assess|hazard|exposure|dose-response|noael|loael|margin of safety|uncertainty factor": "Risk Assessment & Regulatory",
        "toxicokinetic|adme|absorption|distribution|metabolism|excretion|bioavail|half-life": "Toxicokinetics / ADME",
        "biotransform|metabolism|phase i|phase ii|cyp|cytochrome|p450|conjugation": "Biotransformation / Metabolism",
        "mechanism|mode of action|aop|toxicant|receptor|signaling|apoptosis|necrosis": "Mechanisms of Toxicity",
        "alcohol|ethanol|methanol|ethylene glycol|isopropanol": "Alcohols & Methanol/Ethanol",
        "radiation|uv|ionizing|radionuclide|radioactive": "Radiation / UV / Ionizing",
        "plant toxin|phyto|herbal|mushroom|amanita|ricin": "Plant Toxins",
        "venom|snake|spider|scorpion|toxin|animal|microbial|botulinum|tetrodotoxin": "Animal & Microbial Venoms / Toxins",
        "mycotoxin|aflatoxin|ochratoxin|fumonisin|ergot": "Mycotoxins",
        "gas|asphyxiant|irritant|carbon monoxide|cyanide|hydrogen sulfide|chlorine|phosgene": "Gases – Asphyxiants & Irritants",
        "food additive|cosmetic|gras|preservative|additive|contaminant": "Food Additives, Cosmetics & GRAS",
        "drug|therapeutic|acetaminophen|paracetamol|aspirin|digitalis|chemotherapy": "Drugs & Therapeutics – Toxicology",
        "air pollution|particulate|pm2.5|pm10|ozone|smog|diesel": "Air Pollution & Particulates",
    }
    
    qtext_lower = question_text.lower()
    for pattern, topic in keyword_topics.items():
        if re.search(pattern, qtext_lower):
            cursor.execute(
                "INSERT OR IGNORE INTO question_topics (question_id, topic) VALUES (?, ?)",
                (qid, topic)
            )
            return  # Assign first match only


def parse_pdf_files(conn, source_file_id, start_id_num, existing_hashes):
    """Parse PDF files in the Past ABT Exams directory."""
    cursor = conn.cursor()
    inserted = 0
    
    try:
        import fitz  # pymupdf
    except ImportError:
        log("pymupdf not available, skipping PDF parsing")
        return start_id_num
    
    pdf_files = [f for f in os.listdir(PAST_ABT_DIR) if f.endswith('.pdf')]
    
    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(PAST_ABT_DIR, pdf_file)
        log(f"Parsing PDF: {pdf_file}")
        
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text() + "\n\n"
            doc.close()
        except Exception as e:
            log(f"  Error reading PDF {pdf_file}: {e}")
            continue
        
        # Try to identify questions in the PDF
        # Look for patterns like question numbers, "Which of the following", etc.
        lines = full_text.split('\n')
        
        # Simple heuristic: look for blocks that start with a number followed by period,
        # contain "which of the following" or similar question patterns,
        # and have answer options (A) B) C) D) etc.)
        
        questions_found = []
        current_question = []
        in_question = False
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if in_question:
                    questions_found.append('\n'.join(current_question))
                    current_question = []
                    in_question = False
                continue
            
            # Check if line starts a new question (number. text)
            if re.match(r'^\d+[\.\)]\s', stripped) and len(stripped) > 5:
                if in_question:
                    questions_found.append('\n'.join(current_question))
                current_question = [stripped]
                in_question = True
            elif in_question:
                current_question.append(stripped)
        
        # Don't forget the last question
        if in_question and current_question:
            questions_found.append('\n'.join(current_question))
        
        log(f"  Found {len(questions_found)} potential question blocks")
        
        for q_block in questions_found:
            # Extract question text and options
            lines = q_block.split('\n')
            
            option_start = None
            for i, line in enumerate(lines):
                if re.match(r'^[A-H][\).:]\s', line.strip()):
                    option_start = i
                    break
            
            if option_start is None:
                continue
            
            question_text = '\n'.join(lines[:option_start]).strip()
            # Remove leading number
            question_text = re.sub(r'^\d+[\.\)]\s*', '', question_text)
            
            if not question_text or len(question_text) < 10:
                continue
            
            options = {}
            for line in lines[option_start:]:
                line = line.strip()
                m = re.match(r'^([A-H])[\).:]\s*(.*)', line)
                if m:
                    options[m.group(1)] = m.group(2).strip()
            
            if len(options) < 2:
                continue
            
            # Dedup
            qhash = get_question_text_hash(question_text)
            if qhash in existing_hashes:
                continue
            
            qid = f"DABT-{start_id_num:04d}"
            start_id_num += 1
            
            cursor.execute(
                "INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, question_number_in_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (qid, question_text, None, None, None, source_file_id, None)
            )
            
            for letter in sorted(options.keys()):
                cursor.execute(
                    "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                    (qid, letter, options[letter])
                )
            
            # Try to infer topic
            infer_topic_from_text(question_text, qid, conn)
            
            existing_hashes[qhash] = qid
            inserted += 1
            
            if inserted % 50 == 0:
                conn.commit()
        
        conn.commit()
        log(f"  Inserted {inserted} questions from {pdf_file}")
    
    return start_id_num


def parse_docx_files(conn, source_file_id, start_id_num, existing_hashes):
    """Parse .docx files that might contain questions."""
    cursor = conn.cursor()
    inserted = 0
    
    try:
        from docx import Document
    except ImportError:
        log("python-docx not available, skipping docx parsing")
        return start_id_num
    
    # Check Past ABT directory and subdirectories for docx files
    for root_dir, dirs, files in os.walk(PAST_ABT_DIR):
        for filename in files:
            if filename.endswith('.docx'):
                filepath = os.path.join(root_dir, filename)
                log(f"Parsing DOCX: {filepath}")
                
                try:
                    doc = Document(filepath)
                    full_text = []
                    for para in doc.paragraphs:
                        full_text.append(para.text)
                    text = '\n'.join(full_text)
                except Exception as e:
                    log(f"  Error: {e}")
                    continue
                
                # Similar question extraction as PDF
                lines = text.split('\n')
                questions_found = []
                current_question = []
                in_question = False
                
                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        if in_question:
                            questions_found.append('\n'.join(current_question))
                            current_question = []
                            in_question = False
                        continue
                    
                    if re.match(r'^\d+[\.\)]\s', stripped) and len(stripped) > 5:
                        if in_question:
                            questions_found.append('\n'.join(current_question))
                        current_question = [stripped]
                        in_question = True
                    elif in_question:
                        current_question.append(stripped)
                
                if in_question and current_question:
                    questions_found.append('\n'.join(current_question))
                
                for q_block in questions_found:
                    lines = q_block.split('\n')
                    option_start = None
                    for i, line in enumerate(lines):
                        if re.match(r'^[A-H][\).:]\s', line.strip()):
                            option_start = i
                            break
                    
                    if option_start is None:
                        continue
                    
                    question_text = '\n'.join(lines[:option_start]).strip()
                    question_text = re.sub(r'^\d+[\.\)]\s*', '', question_text)
                    
                    if not question_text or len(question_text) < 10:
                        continue
                    
                    options = {}
                    for line in lines[option_start:]:
                        line = line.strip()
                        m = re.match(r'^([A-H])[\).:]\s*(.*)', line)
                        if m:
                            options[m.group(1)] = m.group(2).strip()
                    
                    if len(options) < 2:
                        continue
                    
                    qhash = get_question_text_hash(question_text)
                    if qhash in existing_hashes:
                        continue
                    
                    qid = f"DABT-{start_id_num:04d}"
                    start_id_num += 1
                    
                    cursor.execute(
                        "INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, question_number_in_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (qid, question_text, None, None, None, source_file_id, None)
                    )
                    
                    for letter in sorted(options.keys()):
                        cursor.execute(
                            "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                            (qid, letter, options[letter])
                        )
                    
                    infer_topic_from_text(question_text, qid, conn)
                    
                    existing_hashes[qhash] = qid
                    inserted += 1
                    
                    if inserted % 50 == 0:
                        conn.commit()
                
                conn.commit()
    
    return start_id_num


def verify_database(conn):
    """Run verification queries and generate stats."""
    cursor = conn.cursor()
    
    stats = []
    
    # Total questions
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_q = cursor.fetchone()[0]
    stats.append(f"Total questions: {total_q}")
    
    # Distribution by source
    stats.append("\n=== Distribution by Source ===")
    cursor.execute("""
        SELECT sf.bank_name, COUNT(*) as cnt
        FROM questions q
        JOIN source_files sf ON q.source_file_id = sf.id
        GROUP BY sf.id
        ORDER BY cnt DESC
    """)
    for row in cursor.fetchall():
        stats.append(f"  {row[0]}: {row[1]}")
    
    # Distribution by domain
    stats.append("\n=== Distribution by Domain ===")
    cursor.execute("""
        SELECT domain, COUNT(*) as cnt
        FROM question_domains
        GROUP BY domain
        ORDER BY cnt DESC
    """)
    for row in cursor.fetchall():
        stats.append(f"  {row[0]}: {row[1]}")
    
    # Questions without domains
    cursor.execute("""
        SELECT COUNT(*) FROM questions q
        WHERE NOT EXISTS (SELECT 1 FROM question_domains d WHERE d.question_id = q.id)
    """)
    no_domain = cursor.fetchone()[0]
    stats.append(f"  (No domain assigned: {no_domain})")
    
    # Top topics
    stats.append("\n=== Top 15 Topics ===")
    cursor.execute("""
        SELECT topic, COUNT(*) as cnt
        FROM question_topics
        GROUP BY topic
        ORDER BY cnt DESC
        LIMIT 15
    """)
    for row in cursor.fetchall():
        stats.append(f"  {row[0]}: {row[1]}")
    
    # Answer options count
    cursor.execute("SELECT COUNT(*) FROM answer_options")
    stats.append(f"\nTotal answer options: {cursor.fetchone()[0]}")
    
    # Questions with no answer options
    cursor.execute("""
        SELECT COUNT(*) FROM questions q
        WHERE NOT EXISTS (SELECT 1 FROM answer_options a WHERE a.question_id = q.id)
    """)
    stats.append(f"Questions with no options: {cursor.fetchone()[0]}")
    
    # Spot check: 5 random questions
    stats.append("\n=== Spot Check (5 random questions) ===")
    cursor.execute("""
        SELECT q.id, q.question_text, q.correct_answer_letter, 
               (SELECT COUNT(*) FROM answer_options a WHERE a.question_id = q.id) as opt_count,
               sf.bank_name
        FROM questions q
        JOIN source_files sf ON q.source_file_id = sf.id
        ORDER BY RANDOM()
        LIMIT 5
    """)
    for row in cursor.fetchall():
        stats.append(f"\n  {row[0]} (from {row[4]})")
        qtext = (row[1][:100] + '...') if len(row[1]) > 100 else row[1]
        stats.append(f"    Question: {qtext}")
        stats.append(f"    Correct: {row[2]}")
        stats.append(f"    Options: {row[3]}")
        
        # Verify options
        cursor.execute("SELECT option_letter, option_text FROM answer_options WHERE question_id = ? ORDER BY option_letter", (row[0],))
        for opt in cursor.fetchall():
            otext = (opt[1][:60] + '...') if len(opt[1]) > 60 else opt[1]
            stats.append(f"    {opt[0]}: {otext}")
    
    return '\n'.join(stats)


def main():
    log(f"=== DABT Database Build - {datetime.now().isoformat()} ===")
    
    # Remove old database if exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        log(f"Removed existing database at {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    
    # Create tables
    create_tables(conn)
    log("Tables created")
    
    classifications = load_classifications()
    
    # ==========================================
    # Step 1: Insert source files
    # ==========================================
    cursor = conn.cursor()
    source_files = [
        (1, "Mini-ABT 1-11", "DABT_Practice_Questions_Database.xlsx", "mini-exam", "2024-2025", "Mini-ABT Practice Exams 1–11 (existing DB)"),
        (2, "2000Q Bank", "dabt_extract_2000q.csv", "comprehensive", "2024", "2000 Q practice bank"),
        (3, "Chapter Tests", "dabt_extract_chapter.csv", "chapter-based", "2024", "Chapter-based practice tests"),
        (4, "Kristen Mini Exams", "dabt_extract_mini.csv", "mini-exam", "2024", "Kristen's mini practice exams"),
        (5, "Kristen Topic Tests", "dabt_extract_topic.csv", "topic-based", "2024", "Kristen's topic-specific tests"),
        (6, "Past ABT Exams (2008-2014)", "2008-2014_Compiled_Recert_Exams.xlsx", "real-exam", "2008-2014", "Compiled recertification exams"),
        (7, "Past ABT Exams (PDFs)", "various PDFs", "real-exam", "2012-2017", "Additional past exam PDFs"),
    ]
    for sf in source_files:
        cursor.execute(
            "INSERT INTO source_files (id, bank_name, filename, format_type, year, description) VALUES (?, ?, ?, ?, ?, ?)",
            sf
        )
    conn.commit()
    log("Source files inserted")
    
    # ==========================================
    # Step 2: Load existing 446 questions (Mini-ABT 1-11)
    # ==========================================
    log("\n--- Step 1/2: Loading existing DB (Mini-ABT 1-11) ---")
    existing_hashes = load_existing_xlsx(conn, 1)
    log(f"Existing hashes: {len(existing_hashes)}")
    
    # ==========================================
    # Step 3: Load 2000Q Bank (DABT-0447 onward)
    # ==========================================
    log("\n--- Step 3: Loading 2000Q Bank ---")
    next_id, inserted, skipped, new_hashes = load_csv_data(CSV_2000Q, conn, 2, 447, existing_hashes)
    existing_hashes.update(new_hashes)
    log(f"2000Q Bank: inserted {inserted}, skipped {skipped}, next_id=DABT-{next_id:04d}")
    
    # ==========================================
    # Step 4: Load Chapter Tests
    # ==========================================
    log("\n--- Step 4: Loading Chapter Tests ---")
    next_id, inserted, skipped, new_hashes = load_csv_data(CSV_CHAPTER, conn, 3, next_id, existing_hashes)
    existing_hashes.update(new_hashes)
    log(f"Chapter Tests: inserted {inserted}, skipped {skipped}, next_id=DABT-{next_id:04d}")
    
    # ==========================================
    # Step 5: Load Kristen Mini Exams (dedup against existing 446 Mini-ABT 1-11)
    # ==========================================
    log("\n--- Step 5: Loading Kristen Mini Exams (with dedup) ---")
    mini_next_id = next_id
    mini_inserted = 0
    mini_skipped = 0
    
    cursor = conn.cursor()
    with open(CSV_MINI, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_text = text_or_none(row.get('Question'))
            if not question_text:
                mini_skipped += 1
                continue
            
            # Dedup against existing
            qhash = get_question_text_hash(question_text)
            if qhash in existing_hashes:
                mini_skipped += 1
                continue
            
            qid = f"DABT-{mini_next_id:04d}"
            mini_next_id += 1
            
            correct_letter = text_or_none(row.get('Correct Answer'))
            correct_text = text_or_none(row.get('Correct Answer Text'))
            explanation = text_or_none(row.get('Explanation'))
            qnum = text_or_none(row.get('Question #'))
            
            cursor.execute(
                "INSERT INTO questions (id, question_text, correct_answer_letter, correct_answer_text, explanation, source_file_id, question_number_in_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (qid, question_text, correct_letter, correct_text, explanation, 4, qnum)
            )
            
            option_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            for letter in option_letters:
                val = text_or_none(row.get(letter))
                if val:
                    cursor.execute(
                        "INSERT INTO answer_options (question_id, option_letter, option_text) VALUES (?, ?, ?)",
                        (qid, letter, val)
                    )
            
            parse_topics(row, qid, conn)
            existing_hashes[qhash] = qid
            mini_inserted += 1
            
            if mini_inserted % 100 == 0:
                conn.commit()
    
    conn.commit()
    next_id = mini_next_id
    log(f"Kristen Mini Exams: inserted {mini_inserted}, skipped {mini_skipped} (dedup)")
    
    # ==========================================
    # Step 6: Load Kristen Topic Tests
    # ==========================================
    log("\n--- Step 6: Loading Kristen Topic Tests ---")
    next_id, inserted, skipped, new_hashes = load_csv_data(CSV_TOPIC, conn, 5, next_id, existing_hashes)
    existing_hashes.update(new_hashes)
    log(f"Kristen Topic Tests: inserted {inserted}, skipped {skipped}, next_id=DABT-{next_id:04d}")
    
    # ==========================================
    # Step 7: Load Past ABT Exams (xlsx)
    # ==========================================
    log("\n--- Step 7: Loading Past ABT Exams (2008-2014) ---")
    next_id = parse_past_abt_exams(conn, 6, next_id, existing_hashes)
    
    # ==========================================
    # Step 8: Parse PDF files
    # ==========================================
    log("\n--- Step 8: Parsing PDF files ---")
    next_id = parse_pdf_files(conn, 7, next_id, existing_hashes)
    
    # ==========================================
    # Step 9: Parse DOCX files
    # ==========================================
    log("\n--- Step 9: Parsing DOCX files ---")
    next_id = parse_docx_files(conn, 7, next_id, existing_hashes)
    
    # ==========================================
    # Step 10: Assign domains
    # ==========================================
    log("\n--- Step 10: Assigning domains ---")
    assign_domains(conn, classifications)
    
    # ==========================================
    # Step 11: Verify and generate stats
    # ==========================================
    log("\n--- Step 11: Verification ---")
    stats_text = verify_database(conn)
    
    # Write stats file
    with open(STATS_PATH, 'w') as f:
        f.write(stats_text)
    log(f"\nStats written to {STATS_PATH}")
    
    # Write log
    with open(LOG_PATH, 'w') as f:
        f.write('\n'.join(log_lines))
    log(f"Log written to {LOG_PATH}")
    
    conn.close()
    log("\n=== DABT Database Build Complete ===")


if __name__ == '__main__':
    main()
