"""
Extract PDF textbooks into chapter-level .txt files with index.json.
Uses PyMuPDF TOC to find chapter boundaries, then extracts text.
"""

import fitz
import os
import json
import re
from pathlib import Path

REF = "/home/vthen/work/dabt-tutor/reference"
EXTRACTED = os.path.join(REF, "extracted")

SKIP_PATTERNS = [
    # Exact or word-boundary matches for front matter
    r'^cover$', r'^title page$', r'^copyright page$',
    r'^history and dedication$', r'^contents$', r'^contributors$',
    r'^preface', r'^half title$', r'^foreword', r'^about the editors$',
    r'^glossary$', r'^index$', r'^table of contents$', r'^acknowledgments$',
    r'^volume I$', r'^volume II$', r'^section I:', r'^section II:',
    r'^section III:', r'^section IV:', r'^section V:',
    # single-letter index entries
    r'^[a-z]$',
]
SKIP_RE = re.compile('|'.join(SKIP_PATTERNS), re.IGNORECASE)

def clean_filename(s):
    """Convert title to safe filename."""
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = s.strip('-')
    return s[:80]

def extract_chapters(doc, toc, chapter_level):
    """
    Extract chapters at the given TOC level.
    Returns list of dicts: [{title, page_start, page_end, filename, unit}]
    """
    
    # Collect chapter entries with their unit context
    chapters = []
    current_unit = "Front Matter"
    
    for i, entry in enumerate(toc):
        level, title, page = entry
        title_clean = title.strip().lower()
        
        # Track unit (level 1 in C&D, level 2 in Hayes volumes)
        if level == 1:
            current_unit = title.strip()
        
        # Skip non-chapter entries
        if level != chapter_level:
            continue
        
        # Skip front matter / index using regex word-boundary matching
        if SKIP_RE.match(title_clean):
            continue
        
        # Determine page range: start of this chapter to start of next chapter - 1
        page_start = page - 1  # TOC pages are 1-indexed, fitz is 0-indexed
        
        # Find end page
        page_end = len(doc) - 1  # default: last page
        for j in range(i + 1, len(toc)):
            next_level = toc[j][0]
            if next_level <= chapter_level:
                page_end = toc[j][2] - 2  # page before next chapter
                break
        
        if page_end < page_start:
            page_end = page_start + 1  # minimum one page
        
        filename = clean_filename(title)
        
        chapters.append({
            "title": title.strip(),
            "unit": current_unit,
            "page_start": page_start,
            "page_end": page_end,
            "filename": filename,
        })
    
    return chapters


def extract_text_for_chapter(doc, chapter):
    """Extract text for a chapter, page by page."""
    text_parts = []
    for pg in range(chapter["page_start"], chapter["page_end"] + 1):
        try:
            page_text = doc[pg].get_text("text")
            if page_text.strip():
                text_parts.append(page_text.strip())
        except Exception as e:
            print(f"    Warning: page {pg+1} error: {e}")
    return "\n\n".join(text_parts)


def build_index(chapters, source_name):
    """Build index.json from chapter list."""
    entries = []
    for ch in chapters:
        entries.append({
            "title": ch["title"],
            "unit": ch["unit"],
            "file": ch["filename"] + ".txt",
            "pages": f"{ch['page_start']+1}-{ch['page_end']+1}",
        })
    return {
        "source": source_name,
        "total_chapters": len(entries),
        "chapters": entries,
    }


def process_textbook(pdf_path, output_dir, chapter_level, source_name):
    """Full pipeline: extract, write, index."""
    print(f"\n{'='*60}")
    print(f"Processing: {source_name}")
    print(f"{'='*60}")
    
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    
    if not toc:
        print("  ERROR: No TOC found!")
        doc.close()
        return
    
    chapters = extract_chapters(doc, toc, chapter_level)
    print(f"  Found {len(chapters)} chapters")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate total pages for progress
    total_pages = sum(ch["page_end"] - ch["page_start"] + 1 for ch in chapters)
    pages_done = 0
    
    for i, ch in enumerate(chapters):
        txt_path = os.path.join(output_dir, ch["filename"] + ".txt")
        ch_pages = ch["page_end"] - ch["page_start"] + 1
        
        print(f"  [{i+1}/{len(chapters)}] {ch['title'][:70]}... ({ch_pages}p)", end="")
        
        text = extract_text_for_chapter(doc, ch)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"# {ch['title']}\n")
            f.write(f"# {source_name}\n")
            f.write(f"# Pages: {ch['page_start']+1}-{ch['page_end']+1}\n")
            f.write(f"# Unit: {ch['unit']}\n\n")
            f.write(text)
        
        pages_done += ch_pages
        size_kb = os.path.getsize(txt_path) / 1024
        print(f" → {size_kb:.0f} KB")
    
    # Write index
    index = build_index(chapters, source_name)
    index_path = os.path.join(output_dir, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
    total_size = sum(
        os.path.getsize(os.path.join(output_dir, f))
        for f in os.listdir(output_dir)
        if f.endswith(".txt")
    )
    print(f"\n  Done: {len(chapters)} files, {total_size/1024:.0f} KB total")
    
    doc.close()


# ── Main ──
if __name__ == "__main__":
    # C&D 9e
    process_textbook(
        pdf_path=os.path.join(REF, "textbooks/casarett-doull-9e.pdf"),
        output_dir=os.path.join(EXTRACTED, "casarett-doull-9e"),
        chapter_level=2,
        source_name="Casarett & Doull's Toxicology, 9th Edition",
    )
    
    # Hayes 7e
    process_textbook(
        pdf_path=os.path.join(REF, "textbooks/hayes-7e.pdf"),
        output_dir=os.path.join(EXTRACTED, "hayes-7e"),
        chapter_level=3,
        source_name="Hayes' Principles and Methods of Toxicology, 7th Edition",
    )
    
    print("\n✅ All textbooks extracted.")
