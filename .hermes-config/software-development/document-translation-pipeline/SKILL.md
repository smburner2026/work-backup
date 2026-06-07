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

2. **Determine voice/tone from document type and source language**:

   The user has established multiple approved registers — the correct one depends on SOURCE LANGUAGE and GENRE, not a single preference:

   ### Vietnamese-language sources

   - **Narrative/novel** (e.g. Bảy Viễn) → colloquial English, storytelling voice ("guy telling a story over a beer")
   - **Scholarly history** (e.g. Phạm Văn Sơn, VSTB) → **Burckhardtian scholarly** register: cultured, measured, carries the author's partisan energy. See `vstb-ocr-workflow` skill → Phase 4 → Voice A for full rules.
   - **Documentary compilation** (e.g. Cao Đài Army) → clear expository English, factual but not stiff
   - **Official correspondence/letters** → formal register matching source

   ### French-language sources

   - **Colonial adventure/history** (e.g. Paul Chack, colonial officers' narratives) → **Conrad-Kipling adventure** register: weighted, vivid, slightly formal early-20th-century adventure prose. Sensory landscapes, plain violence, colonial "our/we" perspective. See `vstb-ocr-workflow/references/french-colonial-translation.md` → Phase 3: Register Selection for full rules.

   ### General

   - **Technical/academic** → precise, register-neutral
   - **Rule of thumb**: Source language determines the flavour of the characters' world; source genre determines the narrative register. A Vietnamese historical text gets a different English voice than a French colonial account of the same events.

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

### Kanban batching — multi-segment books

For full-book translations (especially French colonial texts or 60K+ word works), split by part/chapter and batch via kanban + parallel subagents:

1. **Split** the cleaned source text into per-part segment files by page range
2. **Create kanban board + cards** for the project:
   ```bash
   hermes kanban boards create <slug> --name \"Project Name\" --switch
   hermes kanban create --body \"Source: /path/to/source.txt\\nVoice ref: /path/to/voice-ref.txt\" \"Translate: Part N — Title\"
   ```
3. **Save the approved sample** as a voice-reference file for subagents (critical for register consistency)
4. **Dispatch** segments in parallel batches of up to 3:
   ```python
   delegate_task(
       tasks=[{goal: \"...\", context: \"...\", toolsets: [\"file\", \"terminal\"]} for each part],
       toolsets=[\"file\", \"terminal\"]
   )
   ```
5. **Verify** all output files exist with expected sizes
6. **Consolidate** into single translation file
7. **Mark cards complete** via `hermes kanban complete <task_id>`

See `vstb-ocr-workflow/references/french-colonial-translation.md` → Phase 4: Kanban Batching Pattern for the full worked example (Hoang-Tham, 279 pages, 5 segments, ~60K English words).

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

These are established preferences for this user's translation projects. Follow them unless explicitly overridden for a specific text:

### Register selection (source-type-dependent)

| Source type | Voice | Example works |
|---|---|---|
| Vietnamese narrative/novel | Colloquial storytelling | Bảy Viễn |
| Vietnamese scholarly history | Burckhardtian | VSTB (Phạm Văn Sơn) |
| Vietnamese documentary compilation | Clear expository, formal for letters | Cao Đài Army |
| French colonial adventure/history | Conrad-Kipling | Hoang-Tham (Paul Chack) |

### Universal rules (applies to all registers)

- **Proper names**: ALWAYS keep in source language (Vietnamese). Never anglicize or translate names.
- **Titles/ranks**: Translate on first use with original in parentheses, then use English thereafter.
- **Idioms**: Adapt to closest natural English equivalent. Don't translate literally.
- **No footnotes, no translator commentary**: clean text output only.
- **Page markers**: Remove from output.
- **Dialogue**: Natural spoken register, raw when characters speak.
- **OCR garbles**: Reconstruct from context where possible.
- **Output format**: Plain text, not markdown. PDF compilation is a separate post-process step.

### Delivery

- Full compiled PDF via send_message (MEDIA: path or file attachment).
- For kanban-tracked projects: mark cards complete on the project board after verification.

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
