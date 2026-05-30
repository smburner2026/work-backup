#!/usr/bin/env python3
"""
Deep content analysis of ACT Course 2018 and Mid-Amer Tox Course PDFs.
Extracts text, identifies topics, page counts, and practice questions.
"""
import os, sys, json, re
from collections import OrderedDict

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) not available, falling back to pdfminer")
    fitz = None

# ---- DABT Exam Domains (from the official blueprint) ----
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

def extract_pymupdf(path):
    """Extract text and metadata using PyMuPDF."""
    doc = fitz.open(path)
    text_pages = []
    for page in doc:
        text_pages.append(page.get_text())
    full_text = "\n".join(text_pages)
    n_pages = len(doc)
    doc.close()
    return full_text, n_pages

def has_practice_questions(text):
    """Detect if the document contains embedded practice questions/quizzes."""
    indicators = []
    # Look for question patterns
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
        r'^\s*\d+[\.\)]\s+[A-Z]',  # numbered list items starting with a letter (likely MC)
        r'(?i)(which\s+of\s+the\s+following\s+(is|are|would|does|correct|not|true|false))',
        r'(?i)(all\s+of\s+the\s+following\s+(except|are\s+true))',
    ]
    for p in q_patterns:
        m = re.search(p, text)
        if m:
            indicators.append(m.group(0)[:80])
    
    # Count question-like lines
    q_lines = len(re.findall(r'^\s*\d+[\.\)]\s+[A-Z][a-z].*\?', text, re.MULTILINE))
    
    return {
        "has_questions": len(indicators) > 0 or q_lines > 3,
        "indicators": indicators[:5],
        "approx_question_lines": q_lines
    }

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
            topics.append({"topic": topic, "keyword_matches": score, "keywords_found": [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower)]})
    
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

def get_page_count_pymupdf(path):
    """Just get page count."""
    doc = fitz.open(path)
    n = len(doc)
    doc.close()
    return n

def analyze_pdf(path, label=""):
    """Full analysis of a PDF."""
    basename = os.path.basename(path)
    size = os.path.getsize(path)
    
    try:
        text, n_pages = extract_pymupdf(path)
    except Exception as e:
        return {"file": basename, "error": f"Extraction failed: {str(e)}"}
    
    if not text.strip():
        return {"file": basename, "error": "No text extracted (may be scanned/image-based)", "pages": n_pages}
    
    title_guess = basename.replace(".pdf", "").replace("_", " ").strip()
    topics = identify_topics(text, title_guess)
    questions = has_practice_questions(text)
    domains = map_to_dabt_domain(topics)
    
    # Extract a brief summary from first ~500 chars of meaningful content
    lines = text.strip().split('\n')
    lines = [l.strip() for l in lines if l.strip() and len(l.strip()) > 20]
    summary_excerpt = ' '.join(lines[:5])[:500] if lines else "No readable content"
    
    return {
        "file": basename,
        "label": label,
        "size_bytes": size,
        "size_mb": round(size / (1024*1024), 2),
        "pages": n_pages,
        "title_guess": title_guess,
        "topics_found": topics[:8],  # top 8 topics
        "topics_count": len(topics),
        "practice_questions": questions,
        "dabt_domains": domains,
        "summary_excerpt": summary_excerpt
    }

def analyze_all_in_dir(dirpath, file_pattern=r'\.pdf$'):
    """Analyze all PDFs in a directory."""
    results = []
    for f in sorted(os.listdir(dirpath)):
        if re.search(file_pattern, f, re.I):
            fp = os.path.join(dirpath, f)
            r = analyze_pdf(fp)
            results.append(r)
    return results

# ---- MAIN ----
if __name__ == "__main__":
    base = "/root/dabt-curated"
    
    # 1. ACT Course 2018 - Lectures
    print("=" * 70)
    print("ACT COURSE 2018 - LECTURES")
    print("=" * 70)
    act_lectures = analyze_all_in_dir(os.path.join(base, "ACT_Course_2018", "Lectures"))
    for r in act_lectures:
        print(f"\n--- {r['file']} ---")
        if "error" in r:
            print(f"  ERROR: {r['error']}")
            continue
        print(f"  Pages: {r['pages']} | Size: {r['size_mb']} MB")
        print(f"  Topics ({r['topics_count']}): {[t['topic'] for t in r['topics_found']]}")
        print(f"  DABT Domains: {r['dabt_domains']}")
        print(f"  Has Questions: {r['practice_questions']['has_questions']} (indicators: {r['practice_questions']['indicators'][:2]})")
        print(f"  QA lines: {r['practice_questions']['approx_question_lines']}")
    
    # Save results to JSON
    output = {
        "act_course_lectures": act_lectures,
    }
    
    # 2. Mid-Amer Tox Course - Topic Summaries
    print("\n\n" + "=" * 70)
    print("MID-AMER TOX COURSE - TOPIC SUMMARIES")
    print("=" * 70)
    midamer_topics = analyze_all_in_dir(os.path.join(base, "Mid-Amer_Tox_Course", "Topic_Summaries"))
    for r in midamer_topics:
        print(f"\n--- {r['file']} ---")
        if "error" in r:
            print(f"  ERROR: {r['error']}")
            continue
        print(f"  Pages: {r['pages']} | Size: {r['size_mb']} MB")
        print(f"  Topics ({r['topics_count']}): {[t['topic'] for t in r['topics_found']]}")
        print(f"  DABT Domains: {r['dabt_domains']}")
        print(f"  Has Questions: {r['practice_questions']['has_questions']} (indicators: {r['practice_questions']['indicators'][:2]})")
    output["midamer_topic_summaries"] = midamer_topics
    
    # 3. Save full JSON
    with open("/root/dabt_analysis_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\n\nResults saved to /root/dabt_analysis_results.json")
