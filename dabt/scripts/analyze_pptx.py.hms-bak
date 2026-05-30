#!/usr/bin/env python3
"""Analyze PPTX slides from Recert_Discussion_Slides"""
import os
from pptx import Presentation

BASE = "/root/dabt-curated/Practice_Exams/Past_ABT_Exams/Recert_Discussion_Slides"

for root, dirs, files in os.walk(BASE):
    for f in sorted(files):
        if f.endswith('.pptx'):
            path = os.path.join(root, f)
            prs = Presentation(path)
            text_content = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for para in shape.text_frame.paragraphs:
                            text_content.append(para.text)
            
            full_text = '\n'.join(text_content)
            lines = full_text.split('\n')
            non_empty = [l for l in lines if l.strip()]
            
            print(f"\n--- {f} ({len(prs.slides)} slides, {len(non_empty)} text lines) ---")
            # Show first 300 chars
            print(f"  Preview: {full_text[:300]}")
            # Check for answer content
            if 'answer' in full_text.lower() or 'correct' in full_text.lower():
                print(f"  [Contains answer/explanation content]")
            # Check for question numbers
            import re
            qnums = len(re.findall(r'\b\d+[\.\)]', full_text))
            print(f"  Detected numbered items: {qnums}")
