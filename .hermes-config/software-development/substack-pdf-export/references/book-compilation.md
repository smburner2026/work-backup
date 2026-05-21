# Book Compilation: ToC Extraction & Chapter Ordering

## Getting the canonical chapter order

The Substack archive API returns posts in reverse chronological order by publication date. For a book translation published as a serial, this is NOT the correct book order. 

The canonical order lives on the publication's dedicated Table of Contents page. This is typically a post whose title is the book title (e.g. "ERNST NOLTE'S EUROPEAN CIVIL WAR 1917-1945") with subtitle "TABLE OF CONTENTS".

### Extracting the ToC

Fetch the ToC page and extract all chapter links from `body_html` in `window._preloads`:

```python
import re, json, urllib.request

# Find the ToC slug first
# The correct slug is not always obvious — e.g. ernst-noltes-european-civil-war-1917 not -917

html = ... # page HTML
m = re.search(r'"body_html"\s*:\s*"((?:[^"\\]|\\.)*?)"', html)
body_html = m.group(1).encode().decode('unicode_escape')

# Extract all chapter links
links = re.findall(
    r'<a[^>]*href="https?://theognisomegara\.substack\.com/p/([^"?]+)[^"]*"[^>]*>(.*?)</a>',
    body_html, re.DOTALL
)

for slug, anchor_text in links:
    clean = re.sub(r'<[^>]+>', '', anchor_text).strip()
    print(f'{slug}  |  {clean}')
```

The anchor text typically contains the chapter/section label (e.g. "Chapter 2 Section 3 here", "the preface here", "the conclusion here"). Use these to build the canonical ordering.

### When the ToC slug is wrong

The ToC page URL may return 404 if you have the wrong slug. Search for it by crawling the archive:

```python
for post in archive_posts:
    if 'ernst nolte' in post['title'].lower() or 'civil war' in post['title'].lower():
        print(post['slug'], post['title'])
```

### Section numbering pattern

Multi-section chapters use consistent labeling:
- Chapter II: 10 sections (2.1–2.10) 
- Chapter III: 9 sections (3.1–3.9)
- Chapter IV: 8 sections (4.1–4.8)
- Chapter V: 5 sections (5.1–5.5)

Single-section chapters: Chapter I, Introduction, Preface, Conclusion.

## When body_html is null

Some older Substack posts (especially pre-2022, like prefaces that were the first post ever made) serialize `body_html: null` in the `window._preloads` data. The content exists only in the rendered `<article>` HTML tag.

Fallback extraction:
```python
m = re.search(r'<article[^>]*>(.*?)</article>', page_html, re.DOTALL)
if m:
    article_html = m.group(1)
    md = trafilatura.extract(article_html, output_format='markdown', ...)
```

## PDF rendering pitfall: long single-word overflow

fpdf2's `cell()` method does NOT wrap text. If a single word (URL, long hyphenated term, etc.) is wider than the page, `cell()` draws past the right margin. This is common in footnotes with long URLs and in appendices with citations.

**Fix**: Before accumulating words into a justified line, check `get_string_width(word)` against `line_width`. If a word is wider than the page, flush any buffered text with `write_justified_line()`, then render the long word via `multi_cell()` (which wraps), and reset the buffer.

```python
word_w = self.get_string_width(word)
if word_w > line_width:
    if line_buf:
        self.write_justified_line(line_buf, line_width)
    self.multi_cell(line_width, LEADING, word)
    line_buf = ""
    continue
```

Also use `self.l_margin` instead of hardcoded `MARGIN` in `write_justified_line` for consistency when margins change.

## Markdown title extraction: 8-pattern priority chain

Substack-exported book chapters have wildly inconsistent title formats. The extractor must try patterns in order, with each handling one format:

1. `^#\s+(.+)$` — hash heading (standard markdown)
2. `^\*\*(\d+\.\s+[^*]+?)\*\*` — bold + section number (e.g. `**1. Title**`)
3. `^(\d+\.\s+[A-Z][^.\n]+?)(\.?\n\n|\.\s+\n)` — plain numbered section (e.g. `3. Title` with no bold)
4. `^\*\*(?!\[)(?!Chapter\s+[IVXLCDM])(?!\s*[IVXLCDM]+\s)(.+?)\*\*` — unnumbered bold title, but NOT chapter headings, translator notes, or Roman-numeral chapter heads
5. `^Chapter\s+[IVXLCDM]+\s*[.:]\s*(.*)$` — "Chapter III: ..." style
6. `^\*\*([IVXLCDM]+\s+[A-Z][^*]+?)\*\*` — bold Roman-numeral chapter head  
7. `^[IVXLCDM]+\.\s+\d+\.\s+(.*)$` — "IV. 2. Title" chapter.section format
8. First substantive standalone line (15-150 chars, uppercase start, no bold/italic/bracket prefix)

After extraction, `clean_title()` strips leading Roman numerals, section numbers, trailing periods, and normalizes whitespace.

**Key pitfalls**:
- Missing `re.MULTILINE` flag causes bold titles on later lines to never match
- The `**Chapter V.**` heading must be skipped (negative lookahead) so the actual section title (`**The Attack Against...**`) is picked up
- Translator notes like `**[...]**` must be excluded (start with `[`)
- Fallback to slug name creates ugly titles like "the-period-of-stabilization-of-the"

## Subsection heading rendering

Don't skip `##` and `###` lines — render them as bold section headers:

- `##` headings → centered, FONT_SIZE + 2, bold, dark gray
- `###` headings → left-aligned, FONT_SIZE, bold, dark gray

Strip any remaining `**bold**` markers from the heading text before rendering.

## Boilerplate stripping at compile time

Before passing markdown to `write_body()`, strip:
- The extracted title line (exact match with the cleaned title, tried in multiple formats)
- Italic preface notes: `^\*[^*]+\*(\n\n)*` — "This chapter previously appeared on..."
- Standalone Chapter heading lines: `^Chapter\s+[IVXLCDM]+\s*[.:].*$`
- Bold Roman-numeral chapter heads: `^\*\*[IVXLCDM]+\s+[A-Z][^*]*?\*\*\s*$`

This avoids redundant text (the chapter title page already displays the chapter/section label).

## Title casing for chapter/section headings

Apply standard English title case to all extracted titles via `to_title_case()`. Implements Chicago-style rules with proper noun awareness:

- **First and last word always capitalized** (even if a minor word like "the" or "of")
- **Proper nouns always capitalized** via an `always_cap` set (Bolshevik, Soviet, Hitler, Stalin, Communist, European, Röhm, Weimar, Reich, Volkgemeinschaft, etc.)
- **Minor words lowercased** (articles: a/an/the, prepositions: in/of/to/with/from/between/towards/against, conjunctions: and/but/or/for)
- **All other words capitalized**
- **ALL-CAPS preserved as-is** (e.g. "STATEMENT TO MY READERS")
- **Punctuation handling**: use `lstrip`/`rstrip` to properly separate leading/trailing punctuation from the core word, avoiding the double-first-letter bug that occurs with `w[:len(w)-len(clean_word)]` arithmetic

```python
def to_title_case(text):
    minor_words = {"a", "an", "the", "and", "but", "or", "in", "of", "to",
                   "with", "by", "at", "from", "as", "into", "onto", "upon",
                   "on", "off", "over", "under", "through", "between",
                   "against", "within", "without", "along", "among",
                   "about", "after", "before", "behind", "below", "beneath",
                   "beside", "beyond", "down", "during", "except", "inside",
                   "near", "past", "since", "throughout", "toward", "towards",
                   "via", "vs"}
    always_cap = {"bolshevik", "bolshevism", "soviet", "hitler", "stalin",
                  "lenin", "communist", "national", "socialist", "nazi",
                  "fascist", "marxist", "russian", "germany", "european",
                  "weimar", "reich", "volgkgemeinschaft", "röhm", "kirov",
                  "furet", "nolte", "jewish", "holocaust", "auschwitz",
                  "gulag", "anti-bolshevism", "anti-communist", "anti-fascist",
                  "anti-marxist"}

    if text.isupper():
        return text

    words = text.split()
    result = []
    for i, w in enumerate(words):
        stripped = w.strip('""''"".,:;!?—–-()[]{}«»‹›')
        lead_punct = w[:len(w) - len(w.lstrip('""''"".,:;!?—–-()[]{}«»‹›"'))]
        trail_punct = w[len(w.rstrip('""''"".,:;!?—–-()[]{}«»‹›"')):]

        if not stripped:
            result.append(w)
            continue

        if i == 0 or i == len(words) - 1:
            core = stripped[0].upper() + stripped[1:]
        elif stripped.lower() in always_cap:
            core = stripped[0].upper() + stripped[1:]
        elif stripped.lower() in minor_words:
            core = stripped.lower()
        elif re.match(r'^\d', stripped):
            core = stripped
        else:
            core = stripped[0].upper() + stripped[1:]

        result.append(lead_punct + core + trail_punct)
    return " ".join(result)
```

**Test all titles after adding new always_cap entries** — missing proper nouns result in ugly lowercase where uppercase is expected.

## Inline formatting: bold→italic mapping

In academic texts from Substack, `**bold**` markers are typically used for emphasis/foreign terms that should render as italic in the final PDF. The body text parser should:

| Markdown | Rendered style |
|---|---|
| `*text*` | italic |
| `**text**` | italic (NOT bold — academic convention) |
| `***text***` | bold italic |

Standalone `**title lines**` remain as bold (handled by chapter title pages, not `write_body`).

Implementation: use `tokenize_inline()` to split text into styled segments, then `_style_to_font()` maps `{"B": "I", "I": "I", "BI": "BI"}`. Each word in a line is rendered with its per-word font, allowing justified lines with mixed styles. The `write_paragraph` method has two code paths: a fast path for unformatted text (`_write_plain_paragraph`) and a styled path for text with inline markers.

```python
def tokenize_inline(self, text):
    """Split into (text, style) tokens: ***bolditalic***, **bold**, *italic*"""
    tokens = []
    pattern = r'(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*)'
    last = 0
    for m in re.finditer(pattern, text):
        if m.start() > last:
            tokens.append((text[last:m.start()], ""))
        if m.group(1).startswith("***"):
            tokens.append((m.group(2), "BI"))
        elif m.group(1).startswith("**"):
            tokens.append((m.group(3), "B"))  # mapped to I by _style_to_font
        else:
            tokens.append((m.group(4), "I"))
        last = m.end()
    if last < len(text):
        tokens.append((text[last:], ""))
    return tokens
```

## Hierarchical Table of Contents

Flat TOC listings (all entries at the same indentation) are hard to scan. Generate a hierarchical TOC by grouping entries into three tiers:

1. **Front matter**: Preface, Introduction (standalone `Label:` entries with italic titles)
2. **Chapter groups**: Chapter I–V with display titles from `CHAPTER_FULL_NAMES` and indented sections underneath (italic, `Section N:` prefix)
3. **Back matter**: Conclusion, Letter, Appendix (standalone entries)

```python
CHAPTER_FULL_NAMES = {
    "Chapter I": "Chapter I — Final Point and Prelude 1933:\nThe Anti-Marxist Seizure of Power in Germany",
    "Chapter II": "Chapter II — Looking Back in the Years 1917–32:\nCommunists, National Socialists, Soviet Russia",
    ...
}
```

Grouping logic: entries with "Chapter" but no "Section" in their label are chapter heads; entries with "Section" belong under their parent chapter (split label on comma); everything else is standalone. Render in fixed chapter order (`[Chapter I, Chapter II, ...]`), not dict insertion order.

## Recommended font settings for book PDF

- **Body font size**: 12pt with 6.5pt leading for comfortable reading. Older scripts used 11pt / 5.5pt — that's too small for on-screen or printed book use.
- **Chapter title**: 16pt bold, centered
- **Section label**: 11pt italic, centered
- **Page number / running header**: 8pt italic, gray (#787878)
- **Font**: Liberation Serif from `fonts-liberation2` package.

## Book compilation script

See `scripts/compile_book.py` for the updated bound-volume compiler. Features:
- Liberation Serif (Times New Roman equivalent) — install `fonts-liberation2`
- Justified text with proper word-spacing, handles long-word overflow
- Title page with decorative rule
- Table of Contents generated from chapter labels
- Each chapter starts on a new page with centered heading + section label + decorative rule
- Running headers showing current chapter
- Page numbers centered at bottom
- Bold/italic preserved
- Blockquotes indented in gray italic
- Subsection headings (`##` / `###`) rendered as bold section titles
- Title extraction from diverse markdown formats (8 fallback patterns)
- Boilerplate stripped: preface notes, Chapter heading lines, subscribe banners
