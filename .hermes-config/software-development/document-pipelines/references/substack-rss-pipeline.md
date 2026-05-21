# Substack RSS Content Pipeline

Substack-specific details for extracting article content via RSS and generating PDFs.

## Feed URL

```
https://<publication>.substack.com/feed
```

Returns RSS 2.0 with full article HTML in `<content:encoded>` CDATA sections. The feed includes the most recent ~20 posts.

## HTML Content Structure

The `<content:encoded>` HTML from Substack's RSS feed contains the **full article body** including:

- `<p>` tags for paragraphs
- `<div class="captioned-image-container">` with embedded images and captions
- `<div class="preformatted-block">` with `<pre>` text blocks
- Footnotes via `<a class="footnote-anchor">` and `<sup>` tags
- `<figcaption>` elements under images
- Subscribe/paywall buttons via `<p class="button-wrapper">`

**Image tags and captions** — the RSS includes full image HTML with `<picture>` elements, `<source>` sets, and `<img>` tags with `srcset`. These should be stripped when extracting clean text. Captions inside `<figcaption>` are mixed with images and sometimes contain relevant text.

## Clean Text Extraction for Substack

```python
def substack_html_to_text(html_content: str) -> str:
    """Extract clean article text from Substack RSS content:encoded."""
    import re, html
    
    # Remove image blocks entirely (they dominate the HTML)
    html = re.sub(r'<div class="captioned-image-container">.*?</div>', ' ', html_content, flags=re.DOTALL)
    html = re.sub(r'<div class="image2-inset">.*?</div>', ' ', html, flags=re.DOTALL)
    html = re.sub(r'<figure>.*?</figure>', ' ', html, flags=re.DOTALL)
    
    # Remove button/subscribe blocks
    html = re.sub(r'<p class="button-wrapper">.*?</p>', ' ', html, flags=re.DOTALL)
    
    # Remove preformatted blocks but keep their inner text
    html = re.sub(r'<div class="preformatted-block">.*?<pre class="text">(.*?)</pre>.*?</div>', r'\1', html, flags=re.DOTALL)
    
    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    
    # Unescape HTML entities
    text = html.unescape(text)
    
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

## TOC (Table of Contents) Pages

Substack TOC pages are JS-rendered (the `<div class="available-content">` is populated by client-side JavaScript). **Do not attempt to scrape the TOC page for links** — instead, use the RSS feed which lists all articles with their direct URLs, or the Substack API for the full archive.

The RSS feed URL for any Substack is always `https://<name>.substack.com/feed` — the TOC page is just the article that serves as an index, but the actual article links are in the feed.

**Important caveat:** The RSS feed only returns the **most recent ~20 posts**. For publications with dozens or hundreds of articles, you need the Substack API to get the full list.

## Full Archive via Substack API

To get ALL posts (not just the latest 20 from RSS):

```
GET https://<pub>.substack.com/api/v1/archive?sort=new&offset=N
```

- `offset=0` returns the most recent ~23 posts
- `offset=20` returns the next ~30 (overlap is fine — dedup by slug)
- `offset=40`, `offset=60` — continue until the response is empty or non-list
- Pagination stops reliably at ~offset=60 (about 80-100 total posts for most publications)

Each post object from the API contains `slug`, `title`, `post_date`, `id`, but `body_html` is often **null for older posts**. Do NOT use the slug-based endpoint (`/api/v1/posts?slug=...`) — it searches globally and returns the WRONG post (the most recent match, not the one you asked for).

## Individual Page Extraction (window._preloads)

When the archive API returns empty `body_html` for older posts, extract the content from each individual article's HTML page. Substack embeds the full post data in a JavaScript variable:

```python
import re, json, codecs, urllib.request

def fetch_substack_article(slug: str) -> str:
    """Fetch full article HTML body from a Substack page."""
    url = f"https://<pub>.substack.com/p/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=30)
    html = resp.read().decode("utf-8", errors="replace")
    
    # Extract the JSON from window._preloads
    match = re.search(r'window\._preloads\s*=\s*JSON\.parse\(\"(.*?)\"\)', html)
    if not match:
        raise ValueError("Could not find window._preloads")
    
    escaped = match.group(1)
    unescaped = codecs.decode(escaped, "unicode_escape")
    data = json.loads(unescaped)
    
    # Navigate to post data
    if "post" in data:
        post = data["post"]
    else:
        # Search recursively for a dict with body_html
        for key, val in data.items():
            if isinstance(val, dict) and "body_html" in val:
                post = val
                break
        else:
            raise ValueError("Could not find post data")
    
    body_html = post.get("body_html", "")
    return body_html
```

This works for ALL articles regardless of age — the `window._preloads` data is embedded server-side in every Substack article page.

## HTML to Clean Text for Substack

Two approaches:

### 1. html2text (recommended for Substack)

```bash
pip3 install --break-system-packages html2text
```

```python
import html2text, html as html_mod, re

def substack_html_to_text(body_html: str) -> str:
    text = html_mod.unescape(body_html)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    
    h = html2text.HTML2Text()
    h.body_width = 0       # no line wrapping
    h.ignore_links = True   # strip hyperlinks
    h.ignore_images = True  # strip images
    h.ignore_emphasis = False
    h.skip_internal_links = True
    h.unicode_snob = True   # preserve Unicode
    h.single_line_break = True
    
    result = h.handle(text)
    result = re.sub(r'\n{4,}', '\n\n\n', result)  # collapse excessive blanks
    return result.strip()
```

### 2. Regex-based (fast, no dependencies)

```python
import re, html

def substack_html_to_text_fast(html_content: str) -> str:
    html = re.sub(r'<div class="captioned-image-container">.*?</div>', ' ', html_content, flags=re.DOTALL)
    html = re.sub(r'<figure>.*?</figure>', ' ', html, flags=re.DOTALL)
    html = re.sub(r'<p class="button-wrapper">.*?</p>', ' ', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

## PDF Generation with fpdf2 + DejaVu

```bash
pip3 install --break-system-packages fpdf2
```

```python
from fpdf import FPDF

def article_to_pdf(text: str, title: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    
    max_width = pdf.w - pdf.l_margin - pdf.r_margin
    
    def sanitize(line):
        # Strip zero-width Unicode chars that fpdf2 can't render
        for ch in '\u200b\u200c\u200d\u2060\ufeff':
            line = line.replace(ch, '')
        return line
    
    # Title
    pdf.set_font("DejaVu", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(5)
    
    # Body
    pdf.set_font("DejaVu", "", 10)
    lines = text.split('\n')
    for line in lines:
        if pdf.get_y() > 270:
            pdf.add_page()
            pdf.set_font("DejaVu", "", 10)
        
        line = sanitize(line.strip())
        if not line:
            pdf.ln(3)
            continue
        
        # Word-wrap manually for lines wider than page
        words = line.split()
        buf = ""
        for word in words:
            test = (buf + " " + word).strip()
            if pdf.get_string_width(test) > max_width and buf:
                pdf.multi_cell(0, 5, buf)
                buf = word
            else:
                buf = test
        if buf:
            pdf.multi_cell(0, 5, buf)
    
    pdf.output(output_path)
```

## Full Pipeline: All Nolte Chapters for a Substack Publication

For extracting an entire Substack publication's archive:

```python
import json, time, os

def get_all_posts(pub_slug: str) -> list[dict]:
    """Fetch all posts from a Substack via paginated API."""
    all_posts = []
    for offset in range(0, 100, 20):
        url = f"https://{pub_slug}.substack.com/api/v1/archive?sort=new&offset={offset}"
        resp = urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=15
        )
        data = json.loads(resp.read().decode())
        if not isinstance(data, list) or len(data) == 0:
            break
        all_posts.extend(data)
        time.sleep(0.3)
    return all_posts

def identify_nolte_chapters(posts: list[dict]) -> list[dict]:
    """Filter posts to Nolte European Civil War chapters."""
    # Known non-Nolte content (poems, film reviews, guest posts, etc.)
    non_nolte = {
        # Full list of slugs that are NOT Nolte chapters
    }
    return [p for p in posts if p.get('slug', '') not in non_nolte]
```

## Multi-Publication Handling

If articles link to other Substack publications beyond the original one, fetch each publication's separate RSS feed. Cross-links between Substacks are common in shared-author networks.

## Title Sanitization for Filenames

Substack article slugs can be long. For filenames:

```python
def slug_to_filename(link: str) -> str:
    slug = link.rsplit("/", 1)[-1]
    # Shorten if over 60 chars
    return slug[:60]
```

## Known Substack Article IDs

Substack articles use short URL slugs like:

```
https://<pub>.substack.com/p/the-table-of-contents
https://<pub>.substack.com/p/movie-review-eddington
https://<pub>.substack.com/p/thousand-days-fragments-of-a-soldierss
```

The slug is at the end of the `p/` path. Some slugs have appended hash/disambiguation characters (e.g., `soldiers-47c`, `soldiers-d0e`) for parts of multi-article series.