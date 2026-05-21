# WeasyPrint Anthology Pipeline

Validated approach for compiling large multi-work anthologies (1,000+ pages) into a single PDF using WeasyPrint for CSS-controlled typography and pdfunite for memory-safe merging.

## Validated On

- **Nietzsche Complete Works** — 10 works, 2 appendix volumes, 4,402 pages, 7.8 MB output
- **Target**: 6×9 trim (6in × 9in), Liberation Serif 10pt, justified with hyphenation
- **VPS**: 2 GB RAM + 1 GB swap (WeasyPrint OOM on single ~5MB+ HTML → per-work split required)

## Architecture (Per-Work → pdfunite Merge)

Split the anthology into per-work HTML files, build each as its own small PDF via WeasyPrint, then merge with `pdfunite`. This avoids the ~3MB+ single-HTML OOM threshold on memory-constrained systems.

```
Output PDF = pdfunite(title.pdf, toc.pdf, intro.pdf, work_01.pdf, …, work_N.pdf)
```

## Key CSS for 6×9 Anthology

```css
@page {
  size: 6in 9in;
  margin: 0.7in 0.65in 0.75in 0.65in;
  @bottom-center {
    content: counter(page);
    font-family: 'Liberation Serif', Georgia, serif;
    font-size: 9pt;
    color: #666;
  }
}
body {
  font-family: 'Liberation Serif', Georgia, serif;
  font-size: 10pt;
  line-height: 1.3;
  text-align: left;
  hyphens: auto;
  orphans: 3;
  widows: 3;
}
p {
  margin: 0;
  text-indent: 1.2em;
  overflow-wrap: break-word;
  word-wrap: break-word;
  word-break: break-word;
  max-width: 100%;
}
/* CRITICAL: no indent on first para after heading */
h1 + p, h2 + p, h3 + p, h1.part + p, .section-break + p {
  text-indent: 0;
}
```

### Overflow Protection (MANDATORY)

WeasyPrint does NOT break long words by default. Every build MUST include:

```css
overflow-wrap: break-word;
word-wrap: break-word;
word-break: break-word;
```

Without this, German compounds, Greek terms, and long URLs overflow the text column. This is the #1 recurring failure across all PDF builds.

## Per-Work HTML Structure

Each work gets its own HTML file with:
1. Part heading: `<h1 class="part">Part N</h1>`
2. Work title: `<h1>Work Title</h1>`
3. Metadata: `<div class="work-meta">Year — Translated by Translator</div>`
4. Body: markdown-to-HTML converted text

### Markdown → HTML Pipeline

Simple regex-based conversion (no Pandoc needed for clean source texts):
- `# h1` → `<h1>`
- `## h2` → `<h2>`
- `### h3` → `<h3>`
- `**bold**` → `<strong>`, `*italic*` → `<em>`
- `> quote` → `<blockquote>`
- `- list` → `<ul><li>`
- Double-newline-separated blocks → `<p>` paragraphs
- Pre-identify and tag section-break headings with `<div class="section-break">`

## Build Script Pattern

```
sources/           # Source texts (.txt, extracted from PDF/EPUB)
├── work_a.txt
├── work_b.txt
└── ...
build_works.py     # Main build script
├── CSS constant (shared across all works)
├── cleanup_text() — strip editorial apparatus, fix OCR artifacts
├── markdown_to_html() — simple converter
├── build_small_pdf(html, name) — per-work PDF builder
├── build_part() — wrapper that calls build_small_pdf
├── Per-work loop: read → clean → wrap in HTML → build_part
└── pdfunite merge at end
build_tmp/         # Temp per-work PDFs (deleted after merge)
```

## clean_source text() Steps (minimal but essential)

1. `strip_editorial_apparatus()` — Remove COMMENT blocks, inline footnote numbers, numbered footnotes, publisher back-matter
2. `\r\n` → `\n`, `\r` → `\n`
3. Collapse 3+ newlines → 2
4. Collapse 2+ spaces → 1
5. Fix underscore OCR artifacts: `(\w)_(\w)` → `\1 \2`
6. Remove backticks (monospace trigger in HTML)
7. Reflow one-word-per-line OCR artifacts (join consecutive short lines)
8. Break overlong paragraph lines at 300 chars (WeasyPrint chokes on 2000+ char single-line paragraphs)

## Front Matter Structure

```html
Title page:
  THE COMPLETE WORKS OF FRIEDRICH NIETZSCHE
  (subtitle, translator credits, compilation date)

Table of Contents:
  Part I — Work Title
  Part II — Work Title
  ...

Introduction:
  Framing text about the edition, translator notes,
  and editorial choices
```

## Output Stats (Nietzsche Build Reference)

- **Source texts**: 16 files (4 public domain + 12 Anna's Archive extracts)
- **Per-work PDFs**: 15 sub-PDFs (title + TOC + intro + 11 works + 2 appendix parts)
- **Merge**: `pdfunite` — takes ~2 seconds
- **Final size**: 7.8 MB for 4,402 pages
- **Font**: Liberation Serif 10pt (not 12pt — keeps line length manageable at 6×9)
- **Build time**: ~2-3 minutes on 2GB VPS

## Pitfalls Specific to This Pipeline

- **WeasyPrint OOM**: building a single HTML with all works (~5MB+ body) crashes on 2GB RAM. Always split.
- **Do NOT use DejaVu Serif** — the user perceives it as "weird fonts." Liberation Serif is the established choice.
- **Backtick bleed**: source texts with backtick ` markers cause WeasyPrint `<code>` span rendering in DejaVu Sans Mono. Strip backticks in `cleanup_text()`.
- **First para indent**: WeasyPrint applies `text-indent` to every `<p>`, including the first after a heading. Add CSS `h1 + p { text-indent: 0; }` to fix.
- **Conflicting CSS**: Some source texts contain their own inline styles from EPUB extraction. Run body text through `cleanup_text()` before HTML wrapping to strip HTML artifacts.
