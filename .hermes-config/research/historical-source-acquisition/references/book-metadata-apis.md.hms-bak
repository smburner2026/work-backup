# Book Metadata APIs (Fallback when web search / browser tools fail)

When `web_search`, `web_extract`, and `browser_navigate` all fail due to rate limits, CAPTCHAs, or Chrome unavailability, these no-auth API endpoints provide reliable bibliographic data via direct `curl` + JSON parsing.

---

## 1. OpenLibrary Search

**Endpoint:** `GET https://openlibrary.org/search.json?q=<URL_ENCODED_QUERY>`

Search by title, author, or ISBN. Returns work and edition keys.

```bash
curl -sL "https://openlibrary.org/search.json?q=%22Bay+Vien%22+%22le+ma%C3%AEtre+de+Cholon%22"
```

**Key fields in response:**
```json
{
  "numFound": 1,
  "docs": [
    {
      "author_key": ["OL193529A"],
      "author_name": ["Pierre Darcourt"],
      "cover_edition_key": "OL4666468M",
      "ebook_access": "no_ebook",
      "edition_count": 1,
      "first_publish_year": 1977,
      "has_fulltext": false,
      "key": "/works/OL1699693W",
      "language": ["fre"],
      "public_scan_b": false,
      "title": "Bay Vien, le maître de Cholon"
    }
  ]
}
```

**Triage fields:**
- `ebook_access`: `"no_ebook"` = no free copy; `"borrow_available"` = IA lending; `"printdisabled"` = inaccessible
- `has_fulltext`: `false` = no free text
- `public_scan_b`: `false` = not public domain
- `cover_edition_key`: construct the edition URL from this

---

## 2. OpenLibrary Work

**Endpoint:** `GET https://openlibrary.org/works/{OLkey}.json`

Work-level metadata: subjects, classifications, author links.

```bash
curl -sL "https://openlibrary.org/works/OL1699693W.json"
```

**Key fields:**
```json
{
  "title": "Bay Vien, le maître de Cholon",
  "covers": [8373730],
  "subject_places": ["Vietnam"],
  "subject_people": ["Bảy Viễn (1904-)"],
  "lc_classifications": ["DS556.83.B39 D37"],
  "dewey_number": ["959.704/092/4", "B"],
  "subjects": ["Revolutionaries", "Biography"],
  "first_publish_date": "1977"
}
```

---

## 3. OpenLibrary Edition

**Endpoint:** `GET https://openlibrary.org/books/{OLkey}.json`

Edition-level data: ISBN, publisher, pagination, series, OCLC numbers.

```bash
curl -sL "https://openlibrary.org/books/OL4666468M.json"
```

**Key fields:**
```json
{
  "publishers": ["Hachette"],
  "isbn_10": ["201003449X"],
  "pagination": "417 p. ;",
  "number_of_pages": 417,
  "publish_date": "1977",
  "series": ["Les Grands aventuriers"],
  "lccn": ["77556970"],
  "oclc_numbers": ["3629136"],
  "dewey_decimal_class": ["959.704/092/4", "B"],
  "subjects": ["Bảy Viễn, 1904-", "Revolutionaries -- Vietnam -- Biography."],
  "identifiers": { "goodreads": ["1326835"] },
  "source_records": ["amazon:201003449X", ...]
}
```

Note: `identifiers.goodreads` gives you the Goodreads ID for step 4.

---

## 4. Goodreads (Embedded JSON)

**Endpoint:** `GET https://www.goodreads.com/book/show/{goodreads_id}`

Goodreads pages embed a `__NEXT_DATA__` script tag containing full metadata including Kindle pricing and affiliate purchase links. No API key needed.

```bash
curl -sL "https://www.goodreads.com/book/show/1326835"
```

**Extraction (two approaches):**

```bash
# Approach 1: grep + jq
curl -sL "https://www.goodreads.com/book/show/1326835" | \
  grep -oP '__NEXT_DATA__[^>]*>\K.*?(?=</script>)' | \
  jq '.props.pageProps.apolloState' > goodreads-data.json

# Approach 2: grep to Python
curl -sL "https://www.goodreads.com/book/show/1326835" | \
  grep -oP '__NEXT_DATA__[^>]*>\K.*?(?=</script>)' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d, indent=2))"
```

**Target paths in the JSON blob:**

- **Kindle info:** `.props.pageProps.apolloState["Book:..."].links.primaryAffiliateLink`
  ```json
  {
    "name": "Amazon",
    "url": "https://www.amazon.com/gp/product/B08BQFR9YW/...",
    "ebookPrice": "10.99",
    "kuEligible": false
  }
  ```

- **All purchase links:** `.props.pageProps.apolloState["Book:..."].links.secondaryAffiliateLinks`
  Returns array of: Amazon, Audible, Barnes & Noble, AbeBooks, Kobo, Apple Books, Google Play, Alibris, Indigo, Better World Books, IndieBound, Thriftbooks

- **Library links:** `.props.pageProps.apolloState["Book:..."].links.libraryLinks` — WorldCat link

- **Book details:** `.props.pageProps.apolloState["Book:..."].details`
  ```json
  {
    "format": "Paperback",
    "numPages": 417,
    "publisher": "Librairie Hachette",
    "isbn": "201003449X",
    "isbn13": "9782010034497",
    "language": { "name": "French" }
  }
  ```

- **Ratings:** `.props.pageProps.apolloState["Work:..."].stats`
  ```json
  {
    "averageRating": 4,
    "ratingsCount": 3,
    "textReviewsCount": 1
  }
  ```

- **Full review text:** `.props.pageProps.apolloState["Review:..."].text`

---

## 5. Typical Workflow

When all standard web tools are down and you need bibliographic data:

```
1. curl search.json with title/author → get work key + cover_edition_key
2. Check ebook_access + has_fulltext + public_scan_b → is free copy available?
3. curl edition.json → get ISBN, publisher, pages, series, Goodreads ID
4. curl goodreads.com → extract __NEXT_DATA__ for Kindle price + purchase links
5. Report findings: bibliographic data + availability (free / paid / neither)
```

**Remember:** for post-1970 books still under copyright, there is usually no free electronic copy. Report the paid ebook options from Goodreads affiliate links and used physical copies from AbeBooks/Alibris.
