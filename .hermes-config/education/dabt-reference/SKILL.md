---
name: dabt-reference
description: "Look up toxicology concepts across extracted reference texts (Casarett & Doull 9e, Hayes 7e, regulatory guidelines). Multi-pass search: identify chapters → get passages → load full context. Returns cited passages with source, chapter, page range."
category: education
---

# DABT Reference Lookup

## Trigger

Load this skill when:
- A drill question needs a sourced explanation (the database `Explanation` column is empty)
- A deep dive needs primary source citations for a mechanism, guideline, or threshold
- Abud asks "what does Casarett say about X", "look up Y in Hayes", "find the guideline for Z"
- The phrase "→ Read: [source]" appears in drill feedback and needs expansion
- Any time you need to pull a verified passage from the reference library
- The user asks "is this flashcard fact correct?" or requests a truth audit of study materials
- You need to cross-verify a claim across database answers AND reference texts (see `references/cross-verification-workflow.md`)

Always load `dabt-project-workflow` first to get the unified project config (source directories, extracted paths). Then load alongside `dabt-database` (for question context) and `dabt-drill-mode` or `dabt-deep-dive` (for session context).

## Reference Library

All extracted text lives under `/root/work/dabt/dabt-tutor/reference/extracted/`. The authoritative list of searchable sources is in `dabt-config.json` → `reference_library.searchable_sources`:

| Source | Chapters/Files | Size | Searchable |
|--------|---------------|------|-----------|
| Casarett & Doull 9e | 35 chapters | 10 MB | Yes |
| Hayes 7e | 39 chapters | 11 MB | Yes |
| Regulations (ICH, EPA, FDA, OECD) | 29 documents | 4.2 MB | Yes |
| **ABT Handbook 2026** | Full + outline | 99 KB | Yes — added 2026-05-20 |

Each source has an `index.json` (list of `{title, file, unit/category}` dicts). Page ranges are at the head of each extraction file (`# Pages: X-Y`) — always cite from the extraction header, not the index.

For the full source PDF layout, extraction pipeline, scripts, and quirks, see `references/reference-setup.md`.

For the workflow to evaluate and integrate a new batch of exam materials (recert exams, lecture notes, textbook PDFs) into the study infrastructure, see `references/material-onboarding.md`. This covers dedup against the existing library, value tiering, question database expansion, and wiki notebook integration.

For the three-layer flashcard/database/reference cross-verification workflow, see `references/cross-verification-workflow.md`. Use this when the user asks "is this flashcard correct?" or when running periodic truth audits — it walks through confirming flashcard facts against the question database, then against primary reference texts, then directly against references for general-principle cards.

**IMPORTANT — exam weight gap:** See `dabt-config.json` → `exam_blueprint.domains` for the authoritative domain weights vs DB distribution. Domain III (Risk Assessment) = 38% of exam but only 210 Qs (4.3% of DB). Domain IV (Applied) = 13% of exam but 2,850 Qs (58.9% of DB). Always consult the config before planning drilling or topic prioritization. Do NOT let DB availability drive study emphasis.

For the full source PDF layout, extraction pipeline, scripts, and quirks, see `references/reference-setup.md`.

For the workflow to evaluate and integrate a new batch of exam materials (recert exams, lecture notes, textbook PDFs) into the study infrastructure, see `references/material-onboarding.md`. This covers dedup against the existing library, value tiering, question database expansion, and wiki notebook integration.

For the three-layer flashcard/database/reference cross-verification workflow, see `references/cross-verification-workflow.md`. Use this when the user asks "is this flashcard correct?" or when running periodic truth audits — it walks through confirming flashcard facts against the question database, then against primary reference texts, then directly against references for general-principle cards.

## Procedure: Three-Pass Search

### Step 0 — Load Config

Before any search, read the project config to discover which sources are available:

```python
import json
with open('/root/work/dabt/dabt-tutor/dabt-config.json') as f:
    CONFIG = json.load(f)

WORKDIR = CONFIG['project']['workdir']
EXTRACTED_BASE = f"{WORKDIR}/{CONFIG['reference_library']['extracted_base']}"
SEARCHABLE = CONFIG['reference_library']['searchable_sources']
# SEARCHABLE is a list of {name, path, searchable} — use paths from it
```

This replaces hardcoded source paths. When a new source is added to the config, the reference skill automatically picks it up.

### Pass 1 — Identify Candidate Files

Use `search_files` with `output_mode="files_only"` to find which chapter/regulation files mention the query:

```
search_files(
    pattern="BMD|benchmark dose",
    path="/root/work/dabt/dabt-tutor/reference/extracted",
    output_mode="files_only"
)
```

If the query is a specific chemical, use the exact name plus common variants (e.g., `"organophosphate|OP|acetylcholinesterase"`). For regulatory topics, include guideline numbers (e.g., `"ICH S2|genotoxicity testing"`).

### Pass 2 — Get Relevant Passages

Run a content search with context on the top candidate files from Pass 1:

```
search_files(
    pattern="benchmark dose",
    path="/root/work/dabt/dabt-tutor/reference/extracted/casarett-doull-9e",
    context=3
)
```

Read the matches and identify the most relevant chapter. The file names encode chapter numbers and titles — prefer chapters whose titles match the topic (e.g., `3-dose-response-a-fundamental-concept-in-toxicology.txt` for BMD questions).

### Pass 3 — Load Full Section (if needed)

If the passage snippets are too thin, open the chapter file at the right offset:

```
read_file(
    path="/root/work/dabt/dabt-tutor/reference/extracted/hayes-7e/3-dose-response...txt",
    offset=<line near the match>,
    limit=80
)
```

### Citation Format

Always cite findings as:

```
[Source] Ch.[N] "[Chapter Title]" pp.[start]-[end]
→ [1-2 sentence summary of the relevant passage]
```

Examples:
- Casarett Ch.4 "Risk Assessment" pp.146-175 → BMD is defined as...
- Hayes Ch.3 "Dose-Response" pp.125-172 → The BMD approach differs from NOAEL in that...
- ICH S2(R1) Guideline pp.1-29 → The standard battery includes...

## Source Abbreviations

| Source | Abbreviation | Chapter level |
|--------|-------------|---------------|
| Casarett & Doull's Toxicology, 9e | Casarett | 35 numbered chapters |
| Hayes' Principles and Methods, 7e | Hayes | 39 numbered chapters |
| ABT Candidate Handbook 2026 | ABT Handbook | Full document + domain outline |
| ICH guidelines | ICH [code] | Individual documents |
| OECD test guidelines | OECD TG[#] | Individual documents |
| EPA guidelines | EPA [name] | Individual documents |
| FDA guidance | FDA [name] | Individual documents |

## Quick Topic → Chapter Mapping

For common DABT topics, these are the first files to search:

| Topic | Primary source | Chapter/file |
|-------|---------------|-------------|
| Exam blueprint, domain weights, task statements | ABT Handbook | exam-materials/ABT-Candidate-Handbook-2026.pdf |
| Dose-response, BMD, NOAEL | Hayes | 3-dose-response... |
| Risk assessment framework | Casarett | 4-risk-assessment |
| Mechanisms of toxicity | Casarett | 3-mechanisms-of-toxicity |
| Toxicokinetics / ADME | Casarett | 5-absorption..., 7-toxicokinetics |
| Biotransformation / metabolism | Casarett | 6-biotransformation... |
| Chemical carcinogenesis | Casarett | 8-chemical-carcinogenesis |
| Genetic toxicology | Casarett | 9-genetic-toxicology |
| Metals toxicity | Casarett | 23-toxic-effects-of-metals |
| Hayes | 19-metals |
| Pesticides | Casarett | 22-toxic-effects-of-pesticides |
| Hayes | 18-crop-protection-chemicals... |
| Solvents | Casarett | 24-toxic-effects-of-solvents-and-vapors |
| Hayes | 17-solvents-and-industrial-hygiene |
| Hepatotoxicity | Casarett | 13-toxic-responses-of-the-liver |
| Hayes | 32-hepatotoxicology |
| Hematotoxicity / blood toxicity | Casarett | 11-toxic-responses-of-the-blood |
| Nephrotoxicity | Casarett | 14-toxic-responses-of-the-kidney |
| Hayes | 33-principles-and-methods-for-renal-toxicology |
| Neurotoxicity | Casarett | 16-toxic-responses-of-the-nervous-system |
| Hayes | 35-neurotoxicology |
| Immunotoxicology | Casarett | 12-toxic-responses-of-the-immune-system |
| Hayes | 39-immunotoxicology... |
| Developmental toxicity | Casarett | 10-developmental-toxicology |
| Animal/plant toxins, venoms, antivenoms | Casarett | 26-toxic-effects-of-plants-and-animals |
| Animal/plant toxins, venoms, antivenoms | Hayes | 15-plant-and-animal-toxins |
| Clinical toxicology, antidotes, chelation | Casarett | 33-clinical-toxicology |
| Genotoxicity testing | Regulations | ich-s2r1-guideline.txt |
| Genotoxicity testing | Regulations | ich-s2r1-guideline.txt |
| Carcinogenicity testing | Regulations | ich-s1a, s1b-r1, s1cr2 |
| OECD test guidelines | Regulations | oecd/tg*.txt |
| Food safety / Redbook | Regulations | redbook*.txt |

## Pitfalls

- **Don't search the whole extracted/ tree every time** — narrow to the relevant source first (Casarett vs Hayes vs regs) unless the topic spans multiple sources
- **Chapter titles are in the filenames** — use them to gauge relevance before reading
- **Page numbers**: search_files returns file line numbers, not book pages. Scan the text for embedded printed page markers (standalone numbers like "1124" on their own line, often followed by "Toxic Agents" or chapter headers) to report accurate pagination. Never cite extraction line numbers as pp. values.
- **Page numbers: use the extraction header, not internal markers.** Every extraction file begins with a header block including `# Pages: X-Y` — this is the authoritative PDF pagination for the chapter. Internal page markers (standalone numbers on their own lines like `1124`) are printed book page numbers, which may differ from PDF pages. When the user asks for page numbers, always cite from the header, never from line numbers or internal markers. If the header and internal markers disagree, cite the header range and note the offset.
- **Regulations don't have TOC** — they're single documents, so Pass 2 (content search with context) is usually sufficient
- **If a search returns nothing**, the topic may use different terminology. Try synonyms (e.g., "benchmark dose" ↔ "BMD", "uncertainty factor" ↔ "UF" ↔ "safety factor")
- **The index.json files are your best friend** — read them first if you need an overview of available chapters
- **Distinguish clinical from regulatory thresholds.** The same parameter can have different values depending on context. For example, Casarett says lead chelation is warranted at BLL >60 µg/dL (clinical treatment threshold) while OSHA mandates maintaining BLL <40 µg/dL (regulatory standard for occupational exposure). Both are correct — cite the applicable context. When a flashcard or database answer gives one value, verify which frame (clinical vs regulatory) it's answering.
- **DB answers may contradict reference texts.** When writing explanations, always cross-verify the DB's `correct_answer_letter` against the reference text before writing. This session (batch 8) found ~15+ discrepancies in 50 questions. Common patterns to watch for:
  - *Matching-type questions* — the chemical-to-effect mapping in the DB is sometimes swapped or misattributed (e.g., desmopressin matched to megaloblastic anemia instead of von Willebrand treatment; mitomycin to left-shift instead of HUS)
  - *"Except" questions* — the answer letter sometimes points to the TRUE statement, not the exception (e.g., IgG can fix complement listed as the exception when it's actually true; T cells listed as not involved in humoral response)
  - *Basic immunology reversals* — several DB answers contradict the textbook on fundamental concepts: negative selection said to occur in the spleen (DB) vs thymus (Casarett), T cell precursors said to migrate to Peyer's patches (DB) vs thymus (Casarett)
  - *Hematology data* — clotting factor ordering (Casarett says factor VII has shortest half-life at 3-4hr, DB says IX); O2 dissociation curve shifts (DB says acidosis causes left shift, textbook says acidosis causes right shift/Bohr effect)
- **When a contradiction is found**, note it in the explanation rather than silently accepting the DB answer. Format: include the textbook-supported fact alongside the DB's answer, flagged with "Note:" or "Reference check:". The user needs to know which source is authoritative for the DABT exam.
