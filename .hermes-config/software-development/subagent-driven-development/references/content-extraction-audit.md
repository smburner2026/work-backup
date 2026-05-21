# Content Extraction & Audit with Parallel Subagents

## When to Use This Pattern

Use instead of the standard 2-stage review pattern when the task is:
- Analyzing a large collection of files (100+) for value, structure, and content
- Extracting and counting questions from exam/quiz documents
- Identifying duplicates and overlap across directories
- Cross-referencing answers from multiple sources
- Producing structured audit reports of a dataset

This is a **data analysis** workflow, not a **software implementation** workflow.

## The Pattern

### Step 1: Map the Territory

Before delegating, get the lay of the land yourself:

```bash
# File counts and sizes
find /path -type f | wc -l
du -sh /path/*
# File types
find /path -name "*.docx" | wc -l
find /path -name "*.pdf" | wc -l
```

### Step 2: Deploy Parallel Subagents by Category

Spin up one subagent per logical category. Each runs independently in parallel:

```python
delegate_task(
    tasks=[
        {
            "goal": "Extract and count all questions from exam files in directory A",
            "context": "Files at /path/A/ are .docx format. Use python-docx. Report: filename, question count, format, answer key status.",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Extract and analyze question bank files in directory B",
            "context": "Files at /path/B/ are .docx. Check for embedded answer sections at the end of each file.",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Extract text from PDF lecture files in directory C",
            "context": "Files at /path/C/ are PDFs. Use PyMuPDF (fitz). Check for embedded practice questions.",
            "toolsets": ["terminal", "file"]
        },
    ]
)
```

**Key rules:**
- Each subagent gets a **narrow, concrete, outcome-based** goal — not "analyze everything"
- Provide exact file paths and exact tools to use
- Tell each subagent what output format to produce (structured report is best)
- Subagents cannot see each other's results — the orchestrator cross-references

### Step 3: Synthesize Reports

Each subagent returns a structured summary. Cross-reference them to identify:
- Overlap (same questions in different directories)
- Gaps (topics/domains not covered by any source)
- Answer quality differences (a standalone answer PDF may disagree with embedded docx answers)

### Step 4: Deep-Dive on Discoveries

When a subagent report reveals something interesting (e.g., "orphan exam without answer key"), spawn a dedicated subagent to investigate:

```python
delegate_task(
    goal="Create answer key for orphan exam",
    context=f"Exam file at {path}. {details_from_subagent_report}. Check other answer keys for matching questions first.",
    toolsets=["terminal", "file"]
)
```

### Step 5: Apply Findings

Based on the synthesized audit:
- Move/copy valuable files to a curated directory
- Delete confirmed duplicates
- Update answer key mappings
- Write a README for the curated collection

## Pitfalls

- **Subagents cannot see each other's work** — if Task A's output is needed for Task B, run them serially or have the orchestrator intermediate
- **Tool choice matters** — `python-docx` for .docx, `PyMuPDF` (fitz) for text PDFs, `pdfminer.six` for complex PDFs, `Tesseract` for scanned PDFs, `python-pptx` for slides
- **Default regex patterns miss edge cases** — question numbering can use trailing periods (`1.`), spaces (`1 `), or parentheses (`1)`) and may have continuation lines that also start with digits
- **Always check docx files for embedded answer sections** — some put answers at the end of the same file, not in a separate PDF
- **Misspelled filenames** — catch "explainations" by using broad patterns like `*explain*`
- **Don't trust a single answer source** — when standalone PDF and embedded docx answers conflict, the embedded answer (same document as the question) is authoritative
- **Large docx files may contain inline answer formatting** — answers marked with `*` or inline commentary instead of a separate answer section

## Example: DABT 2000Q Analysis

The full workflow used for the 2000Q question bank analysis:

```
Phase 1: Tree scan (orchestrator)
├── Phase 2: 3 parallel subagents
│   ├── Practice Exams (84 files)
│   ├── Question Banks (116 files)
│   └── Lectures/References (74 PDFs)
├── Phase 3: Cross-reference reports → discovered
│   ├── 515 unanswered Qs → deep-dive → found embedded answers
│   ├── 9 conflicting answers → verified embedded is correct
│   └── 1 orphan exam → created answer key
└── Phase 4: Reorganize curated collection (425 files, 2.3 GB)
```
