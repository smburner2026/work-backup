---
name: academic-book-retrieval
description: "Find and download academic books from online sources — identify books mentioned in social media, citations, or references, then locate and retrieve full-text PDFs from shadow libraries (Library Genesis, Anna's Archive, Internet Archive) and alternative mirrors (IPFS, direct download)."
version: 1.0.0
author: Hermes Agent
tags: [libgen, annas-archive, internet-archive, academic, books, pdf, ipfs, research, twitter, x-twitter]
trigger: |
  User asks to find/download/retrieve a specific academic book:
  - "Find the book in this tweet/X post"
  - "Get me [book title] by [author]"
  - "Download this paper/book"
  - "Find [topic] textbook/PDF"
  - Any request to locate and retrieve a scholarly monograph or textbook
---

# Academic Book Retrieval

## Workflow Overview

### 1. Identify the Book

When the source is a **social media post** (X/Twitter, Bluesky, etc.):

- **Preferred: Lightpanda** — `lightpanda fetch <url> --dump markdown --wait-ms 8000`
  - Fast, no API keys, no Chrome needed
  - Works for public X posts (renders JS)
- **Fallback: vxtwitter API** — `curl -s https://api.vxtwitter.com/i/status/POST_ID`
  - Returns JSON with tweet text, media URLs, user info
- **Fallback: fxtwitter proxy** — `curl -s https://api.fxtwitter.com/status/POST_ID | jq '.tweet.text'`
- **Verify visual content**: If the tweet has a book cover image, analyze it with `vision_analyze` to confirm title/author/edition.

Extract: title, author, edition, ISBN (if visible), publisher, year.

### 2. Primary Search — Library Genesis

**Search by title + author:**
```
https://libgen.li/index.php?req=<TITLE>+<AUTHOR>&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=i&topics%5B%5D=v&topics%5B%5D=g&topics%5B%5D=d&res=25&phrase=1&curtab=e
```

**Search by ISBN:**
```
https://libgen.li/index.php?req=<ISBN>&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=i&topics%5B%5D=v&topics%5B%5D=g&topics%5B%5D=d&res=25&phrase=1&curtab=e
```

**IMPORTANT — distinguish full books from journal articles:**
- Full books have 200+ pages and are marked with `<span class="badge badge-secondary">l</span>` (Book badge)
- Journal articles have < 50 pages and are marked with `<span class="badge badge-secondary">a</span>` (Article badge)
- Check the "Pages:" field in the edition details — 400+ = full book, < 50 = journal article

### 3. Edition Details Page

Once you find the right edition, open the edition page:
```
https://libgen.li/edition.php?id=<EDITION_ID>
```

Key fields to verify:
- **Title**: Exact match
- **Author(s)**: Roger Griffin (not just "Griffin")
- **Publisher**: Palgrave Macmillan (or expected publisher)
- **Year**: 2007 (or expected year)
- **Pages**: 487 (full book, not 9-24 which is a journal article)
- **ISBN**: 9781403987839 or similar
- **File info**: Size (e.g. 3 MB), Extension (pdf), Pages (487), OCR (Y)

### 4. Download

From the edition page, extract the download link from the `ads.php` URL:

```
https://libgen.li/ads.php?md5=<MD5_HASH>
```

This page contains a `get.php` link with a dynamic key:
```
get.php?md5=<MD5>&key=<DYNAMIC_KEY>
```

Download using the full URL:
```bash
curl -sL --connect-timeout 30 --max-time 120 \
  "https://libgen.li/get.php?md5=<MD5>&key=<KEY>" \
  -o /path/to/output.pdf
```

#### Alternative Mirrors (on edition page)

IPFS gateways:
- `https://cloudflare-ipfs.com/ipfs/<CID>?filename=<FILENAME>.pdf` — may be unreliable
- `https://gateway.ipfs.io/ipfs/<CID>?filename=<FILENAME>.pdf` — slow but reliable
- `https://gateway.pinata.cloud/ipfs/<CID>?filename=<FILENAME>.pdf` — may block some content

Anna's Archive:
- `https://annas-archive.gl/md5/<MD5>` — requires JS for download, fast_download may need session cookies
- Preferred alternative when libgen.li is slow

### 5. Verification

- Check file starts with `%PDF-1.x` (valid PDF header)
- Check file size matches expected (e.g. 3 MB for a 487-page scanned book)
- For access-restricted files (401 response), try alternative mirrors or check Internet Archive

### 6. Internet Archive (fallback)

```
https://archive.org/details/<IDENTIFIER>
```

- Books are often borrow-only (access-restricted, 401 on direct download)
- Check if the item has open-culture or public-domain status
- Files marked `private="true"` in `files.xml` are access-restricted
- Not suitable for download unless explicitly open-access

---

## Session-Specific References

See `references/` for detailed session transcripts and edge cases.

