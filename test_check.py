#!/usr/bin/env python3
"""Extract text content from all 2015 Part B and Part C PPTX answer files."""
import sys, os, json
print("Starting extraction...")

SRC = "/root/work/dabt/dabt-tutor/reference/exam-materials/practice-exams/abt-2015-recert"
print(f"Source dir: {SRC}")
print(f"Exists: {os.path.exists(SRC)}")

files = ["Szabo questions 1_8.pptx", "2015 Part b JG_9-16.pptx", "Natalia_Recert part B_17-24.pptx",
         "2015 part b 24-40 ADL_AM.pptx", "DS_2015 part C questions 1_8.pptx", "JG_part C 9-16.pptx"]
for f in files:
    p = os.path.join(SRC, f)
    print(f"  {f}: {'EXISTS' if os.path.exists(p) else 'MISSING'}")

# test python-pptx
try:
    from pptx import Presentation
    print("python-pptx is available")
except ImportError:
    print("python-pptx NOT available - need to install")
