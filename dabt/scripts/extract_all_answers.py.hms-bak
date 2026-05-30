#!/usr/bin/env python3
"""
Comprehensive answer extraction from Recert Discussion PPTX files.

For each PPTX file, this script:
1. Extracts text from each slide
2. Identifies the question number from the first slide (or alternating pattern)
3. Finds the answer from the discussion slide using multiple strategies:
   - Explicit "Answer: X" patterns
   - "Correct" / "Best answer" annotations next to option letters
   - Positive markers ("Yes", "True") vs negative markers ("No", "False", "Incorrect")
4. Maps to DB questions
"""
import glob
import os
import re
import json
import sqlite3

try:
    from pptx import Presentation
except ImportError:
    os.system("pip install python-pptx -q")
    from pptx import Presentation

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
BASE_DIR = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams/Recert_Discussion_Slides"

def extract_slides(pptx_path):
    """Extract all text from a PPTX file with slide numbers."""
    prs = Presentation(pptx_path)
    slides = []
    for i, slide in enumerate(prs.slides, 1):
        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if text:
                        texts.append(text)
        slides.append({
            'num': i,
            'texts': texts,
            'full': '\n'.join(texts)
        })
    return slides

def parse_question_number(text):
    """Extract question number from text like '25.', 'Question 25', etc."""
    m = re.search(r'^(\d+)\.\s', text)
    if m:
        return int(m.group(1))
    return None

def find_explicit_answer(text):
    """Find explicit 'Answer: X' patterns."""
    patterns = [
        r'(?i)answer\s*[:\-]?\s*([A-E])\b',
        r'(?i)(?:the\s+)?correct\s+answer\s*[:\-]?\s*([A-E])\b',
        r'(?i)answer\s*[:\-]?\s*([A-E])\s',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1).upper()
    return None

def find_answer_from_annotations(text, question_text_from_slide):
    """
    Find answer from annotation patterns on discussion slides.
    
    The discussion slides typically list A-E again with annotations.
    Strategy: For each option letter, check if it's marked as correct.
    """
    # Get all options in format "A) text" or "A. text" or "A text"
    options = {}
    
    # Split into lines
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Look for patterns like "A) ..." or "A. ..." 
        m = re.match(r'^([A-E])[.)]\s*(.*)', line)
        if m:
            letter = m.group(1)
            rest = m.group(2).strip()
            options[letter] = rest
    
    if not options:
        return None
    
    # Strategy 1: Look for explicit positive markers next to a single option
    positive_markers = [
        r'(?i)\bcorrect\b',
        r'(?i)\byes\b',
        r'(?i)\btrue\b(?!.*false)',
        r'(?i)^best\s+answer',
        r'(?i)^best\s+choice',
        r'(?i)^correct\b',
        r'(?i)^yes\b',
    ]
    
    negative_markers = [
        r'(?i)\bincorrect\b',
        r'(?i)\bno\b',
        r'(?i)\bfalse\b',
        r'(?i)\beliminate\b',
        r'(?i)\bnot\s+(?:correct|true|best)',
        r'(?i)\bwrong\b',
    ]
    
    candidates = []
    for letter, rest in options.items():
        if not rest:
            continue
        
        has_positive = any(re.search(p, rest) for p in positive_markers)
        has_negative = any(re.search(p, rest) for p in negative_markers)
        
        # Check if the option is a reference/citation only
        is_citation = bool(re.match(r'^(?:C&D|Essentials|Ch\.|p\.\s*\d)', rest))
        
        if has_positive and not has_negative:
            candidates.append((letter, rest))
    
    # If exactly one candidate with positive markers, return it
    if len(candidates) == 1:
        return candidates[0][0]
    
    # Strategy 2: If there's text with "Correct" in a paragraph that mentions a letter
    for line in lines:
        m = re.search(r'(?i)([A-E])\s*[.)]\s*.*?\bcorrect\b', line)
        if m:
            letter = m.group(1)
            # Check if this line doesn't also say it's incorrect/false
            if not re.search(r'(?i)(?:not\s+correct|incorrect|false)', line):
                return letter
    
    # Strategy 3: Look for "Letter) ... - true" pattern (like slide 18 in 2013 part A 25-40)
    # Where only one option says "true" and others say something else
    true_count = 0
    true_letter = None
    for letter, rest in options.items():
        if rest and re.search(r'(?i)(?:^|\s+)(?:true|correct)(?:\s|$)', rest):
            true_count += 1
            true_letter = letter
    
    if true_count == 1 and true_letter:
        return true_letter
    
    return None

def process_pptx(pptx_path):
    """Process a single PPTX file and extract question-answer pairs."""
    filename = os.path.basename(pptx_path)
    rel_path = os.path.relpath(pptx_path, BASE_DIR)
    
    slides = extract_slides(pptx_path)
    
    # Determine exam type from path
    path_lower = pptx_path.lower()
    if '2013' in path_lower and 'part a' in path_lower:
        exam = '2013 Part A'
    elif '2013' in path_lower and 'part c' in path_lower:
        exam = '2013 Part C'
    elif '2015' in path_lower and 'part a' in path_lower:
        exam = '2015 Part A'
    elif '2015' in path_lower and 'part b' in path_lower:
        exam = '2015 Part B'
    elif '2015' in path_lower and 'part c' in path_lower:
        exam = '2015 Part C'
    else:
        exam = 'Unknown'
    
    results = []
    
    # First, determine question range from filename
    q_range = None
    fn = filename.lower()
    # Patterns like "questions9_16", "1_8", "17-24", "25-40"
    m = re.search(r'(?:questions?\s*)?(\d+)[\-_](\d+)', fn)
    if m:
        q_start, q_end = int(m.group(1)), int(m.group(2))
        q_range = (q_start, q_end)
    
    # For files where each slide pair is one question:
    # Look for question slides (with a numbered question at the top)
    # and their corresponding discussion slides
    
    # Collect question-discussion pairs
    qa_pairs = []
    i = 0
    while i < len(slides):
        slide = slides[i]
        full_text = slide['full']
        
        # Try to find a question number
        q_num = None
        for text in slide['texts']:
            qn = parse_question_number(text)
            if qn:
                q_num = qn
                break
        
        # Look for "Answer:" in this slide (explicit answer)
        answer = find_explicit_answer(full_text)
        
        if answer:
            qa_pairs.append((q_num, answer, slide['num'], full_text[:200]))
        
        # Try annotation-based answer finding
        if not answer:
            answer = find_answer_from_annotations(full_text, None)
            if answer:
                qa_pairs.append((q_num, answer, slide['num'], full_text[:200]))
        
        i += 1
    
    # For the alternating pattern (question slide then discussion slide),
    # look at pairs
    for j in range(len(slides)-1):
        slide1 = slides[j]
        slide2 = slides[j+1]
        
        # Get question number from slide1
        q_num = None
        for text in slide1['texts']:
            qn = parse_question_number(text)
            if qn:
                q_num = qn
                break
        
        # Check slide2 for answer
        answer = find_explicit_answer(slide2['full'])
        if not answer:
            answer = find_answer_from_annotations(slide2['full'], slide1['full'])
        
        if answer and q_num:
            # Check if we already have this
            existing = [p for p in qa_pairs if p[0] == q_num]
            if not existing:
                qa_pairs.append((q_num, answer, slide2['num'], slide2['full'][:200]))
    
    return {
        'file': rel_path,
        'exam': exam,
        'q_range': q_range,
        'qa_pairs': qa_pairs
    }

def get_db_questions(exam_sections=None):
    """Get questions from DB that need answers."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, substr(question_text,1,150) as qtext, question_number_in_source
        FROM questions 
        WHERE source_file_id=7 
        AND (correct_answer_letter IS NULL OR correct_answer_letter = '')
        ORDER BY id
    """)
    
    questions = []
    for row in cursor.fetchall():
        questions.append({
            'id': row[0],
            'text': row[1],
            'qnum': row[2]
        })
    
    conn.close()
    return questions

# Process all PPTX files
all_pptx = sorted(glob.glob(os.path.join(BASE_DIR, "**/*.pptx"), recursive=True))

all_results = []
for pptx_path in all_pptx:
    rel_path = os.path.relpath(pptx_path, BASE_DIR)
    print(f"Processing: {rel_path}")
    result = process_pptx(pptx_path)
    all_results.append(result)
    
    pairs = result['qa_pairs']
    if pairs:
        print(f"  Found {len(pairs)} Q/A pairs:")
        for q_num, answer, slide_num, context in pairs:
            print(f"    Q{q_num or '?'}: {answer} (slide {slide_num})")
    else:
        print(f"  No Q/A pairs found")
    print()

# Save all results
with open('/root/pptx_extracted_answers.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print("\n\n=== SUMMARY ===")
for r in all_results:
    if r['qa_pairs']:
        print(f"{r['file']}:")
        print(f"  {r['qa_pairs']}")
