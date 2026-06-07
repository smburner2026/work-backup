"""quality_gates — Extracted from GroktoCrawl v0.6.0 (MIT License).

Post-extraction content quality assessment. Detects boilerplate,
incomplete content, and block pages that rendered as text.

Usage:
    from quality_gates import assess_quality, QualityReport

    report = assess_quality(markdown=text, html=page_html, url="https://...")
    if report.score < 0.5:
        print(f"Low quality ({report.score:.2f}): {report.detail}")
        # escalate to alternative backend
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QualityReport:
    """Quality assessment result. Non-blocking — consumers set tolerance."""
    score: float = 0.0           # 0.0–1.0 composite
    checks: dict[str, str] = field(default_factory=dict)
    # "pass" | "warn" | "fail" per check
    detail: str = ""


# ── Block page signatures ───────────────────────────────────────────

_BLOCK_PATTERNS = [
    # JavaScript required
    r"please enable javascript",
    r"enable javascript to continue",
    r"javascript is required",
    r"please turn javascript on",
    # Bot challenges
    r"please verify you are (?:a )?human",
    r"we need to make sure you(?:'re| are) not a robot",
    r"checking your browser",
    r"we are checking your browser",
    # Access control
    r"access denied",
    r"you have been blocked",
    r"your (?:IP|access) has been blocked",
    # Rate limiting
    r"too many requests",
    r"rate limit",
    # Session
    r"your session has expired",
    r"session timed?\s?out",
    # Generic
    r"cloudflare",
    r"attention required",
    r"just a moment",
    # Geo
    r"not available in your country",
    r"not available in your region",
    r"geo-?restriction",
    r"content (?:is )?not available",
    # Paywall
    r"subscribe to continue",
    r"sign up to read more",
    r"members-?only",
    r"this content is for (?:members|subscribers)",
    # Errors
    r"404 not found",
    r"403 forbidden",
    r"500 error",
    r"internal server error",
    r"page not found",
    r"something went wrong",
    # CAPTCHA
    r"hcaptcha",
    r"recaptcha",
    r"captcha",
    # Maintenance
    r"under maintenance",
    r"temporarily unavailable",
]

_BLOCK_REGEX = re.compile(
    "|".join(f"(?:{p})" for p in _BLOCK_PATTERNS),
    re.I,
)


def assess_quality(
    markdown: str = "",
    html: str = "",
    url: str = "",
    title: str = "",
) -> QualityReport:
    """Run three quality gates on extracted content.

    Args:
        markdown: The extracted text/markdown content.
        html: Raw HTML (for boilerplate analysis).
        url: Original URL (for context).
        title: Page title.

    Returns:
        QualityReport with composite score 0.0–1.0,
        per-check status, and detail string.
    """
    checks: dict[str, str] = {}

    score_boilerplate, status_boilerplate = _check_boilerplate(markdown, url)
    score_completeness, status_completeness = _check_completeness(markdown, title)
    score_block, status_block = _check_block_page(markdown, html)

    checks["boilerplate"] = status_boilerplate
    checks["completeness"] = status_completeness
    checks["block_detected"] = status_block

    # Weighted composite: 0.3 boilerplate + 0.3 completeness + 0.4 block
    overall = score_boilerplate * 0.3 + score_completeness * 0.3 + score_block * 0.4
    overall = round(overall, 2)

    # Detail string
    fails = [k for k, v in checks.items() if v == "fail"]
    warns = [k for k, v in checks.items() if v == "warn"]
    if not fails and not warns:
        detail = "all checks passed"
    elif fails and not warns:
        detail = f"fails: {', '.join(fails)}"
    elif not fails:
        detail = f"warnings: {', '.join(warns)}"
    else:
        detail = f"fails: {', '.join(fails)}; warnings: {', '.join(warns)}"

    return QualityReport(score=overall, checks=checks, detail=detail)


# ── Gate 1: Boilerplate detection ───────────────────────────────────

def _check_boilerplate(markdown: str, url: str) -> tuple[float, str]:
    """Detect link-heavy boilerplate pages (nav-heavy, no substance).

    Scores:
        1.0  → pass (≥5 substantive paragraphs)
        0.85 → pass (≥3 substantive paragraphs)
        0.6  → warn (≥1 substantive paragraph but high link density)
        0.4  → warn (high link density, 1-2 substantive)
        0.3  → fail (no substantive content)
        0.2  → fail (link-heavy, <2 substantive)
    """
    if not markdown or len(markdown) < 50:
        return 0.3, "fail"

    lines = markdown.split("\n")
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return 0.3, "fail"

    # Link-heavy lines: more markdown links than text characters
    link_lines = 0
    for line in non_empty:
        links = len(re.findall(r"\[([^\]]*)\]\([^)]+\)", line))
        if links > 0 and len(line) < 120:
            link_lines += 1

    # Substantive paragraphs: ≥60 chars without markdown links
    substantive = 0
    for line in non_empty:
        clean = re.sub(r"\[([^\]]*)\]\([^)]+\)", "", line)
        if len(clean) >= 60:
            substantive += 1

    link_ratio = link_lines / len(non_empty) if non_empty else 0

    if substantive >= 5:
        return 1.0, "pass"
    if substantive >= 3:
        return 0.85, "pass"
    if substantive >= 1:
        if link_ratio > 0.7:
            return 0.4, "warn"
        return 0.6, "warn"
    if link_ratio > 0.5:
        if link_ratio > 0.7:
            return 0.2, "fail"
        return 0.4, "warn"
    return 0.3, "fail"


# ── Gate 2: Completeness ────────────────────────────────────────────

def _check_completeness(markdown: str, title: str) -> tuple[float, str]:
    """Check content length, title quality, and paragraph structure.

    Scores:
        1.0  → pass (≥1000 chars, ≥2 paras, title ok)
        0.85 → pass (≥500 chars, ≥2 paras)
        0.6  → warn (≥200 chars)
        0.4  → warn (<200 chars but ≥2 paras)
        0.3  → warn (<200 chars)
        0.1  → fail (<200 chars, <2 paras)
    """
    if not markdown:
        return 0.1, "fail"

    char_count = len(markdown)
    paras = markdown.split("\n\n")
    paras_count = len([p for p in paras if p.strip()])
    title_ok = len(title) >= 10 if title else True

    if char_count >= 1000 and paras_count >= 2 and title_ok:
        return 1.0, "pass"
    if char_count >= 500 and paras_count >= 2:
        return 0.85, "pass"
    if char_count >= 200:
        return 0.6, "warn"
    if paras_count >= 2:
        return 0.4, "warn"
    return 0.1, "fail"


# ── Gate 3: Block page detection ────────────────────────────────────

def _check_block_page(markdown: str, html: str) -> tuple[float, str]:
    """Detect block/error/JS-required pages that rendered as text.

    Uses regex matching against a comprehensive pattern list.
    Returns 0.05 (fail) if 3+ patterns match, 0.15 (fail) if 2,
    0.3 (warn) if 1, 1.0 (pass) if none.
    """
    if markdown is None and html is None:
        return 1.0, "pass"
    if not markdown or len(markdown.strip()) < 50:
        # Almost empty content — even without block patterns, this is useless
        return 0.2, "fail"

    text = (markdown or "") + "\n" + (html or "")
    matches = _BLOCK_REGEX.findall(text)
    match_count = len([m for m in matches if m])

    if match_count >= 3:
        return 0.05, "fail"
    if match_count >= 2:
        return 0.15, "fail"
    if match_count >= 1:
        return 0.3, "warn"
    return 1.0, "pass"
