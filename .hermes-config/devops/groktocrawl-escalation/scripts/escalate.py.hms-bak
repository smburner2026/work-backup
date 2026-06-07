"""escalate — GroktoCrawl four-level escalation logic.

Wires together:
  - groktocrawl_client (HTTP client to the API)
  - workflow_pattern_kit.DAG (serial task layers)
  - workflow_pattern_kit.ToolRegistry (typed actions)
  - workflow_pattern_kit.OutputGate (reject empty/boilerplate)
  - workflow_pattern_kit.LoopDetector (catch escalation loops)
  - workflow_pattern_kit.Dedup (skip duplicate queries)
  - barrier_classifier (MIT extract — detect Cloudflare/CAPTCHA/rate-limit)
  - quality_gates (MIT extract — boilerplate, completeness, block pages)
  - llms_txt_fetcher (MIT extract — Tier 1 /llms.txt check)
  - hermes-web-search-plus plugin (multi-provider routing)

Entry point:
    result = await escalate(query, url=None, ctx=session_ctx)
    if result.success:
        return result.content
    else:
        surface result.escalation_trace to the user

Failure signals (the ONLY valid escalation triggers):
  A — thin search:    web_search returned <=2 results
  B — empty extract:  web_extract returned empty/error/<200 chars
  C — browser crash:  browser tool returned OOM/crashed/timeout
  D — barrier:        barrier_classifier detected Cloudflare/CAPTCHA/etc
  E — need crawl:     task is "all pages" / site map
  F — total failure:  all lower levels failed
  G — quality fail:   quality_gates returned score < 0.3

Levels:
  0   — Hermes native (web_search, web_extract, browser)
        enhanced by hermes-web-search-plus plugin (multi-provider routing)
  0.5 — /llms.txt & quality check (MIT extract, zero Docker)
        barrier_classifier + quality_gates evaluate the response
  1   — SearXNG search via plugin auto-routing fallback
  2   — Smart scrape with barrier_classifier pre-check
  3   — Playwright browser (Docker on-demand only)
  4   — Autonomous agent (Hermes itself + plugin research mode)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, List, Optional

from workflow_pattern_kit import DAG, OutputGate, LoopDetector, Dedup

from groktocrawl_client import (
    GroktoCrawl,
    GrokToCrawlError,
    extract_barrier,
    extract_markdown,
    extract_quality,
)

# MIT extracts from GroktoCrawl — zero Docker dependencies
from barrier_classifier import classify_barrier, BarrierInfo, is_blocked
from quality_gates import assess_quality, QualityReport
from llms_txt_fetcher import fetch_llms_txt, site_has_llms_txt


# ── Failure signals ─────────────────────────────────────────────────────

class Signal(str, Enum):
    A_THIN_SEARCH    = "A_thin_search"
    B_EMPTY_EXTRACT  = "B_empty_extract"
    C_BROWSER_CRASH  = "C_browser_crash"
    D_BARRIER        = "D_barrier"
    E_NEED_CRAWL     = "E_need_crawl"
    F_TOTAL_FAILURE  = "F_total_failure"
    G_QUALITY_FAIL   = "G_quality_fail"


@dataclass
class EscalationResult:
    success: bool
    content: str = ""
    level_reached: int = 0
    escalation_trace: List[Dict[str, Any]] = field(default_factory=list)
    final_signal: Optional[Signal] = None
    full_failure_chain: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "content": self.content,
            "level_reached": self.level_reached,
            "escalation_trace": self.escalation_trace,
            "final_signal": self.final_signal.value if self.final_signal else None,
            "full_failure_chain": self.full_failure_chain,
        }


# ── Trivial DI: pass native Hermes tools through ctx ───────────────────

@dataclass
class NativeTools:
    """Wraps the three Hermes native tools we may need to call."""
    web_search:   Callable[[str, int], Awaitable[dict]]
    web_extract:  Callable[[str], Awaitable[str]]
    browser:      Callable[[str], Awaitable[dict]]


@dataclass
class SessionContext:
    """Per-session state for the escalation logic."""
    native: NativeTools
    gc: Optional[GroktoCrawl] = None
    loop_detector: LoopDetector = field(default_factory=lambda: LoopDetector(window_size=20))
    output_gate: OutputGate = field(default_factory=OutputGate)
    dedup: Dedup = field(default_factory=lambda: Dedup(duplicate_threshold=0.85, possible_threshold=0.65))
    recent_queries: List[str] = field(default_factory=list)
    escalation_count: int = 0
    loop_threshold: int = 3  # after 3 escalations without success, surface to user

    def is_looping(self) -> bool:
        return self.escalation_count >= self.loop_threshold


# ── Detect failure signals ─────────────────────────────────────────────

async def _level0_native(ctx: SessionContext, query: str, url: Optional[str]) -> dict:
    """Try Hermes native tools first. Returns success marker or failure signal."""
    # Step 1: search
    search_result = await ctx.native.web_search(query, limit=10)
    n_results = len(search_result.get("results", []))

    if n_results <= 2:
        return {"success": False, "signal": Signal.A_THIN_SEARCH, "data": search_result}

    # Step 2: extract the top URL if no specific URL given
    target_url = url or search_result.get("results", [{}])[0].get("url")
    if not target_url:
        return {"success": False, "signal": Signal.A_THIN_SEARCH, "data": search_result}

    # Step 2.5: /llms.txt check (Tier 1 — before full extraction)
    llms = fetch_llms_txt(target_url)
    if llms:
        # /llms.txt gives us the whole site in one go — best possible result
        return {"success": True, "content": llms, "url": target_url, "source": "llms.txt"}

    # Step 3: native extract
    try:
        extracted = await ctx.native.web_extract(target_url)
    except Exception as e:
        return {"success": False, "signal": Signal.C_BROWSER_CRASH,
                "data": {"url": target_url, "error": str(e)}}

    if not extracted or len(extracted) < 200:
        return {"success": False, "signal": Signal.B_EMPTY_EXTRACT,
                "data": {"url": target_url, "length": len(extracted or "")}}

    # Step 4: run barrier_classifier + quality_gates on the response
    barrier = classify_barrier(url=target_url, content=extracted)
    if is_blocked(barrier):
        return {"success": False, "signal": Signal.D_BARRIER,
                "data": {"url": target_url, "barrier": barrier.dict() if hasattr(barrier, 'dict') else barrier}}

    quality = assess_quality(markdown=extracted, url=target_url)
    if quality.score < 0.3:
        return {"success": False, "signal": Signal.G_QUALITY_FAIL,
                "data": {"url": target_url, "quality": quality}}

    return {"success": True, "content": extracted, "url": target_url, "quality": quality.score}


# ── Level 1 — SearXNG fallback ────────────────────────────────────────

async def _level1_gc_search(ctx: SessionContext, query: str) -> dict:
    if ctx.gc is None:
        return {"success": False, "signal": Signal.A_THIN_SEARCH,
                "data": {"reason": "groktocrawl_client not initialized"}}
    if not ctx.gc.is_up():
        return {"success": False, "signal": Signal.A_THIN_SEARCH,
                "data": {"reason": "GroktoCrawl stack not running — call `groktocrawl start`"}}
    try:
        result = ctx.gc.search(query, sources="web", limit=5)
        results = result.get("data", result.get("results", []))
        if isinstance(results, list) and len(results) >= 3:
            return {"success": True, "data": result, "url": results[0].get("url")}
        return {"success": False, "signal": Signal.A_THIN_SEARCH, "data": result}
    except GrokToCrawlError as e:
        return {"success": False, "signal": Signal.A_THIN_SEARCH,
                "data": {"error": str(e)}}


# ── Level 2 — three-tier scrape ───────────────────────────────────────

async def _level2_gc_scrape(ctx: SessionContext, url: str) -> dict:
    if ctx.gc is None or not ctx.gc.is_up():
        return {"success": False, "signal": Signal.B_EMPTY_EXTRACT,
                "data": {"reason": "GroktoCrawl stack not running"}}
    try:
        result = ctx.gc.scrape(url)
    except GrokToCrawlError as e:
        return {"success": False, "signal": Signal.C_BROWSER_CRASH,
                "data": {"url": url, "error": str(e)}}

    # Check for structured barrier
    barrier = extract_barrier(result)
    if barrier:
        return {"success": False, "signal": Signal.D_BARRIER,
                "data": {"url": url, "barrier": barrier}}

    markdown = extract_markdown(result)
    quality = extract_quality(result)

    # Run through OutputGate
    reason = ctx.output_gate.check_deliverable(
        summary=markdown,
        is_data_agent=True,
        report_written=quality >= 0.5,
        data_tool_calls=1,
    )
    if reason and len(markdown) < 200:
        return {"success": False, "signal": Signal.B_EMPTY_EXTRACT,
                "data": {"url": url, "length": len(markdown), "quality": quality,
                          "rejection_reason": reason}}
    if not markdown:
        return {"success": False, "signal": Signal.B_EMPTY_EXTRACT,
                "data": {"url": url, "length": 0, "quality": quality}}

    return {"success": True, "content": markdown, "url": url, "quality": quality}


# ── Level 3 — full browser / crawl ────────────────────────────────────

async def _level3_gc_browser(ctx: SessionContext, url: str, signal: Signal) -> dict:
    if ctx.gc is None or not ctx.gc.is_up():
        return {"success": False, "signal": signal,
                "data": {"reason": "GroktoCrawl stack not running"}}

    if signal == Signal.E_NEED_CRAWL:
        try:
            crawl = ctx.gc.crawl(url, max_depth=2, limit=20)
            return {"success": True, "data": crawl, "url": url}
        except GrokToCrawlError as e:
            return {"success": False, "signal": Signal.F_TOTAL_FAILURE,
                    "data": {"error": str(e)}}

    # Signal C (browser crash) or D (barrier) — force Playwright tier
    try:
        result = ctx.gc.scrape_with_browser(url)
    except GrokToCrawlError as e:
        return {"success": False, "signal": Signal.F_TOTAL_FAILURE,
                "data": {"url": url, "error": str(e)}}

    barrier = extract_barrier(result)
    if barrier:
        # Even with full browser, still blocked
        return {"success": False, "signal": Signal.F_TOTAL_FAILURE,
                "data": {"url": url, "barrier": barrier,
                          "note": "Full Playwright render still blocked"}}

    markdown = extract_markdown(result)
    if not markdown or len(markdown) < 200:
        return {"success": False, "signal": Signal.F_TOTAL_FAILURE,
                "data": {"url": url, "length": len(markdown)}}

    return {"success": True, "content": markdown, "url": url}


# ── Level 4 — autonomous agent (last resort) ─────────────────────────

async def _level4_gc_agent(ctx: SessionContext, query: str, trace: List[dict]) -> dict:
    if ctx.gc is None or not ctx.gc.is_up():
        return {"success": False, "signal": Signal.F_TOTAL_FAILURE,
                "data": {"reason": "GroktoCrawl stack not running"}}
    try:
        result = ctx.gc.agent(
            prompt=(
                f"{query}\n\n"
                f"Context: previous escalation attempts failed:\n"
                f"{chr(10).join(str(t) for t in trace)}\n\n"
                f"Try alternative search angles, different archive sources, "
                f"or accept that this information may not be available "
                f"and report back with what you found and what you tried."
            ),
        )
        return {"success": True, "data": result, "url": None}
    except GrokToCrawlError as e:
        return {"success": False, "signal": Signal.F_TOTAL_FAILURE,
                "data": {"error": str(e)}}


# ── Top-level escalation driver ───────────────────────────────────────

async def escalate(query: str, url: Optional[str] = None,
                   ctx: Optional[SessionContext] = None) -> EscalationResult:
    """Run the 4-level escalation tree. Returns full trace on failure."""
    if ctx is None:
        raise ValueError("ctx (SessionContext) is required — pass NativeTools + GroktoCrawl")

    trace: List[dict] = []

    # Dedup pre-check
    if ctx.recent_queries:
        dedup_result = ctx.dedup.compare_many(query, ctx.recent_queries)
        if dedup_result.is_duplicate:
            matched = dedup_result.matched_with
            return EscalationResult(
                success=False,
                full_failure_chain=(
                    f"Query is a duplicate of recent failure: {matched!r}\n"
                    f"Skipping re-escalation. If you want to retry anyway, "
                    f"clear ctx.recent_queries first."
                ),
            )

    # ── Level 0: native ─────────────────────────────────────────────
    ctx.loop_detector.record_action("level0_native", {"query": query})
    r0 = await _level0_native(ctx, query, url)
    trace.append({"level": 0, "result": {k: v for k, v in r0.items() if k != "data"},
                  "data_summary": _summarize(r0.get("data"))})
    if r0["success"]:
        ctx.recent_queries.append(query)
        return EscalationResult(success=True, content=r0["content"],
                                  level_reached=0)

    # Loop guard: if we keep escalating, stop
    ctx.escalation_count += 1
    if ctx.is_looping():
        return EscalationResult(
            success=False,
            level_reached=0,
            escalation_trace=trace,
            final_signal=r0.get("signal"),
            full_failure_chain=_format_chain(trace, "loop detected — escalating without progress"),
        )

    # ── Level 1: GC search ──────────────────────────────────────────
    ctx.loop_detector.record_action("level1_gc_search", {"query": query})
    r1 = await _level1_gc_search(ctx, query)
    trace.append({"level": 1, "result": {k: v for k, v in r1.items() if k != "data"},
                  "data_summary": _summarize(r1.get("data"))})
    if r1["success"]:
        target_url = url or r1.get("url")
        # Try Level 2 immediately to extract
        r2 = await _level2_gc_scrape(ctx, target_url)
        trace.append({"level": 2, "result": {k: v for k, v in r2.items() if k != "data"},
                      "data_summary": _summarize(r2.get("data"))})
        if r2["success"]:
            ctx.recent_queries.append(query)
            return EscalationResult(success=True, content=r2["content"],
                                      level_reached=2)
        # Level 1 found a URL but Level 2 couldn't extract — fall through to Level 3
        signal = r2.get("signal", Signal.B_EMPTY_EXTRACT)
        target_url = target_url or r1.get("url")
    else:
        signal = r0.get("signal")
        target_url = url

    if not target_url:
        return EscalationResult(
            success=False, level_reached=1, escalation_trace=trace,
            final_signal=Signal.A_THIN_SEARCH,
            full_failure_chain=_format_chain(trace, "no URL to crawl"),
        )

    # ── Level 3: full browser / crawl ───────────────────────────────
    ctx.loop_detector.record_action("level3_gc_browser", {"url": target_url})
    r3 = await _level3_gc_browser(ctx, target_url, signal)
    trace.append({"level": 3, "result": {k: v for k, v in r3.items() if k != "data"},
                  "data_summary": _summarize(r3.get("data"))})
    if r3["success"]:
        if r3.get("content"):
            ctx.recent_queries.append(query)
            return EscalationResult(success=True, content=r3["content"],
                                      level_reached=3)
        # crawl/map result — return raw data
        ctx.recent_queries.append(query)
        return EscalationResult(success=True,
                                  content=str(r3.get("data", "")),
                                  level_reached=3)

    # ── Level 4: agent (last resort) ────────────────────────────────
    ctx.loop_detector.record_action("level4_gc_agent", {"query": query})
    r4 = await _level4_gc_agent(ctx, query, trace)
    trace.append({"level": 4, "result": {k: v for k, v in r4.items() if k != "data"},
                  "data_summary": _summarize(r4.get("data"))})
    if r4["success"]:
        return EscalationResult(success=True,
                                  content=str(r4.get("data", "")),
                                  level_reached=4)

    # All levels failed
    return EscalationResult(
        success=False,
        level_reached=4,
        escalation_trace=trace,
        final_signal=Signal.F_TOTAL_FAILURE,
        full_failure_chain=_format_chain(trace, "all 4 levels failed"),
    )


# ── Formatting helpers ────────────────────────────────────────────────

def _summarize(data: Any) -> str:
    """Compact string summary of a payload, safe for trace logs."""
    if data is None:
        return "None"
    if isinstance(data, str):
        return data[:120]
    if isinstance(data, dict):
        keys = list(data.keys())[:6]
        return "{" + ", ".join(f"{k}={repr(str(v))[:40]}" for k, v in data.items() if k in keys) + "}"
    if isinstance(data, list):
        return f"list[{len(data)}]: {str(data[0])[:80] if data else ''}"
    return str(data)[:120]


def _format_chain(trace: List[dict], footer: str) -> str:
    lines = ["GroktoCrawl escalation trace:", ""]
    for entry in trace:
        lvl = entry.get("level", "?")
        result = entry.get("result", {})
        success = result.get("success")
        signal = result.get("signal")
        marker = "✓" if success else "✗"
        sig_str = f" [{signal.value}]" if signal else ""
        lines.append(f"  {marker} Level {lvl}{sig_str}: {entry.get('data_summary', '')}")
    lines.append("")
    lines.append(f"→ {footer}")
    return "\n".join(lines)
