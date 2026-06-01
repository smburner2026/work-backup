# Project Gutenberg Download Workflow

Clean EPUBs for public-domain texts, searchable by author/title, no auth needed.

## When to Use

- The user requests a specific public-domain book (pre-1928 US, author died >70yrs in most countries)
- Any 18th–19th century classic, historical text, memoir, letters, or autobiography
- User wants EPUB for e-reader (Kindle, Kobo, phone) — Gutenberg EPUBs are natively compatible

Do NOT use Gutenberg for:
- Academic monographs published after 1928 (try LibGen or Internet Archive)
- PDFs specifically requested (Gutenberg has no native PDF — only HTML/EPUB/kinds/text)
- In-copyright books (check publication year + author death date first)

## Step 1 — Search Gutenberg Catalog

### Option A: Web search (preferred when available)

```
https://www.gutenberg.org/ebooks/search/?query=<TITLE>+<AUTHOR>
```

Extracts ebook IDs from the result page. Each result row has a link like `/ebooks/53967`.

### Option B: API search (when web_search/browser fail)

```
https://www.gutenberg.org/ebooks/search/?query=<TITLE>+<AUTHOR>&format=json
```

Or use the direct API:
```
curl -sL "https://www.gutenberg.org/ebooks/search/?query=<TITLE>+<AUTHOR>" | grep -oP '/ebooks/\d+'
```

Gutenberg's search is tolerant — partial titles and author last names work.

## Step 2 — Identify the Right Edition

Multiple editions of the same work may exist. Check:
- **Title** — exact or close enough
- **Author** — correct person
- **Language** — original language vs translation
- **Type** — book, not a magazine article or compilation

Multi-volume works appear as separate entries. Check the subtitle field: "(Vol. I)", "(Vol. II)", etc.

## Step 3 — Download EPUB

Construct the download URL from the ebook ID:

```
https://www.gutenberg.org/ebooks/<ID>.epub.noimages
```

The `.epub.noimages` variant produces a text-only EPUB (smaller, faster, better for e-readers). Images-only `.epub.images` is available but rarely needed for books.

```bash
curl -sL -o "<output-filename>.epub" \
  "https://www.gutenberg.org/ebooks/<ID>.epub.noimages"
```

The server returns HTTP 200 + the file content. Typical size: 300KB–1.5MB for a full book.

## Step 4 — Verify

```bash
file <output>.epub       # Should show: EPUB document
ls -lh <output>.epub      # Reasonable size (>100KB)
```

EPUB is a ZIP container — you can verify structural integrity:
```bash
unzip -t <output>.epub 2>/dev/null | tail -1
```

## Step 5 — Deliver to User

For Telegram delivery, send the file via MEDIA: reference:

```
MEDIA:/path/to/<output>.epub
```

For multi-volume works, either zip them or send individually. A single sending pattern:

```
MEDIA:/path/to/all-volumes.tgz

Description including titles and volumes.
```

Gutenberg URLs also work as persistent links:
```
gutenberg.org/ebooks/<ID>
```

## Multi-Volume Handling

When a work spans multiple volumes, each has a separate Gutenberg ID:

```
Vol I:  gutenberg.org/ebooks/53967 → https://www.gutenberg.org/ebooks/53967.epub.noimages
Vol II: gutenberg.org/ebooks/53968 → https://www.gutenberg.org/ebooks/53968.epub.noimages
```

**Delivery options:**
1. **Individual EPUBs** — send each separately (cleanest for e-reader side-loading)
2. **Single archive** — tar.gz all volumes (convenient for batch transfer):
   ```bash
   tar -czf <work>-all.tgz <work>-vol*.epub
   ```

## Known Works on Gutenberg

| Work | Author | Volumes | IDs |
|------|--------|---------|-----|
| Memorial of St. Helena | Las Cases (recording Napoleon) | 4 vols | 53967, 53968, 53969, 53970 |
| (Add more as discovered) | | | |

## Pitfalls

- **Gutenberg has no PDF** — if the user explicitly wants PDF, check Archive.org or Google Books instead
- **Some books have multiple editions** — make sure you get the translation/edition the user wants (e.g. English vs original language)
- **.epub.noimages vs .epub.images** — always prefer `.noimages` for books; images bloat the file unnecessarily
- **Volumes are separate entries** — don't assume a multi-volume work is bundled. Search each volume's subtitle
- **Single-book limitation** — Gutenberg works best for one book at a time. Don't try to download a whole corpus in parallel
- **Rate limiting** — moderate; sequential downloads with 1-2s gap are fine, but don't hammer the server with 20 parallel requests
- **No search by ISBN** — Gutenberg's catalog uses author+title. If you only have an ISBN, resolve it to a title first via OpenLibrary API
- **Plain text also available** — for text-only processing (OCR bypass for born-digital texts), use:
  ```
  https://www.gutenberg.org/cache/epub/<ID>/pg<ID>.txt
  ```
  This is useful when you need to search/analyze text without EPUB parsing
