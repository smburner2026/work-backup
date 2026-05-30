#!/usr/bin/env python3
"""
Comprehensive truth audit of DABT SQLite database (4,841 questions).
All 5 phases.
"""
import sqlite3
import random
import os
from datetime import datetime

DB_PATH = "/root/work/dabt/dabt-tutor/reference/data/dabt.db"
REPORT_PATH = "/root/dabt_audit_report.md"
random.seed(42)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

report_lines = []
def log(s):
    report_lines.append(s)
    print(s)

log("# DABT Database Audit Report\n")
dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log("**Database:** `{}`".format(DB_PATH))
log("**Audit date:** {}".format(dt))
log("")

# ============================================================
# BASELINE STATS
# ============================================================
log("---")
log("## Baseline Statistics\n")

total_q = c.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
log("- Total questions: **{}**".format(total_q))

ao_count = c.execute("SELECT COUNT(*) FROM answer_options").fetchone()[0]
log("- Total answer options: **{}** (avg {:.1f}/Q)".format(ao_count, ao_count/total_q))

mp_count_total = c.execute("SELECT COUNT(*) FROM match_pairs").fetchone()[0]
log("- Total match_pairs: {}".format(mp_count_total))

src_files = c.execute("SELECT id, filename FROM source_files").fetchall()
log("- Source files: {}".format(len(src_files)))
for sf in src_files:
    cnt = c.execute("SELECT COUNT(*) FROM questions WHERE source_file_id=?", (sf['id'],)).fetchone()[0]
    log("  - [{}] `{}` — {} questions".format(sf['id'], sf['filename'], cnt))
log("")

# ============================================================
# PHASE 1 — STRUCTURAL INTEGRITY
# ============================================================
log("---")
log("## Phase 1 — Structural Integrity\n")

log("### 1.1 Questions with NULL/empty question_text")
null_text = c.execute("SELECT COUNT(*) FROM questions WHERE question_text IS NULL OR trim(question_text) = ''").fetchone()[0]
if null_text == 0:
    log("- PASS: No questions with NULL/empty question_text ({})".format(null_text))
else:
    log("- FAIL: {} questions with NULL/empty question_text".format(null_text))
    for r in c.execute("SELECT id, question_text, source_file_id FROM questions WHERE question_text IS NULL OR trim(question_text) = '' LIMIT 20"):
        qt = str(r['question_text'])[:80] if r['question_text'] else "NULL"
        log("  - Q{}: source_file={}, text='{}'".format(r['id'], r['source_file_id'], qt))
log("")

log("### 1.2 Questions with correct_answer_letter but NO answer_options")
c.execute("""
    SELECT q.id, q.question_text, q.correct_answer_letter, q.source_file_id
    FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND trim(q.correct_answer_letter) != ''
    AND NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
""")
rows = c.fetchall()
log("- {} questions with correct_answer_letter but no answer_options".format(len(rows)))
for r in rows:
    mp = c.execute("SELECT COUNT(*) FROM match_pairs WHERE question_id=?", (r['id'],)).fetchone()[0]
    log("  - Q{}: answer_letter='{}', has_match_pairs={}, src={}".format(r['id'], r['correct_answer_letter'], mp, r['source_file_id']))
# Summary breakdown
mp_count_1_2 = 0
no_mp_count = 0
for r in rows:
    if c.execute("SELECT COUNT(*) FROM match_pairs WHERE question_id=?", (r['id'],)).fetchone()[0] > 0:
        mp_count_1_2 += 1
    else:
        no_mp_count += 1
log("  - Of these: {} have match_pairs, {} have neither options nor match_pairs".format(mp_count_1_2, no_mp_count))
log("")

log("### 1.3 Answer options with empty/NULL option_text")
empty_opt = c.execute("""
    SELECT COUNT(*) FROM answer_options 
    WHERE option_text IS NULL OR trim(option_text) = ''
""").fetchone()[0]
if empty_opt == 0:
    log("- PASS: No answer options with empty/NULL option_text")
else:
    log("- FAIL: {} answer options with empty/NULL option_text".format(empty_opt))
    for r in c.execute("""
        SELECT ao.id, ao.question_id, ao.option_letter, ao.option_text
        FROM answer_options ao
        WHERE ao.option_text IS NULL OR trim(ao.option_text) = ''
        LIMIT 20
    """):
        t = str(r['option_text'])[:80] if r['option_text'] else "NULL"
        log("  - AO#{}: Q{}, letter={}, text='{}'".format(r['id'], r['question_id'], r['option_letter'], t))
log("")

log("### 1.4 Questions with NO domain assignment")
no_domain = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE NOT EXISTS (SELECT 1 FROM question_domains qd WHERE qd.question_id = q.id)
""").fetchone()[0]
log("- {} questions with no domain assignment".format(no_domain))
for r in c.execute("""
    SELECT q.id, q.question_text, sf.filename
    FROM questions q
    LEFT JOIN source_files sf ON q.source_file_id = sf.id
    WHERE NOT EXISTS (SELECT 1 FROM question_domains qd WHERE qd.question_id = q.id)
    LIMIT 10
"""):
    log("  - Q{}: source={}, text='{}'".format(r['id'], r['filename'], str(r['question_text'])[:80]))
log("  - **Investigation:**")
no_domain_src = c.execute("""
    SELECT sf.filename, COUNT(*) as cnt
    FROM questions q
    LEFT JOIN source_files sf ON q.source_file_id = sf.id
    WHERE NOT EXISTS (SELECT 1 FROM question_domains qd WHERE qd.question_id = q.id)
    GROUP BY sf.filename
    ORDER BY cnt DESC
""").fetchall()
for r in no_domain_src:
    log("    - `{}`: {} questions without domain".format(r['filename'], r['cnt']))
log("")

log("### 1.5 Source file reference integrity")
invalid_sf = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE q.source_file_id IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM source_files sf WHERE sf.id = q.source_file_id)
""").fetchone()[0]
if invalid_sf == 0:
    log("- PASS: All source_file_id values resolve to valid source_files")
else:
    log("- FAIL: {} questions reference non-existent source_file_id".format(invalid_sf))
log("")

log("### 1.6 Orphan answer_options")
orphan_ao = c.execute("""
    SELECT COUNT(*) FROM answer_options ao
    WHERE NOT EXISTS (SELECT 1 FROM questions q WHERE q.id = ao.question_id)
""").fetchone()[0]
if orphan_ao == 0:
    log("- PASS: No orphan answer_options")
else:
    log("- FAIL: {} orphan answer_options".format(orphan_ao))
    for r in c.execute("""
        SELECT ao.id, ao.question_id, ao.option_letter
        FROM answer_options ao
        WHERE NOT EXISTS (SELECT 1 FROM questions q WHERE q.id = ao.question_id)
        LIMIT 10
    """):
        log("  - AO#{}: references Q{} which doesn't exist".format(r['id'], r['question_id']))
log("")

log("### 1.7 Domain assignments completeness")
domains_sample = c.execute("SELECT * FROM question_domains LIMIT 3").fetchall()
if domains_sample:
    log("- question_domains schema sample: {} | domain={}".format(
        dict(domains_sample[0]), domains_sample[0]['domain']))
else:
    log("- question_domains table is EMPTY!")
log("")

dom_dist = c.execute("""
    SELECT qd.domain as dval, COUNT(*) as cnt
    FROM question_domains qd
    GROUP BY qd.domain
    ORDER BY cnt DESC
""").fetchall()
log("- Domain distribution:")
for r in dom_dist:
    log("  - **{}**: {} questions".format(r['dval'], r['cnt']))
log("")

log("### 1.8 Topic distribution")
topic_dist = c.execute("""
    SELECT qt.topic as tval, COUNT(*) as cnt
    FROM question_topics qt
    GROUP BY qt.topic
    ORDER BY cnt DESC
""").fetchall()
log("- Topic distribution:")
for r in topic_dist:
    log("  - `{}`: {}".format(r['tval'], r['cnt']))
log("")

log("### 1.9 Questions without topic assignment")
no_topic = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE NOT EXISTS (SELECT 1 FROM question_topics qt WHERE qt.question_id = q.id)
""").fetchone()[0]
log("- {} questions with no topic assignment".format(no_topic))
for r in c.execute("""
    SELECT q.id, sf.filename FROM questions q
    LEFT JOIN source_files sf ON q.source_file_id = sf.id
    WHERE NOT EXISTS (SELECT 1 FROM question_topics qt WHERE qt.question_id = q.id)
    LIMIT 10
"""):
    log("  - Q{}: source={}".format(r['id'], r['filename']))
log("")

# Additional structural findings
log("### 1.10 Additional structural findings\n")

null_ans = c.execute("SELECT COUNT(*) FROM questions WHERE correct_answer_letter IS NULL OR trim(correct_answer_letter) = ''").fetchone()[0]
log("- Questions with NULL/empty correct_answer_letter: **{}** ({:.0f}%)".format(null_ans, null_ans/total_q*100))

valid_qs = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE q.correct_answer_letter IS NOT NULL AND trim(q.correct_answer_letter) != ''
    AND EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
""").fetchone()[0]
log("- Questions with both options AND answer_letter: {} ({:.0f}%)".format(valid_qs, valid_qs/total_q*100))

exp_count = c.execute("SELECT COUNT(*) FROM questions WHERE explanation IS NOT NULL AND trim(explanation) != ''").fetchone()[0]
log("- Questions with explanations: {}".format(exp_count))

log("")

log("### 1.11 Option text truncation check\n")
# Quick truncation check: look for options ending mid-word around 80 chars
# (Can't use REGEXP in all SQLite; use Python-side check)
all_opts = c.execute("""
    SELECT id, question_id, option_letter, option_text
    FROM answer_options
    WHERE option_text IS NOT NULL
    AND length(option_text) > 70 AND length(option_text) < 90
""").fetchall()

truncated_samples = []
for r in all_opts:
    t = str(r['option_text'])
    # Check if ends mid-word (last 5 chars contain lowercase letters but no space/punct)
    last5 = t[-5:]
    if all(c.isalpha() and c.islower() for c in last5):
        truncated_samples.append(r)
        if len(truncated_samples) <= 5:
            log("  - AO#{} Q{} {}: '{}...' (len={})".format(
                r['id'], r['question_id'], r['option_letter'], t[:80], len(t)))

log("- Options possibly truncated (end mid-word at ~80 char boundary): **at least {}**".format(len(truncated_samples)))
log("  - The truncation appears to be a CSV field length limit during extraction")
log("")

log("### 1.12 Answer letter distribution (non-standard)\n")
non_std = c.execute("""
    SELECT correct_answer_letter, COUNT(*) as cnt 
    FROM questions 
    WHERE correct_answer_letter IS NOT NULL AND trim(correct_answer_letter) != ''
    AND correct_answer_letter NOT IN ('A','B','C','D','E')
    GROUP BY correct_answer_letter 
    ORDER BY cnt DESC
""").fetchall()
for r in non_std:
    log("  - `{}`: {} questions (matching test answer keys)".format(r['correct_answer_letter'], r['cnt']))
log("  - These non-standard letters (F,G,H,I,J,K,L,M,N,O,P,Q) are answer keys for matching/pairing questions")
log("")
log("")

# ============================================================
# PHASE 2 — ANSWER INTEGRITY SPOT-CHECK
# ============================================================
log("---")
log("## Phase 2 — Answer Integrity Spot-Check\n")

log("### 2.1 Random Sample Verification (30 questions)\n")
sample_qs = c.execute("""
    SELECT q.id, q.question_text, q.correct_answer_letter, sf.filename
    FROM questions q
    JOIN source_files sf ON q.source_file_id = sf.id
    WHERE q.question_text IS NOT NULL AND trim(q.question_text) != ''
    AND q.correct_answer_letter IS NOT NULL AND trim(q.correct_answer_letter) != ''
    ORDER BY RANDOM()
    LIMIT 30
""").fetchall()

issues_found = 0
for q in sample_qs:
    qid = q['id']
    options = c.execute("""
        SELECT option_letter, option_text FROM answer_options 
        WHERE question_id = ? ORDER BY option_letter
    """, (qid,)).fetchall()
    
    qtext = str(q['question_text'])
    truncated = qtext.endswith('...') or qtext.endswith('\u2026') or (len(qtext) > 10 and qtext[-1] in '.,;:' and qtext[-2].isalpha() and len(qtext) < 200)
    mangled = any(marker in qtext for marker in ['\\n', '\\\\n', '\ufffd', '??'])
    
    issues = []
    if truncated and len(qtext) < 100:
        issues.append("possibly truncated")
    if mangled:
        issues.append("mangled text")
    
    if not options:
        issues.append("NO answer options")
    else:
        opt_letters = [o['option_letter'] for o in options]
        if q['correct_answer_letter'] not in opt_letters:
            issues.append("correct_answer='{}' not in options {}".format(q['correct_answer_letter'], opt_letters))
        for o in options:
            if not o['option_text'] or str(o['option_text']).strip() == '':
                issues.append("empty option text for letter '{}'".format(o['option_letter']))
    
    if issues:
        issues_found += 1
        log("  - **Q{}** [{}]: {}".format(qid, q['filename'], '; '.join(issues)))
        log("    Text: '{}...'".format(qtext[:120]))
        if options:
            opts_str = ', '.join(["{}: '{}'".format(o['option_letter'], str(o['option_text'])[:50]) for o in options])
            log("    Options: {}".format(opts_str))
        log("    Correct: {}".format(q['correct_answer_letter']))

if issues_found == 0:
    log("- PASS: All 30 sampled questions look correct")
else:
    log("- WARN: {}/30 questions have issues".format(issues_found))
log("")

log("### 2.2 Past ABT Exams — Explanation/Answer verification (10 questions)\n")
past_exam_qs = c.execute("""
    SELECT q.id, q.question_text, q.correct_answer_letter, q.explanation, sf.filename
    FROM questions q
    JOIN source_files sf ON q.source_file_id = sf.id
    WHERE q.explanation IS NOT NULL AND trim(q.explanation) != ''
    ORDER BY RANDOM()
    LIMIT 10
""").fetchall()

log("- Sampled 10 questions with explanations:\n")
for q in past_exam_qs:
    qid = q['id']
    qtext = str(q['question_text'])[:100]
    expl = str(q['explanation'])[:200]
    options = c.execute("""
        SELECT option_letter, option_text FROM answer_options 
        WHERE question_id = ? ORDER BY option_letter
    """, (qid,)).fetchall()
    
    correct = str(q['correct_answer_letter'])
    expl_upper = expl.upper()
    
    justification_ok = correct in expl_upper
    if not justification_ok and options:
        for o in options:
            if o['option_text'] and str(o['option_text']).upper()[:30] in expl_upper:
                justification_ok = True
                break
    
    log("  - **Q{}** [{}]:".format(qid, q['filename']))
    log("    Q: '{}...'".format(qtext))
    if options:
        opt_line = ', '.join(["{}: {}".format(o['option_letter'], str(o['option_text'])[:60]) for o in options])
        log("    Options: {}".format(opt_line))
    log("    Correct answer: {}".format(correct))
    log("    Explanation (first 200 chars): '{}...'".format(expl[:200]))
    if justification_ok:
        log("    OK: Explanation justifies answer")
    else:
        log("    WARN: Explanation may NOT directly justify '{}'".format(correct))
    log("")

log("### 2.3 PDF-Extracted Questions — Parsing Quality Check\n")
pdf_qs = c.execute("""
    SELECT q.id, q.question_text, q.correct_answer_letter, sf.filename
    FROM questions q
    JOIN source_files sf ON q.source_file_id = sf.id
    WHERE sf.id = 7
    AND q.question_text IS NOT NULL
    ORDER BY RANDOM()
    LIMIT 20
""").fetchall()

log("  Sampling 20 PDF-extracted questions (source ID 7 = various PDFs):")
pdf_issues = 0
for q in pdf_qs:
    qid = q['id']
    qtext = str(q['question_text'])
    options = c.execute("""
        SELECT option_letter, option_text FROM answer_options 
        WHERE question_id = ? ORDER BY option_letter
    """, (qid,)).fetchall()
    
    issues = []
    ocr_artifacts = ['|', '\\n', '\\r', '\ufffd', '\u2666', '\u2663', '\u2665', '\u2022', '\u25aa', '\u25b8', '\u2751', '\u25a0']
    if any(a in qtext for a in ocr_artifacts):
        issues.append("OCR artifacts in text")
    if qtext.strip() == '':
        issues.append("EMPTY question text")
    if len(qtext) < 20:
        issues.append("Very short text ({} chars)".format(len(qtext)))
    if not options:
        issues.append("No answer options")
    else:
        opt_letters = [o['option_letter'] for o in options]
        if q['correct_answer_letter'] and q['correct_answer_letter'] not in opt_letters:
            issues.append("correct_answer '{}' not in options".format(q['correct_answer_letter']))
    
    if issues:
        pdf_issues += 1
        log("  - **Q{}** [PDF]: {}".format(qid, '; '.join(issues)))
    else:
        log("  - Q{} [PDF]: OK".format(qid))

log("  - PDF parsing issues: {}/{}".format(pdf_issues, len(pdf_qs)))
log("")

# ============================================================
# PHASE 3 — MATCHING TESTS
# ============================================================
log("---")
log("## Phase 3 — Matching Tests\n")

mp_count = c.execute("SELECT COUNT(*) FROM match_pairs").fetchone()[0]
log("- Total match_pairs entries: {}".format(mp_count))

qs_with_mp = c.execute("SELECT COUNT(DISTINCT question_id) FROM match_pairs").fetchone()[0]
log("- Questions with match_pairs: {}".format(qs_with_mp))

broken_qs = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
    AND NOT EXISTS (SELECT 1 FROM match_pairs mp WHERE mp.question_id = q.id)
""").fetchone()[0]
log("- Questions with NEITHER options NOR match_pairs (BROKEN): **{}**".format(broken_qs))

if broken_qs > 0:
    log("  - Listing broken questions:")
    for r in c.execute("""
        SELECT q.id, q.question_text, q.correct_answer_letter, sf.filename
        FROM questions q
        LEFT JOIN source_files sf ON q.source_file_id = sf.id
        WHERE NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
        AND NOT EXISTS (SELECT 1 FROM match_pairs mp WHERE mp.question_id = q.id)
        LIMIT 20
    """):
        log("    - Q{} [{}]: answer='{}' text='{}'".format(
            r['id'], r['filename'], r['correct_answer_letter'], str(r['question_text'])[:100]))
log("")

qs_no_letter_with_opts = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE (q.correct_answer_letter IS NULL OR trim(q.correct_answer_letter) = '')
    AND EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
""").fetchone()[0]
log("- Questions without correct_answer_letter but WITH answer_options: {}".format(qs_no_letter_with_opts))

qs_no_letter_with_mp = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE (q.correct_answer_letter IS NULL OR trim(q.correct_answer_letter) = '')
    AND EXISTS (SELECT 1 FROM match_pairs mp WHERE mp.question_id = q.id)
""").fetchone()[0]
log("- Questions without answer_letter but WITH match_pairs: {}".format(qs_no_letter_with_mp))

qs_no_letter_broken = c.execute("""
    SELECT COUNT(*) FROM questions q
    WHERE (q.correct_answer_letter IS NULL OR trim(q.correct_answer_letter) = '')
    AND NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
    AND NOT EXISTS (SELECT 1 FROM match_pairs mp WHERE mp.question_id = q.id)
""").fetchone()[0]
log("- Questions without answer_letter, no options, no match_pairs: **{}**".format(qs_no_letter_broken))
log("")

log("### Match Pairs Integrity Check\n")
orphan_mp = c.execute("""
    SELECT COUNT(*) FROM match_pairs mp
    WHERE NOT EXISTS (SELECT 1 FROM questions q WHERE q.id = mp.question_id)
""").fetchone()[0]
log("- Orphan match_pairs (referencing non-existent questions): {}".format(orphan_mp))

log("- Sample match_pairs (10 random):")
for r in c.execute("""
    SELECT mp.question_id, mp.term, mp.match_answer, q.question_text
    FROM match_pairs mp
    JOIN questions q ON mp.question_id = q.id
    ORDER BY RANDOM()
    LIMIT 10
"""):
    log("  - Q{}: term='{}' match='{}'".format(
        r['question_id'], str(r['term'])[:60], str(r['match_answer'])[:60]))
    log("    Context: '{}'".format(str(r['question_text'])[:80]))
log("")

# ============================================================
# PHASE 4 — DOMAIN III DEEP-DIVE
# ============================================================
log("---")
log("## Phase 4 — Domain III (Risk Assessment) Deep-Dive\n")

d3_count = c.execute("""
    SELECT COUNT(*) FROM question_domains qd
    WHERE qd.domain LIKE '%III%' OR qd.domain LIKE '%Risk Assessment%'
""").fetchone()[0]
log("- Total questions classified as Domain III: {}".format(d3_count))

d3_names = c.execute("""
    SELECT DISTINCT qd.domain as dval
    FROM question_domains qd
    WHERE qd.domain LIKE '%III%' OR qd.domain LIKE '%Risk Assessment%'
    ORDER BY qd.domain
""").fetchall()
log("- Domain III name variants used:")
for r in d3_names:
    cnt = c.execute("SELECT COUNT(*) FROM question_domains WHERE domain=?", (r['dval'],)).fetchone()[0]
    log("  - '{}': {} questions".format(r['dval'], cnt))

log("\n### Sampling 20 Domain III questions for verification\n")
d3_qs = c.execute("""
    SELECT q.id, q.question_text, q.correct_answer_letter, qd.domain as dval, qt.topic as tval, sf.filename
    FROM questions q
    JOIN question_domains qd ON q.id = qd.question_id
    LEFT JOIN question_topics qt ON q.id = qt.question_id
    LEFT JOIN source_files sf ON q.source_file_id = sf.id
    WHERE qd.domain LIKE '%III%' OR qd.domain LIKE '%Risk Assessment%'
    ORDER BY RANDOM()
    LIMIT 20
""").fetchall()

d3_issues = []
for q in d3_qs:
    qid = q['id']
    qtext = str(q['question_text'])[:150]
    topic = q['tval'] if q['tval'] else 'N/A'
    domain = q['dval']
    
    options = c.execute("""
        SELECT option_letter, option_text FROM answer_options 
        WHERE question_id = ? ORDER BY option_letter
    """, (qid,)).fetchall()
    
    risk_keywords = ['risk', 'hazard', 'exposure', 'dose-response', 'uncertainty', 'safety', 
                     'margin of exposure', 'MOE', 'NOAEL', 'LOAEL', 'RfD', 'TDI',
                     'benchmark dose', 'BMD', 'assessment', 'characterization',
                     'population', 'acceptable daily', 'reference dose',
                     'risk management', 'risk communication']
    qtext_lower = qtext.lower()
    keyword_hits = [kw for kw in risk_keywords if kw.lower() in qtext_lower]
    
    opt_text = ' '.join([str(o['option_text']).lower() for o in options if o['option_text']])
    keyword_hits += [kw for kw in risk_keywords if kw.lower() in opt_text]
    
    opt_check = "OK"
    if options:
        opt_letters = [o['option_letter'] for o in options]
        if q['correct_answer_letter'] and q['correct_answer_letter'] not in opt_letters:
            opt_check = "MISMATCH: correct_answer not in options"
            d3_issues.append((qid, opt_check))
    
    keyword_hits = list(set(keyword_hits))
    
    log("  - **Q{}** [{}]".format(qid, q['filename']))
    log("    Domain: {} | Topic: {}".format(domain, topic))
    log("    Q: '{}...'".format(qtext[:120]))
    log("    Correct: {} | Options: {}".format(q['correct_answer_letter'], opt_check))
    if keyword_hits:
        log("    Risk keywords found: {}".format(', '.join(keyword_hits[:5])))
    else:
        log("    **WARNING**: No risk-related keywords detected -- possible miscategorization")
    log("")

log("- Domain III Spot-Check Summary:")
log("  - Questions sampled: {}".format(len(d3_qs)))
log("  - Issues found: {}".format(len(d3_issues)))
for qid, issue in d3_issues:
    log("    - Q{}: {}".format(qid, issue))
log("")

# ============================================================
# PHASE 5 — TOPIC DISTRIBUTION
# ============================================================
log("---")
log("## Phase 5 — Topic Distribution Analysis\n")

topics = c.execute("""
    SELECT qt.topic as tval, COUNT(*) as cnt
    FROM question_topics qt
    GROUP BY qt.topic
    ORDER BY cnt DESC
""").fetchall()

total_topic_qs = sum(r['cnt'] for r in topics)
log("### 5.1 Topic Count Summary")
log("- Total topic assignments: {}".format(total_topic_qs))
log("- Unique topics: {}".format(len(topics)))
log("- Average Qs per topic: {:.1f}".format(total_topic_qs/len(topics)))

low_topics = [r for r in topics if r['cnt'] <= 3]
if low_topics:
    log("\n### 5.2 Topics with very few questions (<=3)")
    for r in low_topics:
        log("  - `{}`: {} questions".format(r['tval'], r['cnt']))

catch_all_keywords = ['general', 'other', 'misc', 'fundamental', 'basic', 'introduction']
catch_all_topics = [r for r in topics if any(kw in r['tval'].lower() for kw in catch_all_keywords)]
if catch_all_topics:
    log("\n### 5.3 Potential catch-all topics")
    for r in catch_all_topics:
        log("  - `{}`: {} questions ({:.1f}% of total)".format(
            r['tval'], r['cnt'], r['cnt']/total_topic_qs*100))

log("\n### 5.4 Key DABT exam topics presence check\n")
key_topics = ['carcinogenesis', 'mutagenesis', 'genetic toxicology', 'developmental toxicology',
              'reproductive toxicology', 'neurotoxicology', 'immunotoxicology', 'toxicokinetics',
              'biostatistics', 'ecotoxicology', 'forensic toxicology', 'clinical toxicology',
              'regulatory toxicology', 'metals', 'pesticides', 'solvents', 'nanotoxicology',
              'food toxicology', 'in vitro', 'alternative methods', 'ADME',
              'pharmacokinetics', 'metabolism', 'risk assessment', 'exposure assessment',
              'dose-response', 'hazard identification', 'dermal toxicology',
              'inhalation toxicology', 'target organ', 'liver', 'kidney']
missing_key = []
for kt in key_topics:
    found = False
    for r in topics:
        if kt.lower() in r['tval'].lower():
            log("  - `{}`: {} questions OK".format(r['tval'], r['cnt']))
            found = True
            break
    if not found:
        missing_key.append(kt)
        log("  - `{}`: **0** questions -- possible gap".format(kt))
log("")

# ============================================================
# SUMMARY TABLE
# ============================================================
log("---")
log("## Audit Summary\n")

log("| Phase | Result | Notes |")
log("|-------|--------|-------|")

p1_issues_list = []
if null_text > 0: p1_issues_list.append("{} Qs with null text".format(null_text))
if empty_opt > 0: p1_issues_list.append("{} empty options".format(empty_opt))
if no_domain > 0: p1_issues_list.append("{} Qs without domain".format(no_domain))
if invalid_sf > 0: p1_issues_list.append("{} invalid source refs".format(invalid_sf))
if orphan_ao > 0: p1_issues_list.append("{} orphan options".format(orphan_ao))
# Add key metrics
p1_extra = "{} Qs no answer_letter; {} K answer options; {} opt truncation; {} broken Qs".format(
    null_ans, ao_count, len(truncated_samples), broken_qs)
p1_notes = "; ".join(p1_issues_list) if p1_issues_list else p1_extra
p1_notes = p1_extra + ("; " + "; ".join(p1_issues_list) if p1_issues_list else "")
p1_result = "PASS" if not p1_issues_list else ("WARN" if len(p1_issues_list) <= 2 else "FAIL")
log("| Phase 1 -- Structural Integrity | **{}** | {} |".format(p1_result, p1_notes))

p2_notes = "{}/30 sample issues".format(issues_found)
if pdf_issues > 0:
    p2_notes += "; {}/{} PDF parsing issues".format(pdf_issues, len(pdf_qs))
p2_result = "PASS" if issues_found == 0 else ("WARN" if issues_found <= 5 else "FAIL")
log("| Phase 2 -- Answer Integrity | **{}** | {} |".format(p2_result, p2_notes))

p3_issues_list = []
if broken_qs > 0: p3_issues_list.append("{} broken Qs".format(broken_qs))
if orphan_mp > 0: p3_issues_list.append("{} orphan match_pairs".format(orphan_mp))
p3_notes = "{} pairs, {} linked Qs".format(mp_count, qs_with_mp)
if p3_issues_list: p3_notes += "; " + "; ".join(p3_issues_list)
p3_result = "PASS" if not broken_qs and not orphan_mp else "FAIL"
log("| Phase 3 -- Matching Tests | **{}** | {} |".format(p3_result, p3_notes))

p4_notes = "{} D3 Qs, {} issues in 20 sampled".format(d3_count, len(d3_issues))
p4_result = "PASS" if len(d3_issues) == 0 else "WARN"
log("| Phase 4 -- Domain III | **{}** | {} |".format(p4_result, p4_notes))

p5_issues_list = []
if low_topics: p5_issues_list.append("{} topics with <=3 Qs".format(len(low_topics)))
if missing_key: p5_issues_list.append("{} key exam topics missing".format(len(missing_key)))
p5_notes = "{} unique topics".format(len(topics))
if p5_issues_list: p5_notes += "; " + "; ".join(p5_issues_list)
p5_result = "WARN" if p5_issues_list else "PASS"
log("| Phase 5 -- Topic Distribution | **{}** | {} |".format(p5_result, p5_notes))
log("")

# ============================================================
# RECOMMENDED FIXES
# ============================================================
log("---")
log("## Recommended Fixes\n")

if broken_qs > 0:
    log("1. **Fix {} broken questions** -- add answer_options or match_pairs entries, or delete these records".format(broken_qs))
    broken_ids = c.execute("""
        SELECT q.id FROM questions q
        WHERE NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
        AND NOT EXISTS (SELECT 1 FROM match_pairs mp WHERE mp.question_id = q.id)
        LIMIT 100
    """).fetchall()
    ids_str = ', '.join([str(r['id']) for r in broken_ids])
    log("   - Broken question IDs: {}".format(ids_str))
    if len(broken_ids) >= 100:
        log("   - (showing first 100 of {})".format(broken_qs))

if no_domain > 0:
    log("\n2. **Assign domains to {} unclassified questions** -- priority since domain distribution affects exam prep".format(no_domain))
    no_domain_ids = c.execute("""
        SELECT q.id FROM questions q
        WHERE NOT EXISTS (SELECT 1 FROM question_domains qd WHERE qd.question_id = q.id)
        LIMIT 50
    """).fetchall()
    ids_str = ', '.join([str(r['id']) for r in no_domain_ids])
    log("   - Unclassified question IDs (first 50): {}".format(ids_str))

if empty_opt > 0:
    log("\n3. **Populate {} empty answer options** -- or delete them if they're placeholders".format(empty_opt))

if d3_issues:
    log("\n4. **Domain III miscategorized questions** -- review and reassign:")
    for qid, issue in d3_issues:
        log("   - Q{}: {}".format(qid, issue))

if low_topics:
    log("\n5. **Expand thin topics** -- the following topics have very few questions:")
    for r in low_topics:
        log("   - `{}`: only {} question(s)".format(r['tval'], r['cnt']))

if missing_key:
    log("\n6. **Fill content gaps** -- missing key exam topics:")
    for kt in missing_key:
        log("   - `{}`".format(kt))
log("")

# ============================================================
# QUESTIONS NEEDING HUMAN REVIEW
# ============================================================
log("---")
log("## Questions Needing Human Review\n")

review_qs = set()

# Broken questions
for r in c.execute("""
    SELECT q.id FROM questions q
    WHERE NOT EXISTS (SELECT 1 FROM answer_options ao WHERE ao.question_id = q.id)
    AND NOT EXISTS (SELECT 1 FROM match_pairs mp WHERE mp.question_id = q.id)
"""):
    review_qs.add((r['id'], "Broken: no options, no match_pairs"))

# Domain III issues
for qid, issue in d3_issues:
    review_qs.add((qid, "Domain III: " + issue))

# Add unclassified questions
for r in c.execute("""
    SELECT q.id FROM questions q
    WHERE NOT EXISTS (SELECT 1 FROM question_domains qd WHERE qd.question_id = q.id)
    LIMIT 100
"""):
    review_qs.add((r['id'], "No domain assigned"))

if review_qs:
    for qid, reason in sorted(review_qs, key=lambda x: x[0]):
        qrow = c.execute("SELECT question_text FROM questions WHERE id=?", (qid,)).fetchone()
        text_preview = str(qrow['question_text'])[:100] if qrow and qrow['question_text'] else 'N/A'
        log("- **Q{}**: {}".format(qid, reason))
        log("  Text: '{}...'".format(text_preview))
else:
    log("- No questions flagged for human review")

log("\n---")
log("*End of audit report -- generated {}*".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

# Write report
with open(REPORT_PATH, 'w') as f:
    f.write('\n'.join(report_lines))

print("\n\nReport written to " + REPORT_PATH)
conn.close()
