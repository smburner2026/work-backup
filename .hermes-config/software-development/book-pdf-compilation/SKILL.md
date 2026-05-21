---
name: book-pdf-compilation
description: Compile a series of markdown chapters, OCR text pages, or sourced PDFs into a single bound PDF volume (fpdf2 or WeasyPrint). Handles noise cleaning, chapter ordering, table of contents, title casing, inline formatting, and academic styling.
---

# Book PDF Compilation Skill

Compile a series of markdown chapter files into a single bound PDF volume using fpdf2 (Liberation Serif font).

## Sourcing Layer — Before Compilation

See `references/multi-source-text-sourcing.md` for the **text acquisition pipeline** — identifying the right translator/edition, sourcing from public domain (Johnston, Project Gutenberg) vs shadow libraries (Anna's Archive, LibGen) for copyrighted print-only editions, file organization convention, and translation verification. This feeds into the compilation workflow below.

See `references/editorial-apparatus-stripping.md` for the **editorial footprint stripping** — removing Kaufmann's COMMENT blocks, numbered footnotes, translator introductions, and publisher back matter from anthology source texts before compilation.

See `references/johnston-text-cleaning.md` for the specific cleaning patterns used on Ian Johnston's plain-text Nietzsche translations (Birth of Tragedy, BGE, Genealogy, Use and Abuse) — including `\xa0` handling, split-line boilerplate fragments, `=====` section dividers, and per-work content-start markers.

## Workflow

1. **Source texts** — follow `references/multi-source-text-sourcing.md` to acquire all source files into `sources/` (supports public domain, Anna's Archive/LibGen, and cron-based parallel background sourcing)
2. **Inspect reference PDF** — if the user provides or references an existing PDF as a style target, inspect it immediately:
   - `pdfinfo <path>` — page size, margins, page count, producer/creator
   - `pdftotext <path> - | head -80` — structural layout, heading hierarchy, TOC style, font hints
   - Note page size (e.g. Letter vs 6x9), font family, body font size, margins, and any distinctive formatting features (title page, running headers, page numbers)
   - Use these properties as the style target for the build. When the user says "make it look like this," they mean: match the typographic feel and structural quality, not pixel-perfect replication.
3. **Clean source text** — before any pipeline, run a preprocessing pass that always includes:
   - Collapse multiple spaces: `re.sub(r'  +', ' ', text)` — OCR/digitised texts frequently have variable inter-word spacing that breaks layout engines
   - Remove backticks: `` text.replace('`', '') `` — prevent monospace font bleed-through in WeasyPrint
   - Fix underscore artifacts: `re.sub(r'(\w)_(\w)', r'\1 \2', text)` — mid-word underscores from OCR
   - Normalize line endings: `text.replace('\r\n', '\n').replace('\r', '\n')`
   - Collapse triple+ newlines: `re.sub(r'\n{3,}', '\n\n', text)`
   See `references/weasyprint-workflow.md` for the full `cleanup_text()` function template.
4. **Choose PDF engine**:
   - **fpdf2** (default) — for OCR text, academic manuscripts, Liberation Serif 12pt, memory-constrained environments
   - **WeasyPrint** (see `references/weasyprint-workflow.md`) — for CSS-controlled typography, proper justification with hyphenation, font variety. Preferred font: Liberation Serif (same family as fpdf2 path). Use per-work build + pdfunite merge when corpus exceeds ~3MB to avoid memory issues.
   For large multi-work anthologies (1,000+ pp, 5+ works), see `references/weasyprint-anthology-pipeline.md` for the validated per-work → pdfunite merge approach, CSS specs, and cleanup pipeline used on the 4,402-page Nietzsche Complete Works build.
5. **Extract chapters** from source into individual `.md` files in `md_dir/` (for EPUB sources, always use spine order, not alphabetical sort — see `references/weasyprint-anthology-pipeline.md`)
6. **Define chapter order** via a `BOOK_ORDER` list (slugs matching filenames)
7. **Define section mappings** for which slugs belong to which chapter and their section numbers
8. **Create compiler script** (`compile_book.py` for fpdf2, `build_works.py` for WeasyPrint) and run it

## Style Preferences (user's established choices)

- **Quality priority**: Structure and formatting quality (clean typography, proper headings, good spacing, readable body text, no visual overflow) are the primary concern — *not* visual unification across different works in a collection. It is acceptable for different works to look different from each other. Each should simply look good on its own terms.
- **Font**: 12pt Liberation Serif (LiberationSerif-*.ttf on Ubuntu/Debian)
- **Leading**: 6.5pt
- **Margins**: 25mm
- **Body**: justified text for markdown chapters (`align='J'`); left-aligned for OCR-sourced text (`align='L'` — fpdf2's justification engine breaks on long hyphenation-free paragraphs)
- **Chapter titles**: 16pt bold centered, with a decorative rule beneath
- **Section labels on chapter pages**: 11pt italic gray
- **Subsection headings (`##`, `###`)**: rendered as bold centered (`##`) or left (`###`) rather than skipped
- **Inline formatting**: `*italic*` → italic, `**bold**` → italic (academic convention, not bold), `***bold italic***` → bold italic
- **Title case** (applied to all chapter/section titles):
  - First and last word always capitalized
  - First word after `:` , `?` , `—` , `!` , `;` always capitalized
  - Proper nouns always capitalized (Communist, Bolshevik, Soviet, Hitler, Stalin, German, Russian, European, Nazi, Fascist, etc.)
  - Minor words lowercase mid-sentence (of, the, and, in, to, from, with, against, towards, by, at, as, into, etc.)
  - ALL-CAPS preserved as-is
- **TOC**: Hierarchical — chapter headings in bold, sections indented in italic
- **Overflow protection**: single words wider than page width fall back to `multi_cell()` wrapping

## Key Implementation Details

### extract_title_from_md(md_text)
Priority order:
1. `# Heading` (multiline)
2. `**N. Section Title**` (bold with leading number)
3. `N. Section Title` (plain numbered at paragraph start)
4. `**Title**` (bold, excluding Chapter-line starts, `[bracket notes]`, Roman-numeral heads)
5. `Chapter X: Title` pattern
6. `**IV Chapter Head**` (bold Roman-numeral)
7. `IV. N. Title` (chapter.section numbering)
8. First substantive standalone line (15-150 chars, capital start, plain text)

### to_title_case(text)
Standard English title case with custom proper-noun set and after-punctuation capitalization.

## User Workflow Preferences (sequential-gated)

### Plan Phase vs. Execute Phase — Know Which You're In

This user has TWO modes, and confusing them produces frustration:

**Plan Phase (NEW work):** When introducing a new project with unknown translators, formats, or sources — present the complete plan with options, then wait for explicit confirmation before firing any downloads, extractions, or builds. Sourcing preference: Authorized Path 2 — copyrighted translations from Anna's Archive / Library Genesis for personal research compilations when public domain translations are unavailable or inferior. Always confirm the translator-per-work map with the user before sourcing.

**Execute Phase (established/continuing work):** When the user says "continue with this PDF thing" or references a known project, **check disk state and execute immediately**. Do not re-open the planning phase. The user's signal to enter execute phase:
- Refers to a previously-discussed project by name ("the anthology," "that PDF thing," "the Nietzsche book")
- Says "just do it," "queue it up," "/queue," "go ahead," or "pull the pdfs from annas again"
- Sends a reference file and says "this is what I'm talking about"

When in execute phase:
1. Check what's already on disk (sources/, output/)
2. Report what's present and what's missing
3. **Execute what's doable** — don't stop to ask "which ones?"
4. Flag roadblocks concisely: "X missing, Y available, proceeding with Y"
5. The "/queue" prefix means "background this, report when done, don't stop to ask"

**CRITICAL — Don't Double-Back:** Once the user says "continue" and provides a reference, you already have enough context. Searching prior sessions for more detail is fine; asking the user to re-state what they just told you is not. If something is genuinely ambiguous, state the ambiguity + your best guess + execute — don't present a multiple-choice menu.

**Sourcing confirmation shortcut:** When the goal is "pull the same PDFs we used before," the user expects you to know what those were from the current context. If you're unsure, check on-disk state first, then ask a targeted question like "Everything's already here — do you want me to re-download or proceed with whats on disk?" — not "which ones?"

**Post-completion protocol:** When the build finishes and you report state, do NOT offer branching next-step options or menus ("Which direction? A/B/C/D"). State clearly what was built and its dimensions, then stop and await instructions. The user will tell you what they want next — proposing unprompted follow-ups gets deflected. This is the completion-side corollary of the sequential-gated preference.

## Pitfalls

### CRITICAL: EPUB Alphabetical Sorting Bug — Prologue After Part 4

When extracting text from EPUBs, the reading order is defined by the **spine** (`<opf:spine>/<opf:itemref>`) in the OPF file, **not** by alphabetical filename sorting. Extracting via `sorted(z.namelist())` puts `prologue.html` after `part4_chap_20.html` alphabetically, resulting in a text where the Prologue appears after Part 4 — and the user sees Zarathustra's descent, "God is dead," the marketplace speech, and "man is a rope over an abyss" as missing.

**Always use spine order.** Parse the OPF manifest to get the `idref -> href` mapping, then iterate `<spine>` itemrefs in order. The `document-pipelines` skill's `references/curated-anthology-workflow.md` has the full extraction snippet. Cross-reference when building anthology compilers.

**Verification:** After extraction, grep for the Prologue opening line (`"When Zarathustra was thirty"` for Hollingdale, `"thirty years old"` for Parkes) and confirm it appears BEFORE Part 1 content. If the Prologue comes at line 1600+ in a text that should be ~1500 lines total, the extraction used the wrong order — re-extract with spine order.

### CRITICAL: Words Running Off the Page (WeasyPrint) — RECURRING FAILURE

This is the most consistent failure pattern across all PDF build projects. **Always check and fix before delivering.** The user has explicitly flagged this as a "very consistent failure with these projects."

**WeasyPrint path:** CSS body MUST include `overflow-wrap: break-word; word-wrap: break-word;` — WeasyPrint does not break long words by default. Without it, any word wider than the text column (long German compounds, chemical names, URL-like strings, Greek terms in serif) overflows into the margin or off the page. The last build that lacked this produced an 11,013-page volume with running-off text.

**fpdf2 path:** skill covers this already (`multi_cell` fallback for wide words), but verify each build — a single `cell()` call on a wide word in a loop can clip text silently.

**Font size:** Body text at 14pt DejaVu Serif on a 6×9 page with 1in margins leaves only ~4in of text width (roughly 60 characters per line at 14pt). This makes long words far more likely to overflow. For anthologies (1000+ pages), use **11pt body**. For standard books (300-1500p), use **12pt**. Reserve 14pt for short standalone works.

### User Interaction: Terminal Commands Must Be Copy-Pasteable

This user gives commands in Android Termux where copy-paste is painful. When you need them to run terminal commands on their phone:
- Present each command as its OWN code block — no chaining `&&` unless essential
- No inline prose explanations inside or after the command block
- Do not wrap commands in larger sentences or paragraphs
- If there's a sequence, list them as separate raw code blocks without numbering in the prose
- Let the command speak for itself; add explanations separately if needed
- When they ask "Just the raw text" for copy-paste, strip ALL commentary and deliver only the line-by-line commands

### Font Selection — "Weird Fonts" Syndrome

The user's established font is **Liberation Serif** (used in all fpdf2 compilations). When the WeasyPrint path uses DejaVu Serif instead, the user perceives it as "weird fonts." Always match the font family between fpdf2 and WeasyPrint paths for consistency.

Additional font-related traps:
- **Backtick bleed** — source texts containing backtick ` markers (common in Stanford critical edition volumes) cause WeasyPrint to render `<code>` spans in DejaVu Sans Mono. Stripping backticks in `cleanup_text()` prevents this.
- **Missing italic** — plain text source files (Project Gutenberg, Johnston translations) have NO italic markers, so book titles, foreign phrases, and emphasis render as roman. This is a source-quality limitation, not a bug, but flag it when the user asks about italic.

### General Pitfalls

- fpdf2 `cell()` does NOT wrap — any single word wider than page width must use `multi_cell()` instead
- `re.MULTILINE` is required for `^`/`$` patterns when scanning markdown body text
- `self` is not available in outer `compile_book()` function — use `pdf.w` instead of `self.w`
- Liberation Serif italic font missing `\n` glyph is a cosmetic warning, not an error
- When stripping punctuation for `to_title_case`, use `lstrip`/`rstrip` to track leading/trailing punctuation separately (avoids double-letter bug from `w[:len(w)-len(stripped)]` approach)
- **OCR-specific pitfalls and workflow**: see `references/ocr-page-compilation.md` — covers noise identification via frequency analysis, header blacklisting, line-break joining, and continuous text flow. **Critical:** three compounding fpdf2 `multi_cell` bugs (x-position drift, long-string corruption, chunk boundary artifacts) force the use of `write()` instead of `multi_cell` for any continuous text longer than ~50K characters. See the "Critical fpdf2 Pitfalls" section in that reference for symptoms and verification commands.
- **OCR sources always require 2–3 cleaning iterations** — the first pass will miss noise patterns visible only in the cleaned output. Budget for this. Each iteration: generate → inspect with PyMuPDF → add newly visible artifacts to the blacklist → regenerate.\n- **One-word-per-line OCR artifacts** — Some PDF-extracted source texts have every word on its own line. The `cleanup_text()` function in `references/weasyprint-workflow.md` includes an OCR reflow pass that detects and joins consecutive short lines into proper paragraphs. This is essential before any markdown-to-HTML conversion — without it, every word renders as its own `<p>` in the PDF.\n- **Prefix-match for OCR merge artifacts** — running headers sometimes fuse with the next text line (e.g. "The Magic NameT"). Exact-match blacklisting misses these. Use `startswith(header)` plus a ≤3 char trailing tolerance to catch them.
- **Never deliver an OCR-sourced PDF without inspecting it first** — extract 5–8 sample pages, scan for residual headers, numbers, and stamps, and only report to the user once confirmed clean.
- **`align='J'` breaks on OCR text** — fpdf2's justification stretches inter-word spacing to fill the line. Without hyphenation, long paragraphs produce lines with too few words to stretch, causing the engine to break early at the same hard-break positions you just fixed. Use `align='L'` for all OCR-sourced text.
- **Non-breaking space (`\\xa0`) in boilerplate detection** — Source texts from web publishers (Johnston translations, Project Gutenberg) frequently use `\\xa0` (non-breaking space) instead of regular spaces in boilerplate lines. Python's `.strip()` does NOT remove `\\xa0`. Calling `cleaned = stripped.replace('\\xa0', '')` before checking against boilerplate sets/patterns prevents missed matches. This affects lines like `'Beyond Good and Evil [RTF]\\xa0'` and `'\\xa0PART ONE'` where the `\\xa0` causes exact-set and regex-anchor matching to fail silently.
- **Split-line boilerplate fragments** — Boilerplate lines in web-sourced texts are sometimes split across multiple physical lines (e.g. `'[Table '` on one line, `'of Contents for Beyond Good and Evil]'` on the next). Line-by-line detection misses these fragments. Check for unique fragment prefixes (`'[Table'`, `'[RTF]'`, etc.) rather than requiring the full phrase. When in doubt, `'[Table' in cleaned` or `'[RTF]' in cleaned` catches what `r'^\[Table of Contents'` misses on partial lines.
- **OCR files are physical pages, not paragraphs** — joining them with `\\n\\n` and splitting into paragraph blocks creates artificial breaks at page transitions. Either use section-based reconstruction (preferred, Phase A) or join all text as one continuous flow with spaces (monolithic fallback).

## DOCX Compilation (Alternative to PDF)

When the user requests a Word document (.docx) rather than a PDF — for review, editing, or track-changes — use the DOCX compilation workflow instead of the fpdf2 PDF path. See `references/docx-compilation.md` for the complete approach: explicit chapter ordering, source-file heading pattern handling, python-docx formatting (Garamond, heading hierarchy, centered headings with small caps), title page construction, and confirmed pitfalls from the Vallentin Napoleon translation project (36 chapters, ~1.1M chars).

## OCR Text Page Collections (HathiTrust / University of Michigan scans)

When the source is a ZIP or directory of numbered `.txt` files (e.g. `00000001.txt` … `00000328.txt`) rather than structured Markdown chapters, the user's preferred workflow is **section-based reconstruction** — identify structural boundaries, clean each to its own file, then compile. This is superior to the monolithic concatenation approach because it preserves section identity, makes targeted cleaning easier, and allows per-section inspection before the final compile.

### Phase A: Strip Front/Back Matter and Rebuild Sections

1. **Extract** with `python3 -m zipfile -e`, sort strictly numerically by filename.
2. **Frequency-analyze** to discover running headers (see `references/ocr-page-compilation.md` for the sampling script). Build the blacklist from data, not guessing.
3. **Delete TOC and index pages entirely** — do not attempt to clean them. TOC pages are identified by dotted leader lines (`....`), dense page-number references, or "TABLE OF CONTENTS" / "CONTENTS" headers. Index pages are identified by dense `Name, description, page_numbers` patterns. They produce more noise than value and will be rebuilt from the section structure later.
4. **Identify section boundaries** — scan through the cleaned pages and detect chapter/section headers (large text, Roman numerals, standalone bolded lines, `Chapter N` patterns). Split the corpus at these boundaries.
5. **Rebuild each section into its own `.txt` file** in an output directory (e.g. `sections/`). Name files by section number and slug (e.g. `01-preface.txt`, `02-ch1-introduction.txt`). This gives you per-section granularity for inspection and cleaning.

### Phase B: Clean and Fix Each Section File

6. For each `.txt` file: remove running headers, page numbers, library stamps, and OCR merge artifacts (prefix-match with ≤3 char trailing tolerance).
7. **Run a line-break fixing pass** — join hyphenated words across newlines, then detect and fix mid-sentence line breaks (a line ending without sentence-terminal punctuation followed by a line starting lowercase is a mid-sentence break). The text should flow naturally with paragraph breaks only at actual paragraph boundaries.
8. Scan each cleaned section file for residual noise before proceeding.

### Phase C: Compile from Clean Sections

9. Feed the cleaned per-section `.txt` files into the compiler instead of raw OCR output. Either convert to `.md` with appropriate formatting or add a plain-text body writer to the compiler script.
10. Generate the TOC from the section structure, not from OCR content.
11. Use `write(6.2, section_text)` for body text — **never `multi_cell` for continuous OCR text** (see `references/ocr-page-compilation.md` "Critical fpdf2 Pitfalls" for the three compounding bugs this avoids). For the monolithic fallback path (when section-based reconstruction isn't done), join all cleaned text with spaces and call `pdf.write(6.2, full_text)` once. `write()` is always left-aligned, which is correct for OCR-sourced books.
Always inspect the first 5–8 pages of the generated PDF **before** telling the user it's done. Extract with PyMuPDF and scan for residual noise. If clean, report the page count and path. If not, iterate the cleaner and regenerate.

See `references/mantle-of-caesar.md` for the complete reproduction recipe, header blacklist, iteration count, output statistics (328 raw pages → 185-page clean PDF), and rsync transfer pattern from the Friedrich Gundolf / Mantle of Caesar session.

See `references/ocr-page-compilation.md` for the production cleaning function, frequency-analysis snippet, and full script template.
