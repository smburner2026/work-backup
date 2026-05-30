#!/usr/bin/env python3
"""
Substack Paywall Client — authenticated HTTP client for Substack's unofficial API.

Handles:
- Cookie-based auth (connect.sid)
- Publication archive fetching
- Individual article content extraction
- Subscribed publication discovery
- Caching of fetched articles
"""

import os
import re
import json
import time
import codecs
from pathlib import Path
import requests

# --------------- paths ---------------
CONFIG_DIR = Path(os.path.expanduser("~/.hermes/config"))
AUTH_PATH = CONFIG_DIR / "substack_auth.json"
CACHE_DIR = Path(os.path.expanduser("~/.hermes/cache/substack"))

# --------------- HTTP client ---------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def load_auth():
    """Load auth cookie from config file."""
    if not AUTH_PATH.exists():
        return None
    try:
        with open(AUTH_PATH) as f:
            data = json.load(f)
        return data.get("cookie", "")
    except (json.JSONDecodeError, KeyError):
        return None

def save_auth(cookie_value):
    """Save auth cookie to config file (mode 600)."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(AUTH_PATH, "w") as f:
        json.dump({"cookie": cookie_value}, f)
    os.chmod(AUTH_PATH, 0o600)
    print(f"Auth saved to {AUTH_PATH}")

def make_headers(cookie=None, referer=None, json_accept=False):
    """Build request headers with optional auth cookie."""
    h = dict(HEADERS)
    if referer:
        h["Referer"] = referer
    if json_accept:
        h["Accept"] = "application/json, text/plain, */*"
    return h

def fetch_url(url, cookie=None, referer=None, timeout=30):
    """Fetch a URL with optional auth using requests (handles cross-domain cookies).
    Returns (status_code, body_text)."""
    headers = make_headers(cookie, referer=referer or url)
    
    # Build a requests session that preserves cookies across redirects
    session = requests.Session()
    if cookie:
        # Parse cookie string and set it on the session
        # The cookie value might be "connect.sid=s%3A..." or just "s%3A..."
        session.headers.update(headers)
        session.headers["Cookie"] = cookie
    
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        return resp.status_code, resp.text
    except requests.exceptions.Timeout:
        return 0, "Timeout"
    except requests.exceptions.ConnectionError as e:
        return 0, f"ConnectionError: {e}"
    except requests.exceptions.RequestException as e:
        return 0, f"RequestException: {e}"


# --------------- Auth & user info ---------------
def get_current_user(cookie):
    """Try to get current user info from various endpoints.
    Returns dict with handle, email, paidPublicationIds or None."""
    # Method 1: Try the home page and parse preloads
    status, html = fetch_url("https://substack.com/", cookie=cookie)
    if status != 200:
        return None

    user = _extract_user_from_html(html)
    if user:
        return user

    # Method 2: Try the reader feed 
    status2, feed = fetch_url(
        "https://substack.com/api/v1/reader/feed?limit=1",
        cookie=cookie,
        referer="https://substack.com/",
    )
    if status2 == 200:
        try:
            data = json.loads(feed)
            # Scan context users for the current user
            for item in data.get("items", []):
                ctx = item.get("context", {})
                for u in ctx.get("users", []):
                    if u.get("id"):
                        return {
                            "handle": u.get("handle", ""),
                            "name": u.get("name", ""),
                            "id": u.get("id"),
                        }
        except (json.JSONDecodeError, KeyError):
            pass

    return None


def _extract_user_from_html(html):
    """Parse window._preloads from Substack HTML to extract currentUser."""
    # Try escaped JSON.parse format
    m = re.search(r'window\._preloads\s*=\s*JSON\.parse\(\s*"(.*?)"\s*\)', html)
    if m:
        try:
            escaped = m.group(1)
            unescaped = codecs.decode(escaped, "unicode-escape")
            data = json.loads(unescaped)
            cu = data.get("currentUser") or data.get("user")
            if cu:
                user = {
                    "handle": cu.get("handle", ""),
                    "name": cu.get("name", ""),
                    "id": cu.get("id"),
                    "email": cu.get("email", ""),
                    "paid_publication_ids": cu.get("status", {}).get("paidPublicationIds", []),
                    "is_subscribed": cu.get("is_subscribed", False),
                    "is_free_subscribed": cu.get("is_free_subscribed", False),
                }
                return user
        except (json.JSONDecodeError, KeyError, Exception):
            pass
    
    # Try direct JSON assignment format
    m2 = re.search(r'window\._preloads\s*=\s*(\{.*?\});', html)
    if m2:
        try:
            data = json.loads(m2.group(1))
            cu = data.get("currentUser") or data.get("user", {})
            if cu:
                return {
                    "handle": cu.get("handle", ""),
                    "name": cu.get("name", ""),
                    "id": cu.get("id"),
                }
        except (json.JSONDecodeError, Exception):
            pass

    return None


# --------------- Publication discovery ---------------
def discover_subscriptions(cookie):
    """Discover subscribed publications. Returns list of pub dicts."""
    pubs = []

    # Method 1: API endpoint
    status, body = fetch_url(
        "https://substack.com/api/v1/subscriptions?tvOnly=false",
        cookie=cookie,
        referer="https://substack.com/",
    )
    if status == 200:
        try:
            data = json.loads(body)
            pubs.extend(data.get("publications", []))
        except (json.JSONDecodeError, Exception):
            pass

    # Method 2: Look up paidPublicationIds from user profile
    user = get_current_user(cookie)
    if user and user.get("paid_publication_ids"):
        print(f"  Found {len(user['paid_publication_ids'])} paid publication IDs in profile")

    return pubs


def resolve_publication_id(pub_id, cookie):
    """Try to resolve a publication ID to name+subdomain by fetching its home page."""
    # Try common patterns
    # Method: Search for the publication by trying to access {id}.substack.com
    # or look it up through various means
    
    # For now, return the ID so the user can identify it
    return {"id": pub_id, "name": f"Publication #{pub_id}", "subdomain": str(pub_id)}


# --------------- Archive fetching ---------------
def resolve_pub_url(pub):
    """Resolve a publication identifier to its base URL.
    Handles bare subdomains (theognisomegara), custom domains (bronzeagepervert.yoga),
    and full URLs. Returns the primary URL."""
    pub = pub.strip().lower()
    pub = re.sub(r'^https?://', '', pub)
    # Keep www. in the name if present — some domains require it
    # Don't strip it since some custom domains need www. prefix
    # If it contains a dot, it's already a domain — use as-is
    if '.' in pub:
        return f"https://{pub}"
    # Otherwise it's a Substack subdomain
    return f"https://{pub}.substack.com"


def _get_domain_variants(pub):
    """Get domain variants to try (www and non-www variants of custom domains)."""
    base = resolve_pub_url(pub)
    
    # Extract the domain part
    domain = base.replace("https://", "")
    
    # For custom domains (contain a dot), try www and non-www
    if '.' in pub and 'substack.com' not in pub:
        variants = []
        if domain.startswith("www."):
            variants.append(base)
            variants.append(f"https://{domain[4:]}")
        else:
            variants.append(base)
            variants.append(f"https://www.{domain}")
        return variants
    
    # For subdomains, just use as-is
    return [base]


def fetch_archive(pub, cookie, max_pages=5):
    """Fetch all posts from a publication's archive.
    Returns list of post dicts with slug, title, post_date, id.
    Handles both bare subdomains and custom domains."""
    domains_to_try = _get_domain_variants(pub)
    posts = []
    seen = set()

    for base_url in domains_to_try:
        for page in range(max_pages):
            offset = page * 20
            url = f"{base_url}/api/v1/archive?sort=new&offset={offset}&limit=20"
            status, body = fetch_url(url, cookie=cookie)

            if status != 200:
                if page == 0:
                    print(f"  Archive API returned {status} — publication may not exist or is private")
                break

            try:
                batch = json.loads(body)
            except json.JSONDecodeError:
                break

            if not batch:
                break

            for post in batch:
                slug = post.get("slug", "")
                if slug and slug not in seen:
                    seen.add(slug)
                    posts.append({
                        "slug": slug,
                        "title": post.get("title", ""),
                        "post_date": post.get("post_date", ""),
                        "id": post.get("id"),
                        "audience": post.get("audience", ""),
                        "type": post.get("type", ""),
                        "wordcount": post.get("wordcount", 0),
                    })

            if len(batch) < 20:
                break

            time.sleep(0.3)

        # If we found posts on this domain, don't try the fallback
        if posts:
            break

    return posts


# --------------- Article content extraction ---------------
def fetch_article_content(pub, slug, cookie):
    """Fetch full article content from a Substack page.
    Returns dict with body_html, title, paywall_status or None."""
    domains_to_try = _get_domain_variants(pub)
    
    for base in domains_to_try:
        url = f"{base}/p/{slug}"
        status, html = fetch_url(url, cookie=cookie, referer=f"{base}/")
        
        if status != 200:
            continue
        
        # Try to extract content from the page
        result = _try_extract_article(html, slug)
        if result:
            # Check for multi-page
            content = _check_multipage(result, base, slug, cookie)
            return content
    
    # If all domains failed, try once with following redirects
    # (some custom domains redirect to substack subdomain or vice versa)
    url = f"{resolve_pub_url(pub)}/p/{slug}"
    status, html = fetch_url(url, cookie=cookie)
    if status == 200:
        result = _try_extract_article(html, slug)
        if result:
            return _check_multipage(result, resolve_pub_url(pub), slug, cookie)
    
    return None


def _try_extract_article(html, slug):
    """Try to extract article content from HTML. Returns dict or None."""
    # Method 1: Extract window._preloads
    post = _extract_post_preloads(html)
    if post:
        body_html = post.get("body_html", "")
        title = post.get("title", slug.replace("-", " ").title())
        is_paywalled = post.get("audience", "") == "only_paid" or post.get("visibility", "") == "paywalled"
        page_count = post.get("post_page_count", 1)
        
        return {
            "body_html": body_html,
            "title": title,
            "is_paywalled": is_paywalled,
            "page_count": page_count,
        }

    # Method 2: Fall back to extracting <article> tag
    article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if article_match:
        article_html = article_match.group(1)
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = ""
        if title_match:
            title = re.sub(r'<[^>]+>', "", title_match.group(1)).strip()
        
        return {
            "body_html": article_html,
            "title": title or slug.replace("-", " ").title(),
            "is_paywalled": False,
            "page_count": 1,
        }
    
    return None


def _check_multipage(content, base, slug, cookie):
    """Check if article has multiple pages and fetch them."""
    page_count = content.get("page_count", 1)
    if page_count <= 1:
        return content
    
    all_html = [content["body_html"]] if content.get("body_html") else []
    for pg in range(2, page_count + 1):
        pg_url = f"{base}/p/{slug}?page={pg}"
        pg_status, pg_html = fetch_url(pg_url, cookie=cookie)
        if pg_status == 200:
            pg_post = _extract_post_preloads(pg_html)
            if pg_post and pg_post.get("body_html"):
                all_html.append(pg_post["body_html"])
        time.sleep(0.3)
    
    content["body_html"] = "\n\n".join(filter(None, all_html))
    return content


def _extract_post_preloads(html):
    """Extract post data from window._preloads in Substack page HTML."""
    m = re.search(r'window\._preloads\s*=\s*JSON\.parse\(\s*"(.*?)"\s*\)', html)
    if m:
        try:
            escaped = m.group(1)
            unescaped = codecs.decode(escaped, "unicode-escape")
            data = json.loads(unescaped)
            
            # Navigate to post data (various possible paths)
            if "post" in data:
                return data["post"]
            if "preloads" in data and "post" in data["preloads"]:
                return data["preloads"]["post"]
            for v in data.values():
                if isinstance(v, dict) and "body_html" in v:
                    return v
            return None
        except (json.JSONDecodeError, Exception):
            return None

    # Try non-escaped JSON
    m2 = re.search(r'window\._preloads\s*=\s*(\{.*?\});', html, re.DOTALL)
    if m2:
        try:
            data = json.loads(m2.group(1))
            if "post" in data:
                return data["post"]
            return None
        except (json.JSONDecodeError, Exception):
            return None
    
    return None


# --------------- HTML to markdown ---------------
def body_html_to_markdown(body_html, method="trafilatura"):
    """Convert Substack body_html to clean markdown."""
    if method == "trafilatura":
        try:
            import trafilatura
            text = trafilatura.extract(
                body_html,
                output_format="markdown",
                include_links=False,
                include_images=False,
                include_formatting=True,
                favor_precision=True,
            )
            if text:
                # Strip Substack boilerplate
                text = re.sub(r'^This below is.*?\n', '', text, flags=re.MULTILINE)
                text = re.sub(r'^FUNDRAISING.*?\n', '', text, flags=re.MULTILINE)
                text = re.sub(r'^Click here to navigate.*?\n', '', text, flags=re.MULTILINE)
                text = re.sub(r'^Subscribe now\s*\n', '', text, flags=re.MULTILINE)
                text = re.sub(r'\n{4,}', '\n\n\n', text)
                return text.strip()
        except ImportError:
            pass  # Fall through to html2text

    # html2text fallback
    try:
        import html as html_mod
        import html2text
        text = html_mod.unescape(body_html)
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        h = html2text.HTML2Text()
        h.body_width = 0
        h.ignore_links = True
        h.ignore_images = True
        h.unicode_snob = True
        result = h.handle(text)
        result = re.sub(r'\n{4,}', '\n\n\n', result)
        return result.strip()
    except ImportError:
        return None


# --------------- Caching ---------------
def get_cache_dir():
    """Ensure cache dir exists and return it."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def get_article_cache_path(pub, slug):
    """Get path for cached article raw HTML/JSON."""
    cache = get_cache_dir()
    pub_dir = cache / pub
    pub_dir.mkdir(exist_ok=True)
    return pub_dir / f"{slug}.json"


def load_cached_article(pub, slug):
    """Load cached article data if available."""
    path = get_article_cache_path(pub, slug)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def save_cached_article(pub, slug, data):
    """Cache article data."""
    path = get_article_cache_path(pub, slug)
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_archive_cache_path(pub):
    """Get path for cached archive list."""
    cache = get_cache_dir()
    return cache / f"{pub}_archive.json"


def load_cached_archive(pub):
    """Load cached archive if available."""
    path = get_archive_cache_path(pub)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def save_cached_archive(pub, posts):
    """Cache archive list."""
    path = get_archive_cache_path(pub)
    with open(path, "w") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
