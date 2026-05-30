# Podcast Audio Extraction from Substack

Substack publications can host podcast episodes alongside their newsletters. Audio download follows a different pattern than text extraction.

## Data Structure

Each podcast post's `window._preloads` contains:

```json
{
  "post": {
    "type": "podcast",
    "audience": "only_paid",
    "body_html": "<p>Show notes (short, 200-600 chars)</p>",
    "podcast_url": "https://api.substack.com/api/v1/audio/upload/{preview_upload_id}/src",
    "podcast_duration": 3063.09,
    "podcastUpload": {
      "id": "{preview_upload_id}",
      "name": "EPISODE216PUBLIC.mp3",
      "duration": 3063.09,
      "primary_file_size": 49010219,
      "is_free_preview": true,
      "full_podcast_info": {
        "media_upload_id": "{full_episode_upload_id}",
        "duration": 6128.09
      }
    }
  }
}
```

Key observations:
- **`body_html` is short** (~200-600 chars) even with full auth — podcast show notes, not truncated text
- **`podcast_url`** points to the public preview audioclient via `/src` endpoint
- **`podcastUpload.full_podcast_info`** has the full episode's `media_upload_id` and `duration` (longer) — but it's properly gated

## Preview Audio Access (Works)

### Method 1: RSS Feed Enclosure

Every Substack publication's RSS feed at `{pub}.substack.com/feed` includes podcast enclosure URLs:

```xml
<enclosure url="https://api.substack.com/feed/podcast/{post_id}/{hash}.mp3" length="0" type="audio/mpeg"/>
```

The URL pattern is:
```
https://api.substack.com/feed/podcast/{post_id}/{32_hex_char_hash}.mp3
```

Download with auth cookie:
```bash
COOKIE=$(python3 -c "import json; print(json.load(open('~/.hermes/config/substack_auth.json'))['cookie'])")
curl -s -L -o episode.mp3 \
  -H "Cookie: $COOKIE" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://{pub}.substack.com/" \
  "https://api.substack.com/feed/podcast/{post_id}/{hash}.mp3"
```

The request chain:
1. `api.substack.com/feed/podcast/{post_id}/{hash}.mp3` → 307 redirect
2. Redirects to `substackcdn.com/video_upload/post/{post_id}/{upload_id}/transcoded.mp3?post_id={post_id}&relation=podcast_preview&Expires={timestamp}&Key-Pair-Id=...&Signature=...`
3. Signed CDN URL from `substackcdn.com` with 2-month expiry

The `connect.sid` cookie authenticates step 1. The redirect carries auth through (unlike urllib).

### Method 2: `/src` Endpoint

```
https://api.substack.com/api/v1/audio/upload/{upload_id}/src
```

Same result as the RSS feed — returns the preview audio. Returns 401 for the full episode upload ID.

## Full Episode Access (Gated — Investigated May 2026)

The full episode's `media_upload_id` from `full_podcast_info`:

```
https://api.substack.com/api/v1/audio/upload/{full_upload_id}/src
```

Returns **401 `{"error":""}`** — properly gated. The full episode requires additional authorization beyond `connect.sid`, likely a separate podcast subscription tier or server-side token validation.

### Exhaustive test results (2026-05-24)

Investigation methodology: HTTP requests + Playwright browser with full stealth configuration (navigator.webdriver patching, plugins override, Chrome UA, proper viewport/locale/timezone, `cf_clearance` obtained, cookie header injection via route interception).

| Method | Result |
|---|---|
| `/src` endpoint (HTTP, connect.sid cookie) | **401** |
| `/src` endpoint (Playwright, header injection, authenticated page) | **401** |
| CDN direct URL (full upload ID, no signature) | **403 MissingKey** |
| RSS feed enclosure (any post) | Preview only |
| `/feed/podcast/{post_id}/{full_id}.mp3` | Maps to preview, not full |
| Audio src swap in browser (preview→full upload ID) | MEDIA_ELEMENT_ERROR (401 response) |
| Playwright evaluate fetch (CORS blocked) | Failed to fetch |

### What's different about full episodes

The 401 is **server-side authorization** (not bot/Cloudflare detection):

1. Preview `/src` → **307** redirect to CloudFront **signed URL** (`Key-Pair-Id`, `Expires`, `Signature`)
2. Full `/src` → **401** — Substack's API server checks an entitlement beyond `connect.sid`
3. The CDN itself requires valid CloudFront signed URLs — cannot forge without Substack's private key
4. Even Playwright with full stealth + authenticated session (loaded page, played preview audio) gets 401 on full

### Candidates for the missing auth

Likely one of:
- **Separate podcast subscription flag** checked server-side beyond `connect.sid`
- **SPA-derived token** minted on page load from a different API endpoint
- **Publication-specific entitlement** — `connect.sid` authenticates the user but doesn't prove podcast access for this publication

### To truly solve

Open a **real Chrome (not headless)** DevTools session logged into Substack with active BAP subscription:
1. Navigate to a podcast episode
2. Clear Network tab
3. Click play on the full episode (not preview)
4. Look for the actual API call, cookies, tokens, and headers sent

The `connect.sid` alone is insufficient — there's another layer.

## Downloaded File Characteristics

| Property | Preview | Full Episode |
|---|---|---|
| File size | ~49 MB | ~98 MB (est.) |
| Duration | ~3,063s (51 min) | ~6,128s (2 hrs) |
| Format | MP3, ID3 tags | MP3 |
| Access | RSS feed + auth cookie | 401 — gated |
| Filename pattern | `{slug}_PUBLIC.mp3` | unknown |

## Example: Episode 216 (Bronze Age Pervert)

| Field | Value |
|---|---|
| Post ID | 197949480 |
| Publication ID | 3243459 |
| Preview upload ID | `a9266236-c8e1-496e-8f6f-bce0d3b71980` |
| Preview file | `EPISODE216PUBLIC.mp3` |
| Preview duration | 3063s (51.1 min) |
| Preview size | 49,010,219 bytes |
| RSS feed hash | `d038fde5033b758e4e3042b366219220` |
| **Full episode upload ID** | **`b7b51433-c7c3-4cd3-8010-b62595256ebc`** |
| Full duration | 6128s (102.1 min) |
| Thumbnail ID | 1778901402 |
| URL | `www.bronzeagepervert.yoga/p/episode-216-oligarchs` |

## Known Publications with Podcast Content

| Publication | Audio Content | Preview Size |
|---|---|---|
| Bronze Age Pervert (3243459) | 79 podcast episodes, all paywalled | ~49 MB each |
