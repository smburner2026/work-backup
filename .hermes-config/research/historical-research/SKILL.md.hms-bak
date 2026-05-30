---
name: historical-research
description: "Primary-source historical research with Hermes — document acquisition, OCR/extraction, translation, provenance tracking, and structured data extraction from archival sources. Covers the full pipeline from source discovery to G-Brain ingestion."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [history, archives, primary-sources, OCR, provenance, document-extraction, research]
    category: research
    requires_toolsets: [terminal, file, web, search]
    related_skills:
      - ocr-and-documents
      - academic-book-retrieval
      - book-hunting
      - document-translation
---

# Historical Primary Source Research

Class-level skill for conducting primary-source historical research using Hermes. Covers source acquisition, document processing (text and scanned), translation, structured data extraction, and provenance tracking.

This skill encodes the **agentic historian methodology** — inspired by the Chronos AI Historian framework (arXiv 2604.03553, Apr 2026), adapted to Hermes's tool ecosystem. The core principle: historical research is an iterative reasoning process, not a fixed pipeline. Each source type (census, directory, manuscript, newspaper, correspondence) needs adapted extraction procedures.

## Architecture

```
WORKSPACE/
├── sources/           # Read-only source documents (originals preserved)
│   └── <source-name>/ # Per-source directory
│       ├── source.pdf # Original file
│       └── extracted/ # Text output from OCR/PDF extraction
├── data/              # Structured output (JSON, CSV per source)
├── skills/            # Source-type-specific extraction procedures
│   └── <source-type>/
│       └── SKILL.md   # Natural-language extraction instructions
├── memory/            # Cross-session persistent findings
│   ├── MEMORY.MD      # Cross-source insights, provenance chain
│   └── <source-name>.md # Per-source findings and notes
└── reference/         # Downloaded documents indexed in G-Brain
```

## Pipeline (4-Step Agentic Extraction)

### Step 1 — Range-Finder (Source Orientation)
Before extracting, understand the document structure:
- Scan table of contents, index, captions, figure legends
- Identify the page ranges containing target data
- Note structural cues: column layouts, abbreviations, date format, name patterns
- Handle printed page numbers vs PDF page number discrepancies
- **Verification:** Show the historian proposed start/end pages before proceeding

### Step 2 — Prompt Construction (Per-Source Adaptation)
Build extraction instructions tailored to the source type:
- Incorporate structural cues from surrounding pages
- Define column schemas and field extraction rules
- Note source-specific edge cases (missing data, ambiguous entries, variant spellings)
- Test on 1-2 representative pages before full batch
- **Pitfall:** Do not assume a fixed prompt works across different source types — adapt per corpus

### Step 3 — Batch Extraction
Parallel extraction with human-in-the-loop confirmation:
- Use `delegate_task` for independent page batches
- Include the extraction prompt AND source-specific structural notes in every delegate context
- Process pages in batches of 5-10, with quality checkpoints between batches
- **Pitfall:** Subagents have no session memory — pass all extraction rules explicitly in context

### Step 4 — Quality Control
Verify extracted data against source:
- Spot-check N pages (N ≥ 5% of total, minimum 3)
- Verify: field alignment, missing entries, boundaries, edge cases
- Fix extraction prompt for systematic errors, re-run affected batches
- Flag contradictions between sources rather than harmonizing them
- Log provenance: which source, page, line extracted each fact

## Capabilities

### Source Acquisition
Use these installed skills to find and download primary/secondary sources:
- **`academic-book-retrieval`** — LibGen/Anna's Archive/Internet Archive (monographs, textbooks)
- **`book-hunting`** — LibGen ISBN search + download (narrower, textbook-focused)
- **`web_search` + `web_extract`** — archival finding aids, library catalogs, open-access repositories, Google Books
- **`web_extract`** (PDF URLs) — direct extraction from online PDFs (arxiv, institutional repositories)

### Document Processing
| Source Type | Tool | Approach |
|---|---|---|
| Text-based PDF (post-2000) | `ocr-and-documents` → pymupdf | Straight text extraction, instant |
| Scanned PDF (image-only) | `ocr-and-documents` → marker-pdf | Full OCR (~3GB PyTorch models, 90+ languages) |
| Fraktur/Gothic type (pre-1945 German) | pymupdf + Fraktur cleaning | Text extraction + 4-pass regex/dictionary cleanup (see `ocr-and-documents/references/fraktur-german-ocr-cleaning.md`) |
| Handwritten/manuscript | `vision_analyze` | VLM-based transcription per page image |
| Multi-column/complex layout | marker-pdf | Layout-aware extraction with reading order detection |

### Translation
Use **`document-translation`** for foreign-language primary sources:
- Vietnamese/French/German/etc. source text → English
- Glossary construction for proper nouns, ranks, place names
- Layout-preserving output with embedded images at narrative positions
- **Critical:** Always translate chapters 1-3 as sample for user sign-off before batch translation

### Provenance Tracking
Every fact extracted should carry:
1. **Source identifier** (archive/document/page)
2. **Extraction method** (pymupdf text / marker-pdf OCR / VLM / manual)
3. **Confidence assessment** (high: direct text extraction; medium: OCR with post-processing; low: VLM transcription)
4. **Cross-references** to other sources that confirm or contradict

Ingest to G-Brain with tags: `era`, `region`, `source-type`, `archive`.

## Extraction Prompt Formula (for Structured Data)

When building an extraction prompt for a batch:

```
You are extracting data from <SOURCE-TYPE> on pages <N-M>.
Document language: <LANG> | Date: <DATE> | Archive: <ARCHIVE>

Structure:
- Each entry has: <FIELD1>, <FIELD2>, <FIELD3>
- Column layout: <describe visually>
- Abbreviation table: <list known abbreviations>

Rules:
- Missing data: leave null, do not infer
- Ambiguous entries: flag with "??" and note the ambiguity
- Variant spellings: preserve original, add a note
- Boundary detection: <rule for where entries start/end>

Return as JSON array with per-entry provenance: {source_page: N, extracted_text: "...", fields: {...}}
```

## Pitfalls

- **Source-distinguish failure:** When researching multiple sources on the same topic, do not assume you know which source the historian means after providing options. One clarifying question ("Which source should we work from?") costs less than building a pipeline for the wrong document.
- **terminal() stdout cap** at ~50KB. For large text blocks (full-page OCR, multi-page extractions), read with Python `open()` directly or split reads.
- **PDF header verification:** Always check downloaded PDF starts with `%PDF-1.x` and has a reasonable file size before investing time in extraction.
- **Fraktur text pymupdf sufficiency:** Google Books pre-1924 German PDFs are text-based (not scanned), so pymupdf alone suffices — marker-pdf adds ~3GB model download for no benefit.
- **Provenance chain maintenance:** When switching between sources, update the cross-source memory file before starting the new source. Otherwise, contradictions between sources are discovered too late for efficient correction.

## References

- Chronos: AI Agent for Historical Data Extraction — arXiv 2604.03553, `github.com/ai-historian/chronos`
- `ocr-and-documents/references/fraktur-german-ocr-cleaning.md` — Fraktur cleaning patterns
- `academic-book-retrieval` — Book/source acquisition workflow
- `document-translation` — Foreign language document translation pipeline
