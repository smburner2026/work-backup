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

### Tier 0.5 — API Fallback (when web search / browser tools fail)

When `web_search`, `web_extract`, and `browser_navigate` all fail (rates exhausted, CAPTCHAs, Chrome unavailable), fall back to direct API calls via `curl`. These are no-auth endpoints that return reliable bibliographic data.

| Source | Endpoint | Best for |
|--------|----------|----------|
| **OpenLibrary Search** | `https://openlibrary.org/search.json?q=<QUERY>` | Title/author search → work key + edition key |
| **OpenLibrary Work** | `https://openlibrary.org/works/{OLkey}.json` | Work-level metadata (subjects, authors, LC class) |
| **OpenLibrary Edition** | `https://openlibrary.org/books/{OLkey}.json` | Edition-level data (ISBN, publisher, pages, pagination, series) |
| **Goodreads** | `https://www.goodreads.com/book/show/{id}` | Kindle price, affiliate purchase links, reviews, embedded `__NEXT_DATA__` JSON |
| **Wikipedia Search** | `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=<QUERY>&format=json` | Book citations, academic bibliography discovery (e.g. finding that a rare book is cited by Wikipedia's Yên Thế Insurrection article) |
| **Wikipedia External Links** | `https://en.wikipedia.org/w/api.php?action=parse&page=<PAGE>&prop=externallinks&format=json` | Extract external links from a Wikipedia page (bibliography references, archive URLs, authority records) |
| **AbeBooks** | `https://www.abebooks.fr/servlet/SearchResults?tn=<TITLE>&an=<AUTHOR>` | Used/rare physical copies for out-of-print books. Parsable via curl (no API key needed). Search per-country domain (.fr, .com, .co.uk) for best results on region-specific books. |

See `references/book-metadata-apis.md` for full endpoint docs and response parsing patterns.
See `references/french-colonial-sources.md` for the specific pattern of acquiring rare French colonial-era books on Indochina (out-of-print, copyright-restricted, used-physical-only).

**Triage rule for in-copyright books:** If `ebook_access` is `"no_ebook"` AND `has_fulltext` is `false` AND the book was published after 1928 (US) or 1970+ (international), the book is under copyright and no free electronic copy exists. In that case, report paid ebook availability (Kindle, Google Play, Kobo, Apple Books — found via Goodreads affiliate links) and used physical copy sources (AbeBooks, Alibris).

### Tier 1b — Direct Sharing / P2P Sources

Always check if the source is already hosted on a personal/community sharing platform before resorting to archives. Common patterns:

| Source | How to access | Pitfall |
|--------|---------------|---------|
| **Google Drive shared folder** | Extract folder ID from URL, use `docs.google.com/uc?export=download&id=<FILEID>` for individual files. File IDs are embedded in the page JavaScript. | Folders may show only a subset of files publicly. The link text says "Trọn bộ" (complete set) but only what's publicly visible is accessible. User may need to mirror the folder. |
| **Personal blogs / WordPress sites** | `web_extract` pages or curl for embedded download buttons | WordPress sites often have ad-heavy layouts. Target the download URL patterns from the button HTML. |
| **Telegram / Discord** | Files shared in channels | Size limits, expiration windows |

### Tier 2 — Shadow Libraries (for out-of-print, restricted, or paywalled sources)

| Source | Best for | Search method |
|--------|----------|---------------|
| **Library Genesis** (libgen.li) | Academic books, textbooks, older publications | ISBN/title search via URL construction (see book-hunting skill) |
| **Anna's Archive** (annas-archive.org) | Broad coverage, mirrors LibGen | MD5 lookup or search |

### Tier 3 — Specialized Archives

| Source | Best for |
|--------|----------|
| **JSTOR** (jstor.org) | Academic journal articles (some free) |
| **Gallica** (gallica.bnf.fr) | French-language historical documents (pre-1935 public domain in France) |
| **Vietnamese-French colonial books** | See `references/french-colonial-sources.md` — pattern for rare French colonial-era biographies that are out-of-print, copyright-restricted, and only available as used physical copies |
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

### From Google Drive (Shared Folder)

```bash
# 1. Get the folder URL from the source page
# 2. Visit the folder URL to scrape file IDs from JavaScript data
#    Look for: file IDs in URL patterns like "id=XXXXXXXXX"
# 3. Download each file:
curl -sL -o output.pdf "https://docs.google.com/uc?export=download&id=<FILE_ID>"

# With confirm token (if it's a large file):
curl -sL -o output.pdf "https://docs.google.com/uc?export=download&confirm=t&id=<FILE_ID>"

# Verify
file output.pdf  # Should show "PDF document"
head -c 5 output.pdf  # Should start with %PDF-
```

**Pitfalls:**
- Google Drive has rate limits — download files sequentially, not in parallel
- Large files (>100MB) may trigger virus scan warning — use `&confirm=t` parameter
- Folder contents may be partially hidden — what's publicly visible may not be the full set
- The folder owner may have download restrictions enabled (usually just prevents direct link sharing, not downloads)

### From Gallica (BnF digital library) — IIIF extraction

When a book is publicly accessible on Gallica but the PDF download is behind an Altcha CAPTCHA, use the IIIF manifest to download individual page images and compile them into a PDF. The IIIF image API is unrestricted even when the PDF download is challenged.

**Prerequisites:** Confirm the book is public domain first (check OAI rights metadata or the Gallica page for "domaine public"). If the book is still under copyright, the IIIF images may still be blocked or watermarked.

**Step-by-step:**

1. **Get the IIIF manifest URL:**
   Find the book's Gallica ARK (e.g. `ark:/12148/bpt6k374553s`). The IIIF manifest is at:
   ```
   https://gallica.bnf.fr/iiif/ark:/12148/<ARK>/manifest.json
   ```
   If the ARK starts with `bpt6k`, it's a digitized item.

2. **Download the manifest:**
   ```bash
   curl -sL "https://gallica.bnf.fr/iiif/ark:/12148/<ARK>/manifest.json" -o manifest.json
   ```

3. **Extract page image URLs from manifest:**
   ```bash
   python3 -c "
   import json
   with open('manifest.json') as f:
       data = json.load(f)
   canvases = data['sequences'][0]['canvases']
   for i, canvas in enumerate(canvases):
       img_service = canvas['images'][0]['resource']['service']['@id']
       print(f'{i+1}|{img_service}/full/full/0/default.jpg|{canvas.get(\"label\", f\"p{i+1}\")}')
   " > page_urls.txt
   ```

4. **Download pages with rate limiting and 429 retry:**
   ```bash
   while IFS='|' read -r num url label; do
     curl -sL -o "page_$(printf '%04d' $num).jpg" "$url"
     sleep 1.0  # mandatory — Gallica 429s at ~55 requests in quick succession
   done < page_urls.txt
   ```

5. **Compile into PDF using img2pdf (lossless, no re-encoding):**
   ```bash
   python3 -c "
   import img2pdf, os, sys
   images = sorted([f for f in os.listdir('.') if f.startswith('page_') and f.endswith('.jpg')])
   with open('output.pdf', 'wb') as f:
       f.write(img2pdf.convert([os.path.join('.', img) for img in images]))
   print(f'PDF created: {len(images)} pages')
   "
   ```

**Rate limiting notes (real-world experience, as of May 2026):**
- Gallica's IIIF server has a **sliding window rate limit** — 429s can cascade. Once you hit 429, even the next request may fail because you're still inside the window. A ~120s cooldown resets it.
- The limit triggers after ~55 sequential requests with 1s delays, OR immediately if a recent session already exhausted your window. On fresh starts after previous failures, **wait 120s before the first request**.
- Use **4-5 second minimum delay** between requests (`--delay 4.0`). Shorter delays trigger cascade 429s.
- Use **lower resolution** to reduce server load: `--res-width 600` or `--res-width 800` (600px JPEGs are ~100KB each, still readable, far fewer 429s).
- Implement aggressive exponential backoff on 429: **180s on first retry**, doubling each attempt (the script defaults to 180s base, 5 retries).
- At 4s per page with 600px width, a 279-page book takes ~20 min. At full res with 12s delays, ~55 min.
- **Script supports `--resume`** — killed processes pick up where they left off. Cached pages are skipped.
- `--delay` defaults to 2.0s in the script. On real Gallica servers, you may need to override to 4.0s+ (`--delay 4.0`) for reliability.
- The **manifest download** can also get 429d — the script now retries the manifest with the same backoff logic.
- Use `img2pdf` over Pillow for compilation: img2pdf does not re-encode JPEGs (lossless, fast), Pillow decodes and re-encodes (lossy, slow).

**Full runnable script:** See `scripts/gallica-iiif-extract.py` in this skill for a fully parameterized downloader with retry logic, resume-from-cache, and progress reporting.
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
- **In-copyright books (post-1970)** — when ebook_access="no_ebook" and has_fulltext=false, no free electronic copy exists anywhere legitimate. Do not spend time trying Archive.org/LibGen/Google Books for a free copy — it's protected by copyright. Instead, report paid ebook options (Kindle, Google Play, Kobo — found via Goodreads API fallback) and used physical copies (AbeBooks, Alibris).
- **French colonial-era books — copyright depends on author death date, not publication date.** Under French law: public domain = author died >70 years ago + WWII extensions for authors who died in 1945 (collaboration executions). Books from the 1930s by authors executed in 1945 (e.g. Paul Chack, Hoang-Tham pirate, 1933) **ARE public domain** in France—check Gallica first. Books from the 1970s by living-then authors (e.g. Pierre Darcourt, Bay Vien, 1977) are NOT. Triage rule:
  - **Author died before 1955** → check Gallica (bnf.fr) via IIIF manifest for digital copy
  - **Author lived past 1955** → no free copy, pivot to paid/used (Goodreads → Kindle/AbeBooks)
- **PDF vs DJVU** — some Internet Archive items are DJVU format, not PDF. Convert with `djvudjvu` or use the text version.
- **No editorializing about historical figures** — never characterize a person's politics, ideology, or views as yours-to-judge. No "troubling," "controversial," "problematic" equivalents. State facts (they lived at these dates, wrote these books, held these roles, took these actions). Let readers draw their own conclusions. This is an iron rule — applies to every figure, every context, always.

## Verification

After completing the pipeline:
1. ✅ Original file downloaded and accessible
2. ✅ Text extraction quality checked (first 3 pages readable)
3. ✅ metadata.json populated with all provenance fields
4. ✅ Source ingested to G-Brain with appropriate tags
5. ✅ User notified of any quality issues or access restrictions

## Kanban Source-Tracking Card Pattern

When acquiring significant sources (rare books, large downloads, multi-volume sets), create a kanban card to track the work. This makes the acquisition visible on the board and survives crashes/restarts.

```bash
hermes kanban create \
  --body "Key metadata: author, year, ISBN, source URL, format details. Current status: what's been done, what's pending." \
  --assignee default \
  --priority 2 \
  "Source: <Title> (<Author>, <Year>)"
```

**When to create a card:**
- Any download that takes >2 minutes (background process)
- Multi-volume or batch acquisitions
- Sources that require downstream processing (OCR, translation, analysis)
- Anything the user should be able to check on later without asking

**What the card body should contain:**
- Full bibliographic metadata (title, author, year, publisher, ISBN, URL)
- Current processing status (downloading, extracting, OCR, complete)
- Known limitations (copyright, quality, missing pages)
- Next steps (pending actions the user may want to take)
