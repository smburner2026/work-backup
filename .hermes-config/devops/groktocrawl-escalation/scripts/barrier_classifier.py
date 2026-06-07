"""barrier_classifier — Extracted from GroktoCrawl v0.6.0 (MIT License).

Detects web page barriers (Cloudflare, CAPTCHA, rate-limit, etc.)
before wasting a browser render. Pure Python, zero external deps.

Usage:
    from barrier_classifier import classify_barrier, BarrierInfo

    info = classify_barrier(url="https://example.com", html=page_html)
    if info.detected and info.confidence > 0.7:
        print(f"Blocked by {info.barrier_type} (conf: {info.confidence:.2f})")
        # escalate to Playwright/SearXNG fallback
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse


@dataclass
class BarrierInfo:
    """Structured result from barrier classification."""
    detected: bool = False
    barrier_type: Optional[str] = None
    # "cloudflare" | "ddos-guard" | "captcha" | "rate-limit"
    # | "substack-redirect" | "empty" | "suspicious" | None
    confidence: float = 0.0
    detail: str = ""
    title: str = ""


# ── Signal patterns ─────────────────────────────────────────────────

CLOUDFLARE_TITLE_INDICATORS = re.compile(
    r"(just a moment|checking your browser|attention required"
    r"|403 forbidden|cf-error-404|cloudflare)", re.I
)
DDOS_GUARD_TITLE_INDICATORS = re.compile(
    r"(ddos-guard|ddos protection)", re.I
)
CAPTCHA_CONTENT = re.compile(r"(hcaptcha|recaptcha)", re.I)
RATE_LIMIT_CONTENT = re.compile(
    r"(rate limit(?:ed)?|too many requests|try again later"
    r"|please slow down)", re.I
)
SUBSTACK_REDIRECT = re.compile(
    r"(session-attribution-frame|channel-frame)", re.I
)
EMPTY_MIN_CHARS = 100


def classify_barrier(
    url: str,
    html: str = "",
    content: str = "",
    title: str = "",
) -> BarrierInfo:
    """Classify whether a page response is a barrier/block/challenge.

    Args:
        url: The URL that was requested.
        html: Raw HTML of the response.
        content: Markdown or extracted text content.
        title: Page title.

    Returns:
        BarrierInfo with detected, barrier_type, confidence, detail.
    """
    if not html and not content:
        return BarrierInfo(detected=False)

    signals: set[str] = set()
    title_lower = title.lower()
    html_lower = html.lower()
    content_lower = content.lower()
    url_str = str(url)
    parsed = urlparse(url_str)

    # ── 1. Empty content ────────────────────────────────────────────
    content_len = max(len(content), len(html))
    if content_len < EMPTY_MIN_CHARS:
        signals.add("empty")

    # ── 2. Cloudflare patterns ──────────────────────────────────────
    if CLOUDFLARE_TITLE_INDICATORS.search(title_lower):
        signals.add("cloudflare-title")
    if "cf_chl" in url_str or "challenge-platform" in url_str:
        signals.add("cloudflare-url")
    if "cf-error-404" in html_lower or "cf-error" in html_lower:
        signals.add("cloudflare-error")
    if "___cf" in html_lower:
        signals.add("cloudflare-cookie")

    # ── 3. DDoS-Guard ────────────────────────────────────────────────
    if DDOS_GUARD_TITLE_INDICATORS.search(title_lower):
        signals.add("ddos-guard-title")
    if "ddos-guard" in url_str:
        signals.add("ddos-guard-url")

    # ── 4. CAPTCHA ──────────────────────────────────────────────────
    if CAPTCHA_CONTENT.search(html_lower):
        signals.add("captcha")

    # ── 5. Rate limit ────────────────────────────────────────────────
    if RATE_LIMIT_CONTENT.search(content_lower) or RATE_LIMIT_CONTENT.search(title_lower):
        signals.add("rate-limit")

    # ── 6. Substack redirect ────────────────────────────────────────
    if SUBSTACK_REDIRECT.search(html_lower):
        signals.add("substack-redirect")

    # ── 7. Suspicious patterns (broad net) ──────────────────────────
    suspicious_kw = ["enable javascript", "please enable js", "your browser"]
    for kw in suspicious_kw:
        if kw in html_lower or kw in content_lower:
            signals.add("suspicious-js-required")
            break

    # ── Classify barrier type from strongest signal ─────────────────
    barrier_type: Optional[str] = None
    if any(s.startswith("cloudflare") for s in signals):
        barrier_type = "cloudflare"
    elif any(s.startswith("ddos") for s in signals):
        barrier_type = "ddos-guard"
    elif "captcha" in signals:
        barrier_type = "captcha"
    elif "rate-limit" in signals:
        barrier_type = "rate-limit"
    elif "substack-redirect" in signals:
        barrier_type = "substack-redirect"
    elif "empty" in signals:
        barrier_type = "empty"
    elif signals:
        barrier_type = "suspicious"

    # ── Confidence scoring ──────────────────────────────────────────
    # 1 signal → 0.70, 2 → 0.85, 3+ → 0.95
    # Empty-only with 1 signal is low confidence (likely a legit short page)
    signal_count = len(signals)
    if barrier_type == "empty" and signal_count == 1:
        confidence = 0.65  # below 0.7 — don't escalate on short content alone
    else:
        confidence = min(0.50 + (signal_count * 0.20), 0.95)

    detected = confidence >= 0.70 and barrier_type is not None

    detail_parts = sorted(signals)
    return BarrierInfo(
        detected=detected,
        barrier_type=barrier_type,
        confidence=confidence,
        detail=", ".join(detail_parts),
        title=title,
    )


def is_blocked(info: BarrierInfo, threshold: float = 0.7) -> bool:
    """Shortcut: is the barrier serious enough to escalate?"""
    return info.detected and info.confidence >= threshold
