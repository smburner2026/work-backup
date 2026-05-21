# Chapter Validation: Cross-Referencing Against TOC

The most common failure in Substack book exports is missing chapters due to manual slug curation. Here's the validation workflow:

## 1. Find the TOC page

Many book-translation publications have a dedicated Table of Contents post. Search for it:

```python
# Scan archive for TOC-like titles
for post in all_posts:
    title = post['title'].lower()
    if any(w in title for w in ['table of contents', 'toc', 'contents', 'chapters']):
        toc_slug = post['slug']
        break
```

## 2. Extract all chapter links from TOC

```python
html = fetch_page(f"https://{pub}.substack.com/p/{toc_slug}")
body_html, _ = extract_post_data(html)
links = re.findall(r'href="(?:https://{pub}\.substack\.com)?/p/([^"?#]+)', body_html)
chapter_slugs = list(dict.fromkeys(links))  # deduplicate, preserve order
```

Note: the TOC post slug itself and comment links will be in the list — filter those out.

## 3. Diff against your curated set

```python
toc_set = set(chapter_slugs)
curated_set = set(YOUR_SLUGS)

missing = toc_set - curated_set
extra = curated_set - toc_set

if missing:
    print(f"MISSING from curated set: {missing}")
if extra:
    print(f"IN curated set but not in TOC: {extra} — verify these are chapters")
```

## Known failure from the Nolte export

The slug `the-failure-of-the-anti-communist` (title: "The Failure of the Anti-Communist and Anti-Fascist Concepts in Great European Politics") was missed because the title doesn't contain obvious Nolte/European Civil War keywords. It was only discovered by scanning all archive titles for topic-relevant patterns.
