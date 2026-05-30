#!/usr/bin/env python3
"""Extract actual answer letters from answer key files by comparing with no-answer versions."""

import os
import re
from docx import Document
from difflib import SequenceMatcher

KRISTEN_DIR = "/root/dabt-curated/Practice_Exams/Kristen_Mini_Exams"

def extract_all_text(doc_path):
    doc = Document(doc_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return paragraphs

# 1) Compare 02 June no-answers vs with-answers to find added answer content
print("=" * 70)
print("COMPARING 02 JUNE 2017: NO-ANSWERS vs WITH-ANSWERS")
print("=" * 70)

no_ans = extract_all_text(os.path.join(KRISTEN_DIR, "Mini-ABT examination 02 June 2017.docx"))
with_ans = extract_all_text(os.path.join(KRISTEN_DIR, "Mini-ABT examination with answers 02 June 2017.docx"))

# Find text that appears in with_ans but not in no_ans
no_set = set(no_ans)
with_set = set(with_ans)
added = with_set - no_set

print(f"Lines only in with-answers version: {len(added)}")
# These are likely answer annotations/keys
answer_related = [l for l in added if any(x in l.lower() for x in ['*', 'answer', 'correct', 'p.', 'http', 'source', 'recall'])]
print(f"Answer-related added lines (showing first 40):")
for l in sorted(list(answer_related))[:40]:
    print(f"  {l[:200]}")

# 2) Directly check Q37 answer in 02 June with-answers
print("\n" + "=" * 70)
print("DIRECT ANSWER ANALYSIS: Q37 (02 June file)")
print("=" * 70)
# Q37: Carbon tetrachloride, ethionine, phosphorus, puromycin, and tetracycline have the following common effect regarding fatty liver induction in the rat?
# Options: A-E, F. B and C, G. C and D, H. D but not A B or C, I. C but not A B or D

# From the output above, let me look at what commentary exists for each option:
# A. lower the level of circulating lipoprotein — *Niacin (vitamin B3) increases HDL... (not directly about CCl4)
# B. interfere with synthesis of the protein moiety of lipoproteins — *Carbon tetrachloride, ethionine, and puromycin inhibit...
# C. impair phospholipid synthesis — *Fumonisins... inhibit...
# D. block the secretion of hepatic triglycerides into the plasma — *Carbon tetrachloride is capable of inhibiting the conjugation...
# E. A and B, F. B and C, G. C and D, H. D but not A B or C, I. C but not A B or D

# Based on the commentaries:
# Option A commentary talks about Niacin which is unrelated to the listed chemicals
# Option B commentary says CCl4, ethionine, puromycin inhibit protein moiety synthesis - this matches some of the listed chemicals
# Option D commentary says CCl4 inhibits conjugation of protein moiety with triglyceride

# The common effect seems to be both B and D are true for at least some of the chemicals.
# Looking at the structure: each option has a *commentary but the one for the correct combination should be identifiable
# Let me check the no-answers version to see if there are differences

# Find Q37 in both files
for idx_no, p in enumerate(no_ans):
    if '37.' in p:
        print(f"No-ans Q37 context:")
        for j in range(idx_no, min(len(no_ans), idx_no+20)):
            print(f"  [{j}] {no_ans[j][:150]}")
        break

for idx_wa, p in enumerate(with_ans):
    if '37.' in p:
        print(f"\nWith-ans Q37 context:")
        for j in range(idx_wa, min(len(with_ans), idx_wa+20)):
            print(f"  [{j}] {with_ans[j][:150]}")
        break

# 3) Let me also check the answer key for 26 May 2017 Q33 (orphan Q6)
print("\n" + "=" * 70)
print("ANSWER ANALYSIS: Q33 in 26 May file (matches orphan Q6)")
print("=" * 70)
may26 = extract_all_text(os.path.join(KRISTEN_DIR, "Mini-ABT exam answers 26 May 2017.docx"))
for i, p in enumerate(may26):
    if '33.' in p:
        print(f"Q33 context:")
        for j in range(i, min(len(may26), i+12)):
            print(f"  [{j}] {may26[j][:200]}")
        break
        
# 4) Check Q10 in 28 July 2017-PART B (matches orphan Q26)
print("\n" + "=" * 70)
print("ANSWER ANALYSIS: Q10 in 28 July PART B (matches orphan Q26)")
print("=" * 70)
july28b = extract_all_text(os.path.join(KRISTEN_DIR, "Mini-ABT exam with answers 28 July 2017-PART B.docx"))
for i, p in enumerate(july28b):
    if '10.' in p:
        print(f"Q10 context:")
        for j in range(i, min(len(july28b), i+10)):
            print(f"  [{j}] {july28b[j][:200]}")
        break
