---
name: book-to-knowledge-skill
description: "Convert any book (PDF, EPUB, DOCX, TXT, MD, HTML, RTF, MOBI) into a structured Hermes knowledge skill — extract frameworks, mental models, principles, and techniques into reusable agent skills. Use when the user wants to study a book through Hermes, apply an author's frameworks while working, or build a reusable knowledge base from a document."
version: 1.0.0
---

# Book-to-Knowledge-Skill Pipeline

Transform any book or document into a structured Hermes agent skill that extracts the author's frameworks, mental models, principles, and techniques — not summaries, but actionable toolkits.

## Philosophy

Books contain crystallized expertise. This pipeline extracts that knowledge into a format Hermes can leverage repeatedly. The output is a skill directory with:
- **SKILL.md** — core frameworks, mental models, and chapter index (loaded on-demand)
- **chapters/** — per-chapter summaries (loaded only when relevant)
- **glossary.md** — all key terms with definitions
- **patterns.md** — techniques, methods, anti-patterns
- **cheatsheet.md** — decision tables and quick reference

**Extract structure, not summaries.** A skill isn't a book report. It's a toolkit of named frameworks, actionable principles, step-by-step techniques, and things to avoid.

## Pipeline Overview

```
Source Document → extract.py → full_text.txt + metadata.json
                                      ↓
                              hermes_skill_gen.py → SKILL.md + chapters/ + glossary + patterns + cheatsheet
                                      ↓
                              Manual refinement → source verification, framework extraction, voice calibration
```

## Step 1 — Extract Text

Use `extract.py` from the book-to-skill repo (`/root/work/book-to-skill/scripts/extract.py`).

```bash
EXTRACT_SCRIPT="/root/work/book-to-skill/scripts/extract.py"
WORK_DIR="/tmp/book_skill_work"

# Technical books (code, tables, formulas):
python3 "$EXTRACT_SCRIPT" <BOOK_PATH> --mode technical --install-missing yes

# Text-heavy books (prose, narrative, analysis):
python3 "$EXTRACT_SCRIPT" <BOOK_PATH> --mode text --install-missing yes
```

**Supported formats:** PDF (via Docling/pdftotext/PyPDF2/pdfminer), EPUB (via ebooklib), DOCX, TXT, Markdown, HTML, RTF, MOBI/AZW (via Calibre).

The script creates:
- `$WORK_DIR/full_text.txt` — complete extracted text
- `$WORK_DIR/metadata.json` — title, word count, estimated tokens, chapter detection

## Step 2 — Generate Hermes Skill

Use `hermes_skill_gen.py` (`/root/work/book-to-skill/scripts/hermes_skill_gen.py`).

```bash
GEN_SCRIPT="/root/work/book-to-skill/scripts/hermes_skill_gen.py"

python3 "$GEN_SCRIPT" "$WORK_DIR" \
  --skill-name "<author>-<concept>" \
  --category research \
  --author "<Author Name>" \
  --title "<Book Title>" \
  --book-type text \
  --source-verified   # only if you have the primary source on disk
```

This generates the skill directory at `~/.hermes/skills/research/<skill-name>/`.

## Step 3 — Refine and Verify (CRITICAL)

The auto-generated skill is a **skeleton**. The agent must refine it:

### 3a. Core Frameworks Section
Read the full extracted text and write the Core Frameworks section in SKILL.md:
- Extract the author's **named frameworks** with exact formulations
- Write as "Use X when Y" or "Prefer X over Y because Z"
- Preserve the author's precision — "The 5 Whys" isn't interchangeable with "ask why multiple times"
- Target: 1500-2500 tokens for the core section

### 3b. Chapter Summaries
For each chapter file, replace the skeleton with actual content:
- Read the corresponding chapter text
- Extract: core idea (1-2 sentences), key concepts, frameworks, anti-patterns
- Target: 800-1200 tokens per chapter
- Files are loaded on-demand — keep them useful and tight

### 3c. Source Verification
Mark the skill's verification status in frontmatter:

| Status | Meaning |
|--------|---------|
| `source: primary` | Primary source on disk, verbatim quotes bound to page numbers |
| `source: extracted` | Full text extracted, claims should be verified |
| `source: training` | Derived from model training, unverified |

For `primary` status, add a verification banner at the top of SKILL.md:
```
VERIFIED — Primary source acquired. Verbatim quotes with page citations below.
```

### 3d. Topic Index
Generate an alphabetical topic index linking terms to chapter files.

## Step 4 — Verify Output

Before delivering, check:
- SKILL.md loads without errors (skill_view)
- Chapter files are present and have real content
- Glossary has actual terms (not just placeholders)
- Core Frameworks section is substantive (not a skeleton)
- Source verification status is accurate

## Existing Book-Derived Skills

These skills were created manually using this pipeline's approach:
- `luttwak-strategic-analysis` — verified (Byzantine Empire, pp.424-433)
- `wickham-material-foundation` — verified (Introduction OCR'd)
- `burckhardt-reflection-method` — needs primary source
- `nietzsche-vitalist-method` — draft, needs verification
- `historiographical-style-guide` — meta-orchestrator (references all method skills)

## Pitfalls

### Token Budget
- SKILL.md body: max 4,000 tokens (compaction truncates from END — put important content FIRST)
- Chapter files: 800-1,200 tokens each
- Glossary: max 1,500 tokens
- Patterns: max 2,000 tokens
- Cheatsheet: max 1,000 tokens

### Chapter Detection Failures
If detect_chapters finds no chapters, the text is treated as a single work. For books with unusual chapter formatting, manually set chapter boundaries in the extracted text (add `Chapter N: Title` headers).

**Detection strategies (v2):** `detect_chapters()` now uses three strategies in order:
1. Standard patterns (`Chapter N`, `Part X`) — business/technical books
2. ToC-based detection — parses Roman numeral entries (`I. Title`, `II. Title`) from the table of contents, then finds their first occurrence in the body text as boundaries
3. Centered uppercase headings after form feeds — academic book format (e.g. `\f\f                           THE EGO`)

The `N. Title` pattern was removed — it produced too many false positives (footnotes, index entries).

**Remaining limitation:** Appendix entries (e.g. `II. of Psychology and Alchemy` from a List of Plates) can collide with chapter numbering. Verify the detected chapter count against the book's actual structure (ToC, page count, known edition).

**Roman numeral filenames:** Generated as-is (`chI-the-ego.md`, `chII-the-shadow.md`) — no leading zeros.

### Glossary Extraction Quality
The current glossary generator uses regex: `**bold**` patterns and `Term — definition` patterns. On academic texts, this pulls random fragments (publication dates, partial sentences with em-dashes). **After auto-generation, review and curate the glossary manually** — the regex is a starting point, not a deliverable. For dense academic texts, consider loading the chapter text and extracting terms with LLM synthesis instead.

### Patterns Section
The patterns generator only detects `### How to apply:` sections. Academic, literary, and philosophical books don't use this format. The patterns section will be empty for most non-business books. **Manually extract techniques and methods** from the text — look for named procedures, step-by-step accounts, methodological descriptions, and analytical frameworks the author actually uses.

### Core Frameworks Placeholder
The SKILL.md template includes a placeholder comment `<!-- Extract the author's most important named frameworks here. -->` that the generator does NOT populate. **This section must be written manually** after reading the full text. It's the most important part of the skill — the 1500-2500 token core that gets loaded every time. Don't skip it.

### Large Books (>50K tokens)
Don't load the full text into context. Use grep and sed to pull specific sections:
```bash
grep -n "Chapter 5" full_text.txt
sed -n '1200,1400p' full_text.txt
```

### Verification Completeness
A skill with `source: training` is a draft, not a deliverable. Always note what remains unverified. The Luttwak skill pattern is the gold standard for source_evidence format.

### Academic Books vs. Business/Technical Books
The pipeline's heuristics are tuned for business books (clear chapter headings, "How to apply" sections, bold key terms). Academic and literary books need more manual work:
- Chapter detection: v2 handles Roman numerals and ToC-based detection, but verify the count manually
- Glossary: regex output will be garbage — curate manually
- Patterns: empty — extract techniques by reading the text
- Core frameworks: must be written from scratch by reading the author's actual arguments

## Integration with Existing Pipeline
This skill replaces the manual process that created the historical method skills. The full book-to-knowledge workflow:

1. **Source the book** — `historical-source-acquisition` skill
2. **Extract text** — `extract.py` (this skill)
3. **Generate skill** — `hermes_skill_gen.py` (this skill)
4. **Refine and verify** — manual refinement (this skill)
5. **Compile to PDF** — `book-pdf-compilation` skill (if needed)
6. **Integrate** — reference from `historiographical-style-guide` or relevant category

## References
- `references/academic-book-test-results.md` — Test results from Aion (Jung), documents chapter detection failures, glossary quality issues, and workarounds for academic books
- `references/pipeline-audit-2026-06-02.md` — Full audit of extract.py + hermes_skill_gen.py (32 findings), documents all fixes applied and remaining known issues
