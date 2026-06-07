# Government & Institutional Archive Sources

## IGNCA — Indira Gandhi National Centre for the Arts

**Base URL**: https://ignca.gov.in/Asi_data/<ID>.pdf

IGNCA hosts scanned books from the Archaeological Survey of India library and other defunct Indian institutional collections. These are typically pre-2000 academic books, scanned as image-based PDFs.

**How to find books on IGNCA**:
- Search: `site:ignca.gov.in <book title>`
- Search: `site:ignca.gov.in <author name>`
- The PDF IDs (e.g. `38191.pdf`, `11113.pdf`) are opaque numeric identifiers. You cannot browse sequentially.

**Characteristics**:
- Direct HTTP download — no JS, no auth, no cloudflare
- PDF size: 2-30 MB typical, scanned@300dpi
- Contains library stamps, handwritten catalog numbers, binding marks
- No OCR text layer (image-based)
- No download rate limits observed

**Common pitfalls**:
- The title page may list the UK edition title even when searching for the US title (same translation, different publisher)
- Catalog metadata (pdfinfo) is usually empty — verify content by reading the title page
- Some PDFs have corrupted page ordering; check first and last pages

## HathiTrust

**Base URL**: https://babel.hathitrust.org/cgi/pt?id=<id>

**Access model**:
- Pre-1928 works: full PDF download available
- 1928+ works: limited preview only (in-copyright). Shown as "Limited (search-only)" in the catalog
- May present Cloudflare JS challenges — not reliably accessible from curl or headless browsers

**How to use**:
- Search on HathiTrust directly, or via Google with `site:hathitrust.org "title"`
- For in-copyright books, it may still help verify bibliographic details even if full-text is blocked

## Other national & university repositories

Common patterns:
- `site:.gov.in` + filetype:pdf — Indian government archives
- `site:.ac.in` + filetype:pdf — Indian academic repositories
- `site:bnf.fr` + filetype:pdf — Bibliothèque nationale de France (Gallica)
- `site:dbc.wroc.pl` — Polish digital library collections
- `site:archive.org` — Internet Archive (limited for in-copyright, full for pre-1928)

**Search strategy**:
```
"<exact title>" "<author surname>" filetype:pdf site:.gov.in OR site:.ac.in
```

Use broad title terms (drop subtitles) for better coverage.
