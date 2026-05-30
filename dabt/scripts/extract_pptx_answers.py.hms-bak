#!/usr/bin/env python3
"""Extract text and answer markers from all Recert Discussion PPTX files."""
import glob
import os
import re

try:
    from pptx import Presentation
except ImportError:
    os.system("pip install python-pptx -q")
    from pptx import Presentation

def extract_all_text(pptx_path):
    """Extract all text from a PPTX file with slide numbers."""
    prs = Presentation(pptx_path)
    slides_text = []
    for i, slide in enumerate(prs.slides, 1):
        slide_texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if text:
                        slide_texts.append(text)
        slides_text.append({
            'slide_num': i,
            'texts': slide_texts,
            'full_text': '\n'.join(slide_texts)
        })
    return slides_text

def find_answers(slides_text):
    """Find answer patterns in slide text."""
    answer_patterns = [
        r'(?i)answer\s*[:\-]?\s*([A-E])',
        r'(?i)correct\s*answer\s*[:\-]?\s*([A-E])',
        r'(?i)(?:the\s+)?correct\s+(?:choice|option|letter|response)\s*[:\-]?\s*(?:is\s+)?([A-E])',
        r'(?i)^\s*([A-E])\s*[.)]\s*(?:is\s+)?(?:correct|the\s+answer)',
    ]
    
    results = []
    for slide in slides_text:
        text = slide['full_text']
        for pattern in answer_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                results.append({
                    'slide_num': slide['slide_num'],
                    'answer': m.upper(),
                    'context': text[:300]
                })
    return results

# Process all PPTX files
base_dir = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams/Recert_Discussion_Slides"
all_pptx = glob.glob(os.path.join(base_dir, "**/*.pptx"), recursive=True)

print(f"Found {len(all_pptx)} PPTX files")

for pptx_path in sorted(all_pptx):
    rel_path = os.path.relpath(pptx_path, base_dir)
    print(f"\n{'='*80}")
    print(f"FILE: {rel_path}")
    print(f"{'='*80}")
    
    try:
        slides = extract_all_text(pptx_path)
        
        # Print all slide text
        for slide in slides:
            print(f"\n--- Slide {slide['slide_num']} ---")
            for t in slide['texts']:
                print(t)
        
        # Find answers
        answers = find_answers(slides)
        if answers:
            print(f"\n>>> FOUND ANSWERS:")
            for a in answers:
                print(f"  Slide {a['slide_num']}: Answer = {a['answer']}")
                print(f"  Context: {a['context'][:200]}")
        else:
            print(f"\n>>> NO CLEAR ANSWER PATTERNS FOUND")
            
    except Exception as e:
        print(f"ERROR processing {rel_path}: {e}")
