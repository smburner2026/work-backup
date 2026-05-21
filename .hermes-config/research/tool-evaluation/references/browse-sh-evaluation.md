# browse.sh Evaluation

**URL:** https://browse.sh  
**Repo:** github.com/browserbase/cli (part of Browserbase ecosystem)  
**Status:** Installed — conditional use  
**Date evaluated:** 2026-05-21  

## What It Is

browse.sh is a CLI for browser automation backed by Browserbase's cloud infrastructure. Provides:
- **Pre-built skills** for 111+ websites (Amazon, Airbnb, Craigslist, etc.) that return structured JSON
- **Low-level browser commands**: open, click, type, scroll, snapshot, fill, etc.
- **Cloud session management** via Browserbase (remote browsers with proxy support)
- **Local browser mode** via managed local Chromium or CDP attach

## Installation

```bash
npm install -g browse
browse skills install          # installs Hermes skill
browse skills add <skill>      # installs site-specific skills
```

Installed globally at `/root/.hermes/node/bin/browse`. Hermes skill at `~/.hermes/skills/browse/`.

## Browser Targets

| Mode | Flag | Requirements | Use Case |
|------|------|-------------|---------|
| CDP attach | `--cdp <port>` | Running Chrome with `--remote-debugging-port` | Development, local testing |
| Managed local | `--local` | CHROME_PATH env var, Chrome/Chromium installed | Simple sites, no bot protection |
| Browserbase cloud | `--remote` | `BROWSERBASE_API_KEY` in environment | Protected sites, scaling |

## Chrome Setup

If Chrome/Chromium is available from Playwright:

```bash
# Find the Chrome binary
ls ~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome
# Symlink to PATH
ln -sf ~/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome /usr/local/bin/chrome
export CHROME_PATH=/usr/local/bin/chrome
```

## CDP Mode (Recommended for Local)

The managed local mode (`browse open --local`) has environment-heriting issues with CHROME_PATH. CDP mode is more reliable:

```bash
# 1. Start Chrome with remote debugging
chrome --headless --remote-debugging-port=9222 --no-sandbox --disable-gpu &

# 2. Connect browse to it
browse open "https://example.com" --cdp 9222
browse snapshot --cdp 9222         # inspect page
browse click @0-5 --cdp 9222       # interact
browse get html body --cdp 9222    # get HTML
```

## Amazon / Akamai Blocking

**Amazon blocks headless Chrome** with Akamai Bot Manager. CDP and managed local modes both fail with "Sorry! Something went wrong!" ~75% of the time.

The Amazon search skill's documented fix:
1. Create a Browserbase cloud session with `--verified --proxies` flags
2. Warm the session by visiting Amazon homepage first (seeds ak_bmsc/bm_sz cookies)
3. Then navigate to the search results page

**Prerequisite:** `BROWSERBASE_API_KEY` must be set in `~/.hermes/.env`.

## Skills Catalog

Browse.sh has 111+ pre-built skills. Find and install:

```bash
browse skills find <keyword>
browse skills add <domain>/<task>
```

Notable skills: Amazon Product Search, Airbnb Search, Craigslist Posting, ArXiv Papers, Best Buy Stock Check, Booking.com Hotels, CarGurus Listings, GitHub Trending, Google Flights, HackerNews Search, LinkedIn Profile, Reddit Search, Wikipedia, Yelp Reviews, YouTube Transcripts.

## Limitations

- Local mode requires Chrome/Chromium installed and accessible via CHROME_PATH
- Managed local daemon has subprocess environment issues — prefers CDP mode
- Amazon and similar high-protection sites require Browserbase cloud with verified+proxies
- No Browserbase API key configured in this environment as of 2026-05-21
