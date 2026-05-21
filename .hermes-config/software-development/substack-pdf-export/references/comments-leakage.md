# Reader Comments Leakage

## Discovery

When the `substack-pdf-export` skill was first updated to use trafilatura,
step 4 recommended feeding the **full page HTML** (the entire fetched page,
including `<head>`, navigation, comment sections, etc.) to trafilatura.

This leaked reader comments into the extracted markdown.

## Example

The introduction chapter's markdown ended with:

```
...Only for historical thinking and revising there would be no place...

Whenever we see the proposition of a dichotomy - only two forces or reasons
for a complex event - no matter how well argued that proposition is, we must
ask whether there is a possibility for a third force...

Hello! Please let me know where I can download the book.
INTRODUCTION of EUROPEAN CIVIL WAR 1917-1945
```

The last three paragraphs are reader comments, not part of the chapter.

## Root Cause

trafilatura's content-detection algorithm identifies article text by analyzing
the DOM structure. On Substack pages, reader comments are rendered in `<div>`
elements within the same `<article>` container as the post body. trafilatura
correctly identifies the entire `<article>` as "content" but cannot distinguish
between the author's body and reader comments — both are text content within
the article.

## Fix

Extract `body_html` from `window._preloads` JSON first, then feed ONLY
`body_html` to trafilatura. The `body_html` field contains just the author's
article content — no comments, no page chrome.

```python
# WRONG — leaks comments
md = trafilatura.extract(full_page_html)

# RIGHT — article only
body_html = data["post"]["body_html"]  # from _preloads
md = trafilatura.extract(body_html)
```

## Detection

The easiest detection: chapters ending with informal text, questions, or
signatures that don't match the academic/professional tone of the rest of
the chapter. Reader comments are typically:
- Shorter paragraphs with informal tone
- Questions ("Where can I download...")
- Personal observations ("I think a third force...")
- Appended to the very end of the markdown output
