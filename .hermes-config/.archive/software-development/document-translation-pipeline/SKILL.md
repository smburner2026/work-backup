---
name: document-translation-pipeline
category: software-development
description: Full pipeline for translating foreign-language books/documents into English — extraction, glossary, batch LLM translation, PDF compilation with embedded images.
domain: document-processing, translation
---

# Document Translation Pipeline

Translate foreign-language documents (PDF books, scanned texts, compilation docs) into English with consistent style, glossary preservation, and formatted output.

## Trigger

User presents a document and says "translate this" or similar.

## Assessment Phase

1. **Identify format**: PDF vs scanned vs text
   - `pdfinfo` → check page count, embedded text vs image-based
   - `pdftotext` → test extraction quality. Clean text? Spacing artifacts? Form feeds?
   - `pdfimages -list` → check for embedded photos/illustrations

2. **Determine voice/tone from document type**:
   - **Narrative/novel** → colloquial English, storytelling voice ("guy telling a story over a beer")
   - **Documentary/historical compilation** → clear expository English, factual but not stiff
   - **Official correspondence/letters** → formal register matching source
   - **Technical/academic** → precise, register-neutral

3. **Size estimation**: chars of source text → estimate token cost and batch strategy
   - Under 50K chars → single delegate_task batch
   - 50-200K chars → 2-3 batches
   - Over 200K chars → batch in groups of 3 chapters via parallel delegate_task

## Glossary Building

Before translating, identify:

- **Proper names** (people, places, organizations) → ALWAYS keep in source language, never translate
- **Specialized terms** (religious offices, military ranks, historical titles) → define once, preserve consistently
- **Untranslatable idioms** → note for adaptation to nearest English equivalent
- **Common pitfalls** — names that look like they could be translated but shouldn't be

### Glossary format for delegate_task context:
List key terms with `source → English` mapping. Include the glossary in each translation batch's context so every subagent uses consistent rendering.

## Extraction & Cleaning

```bash
# Extract text
pdftotext input.pdf /tmp/raw.txt

# Check quality
wc -l /tmp/raw.txt
head -50 /tmp/raw.txt

# Extract images (if needed for output PDF)
mkdir -p /tmp/images
pdfimages -j input.pdf /tmp/images/img
```

### Cleaning steps:
- Strip page number lines, ebook boilerplate, form-feed chars
- Fix spacing artifacts (e.g. "T ỉnh T âm" → "Tỉnh Tâm")
- Remove TOC page headers that repeat in body
- Split into logical sections/chapters
- Write cleaned text to a single file for translation

## Translation Strategy

### For narrative books (e.g. Bay Vien):
- Use delegate_task with `goal` describing the voice/rules
- Batch 3 chapters at a time
- Each subagent reads source file, translates, writes output
- Include full glossary in context
- Key rules: colloquial English, preserve proper names, adapt idioms, no commentary

### For documentary compilations (e.g. Cao Dai Army):
- Clear, factual English — not slangy, not stiff academic
- Formal register for historical letters/official documents
- Poems rendered as rhymed English verse
- "Bần Đạo" → "This humble priest" (formal self-reference)
- Preserve all dates (lunar + Western), ranks, signatories

### Batch pattern:
```python
delegate_task(tasks=[
    {"goal": "Translate chapter X...", "context": source_text + glossary, "toolsets": ["terminal","file"]},
    ...  # up to 3 parallel
])
```

Each subagent: reads → translates → writes to output directory.

## PDF Compilation

1. Build HTML with proper book styling (Georgia serif, 6×9in page, title page, section headers)
2. Include extracted images:
   - Photo section at end → numbered gallery
   - Portrait images → embed near relevant text sections
3. Convert via weasyprint: `weasyprint book.html book.pdf`
4. Verify with `pdfinfo`: check pages, images, file size

### Image handling:
- Extract with `pdfimages`
- Convert PPM to JPG with PIL: `Image.open(ppm).save(jpg, 'JPEG', quality=85)`
- Reference in HTML via `file://` absolute paths
- WeasyPrint embeds them directly

## User Preferences (TempMoon)

These are embedded preferences for this user — follow them unless explicitly overridden:

- **Style**: colloquial English for narrative, documentary-clear for factual. Storytelling voice.
- **Proper names**: ALWAYS keep in source language (Vietnamese). Never anglicize or translate.
- **Idioms**: adapt to closest natural English equivalent. Don't translate literally.
- **No footnotes, no translator commentary**: clean text only.
- **Include original photos/images** in output PDF when source has them.
- **Delivery**: full compiled PDF via send_message (MEDIA: path or file attachment).

## Pitfalls

- **PDF text extraction quality varies**: Always check pdftotext output before cleaning. Some PDFs have embedded text with spacing artifacts; some are pure scans (need OCR).
- **Form-feed separators**: Strip `\f` chars during cleaning, they break paragraph flow.
- **Subagent filenames**: delegate_task subagents may save with English filenames instead of original — verify after batch completes. Rename if needed for sorted order.
- **WeasyPrint file paths**: Use absolute paths with `file://` prefix. PPM images must be converted to JPG first.
- **Tone consistency across batches**: Include the glossary AND a tone/voice note in every delegate_task context so all subagents maintain the same register.
- **Poetry translation**: Allow creative license — preserve meaning and emotion, not syllable count. Rhymed verse preferred.

## Verification

- Spot-check first 3 paragraphs of each batch for voice consistency
- Verify proper names are preserved (not translated)
- Check that poems/songs have natural English verse
- Verify PDF renders correctly (pages, images, no overflow)
