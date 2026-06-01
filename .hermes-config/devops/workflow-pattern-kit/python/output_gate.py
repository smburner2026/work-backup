"""
output_gate.py — Classify agent deliverables as valid work vs. plan stubs.

Pattern borrowed from Vibe-Trading's _classify_deliverable. The gate checks
that the agent produced substantive output — not a plan describing what it
*will* do, not a raw tool-result envelope, not hallucinated/mock data.

Usage:
    gate = OutputGate()
    
    reason = gate.check_deliverable(
        summary=agent_output,
        is_data_agent=True,       # Has data-fetching tools?
        report_written=True,      # Wrote a final file?
        data_tool_calls=5,        # How many data tools called?
    )
    if reason:
        print(f"Rejected: {reason}")  # Send back to agent
    else:
        print("Good output")          # Accept
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# ── Constants ──────────────────────────────────────────────────────

# Generic tools that don't fetch/analyze data
_GENERIC_TOOLS = {"bash", "read_file", "write_file", "load_skill", "edit_file", "echo", "cat", "ls"}

# Markers of unparsed tool-call markup in output
_UNPARSED_TOOL_MARKERS = (
    "<\uff5ctool\u2581calls\u2581begin\uff5c>",
    "<tool_calls_begin>",
    "<tool_call_begin>",
    "<tool_sep>",
    "tool\u2581sep",
    "<function_calls>",
    "<invoke>",
)

# Markers indicating fabricated/placeholder data
_FABRICATION_MARKERS = (
    "mock data",
    "without actual data",
    "fabricated data",
    "placeholder data",
    "simulated data",
    "example data",
    "dummy data",
)

# Plan-only prefixes (output is a plan, not execution)
_PLAN_PREFIXES = (
    "# phase 1", "## phase 1", "### phase 1",
    "phase 1 \u2014 plan", "phase 1 - plan", "phase 1: plan",
    "# plan", "## plan", "### plan", "**plan**",
    "## next steps",
    "## recommended approach",
    "## proposed solution",
    "## approach",
    "**approach:**",
)

_HANDOFF_TAILS = (
    "execute", "execute.", "execute:",
    "skills.", "skills",
    "proceed?", "proceed.",
    "without writing files.",
    "let me adjust the approach",
    "let me adjust the approach.",
    "stand by for final synthesis.",
)

# ── Gate ───────────────────────────────────────────────────────────


@dataclass
class OutputGate:
    """Check agent output against deliverable quality contracts.

    The gate is lenient by design — it flags problems without
    hard-blocking. The caller decides whether to reject.
    """

    # Content thresholds
    min_content_length: int = 20
    max_plan_only_length: int = 600  # If text is short AND plan-like → reject

    def check_deliverable(
        self,
        summary: str,
        *,
        is_data_agent: bool = True,
        report_written: bool = False,
        data_tool_calls: int = 0,
    ) -> str | None:
        """Check if the output meets the delivery contract.

        Returns:
            None if the output passes all checks.
            A string reason explaining why it was rejected.
        """
        text = (summary or "").strip()
        low = text.lower()

        # 1. Empty
        if not text:
            return "empty deliverable"

        # 2. Unparsed tool-call markup
        if any(m in text for m in _UNPARSED_TOOL_MARKERS):
            return "unparsed tool-call markup (provider did not parse tool calls) — re-run with correct output format"

        # 3. Explicitly fabricated / mock data
        if any(m in low for m in _FABRICATION_MARKERS):
            return "explicitly fabricated or mock data — use real tool results"

        # 4. Raw tool-result envelope
        if text.startswith("{") and '"status"' in text[:40] and ('"content"' in text[:300] or '"ok"' in text[:40]):
            return "raw tool-result envelope, not analysis — extract and summarize the result"

        # 5. Plan-only stub
        if low.startswith(_PLAN_PREFIXES):
            tail = low.rsplit("phase 2", 1)[-1].strip() if "phase 2" in low else ""
            is_stub = (
                len(text) < self.max_plan_only_length
                or low.rstrip().endswith(_HANDOFF_TAILS)
                or ("phase 2" in low and len(tail) < 80)
            )
            if is_stub:
                return (
                    "plan-only stub with no executed analysis or output — "
                    "execute the plan instead of describing it"
                )

        # 6. Data agent with no evidence
        if is_data_agent and not report_written and data_tool_calls == 0:
            return (
                "data agent produced no tool calls and no report.md — "
                "use available tools to fetch real data before concluding"
            )

        # 7. Short non-answer
        if len(text) < self.min_content_length:
            return f"deliverable too short ({len(text)} chars) — provide a substantive response"

        return None  # Passed all checks

    # ── Convenience wrappers ────────────────────────────────────────

    def is_valid_deliverable(
        self,
        summary: str,
        **kwargs,
    ) -> bool:
        """Return True if the output passes all checks."""
        return self.check_deliverable(summary, **kwargs) is None

    def check_with_report(
        self,
        summary: str,
        report_path: str | None = None,
        data_tool_calls: int = 0,
        toolset: set[str] | None = None,
    ) -> str | None:
        """Convenience check that infers is_data_agent from toolset.

        Args:
            summary: The agent's output text.
            report_path: Path to a written report file (checks existence).
            data_tool_calls: Number of non-generic tool calls made.
            toolset: Set of tool names the agent has. Data agent = has
                at least one tool beyond the generic kit.

        Returns:
            Reason string or None.
        """
        tools = toolset or set()
        is_data = bool(tools - _GENERIC_TOOLS) if tools else True

        import os as _os
        report_written = bool(report_path and _os.path.isfile(report_path))

        return self.check_deliverable(
            summary=summary,
            is_data_agent=is_data,
            report_written=report_written,
            data_tool_calls=data_tool_calls,
        )
