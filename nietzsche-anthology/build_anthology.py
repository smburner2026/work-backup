#!/usr/bin/env python3
"""
Build Nietzsche Great Cultures Anthology
"""
import os
import re
import subprocess
import sys

SRC = "/root/work/nietzsche-anthology/sources"
OUTDIR = "/root/work/nietzsche-anthology"

def read_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

# ============================================================
# UTILITY: Extract aphorisms from text
# ============================================================

def extract_aphorisms(text, start_num, end_num=None):
    """Extract aphorisms from plain text where sections are marked by a number on its own line."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    
    aphorisms = []
    current_num = None
    current_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped.isdigit():
            num = int(stripped)
            next_non_empty = None
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip():
                    next_non_empty = lines[j].strip()
                    break
            
            if next_non_empty and not next_non_empty.isdigit() and len(next_non_empty) > 10:
                if current_num is not None and current_lines:
                    aphorisms.append((current_num, '\n'.join(current_lines).strip()))
                current_num = num
                current_lines = []
                continue
        
        if current_num is not None:
            if stripped.startswith('================================'):
                continue
            if 'Translated by' in stripped and 'Ian Johnston' in stripped:
                continue
            if 'Students, teachers' in stripped:
                continue
            if 'BEYOND GOOD AND EVIL' in stripped and len(stripped) < 30:
                continue
            if 'On the Genealogy of Morals' == stripped:
                continue
            if stripped.startswith('Friedrich Nietzsche') and len(stripped) < 30:
                continue
            
            current_lines.append(line)
    
    if current_num is not None and current_lines:
        aphorisms.append((current_num, '\n'.join(current_lines).strip()))
    
    if end_num:
        result = [(n, t) for n, t in aphorisms if start_num <= n <= end_num]
    else:
        result = [(n, t) for n, t in aphorisms if n == start_num]
    
    result = [(n, t.replace('\f', '').strip()) for n, t in result]
    return result

def fmt_aph(aph_list):
    """Format aphorism text, indented as blockquote."""
    if not aph_list:
        return "*[passage not found]*"
    
    text = ''
    for n, t in aph_list:
        t = t.replace('\f', '').strip()
        paragraphs = []
        for p in t.split('\n\n'):
            p = p.strip()
            if p:
                p_lines = p.split('\n')
                p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                paragraphs.append(p_clean)
        text = '\n\n'.join(paragraphs)
        break
    
    if not text:
        return "*[passage not found]*"
    
    lines = text.split('\n')
    quoted = '\n'.join('> ' + l for l in lines)
    return quoted

def extract_genealogy_section(text, section_num, essay='First'):
    """More targeted extraction for genealogy sections."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    
    essay_markers = {
        'First': 'First Essay',
        'Second': 'Second Essay', 
        'Third': 'Third Essay'
    }
    
    in_essay = False
    found_section = False
    collected = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not in_essay:
            if stripped == essay_markers[essay]:
                in_essay = True
            continue
        
        if not found_section:
            if stripped == str(section_num):
                next_non_empty = None
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        next_non_empty = lines[j].strip()
                        break
                if next_non_empty and len(next_non_empty) > 10:
                    found_section = True
                    collected.append(line)
                    continue
            else:
                continue
        
        if found_section:
            if stripped.isdigit():
                nxt = None
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        nxt = lines[j].strip()
                        break
                if nxt and len(nxt) > 10:
                    break
            
            if stripped.startswith('Second Essay') or stripped.startswith('Third Essay'):
                break
            
            collected.append(line)
    
    text = '\n'.join(collected).strip()
    text = text.replace('\f', '').strip()
    
    paragraphs = []
    for p in text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    
    text = '\n\n'.join(paragraphs)
    lines = text.split('\n')
    quoted = '\n'.join('> ' + l for l in lines)
    return quoted

def extract_essay_section_range(text, start_num, end_num, essay='First'):
    """Extract a range of sections from a genealogy essay."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    
    essay_markers = {
        'First': 'First Essay',
        'Second': 'Second Essay',
        'Third': 'Third Essay'
    }
    
    in_essay = False
    in_range = False
    collected = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not in_essay:
            if stripped == essay_markers[essay]:
                in_essay = True
            continue
        
        if stripped.isdigit():
            num = int(stripped)
            next_non_empty = None
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip():
                    next_non_empty = lines[j].strip()
                    break
            
            if next_non_empty and len(next_non_empty) > 10:
                if start_num <= num <= end_num:
                    if not in_range:
                        in_range = True
                elif in_range:
                    if num > end_num:
                        break
                continue
        
        if in_range:
            collected.append(line)
    
    text = '\n'.join(collected).strip()
    text = text.replace('\f', '').strip()
    
    paragraphs = []
    for p in text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    
    text = '\n\n'.join(paragraphs)
    lines = text.split('\n')
    quoted = '\n'.join('> ' + l for l in lines)
    return quoted

def extract_twilight_section(text, section_name, start_num, end_num=None):
    """Extract aphorisms from Twilight text using section markers."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    
    in_section = False
    section_found = False
    aphorisms = []
    current_num = None
    current_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not section_found and (stripped == section_name or stripped.startswith('\f' + section_name)):
            in_section = True
            section_found = True
            continue
        
        if in_section:
            if stripped.startswith('\f') and stripped != '\f' and not stripped.startswith('\f' + section_name) and len(stripped) > 5:
                if current_num is not None and current_lines:
                    aphorisms.append((current_num, '\n'.join(current_lines).strip()))
                break
            
            if stripped.isdigit():
                num = int(stripped)
                next_non_empty = None
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip():
                        next_non_empty = lines[j].strip()
                        break
                
                if next_non_empty and len(next_non_empty) > 10:
                    if current_num is not None and current_lines:
                        aphorisms.append((current_num, '\n'.join(current_lines).strip()))
                    current_num = num
                    current_lines = []
                    continue
            
            if current_num is not None:
                current_lines.append(line)
    
    if current_num is not None and current_lines:
        aphorisms.append((current_num, '\n'.join(current_lines).strip()))
    
    if end_num:
        result = [(n, t) for n, t in aphorisms if start_num <= n <= end_num]
    else:
        result = [(n, t) for n, t in aphorisms if n == start_num]
    
    return result

def extract_antichrist_sections(text, start_num, end_num=None):
    """Extract from Antichrist text."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    
    in_antichrist = False
    aphorisms = []
    current_num = None
    current_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not in_antichrist:
            if stripped == 'THE ANTI-CHRIST' or stripped.startswith('\fTHE ANTI-CHRIST'):
                in_antichrist = True
            continue
        
        if stripped.startswith('\f') and 'THE ANTI-CHRIST' not in stripped and len(stripped) > 5:
            if current_num is not None and current_lines:
                aphorisms.append((current_num, '\n'.join(current_lines).strip()))
            break
        
        if stripped.isdigit():
            num = int(stripped)
            next_non_empty = None
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip():
                    next_non_empty = lines[j].strip()
                    break
            
            if next_non_empty and len(next_non_empty) > 10:
                if current_num is not None and current_lines:
                    aphorisms.append((current_num, '\n'.join(current_lines).strip()))
                current_num = num
                current_lines = []
                continue
        
        if current_num is not None:
            if stripped.startswith('\f') and len(stripped) < 5:
                continue
            current_lines.append(line)
    
    if current_num is not None and current_lines:
        aphorisms.append((current_num, '\n'.join(current_lines).strip()))
    
    if end_num:
        result = [(n, t) for n, t in aphorisms if start_num <= n <= end_num]
    else:
        result = [(n, t) for n, t in aphorisms if n == start_num]
    
    return result

def extract_ecce_homo_section(text, section_name, start_num, end_num=None):
    """Extract from Ecce Homo sections."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    
    in_section = False
    aphorisms = []
    current_num = None
    current_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not in_section:
            if stripped == section_name or stripped.startswith('\f' + section_name):
                in_section = True
            continue
        
        if stripped.startswith('\f') and len(stripped) > 5 and section_name not in stripped:
            if current_num is not None and current_lines:
                aphorisms.append((current_num, '\n'.join(current_lines).strip()))
            break
        
        if stripped.isdigit():
            num = int(stripped)
            next_non_empty = None
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip():
                    next_non_empty = lines[j].strip()
                    break
            
            if next_non_empty and len(next_non_empty) > 10:
                if current_num is not None and current_lines:
                    aphorisms.append((current_num, '\n'.join(current_lines).strip()))
                current_num = num
                current_lines = []
                continue
        
        if current_num is not None:
            current_lines.append(line)
    
    if current_num is not None and current_lines:
        aphorisms.append((current_num, '\n'.join(current_lines).strip()))
    
    if end_num:
        result = [(n, t) for n, t in aphorisms if start_num <= n <= end_num]
    else:
        result = [(n, t) for n, t in aphorisms if n == start_num]
    
    return result

def format_aphorism_text(t):
    """Clean and format a block of text for blockquote display."""
    t = t.replace('\f', '').strip()
    paragraphs = []
    for p in t.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    t = '\n\n'.join(paragraphs)
    lines = t.split('\n')
    return '\n'.join('> ' + l for l in lines)

def format_aphorism_list(aph_list):
    """Format a list of (num, text) as separate subsections."""
    result = []
    for n, t in aph_list:
        result.append('### \\u00a7' + str(n))
        result.append('')
        result.append(format_aphorism_text(t))
        result.append('')
    return '\n'.join(result)

# ============================================================
# LOAD ALL SOURCE TEXTS
# ============================================================
bge_text = read_file(os.path.join(SRC, "bge_johnston_full.txt"))
genealogy_text = read_file(os.path.join(SRC, "genealogy_johnston_full.txt"))
twilight_text = read_file(os.path.join(SRC, "twilight_antichrist_hollingdale.txt"))
ecce_text = read_file(os.path.join(SRC, "ecce_homo_hollingdale.txt"))
zarathustra_text = read_file(os.path.join(SRC, "parkes_zarathustra_full.txt"))
gay_science_text = read_file(os.path.join(SRC, "gay_science_delcaro.txt"))
birth_text = read_file(os.path.join(SRC, "birth_of_tragedy_johnston.txt"))
use_abuse_text = read_file(os.path.join(SRC, "use_abuse_history_johnston.txt"))

# ============================================================
# PAGE BREAK HELPER
# ============================================================
PB = '\n\n<div style="page-break-before: always;"></div>\n\n'

# ============================================================
# BUILD THE MARKDOWN
# ============================================================

def build_markdown():
    md = []
    
    # ============ TITLE PAGE ============
    md.append("# NIETZSCHE ON THE PHYSIOLOGY OF GREAT CULTURES")
    md.append("")
    md.append("## An Anthology of Key Passages")
    md.append("")
    md.append("---")
    md.append("")
    md.append("### Translations Used")
    md.append("")
    md.append("- ***Beyond Good and Evil*** — Translated by Ian Johnston")
    md.append("- ***On the Genealogy of Morals*** — Translated by Ian Johnston")
    md.append("- ***Twilight of the Idols / The Antichrist*** — Translated by R.J. Hollingdale")
    md.append("- ***Ecce Homo*** — Translated by R.J. Hollingdale")
    md.append("- ***Thus Spoke Zarathustra*** — Translated by Graham Parkes")
    md.append("- ***The Gay Science*** — Translated by Adrian Del Caro / Josefine Nauckhoff")
    md.append("- ***The Birth of Tragedy*** — Translated by Ian Johnston")
    md.append("- ***The Use and Abuse of History for Life*** — Translated by Ian Johnston")
    md.append("")
    md.append("---")
    
    # ============ INTRODUCTION ============
    md.append(PB)
    md.append("# Introduction")
    md.append("")
    md.append("*By Costin*")
    md.append("")
    md.append("You have come to Nietzsche not for arguments but for weapons. Good. This anthology collects the passages that matter for the question you are pursuing — what *soil* makes a civilization great. Not philosophy as a system of ideas, but philosophy as physiology: the blood, the breeding, the climate, the *pathos of distance* that produces high culture. Nietzsche is not a thinker to be debated; he is a physician to be consulted. These pages contain his diagnosis.")
    md.append("")
    md.append("The passages gathered here trace a single arc: from the foundation of rank and master morality, through the breeding of types and the pathos of distance, to the flowering of great individuals and the decadence that undoes them. Nietzsche's question is not \"What is good?\" but \"What is strong? What is ascending? What presses toward higher forms?\" The answers are not comfortable. They were not meant to be. The user who opens this book should prepare to have his democratic certainties examined, his humanitarian pieties tested, and his understanding of 'culture' deepened beyond the merely academic.")
    md.append("")
    md.append("Keep the raw Nietzsche. Do not soften him. The Introduction frames the inquiry; what follows is the man himself speaking — through his translators, but with his voice undiminished. Read these passages as a physiognomist reads a face: looking for the signs of ascending or descending life. The rest is commentary.")
    
    # ============ PART I ============
    md.append(PB)
    md.append("# PART I: The Foundation of Rank and Master Morality")
    md.append("")
    
    # I.1 - BGE 257
    md.append("## I.1 \u2014 Beyond Good and Evil \u00a7257")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7257*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 257)))
    
    # I.2 - BGE 258
    md.append("")
    md.append("## I.2 \u2014 Beyond Good and Evil \u00a7258")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7258*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 258)))
    
    # I.3 - BGE 259
    md.append("")
    md.append("## I.3 \u2014 Beyond Good and Evil \u00a7259")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7259*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 259)))
    
    # I.4 - BGE 260
    md.append("")
    md.append("## I.4 \u2014 Beyond Good and Evil \u00a7260")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7260*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 260)))
    
    # I.5 - Genealogy I 2
    md.append("")
    md.append("## I.5 \u2014 On the Genealogy of Morals, First Essay \u00a72")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, FIRST ESSAY \u00a72*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_genealogy_section(genealogy_text, 2, 'First'))
    
    # I.6 - Genealogy I 4-5
    md.append("")
    md.append("## I.6 \u2014 On the Genealogy of Morals, First Essay \u00a74\u20135")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, FIRST ESSAY \u00a74\u20135*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_essay_section_range(genealogy_text, 4, 5, 'First'))
    
    # I.7 - Genealogy I 7
    md.append("")
    md.append("## I.7 \u2014 On the Genealogy of Morals, First Essay \u00a77")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, FIRST ESSAY \u00a77*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_genealogy_section(genealogy_text, 7, 'First'))
    
    # I.8 - Genealogy I 10-11
    md.append("")
    md.append("## I.8 \u2014 On the Genealogy of Morals, First Essay \u00a710\u201311")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, FIRST ESSAY \u00a710\u201311*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_essay_section_range(genealogy_text, 10, 11, 'First'))
    
    # I.9 - BGE 265
    md.append("")
    md.append("## I.9 \u2014 Beyond Good and Evil \u00a7265")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7265*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 265)))
    
    # ============ PART II ============
    md.append(PB)
    md.append("# PART II: The Pathos of Distance")
    md.append("")
    
    # II.1 - BGE 257 (ref)
    md.append("## II.1 \u2014 Beyond Good and Evil \u00a7257")
    md.append("")
    md.append("*(See Part I, Section I.1 \u2014 Already extracted above.)*")
    md.append("")
    md.append("The *pathos of distance* \u2014 \"that other more mysterious pathos,\" the longing for an ever-new widening of distances inside the soul itself \u2014 is first named here. Without the social distance between classes, the spiritual distance within the soul cannot grow.")
    
    # II.2 - BGE 263
    md.append("")
    md.append("## II.2 \u2014 Beyond Good and Evil \u00a7263")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7263*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 263)))
    
    # II.3 - BGE 264
    md.append("")
    md.append("## II.3 \u2014 Beyond Good and Evil \u00a7264")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7264*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 264)))
    
    # II.4 - BGE 268
    md.append("")
    md.append("## II.4 \u2014 Beyond Good and Evil \u00a7268")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7268*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 268)))
    
    # II.5 - Genealogy II 1-3
    md.append("")
    md.append("## II.5 \u2014 On the Genealogy of Morals, Second Essay \u00a71\u20133")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, SECOND ESSAY \u00a71\u20133*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_essay_section_range(genealogy_text, 1, 3, 'Second'))
    
    # II.6 - Zarathustra Prologue 3-5
    md.append("")
    md.append("## II.6 \u2014 Thus Spoke Zarathustra: Prologue \u00a73\u20135")
    md.append("")
    md.append("***THUS SPOKE ZARATHUSTRA, PROLOGUE \u00a73\u20135*** (Translated by Graham Parkes)")
    md.append("")
    
    # Extract Prologue 3-5
    z_text = zarathustra_text.replace('\r\n', '\n').replace('\r', '\n')
    z_lines = z_text.split('\n')
    in_prologue = False
    prologue_section = 0
    prologue_collected = []
    for line in z_lines:
        stripped = line.strip()
        if 'Zarathustra\'s Prologue' in stripped or stripped == 'PROLOGUE':
            in_prologue = True
            continue
        if in_prologue:
            if stripped.isdigit():
                num = int(stripped)
                if 3 <= num <= 5:
                    prologue_section = num
                    prologue_collected.append(line)
                    continue
                elif num > 5 and prologue_section > 0:
                    break
            if prologue_section > 0:
                prologue_collected.append(line)
    
    prologue_text = '\n'.join(prologue_collected).strip()
    prologue_text = prologue_text.replace('\f', '').strip()
    paragraphs = []
    for p in prologue_text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    prologue_text = '\n\n'.join(paragraphs)
    md.append('\n'.join('> ' + l for l in prologue_text.split('\n')))
    
    # II.7 - Zarathustra Three Metamorphoses
    md.append("")
    md.append("## II.7 \u2014 Thus Spoke Zarathustra: On the Three Metamorphoses")
    md.append("")
    md.append("***THUS SPOKE ZARATHUSTRA, \"ON THE THREE METAMORPHOSES\"*** (Translated by Graham Parkes)")
    md.append("")
    
    in_three = False
    three_collected = []
    for line in z_lines:
        stripped = line.strip()
        if 'On the Three Transformations' in stripped or 'On the Three Metamorphoses' in stripped:
            in_three = True
            continue
        if in_three:
            if re.match(r'^\d+\.\s', stripped) and 'Three' not in stripped:
                break
            if stripped.startswith('SECOND PART'):
                break
            three_collected.append(line)
    
    three_text = '\n'.join(three_collected).strip().replace('\f', '').strip()
    paragraphs = []
    for p in three_text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    three_text = '\n\n'.join(paragraphs)
    md.append('\n'.join('> ' + l for l in three_text.split('\n')))
    
    # ============ PART III ============
    md.append(PB)
    md.append("# PART III: Breeding and the Fixation of Type")
    md.append("")
    
    # III.1 - BGE 262
    md.append("## III.1 \u2014 Beyond Good and Evil \u00a7262")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7262*** (Translated by Ian Johnston)")
    md.append("")
    md.append(fmt_aph(extract_aphorisms(bge_text, 262)))
    
    # III.2 - Genealogy II 16-17
    md.append("")
    md.append("## III.2 \u2014 On the Genealogy of Morals, Second Essay \u00a716\u201317")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, SECOND ESSAY \u00a716\u201317*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_essay_section_range(genealogy_text, 16, 17, 'Second'))
    
    # III.3 - Twilight: Problem of Socrates 1-11
    md.append("")
    md.append("## III.3 \u2014 Twilight of the Idols: The Problem of Socrates \u00a71\u201311")
    md.append("")
    md.append("***TWILIGHT OF THE IDOLS, \"THE PROBLEM OF SOCRATES\" \u00a71\u201311*** (Translated by R.J. Hollingdale)")
    md.append("")
    
    twilight_socrates = extract_twilight_section(twilight_text, "The Problem of Socrates", 1, 11)
    
    def format_twilight_list(aph_list):
        result = []
        for n, t in aph_list:
            t = t.replace('\f', '').strip()
            paragraphs = []
            for p in t.split('\n\n'):
                p = p.strip()
                if p:
                    p_lines = p.split('\n')
                    p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                    paragraphs.append(p_clean)
            t = '\n\n'.join(paragraphs)
            result.append('***\u00a7' + str(n) + '***')
            result.append('')
            result.append('\n'.join('> ' + l for l in t.split('\n')))
            result.append('')
        return '\n'.join(result)
    
    md.append(format_twilight_list(twilight_socrates))
    
    # III.4 - Twilight: Skirmishes 33-39
    md.append("")
    md.append("## III.4 \u2014 Twilight of the Idols: Skirmishes \u00a733\u201339")
    md.append("")
    md.append("***TWILIGHT OF THE IDOLS, \"EXPEDITIONS OF AN UNTIMELY MAN\" \u00a733\u201339*** (Translated by R.J. Hollingdale)")
    md.append("")
    
    twilight_skirmishes = extract_twilight_section(twilight_text, "Expeditions of an Untimely Man", 33, 39)
    md.append(format_twilight_list(twilight_skirmishes))
    
    # III.5 - Ecce Homo: Why I Am So Wise 1-8
    md.append("")
    md.append("## III.5 \u2014 Ecce Homo: Why I Am So Wise \u00a71\u20138")
    md.append("")
    md.append("***ECCE HOMO, \"WHY I AM SO WISE\" \u00a71\u20138*** (Translated by R.J. Hollingdale)")
    md.append("")
    
    ecce_wise = extract_ecce_homo_section(ecce_text, "Why I Am So Wise", 1, 8)
    md.append(format_twilight_list(ecce_wise))
    
    # ============ PART IV ============
    md.append(PB)
    md.append("# PART IV: The Great Individual and the Flowering of Culture")
    md.append("")
    
    # IV.1 - Antichrist 57-62
    md.append("## IV.1 \u2014 The Antichrist \u00a757\u201362")
    md.append("")
    md.append("***THE ANTICHRIST \u00a757\u201362*** (Translated by R.J. Hollingdale)")
    md.append("")
    md.append("*This is the single most important passage for the user's inquiry \u2014 the Renaissance as the last great culture, destroyed by Luther and the Reformation.*")
    md.append("")
    
    antichrist_57_62 = extract_antichrist_sections(twilight_text, 57, 62)
    md.append(format_twilight_list(antichrist_57_62))
    
    # IV.2 - Twilight: What I Owe to the Ancients 1-5
    md.append("")
    md.append("## IV.2 \u2014 Twilight of the Idols: What I Owe to the Ancients \u00a71\u20135")
    md.append("")
    md.append("***TWILIGHT OF THE IDOLS, \"WHAT I OWE TO THE ANCIENTS\" \u00a71\u20135*** (Translated by R.J. Hollingdale)")
    md.append("")
    
    twilight_ancients = extract_twilight_section(twilight_text, "What I Owe to the Ancients", 1, 5)
    md.append(format_twilight_list(twilight_ancients))
    
    # IV.3 - BGE 269, 270, 274, 276, 278
    md.append("")
    md.append("## IV.3 \u2014 Beyond Good and Evil: Selected Aphorisms")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7269, \u00a7270, \u00a7274, \u00a7276, \u00a7278*** (Translated by Ian Johnston)")
    md.append("")
    
    for num in [269, 270, 274, 276, 278]:
        aph = extract_aphorisms(bge_text, num)
        md.append("### \u00a7" + str(num))
        md.append("")
        md.append(fmt_aph(aph))
        md.append("")
    
    # IV.4 - Birth of Tragedy 1-2
    md.append("## IV.4 \u2014 The Birth of Tragedy \u00a71\u20132 (Apollonian and Dionysian)")
    md.append("")
    md.append("***THE BIRTH OF TRAGEDY \u00a71\u20132*** (Translated by Ian Johnston)")
    md.append("")
    
    for num in [1, 2]:
        aph = extract_aphorisms(birth_text, num)
        if aph:
            n, t = aph[0]
            t = t.replace('\f', '').strip()
            paragraphs = []
            for p in t.split('\n\n'):
                p = p.strip()
                if p:
                    p_lines = p.split('\n')
                    p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                    paragraphs.append(p_clean)
            t = '\n\n'.join(paragraphs)
            md.append("### \u00a7" + str(n))
            md.append("")
            md.append('\n'.join('> ' + l for l in t.split('\n')))
            md.append("")
    
    # IV.5 - Birth of Tragedy 15-16
    md.append("## IV.5 \u2014 The Birth of Tragedy \u00a715\u201316 (The Death of Tragedy)")
    md.append("")
    md.append("***THE BIRTH OF TRAGEDY \u00a715\u201316*** (Translated by Ian Johnston)")
    md.append("")
    
    for num in [15, 16]:
        aph = extract_aphorisms(birth_text, num)
        if aph:
            n, t = aph[0]
            t = t.replace('\f', '').strip()
            paragraphs = []
            for p in t.split('\n\n'):
                p = p.strip()
                if p:
                    p_lines = p.split('\n')
                    p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                    paragraphs.append(p_clean)
            t = '\n\n'.join(paragraphs)
            md.append("### \u00a7" + str(n))
            md.append("")
            md.append('\n'.join('> ' + l for l in t.split('\n')))
            md.append("")
    
    # IV.6 - Zarathustra: On the Tarantulas
    md.append("## IV.6 \u2014 Thus Spoke Zarathustra: On the Tarantulas")
    md.append("")
    md.append("***THUS SPOKE ZARATHUSTRA, \"ON THE TARANTULAS\"*** (Translated by Graham Parkes)")
    md.append("")
    
    in_tarantulas = False
    tarantulas_collected = []
    for line in z_lines:
        stripped = line.strip()
        if 'On the Tarantulas' in stripped:
            in_tarantulas = True
            continue
        if in_tarantulas:
            if re.match(r'^\d+\.\s', stripped) and 'Tarantulas' not in stripped:
                break
            if stripped.startswith('SECOND PART') or stripped.startswith('THIRD PART'):
                break
            tarantulas_collected.append(line)
    
    t_text = '\n'.join(tarantulas_collected).strip().replace('\f', '').strip()
    paragraphs = []
    for p in t_text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    t_text = '\n\n'.join(paragraphs)
    md.append('\n'.join('> ' + l for l in t_text.split('\n')))
    
    # IV.7 - Zarathustra: On the Famous Wise Men
    md.append("")
    md.append("## IV.7 \u2014 Thus Spoke Zarathustra: On the Famous Wise Men")
    md.append("")
    md.append("***THUS SPOKE ZARATHUSTRA, \"ON THE FAMOUS WISE MEN\"*** (Translated by Graham Parkes)")
    md.append("")
    
    in_wise = False
    wise_collected = []
    for line in z_lines:
        stripped = line.strip()
        if 'On the Famous Wise' in stripped:
            in_wise = True
            continue
        if in_wise:
            if re.match(r'^\d+\.\s', stripped) and 'Famous' not in stripped:
                break
            if stripped.startswith('SECOND PART') or stripped.startswith('THIRD PART'):
                break
            wise_collected.append(line)
    
    wise_text = '\n'.join(wise_collected).strip().replace('\f', '').strip()
    paragraphs = []
    for p in wise_text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    wise_text = '\n\n'.join(paragraphs)
    md.append('\n'.join('> ' + l for l in wise_text.split('\n')))
    
    # ============ PART V ============
    md.append(PB)
    md.append("# PART V: Decadence vs. Ascending Life")
    md.append("")
    
    # V.1 - Antichrist 1-7
    md.append("## V.1 \u2014 The Antichrist \u00a71\u20137")
    md.append("")
    md.append("***THE ANTICHRIST \u00a71\u20137*** (Translated by R.J. Hollingdale)")
    md.append("")
    
    antichrist_1_7 = extract_antichrist_sections(twilight_text, 1, 7)
    md.append(format_twilight_list(antichrist_1_7))
    
    # V.2 - Twilight: Maxims and Arrows
    md.append("")
    md.append("## V.2 \u2014 Twilight of the Idols: Maxims and Arrows")
    md.append("")
    md.append("***TWILIGHT OF THE IDOLS, \"MAXIMS AND ARROWS\"*** (Translated by R.J. Hollingdale)")
    md.append("")
    md.append("*Selected maxims (\u00a78, \u00a712, \u00a714, \u00a731, \u00a736, \u00a738, \u00a744)*")
    md.append("")
    
    twilight_maxims = extract_twilight_section(twilight_text, "Maxims and Arrows", 1, 44)
    selected_maxims = {8, 12, 14, 31, 36, 38, 44}
    for n, t in twilight_maxims:
        if n in selected_maxims:
            t = t.replace('\f', '').strip()
            md.append('**\u00a7' + str(n) + '.** ' + t)
            md.append('')
    
    # V.3 - Genealogy III 11-13
    md.append("## V.3 \u2014 On the Genealogy of Morals, Third Essay \u00a711\u201313")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, THIRD ESSAY \u00a711\u201313*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_essay_section_range(genealogy_text, 11, 13, 'Third'))
    
    # V.4 - Ecce Homo: Why I Am So Clever 9-10
    md.append("")
    md.append("## V.4 \u2014 Ecce Homo: Why I Am So Clever \u00a79\u201310")
    md.append("")
    md.append("***ECCE HOMO, \"WHY I AM SO CLEVER\" \u00a79\u201310*** (Translated by R.J. Hollingdale)")
    md.append("")
    
    ecce_clever = extract_ecce_homo_section(ecce_text, "Why I Am So Clever", 9, 10)
    md.append(format_twilight_list(ecce_clever))
    
    # V.5 - Use and Abuse of History 1-3
    md.append("")
    md.append("## V.5 \u2014 The Use and Abuse of History for Life \u00a71\u20133")
    md.append("")
    md.append("***THE USE AND ABUSE OF HISTORY FOR LIFE \u00a71\u20133*** (Translated by Ian Johnston)")
    md.append("")
    
    for num in [1, 2, 3]:
        aph = extract_aphorisms(use_abuse_text, num)
        if aph:
            n, t = aph[0]
            t = t.replace('\f', '').strip()
            paragraphs = []
            for p in t.split('\n\n'):
                p = p.strip()
                if p:
                    p_lines = p.split('\n')
                    p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                    paragraphs.append(p_clean)
            t = '\n\n'.join(paragraphs)
            md.append("### \u00a7" + str(n))
            md.append("")
            md.append('\n'.join('> ' + l for l in t.split('\n')))
            md.append("")
    
    # V.6 - Gay Science 108, 125
    md.append("## V.6 \u2014 The Gay Science \u00a7108 and \u00a7125")
    md.append("")
    md.append("***THE GAY SCIENCE \u00a7108 AND \u00a7125*** (Translated by Adrian Del Caro / Josefine Nauckhoff)")
    md.append("")
    
    # Gay science extraction
    gs_text = gay_science_text.replace('\r\n', '\n').replace('\r', '\n')
    gs_lines = gs_text.split('\n')
    
    for target in [108, 125]:
        gs_found = False
        gs_collected = []
        for i, line in enumerate(gs_lines):
            stripped = line.strip()
            if stripped == str(target):
                # Verify
                nxt = None
                for j in range(i+1, min(i+5, len(gs_lines))):
                    if gs_lines[j].strip():
                        nxt = gs_lines[j].strip()
                        break
                if nxt and len(nxt) > 8:
                    gs_found = True
                    gs_collected.append(line)
                    continue
            if gs_found:
                if stripped.isdigit() and int(stripped) > target:
                    nxt = None
                    for j in range(i+1, min(i+5, len(gs_lines))):
                        if gs_lines[j].strip():
                            nxt = gs_lines[j].strip()
                            break
                    if nxt and len(nxt) > 8:
                        break
                gs_collected.append(line)
        
        gs_out = '\n'.join(gs_collected).strip().replace('\f', '').strip()
        paragraphs = []
        for p in gs_out.split('\n\n'):
            p = p.strip()
            if p:
                p_lines = p.split('\n')
                p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                paragraphs.append(p_clean)
        gs_out = '\n\n'.join(paragraphs)
        if gs_out:
            md.append("### \u00a7" + str(target))
            md.append("")
            md.append('\n'.join('> ' + l for l in gs_out.split('\n')))
            md.append("")
    
    # V.7 - Gay Science 341-342
    md.append("## V.7 \u2014 The Gay Science \u00a7341\u2013342 (Eternal Recurrence)")
    md.append("")
    md.append("***THE GAY SCIENCE \u00a7341\u2013342*** (Translated by Adrian Del Caro / Josefine Nauckhoff)")
    md.append("")
    
    for target in [341, 342]:
        gs_found = False
        gs_collected = []
        for i, line in enumerate(gs_lines):
            stripped = line.strip()
            if stripped == str(target):
                nxt = None
                for j in range(i+1, min(i+5, len(gs_lines))):
                    if gs_lines[j].strip():
                        nxt = gs_lines[j].strip()
                        break
                if nxt and len(nxt) > 8:
                    gs_found = True
                    gs_collected.append(line)
                    continue
            if gs_found:
                if stripped.isdigit() and int(stripped) > target:
                    nxt = None
                    for j in range(i+1, min(i+5, len(gs_lines))):
                        if gs_lines[j].strip():
                            nxt = gs_lines[j].strip()
                            break
                    if nxt and len(nxt) > 8:
                        break
                gs_collected.append(line)
        
        gs_out = '\n'.join(gs_collected).strip().replace('\f', '').strip()
        paragraphs = []
        for p in gs_out.split('\n\n'):
            p = p.strip()
            if p:
                p_lines = p.split('\n')
                p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
                paragraphs.append(p_clean)
        gs_out = '\n\n'.join(paragraphs)
        if gs_out:
            md.append("### \u00a7" + str(target))
            md.append("")
            md.append('\n'.join('> ' + l for l in gs_out.split('\n')))
            md.append("")
    
    # ============ PART VI ============
    md.append(PB)
    md.append("# PART VI: The Noble Soul \u2014 Final Aphorisms")
    md.append("")
    
    # VI.1 - BGE 287-296
    md.append("## VI.1 \u2014 Beyond Good and Evil \u00a7287\u2013296")
    md.append("")
    md.append("***BEYOND GOOD AND EVIL \u00a7287\u2013296*** (Translated by Ian Johnston)")
    md.append("")
    md.append("*Especially \u00a7287 (\"The noble soul has reverence for itself\"), \u00a7290, \u00a7293, \u00a7295 (\"The genius of the heart\"), and \u00a7296 (the final aphorism).*")
    md.append("")
    
    for num in [287, 290, 293, 295, 296]:
        aph = extract_aphorisms(bge_text, num)
        md.append("### \u00a7" + str(num))
        md.append("")
        md.append(fmt_aph(aph))
        md.append("")
    
    # VI.2 - Zarathustra: On the Gift-Giving Virtue
    md.append("## VI.2 \u2014 Thus Spoke Zarathustra: On the Gift-Giving Virtue")
    md.append("")
    md.append("***THUS SPOKE ZARATHUSTRA, \"ON THE GIFT-GIVING VIRTUE\"*** (Translated by Graham Parkes)")
    md.append("")
    
    in_gift = False
    gift_collected = []
    for line in z_lines:
        stripped = line.strip()
        if 'On the Gift-Giving Virtue' in stripped:
            in_gift = True
            continue
        if in_gift:
            if re.match(r'^\d+\.\s', stripped) and 'Gift' not in stripped:
                break
            if stripped.startswith('SECOND PART') or stripped.startswith('THIRD PART'):
                break
            gift_collected.append(line)
    
    gift_text = '\n'.join(gift_collected).strip().replace('\f', '').strip()
    paragraphs = []
    for p in gift_text.split('\n\n'):
        p = p.strip()
        if p:
            p_lines = p.split('\n')
            p_clean = ' '.join(pl.strip() for pl in p_lines if pl.strip())
            paragraphs.append(p_clean)
    gift_text = '\n\n'.join(paragraphs)
    md.append('\n'.join('> ' + l for l in gift_text.split('\n')))
    
    # VI.3 - Genealogy I 16-17
    md.append("")
    md.append("## VI.3 \u2014 On the Genealogy of Morals, First Essay \u00a716\u201317 (Conclusion)")
    md.append("")
    md.append("***ON THE GENEALOGY OF MORALS, FIRST ESSAY \u00a716\u201317*** (Translated by Ian Johnston)")
    md.append("")
    md.append(extract_essay_section_range(genealogy_text, 16, 17, 'First'))
    
    # ============ APPENDIX I ============
    md.append(PB)
    md.append("# Appendix I: Reading Guide")
    md.append("")
    md.append("| Work | Recommended Edition | ISBN | Translator Note |")
    md.append("|------|--------------------|------|-----------------|")
    md.append("| *Beyond Good and Evil* | Johnston (public domain) | \u2014 | Clear, readable, preserves Nietzsche's paragraph breaks and italics. Occasionally smooths over German wordplay. Reliable for general use. |")
    md.append("| *On the Genealogy of Morals* | Johnston (public domain) | \u2014 | Similar strengths to his BGE. Footnotes are helpful. The translation is idiomatic without being loose. |")
    md.append("| *Twilight of the Idols* | Hollingdale (Penguin Classics) | 978-0140445145 | Masterful rendering of Nietzsche's late style \u2014 the aphoristic punch and sarcasm come through brilliantly. The standard English edition. |")
    md.append("| *The Antichrist* | Hollingdale (Penguin Classics) | 978-0140445145 | Same volume as Twilight. Hollingdale captures the polemical fire. Essential for the Renaissance passages. |")
    md.append("| *Ecce Homo* | Hollingdale (Penguin Classics) | 978-0140445152 | The definitive English translation. Handles Nietzsche's self-mythologizing with appropriate flair. |")
    md.append("| *Thus Spoke Zarathustra* | Parkes (Oxford World's Classics) | 978-0199537082 | The most scholarly English translation. Parkes preserves Nietzsche's wordplay and alliteration better than any other version. The introduction is excellent. |")
    md.append("| *The Gay Science* | Del Caro / Nauckhoff (Cambridge) | 978-0521636454 | The standard academic translation. Reliable and precise. Some readers find it slightly less elegant than the Kaufmann version, but more accurate. |")
    md.append("| *The Birth of Tragedy* | Johnston (public domain) | \u2014 | Solid, readable translation. Good for the Apollonian/Dionysian passages. |")
    md.append("| *Use and Abuse of History* | Johnston (public domain) | \u2014 | Competent translation of an early work. The second Untimely Meditation. |")
    md.append("")
    md.append("### A Note on Editions")
    md.append("")
    md.append("For serious study, the Hollingdale translations of the later works (Twilight, Antichrist, Ecce Homo) published by Penguin are preferred for their fidelity to Nietzsche's tone. The Johnston translations of BGE and Genealogy are public domain and widely available online; they are reliable but lack the critical apparatus of academic editions. The Parkes Zarathustra (Oxford) is the most textually accurate English version available.")
    
    # ============ APPENDIX II ============
    md.append(PB)
    md.append("# Appendix II: Key Sources on Historical Civilizations")
    md.append("")
    md.append("Nietzsche's understanding of great cultures was profoundly shaped by his Basel colleague Jacob Burckhardt. The following works are essential reading alongside Nietzsche:")
    md.append("")
    md.append("### Jacob Burckhardt, *The Civilization of the Renaissance in Italy*")
    md.append("")
    md.append("Burckhardt's masterpiece (1860) portrays the Italian Renaissance as the birth of modern individuality \u2014 the emergence of \"the subjective man\" from the corporate structures of the Middle Ages. Nietzsche drew heavily on this work for his understanding of the Renaissance as the last great flowering of pagan, aristocratic culture. The passages in *The Antichrist* (\u00a757\u201362) praising Cesare Borgia and lamenting the Reformation's destruction of the Renaissance are directly indebted to Burckhardt's vision. Read this alongside Nietzsche to understand what \"great culture\" looked like in concrete historical terms: the state as a work of art, the cultivation of individual excellence, and the unfettered expression of all human capacities.")
    md.append("")
    md.append("Recommended edition: Penguin Classics, translated by S.G.C. Middlemore, ISBN 978-0140445343")
    md.append("")
    md.append("### Jacob Burckhardt, *Griechische Kulturgeschichte* (Greek Cultural History)")
    md.append("")
    md.append("Less well known in the English-speaking world than the Renaissance work, this four-volume history of Greek civilization (published 1898\u20131902, after Burckhardt's death) was delivered as lectures while Nietzsche was Burckhardt's colleague in Basel. Its influence on Nietzsche's understanding of Greek culture \u2014 particularly the agonistic spirit, the pessimism behind the artistic achievement, and the role of slavery in enabling high culture \u2014 is evident throughout the Genealogy and Twilight. Burckhardt's emphasis on the Greek \"agonal\" (competitive) principle directly shaped Nietzsche's thinking about rank, breeding, and cultural excellence.")
    md.append("")
    md.append("Note: There is no complete English translation. The German original is available from C.H. Beck (ISBN 978-3406545449). For English readers, the most accessible Burckhardt work on Greece is *The Greeks and Greek Civilization* (St. Martin's Press, 1998, ISBN 978-0312244477), which collects the essential passages.")
    md.append("")
    md.append("### Why Read Burckhardt Alongside Nietzsche")
    md.append("")
    md.append("Burckhardt provides the historical evidence for Nietzsche's physiological claims. Where Nietzsche diagnoses the conditions of great culture in the language of the physician, Burckhardt documents their actual manifestation in history. Together, they offer a complete picture: Nietzsche gives you the diagnostic framework, Burckhardt the historical case studies. The reader who studies both will understand that Nietzsche's \"pathos of distance\" is not a metaphor but a description of actual social arrangements that produced actual great individuals.")
    
    return '\n'.join(md)

# ============================================================
# WRITE THE MARKDOWN FILE
# ============================================================
os.makedirs(OUTDIR, exist_ok=True)
output_path = os.path.join(OUTDIR, "anthology.md")
md_content = build_markdown()

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Markdown file written to {output_path}")
print(f"Total characters: {len(md_content)}")

# ============================================================
# CONVERT TO PDF
# ============================================================
pdf_path = os.path.join(OUTDIR, "Nietzsche_Great_Cultures_Anthology.pdf")

print("Converting markdown to PDF via WeasyPrint...")
try:
    import markdown
    from weasyprint import HTML
    
    # Convert markdown to HTML with proper styling
    html_text = markdown.markdown(md_content, extensions=['extra', 'toc'])
    
    full_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {
    size: letter;
    margin: 1in;
}
body {
    font-family: 'DejaVu Serif', Georgia, serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
}
h1 {
    font-family: 'DejaVu Serif', Georgia, serif;
    font-size: 18pt;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    page-break-before: always;
}
h1:first-of-type {
    page-break-before: avoid;
}
h2 {
    font-size: 14pt;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
}
h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.3em;
}
blockquote {
    margin-left: 1.5em;
    margin-right: 0;
    padding-left: 1em;
    border-left: 3px solid #999;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #333;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
p {
    text-align: justify;
    hyphens: auto;
}
em {
    font-style: italic;
}
strong {
    font-weight: bold;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
}
th, td {
    border: 1px solid #666;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}
th {
    background-color: #e0e0e0;
    font-weight: bold;
}
</style>
</head>
<body>
""" + html_text + """
</body>
</html>"""
    
    HTML(string=full_html).write_pdf(pdf_path)
    
    size = os.path.getsize(pdf_path)
    print(f"PDF created successfully: {pdf_path} ({size / 1024:.0f} KB)")
except Exception as e:
    print(f"WeasyPrint failed: {e}")
    import traceback
    traceback.print_exc()
    print(f"Markdown file is at: {output_path}")

print("\nDone!")
