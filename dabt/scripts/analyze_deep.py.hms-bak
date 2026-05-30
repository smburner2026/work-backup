#!/usr/bin/env python3
"""
OCR-based analysis of Mid-Amer Tox Course Topic Summaries PDFs.
Also deep-checks ACT Course lectures for practice questions.
"""
import os, sys, json, re
from collections import OrderedDict

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

# Try pytesseract
try:
    import pytesseract
    from PIL import Image
    import io
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

def ocr_pdf_with_pymupdf(path):
    """Extract text from scanned PDF using PyMuPDF to render pages + Tesseract OCR."""
    doc = fitz.open(path)
    full_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render page to image at 200 DPI
        pix = page.get_pixmap(dpi=200)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(img)
        full_text.append(f"--- Page {page_num+1} ---\n{text}")
    doc.close()
    return "\n".join(full_text), len(doc)

def extract_text_fallback(path):
    """Try PyMuPDF text extraction first, fall back to OCR if needed."""
    if not fitz:
        return None, 0
    
    doc = fitz.open(path)
    n_pages = len(doc)
    
    # First try extracting text directly
    text_parts = []
    has_text = False
    for page in doc:
        t = page.get_text()
        if t.strip():
            has_text = True
        text_parts.append(t)
    
    text = "\n".join(text_parts)
    
    if not has_text and HAS_OCR:
        print(f"  -> No text found, attempting OCR...")
        doc.close()
        text, n_pages = ocr_pdf_with_pymupdf(path)
        return text, n_pages
    
    doc.close()
    return text, n_pages

# ---- DABT Exam Domains ----
DABT_DOMAINS = OrderedDict([
    ("1_General_Principles", {
        "code": "I",
        "name": "General Principles of Toxicology",
        "subtopics": [
            "Dose-response", "Toxicologic pathology", "Mechanisms of toxicity",
            "Absorption, distribution, excretion", "Biotransformation",
            "Toxicokinetics", "Chemical carcinogenesis", "Genetic toxicology"
        ]
    }),
    ("2_Systemic_Tox", {
        "code": "II",
        "name": "Systemic Toxicology",
        "subtopics": [
            "Hematopoietic", "Hepatotoxicity", "Nephrotoxicity",
            "Respiratory", "Neurotoxicity", "Ocular", "Dermal",
            "Reproductive & developmental", "Cardiovascular",
            "Endocrine", "Immunotoxicity"
        ]
    }),
    ("3_Agent_Tox", {
        "code": "III",
        "name": "Toxic Agents",
        "subtopics": [
            "Metals", "Pesticides", "Solvents & vapors",
            "Food toxicology", "Natural products/toxins",
            "Radiation", "Environmental toxicants"
        ]
    }),
    ("4_Applied_Tox", {
        "code": "IV",
        "name": "Applied Toxicology",
        "subtopics": [
            "Analytical/forensic", "Clinical toxicology",
            "Occupational toxicology", "Ecotoxicology",
            "Risk assessment", "Regulatory guidelines",
            "Epidemiology"
        ]
    })
])

def identify_topics(text, title):
    """Identify main topics covered in the text."""
    topics = []
    text_lower = text.lower()
    
    topic_keywords = {
        "Dose-Response": ["dose-response", "dose response", "dose-effect", "ld50", "lc50", "noael", "loael"],
        "Mechanisms of Toxicity": ["mechanism", "toxicant action", "toxicity pathway", "mode of action", "molecular mechanism"],
        "ADME": ["absorption", "distribution", "excretion", "adme", "bioavailab"],
        "Toxicokinetics": ["toxicokinetic", "pharmacokinetic", "compartment model", "half-life", "clearance", "volume of distribution"],
        "Biotransformation": ["biotransformation", "metabolism", "phase i", "phase ii", "cyp450", "cytochrome", "conjugation", "oxidation", "reduction", "hydrolysis"],
        "Chemical Carcinogenesis": ["carcinogen", "cancer", "tumor", "neoplas", "oncogene", "initiation", "promotion", "progression"],
        "Genetic Toxicology": ["genotox", "mutagen", "ames test", "chromosomal aberration", "dna damage", "micronucleus", "comet assay"],
        "Hematopoietic Toxicity": ["hematopoi", "blood", "erythrocyte", "anemia", "methemoglobin", "hemoglobin", "bone marrow"],
        "Hepatotoxicity": ["hepatotox", "liver", "hepatic", "cholestasis", "steatosis", "necrosis"],
        "Nephrotoxicity": ["nephrotox", "kidney", "renal", "glomerul", "tubular necrosis"],
        "Respiratory Toxicity": ["respirat", "lung", "pulmonary", "inhalation", "bronch", "alveol", "pneumotox"],
        "Neurotoxicity": ["neurotox", "nervous system", "neuron", "neuropath", "axon", "myelin", "brain"],
        "Ocular Toxicity": ["ocular", "eye", "visual", "retina", "cornea", "cataract"],
        "Dermal Toxicity": ["dermal", "skin", "dermatotox", "irritation", "sensitization", "percutaneous"],
        "Reproductive & Developmental Toxicity": ["repro", "developmental", "teratogen", "fertility", "fetal", "embryo", "placenta"],
        "Cardiovascular Toxicity": ["cardiovasc", "heart", "cardiotox", "arrhythmia", "vascular"],
        "Endocrine Toxicity": ["endocrine", "hormone", "thyroid", "estrogen", "androgen", "steroid"],
        "Immunotoxicity": ["immunotox", "immune", "hypersensitivity", "immunosuppression", "allerg"],
        "Metals Toxicology": ["metal", "lead", "mercury", "cadmium", "arsenic", "chromium", "nickel"],
        "Pesticides": ["pesticide", "insecticide", "herbicide", "fungicide", "organophosphate", "carbamate", "pyrethroid", "organochlorine"],
        "Solvents & Vapors": ["solvent", "vapor", "benzene", "toluene", "xylene", "trichloroethylene", "methanol", "ethanol"],
        "Food Toxicology": ["food toxic", "food additive", "contaminant", "mycotoxin", "aflatoxin", "botulism"],
        "Natural Products & Toxins": ["venom", "toxin", "snake", "spider", "plant", "mushroom", "phycotoxin"],
        "Radiation": ["radiation", "radionuclide", "ionizing"],
        "Forensic Toxicology": ["forensic", "analytical", "drug testing", "postmortem", "chain of custody"],
        "Clinical Toxicology": ["clinical", "antidote", "poison", "overdose", "toxidrome"],
        "Occupational Toxicology": ["occupational", "workplace", "exposure limit", "industrial hygiene", "tlv", "pel"],
        "Ecotoxicology": ["ecotox", "environmental toxic", "aquatic", "avian", "wildlife", "food chain"],
        "Risk Assessment": ["risk assessment", "hazard identification", "exposure assessment", "risk characterization", "uncertainty factor"],
        "Regulatory": ["regulatory", "ich", "oecd", "fda", "epa", "glp", "guideline"],
        "Epidemiology": ["epidemiology", "cohort", "case-control", "cross-sectional", "odds ratio"],
    }
    
    for topic, keywords in topic_keywords.items():
        score = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower))
        if score > 0:
            topics.append({"topic": topic, "keyword_matches": score})
    
    topics.sort(key=lambda x: x["keyword_matches"], reverse=True)
    return topics

def map_to_dabt_domain(topics):
    """Map identified topics to DABT exam domains."""
    domain_mapping = {
        "Dose-Response": "1_General_Principles",
        "Mechanisms of Toxicity": "1_General_Principles",
        "ADME": "1_General_Principles",
        "Toxicokinetics": "1_General_Principles",
        "Biotransformation": "1_General_Principles",
        "Chemical Carcinogenesis": "1_General_Principles",
        "Genetic Toxicology": "1_General_Principles",
        "Hematopoietic Toxicity": "2_Systemic_Tox",
        "Hepatotoxicity": "2_Systemic_Tox",
        "Nephrotoxicity": "2_Systemic_Tox",
        "Respiratory Toxicity": "2_Systemic_Tox",
        "Neurotoxicity": "2_Systemic_Tox",
        "Ocular Toxicity": "2_Systemic_Tox",
        "Dermal Toxicity": "2_Systemic_Tox",
        "Reproductive & Developmental Toxicity": "2_Systemic_Tox",
        "Cardiovascular Toxicity": "2_Systemic_Tox",
        "Endocrine Toxicity": "2_Systemic_Tox",
        "Immunotoxicity": "2_Systemic_Tox",
        "Metals Toxicology": "3_Agent_Tox",
        "Pesticides": "3_Agent_Tox",
        "Solvents & Vapors": "3_Agent_Tox",
        "Food Toxicology": "3_Agent_Tox",
        "Natural Products & Toxins": "3_Agent_Tox",
        "Radiation": "3_Agent_Tox",
        "Forensic Toxicology": "4_Applied_Tox",
        "Clinical Toxicology": "4_Applied_Tox",
        "Occupational Toxicology": "4_Applied_Tox",
        "Ecotoxicology": "4_Applied_Tox",
        "Risk Assessment": "4_Applied_Tox",
        "Regulatory": "4_Applied_Tox",
        "Epidemiology": "4_Applied_Tox",
    }
    
    domains_hit = set()
    for t in topics:
        d = domain_mapping.get(t["topic"])
        if d:
            domains_hit.add(d)
    return sorted(domains_hit)

def has_practice_questions(text):
    """Detect if the document contains embedded practice questions/quizzes."""
    indicators = []
    q_patterns = [
        r'(?i)(practice\s+(questions|exam|test|quiz|problems))',
        r'(?i)(multiple\s+choice\s+questions?)',
        r'(?i)(self[- ]assessment\s+questions?)',
        r'(?i)(review\s+questions?)',
        r'(?i)(study\s+questions?)',
        r'(?i)(sample\s+exam\s+questions?)',
        r'(?i)(test\s+your\s+(knowledge|understanding))',
        r'(?i)(questions?\s+(for|to)\s+consider)',
        r'(?i)(answers?\s+(to|for|provided))',
        r'(?i)(which\s+of\s+the\s+following\s+(is|are|would|does|correct|not|true|false))',
    ]
    for p in q_patterns:
        m = re.search(p, text)
        if m:
            indicators.append(m.group(0)[:80])
    
    # Count question-like lines (numbered items ending with ?)
    q_lines = len(re.findall(r'^\s*\d+[\.\)]\s+[A-Z][a-z].*\?', text, re.MULTILINE))
    
    return {
        "has_questions": len(indicators) > 0 or q_lines > 3,
        "indicators": indicators[:5],
        "approx_question_lines": q_lines
    }

def analyze_topic_summary_pdf(path):
    """Analyze Mid-Amer Tox Course Topic Summary PDF (with OCR fallback)."""
    basename = os.path.basename(path)
    size = os.path.getsize(path)
    
    text, n_pages = extract_text_fallback(path)
    
    if text is None or not text.strip():
        return {"file": basename, "error": "No text extracted (OCR unavailable)", "pages": n_pages if n_pages else 0}
    
    # Use first meaningful text as identifier
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 15]
    
    topics = identify_topics(text, basename)
    questions = has_practice_questions(text)
    domains = map_to_dabt_domain(topics)
    
    return {
        "file": basename,
        "pages": n_pages,
        "size_bytes": size,
        "size_mb": round(size / (1024*1024), 2),
        "topics_found": topics[:10],
        "topics_count": len(topics),
        "practice_questions": questions,
        "dabt_domains": domains,
        "sample_text": lines[:5] if lines else ["No readable content"],
    }

def deep_check_lecture_questions(path):
    """Deep-check an ACT lecture PDF for embedded practice questions or quiz sections."""
    if not fitz:
        return None
    
    doc = fitz.open(path)
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    text = "\n".join(text_parts)
    n_pages = len(doc)
    doc.close()
    
    # More thorough question detection
    # Look at last 20% of pages for quiz/review sections
    total_lines = text.split('\n')
    
    # Check for common quiz section headers
    quiz_headers = re.findall(r'^\s*(Review Questions?|Study Questions?|Practice (Questions|Exam|Test|Quiz)|Sample Questions?|Self[ -]Assessment|Check Your (Knowledge|Understanding)|Questions? (for|to) Consider|Discussion Questions?|Exam Questions?|Test Your Knowledge)', text, re.MULTILINE | re.IGNORECASE)
    
    # Check for answer keys
    answer_keys = re.findall(r'^\s*(Answer[s]?\s*(Key|s)?:|Answers?\s*(to|for)\s+(Review|Practice|Study|Sample)\s+(Questions?|Problems?))', text, re.MULTILINE | re.IGNORECASE)
    
    # Check for numbered questions (e.g., "1. Which of the following...")
    numbered_questions = re.findall(r'^\s*(\d+)\.\s+[A-Z].*\?', text, re.MULTILINE)
    
    # Check for MCQ answer choices
    mcq_choices = re.findall(r'^\s*[A-E][\)\.]\s+', text, re.MULTILINE)
    
    # Check for "Questions" slide at end
    has_questions_slide = bool(re.search(r'(?i)(?:Questions?|Quiz|Exam|Review)\s*(?:and\s*Answers?)?\s*$', text[:2000] if len(text) > 2000 else text))
    
    return {
        "quiz_headers_found": quiz_headers[:5] if quiz_headers else [],
        "answer_keys_found": answer_keys[:3] if answer_keys else [],
        "numbered_questions_count": len(numbered_questions),
        "mcq_choice_lines_count": len(mcq_choices),
        "has_dedicated_quiz_headers": len(quiz_headers) > 0,
        "total_pages": n_pages,
        "text_length": len(text),
    }

if __name__ == "__main__":
    base = "/root/dabt-curated"
    
    # Deep-check ACT lectures for questions
    print("=" * 70)
    print("ACT COURSE 2018 - DEEP QUESTION CHECK")
    print("=" * 70)
    act_dir = os.path.join(base, "ACT_Course_2018", "Lectures")
    
    all_act_deep = []
    for f in sorted(os.listdir(act_dir)):
        if f.endswith(".pdf"):
            fp = os.path.join(act_dir, f)
            r = deep_check_lecture_questions(fp)
            if r:
                print(f"\n{f}:")
                print(f"  Pages: {r['total_pages']}, Text: {r['text_length']:,} chars")
                print(f"  Quiz headers: {r['quiz_headers_found']}")
                print(f"  Answer keys: {r['answer_keys_found']}")
                print(f"  Numbered questions: {r['numbered_questions_count']}")
                print(f"  MCQ choice lines: {r['mcq_choice_lines_count']}")
                print(f"  Has dedicated quiz section: {r['has_dedicated_quiz_headers']}")
                all_act_deep.append({"file": f, **r})
    
    # OCR Mid-Amer Topic Summaries
    print("\n\n" + "=" * 70)
    print("MID-AMER TOX COURSE - OCR ANALYSIS")
    print("=" * 70)
    midamer_dir = os.path.join(base, "Mid-Amer_Tox_Course", "Topic_Summaries")
    
    all_midamer = []
    for f in sorted(os.listdir(midamer_dir)):
        if f.endswith(".pdf"):
            fp = os.path.join(midamer_dir, f)
            print(f"\nAnalyzing {f}...")
            r = analyze_topic_summary_pdf(fp)
            print(f"  Pages: {r.get('pages', '?')} | Size: {r.get('size_mb', '?')} MB")
            if "error" in r:
                print(f"  ERROR: {r['error']}")
            else:
                print(f"  Topics ({r['topics_count']}): {[t['topic'] for t in r['topics_found'][:6]]}")
                print(f"  Has Questions: {r['practice_questions']['has_questions']}")
                print(f"  Sample: {r['sample_text'][:2]}")
            all_midamer.append(r)
    
    # Save
    output = {
        "act_lectures_deep_question_check": all_act_deep,
        "midamer_ocr_analysis": all_midamer,
    }
    with open("/root/dabt_analysis_deep.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nDeep results saved to /root/dabt_analysis_deep.json")
