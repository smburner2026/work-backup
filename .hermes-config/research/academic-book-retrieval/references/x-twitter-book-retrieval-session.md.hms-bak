# Session: Book from X/Twitter Post — Roger Griffin's "Modernism and Fascism"

**Date:** 2026-05-27
**Source:** `https://x.com/i/status/2059632889818489205`
**User:** @NaturalRightFan (Sorel's Pistol)
**Book:** *Modernism and Fascism: The Sense of a Beginning under Mussolini and Hitler* — Roger Griffin, Palgrave Macmillan, 2007

## Workflow

### 1. Tweet Extraction

**Preferred: Lightpanda** (fast, no API needed):
```bash
lightpanda fetch https://x.com/i/status/2059632889818489205 --dump markdown --json --wait-ms 8000
```
Returns full tweet text + image URL embedded in the page.

**Also works: vxtwitter API:**
```bash
curl -sL "https://api.vxtwitter.com/i/status/2059632889818489205" | jq '.text'
```

**Tweet content:**
> "Roger Griffin is one of the handful historians brave enough to make the opposite case: generic fascism as a positive phenomenon ("Palingenetic ultranationalism") and, more controversially, a species of modernism. Frogs should put down Evola and read this instead..."

### 2. Image Analysis

The tweet had an attached image of the book cover (`https://pbs.twimg.com/media/HJVIMnOW4AUCl5k.jpg`). Used `vision_analyze` to confirm:
- **Title:** Modernism and Fascism
- **Subtitle:** The Sense of a Beginning under Mussolini and Hitler
- **Author:** Roger Griffin
- **Publisher:** Palgrave Macmillan, 2007

### 3. Library Genesis Search

Searched libgen.li with:
```
https://libgen.li/index.php?req=Modernism+and+Fascism+Griffin&...&curtab=e
```

**Key distinction:** LibGen returns BOTH books and journal articles under the same title search. The edition page shows:
- **Book badge** (`<span class="badge badge-secondary">l</span>`) = full book (487 pp)
- **Article badge** (`<span class="badge badge-secondary">a</span>`) = journal article (9-24 pp)

The correct edition ID was **136504831**:
- Publisher: Palgrave Macmillan (not Johns Hopkins University Press)
- Pages: 487 (not 9-24)
- ISBN: 9781403987839
- File: 3 MB PDF, 487 pp, OCR: Y

### 4. Download

The edition page had download links. The `ads.php?md5=<HASH>` page contained a `get.php` link with a dynamic key:

```bash
curl -sL --connect-timeout 30 --max-time 120 \
  "https://libgen.li/get.php?md5=1454d278375bd6acdb7dcfc7be59cdb6&key=*** \
  -o /tmp/Modernism_and_Fascism.pdf
```

Result: 3,113,330 bytes, valid PDF (%PDF-1.5 header).

### 5. Pitfalls Encountered

- **LibGen returns journal articles alongside books** — always check page count and publisher to distinguish
- **Internet Archive direct downloads require auth** — the PDF returned 401 unless you're logged in with borrowing privileges
- **Pinata IPFS blocks scholarly content** — returned "This content has been blocked"
- **Cloudflare IPFS gateway DNS resolution failed** — unreliable, try libgen.li directly
- **libgen.li download timeouts** — use `--connect-timeout 30 --max-time 120` for slow servers
- **Anna's Archive fast_download returned HTML** — requires browser session/cookies; libgen.li direct download is more reliable via CLI
