---
name: book-hunting
description: "Find and download academic PDFs — textbook workflow for libgen.li ISBN search + direct download."
version: 1.1.0
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

## Title variants

Books translated to English may carry **different titles in US vs UK markets**. The same translation can appear under two completely different names. When ISBN-based search fails, search by:
- Author (primary surname + first initial)
- Original-language title (German, French, etc.)
- UK title if the US title fails and vice versa

**Example**: Paul Herrmann's *The Great Age of Discovery* (Harper, US) was published in the UK as *The World Unveiled: The Story of Exploration from Columbus to Livingstone* (Hamish Hamilton). Same translation, different title, different ISBN.

## Government / Institutional repositories

When shadow libraries are unreachable or the book isn't indexed, government and institutional digital archives are a strong fallback. They host scanned academic books (typically pre-2000s, often from defunct library collections) and serve them as plain PDFs with no cloudflare, no JS, no auth wall.

- **IGNCA (Indira Gandhi National Centre for the Arts)** — `ignca.gov.in/Asi_data/<ID>.pdf`. Browse for books via web search with `site:ignca.gov.in` or direct title search. Direct download, no blocking.
- **HathiTrust** — `babel.hathitrust.org`. May have cloudflare challenges. Check the catalog record — in-copyright books show limited preview, pre-1928 works have full PDF.
- **National libraries and university repositories** — search `site:.gov.in` or `site:.ac.in` for Indian sources; similar patterns exist for other countries (e.g. `site:.bnf.fr`, `site:dbc.wroc.pl`).

**Search pattern**: `"<title>" "<author>" filetype:pdf site:.gov.in OR site:.ac.in`

Verify downloaded PDFs by checking the title page (first 1-3 pages) — institutional scans often have handwritten catalog numbers, stamps, or binding marks.

## Public-domain / Open-access alternative workflow

For public-domain classics (pre-1928), skip libgen entirely — cleaner PDFs are available from open-access sources:

1. **Online Library of Liberty** — born-digital text PDFs, standard scholarly translations. If the page is JS-heavy, brute-force the S3 URL pattern (see `references/public-domain-sources.md`).
2. **Project Gutenberg** — HTML/EPUB/plain text, no PDF. Convert in-browser.
3. **Bill Thayer's LacusCurtius** — minutely proofread classical texts with scholarly apparatus.

**When to use**: User asks for a classic work (Plutarch, Plato, Aristotle, Cicero, etc.) and specifically wants a clean PDF, not a scanned OCR mess. The OLL PDFs are tiny (~1 MB per volume, born-digital text) vs. the scanned behemoths on Archive.org.

**Detail**: `references/public-domain-sources.md`

## Delegation as fallback (VPS-network blocking)

Some VPS/cloud IP ranges are blocked by shadow libraries (libgen, Anna's Archive) or hit aggressive rate limits, returning empty responses. Similarly, Cloudflare JS challenges on HathiTrust and some library sites may be impassable from headless environments.

When direct curl/browser approaches return empty or timeout for 3+ sources in a row:

1. **Use `delegate_task`** — spawn a subagent with `toolsets=['web','terminal','file']`. The subagent uses the Hermes runtime's network stack which may route through a different exit IP.
   - Pass all known identifiers: title, author, ISBNs (US + UK if found), original-language title, publisher, year
   - Ask it to try every mirror systematically
   - Ask it to check government repositories (IGNCA, etc.) if shadow libraries fail
   - Tell it to save the result to a known path and report back
2. Subagents are **NOT guaranteed** to have different routing — but often do when the main agent's VPS has been firewalled.

## Network quirks and mirror fallbacks

- `libgen.rs` may return empty responses from some IP ranges; prefer `libgen.li` for author search.
- `get.php?md5=...` requires a `key` parameter scraped from `ads.php?md5=...` first. A bare `get.php?md5=...` without key returns a short HTML interstitial, not the file.
- Anna's Archive (`annas-archive.org`) is JS-heavy. Both curl and Lightpanda can return empty responses from cloud VPS. Do not retry the same host with multiple fetch methods; record it as `acquisition_blocker` and pivot.
