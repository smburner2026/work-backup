---
title: Document Translation Pipeline
name: document-translation
description: Translate foreign-language books/documents to English — PDF extraction, glossary construction, translation with voice control, layout-preserving output compilation.
domain: productivity
keywords: [translation, pdf, vietnamese, glossary, layout-preservation, tts]
---

# Document Translation Pipeline

Translate foreign-language documents (books, pamphlets, PDFs) into English with controlled voice, glossary injection, and layout-preserving output.

## When to Use

- User provides a foreign-language document/PDF and asks for translation
- Workflow involves: extract text → clean → build glossary → translate → compile output
- The output needs to preserve original layout (images, photos, document structure)

## Workflow

### 1. Source Assessment
- Check format: PDF (embedded text vs scanned), EPUB, DOCX
- Check language: identify source language
- Check size: page count, character count, image count
- Check text quality: pdftotext for embedded text; OCR (tesseract) for scans

```
pdfinfo <file.pdf>                # pages, size, metadata
pdftotext <file.pdf> <output.txt> # extract text
wc -c <output.txt>                # text size
```

**IMPORTANT**: The `terminal()` tool has a ~50KB stdout cap. For files >50KB, read with Python's `open()` directly or `write_file` + `read_file`.

### 2. Extract & Clean Text
- Split by form-feed (`\f`) or known chapter boundaries
- Strip boilerplate (ebook headers, page numbers, "Tạo Ebook:" lines, "Nguồn:" lines)
- Fix spacing artifacts (search for `T ỉnh T âm`-style character spacing)
- Save individual chapter files for parallel translation

### 3. Build Glossary
Extract proper nouns, domain terms, rank names, place names, organization names. These MUST be preserved in original language in the translation.

**Vietnamese-specific glossary patterns:**
- Military ranks: Thiếu Tướng (Major General), Đại Tá (Colonel), Trung Tướng (Lieutenant General)
- Honorifics: Đức (His Holiness), Bần Đạo (this humble priest), Ngài (His Excellency)
- Religious titles: Hộ Pháp (Pope/Dharma Protector), Giáo Tông (Pope), Chức Sắc (Dignitary)
- Cao Đài specific: Tòa Thánh (Holy See), Thánh Địa (Holy Land), Đạo Hữu (Caodaiist)
- Bình Xuyên specific: giang hồ (gangster/outlaw), du đãng (hooligan), vượt ngục (prison break), chi đội (battalion/regiment)
- Period terms: Phòng Nhì (Deuxième Bureau), Việt Minh, chúa đảo (island warden)

### 4. Translation — Voice Control
- **Determine the right tone from the source material:**
  - Narrative/novel → colloquial storytelling voice ("a guy telling a story over a beer")
  - Documentary/archival → clear expository English, formal for official documents
  - Historical letters → period-appropriate formal register

**User preferences (TempMoon, Vietnamese→English):**
- Keep ALL proper names in original Vietnamese — never translate "Bảy Viễn" to "Seven Vien" etc.
- Colloquial English voice: contractions, sentence fragments, natural dialogue rhythm
- Adapt idioms that don't translate literally to closest English equivalent
- NO footnotes, NO translator commentary, NO bracketed explanations
- Dialogue rendered in natural spoken English
- Poems → English verse with rhyme where possible

**Preserve:** all dates (lunar + Western), signatures, document metadata (signatories, attendees, locations)

**Sample first:** Always translate chapters 1-3 (or the prologue/introduction) as a sample for user sign-off before committing to full batch. User feedback on sample voice/register/idiom choices is binding for the rest of the document. A 3-chapter sample costs far less than retranslating 50+ chapters.

### 5. Output Compilation

#### Option A — Clean text PDF (no layout preservation)
- Use weasyprint to convert HTML → PDF
- Configure `@page` CSS for book format (6in × 9in recommended)
- Title page, table of contents, chapter headings
- Books over 200 pages: generate preview (first 3 chapters) for user approval first

**CRITICAL — Layout Preservation for Images:**
If the original has photos/images embedded in the text, use extracted-image embedding — NOT page-image overlays.

Layout preservation approach (accepted by the user after 3 iterations):
1. Extract images from source PDF with `pdfimages -j input.pdf /tmp/images/img`
2. Map each extracted image to its source page using `pdfimages -list`
3. Extract text and translate
4. Generate HTML with English text and images embedded at their narrative positions (portraits next to the relevant biography, maps next to battle descriptions)
5. Append a photo gallery section at the end for any remaining full-page photos
6. Compile via WeasyPrint with `file:///` absolute paths for images

**THREE ITERATIONS (in order of rejection):**
1. ✗ All photos dumped at end → "they are not where they are supposed to be"
2. ✗ Full-page screenshots of original pages with English overlaid → "looks weird"
3. ✓ Clean English text + extracted photos at narrative positions + gallery at end → "a little weird but fine"

**Always go straight to approach 3. Do not attempt 1 or 2.**

Workflow:
```bash
# Extract images
pdfimages -j input.pdf /tmp/images/img
pdfimages -list input.pdf   # see page→image mapping

# Convert any PPM images to JPEG
python3 -c "from PIL import Image; import glob; [Image.open(f).save(f.replace('.ppm','.jpg'),'JPEG',quality=85) for f in glob.glob('/tmp/images/*.ppm')]"
```

**CRITICAL RULES:**
- PPM images MUST be converted to JPEG before embedding in HTML — WeasyPrint cannot render PPM
- Use absolute `file:///tmp/images/img-xxx.jpg` paths in HTML — WeasyPrint doesn't support relative paths consistently
- Verify all images render: WeasyPrint emits "Failed to load image" errors on stderr for missing files
- Page numbers from `pdfimages -list` use 1-indexed PDF page numbers, which may differ from the printed page numbers in the source book's footer

**Approval workflow:**
- For books over ~100 pages: generate preview (first 3 chapters) first
- Wait for user sign-off on voice, format, and image placement
- Then generate full book

### Size Estimation & Batch Strategy

Estimate total source text size and select the right parallelism level:

| Size | Batch strategy |
|------|---------------|
| Under 50K chars | Single `delegate_task` batch |
| 50–200K chars | 2–3 batches, sequential |
| Over 200K chars | Parallel batches of 3 chapters each via `delegate_task(tasks=[...])` |

### Tone Consistency Across Batches

When using parallel subagents for batch translation, include BOTH the glossary AND a tone/voice note in every delegate_task context so all subagents maintain the same register:

```python
delegate_task(tasks=[
    {"goal": "Translate chapter X...", 
     "context": source_text + glossary + tone_note, 
     "toolsets": ["terminal", "file"]},
])
```

Key consistency rules:
- **Subagent filenames**: Verify after batch completion — subagents may save with English filenames instead of original. Rename if needed for sorted chapter order.
- **Poetry translation**: Allow creative license — preserve meaning and emotion, not syllable count. Rhymed verse preferred.
- **Spot-check**: Verify first 3 paragraphs of each batch for voice consistency. Confirm proper names are preserved (not translated).

## Pitfalls

- **Multi-candidate source confusion**: When the user says "I'm interested in [topic], what books are out there on X" and then picks one from the list you provided — do NOT assume you know which source they meant. They will say "No, the [other language] book" after you've built a pipeline for the wrong one. After the user picks a source text: one clarifying question ("Which source should we work from?") costs less than backpedaling a full pipeline.
- **terminal() stdout cap** at ~50KB. For large files, read with Python `open()` directly or split reads.
- **`\f` (form feed)** characters in PDF text extraction = page breaks. Use these for chapter splitting.
- **Vietnamese diacritics** (`đ` vs `ð`, `ơ` vs `o`) cause filename mismatches. Use `find` with wildcards.
- **PPM images** need conversion to JPEG. Use Python PIL: `Image.open(ppm).save(path, 'JPEG', quality=85)`
- **weasyprint** needs absolute file paths for images (`file:///tmp/path/to/image.jpg`).
- **ImageMagick `convert`** may not be installed. Use Python PIL as fallback.
- **PDF size** >8MB fails Discord delivery. Compress aggressively (lower DPI, lower quality).
- **Mnemosyne** can have database issues — if `mnemosyne_remember` fails, use `memory` or `terminal` tools as fallback.
- User may correct photo placement FIRST before text quality — image positioning is highest-priority quality signal.
