# YouTube IP Block Workarounds

Cloud VPS IPs (AWS, GCP, Azure, Hetzner, DigitalOcean, etc.) are blocked by YouTube for transcript/subtitle API requests and most third-party tools.

## Method 1: oEmbed API (always works)

```python
import requests
resp = requests.get(
    "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"
)
data = resp.json()
# Returns: title, author_name, author_url, type, height, width
```

No cookies, no auth, no IP check. Limited to title + channel metadata — no description, no transcript, no duration.

## Method 2: yt-dlp with cookies

Export cookies from a browser logged into YouTube:

1. Install `yt-dlp` and a cookie exporter extension (e.g., "Get cookies.txt" for Chrome/Firefox)
2. Export cookies to `youtube_cookies.txt`
3. Use with yt-dlp:

```bash
yt-dlp --cookies youtube_cookies.txt \
  --skip-download \
  --write-auto-subs \
  --sub-langs en \
  --convert-subs srt \
  -o "/tmp/yt_video" \
  'https://www.youtube.com/watch?v=VIDEO_ID'
```

⚠️ **Risk**: YouTube may permanently ban the account used for cookie auth. Only use with throwaway accounts.

## Method 3: Alternative YouTube Frontend APIs (mostly also blocked)

Try these instances — success varies by IP:

| Instance | API Endpoint | Status from VPS |
|---|---|---|
| invidious.* | `/api/v1/videos/VIDEO_ID` | Mostly 403/502 |
| pipedapi.* | `/streams/VIDEO_ID` | Mostly timeout/526 |

These are unreliable from cloud IPs. Don't depend on them.

## Method 4: Infer from Public Sources (most reliable fallback)

When all direct extraction fails:

1. Get title + channel from oEmbed API
2. Search web for the exact video title + channel name (often surfaces blog posts, Reddit discussions, article references)
3. Search web for the channel's description and focus
4. Read any linked sources or GitHub repos mentioned in search results
5. Synthesize what you know: video title gives you the concept, channel focus gives you the framing, domain knowledge fills in the probable approach

**Always separate confirmed from inferred in your output.** Example:
- ✅ Confirmed: Title, channel, upload timeframe
- ⚠️ Inferred from title + channel focus: The approach likely involves [specific technique]

## Method 5: YouTube Data API v3

If a `YOUTUBE_API_KEY`, `YOUTUBE_DATA_API_KEY`, or `GOOGLE_API_KEY` env var is configured:

```python
import os, requests
api_key = os.environ.get('YOUTUBE_API_KEY')
resp = requests.get(
    f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id=VIDEO_ID&key={api_key}"
)
data = resp.json()
# Returns: full description, tags, category, duration, statistics
```

Check via environment variable scan before assuming it exists — most Hermes instances don't have one configured.

## Method 6: Browser-based subagent (highest yield, heavy)

When every API-based method fails, spawn a subagent with the `browser` toolset to navigate the YouTube page directly:

```
delegate_task(
    goal="Navigate to this YouTube video and extract its complete content...",
    toolsets=["browser", "web"],
    context="...require the subagent to click 'More' to expand description, check for transcript button..."
)
```

The headless browser renders the full YouTube page including JavaScript-loaded content — description, metadata, channel info, and any UI elements revealing transcripts. This is the only method that works from a blocked IP for rich extraction.

**Limitations:**
- Expensive: a full browser-based extraction can take 3-5 minutes and 30+ tool calls
- Still cannot bypass YouTube's sign-in wall for transcripts (the browser renders the same IP-blocked page, just with JS enabled)
- Best for getting the full description, metadata, and channel info when oEmbed's title-only is insufficient

**When to use:** when the user needs the actual video description, channel statistics, linked resources, or timestamps — and methods 1-5 have failed.
