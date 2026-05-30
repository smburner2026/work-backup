# Playwright Cloudflare Bypass: Route Interception for Auth Cookies

When investigating Substack (or Cloudflare-protected sites) with Playwright, **pre-setting cookies via `context.add_cookies()` before navigation triggers Cloudflare bot detection** — the page loads as a minimal 404 shell with no content.

## The Problem

```python
# This FAILS — Cloudflare blocks the authenticated request
context.add_cookies([{'name': 'connect.sid', 'value': 's%3A...', 'domain': '.substack.com'}])
page.goto(url)  # Returns stripped 404 page, no _preloads, no audio
```

Even with full stealth configuration (`navigator.webdriver` patching, plugins override, Chrome UA, viewport, locale, timezone), pre-set cookies cause Cloudflare to serve a stripped page. The browser's initial request with unknown cookies combined with headless detection triggers a challenge that fails.

## The Fix: Route Interception

Load the page **without cookies first** (passes Cloudflare), then inject the `Cookie` header via route interception for all subsequent requests:

```python
cookie_header = json.load(open('/root/.hermes/config/substack_auth.json'))['cookie']

# Intercept ALL requests to inject cookie header
page.route('**/*', lambda route: route.continue_(
    headers={**route.request.headers, 'Cookie': cookie_header}
))

# Now navigate — page loads fully because the initial request 
# doesn't have the cookie pre-loaded, Cloudflare passes it,
# and subsequent XHR/fetch/audio requests carry the auth header
page.goto(url, wait_until='domcontentloaded')
```

## Why It Works

1. Cloudflare sees the browser's initial request **without** the pre-loaded cookie
2. The browser passes the JS challenge (or gets a `cf_clearance` token set by the page)
3. Subsequent requests with the Cookie header injected via `route.continue_()` are trusted
4. The `cf_clearance` cookie + the `connect.sid` cookie together authenticate all API calls

## Limitations

- The initial page response is **unauthenticated** — `window._preloads.confirmedLogin` will be `false`
- The cookie IS sent on XHR/fetch/audio element requests after page load
- `fetch()` from within `page.evaluate()` may still fail with CORS errors when fetching cross-origin API endpoints (e.g., `api.substack.com` from a custom domain page)
- Media elements (`<audio>`, `<video>`) that reference the API endpoint work correctly because they don't have CORS restrictions on simple GET requests

## Cookie Format

Store the cookie in the standard `Header: value` format:
```python
cookie_header = json.load(open('~/.hermes/config/substack_auth.json'))['cookie']
# Format: "connect.sid=s%3A..."
```

Don't parse it — pass the full header value directly to the `Cookie` header.

## When to Use vs. Not

| Use route interception | Use context.add_cookies() |
|---|---|
| Cloudflare-protected sites with auth cookies | Sites without Cloudflare |
| Substack with connect.sid cookie | Local/internal sites |
| Authenticated scraping of CDN/media URLs | Sites where cookies don't trigger challenges |
| Browser tests where first-party cookies trigger detection | API testing |

## Full Working Pattern

```python
from playwright.sync_api import sync_playwright
import json

cookie_header = json.load(open('/root/.hermes/config/substack_auth.json'))['cookie']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    )
    page = context.new_page()
    
    # Route interception — injects cookie on every request
    page.route('**/*', lambda route: route.continue_(
        headers={**route.request.headers, 'Cookie': cookie_header}
    ))
    
    page.goto(url, wait_until='domcontentloaded')
    page.wait_for_timeout(3000)
    
    # Now page.content() has the full HTML with _preloads
    # Audio/video elements load with auth
    # XHR/fetch requests carry the cookie
```

Note: This technique is **Substack-specific** in our usage but the pattern applies to any site where Cloudflare blocks pre-set auth cookies in headless browsers.
