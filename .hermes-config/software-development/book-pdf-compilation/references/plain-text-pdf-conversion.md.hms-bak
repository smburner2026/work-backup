# Plain Text → PDF via WeasyPrint

When the source is a `.txt` file (no markdown headers, no formatting), use WeasyPrint with heuristic paragraph detection rather than fpdf2.

## Paragraph Detection

Plain text files don't have markdown headings. Split on double newlines (`\n\n`) and classify each block:

- **Short blocks (≤4 lines, <120 chars)** → render as `<h2>` (likely a chapter heading, scene break, or epigraph)
- **Long blocks** → render as `<p>` with all internal newlines collapsed to spaces

```python
paragraphs = text.strip().split('\n\n')
for para in paragraphs:
    para = para.strip()
    lines = para.split('\n')
    if len(lines) <= 4 and len(para) < 120:
        html_body += f'<h2>{para}</h2>\n'
    else:
        html_body += f'<p>{para}</p>\n'
```

## Style Template

For translated book texts, use the established 6×9 / Georgia 11pt format:

```python
STYLE = """
@page {
  size: 6in 9in;
  margin: 0.9in 0.85in;
  @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 9pt; color: #555; }
}
body {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 11pt;
  line-height: 1.6;
  text-align: justify;
  hyphens: auto;
  overflow-wrap: break-word;  /* CRITICAL — prevent word overflow */
}
h1 { font-size: 18pt; text-align: center; margin-top: 1.5em; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 14pt; margin-top: 1.2em; text-align: center; }
p { margin: 0.3em 0; text-indent: 1.5em; }
p:first-of-type { text-indent: 0; }
"""
```

## Pitfalls

- **No italic markers in plain text** — book titles, foreign phrases, emphasis all render roman. This is a source limitation, not fixable without manual markup.
- **Short-line detection can misclassify** — a very short paragraph (e.g. a two-line epigraph) will get rendered as an `<h2>` heading. Inspect output and adjust the threshold if needed.
- **`overflow-wrap: break-word` is critical** — WeasyPrint does not break long words by default. Without it, any word wider than the column (long German compounds, chemical names, URLs) overflows into the margin. Always include this in the CSS.
- **Text-indent on first paragraph** — CSS `p:first-of-type { text-indent: 0; }` prevents indenting the very first paragraph of a section, which looks amateurish.
