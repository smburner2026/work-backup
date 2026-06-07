---
name: dabt-reference
description: "Primary reference lookup for DABT study — file search + grep cross-source synthesis across Casarett & Doull 9e, Hayes 7e, regulatory guidelines, ABT handbook. Multi-pass workflow for page-level depth."
category: education
---

# DABT Reference Lookup

## Trigger
Load when: drill question needs sourced explanation (DB Explanation empty) | deep dive needs citations | "what does Casarett say about X" | "look up Y in Hayes" | "→ Read: [source]" drill feedback | truth audit | flashcard fact verification. Load `dabt-project-workflow` first for config (source directories, extracted paths).

## Content Gap Discovery (When Material Is Missing)
When the user asks about missing content or you discover the library is incomplete:

1. **Audit what's on disk** — Compare the source directories against the DABT exam outline. Resolve searchable source paths from `config['reference_library']['searchable_sources']`. List files, count them, note what's present and what's absent.
2. **PRESENT findings FIRST** — Show the user the gap analysis: what's there, what's missing, prioritized by DABT exam weight. Include file counts and size estimates. **Do not start downloading.** The user needs to see the map before approving the route.
3. **Get confirmation** — Let the user confirm the priority list and batch sizes before any downloads begin.
4. **Cron-job exception** — When this skill is triggered from a cron job (no user present — detectable via the system prompt note: "You are running as a scheduled cron job"), steps 2-3 are skipped. The user already specified exact targets in the cron definition. Proceed directly to downloading.
5. **Download via background-agents or cron** — Batch downloads of 5+ documents MUST use async methods (cron jobs or background agents), NOT synchronous `delegate_task`:
   - **1–4 docs** → small synchronous batch is acceptable
   - **5+ docs** → use `background-agents` skill (cronjob with `schedule='1m'`, `repeat=1`, `enabled_toolsets=['web','terminal','file']`)
   - **3+ parallel batches** → multiple cron jobs, not multiple delegate_task calls
5. **Verify files landed** — When the background job reports back, check file sizes (not empty/truncated) before telling the user it's done.
6. **Update index.json** — After new files arrive:
   - Read the current `index.json` from the relevant source directory (resolved from `config['reference_library']['searchable_sources']`)
   - Add entries for new files with `title`, `category`, `file`, and `pages` fields
   - Rebuild the full index (don't just append — recalculate `total_documents` and sort)
   - Write the updated file. The index is what makes `search_files` discover new content.

**Critical pitfall — synchronous timeout cascade:** `delegate_task` blocks the LLM turn. A subagent searching/downloading/parsing 15–20 government PDFs can take several minutes. The model provider will timeout, the session will drop all work-in-progress, and zero output reaches the user. Using cron jobs for large batches decouples the download time from the conversation and avoids this entirely.

**Download strategy by content type:**
- **HTML pages** (EPA summaries, ECHA, OSHA text): Use `web_extract` directly — fast enough for 10+ pages in a single session. Up to 5 URLs per call.
- **eCFR content**: Use `https://www.ecfr.gov/current/` path (NOT `/api/versioner/` which returns 404). `web_extract` handles this well.
- **PDFs** (full guideline documents): Use pdftotext. For 5+ PDFs, use cron/background-agents to avoid timeout.
- **Multi-page composition**: For comprehensive coverage, compile from 2-4 source URLs per document. Each extracted section adds a `# Source: <url>` comment.
- See `references/regulatory-source-urls.md` for verified source URLs by regulatory body.

## Reference Library
Extracted texts at `config['reference_library']['extracted_dir']` from `dabt-config.json`. Searchable sources:

| Source | Chapters | Size | 
|--------|---------|------|
| Casarett & Doull 9e | 35 ch | 10 MB |
| Hayes 7e | 35 ch | 10 MB |
| ABT Handbook | full | | 
| FDA Redbook | full | |
| EPA Guidelines | full | |
| ICH Guidelines | full | |
| NTP Studies | various | |

## Lookup Workflow (3-Pass)

**CRITICAL: File search is PRIMARY.** Every reference lookup starts with file search. Grep and read_file provide progressively deeper detail.

### Pass 1 — Identify Target (File Search)
Use `search_files` to find which source and chapter contain the answer.

**Pass 1 commands:**
- `search_files(target='files', pattern='*chapter*', path=SOURCE_DIR)` — locate chapter files
- `search_files(target='content', pattern='keyword|synonym1|synonym2', path=SOURCE_DIR, file_glob='*.md')` — cross-source content search

**Pass 1 tips:**
- Use multiple keyword variations (synonyms, abbreviations) to cast a wide net
- Filter by file glob (e.g., `*.md`) to target extracted markdown files
- Limit results to 3-5 most relevant files
- Note the file paths and line numbers of promising matches
- When you need the exact passage, proceed to Pass 2

### Pass 2 — Extract Relevant Passage (Grep)
Search within the identified file(s) for the specific passage.

**Pass 2 commands:**
- `search_files(target='content', pattern='...', path=SPECIFIC_FILE, context=3)` — grep with context lines
- Narrow the pattern to the exact claim or phrase you need to verify

### Pass 3 — Load Full Section (Read File)
Read the full section/paragraph using `read_file` with offset+limit for the relevant lines.

## Citation Format
`[Source] Ch.[N] "[Chapter Title]" pp.[start]-[end]`

## Cross-Verification Workflow (Drill Questions)
When a DB answer conflicts with reference text:
1. Search extracted markdown for the specific claim (file search)
2. Grep within matched files for the exact passage
3. Flag discrepancy to user with both sources cited
4. Do NOT silently correct — present both sources and let user decide

Full workflow in `references/cross-verification-workflow.md`.

## Vault Handoff (after every lookup)

When a reference lookup produces a non-trivial finding (a passage that anchors an exam-relevant fact, a regulatory threshold, a mechanism clarification):

1. **Identify the concept** — what topic does this passage most directly support? Check the topic→chapter map in `wiki/populate-vault.py` (or `wiki/concepts/<slug>.md` if a note exists).
2. **Suggest expansion** — at the end of the lookup response, surface: "This passage is cited by `wiki/concepts/<slug>.md` (stub) — want me to add it as a source pointer?"
3. **When user agrees (or when running unattended)**, patch the concept note's `## Source pointers` section with the chapter:line citation, OR create a new concept note stub if the topic isn't yet in the vault.
4. **Wikilink the chapter** — if the chapter file doesn't already have a `## Cross-references (vault)` section, append one. (The `wiki/inject-wikilinks.py` script does this in bulk for the standard curriculum map; ad-hoc additions are fine.)

The lookup is half the work. The other half is making the finding findable next time — the vault is the layer that makes that happen.

## Batch Download Reference (Regulatory URLs)
When downloading regulatory documents for the reference library, consult `references/regulatory-source-urls.md` for verified source URLs across EPA, OSHA, eCFR, ECHA (REACH), UN GHS, and NTP. Documents the URL patterns, fallback sources (e.g., PubChem when UNECE is unreachable), batch extraction strategy, and file provenance conventions. New regulatory source patterns discovered during downloads should be added there.
