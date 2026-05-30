---
name: substack-paywall-export
description: Fetch and export paywalled Substack articles and podcast audio from newsletters you subscribe to. Uses browser session cookie (connect.sid) for authenticated access. Extracts full article content via window._preloads, saves as markdown, generates PDFs, and downloads podcast audio from RSS feed enclosures.
---

# Substack Paywall Export

Export paywalled Substack articles and podcast audio from newsletters you're subscribed to. Built on the base `substack-pdf-export` skill but adds cookie-based authentication, subscription discovery, custom domain handling, bulk fetch, and audio download.

## When to use

- You're subscribed to a paid Substack newsletter and want to archive articles locally
- You want to batch-download all posts from a publication you have access to
- You need programmatic access to paywalled content you're entitled to read
- You want to download podcast audio episodes from a Substack publication

## Related Skills

- **`substack-pdf-export`** — Base Substack export skill for free/public articles. Same extraction pipeline, no auth. Use for publications where all content is free. This skill extends it with auth, subscription discovery, custom domain handling, bulk fetch, and audio download.

## Prerequisites

```bash
pip3 install --break-system-packages requests trafilatura fpdf2
```

## Quick Start

```bash
# Symlink the CLI
ln -sf ~/.hermes/skills/software-development/substack-paywall-export/scripts/stash_cli.py ~/.local/bin/stash
# Ensure ~/.local/bin is in PATH
export PATH="$HOME/.local/bin:$PATH"
# Or add to ~/.bashrc: export PATH="$HOME/.local/bin:$PATH"

# Set up auth
stash auth --cookie "s%3A..."

# Add a publication
stash pubs --add bronzeagepervert

# Fetch everything
stash fetch bronzeagepervert --limit 50

# Export articles
stash export bronzeagepervert --format both
```

## Cookie Setup

The skill uses your Substack session cookie (`connect.sid`) for authentication.

### Getting the cookie

**Chrome/Edge/Brave:** DevTools (F12) → Application → Cookies → substack.com → copy `connect.sid` value
**Firefox:** DevTools (F12) → Storage → Cookies → substack.com → copy `connect.sid` value

### Saving it

```bash
# Using the CLI tool
stash auth --cookie "s%3A..."
```

Or manually create `~/.hermes/config/substack_auth.json`:
```json
{"cookie": "connect.sid=s%3A..."}
```

The cookie file is stored at `~/.hermes/config/substack_auth.json` with mode 600. It stays valid for months unless you sign out.

### Security rules
- **Never pass connect.sid in shell commands** — it gets saved to shell history. Always use the JSON config file or `stash auth --cookie`
- Only use your own cookie from your own authenticated session
- Rotate by signing out and signing back in

## Workflow

### 1. Auth check + list your subscribed publications

```bash
stash auth          # Validate cookie, show account info
stash pubs          # Auto-discover subscribed pubs (from API + profile scan)
stash pubs --add "pubname"   # Manually add a publication
stash pubs --remove "pubname"  # Remove one
```

Auto-discovery is unreliable — Substack's internal API often returns empty lists. The most reliable method is adding publication names manually. See `references/api-endpoints.md` for discovery techniques.

### 2. Fetch articles from a publication

```bash
stash fetch <pub>              # Fetch all articles (archive pages)
stash fetch <pub> --since 2025-01-01   # Only articles since a date
stash fetch <pub> --limit 50           # Limit to N most recent
stash fetch --all               # Fetch all known pubs
stash fetch <pub> --force       # Re-fetch even if cached locally
```

Publication names accept:
- **Bare subdomain**: `theognisomegara` → resolves to `{pub}.substack.com`
- **Custom domain**: `bronzeagepervert.yoga` or `www.bronzeagepervert.yoga` → handles www/non-www variant auto-detection
- **Full URL**: `https://example.substack.com` → strips protocol

When a custom domain is given, the stash CLI tries both www and non-www variants automatically. The primary entry point is always the substack subdomain redirect chain (see `references/custom-domains-and-redirects.md`).

### 3. Export as text/PDF

```bash
stash export <pub> --format md          # Export all as markdown
stash export <pub> --format pdf         # Export all as text-only PDF
stash export <pub> --format both        # Both (default)
stash export <pub> --slug "post-title"  # Single article
stash list <pub>                        # List what's been fetched
```

### 4. Download podcast audio

```bash
# Podcast audio is accessible from the publication's RSS feed:
#   {pub}.substack.com/feed
# Enclosure URLs follow this pattern:
#   https://api.substack.com/feed/podcast/{post_id}/{hash}.mp3
# These are downloadable with the auth cookie.

# Manual download (find the post_id first):
curl -s -L -o episode.mp3 \
  -H "Cookie: $(cat ~/.hermes/config/substack_auth.json | python3 -c 'import sys,json;print(json.load(sys.stdin)[\"cookie\"])')" \
  "https://api.substack.com/feed/podcast/{post_id}/{hash}.mp3"
```

**Important**: The RSS feed gives the **public preview** (typically ~51 min). The **full episode** (sometimes 2hr+) is behind additional auth — the direct `/src` endpoint for the full upload ID returns 401. The full podcast access may require a separate subscription tier or additional authorization beyond `connect.sid`.

To find a podcast episode's enclosure URL:
```bash
curl -s "https://bronzeagepervert.substack.com/feed" | grep -oP 'enclosure[^>]+url="([^"]+)"'
```

### 5. Cache management

```bash
stash status                # Show download cache status
stash clean                 # Clean export artifacts (keep raw content)
```

## How It Works

### Authentication

The `connect.sid` cookie authenticates requests to Substack's API. When making requests to publication-specific endpoints (archive list, individual posts), the server returns the **full article content** for paywalled posts when authenticated — the same `window._preloads` extraction method as the base skill, but with the auth cookie attached.

**Critical**: `requests.Session()` must be used instead of `urllib.request` because `urllib` strips Cookie headers on cross-domain redirects (custom domains). The `stash` CLI uses `requests` internally.

### Content Extraction

Same pipeline as `substack-pdf-export`:
1. Fetch archive list from archive API (with auth cookie)
2. For each post, fetch individual page HTML
3. Extract `window._preloads` JSON → `body_html`
4. Convert HTML to clean markdown via **trafilatura** (preferred) or html2text
5. Optionally generate text-only PDF via fpdf2

### Publication Discovery

Three methods:
1. **API-based**: Hits `substack.com/api/v1/subscriptions` to find subscribed pubs — often returns empty
2. **Profile-based**: Scans the authenticated user's profile for `paidPublicationIds` and resolves them
3. **Manual**: User adds publications by name (most reliable)

### Custom Domain Handling

When a publication uses a custom domain (e.g. `bronzeagepervert.yoga` instead of `bronzeagepervert.substack.com`):

1. Always use the **substack subdomain** as the primary entry point — it carries auth and redirects to the custom domain
2. Direct hits to the custom domain's API endpoints return **404** — the redirect chain is required
3. Try both **www** and **non-www** variants — some domains require the `www.` prefix
4. **`requests.Session` preserves cookies across the redirect** — `urllib.request` strips them (this is the #1 failure mode)

See `references/custom-domains-and-redirects.md` for the full mechanics.

### Podcast Audio

Podcast episodes on Substack have a specific data structure:

```json
{
  "type": "podcast",
  "audience": "only_paid",
  "body_html": "<p>Short show notes (200-600 chars)</p>",
  "podcast_url": "https://api.substack.com/api/v1/audio/upload/{preview_upload_id}/src",
  "podcastUpload": {
    "id": "{preview_upload_id}",
    "name": "EPISODE216PUBLIC.mp3",
    "duration": 3063,
    "primary_file_size": 49010219,
    "is_free_preview": true,
    "full_podcast_info": {
      "media_upload_id": "{full_episode_upload_id}",
      "duration": 6128
    }
  }
}
```

- The `podcast_url` and RSS feed enclosure always point to the **free preview** (~51 min)
- The `full_podcast_info.media_upload_id` points to the **full episode** (~2 hrs) but `/src` endpoint returns 401 — properly gated
- **body_html is short** for podcast episodes (just show notes) regardless of auth status — the real content is audio

## PDF Generation Quality

The export PDF generator must produce **clean paragraph separation** and **justified text** — not raw line-wrapping. The user explicitly rejected single-line rendering that squishes paragraphs together.

### Requirements for PDF output:

1. **Paragraph-aware rendering**: Split markdown by `\n\n` (double newlines), not every `\n`. Rejoin lines within a paragraph into one text block before rendering.
2. **Justified text**: Multi-word paragraphs should use word-spacing justification, not left-aligned ragged text.
3. **Proper paragraph spacing**: `pdf.ln(4)` between paragraphs, not `pdf.ln(2)`.
4. **Heading handling**: `#` headings rendered bold, centered, with appropriate font size (14pt title, 12pt heading, 10pt body).
5. **Sanitize Unicode**: Strip zero-width chars (U+200B etc.), replace fancy quotes/dashes with ASCII equivalents.

The `stash export --format pdf` command uses the improved paragraph-aware renderer. If custom PDF generation is needed (e.g. for book compilation with TOC), use `substack-pdf-export`'s `scripts/compile_book.py` which has Liberation Serif, Chicago title case, and hierarchical TOC support.

### Common PDF quality issues and fixes

| Issue | Cause | Fix |
|---|---|---|
| Paragraphs squished | `pdf.ln(2)` between paragraphs | Change to `pdf.ln(4)` + rejoin lines into blocks |
| Mid-paragraph breaks | Splitting on every `\n` | Split on `\n\n` instead |
| Ragged/uneven text | `multi_cell` left-aligned | Use justified rendering for multi-word lines |
| Single chars overflow | `multi_cell` throws with narrow space | Word-wrap on boundaries, detect width before calling |
| Zero-width chars crash | Unicode U+200B in Substack HTML | `str.replace()` before `get_string_width()` |

## Podcast Audio

See `references/podcast-audio.md` for detailed architecture, CDN URL mechanics, full episode gating investigation, and all endpoint patterns tested. Key findings from browser-level investigation:

- Preview audio (51 min) is accessible via RSS feed enclosure or `/src` endpoint with `connect.sid`
- Full episode (102 min) **always returns 401** — even from a real Playwright browser with proper auth headers
- The gate is server-side authorization, not bot detection or Cloudflare challenges — stealth browser config does not help
- The CDN uses CloudFront signed URLs (Key-Pair-Id + Signature) — cannot forge without Substack's private key
- For full-episode access investigation: DevTools network trace from a real (non-headless) browser session is the next step

## CLI Reference

The `stash` CLI is installed at:
`~/.hermes/skills/software-development/substack-paywall-export/scripts/stash_cli.py`

```bash
python3 ~/.hermes/skills/software-development/substack-paywall-export/scripts/stash_cli.py --help
```

Or symlink to PATH for convenience:
```bash
ln -sf ~/.hermes/skills/software-development/substack-paywall-export/scripts/stash_cli.py ~/.local/bin/stash
```

Note: `~/.local/bin` may not be in PATH by default. Either export it (`export PATH="$HOME/.local/bin:$PATH"`) or add to `~/.bashrc`.

## Pitfalls

- **Rate limits**: Don't exceed ~1 request/second to Substack — the API is unofficial and undocumented
- **Cookie expiry**: The cookie expires if you sign out or change your password. You'll get 403/401 errors — just re-export from browser
- **`requests` vs `urllib` on custom domains**: `urllib.request.urlopen` strips Cookie headers on cross-domain redirects. Always use `requests.Session` for authenticated Substack requests. This is the #1 failure mode for custom domain publications — it returns 404 on the custom domain despite valid auth
- **Custom domains require substack subdomain redirect**: The API endpoints (`/api/v1/archive`, individual posts) only work when accessed via the substack subdomain first, which redirects to the custom domain. Direct hits to the custom domain return 404
- **www vs non-www**: Some custom domains require the `www.` prefix. The stash CLI tries both variants automatically, but when your code tries to construct URLs manually, always try both
- **401 on full podcast episodes**: The RSS feed and `/src` endpoint give only the public preview (~51 min). The full episode (~2 hrs) returns 401 — Substack properly gates it behind additional auth beyond `connect.sid`. Full investigation in `references/podcast-audio.md`
- **Playwright cookie injection**: Pre-setting cookies via `context.add_cookies()` before navigation triggers Cloudflare bot detection (stripped 404 page). Use route interception instead — see `references/playwright-cloudflare-bypass.md` for the technique
- **`paidPublicationIds` doesn't always map to active subscriptions**: The user profile shows publication IDs you've paid at some point, but some may be expired or cancelled — cross-reference against what the archive API actually returns
- **Substack.com API vs publication API**: The main `substack.com/api/v1/` endpoints (user/me, etc.) require additional CSRF headers that are hard to replicate. Publication-specific endpoints with redirect chain work with just the cookie
- **Multi-page posts**: Long articles may span multiple pages (`?page=2`). Check for `post_page_count` in `_preloads`
- **body_html null**: Some older posts have `body_html: null` in `_preloads`. Fall back to extracting `<article>` tag from raw HTML
- **Archive pagination**: Default is 20-30 posts per page. Fetch offset=0,20,40,60... to get everything
- **Telegram MEDIA directive limitations**: The `send_message` tool's `MEDIA:<path>` only handles images (.png/.jpg/.webp), audio (.ogg), and video (.mp4). PDFs/arbitrary files are NOT delivered as attachments — use SCP or direct file transfer instead
- **Podcast body_html is always short**: Even with valid auth, podcast episodes show only show notes (200-600 chars) — not truncated content. The real content is audio
- **PDF formatting requires paragraph awareness**: Raw line-by-line rendering produces rough output. Always split by `\n\n` and rejoin paragraph lines, with justified text and proper spacing

## Verification

- Check that exported `.md` files have actual article content (not paywall previews)
- For podcast episodes: verify `body_html` length — 30-600 chars is normal (show notes), >1000 chars is a text article
- Verify auth: run `stash auth` — should show your handle and any paid publication IDs
- Compare fetched count vs estimated publication post count
- Spot-check a paywalled article in the exported markdown to ensure full text was captured
- **PDF quality check**: Open a page and verify paragraphs are separated (not squished), text is justified, and no mid-paragraph line breaks exist
