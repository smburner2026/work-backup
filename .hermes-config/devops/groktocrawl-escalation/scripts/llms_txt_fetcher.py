"""llms_txt_fetcher — Tier 1 scraper from GroktoCrawl v0.6.0 (MIT License).

Checks for /llms.txt at a site root — a single GET that returns the
entire site as clean markdown. Fast, zero parsing needed.

Usage:
    from llms_txt_fetcher import fetch_llms_txt

    result = fetch_llms_txt("https://example.com")
    if result:
        print(f"Got {len(result)} chars of site-wide markdown")
"""

import urllib.request
import urllib.error
from urllib.parse import urlparse
from typing import Optional


def fetch_llms_txt(url: str, timeout: int = 10) -> Optional[str]:
    """Try to fetch /llms.txt from the site root.

    If the URL is already a page path, strips to scheme + netloc
    and appends /llms.txt.

    Returns the markdown content as a string, or None if:
      - /llms.txt doesn't exist (HTTP 4xx)
      - The server times out or is unreachable
      - The response is empty or binary
    """
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    llms_url = f"{root}/llms.txt"

    req = urllib.request.Request(
        llms_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (compatible; HermesAgent;"
                " groktocrawl-extraction; +https://hermes-agent.org)"
            ),
            "Accept": "text/markdown, text/plain, */*",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()
    except urllib.error.HTTPError as e:
        # 404 = no /llms.txt, that's normal
        return None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None

    if status != 200:
        return None
    if not raw:
        return None
    # Skip binary content
    if not content_type.startswith("text/") and "markdown" not in content_type:
        return None

    text = raw.decode("utf-8", errors="replace")
    if len(text) < 20:
        return None
    return text


def site_has_llms_txt(url: str) -> bool:
    """Quick check: does this site support /llms.txt?"""
    return fetch_llms_txt(url) is not None
