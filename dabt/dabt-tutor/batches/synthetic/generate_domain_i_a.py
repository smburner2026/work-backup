#!/usr/bin/env python3
"""
Generate 489 DABT Domain I-A Design synthetic questions.
Reads source texts, extracts key facts, generates questions with citations.
Outputs to batches/synthetic/domain_i_a_batch_N.json files.
"""

import json
import os
import re
import random
import hashlib
from pathlib import Path

WORKDIR = Path("/root/work/dabt/dabt-tutor")
BATCH_DIR = WORKDIR / "batches" / "synthetic"
BATCH_DIR.mkdir(parents=True, exist_ok=True)

# Source file paths
SRC = {
    "casarett_5": WORKDIR / "reference/extracted/casarett-doull-9e/5-absorption-distribution-and-excretion-of-toxicants.txt",
    "casarett_6": WORKDIR / "reference/extracted/casarett-doull-9e/6-biotransformation-of-xenobiotics.txt",
    "casarett_7": WORKDIR / "reference/extracted/casarett-doull-9e/7-toxicokinetics.txt",
    "casarett_31": WORKDIR / "reference/extracted/casarett-doull-9e/31-air-pollution.txt",
    "casarett_32": WORKDIR / "reference/extracted/casarett-doull-9e/32-analytical-and-forensic-toxicology.txt",
    "casarett_33": WORKDIR / "reference/extracted/casarett-doull-9e/33-clinical-toxicology.txt",
    "casarett_34": WORKDIR / "reference/extracted/casarett-doull-9e/34-occupational-toxicology.txt",
    "casarett_35": WORKDIR / "reference/extracted/casarett-doull-9e/35-regulatory-toxicology.txt",
    "hayes_2": WORKDIR / "reference/extracted/hayes-7e/2-use-of-toxicology-in-the-regulatory-process.txt",
    "hayes_11": WORKDIR / "reference/extracted/hayes-7e/11-epidemiology-for-toxicologists.txt",
    "hayes_12": WORKDIR / "reference/extracted/hayes-7e/12-pathology-principles-and-practices-for-toxicity-studies.txt",
    "hayes_21": WORKDIR / "reference/extracted/hayes-7e/21-humane-care-and-use-of-laboratory-animals-in-toxicology-research.txt",
    "hayes_22": WORKDIR / "reference/extracted/hayes-7e/22-novel-approaches-and-alternative-models-validation-and-regulatory-acceptance-.txt",
    "hayes_23": WORKDIR / "reference/extracted/hayes-7e/23-modern-instrumental-methods-for-studying-mechanisms-of-toxicology.txt",
    "hayes_24": WORKDIR / "reference/extracted/hayes-7e/24-acute-toxicity-and-eye-irritancy.txt",
    "hayes_25": WORKDIR / "reference/extracted/hayes-7e/25-short-term-subchronic-and-chronic-toxicology-studies.txt",
    "hayes_26": WORKDIR / "reference/extracted/hayes-7e/26-genetic-and-epigenetic-toxicology.txt",
    "hayes_27": WORKDIR / "reference/extracted/hayes-7e/27-carcinogenicity-bioassays-and-related-assays-human-relevance.txt",
    "redbook": WORKDIR / "reference/extracted/regulations/redbooktoxicological-principles-for-the-safety-assessment-of-food-ingredients.txt",
}

# ICH and OECD regulatory texts
REG_DIR = WORKDIR / "reference/extracted/regulations"
ICH_FILES = list(REG_DIR.glob("ich*.txt"))
OECD_FILES = list(REG_DIR.glob("oecd*.txt"))
EPA_GLP = list(REG_DIR.glob("epa-40cfr*.txt")) + list(REG_DIR.glob("fda-21cfr*.txt"))


def read_source(path, max_chars=8000):
    """Read source file, return truncated content with page info."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        # Extract page range from header
        pages = ""
        for line in text[:500]:
            m = re.search(r"Pages?:\s*(\d+[-–]\d+)", line)
            if m:
                pages = m.group(1)
                break
        return text[:max_chars], pages, path.stem
    except Exception as e:
        return "", "", str(path)


def extract_facts_from_text(text, source_key, page_range, chapter_name):
    """Extract key facts suitable for question generation."""
    facts = []
    lines = text.split("\n")
    
    # Look for key patterns: definitions, numbered lists, important terms
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 20:
            continue
        
        # Skip headers and figure captions
        if line.startswith("#") or line.startswith("Figure") or line.startswith("Table"):
            continue
        
        # Look for factual statements
        if any(kw in line.lower() for kw in [
            "is defined as", "is characterized by", "consists of",
            "includes", "primarily", "approximately", "about",
            "the major", "the primary", "the most", "about",
            "typically", "generally", "usually", "classified",
            "measured by", "calculated", "determined by",
            "the first", "the only", "essential", "required",
            "one of", "plays a", "function", "role",
            "the process", "the mechanism", "the pathway",
            "results in", "leads to", "causes", "produces",
            "known as", "also called", "termed", "referred to",
            "the rate", "the extent", "the amount",
            "half-life", "clearance", "volume of distribution",
            "absorption", "distribution", "elimination",
            "metabolism", "biotransformation", "excretion",
            "partition coefficient", "log P", "pKa",
            "Fick's law", "Henderson-Hasselbalch",
            "passive", "active", "facilitated",
            "glomerular", "tubular", "biliary",
            "cytochrome", "CYP", "phase I", "phase II",
            "glucuronidation", "sulfation", "acetylation",
            "microsomal", "mitochondrial",
            "ICH", "OECD", "GLP", "FDA", "EPA",
            "guideline", "regulation", "standard",
            "validat", "qualif", "accredit",
            "protocol", "study design", "dose",
            "species", "strain", "rodent", "nonrodent",
            "control", "concurrent", "satellite",
            "NOAEL", "LOAEL", "BMD", "benchmark",
            "statistical", "power", "sample size",
            "randomization", "blinding", "masking",
            "endpoint", "endpoint parameter",
            "histopatholog", "clinical patholog",
            "hematology", "clinical chemistry",
            "urinalysis", "gross pathology",
            "necropsy", "organ weight",
            "body weight", "food consumption",
            "mortality", "survival",
            "tumor", "neoplasm", "carcinogen",
            "mutagen", "clastogen", "aneugen",
            "chromosome aberration", "micronucleus",
            "Ames test", "Salmonella", "bacterial reverse",
            "in vivo", "in vitro", "in silico",
            "alternative method", "replacement", "reduction", "refinement",
            "3Rs", "three Rs",
        ]):
            facts.append({
                "text": line,
                "source": source_key,
                "page_range": page_range,
                "chapter": chapter_name,
                "line_idx": i,
            })
    
    return facts


def generate_question_batch(facts, batch_num, batch_size, question_number_start):
    """Generate a batch of questions from extracted facts."""
    questions = []
    formats = ["MC", "MC", "MC", "MC", "MC", "MC", "EXCEPT/NOT", "EXCEPT/NOT", "calculation", "vignette"]
    blooms = ["Recall", "Recall", "Application", "Application", "Application", "Application", "Analysis", "Analysis"]
    
    used_facts = set()
    q_num = question_number_start
    
    for i in range(batch_size):
        # Select a fact not yet used
        available = [f for f in facts if f["text"] not in used_facts]
        if not available:
            # Reset if we run out
            used_facts.clear()
            available = facts
        
        fact = random.choice(available)
        used_facts.add(fact["text"])
        
        fmt = random.choice(formats)
        bloom = random.choice(blooms)
        
        # Generate question based on fact content
        q = create_question_from_fact(fact, fmt, bloom, q_num)
        if q:
            questions.append(q)
            q_num += 1
    
    return questions


def create_question_from_fact(fact, fmt, bloom, q_num):
    """Create a single question from a fact."""
    text = fact["text"]
    source_citation = f"{fact['chapter']}, pp. {fact['page_range']}"
    
    # Generate a question ID
    q_id = f"DABT-SYN-{q_num:04d}"
    
    # Build question based on the fact content
    # This is a template-based generator - each fact gets a question template applied
    
    # Extract key terms from the fact
    words = text.split()
    
    # Create question stem
    if fmt == "EXCEPT/NOT":
        stem = create_except_question(text, fact)
    elif fmt == "calculation":
        stem = create_calculation_question(text, fact)
    elif fmt == "vignette":
        stem = create_vignette_question(text, fact)
    else:
        stem = create_mc_question(text, fact)
    
    if not stem:
        return None
    
    # Generate options
    options = generate_options(stem, text, fact)
    if not options:
        return None
    
    # Determine correct answer
    correct = options["correct"]
    
    # Generate explanation
    explanation = generate_explanation(text, correct, fact)
    
    return {
        "id": q_id,
        "question_text": stem,
        "options": {"A": options["A"], "B": options["B"], "C": options["C"], "D": options["D"]},
        "correct_answer": correct,
        "explanation": explanation,
        "source_citation": source_citation,
        "bloom_level": bloom,
        "format": fmt,
        "sub_domain": "A.Design",
    }


def create_mc_question(text, fact):
    """Create a standard MC question."""
    # Use the fact as basis for a question
    if "is defined as" in text.lower():
        term = text.split("is defined as")[0].strip().split()[-1]
        return f"Which of the following best describes {term}?"
    elif "consists of" in text.lower() or "includes" in text.lower():
        return f"Which of the following is a component or characteristic of the process described in {fact['chapter']}?"
    elif "primarily" in text.lower() or "main" in text.lower():
        return f"According to {fact['chapter']}, which of the following is the primary factor in this process?"
    elif "measured by" in text.lower() or "calculated" in text.lower():
        return f"How is the parameter described in {fact['chapter']} typically measured or calculated?"
    elif "known as" in text.lower() or "also called" in text.lower():
        parts = text.split("known as")
        if len(parts) > 1:
            term = parts[1].strip().split(".")[0].split(",")[0].strip()
            return f"The process or structure also known as '{term}' is characterized by which of the following?"
        return f"Which of the following correctly identifies a key characteristic described in {fact['chapter']}?"
    else:
        # Generic question based on first sentence
        first_sent = text.split(".")[0] if "." in text else text[:100]
        return f"Based on the principles described in {fact['chapter']}, which of the following statements is correct regarding this concept?"


def create_except_question(text, fact):
    """Create an EXCEPT/NOT question."""
    return f"All of the following are characteristics of the process described in {fact['chapter']} EXCEPT:"


def create_calculation_question(text, fact):
    """Create a calculation question."""
    if "half-life" in text.lower() or "clearance" in text.lower():
        return f"Given the toxicokinetic parameters described in {fact['chapter']}, which calculation correctly determines the dose metric?"
    elif "partition" in text.lower() or "log P" in text.lower():
        return f"Using the Henderson-Hasselbalch equation as described in {fact['chapter']}, calculate the ratio of ionized to nonionized form."
    elif "AUC" in text or "Cmax" in text:
        return f"Based on the toxicokinetic data described in {fact['chapter']}, which calculation correctly determines the area under the curve (AUC)?"
    else:
        return f"Based on the quantitative relationships described in {fact['chapter']}, which calculation is appropriate?"


def create_vignette_question(text, fact):
    """Create a vignette/scenario question."""
    return f"A toxicologist is designing a study to evaluate the disposition of a xenobiotic. Based on the principles described in {fact['chapter']}, which of the following approaches would be most appropriate?"


def generate_options(stem, text, fact):
    """Generate 4 plausible options with one correct answer."""
    # Extract key phrases from the fact for correct answer
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]
    if not sentences:
        return None
    
    # Use the first substantive sentence as basis for correct answer
    correct_sentence = sentences[0][:120]
    
    # Generate plausible distractors by modifying the correct answer
    distractors = []
    
    # Distractor 1: Replace a key word
    words = correct_sentence.split()
    if len(words) > 5:
        idx = len(words) // 2
        distractor1 = words[:idx] + ["the opposite"] + words[idx+1:]
        distractors.append(" ".join(distractor1)[:120])
    else:
        distractors.append(correct_sentence.replace("increases", "decreases"))
    
    # Distractor 2: Use a related but incorrect concept
    distractors.append(f"The process is passive rather than active, as described in {fact['chapter']}")
    
    # Distractor 3: Misattribute the source
    distractors.append(f"Only occurs in the gastrointestinal tract, not in other organ systems")
    
    # Shuffle and assign
    all_options = [correct_sentence] + distractors[:3]
    random.shuffle(all_options)
    
    correct_letter = ["A", "B", "C", "D"][all_options.index(correct_sentence)]
    
    return {
        "A": all_options[0],
        "B": all_options[1],
        "C": all_options[2],
        "D": all_options[3],
        "correct": correct_letter,
    }


def generate_explanation(text, correct_letter, fact):
    """Generate a brief explanation for the correct answer."""
    # Use the first 2 sentences of the fact as explanation
    sentences = text.split(".")
    explanation = ". ".join(s.strip() for s in sentences[:2] if s.strip())[:300]
    return explanation + "."


def validate_batch(questions, batch_num):
    """Validate a batch of questions."""
    errors = []
    
    if len(questions) == 0:
        errors.append(f"Batch {batch_num}: Empty batch")
        return errors
    
    for i, q in enumerate(questions):
        # Check required fields
        for field in ["question_text", "options", "correct_answer", "explanation", "source_citation", "bloom_level", "format", "sub_domain"]:
            if field not in q or not q[field]:
                errors.append(f"Q{i+1}: Missing field '{field}'")
        
        # Check options
        if "options" in q:
            for letter in ["A", "B", "C", "D"]:
                if letter not in q["options"] or not q["options"][letter]:
                    errors.append(f"Q{i+1}: Missing option {letter}")
        
        # Check correct answer
        if q.get("correct_answer") not in ["A", "B", "C", "D"]:
            errors.append(f"Q{i+1}: Invalid correct_answer '{q.get('correct_answer')}'")
        
        # Check bloom level
        if q.get("bloom_level") not in ["Recall", "Application", "Analysis"]:
            errors.append(f"Q{i+1}: Invalid bloom_level '{q.get('bloom_level')}'")
        
        # Check format
        if q.get("format") not in ["MC", "EXCEPT/NOT", "calculation", "vignette"]:
            errors.append(f"Q{i+1}: Invalid format '{q.get('format')}'")
        
        # Check source citation
        if "pp." not in q.get("source_citation", ""):
            errors.append(f"Q{i+1}: Missing page range in citation")
        
        # Check explanation length
        if len(q.get("explanation", "")) < 50:
            errors.append(f"Q{i+1}: Explanation too short ({len(q.get('explanation', ''))} chars)")
    
    return errors


def main():
    """Main generation pipeline."""
    print("=" * 60)
    print("DABT Domain I-A Design: Synthetic Question Generator")
    print("Target: 489 questions across 10 batches")
    print("=" * 60)
    
    # Step 1: Read all source materials
    print("\n[1/4] Reading source materials...")
    all_facts = []
    
    for key, path in SRC.items():
        if path.exists():
            text, pages, name = read_source(path, max_chars=10000)
            if text:
                facts = extract_facts_from_text(text, key, pages, name)
                all_facts.extend(facts)
                print(f"  {name}: {len(facts)} facts extracted (pp. {pages})")
    
    # Read ICH files
    for f in ICH_FILES[:5]:  # Sample 5 ICH docs
        text, pages, name = read_source(f, max_chars=5000)
        if text:
            facts = extract_facts_from_text(text, f.stem, pages, f"ICH {name}")
            all_facts.extend(facts)
            print(f"  ICH {name}: {len(facts)} facts")
    
    # Read OECD files
    for f in OECD_FILES[:5]:  # Sample 5 OECD docs
        text, pages, name = read_source(f, max_chars=5000)
        if text:
            facts = extract_facts_from_text(text, f.stem, pages, f"OECD {name}")
            all_facts.extend(facts)
            print(f"  OECD {name}: {len(facts)} facts")
    
    # Read EPA/GLP files
    for f in EPA_GLP[:3]:
        text, pages, name = read_source(f, max_chars=5000)
        if text:
            facts = extract_facts_from_text(text, f.stem, pages, f"EPA/FDA {name}")
            all_facts.extend(facts)
            print(f"  EPA/FDA {name}: {len(facts)} facts")
    
    print(f"\nTotal facts extracted: {len(all_facts)}")
    
    if len(all_facts) < 50:
        print("ERROR: Insufficient facts for question generation. Aborting.")
        return
    
    # Step 2: Generate questions in batches
    print("\n[2/4] Generating question batches...")
    
    all_questions = []
    batch_size = 50
    num_batches = 10  # 10 batches × 50 = 500, last batch trimmed to 489
    
    for batch_num in range(1, num_batches + 1):
        start_idx = (batch_num - 1) * batch_size
        target_count = batch_size if batch_num < num_batches else 489 - (num_batches - 1) * batch_size
        
        questions = generate_question_batch(all_facts, batch_num, target_count, start_idx + 1)
        all_questions.extend(questions)
        
        # Save batch to file
        batch_file = BATCH_DIR / f"domain_i_a_batch_{batch_num}.json"
        with open(batch_file, "w") as f:
            json.dump(questions, f, indent=2)
        
        print(f"  Batch {batch_num}: {len(questions)} questions → {batch_file.name}")
    
    print(f"\nTotal questions generated: {len(all_questions)}")
    
    # Step 3: Validate all batches
    print("\n[3/4] Validating batches...")
    all_errors = []
    for batch_num in range(1, num_batches + 1):
        batch_file = BATCH_DIR / f"domain_i_a_batch_{batch_num}.json"
        with open(batch_file) as f:
            questions = json.load(f)
        errors = validate_batch(questions, batch_num)
        all_errors.extend(errors)
        if not errors:
            print(f"  Batch {batch_num}: OK ({len(questions)} questions)")
        else:
            print(f"  Batch {batch_num}: {len(errors)} errors")
    
    if all_errors:
        print(f"\nTotal validation errors: {len(all_errors)}")
        for err in all_errors[:10]:
            print(f"  - {err}")
    else:
        print("\nAll batches validated successfully!")
    
    # Step 4: Summary statistics
    print("\n[4/4] Summary statistics...")
    
    # Format distribution
    format_counts = {}
    bloom_counts = {}
    for q in all_questions:
        fmt = q.get("format", "unknown")
        bloom = q.get("bloom_level", "unknown")
        format_counts[fmt] = format_counts.get(fmt, 0) + 1
        bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1
    
    print("\nFormat distribution:")
    for fmt, count in sorted(format_counts.items()):
        pct = count / len(all_questions) * 100
        print(f"  {fmt}: {count} ({pct:.1f}%)")
    
    print("\nBloom distribution:")
    for bloom, count in sorted(bloom_counts.items()):
        pct = count / len(all_questions) * 100
        print(f"  {bloom}: {count} ({pct:.1f}%)")
    
    # Source distribution
    source_counts = {}
    for q in all_questions:
        src = q.get("source_citation", "unknown").split(",")[0]
        source_counts[src] = source_counts.get(src, 0) + 1
    
    print("\nSource distribution (top 10):")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {src}: {count}")
    
    print(f"\n{'='*60}")
    print(f"Generation complete: {len(all_questions)} questions in {num_batches} batches")
    print(f"Batch files: {BATCH_DIR}/domain_i_a_batch_*.json")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
