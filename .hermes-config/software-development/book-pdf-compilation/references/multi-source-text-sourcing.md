# Multi-Source Text Sourcing for Anthology & Complete Works

For projects where source texts come from multiple channels — public domain, shadow libraries, and OCR scans — use this pattern to identify, acquire, and organize the materials before compilation.

## Phase 0: Identify the Right Translation

Before downloading anything, establish the translator-per-work map:

1. **Check user's translation preferences** from memory/profile (e.g. Johnston for doctrinal Nietzsche, Hollingdale for bite, Parkes for Zarathustra, Del Caro for Gay Science)
2. **Determine which translators did which works** — a single translator like Johnston may have only done 4 works, not the complete corpus
3. **For each missing work**, identify the best-available translator given the user's preference hierarchy
4. **Confirm scope with the user** before proceeding — some works are optional (e.g. *The Will to Power*)

Keep a running table:

| Work | Translator | Source Type | Status |
|------|-----------|-------------|--------|
| Birth of Tragedy | Ian Johnston | Public domain (online) | ✅ On disk |
| Twilight of the Idols | R.J. Hollingdale | Copyrighted (Cambridge/Penguin) | ✅ Sourced |
| Human, All Too Human | R.J. Hollingdale | Copyrighted (Cambridge/Penguin) | ❌ Need |

## Phase 1: Public Domain Sources

Start with free, legally clear sources for works in public domain translations:

### Ian Johnston (johnstoniatexts.x10host.com)
- Full texts available in HTML with per-part pages
- Structure: `<workname>tofc.html` for TOC, `beyondgoodandevil{N}html.html` for individual parts
- Download all parts, strip HTML, concatenate into a single clean `.txt` file
- Johnston covers: BGE, Genealogy, Birth of Tragedy, Use & Abuse of History

### Project Gutenberg (gutenberg.org)
- Search by translator name (Ludovici, Collins, Zimmern, Common)
- Raw text files available at `https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt`
- Useful for: Ludovici's Case of Wagner / Nietzsche Contra Wagner, Collins' Schopenhauer as Educator, Zimmern's Human All Too Human (Part I only)

### Internet Archive (archive.org)
- Search by title + translator
- Often has full-text PDF of out-of-print editions
- Can extract text via OCR

## Phase 2: Copyrighted / Print-Only Sources

When the best translation is only available in a print edition (Cambridge, Stanford, Oxford, Penguin):

### Anna's Archive (annas-archive.org)
- Search by ISBN for precision
- Search query: `"Twilight of the Idols" "R.J. Hollingdale"` or `Title + Translator`
- Preferred format: EPUB (best text extraction) > PDF (OCR needed if scanned)
- Download to `sources/` with a descriptive filename

### Library Genesis (libgen.is, libgen.li)
- Search by ISBN or title+author
- API via `https://libgen.is/search.php?req={query}`
- Returns MD5 hashes for direct download
- Better for academic editions than Penguin paperbacks

### Fallback: OCR from Scanned PDF
If only a scanned PDF is available:
- Extract text with `pdftotext` or `pdfminer`
- Clean aggressively (header removal, hyphenation repair, line-break joining)
- See `references/ocr-page-compilation.md` for the full OCR cleaning workflow

## Phase 3: Organization Convention

```
project-root/
├── sources/                    # All source texts
│   ├── bge_johnston_full.txt   # Public domain
│   ├── twilight_hollingdale.txt # From Anna's Archive
│   ├── parkes_zarathustra_full.txt
│   ├── gay_science_delcaro.txt
│   └── ...
├── anthology.md                # Compiled markdown (for anthology)
├── build_anthology.py          # Compilation script
└── anthology.pdf               # Output
```

- **Source file naming**: `{work}_{translator}_{source}.{ext}` — e.g. `bge_johnston_full.txt`, `twilight_antichrist_hollingdale.txt`
- **Each source file** should be the FULL text of the work, not excerpts — excerpting happens at the markdown compilation stage
- **Version the markdown source**, not the PDF — the build script is the pipeline

## Phase 3.5: Parallel Background Sourcing (Cron Pattern)

For projects with 5+ texts to acquire, fire **background cron jobs** instead of blocking on sequential delegate_task calls. This lets the user keep working while sourcing runs in parallel.

### Why Cron Instead of delegate_task

- `delegate_task` runs inside the current turn — user messages interrupt children, killing downloads
- `cronjob(action='create', schedule='1m', repeat=1, enabled_toolsets=['web','terminal','file'])` launches a fresh agent session that runs independently
- Multiple cron jobs fire in parallel (they're independent scheduler events)
- Each cron job delivers its report back to `origin` (the current conversation) when done
- The user is never blocked — they continue their conversation while sourcing happens

### Parallel Text Extraction (delegate_task)

After sourcing, extract text from the acquired files using `delegate_task` with parallel tasks. Split by logical groups:

```python
delegate_task(tasks=[
    {goal: "Extract from PDFs Group A (3 works)", context: "Use PyMuPDF for PDF, zipfile+BeautifulSoup for EPUB", toolsets: ["terminal","file"]},
    {goal: "Extract from PDFs Group B (3 works)", context: "Same methods", toolsets: ["terminal","file"]},
])
```

Heuristic: group by source format — EPUB-extractable works together, PDF-only works together. EPUB extraction is cleaner and faster.

### Batching Strategy

Given the 3-concurrent limit on delegate_task, group works logically:

**Batch 1:** Works from same translator/publisher (e.g. all 3 Hollingdale Cambridge texts)
**Batch 2:** Multi-work volume (e.g. Stanford vol.9) + first chunk of multi-volume set (e.g. Nachlass vols 11-13)
**Batch 3:** Remaining volumes

Grouping heuristic: same translator + same publisher = one cron job. Multiple volumes of the same series = one cron job per 2-3 volumes.

### Cron Job Prompt Structure

```
cronjob(action='create',
    name='Descriptive name',
    prompt='''Search Anna's Archive and Library Genesis for:
    [Work Title] (tr. [Translator], [Publisher], [Year]) — ISBN [number]
    Search by ISBN, exact title, and translator name.
    Try at least 3 mirrors per item. Preferred format: EPUB > PDF.
    Save to /path/to/project/sources/
    Report exactly what was found and what wasn't.''',
    schedule='1m',           # Fire in 1 minute
    repeat=1,                # Run once
    deliver='origin',        # Report back here
    enabled_toolsets=['web', 'terminal', 'file'])
```

### Organisation After Cron Jobs Complete

When all batches report back:
1. Check source directory for new files
2. Move any files saved to wrong directories
3. Deduplicate exact duplicates (same byte count)
4. Strip superseded files (chapter HTML superseded by combined TXT)
5. Report the delta to the user

See `references/weasyprint-workflow.md` for the next step (per-work PDF building with WeasyPrint).

## Phase 4: Translation Verification

After downloading, verify you got the right translation:

1. **Check the translator's name** in the file header/footer — Hoffmann, Common, and Levy all have Victorian-era translations that differ radically from modern ones
2. **Spot-check 3 passages** known from the user's corpus:
   - BGE §257 opening: "Every enhancement in the type 'man'" (Johnston) vs "Every elevation of the type 'man'" (Kaufmann)
   - Zarathustra Prologue: "Overman" (Parkes) vs "Overhuman" (Del Caro) vs "Superman" (Common)
   - Antichrist §57: "Imperium Romanum" (Hollingdale) vs "the Roman Empire" (Kaufmann)
3. **If the file is an EPUB**, extract text with `python3 -c "import zipfile; z=zipfile.ZipFile(f); html=z.read(z.namelist()[0])"` and parse HTML
4. **If the file is a scanned PDF**, verify OCR quality on 3 pages before committing

## Phase 5: Pre-Compilation Pipeline

Once all texts are sourced:

1. Create the master markdown file (anthology.md or complete-works.md)
2. Identify sections/chapters and create the table of contents
3. Write the introduction framing the selection
4. Build the compilation script (fpdf2)
5. Run and verify

See `book-pdf-compilation` SKILL.md for the full compilation workflow — this reference covers only the sourcing layer.
