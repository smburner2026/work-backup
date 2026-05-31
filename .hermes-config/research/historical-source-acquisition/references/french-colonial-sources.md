# French Colonial-Era Source Acquisition

Pattern for rare French-language books on colonial Indochina (1920s–1970s). These are typically out-of-print biographies of Vietnamese historical figures written by French colonial officers, journalists, or naval personnel.

## Common publishers & imprints

| Publisher | Active period | Characteristics |
|-----------|--------------|-----------------|
| Hachette | 1826–present | General trade, series like *Les Grands aventuriers* (e.g. Darcourt's *Bay Vien*) |
| Les Éditions de France | 1920s–1940s | Colonial adventure biographies (e.g. Chack's *Hoang-Tham, pirate*) |
| Éditions du Scorpion | 1946–1970s | Pulp biographies, veteran memoirs |
| Plon | 1852–present | Broader trade, some colonial works |
| Berger-Levrault | 1876–present | Military and colonial publications |

## What to expect (copyright & availability)

- **Pre-1945, author died before 1955:** Public domain in France (70 years pma). Check Gallica FIRST — may be fully digitized and rights-free.
  - French WWII extensions (+8 years for 1939-1945) apply to authors who died during the war, but the 70-year pma period has now elapsed for authors who died in or before 1945.
  - Example: Paul Chack (executed 1945) — his 1933 work *Hoang-Tham, pirate* IS in the public domain and available freely on Gallica.
- **Author died 1946–1955:** Entering / entered public domain gradually through 2016–2025.
- **Post-1955 author death:** Still under copyright in France. No free digital copy exists.
- **Digital copies:** Variable by date. Pre-1945 works where author died early → Gallica has them. Post-1945 → virtually none. These are niche colonial interest books that were never digitized commercially.
- **Used physical copies:** Available on AbeBooks, Amazon.fr marketplace, eBay.fr typically for €10–50.
- **Modern reprints:** Some works have been reprinted by Éditions Édilys (e.g. *Le sanglier du Yen Thé ou Hoang Tham, pirate*, ISBN 979-10-94912-38-6, 17€). Check BnF SRU for DL (Dépôt Légal) dates — a post-2000 DL date usually indicates a modern reprint.

## Search strategy

### Step 1 — Metadata discovery (when web_search is down)

```bash
# OpenLibrary — search by title and author
curl -sL "https://openlibrary.org/search.json?q=%22<QUOTED+TITLE>%22+<AUTHOR>"

# Key triage: check ebook_access, has_fulltext, public_scan_b
# If all three say no_ebook/false — no free digital copy exists anywhere
```

```bash
# Goodreads — get purchase links and Kindle info
# First get the Goodreads ID from OpenLibrary edition.json:
curl -sL "https://openlibrary.org/books/<OLkey>.json" | grep -o '"goodreads":[^]]*'

# Then scrape Goodreads for embedded __NEXT_DATA__
curl -sL "https://www.goodreads.com/book/show/<goodreads_id>"
# Extract the next data blob and look for:
# - .primaryAffiliateLink.ebookPrice (Kindle pricing)
# - .secondaryAffiliateLinks (AbeBooks, Alibris, etc.)
```

```bash
# Wikipedia API — check if the book is cited in related articles
curl -sL "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=%22<TITLE>%22&format=json"
curl -sL "https://en.wikipedia.org/w/api.php?action=parse&page=<RELEVANT_PAGE>&prop=externallinks&format=json"
```

### Step 2 — Used copy search (AbeBooks)

```bash
# Search by title + author on AbeBooks France (best for French colonial books)
curl -sL "https://www.abebooks.fr/servlet/SearchResults?tn=<TITLE>&an=<AUTHOR>"
# Parse for: item-price (EUR) and item-detail (condition)

# Also try AbeBooks .com for US/international sellers
curl -sL "https://www.abebooks.com/servlet/SearchResults?tn=<TITLE>&an=<AUTHOR>"
```

### Step 3 — Verify the book is what the user needs

For these rare French colonial books, once you confirm:
1. ✅ Correct title and author
2. ✅ Correct subject (e.g. Vietnam/French Indochina)
3. ✅ Reasonable page count for a book (200+ pages, not a pamphlet)
4. ❌ No free digital copy exists (confirm via OpenLibrary ebook_access)

...immediately present the paid/used options. Do NOT continue searching for free copies. These books are simply not digitized.

## Known books in this category

| Title | Author | Year | Publisher | Digital | Notes |
|-------|--------|------|-----------|---------|-------|
| *Bay Vien, le maître de Cholon* | Pierre Darcourt | 1977 | Hachette | ❌ No (copyright) | Biography of Bảy Viễn (Binh Xuyen leader). Kindle $10.99 exists. AbeBooks: €10–20. |
| *Hoang-Tham, pirate* | Paul Chack | 1933 | Éditions de France | ✅ **Free on Gallica** (public domain) | Biography of Đề Thám (Yên Thế Insurrection). 279 pages. IIIF-extractable. Also has 2017 reprint: *Le sanglier du Yen Thé*, Éditions Édilys, ISBN 979-10-94912-38-6, 17€. |
| *Au Tonkin* | Paul Chack | 1942 | Éditions de France, coll. *La mer et notre empire* n°21 | ❌ Not digitized | 155 pp, illustrated by Léon Haffner. BnF holds physical copies. AbeBooks: ~US$7. |
| *Les trois Dumas* (not colonial) | various | — | — | — | Not relevant pattern. |

## LC Classification cheat sheet for Vietnam colonial history

| Range | Subject |
|-------|---------|
| DS556–DS559.93 | Vietnam — History |
| DS556.39–556.44 | Biography of Vietnamese figures |
| DS556.8 | French Indochina |
| DS556.83.B39 | Bảy Viễn (LC class for the Bay Vien book) |
| DS557–DS559.9 | Vietnam War era |
| DS560–DS560.72 | Post-war |

When you search OpenLibrary, check `lc_classifications` — DS556+ usually means Vietnam colonial history.

## Gallica IIIF extraction (when the PDF is behind a captcha)

Some Gallica books are fully digitized but require an Altcha CAPTCHA challenge to download the PDF. The IIIF image API is unrestricted. Use the `scripts/gallica-iiif-extract.py` script from the `historical-source-acquisition` skill to extract pages via IIIF and compile into a PDF.

**Pre-flight check before extracting:**
1. Verify the book is public domain (`"domaine public"` in the OAI rights metadata or on the Gallica page)
2. Get the book's ARK from the Gallica URL (e.g. `ark:/12148/bpt6k374553s`)
3. Check the IIIF manifest exists: `https://gallica.bnf.fr/iiif/ark:/12148/<ARK>/manifest.json`
4. If the ARK starts with `bpt6k`, the book is digitized and extractable

**For command details and the runnable script:** see `historical-source-acquisition` SKILL.md → "From Gallica (BnF digital library) — IIIF extraction" section, and `scripts/gallica-iiif-extract.py`.
