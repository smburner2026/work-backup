---
name: gallica-book-extractor
description: Download public-domain and open-access digitized books from Gallica (BnF) via IIIF image API, compile into PDF. For French colonial-era and Indochina/Vietnam sources.
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [gallica, bnf, digitization, pdf, iiif, french-colonial, vietnam]
    related_skills: [vietnamese-historian]
---

# Gallica Book Extractor

Extract digitized books from Gallica (Bibliothèque nationale de France) using the IIIF image API and compile them into PDFs. Works for public-domain books. Some copyright-restricted books also serve IIIF images (for onsite consultation) which can be downloaded.

## Trigger conditions

- User asks to download/extract a book from Gallica/BnF
- User shares a Gallica ARK URL (e.g. `https://gallica.bnf.fr/ark:/12148/bpt6k374553s`)
- A French colonial-era or Vietnamese history book needs digitization

## Workflow

### 1. Check if the book is on Gallica

Search for the book in the BnF catalog via SRU:

```
curl -s 'https://catalogue.bnf.fr/api/SRU?operation=searchRetrieve&query=bib.title%20all%20%22TITLE%22%20and%20bib.author%20all%20%22AUTHOR%22&maximumRecords=10'
```

Look for `ark:/12148/bpt6k...` records — `bpt6k` prefix means it's digitized.

### 2. Download the IIIF manifest

```
curl -sL 'https://gallica.bnf.fr/iiif/ark:/12148/bpt6kXXXXXXX/manifest.json'
```

This gives: page count, image service URLs, metadata.

### 3. Download page images

Each page image is at:
```
https://gallica.bnf.fr/iiif/ark:/12148/bpt6kXXXXXXX/f{N}/full/600,/0/default.jpg
```

**Rate limiting:** Gallica's IIIF server aggressively rate-limits (HTTP 429). Use:
- 12-second delays between page downloads
- 300-second backoff on 429
- 120-second initial cooldown before starting
- Use lower resolution (800, or 600,) to reduce load

### 4. Compile PDF

Use `img2pdf` for lossless JPEG-to-PDF conversion:
```python
import img2pdf
with open(output_pdf, "wb") as f:
    f.write(img2pdf.convert(sorted_page_files))
```

### 5. Save to project directory

For Vietnam-related sources:
```
/root/work/post-colonial-vietnam/sources/{author}/
```

## Pitfalls

- **Rate limiting (429):** Always include 2min initial wait + 12s+ delays + 5min backoff. Never retry faster.
- **Copyright:** Books published after ~1925 may have restricted IIIF access. Check the IIIF manifest `license` field. Test with `curl -I` on a single image page — if 200, images are accessible.
- **Altcha CAPTCHA:** The PDF download endpoint (`/ark/.../f1.pdf`) redirects to an Altcha proof-of-work challenge. The IIIF image API bypasses this. Always use IIIF, not PDF direct download.
- **Resume support:** Write scripts that skip already-cached image files so interrupted runs can resume.
- **IIIF image server URL:** Follows pattern `https://gallica.bnf.fr/iiif/ark:/12148/bpt6kXXXXXXX/f{N}`. The manifest is the authoritative source.
- **Use `img2pdf` not Pillow:** Pillow re-encodes JPEGs (lossy), `img2pdf` wraps them losslessly.
- **Session affinity:** Some Gallica requests require JSESSIONID cookies. The first request to the manifest sets this.
