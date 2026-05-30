#!/usr/bin/env python3
"""Download all parts of Beyond Good and Evil (Johnston translation) and combine into one clean text file."""

import urllib.request
import re
import os
import html

# URLs for each part
# Prologue (part 0)
# Parts 1-9: http://johnstoniatexts.x10host.com/nietzsche/beyondgoodandevil[1-9]html.html
urls = {
    0: "http://johnstoniatexts.x10host.com/nietzsche/beyondgoodandevilprologuehtml.html",
}

for i in range(1, 10):
    urls[i] = f"http://johnstoniatexts.x10host.com/nietzsche/beyondgoodandevil{i}html.html"

part_names = {
    0: "Prologue",
    1: "Part 1: On the Prejudices of Philosophers",
    2: "Part 2: The Free Spirit",
    3: "Part 3: The Religious Mood",
    4: "Part 4: Epigrams and Interludes",
    5: "Part 5: On the Natural History of Morals",
    6: "Part 6: We Scholars",
    7: "Part 7: Our Virtues",
    8: "Part 8: Peoples and Fatherlands",
    9: "Part 9: What is Noble?",
}

output_dir = "/root/work/nietzsche-anthology/sources"
output_file = os.path.join(output_dir, "bge_johnston_full.txt")

# Check if output already has Part 9 content
existing_content = ""
if os.path.exists(output_file):
    with open(output_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()

# Also check if there's a separate file for part 9
part9_file = os.path.join(output_dir, "bge_johnston_part9.txt")
part9_content = ""
if os.path.exists(part9_file):
    with open(part9_file, 'r', encoding='utf-8') as f:
        part9_content = f.read()

all_texts = {}
missing_parts = []

for part_num in sorted(urls.keys()):
    url = urls[part_num]
    name = part_names[part_num]
    print(f"\n{'='*60}")
    print(f"Processing {name} ({url})")
    print(f"{'='*60}")
    
    # Check if part 9 already exists in the combined file or separately
    if part_num == 9:
        if part9_content:
            print(f"Part 9 found in separate file, reusing...")
            all_texts[part_num] = f"\n\n{'='*60}\n{part_names[part_num]}\n{'='*60}\n\n{part9_content.strip()}\n"
            continue
        elif "What is Noble?" in existing_content:
            print(f"Part 9 already in output file, extracting...")
            # Just note that it's there - we'll rebuild the whole file
            pass
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; BGE-Downloader/1.0)'
        })
        response = urllib.request.urlopen(req, timeout=30)
        raw_html = response.read().decode('utf-8', errors='replace')
        print(f"Downloaded {len(raw_html)} bytes")
    except Exception as e:
        print(f"ERROR downloading {url}: {e}")
        missing_parts.append(part_num)
        continue
    
    # Extract text content between <body> and </body> (or <html> as fallback)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', raw_html, re.DOTALL | re.IGNORECASE)
    if body_match:
        body = body_match.group(1)
    else:
        body = raw_html
    
    # Remove <script> and <style> blocks
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Clean whitespace: collapse multiple newlines into max 2, remove trailing spaces
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n\n', text)
    text = re.sub(r' +\n', '\n', text)
    text = re.sub(r'\n +', '\n', text)
    text = text.strip()
    
    # Add section header
    section = f"\n\n{'='*60}\n{part_names[part_num]}\n{'='*60}\n\n{text}\n"
    all_texts[part_num] = section
    print(f"Extracted ~{len(text)} characters of text")

# Build the full text
full_text = ""
for part_num in sorted(all_texts.keys()):
    full_text += all_texts[part_num]

# Add the footer
full_text += f"\n\n{'='*60}\nEnd of Beyond Good and Evil (translated by Ian Johnston)\n{'='*60}\n"

# Write output
os.makedirs(output_dir, exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(full_text.strip() + '\n')

print(f"\n\n{'='*60}")
print(f"Done! Output written to: {output_file}")
print(f"Total size: {len(full_text)} characters")
if missing_parts:
    print(f"\nWARNING: The following parts failed to download: {missing_parts}")
else:
    print(f"\nAll parts downloaded successfully!")
print(f"{'='*60}")
