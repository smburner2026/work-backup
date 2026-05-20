#!/usr/bin/env python3
"""Fix the unterminated string in generate_explanations_3.py"""
with open('/root/work/dabt/generate_explanations_3.py', 'r') as f:
    content = f.read()

# Fix DABT-4547 - closing triple quotes were missing one quote
old = '**Source:** C&D 8th ed., Ch. 22; ICH S1; EPA"\n\n    explanations['
new = '**Source:** C&D 8th ed., Ch. 22; ICH S1; EPA"""\n\n    explanations['
content = content.replace(old, new)

with open('/root/work/dabt/generate_explanations_3.py', 'w') as f:
    f.write(content)
print('Fixed')
