---
name: book-hunting
description: "Find and download academic PDFs — textbook workflow for libgen.li ISBN search + direct download."
version: 1.0.0
author: Hermes Agent
tags: [libgen, pdf, books, research, isbn, public-domain, oll]
---

# Book Hunting

## Primary workflow (libgen.li)

1. Search by ISBN on libgen.li:
   ```
   https://libgen.li/index.php?req=<ISBN>&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=i&topics%5B%5D=v&topics%5B%5D=g&topics%5B%5D=d&res=25&phrase=1
   ```

2. Find the edition with the full book (not just a journal article). Check:
   - Pages ~400-500 for a monograph
   - Extension: pdf
   - Size: 2-15 MB typical

3. Get the edition ID (e.g. `edition.php?id=136504831`), scrape the `get.php?md5=...&key=...` URL from the ads page:
   ```
   curl -sL "https://libgen.li/ads.php?md5=<MD5>" | grep -oP 'get\.php\?md5=[^"]+'
   ```

4. Download using the extracted URL:
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

## Pitfalls
- libgen.li may timeout on first attempt; retry with longer timeout
- The `key` parameter in get.php is dynamically generated — must scrape fresh each time
- Some editions on libgen are journal articles, not the full book — verify page count
- Always verify downloaded file: check for `%PDF` header and reasonable size
- **Tool selection**: use Lightpanda for the source URL (X/Twitter post), curl for the actual download. Don't use Lightpanda for libgen/archive downloads.
- **Reference:** `references/efficient-workflow.md` — optimized turn-by-turn sequence from the 2026-05-27 session.
