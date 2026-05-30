# Public Domain / Open-Access Sources

For public-domain classic works (pre-1928), prefer these sources over shadow libraries — they deliver clean born-digital text PDFs, not scanned OCR mess.

## 1. Online Library of Liberty (OLL)

- **What**: Free, open-access digital editions of classic works in philosophy, history, politics, economics
- **Format**: Clean born-digital text PDFs (~1 MB per volume — not scanned images)
- **Translations**: Often has the standard scholarly translations (e.g. Dryden/Clough Plutarch, Jowett Plato)
- **URL**: https://oll.libertyfund.org/

### Direct PDF URL pattern (JS-heavy site workaround)

OLL uses Turbo/JavaScript to load volume lists. When the page doesn't render with curl, brute-force the underlying S3 storage:

Pattern:
```
https://oll-resources.s3.us-east-2.amazonaws.com/oll3/store/titles/{TITLE_ID}/{TitleShort}_{Code}-{Vol}_EBk_v6.0.pdf
```

Discovery method:
1. Search `oll.libertyfund.org` for the work
2. Note the title ID from the set page (or search results)
3. Try consecutive title IDs until you find the volumes
4. The file pattern uses sequential volume numbers `01`, `02`, etc.

Example — Plutarch's Lives (Dryden trans.), 5 volumes, title IDs 1771–1775:
- https://oll-resources.s3.us-east-2.amazonaws.com/oll3/store/titles/1771/Plutarch_1014-01_EBk_v6.0.pdf
- https://oll-resources.s3.us-east-2.amazonaws.com/oll3/store/titles/1772/Plutarch_1014-02_EBk_v6.0.pdf
- etc.

Use HEAD requests to verify the PDF exists before committing to a download.

## 2. Project Gutenberg

- **What**: 70,000+ free eBooks, mostly public domain
- **Formats**: HTML, plain text, EPUB, Kindle — but NOT PDF
- **URL**: https://www.gutenberg.org/
- **To find**: Search by title/author, then look for ebook ID
- **HTML version**: Can be saved as PDF from browser (Ctrl+P → PDF)
- **Direct text**: `https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt`
- **Example**: Plutarch's Lives (ID 674) at https://www.gutenberg.org/ebooks/674
- **Note**: PG's text files are proofread but may have footnotes inline as endnotes; the HTML version is better formatted

## 3. Bill Thayer's LacusCurtius (Penelope)

- **What**: Classical texts with scholarly apparatus — Greek/Latin originals with English translations
- **Format**: HTML web pages, minutely proofread
- **URL**: http://penelope.uchicago.edu/Thayer/E/Roman/Texts/
- **Strengths**: Loeb translations (Bernadotte Perrin for Plutarch); Stephanus page numbering; very high quality control
- **Best for**: Research use where pagination and scholarly apparatus matter
- **Not**: PDF — browser-based reading

## 4. Internet Archive

- **What**: Scanned public domain books (Open Library)
- **Format**: PDF, DJVU, EPUB (scanned page images, not born-digital text)
- **URL**: https://archive.org/
- **Use case**: When you need a scan of a specific physical edition, or when OLL/Gutenberg don't have a work
- **Caveats**: Mixed OCR quality; many books are "borrow-only" (access-restricted); check for "open-culture" or public-domain status
- **Best accessed via**: Direct search, then look for the "PDF" link on the item page

## Selection guide

| Need | Go to |
|------|-------|
| Clean text PDF, standard translation | OLL |
| HTML/EPUB to read on device | Project Gutenberg |
| Proofread text with academic apparatus | LacusCurtius |
| Scan of a specific edition | Internet Archive |
| Copyrighted academic book | book-hunting (libgen) workflow |

## Pitfalls

- OLL volumes use sequential title IDs — if you find vol 1 at ID X, try X, X+1, X+2, etc. for subsequent volumes
- OLL PDFs are sometimes numbered as e.g. `1014-01` for vol 1 of work code 1014 — look for the pattern in any working URL or the set's cover image URL
- Gutenberg has no PDF downloads — convert from HTML in-browser or use an EPUB→PDF converter
- Archive.org direct download may return 401 for borrow-only items (marked `private="true"` in files.xml)
- Always verify PDF integrity: file starts with `%PDF`, size matches expectation, content is readable text not garbled OCR
