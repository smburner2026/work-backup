"""
loop_detector.py — Action repetition and page stagnation detection.

Pattern borrowed from browser-use's ActionLoopDetector. Tracks action
similarity via normalized hashing and page state via fingerprinting.
Emits escalating awareness nudges so the LLM can self-correct — never
hard-blocks.

Usage:
    detector = LoopDetector(window_size=20)
    
    # After each action:
    detector.record_action("click", {"index": 3})
    detector.record_action("search", {"query": "NVDA stock"})
    detector.record_page_state(url="...", dom_text="...", element_count=42)
    
    # Before next LLM call:
    nudge = detector.get_nudge_message()
    if nudge:
        messages.append({"role": "user", "content": nudge})
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any


# ── Page Fingerprint ───────────────────────────────────────────────


@dataclass(frozen=True)
class PageFingerprint:
    """Lightweight fingerprint of the browser/page state."""

    url: str
    element_count: int
    text_hash: str  # SHA-256 first 16 chars

    @staticmethod
    def from_state(url: str, dom_text: str, element_count: int) -> PageFingerprint:
        text_hash = hashlib.sha256(dom_text.encode("utf-8", errors="replace")).hexdigest()[:16]
        return PageFingerprint(url=url, element_count=element_count, text_hash=text_hash)


# ── Action Hashing ─────────────────────────────────────────────────


def _normalize_search_query(text: str) -> str:
    """Lowercase, strip punctuation, sort unique tokens."""
    tokens = sorted(set(re.sub(r"[^\w\s]", " ", text.lower()).split()))
    return " ".join(tokens)


def compute_action_hash(action_name: str, params: dict[str, Any]) -> str:
    """Stable hash for an action based on type + normalized parameters.

    Normalization rules mirror browser-use's approach:
    - search: sort tokens, ignore engine
    - click/input: hash by index (+ normalized text for input)
    - navigate: use full URL
    - scroll: hash by direction + index
    - default: action_name + sorted params
    """
    if action_name == "search":
        query = _normalize_search_query(str(params.get("query", "")))
        engine = params.get("engine", "google")
        signature = f"search|{engine}|{query}"
    elif action_name in ("click", "input", "select", "type"):
        index = params.get("index")
        if action_name == "input" or action_name == "type":
            text = str(params.get("text", "")).strip().lower()
            signature = f"{action_name}|{index}|{text}"
        else:
            signature = f"{action_name}|{index}"
    elif action_name == "navigate":
        signature = f"navigate|{params.get('url', '')}"
    elif action_name == "scroll":
        direction = "down" if params.get("down", True) else "up"
        index = params.get("index")
        signature = f"scroll|{direction}|{index}"
    else:
        filtered = {k: v for k, v in sorted(params.items()) if v is not None}
        signature = f"{action_name}|{json.dumps(filtered, sort_keys=True, default=str)}"

    return hashlib.sha256(signature.encode("utf-8")).hexdigest()[:12]


# ── Loop Detector ──────────────────────────────────────────────────


@dataclass
class LoopDetector:
    """Tracks action repetition and page stagnation. Emits nudges, never blocks.

    Attributes:
        window_size: Rolling window for action hash tracking.
        max_repetition_before_nudge: Nudge levels at 5, 8, 12 repeats.
        max_stagnant_before_nudge: Nudge after N consecutive same-page states.
    """

    window_size: int = 20
    max_repetition_before_nudge: tuple[int, int, int] = (5, 8, 12)
    max_stagnant_before_nudge: int = 5

    # Rolling windows
    recent_action_hashes: list[str] = field(default_factory=list)
    recent_page_fingerprints: list[PageFingerprint] = field(default_factory=list)

    # Computed state
    max_repetition_count: int = 0
    most_repeated_hash: str | None = None
    consecutive_stagnant_pages: int = 0

    # Suppression: don't nudge more than once every N calls
    _last_nudge_tick: int = 0
    _nudge_cooldown: int = 3  # steps between nudges

    def record_action(self, action_name: str, params: dict[str, Any]) -> None:
        """Record an action and update repetition stats."""
        h = compute_action_hash(action_name, params)
        self.recent_action_hashes.append(h)
        # Trim to window
        if len(self.recent_action_hashes) > self.window_size:
            self.recent_action_hashes = self.recent_action_hashes[-self.window_size :]
        self._update_repetition_stats()

    def record_page_state(self, url: str, dom_text: str, element_count: int) -> None:
        """Record page fingerprint and update stagnation count."""
        fp = PageFingerprint.from_state(url, dom_text, element_count)
        if self.recent_page_fingerprints and self.recent_page_fingerprints[-1] == fp:
            self.consecutive_stagnant_pages += 1
        else:
            self.consecutive_stagnant_pages = 0
        self.recent_page_fingerprints.append(fp)
        # Keep last 5
        if len(self.recent_page_fingerprints) > 5:
            self.recent_page_fingerprints = self.recent_page_fingerprints[-5:]

    def _update_repetition_stats(self) -> None:
        """Recompute max_repetition_count from the current window."""
        if not self.recent_action_hashes:
            self.max_repetition_count = 0
            self.most_repeated_hash = None
            return
        counts: dict[str, int] = {}
        for h in self.recent_action_hashes:
            counts[h] = counts.get(h, 0) + 1
        self.most_repeated_hash = max(counts, key=lambda k: counts[k])
        self.max_repetition_count = counts[self.most_repeated_hash]

    def get_nudge_message(self, tick: int = 0) -> str | None:
        """Return escalating nudge or None.

        Args:
            tick: Step counter. Used for cooldown suppression.

        Returns:
            Nudge text if a loop is detected and cooldown has passed.
        """
        # Cooldown check: only suppress if a nudge was already emitted
        if tick and self._last_nudge_tick > 0 and tick - self._last_nudge_tick < self._nudge_cooldown:
            return None

        messages: list[str] = []
        mid, high, critical = self.max_repetition_before_nudge

        if self.max_repetition_count >= critical:
            messages.append(
                f"You have repeated a similar action {self.max_repetition_count} times "
                f"in the last {len(self.recent_action_hashes)} actions. "
                "If you're making progress with each repetition, keep going. "
                "If not, try a fundamentally different approach."
            )
        elif self.max_repetition_count >= high:
            messages.append(
                f"You have repeated a similar action {self.max_repetition_count} times "
                f"in the last {len(self.recent_action_hashes)} actions. "
                "Are you still making progress? If so, carry on. "
                "Otherwise, try a different approach."
            )
        elif self.max_repetition_count >= mid:
            messages.append(
                f"You have repeated a similar action {self.max_repetition_count} times "
                f"in the last {len(self.recent_action_hashes)} actions. "
                "If this is intentional and making progress, carry on. "
                "If not, it might be worth reconsidering."
            )

        if self.consecutive_stagnant_pages >= self.max_stagnant_before_nudge:
            messages.append(
                f"The page content has not changed across {self.consecutive_stagnant_pages} "
                f"consecutive actions. Your actions might not be having the intended effect. "
                f"Try a different element or approach."
            )

        if messages:
            self._last_nudge_tick = tick
            return "\n\n".join(messages)
        return None

    def reset(self) -> None:
        """Clear all tracking state."""
        self.recent_action_hashes.clear()
        self.recent_page_fingerprints.clear()
        self.max_repetition_count = 0
        self.most_repeated_hash = None
        self.consecutive_stagnant_pages = 0
        self._last_nudge_tick = 0

    def summary(self) -> dict:
        """Return current detector state as a dict."""
        return {
            "window_size": self.window_size,
            "current_repetition_count": self.max_repetition_count,
            "most_repeated_hash": self.most_repeated_hash,
            "consecutive_stagnant_pages": self.consecutive_stagnant_pages,
            "window_fill": len(self.recent_action_hashes),
        }
