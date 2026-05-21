# The `\n_+.*?$` Truncation Bug

## Discovery

During a session exporting Ernst Nolte's "European Civil War 1917-1945" from
theognisomegara.substack.com, all 37 PDFs appeared "incomplete." Spot-checking
revealed chapters were silently truncated — some reduced to a single paragraph.

## Root Cause

The original `html_to_text()` function included a cleanup line meant to strip
Substack boilerplate footers (which use underscore separators):

```python
result = re.sub(r'\n_+.*?$', '', result, flags=re.DOTALL)
```

html2text converts `<em>italic text</em>` to `_italic text_`. When an italic
word appears after a line break, the regex matches from `\n_` to end-of-file
(`.*?$` with DOTALL is non-greedy but `$` forces expansion to end of string).

## Impact

Any chapter containing italic text was truncated at the first italic word.
Example: "The Great Purge and the Construction Pathos in the Soviet Union"
- body_html: 33,212 chars (4,440 words)
- after html2text + regex: 2,074 chars (~200 words)
- Lost: 93.7% of content

## Detection

The bug was silent — no errors, no warnings. Chapters appeared "short" but not
obviously broken. The user spotted it by reading the PDFs and noticing they
ended mid-content.

To check: compare `wordcount` from `_preloads` post data against the converted
text length. The Great Purge chapter had wordcount=4440 but only ~200 words in
the output — a clear sign.

## Fix

1. Remove the regex entirely. It is never safe on html2text output.
2. Strip boilerplate by targeting exact strings at PDF rendering time:
   - "Subscribe now"
   - "FUNDRAISING for this project..."
   - "Click here to navigate..."
   - "Share "
3. Prefer trafilatura over html2text — it handles boilerplate automatically.