# Substack Unofficial API Endpoints

Discovered via browser DevTools and empirical testing (May 2026). All endpoints are internal/undocumented — no guarantees of stability.

## Authentication

All endpoints below that require auth use the **`connect.sid`** cookie:

```
connect.sid=s%3A<hex>.<signature>
```

Extracted from browser DevTools → Application → Cookies → `substack.com`. Valid for months unless user signs out. Rotate by signing out and back in.

The cookie works on **publication-specific subdomains** (`{pub}.substack.com`) but the main `substack.com` API requires additional CSRF/XSRF headers (hard to replicate from CLI).

## Publication Endpoints

### `/api/v1/archive`
```
GET https://{pub}.substack.com/api/v1/archive?sort=new&offset={N}&limit=20
```
Returns array of post metadata objects. Each object has: `slug`, `title`, `id`, `post_date`, `audience`, `type`, `wordcount`, etc. The `body_html` field is **always empty** in archive responses — full content requires fetching each post page individually.

Pagination: ~20-30 posts per page. Use offset increments of 20.

Auth: not strictly required (public posts visible), but with `connect.sid` cookie the archive includes paywalled posts the user has access to.

Custom domains: The archive endpoint only works via the substack subdomain redirect chain. Hit `{pub}.substack.com/api/v1/archive` and follow the 301 redirect to the custom domain. Direct hits to the custom domain archive endpoint return 404.

**Important**: This endpoint is NOT the same as `/api/v1/posts` (which searches globally and often returns wrong results).

### `/api/v1/posts`
```
GET https://{pub}.substack.com/api/v1/posts?slug={slug}
```
⚠️ **Do not use.** Searches globally across ALL Substack posts, often returns wrong/first-match-only results. Use `window._preloads` from the individual page HTML instead.

## Individual Article Endpoints

### Page HTML (via redirect)
```
GET https://{pub}.substack.com/p/{slug}
```
Returns full page HTML with embedded `window._preloads` JSON. This is the primary extraction method for article content.

Auth: with `connect.sid` → returns full `body_html` for paywalled content.
Auth: without → returns truncated preview for gated articles.

Custom domain redirect: follows same pattern as archive. Use substack subdomain → follow 301.

Multi-page articles: checked via `post_page_count` in _preloads. Remaining pages at `/p/{slug}?page={N}`.

### `/api/v1/feed`
```
GET https://{pub}.substack.com/feed
```
RSS/Atom feed. Works without auth. Contains full article HTML for **free** posts but only excerpts/metadata for paywalled. Useful as a secondary source but not for paywalled content.

## Substack.com Endpoints (require CSRF)

These live on the main `substack.com` domain. All return 403 with just the `connect.sid` cookie — they need additional CSRF tokens or headers.

| Endpoint | Method | Purpose | Status |
|---|---|---|---|
| `/api/v1/user/me` | GET | Current user profile | 403 without CSRF |
| `/api/v1/me` | GET | Alias | 404 |
| `/api/v1/subscriptions?tvOnly=false` | GET | List subscribed publications | 200 but returns empty for most users |
| `/api/v1/reader/feed` | GET | Notes feed (Substack's Twitter-like) | 200, returns items with user/publication data |
| `/api/v1/reader/home` | GET | Reader home | 404 |
| `/api/v1/reader/subscriptions` | GET | Reader subscriptions | 404 |

### Working discovery: `/api/v1/subscriptions`
```
GET https://substack.com/api/v1/subscriptions?tvOnly=false
```
When it works, returns:
```json
{
  "subscriptions": [],
  "publications": [{"id": N, "name": "...", "subdomain": "..."}]
}
```
For most users this returns empty `subscriptions` and only the default "Substack Post" in `publications`. The `tvOnly` parameter accepts `true`/`false`/`1`/`0` but doesn't change results.

Alternative discovery method: Parse `window._preloads` from the main `substack.com/` page. It contains `currentUser.status.paidPublicationIds` — an array of publication IDs the user has paid for. These can't be looked up by ID via API, but you can match them to known publications by checking the home page's preloads or by the publication's `id` field in archive responses.

## Page HTML — window._preloads

Every Substack page embeds post data in a `<script>` tag:

```html
<script>
window._preloads = JSON.parse("{\"post\": {...}, \"currentUser\": {...}, ...}");
</script>
```

Extraction (Python):
```python
import re, codecs, json

m = re.search(r'window\._preloads\s*=\s*JSON\.parse\(\s*"(.*?)"\s*\)', html)
data = json.loads(codecs.decode(m.group(1), "unicode-escape"))
post = data.get("post", {})
```

Key fields in `post`:
| Field | Type | Description |
|---|---|---|
| `body_html` | str | Full article HTML. Empty in archive, populated on per-page fetch |
| `title` | str | Article title |
| `slug` | str | URL slug |
| `audience` | str | `"everyone"`, `"only_paid"`, or `"founding"` |
| `type` | str | `"newsletter"`, `"podcast"`, etc. |
| `post_page_count` | int | Number of pages (multi-page articles) |
| `publication_id` | int | Publication identifier |
| `podcast_url` | str | Audio URL for podcast-type posts |
| `wordcount` | int | Word count (often unreliable for podcasts) |

## Known gotchas

- **`body_html` null**: Older posts (pre-2022) may have `body_html: null`. Fall back to extracting `<article>` tag from the raw HTML and feeding to trafilatura.
- **Podcast-type posts**: `body_html` contains only show notes (~200-600 chars), not full article text. The actual content is audio at `podcast_url`.
- **Rate limits**: No documented limit, but be conservative (~1 req/sec). Archive endpoint ≈ 300ms between calls is fine; article pages need 500ms+.
