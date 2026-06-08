# Rare & Out-of-Print French Colonial Book Search Workflow

For finding rare French colonial-era books (1930s–1970s) about Vietnam/Indochina. These are typically **not digitized**, still under copyright, and only available as used physical copies or modern reprints.

## Search order (preferred sequence when web_search/Tavily is down)

### 1. OpenLibrary API (fast, reliable, no JS)

```bash
# Search by title + author
curl -s 'https://openlibrary.org/search.json?q=<TITLE>+<AUTHOR>&limit=10'

# Get work details
curl -s 'https://openlibrary.org/works/<WORK_KEY>.json'

# Get edition details (includes ISBN, publisher, page count)
curl -s 'https://openlibrary.org/books/<EDITION_KEY>.json'
```

Key fields in response:
- `ebook_access`: "no_ebook" = not freely available (typical for in-copyright)
- `has_fulltext`: false = no full text
- `first_publish_year`, `publisher`, `isbn_10`, `lccn`, `oclc_numbers`

### 2. Goodreads (for purchase links and Kindle availability)

Fetch the HTML page then extract `__NEXT_DATA__` JSON — it contains:
- Affiliate links (Amazon Kindle $price, paperback)
- Alternative retailers (AbeBooks, Kobo, Apple Books, Google Play, Alibris)
- User reviews and ratings
- Edition metadata (format, pages, publisher, language)

The `__NEXT_DATA__` script tag contains `props.pageProps.apolloState` with the full book object including `primaryAffiliateLink.ebookPrice` for Kindle pricing.

### 3. AbeBooks (for used physical copies)

```bash
curl -sL 'https://www.abebooks.fr/servlet/SearchResults?tn=<TITLE>&an=<AUTHOR>'
```

Search by ISBN for tighter results. Extract prices with `grep -oP 'item-price[^>]*>[^<]*'`.

### 4. Wikipedia search API

```bash
# Search for book mention in citations
curl -s 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=<TITLE>&format=json'

# Get full page to find the book in the Works/Bibliography section
curl -s 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=<PAGE>&format=json&explaintext=1'

# Get external links from a page (may include library catalog links)
curl -s 'https://en.wikipedia.org/w/api.php?action=parse&page=<PAGE>&prop=externallinks&format=json'
```

### 5. BnF Catalogue SRU API (French National Library — covers all holdings)

**Endpoint:** `https://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve`

**Query examples:**
```
# By author
bib.author all "Chack, Paul"

# By title  
bib.title all "Hoang-Tham"

# Combined
bib.author all "Chack" and bib.title all "Tonkin"
```

**Get full bibliographic record:**
```
https://catalogue.bnf.fr/ark:/12148/<ARK_ID>
```
The HTML page contains MARC subfield data with publisher, date, pagination, series, BnF location, call number.

**Get structured data (RDF/XML or JSON):**
```
https://data.bnf.fr/ark:/12148/<ARK_ID>
```

**Key facts:** BnF catalogues ALL its holdings — not just digitized items. In-copyright books (post-1920s) will have full metadata even if no digital copy exists.

### 6. WorldCat (worldcat.org or search.worldcat.org)

Search by title, author, ISBN, or OCLC number. Shows library holdings worldwide. May require session/JS — use as fallback when BnF is insufficient.

## Typical outcome patterns

| Book era | Likelihood of digital copy | Best next step |
|----------|---------------------------|----------------|
| Pre-1920s | Moderate–high (public domain, Gallica/Archive.org) | Check Gallica, Archive.org, HathiTrust |
| 1930s–1950s French colonial | Low for most, but **check Gallica** if author died before 1955 (French copyright: 70y pma + possible WWII extensions). Example: Paul Chack (executed 1945), Hoang-Tham pirate (1933) IS public domain in France and on Gallica despite 1933 publication date. | Check Gallica IIIF manifest (ark:/12148/bpt6k...), then `historical-source-acquisition`'s `scripts/gallica-iiif-extract.py`. If not on Gallica: AbeBooks used copy. |
| 1960s–1970s French colonial | Very low. Author likely alive past 1955 → still in copyright. Example: Pierre Darcourt, Bay Vien (1977) — NOT public domain. | Pivot to paid/used: Goodreads → Kindle/AbeBooks. |
| Modern reprint (2010s+) | Purchase only | ISBN search → French bookstores (leslibraires.fr, Amazon.fr, Fnac) |

## French reprint detection

Check BnF SRU for multiple entries — a later DL (Dépôt Légal) date indicates a reprint. Look for:
- `dateEdit=DL 20XX` in the BnF record
- Modern ISBN (979- prefix typically)
- Different publisher (often Édilys, L'Harmattan, Hachette rééditions)

## Verifying book availability in Vietnam

- **National Library of Vietnam** (nlv.gov.vn) — OPAC available at opac.nlv.gov.vn (requires login for full search)
- **Vietnamese university libraries** — may hold French colonial collections
- Used French books sometimes appear on Vietnamese secondhand book markets (HCMC book street, Cholon area)

## When to skip to "not available digitally"

If OpenLibrary returns `ebook_access: "no_ebook"` AND `has_fulltext: false` AND the book is post-1928 (copyrighted), pivot immediately to paid/used options. Do not waste time searching Archive.org, HathiTrust, or shadow libraries for post-1930 French colonial books — they will not be there.
