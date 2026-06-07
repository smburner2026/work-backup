---
name: historical-source-extraction
description: "Extract structured data from historical documents — orientation, extraction prompt construction, batch processing, quality control, and structured output with page-level provenance."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [history, extraction, primary-sources, structured-data, OCR, provenance]
    category: research
    related_skills: [historical-source-acquisition, ocr-and-documents, source-provenance-tracker]
    requires_toolsets: [web, terminal, file]
---

# Historical Source Extraction

Extract structured, citable data from historical documents using a 4-step pipeline inspired by the Chronos AI Historian framework (arXiv 2604.03553).

## When to Use

- User has a historical document (PDF, scan, or extracted text) and wants structured data from it
- User wants to build a dataset from a historical source (names, dates, events, places, prices, etc.)
- User wants to systematically extract information from a multi-page historical document
- User asks "what's in this document" in a structured, research-grade way

## Prerequisites

- Source text already extracted (via `historical-source-acquisition` or `ocr-and-documents`)
- If not extracted yet, run the acquisition skill first

## The 4-Step Pipeline

### Step 1 — Document Orientation

Before extracting anything, understand the document's structure.

**Read the first 3-5 pages** to identify:
- Title page, author, date, publisher
- Table of contents (if present)
- Preface/introduction (often explains the document's purpose and structure)
- Abbreviation tables, legends, or keys (critical for structured data)
- Index (at the end — tells you what the document considers important)

**For each structural element found, note it in a source profile:**

```markdown
## Source Profile: <title>

**Type:** [city directory / census / government report / newspaper / ...]
**Date:** [publication date]
**Language:** [language + script]
**Structure:** [how the document is organized]
**Key abbreviations:** [list any abbreviation tables found]
**Estimated extraction scope:** [which pages/sections contain the target data]
```

**If the document has a table of contents or index:**
- Map chapter/section boundaries to page numbers
- Identify which sections contain the target data
- Note any supplements, appendices, or corrections

**If the document has no TOC (common for older sources):**
- Sample 3-5 pages spread across the document to identify recurring patterns
- Note page layout (columns, tables, free text, forms)
- Identify the "data zone" vs front matter/back matter

### Step 2 — Extraction Prompt Construction

Build a tailored extraction prompt based on what you learned in Step 1.

**The prompt must include:**

1. **Source context** — what this document is, when it was created, what it contains
2. **Structural cues** — how the data is laid out (columns? tables? narrative? forms?)
3. **Abbreviation key** — any abbreviations or shorthand found in the document
4. **Target schema** — what fields you're extracting (names, dates, places, etc.)
5. **Edge cases** — things to watch for (missing data markers, cross-references, footnotes)

**Example prompt for a 19th-century city directory:**

```markdown
You are extracting structured data from a city directory published in 1875.

The directory lists residents alphabetically by last name. Each entry has:
- Name (last, first)
- Occupation
- Home address
- Business address (if different)

Abbreviations found on page 12:
- "bds." = boards at
- "h." = home
- "res." = residence
- "n.s." = north side
- "e." = east of

Special handling:
- Married women listed as "Mrs. [husband's first name] [surname]"
- Entries with "wid." indicate widow/widower
- Entries with "rem." indicate removed/moved away
- Cross-references: "see [other name]" means an alias or married name

Output format: JSON array of objects with fields: name, occupation, home_address, business_address, notes
```

**Test the prompt on a single representative page first.** Verify the output matches expectations before proceeding to batch extraction.

### Step 3 — Batch Extraction

Once the prompt is validated, process the target pages.

**Single-page extraction (when pages are independent):**
- Send each page to the LLM with the extraction prompt
- Collect structured output (JSON/CSV)
- Tag each record with source + page number

**Multi-page extraction (when context spans pages):**
- Process pages in overlapping windows (e.g., pages 1-3, then 3-5, then 5-7)
- Deduplicate entries that appear in overlapping windows
- Handle cross-page entries (names split across page boundaries)

**For large documents (100+ pages):**
- Use `delegate_task` with parallel batches of 5-10 pages each
- Each batch includes the full extraction prompt + abbreviation key
- Merge results after all batches complete

```python
# Parallel batch pattern
delegate_task(tasks=[
    {
        "goal": "Extract structured data from pages 1-10 of <source>",
        "context": f"Extraction prompt: {prompt}\n\nPages text: {pages_1_10}",
        "toolsets": ["terminal", "file"]
    },
    {
        "goal": "Extract structured data from pages 11-20 of <source>",
        "context": f"Extraction prompt: {prompt}\n\nPages text: {pages_11_20}",
        "toolsets": ["terminal", "file"]
    },
    # ... more batches
])
```

### Step 4 — Quality Control

After extraction, verify quality before delivering results.

**Automated checks:**
- Count of extracted records vs expected (if known)
- Empty/null field rate (flag if > 20% of records have missing fields)
- Duplicate detection (exact matches across pages)
- Format validation (dates parse, addresses have street names, etc.)

**Manual spot-check (always do this):**
- Pick 3-5 random pages
- Compare extracted data against the original text
- Note any systematic errors (e.g., consistently misreading a character)
- If errors found, adjust the extraction prompt and re-run affected pages

**Quality score:**
```markdown
## QC Report: <source>

**Pages processed:** N
**Records extracted:** N
**Empty field rate:** X%
**Duplicate records:** N
**Spot-check results:** N/N pages correct
**Systematic errors found:** [list any]
**Quality score:** [high/medium/low]
**Recommended action:** [proceed / re-run with adjusted prompt / manual review needed]
```

## Output Format

### Structured Data File

Save as JSON with full provenance:

```json
{
  "source": {
    "title": "...",
    "author": "...",
    "date": "...",
    "archive": "...",
    "archive_url": "...",
    "extraction_date": "2026-05-29T...",
    "extraction_prompt_version": "v1"
  },
  "records": [
    {
      "id": 1,
      "data": {
        "name": "...",
        "occupation": "...",
        "address": "..."
      },
      "provenance": {
        "page": 42,
        "page_text_excerpt": "Smith, John — carpenter — 123 Main St",
        "confidence": "high"
      }
    }
  ],
  "qc": {
    "total_records": 1500,
    "empty_field_rate": 0.05,
    "quality_score": "high"
  }
}
```

### CSV Export (for spreadsheet/database import)

```csv
id,name,occupation,address,page,confidence
1,John Smith,Carpenter,123 Main St,42,high
```

## Data Storage

After extraction, store structured data to your knowledge base:

```python
# Create a summary page for the extraction
# Use whatever storage backend is available (memory, files, or a knowledge base tool)
```

## Pitfalls

- **Don't skip Step 1.** Orientation prevents wasted extraction runs on the wrong pages.
- **Test on a single page first.** A bad extraction prompt wastes tokens on every subsequent page.
- **Abbreviation tables are gold.** Always look for them — they're usually in the front matter or first few pages of data.
- **OCR errors compound.** If the source text has OCR errors, the extraction will inherit them. Clean the text first if possible.
- **Cross-page entries.** Names or records split across page boundaries require overlapping windows.
- **Confidence scores.** Always assign confidence (high/medium/low) based on OCR quality and extraction clarity.
- **Don't over-extract.** Only extract what the user asked for. Pulling every possible field wastes tokens and creates noise.

## Verification

After completing the pipeline:
1. ✅ Source profile created with structural analysis
2. ✅ Extraction prompt tested on 1-3 sample pages
3. ✅ Batch extraction completed with quality scores
4. ✅ Spot-check performed on 3-5 random pages
5. ✅ Structured output saved with full provenance
6. ✅ Results ingested to knowledge base
