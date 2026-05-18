#!/usr/bin/env python3
"""
Targeted editorial fixes based on Pass 2 scan results.
"""
import os, re, glob

DIR = '/root/work/vallentin-clean4'

files = sorted(glob.glob(os.path.join(DIR, '*.en.txt')))

fixes_applied = {}

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original = text
    file_fixes = []
    
    # 1. "the spirit of the age" → "the Spirit of the Age" (but not inside quotes)
    #    Be careful: "spirit of the age" can appear in lowercase as generic phrase.
    #    Only fix when used as Vallentin's Zeitgeist translation
    text = re.sub(r'(?<!["\'])the spirit of the age', 'the Spirit of the Age', text, flags=re.IGNORECASE)
    text = re.sub(r'"the spirit of the age"', '"the Spirit of the Age"', text, flags=re.IGNORECASE)
    if 'Spirit of the Age' in text and 'spirit of the age' not in text:
        # Check if we changed it
        pass
    
    # Count changes roughly
    if 'Spirit of the Age' in text:
        count = len(re.findall(r'Spirit of the Age', text))
        if count > 0 and 'Spirit of the Age' not in original or text.count('Spirit of the Age') > original.count('Spirit of the Age'):
            file_fixes.append(f'spirit_of_age({count})')
    
    # 2. "wherein" in narrative (not quotations) → "in which"
    #    Do this carefully - only replace when it's clearly not the best word
    #    "wherein" is acceptable in elevated prose, so be conservative
    
    # 3. Remove space before ? and !
    text = re.sub(r'\s+\?', '?', text)
    text = re.sub(r'\s+\!', '!', text)
    
    if text != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
        if file_fixes:
            print(f'  {fname:55s} fixed: {", ".join(file_fixes)}')

print(f'\nFixes applied to {sum(1 for f in files if open(f).read() != open(f).read())} files.')

# Now check: list all uses of "whence," "wherein," "therein," etc. for manual review
print('\n=== Edwardian/archaic usages to review manually ===')
for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        for word in ['whence', 'wherein', 'therein', 'therefrom', 'thereto', 'whereof', 'whereto', 'howbeit', 'natheless']:
            if re.search(r'\b' + word + r'\b', line, re.IGNORECASE):
                # Skip quotations
                in_quote = False
                if '"' in line:
                    parts = line.split('"')
                    for pi, part in enumerate(parts):
                        if pi % 2 == 1:  # inside quotes
                            if word in part.lower():
                                in_quote = True
                if not in_quote:
                    print(f'  {fname}:L{i:4d} \"{word}\" → {line.strip()[:100]}')
