#!/usr/bin/env python3
"""QC check on ch5-clean.txt"""
import re

with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch5-clean.txt','r') as f:
    lines = f.readlines()

suspicious = []
for i, line in enumerate(lines, 1):
    if 'nghiềm' in line.lower():
        suspicious.append((i, line.rstrip()))
    if 'sï' in line:
        suspicious.append((i, line.rstrip()))
    if 'ÿ' in line and 'kỳ' not in line.lower() and 'kÿ' not in line.lower():
        suspicious.append((i, line.rstrip()))
    if re.search(r'[d]ai-di', line):
        suspicious.append((i, line.rstrip()))
    if 'CHUONG 1V' in line:
        suspicious.append((i, line.rstrip()))
    if '===' in line:
        suspicious.append((i, line.rstrip()))
    if re.search(r'VIET-NAM CACH-MANG CAN-SU', line):
        suspicious.append((i, line.rstrip()))

print("=== Suspicious lines ===")
for ln, txt in suspicious:
    print(f'{ln}: {txt}')
print(f"Total: {len(suspicious)}")

# Check for remaining word-break hyphens
print("\n=== Lines with word-break hyphens not joined ===")
for i, line in enumerate(lines):
    if i < len(lines) - 1 and re.search(r'\w-$', line.rstrip()) and re.search(r'^\w', lines[i+1]):
        print(f'{i+1}: {line.rstrip()}')
        print(f'{i+2}: {lines[i+1].rstrip()}')
