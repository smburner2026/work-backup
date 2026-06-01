---
name: book-hunting
description: "Find and download academic PDFs — textbook workflow for libgen.li ISBN search + direct download."
version: 1.0.0
author: Hermes Agent
tags: [libgen, pdf, books, research, isbn, public-domain, oll]
---

# Book Hunting

## When to Use

User asks to find/download/retrieve a specific academic book, or any request to locate and retrieve a scholarly monograph or textbook.

## Source Identification

When the source is a **social media post** (X/Twitter, Bluesky, etc.):

- **Preferred: Lightpanda** — `lightpanda fetch <url> --dump markdown --wait-ms 8000`
  - Fast, no API keys, no Chrome needed
  - Works for public X posts (renders JS)
- **Fallback: vxtwitter API** — `curl -s https://api.vxtwitter.com/i/status/POST_ID`
  - Returns JSON with tweet text, media URLs, user info
- **Fallback: fxtwitter proxy** — `curl -s https://api.fxtwitter.com/status/POST_ID | jq '.tweet.text'`
- **Verify visual content**: If the post has a book cover image, analyze it with `vision_analyze` to confirm title/author/edition.

Extract: title, author, edition, ISBN (if visible), publisher, year.

## Primary workflow (libgen.li)

1. Search by ISBN on libgen.li:
   ```
   https://libgen.li/index.php?req=<ISBN>&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=i&topics%5B%5D=v&topics%5B%5D=g&topics%5B%5D=d&res=25&phrase=1
   ```

2. Find the edition with the full book (not just a journal article). Check:
   - Pages ~400-500 for a monograph
   - Extension: pdf
   - Size: 2-15 MB typical
   - **Book badge** (`l` badge) = full book; **Article badge** (`a` badge) = journal article

3. Open the edition details page (`edition.php?id=...`) and verify:
   - Title, author(s), publisher, year, ISBN all match expected
   - Page count confirms it's a full book (200+ pages)

4. Get the edition ID (e.g. `edition.php?id=136504831`), scrape the `get.php?md5=...&key=...` URL from the ads page:
   ```
   curl -sL "https://libgen.li/ads.php?md5=<MD5>" | grep -oP 'get\.php\?md5=[^"]+'
   ```

5. Download using the extracted URL:
   ```
   curl -sL "https://libgen.li/get.php?md5=<MD5>&key=<KEY>" -o <output.pdf>
   ```

## What to skip
- **IPFS gateways** (cloudflare-ipfs.com, gateway.pinata.cloud) — unreliable, blocked, or content-redacted
- **Anna's Archive fast_download** — requires JS session, not curl-friendly
- **Internet Archive direct PDF** — access-restricted (401) for in-copyright books

## Lightpanda usage
- **X/Twitter posts**: `lightpanda fetch <url> --dump markdown --wait-ms 8000` — works where curl/browser fail
- **NOT for**: libgen, Anna's Archive, or shadow library downloads — curl is faster and more reliable

## Public-domain / Open-access alternative workflow

For public-domain classics (pre-1928), skip libgen entirely — cleaner PDFs are available from open-access sources:

1. **Online Library of Liberty** — born-digital text PDFs, standard scholarly translations. If the page is JS-heavy, brute-force the S3 URL pattern (see `references/public-domain-sources.md`).
2. **Project Gutenberg** — HTML/EPUB/plain text, no PDF. Convert in-browser.
3. **Bill Thayer's LacusCurtius** — minutely proofread classical texts with scholarly apparatus.

**When to use**: User asks for a classic work (Plutarch, Plato, Aristotle, Cicero, etc.) and specifically wants a clean PDF, not a scanned OCR mess. The OLL PDFs are tiny (~1 MB per volume, born-digital text) vs. the scanned behemoths on Archive.org.

**Detail**: `references/public-domain-sources.md`

## Network quirks and mirror fallbacks

- `libgen.rs` may return empty responses from some IP ranges; prefer `libgen.li` for author search.
- `get.php?md5=...` requires a `key` parameter scraped from `ads.php?md5=...` first. A bare `get.php?md5=...` without key returns a short HTML interstitial, not the file.
- Anna's Archive (`annas-archive.org`) is JS-heavy. Both curl and Lightpanda can return empty responses from cloud VPS. Do not retry the same host with multiple fetch methods; record it as `acquisition_blocker` and pivot.
