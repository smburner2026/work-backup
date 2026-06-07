"""groktocrawl_client — HTTP client for GroktoCrawl endpoints.

Wraps the GroktoCrawl Firecrawl v2-compatible API. Returns typed dicts
that the escalate.py module can route through OutputGate.

Environment:
    GROKTOCRAWL_URL  — base URL, default http://100.110.237.89:8080
    GROKTOCRAWL_KEY  — optional bearer token (set if API_KEY= in .env)

Usage:
    from groktocrawl_client import GroktoCrawl
    gc = GroktoCrawl()
    result = gc.search("VSTB quyen 1")  # Level 1
    page = gc.scrape("https://gallica.bnf.fr/...")  # Level 2
    page = gc.scrape(url, use_browser=True)  # Level 3
    job = gc.agent("research question")  # Level 4
"""

import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, Dict, Any, List


class GrokToCrawlError(Exception):
    """Raised on transport or non-2xx response from GroktoCrawl."""
    def __init__(self, message: str, status: Optional[int] = None, body: Optional[str] = None):
        super().__init__(message)
        self.status = status
        self.body = body


class GroktoCrawl:
    """Thin HTTP client around the Firecrawl v2 API surface.

    Option A: stack runs on VPS localhost, started on-demand via
    `groktocrawl start` (docker compose up). 0MB RAM when stopped.
    """

    DEFAULT_URL = "http://localhost:8080"
    DEFAULT_TIMEOUT = 30

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("GROKTOCRAWL_URL") or self.DEFAULT_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("GROKTOCRAWL_KEY")

    def _request(self, method: str, path: str, body: Optional[dict] = None,
                 timeout: int = DEFAULT_TIMEOUT) -> dict:
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")

        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                status = resp.status
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace") if e.fp else ""
            raise GrokToCrawlError(f"{method} {path} → {e.code}: {raw[:200]}",
                                    status=e.code, body=raw) from e
        except urllib.error.URLError as e:
            raise GrokToCrawlError(f"{method} {path} → network error: {e.reason}") from e
        except TimeoutError as e:
            raise GrokToCrawlError(f"{method} {path} → timeout after {timeout}s") from e

        elapsed = time.time() - t0
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"_raw": raw}

        payload["_elapsed"] = round(elapsed, 2)
        payload["_status"] = status
        return payload

    # ── Health ─────────────────────────────────────────────────────────

    def health(self) -> dict:
        return self._request("GET", "/health", timeout=5)

    def is_up(self) -> bool:
        try:
            return self.health().get("status") == "ok" or self.health().get("_status") == 200
        except GrokToCrawlError:
            return False

    # ── Level 1 — search ───────────────────────────────────────────────

    def search(self, query: str, sources: list = None, categories: Optional[str] = None,
               limit: int = 5, timeout: int = 20) -> dict:
        """SearXNG-backed search via GroktoCrawl. Triggered by Signal A."""
        body: Dict[str, Any] = {"query": query, "limit": limit}
        if sources is None:
            sources = ["web"]
        body["sources"] = sources
        if categories:
            body["categories"] = categories
        return self._request("POST", "/v2/search", body=body, timeout=timeout)

    # ── Level 2 — scrape (three-tier) ──────────────────────────────────

    def scrape(self, url: str, timeout: int = 30) -> dict:
        """Three-tier scraper: /llms.txt → markdown header → Playwright.
        Triggered by Signal B. Returns barrier info if blocked."""
        return self._request("POST", "/v2/scrape", body={"url": url}, timeout=timeout)

    # ── Level 3 — full browser / crawl / map ──────────────────────────

    def scrape_with_browser(self, url: str, timeout: int = 60) -> dict:
        """Force Playwright tier. Triggered by Signals C and D."""
        return self._request("POST", "/v2/scrape",
                              body={"url": url, "useBrowser": True}, timeout=timeout)

    def crawl(self, url: str, max_depth: int = 2, limit: int = 50,
              timeout: int = 120) -> dict:
        """Site crawl. Triggered by Signal E (need site-wide structure)."""
        return self._request("POST", "/v2/crawl",
                              body={"url": url, "maxDepth": max_depth, "limit": limit},
                              timeout=timeout)

    def map_urls(self, url: str, limit: int = 100, timeout: int = 60) -> dict:
        """URL discovery. Triggered by Signal E."""
        return self._request("POST", "/v2/map",
                              body={"url": url, "limit": limit}, timeout=timeout)

    # ── Level 4 — autonomous agent ─────────────────────────────────────

    def agent(self, prompt: str, model: Optional[str] = None,
              timeout: int = 300) -> dict:
        """Autonomous research loop. Last resort — Signal F."""
        body: Dict[str, Any] = {"prompt": prompt}
        if model:
            body["model"] = model
        return self._request("POST", "/v2/agent", body=body, timeout=timeout)

    def agent_status(self, job_id: str, timeout: int = 30) -> dict:
        return self._request("GET", f"/v2/agent/{job_id}", timeout=timeout)


# ── Helper: classify a GroktoCrawl scrape result ──────────────────────

def extract_barrier(payload: dict) -> Optional[dict]:
    """If the scrape returned a barrier, return its structured info.
    Otherwise None. Used by the escalation logic to decide between
    Level 2 → Level 3."""
    barrier = payload.get("barrier")
    if not barrier:
        return None
    if not barrier.get("detected"):
        return None
    if barrier.get("confidence", 0) < 0.7:
        return None
    return barrier


def extract_markdown(payload: dict) -> str:
    """Best-effort markdown extraction from a GroktoCrawl response."""
    # Check nested data first (standard GroktoCrawl response format)
    data = payload.get("data") or payload
    for key in ("markdown", "content", "text"):
        val = data.get(key)
        if isinstance(val, str) and len(val) >= 50:
            return val
    # Fallback: check top-level
    for key in ("markdown", "content", "text"):
        val = payload.get(key)
        if isinstance(val, str) and len(val) >= 50:
            return val
    return ""


def extract_quality(payload: dict) -> float:
    """Return the 0.0–1.0 quality score if present, else heuristic on content length."""
    data = payload.get("data") or payload
    q = data.get("quality") or payload.get("quality")
    if isinstance(q, dict) and "score" in q:
        return float(q["score"])
    if isinstance(q, (int, float)):
        return float(q)
    # Heuristic fallback
    md = extract_markdown(payload)
    if not md:
        return 0.0
    if len(md) < 200:
        return 0.2
    if len(md) < 1000:
        return 0.5
    return 0.8
