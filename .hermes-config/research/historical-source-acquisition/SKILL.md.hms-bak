---
name: historical-source-acquisition
description: "Find, verify, download, and extract text from primary/secondary historical sources — archives, libraries, shadow libraries, and digital repositories."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [history, primary-sources, archives, PDF, OCR, research, provenance]
    category: research
    related_skills: [ocr-and-documents, academic-book-retrieval, book-hunting, document-translation]
    requires_toolsets: [web, terminal, file]
---

# Historical Source Acquisition

Find, verify, download, and extract text from primary and secondary historical sources across multiple archives and repositories.

## When to Use

- User asks to find a specific historical document, book, pamphlet, or record
- User mentions an archival source, historical publication, or primary document
- User needs to build a research corpus from historical materials
- User references a source by title, author, date, archive, or catalog number

## Step 1 — Source Identification

Before searching, extract all known metadata from the user's request:

| Field | What to capture |
|-------|----------------|
| Title | Full or partial title |
| Author | Individual, institution, government body |
| Date | Publication year, period, era |
| Language | Original language of the document |
| Type | Book, pamphlet, newspaper, government report, census, manuscript, map, photograph |
| Archive/Repository | Where the original is held (if known) |
| Catalog/Call number | Library of Congress, OCLC, shelf mark |
| Edition | Specific edition if multiple exist |

If the user only gives a vague reference ("a 19th century Vietnamese census"), ask for more specifics before proceeding. A vague search wastes tokens.

## Step 2 — Search Strategy (by priority)

### Tier 1 — Open Access (always try first)

| Source | Best for | Search method |
|--------|----------|---------------|
| **Internet Archive** (archive.org) | Books, government docs, newspapers, manuscripts | `web_search` + `web_extract` on identifier pages |
| **Google Books** (books.google.com) | Published books, especially pre-1900 | `web_search` with `site:books.google.com` |
| **HathiTrust** (hathitrust.org) | Academic library collections | `web_search` with `site:hathitrust.org` |
| **Project Gutenberg** (gutenberg.org) | Public domain texts | Direct search API or `web_search` |
| **WorldCat** (worldcat.org) | Find which libraries hold a copy | `web_search` for catalog records |

### Tier 2 — Shadow Libraries (for out-of-print, restricted, or paywalled sources)

| Source | Best for | Search method |
|--------|----------|---------------|
| **Library Genesis** (libgen.li) | Academic books, textbooks, older publications | ISBN/title search via URL construction (see book-hunting skill) |
| **Anna's Archive** (annas-archive.org) | Broad coverage, mirrors LibGen | MD5 lookup or search |

### Tier 3 — Specialized Archives

| Source | Best for |
|--------|----------|
| **JSTOR** (jstor.org) | Academic journal articles (some free) |
| **Gallica** (gallica.bnf.fr) | French-language historical documents |
| **Google Books Ngram** | Finding which books contain specific terms |
| **National Archives** (archives.gov) | US government records |
| **Repository-specific** | Ask user for institution-specific digital archives |

## Step 3 — Verification

Before downloading, verify it's the right document:

1. **Title match** — exact or close enough
2. **Author match** — individual or institutional
3. **Date match** — publication year, not scan year
4. **Page count** — full monograph (200+ pages) vs article (< 50 pages) vs pamphlet (10-50 pages)
5. **Language** — original language, not a translation (unless that's what's wanted)
6. **Edition** — correct edition/reprint
7. **OCR availability** — does the scan have text layer?

**Red flags:**
- Page count < 10 — likely a journal article, not a book
- Title matches but date is wildly wrong — different edition
- Language mismatch — may be a translation

## Step 4 — Download

### From Internet Archive
```bash
# Find the identifier from the URL (e.g., /details/somebook1923)
curl -sL "https://archive.org/download/<IDENTIFIER>/<IDENTIFIER>.pdf" -o output.pdf
# Or for text version:
curl -sL "https://archive.org/download/<IDENTIFIER>/<IDENTIFIER>_djvu.txt" -o output.txt
```

### From Google Books
- Full preview: use `web_extract` on the book URL
- Snippet view only: note this to user, suggest archive.org or LibGen for full text

### From LibGen
Use the `academic-book-retrieval` or `book-hunting` skill workflow:
- Search by ISBN or title
- Verify edition details on the edition page
- Download via the `get.php` link

### From HathiTrust
- Public domain works: direct download via the "Download" button (requires login for some)
- In-copyright: limited to search/snippet — note this to user

### General Download Pattern
```bash
# With timeout and retry
curl -sL --connect-timeout 30 --max-time 300 \
  --retry 3 --retry-delay 5 \
  "<URL>" -o "<output_path>"

# Verify download
file <output_path>  # Check it's actually a PDF
ls -lh <output_path>  # Check size is reasonable
head -c 5 <output_path>  # Should start with %PDF- for PDFs
```

## Step 5 — Text Extraction

Use the `ocr-and-documents` skill for extraction. Choose method based on document type:

| Document type | Method |
|---------------|--------|
| Text-based PDF (post-1990) | `pymupdf` — instant, no models needed |
| Scanned PDF (pre-1990, image-only) | `marker-pdf` — OCR with layout detection |
| Fraktur/Gothic German text | `pymupdf` + fraktur cleaning pipeline |
| Handwritten manuscript | `vision_analyze` — VLM page-by-page transcription |
| Newspaper/multi-column | `marker-pdf` — handles column layout |

```bash
# Quick check: does the PDF have embedded text?
python3 -c "
import pymupdf
doc = pymupdf.open('source.pdf')
sample = doc[0].get_text()
if len(sample.strip()) > 100:
    print('TEXT-BASED: use pymupdf')
else:
    print('IMAGE-ONLY: use marker-pdf or vision_analyze')
"
```

### Output structure
```
research/sources/
├── <source-slug>/
│   ├── original.pdf           # Downloaded file
│   ├── extracted.txt          # Full text extraction
│   ├── metadata.json          # Provenance: URL, date downloaded, archive, catalog info
│   └── pages/                 # Optional: per-page text files
│       ├── page_001.txt
│       └── ...
```

### metadata.json format
```json
{
  "title": "...",
  "author": "...",
  "date": "...",
  "language": "...",
  "type": "book|pamphlet|report|census|manuscript|...",
  "archive": "internet-archive|hathi-trust|libgen|google-books|...",
  "archive_url": "...",
  "archive_identifier": "...",
  "downloaded_at": "2026-05-29T...",
  "file_size_bytes": 1234567,
  "page_count": 350,
  "ocr_method": "pymupdf|marker-pdf|vision-analyze",
  "extraction_quality": "high|medium|low",
  "catalog_numbers": {
    "lccn": "...",
    "oclc": "...",
    "isbn": "..."
  },
  "notes": "..."
}
```

## Step 6 — Ingestion to Knowledge Base

After extraction, ingest to G-Brain:

```python
# For each source:
mcp_gbrain_put_page(
    slug=f"historical-sources/<source-slug>",
    content="<extracted text or summary>",
    source_kind="put_page"
)
mcp_gbrain_add_tag(slug=f"historical-sources/<source-slug>", tag="primary-source")
mcp_gbrain_add_tag(slug=f"historical-sources/<source-slug>", tag="<era>")
mcp_gbrain_add_tag(slug=f"historical-sources/<source-slug>", tag="<language>")
mcp_gbrain_add_tag(slug=f"historical-sources/<source-slug>", tag="<region>")
```

## Pitfalls

- **Google Books snippet view** — only shows fragments, not full text. Don't waste tokens trying to piece together a book from snippets.
- **Internet Archive borrow-only** — many in-copyright books are "lending library" only (1-hour loans). Check if the item has open/download access before attempting download.
- **LibGen timeouts** — the `get.php` link uses dynamic keys that expire. Scrape fresh each time.
- **OCR quality varies wildly** — pre-1900 printing, Fraktur type, faded ink, and handwritten marginalia all degrade OCR. Always spot-check the first few pages.
- **Duplicate editions** — the same book may appear under multiple editions/years. Verify you have the right one.
- **Copyright status** — pre-1928 US publications are public domain. Post-1928 varies. International sources vary by country. Note the copyright status in metadata.
- **PDF vs DJVU** — some Internet Archive items are DJVU format, not PDF. Convert with `djvudjvu` or use the text version.

## Verification

After completing the pipeline:
1. ✅ Original file downloaded and accessible
2. ✅ Text extraction quality checked (first 3 pages readable)
3. ✅ metadata.json populated with all provenance fields
4. ✅ Source ingested to G-Brain with appropriate tags
5. ✅ User notified of any quality issues or access restrictions
