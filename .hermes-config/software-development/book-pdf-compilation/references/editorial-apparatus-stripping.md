# Editorial Apparatus Stripping (WeasyPrint Anthology Path)

When compiling an anthology of translated works, the source texts often contain extensive editorial apparatus — footnotes, introductory commentary, translator's endnotes, and publisher front/back matter that should be excluded from the clean text.

## Source Types and Their Editorial Footprint

| Source | Editorial Burden | Typical Artifacts |
|--------|-----------------|-------------------|
| **Kaufmann (Will to Power)** | Heavy — ~1.6MB text, ~20% editorial | `COMMENT` sections between aphorisms, numbered footnotes (e.g. `1 Atemanhalten...`), lengthy introduction, "About the Author" back matter, inline superscript markers (`his1`), section-by-section editorial commentary |
| **Hollingdale / Cambridge editions** | Medium | Numbered endnotes scattered throughout, translator's introduction, editorial preface |
| **Johnston (public domain)** | Light | Minimal — generally just the Nietzsche text with section numbers |
| **Stanford Nachlass volumes** | Medium | Editorial apparatus on section numbering, transcription notes in brackets |

## Stripping Strategy (by Source)

The `strip_editorial_apparatus(text, source)` function is called before `cleanup_text()` in the build pipeline. It takes the filename as context so each source gets the right treatment.

### Will to Power (Kaufmann) — Most Aggressive

```python
# 1. Strip everything before the first numbered section
first_section = re.search(r'^[0-9]+\s+\(', text, re.MULTILINE)
if first_section:
    text = text[first_section.start():]

# 2. Remove COMMENT blocks (Kaufmann's paragraph-length editorial interjections)
text = re.sub(r'\n\nCOMMENT\n\n.*?(?=\n\n[0-9]+\s+\()', '', text, flags=re.DOTALL)

# 3. Remove numbered footnote lines at section ends
text = re.sub(r'\n[0-9]+\s+[A-Z][a-z].*?(?=\n\n)', '', text)

# 4. Remove inline footnote markers (e.g. "his1" → "his")
text = re.sub(r'([a-z])[0-9]+([,.;\s)!?])', r'\1\2', text)

# 5. Remove About the Author / publisher back matter
text = re.sub(r'\n\n.*?About the Author.*?(?=\n\n[0-9]+\s+\()', '', text, flags=re.DOTALL)
```

### Cambridge / Hollingdale Editions

```python
# Remove numbered editorial endnotes inline
text = re.sub(r'\n[0-9]+\.\s+[A-Z][a-z].*?(?=\n\n)', '', text)

### Aggressive Inline Number Stripping (ALL Works)

After source-specific stripping, apply these patterns across ALL works to catch remaining inline footnote markers:

```python
# Pattern 1: digits attached to words — "bêtise111" → "bêtise"
text = re.sub(r'([a-z])[0-9]+([,.;:!?)\s\])]*)', r'\1\2', text)

# Pattern 2: digits with surrounding punctuation — "Wallace112)" → "Wallace)"
text = re.sub(r'([a-zA-Z])([0-9]+)([)\]})]*)', r'\1\3', text)

# Pattern 3: Cambridge-style footnote starts — "1879. While at Basle..."
text = re.sub(r'\n[0-9]+\.\s+[A-Z].*?(?=\n\n)', '', text)
text = re.sub(r'\n[0-9]+\.\s+[A-Z].*?(?=\n[A-Z])', '', text)
```

**Caveat:** These are aggressive. They will strip any number attached to a letter — including legitimate page numbers in cross-references like "see Vol. 14". Test the output on the first 20 pages after applying. The trade-off is accepted because the user explicitly wants ALL editorial numbering removed for a clean reading experience.
```

### General (All Sources)

```python
# Remove EPUB cruft lines (horizontal rules and section markers)
text = re.sub(r'\n---.*?---\n', '\n\n', text)
```

## Section Break Formatting

After stripping editorial matter, numbered aphorisms/sections (e.g. `2 (Spring-Fall 1887)`) should get page breaks before them. This is handled in `markdown_to_html()`:

```python
# Convert numbered section headers into page-breaking HTML elements
text = re.sub(r'^([0-9]+\s+\([A-Z].*?\))$', 
              r'<div class="section-break"><p>\1</p></div>', 
              text, flags=re.MULTILINE)
```

With CSS:

```css
.section-break { page-break-before: always; margin-top: 1.5em; }
.section-break p:first-child { font-weight: bold; font-size: 11pt; color: #444; }
```

## Limitations

- **Regex-based stripping is fragile** — editorial footnotes that blend into Nietzsche's own text paragraphs (multi-sentence notes starting mid-section) may not match the pattern. Manual inspection of the first 20 pages is always required after a stripping pass.
- **Inline numbers can be ambiguous** — Nietzsche's own aphorisms use numbered sections (e.g. "2 (Spring-Fall 1887)"). The `strip_editorial_apparatus` function preserves these. Only editorial footnotes (pattern: `[number] [space] [uppercase start of commentary paragraph]`) are stripped.
- **COMMENT blocks must not remove Nietzsche text** — The regex looks for `\n\nCOMMENT\n\n` followed by text up to the next section header. If a COMMENT block lacks section headers (unusual but possible), the regex won't match and the block survives — better to leave editorial text than to delete Nietzsche's.
- The patterns above work specifically for the **Vintage Books / Random House** edition of WtP (Kaufmann translation). Other editions may use different footnote conventions.
