"""
workflow-pattern-kit — Reusable agent workflow architecture patterns.

Patterns adapted from:
  - browser-use (tool registry, loop detection, event-driven browser)
  - Vibe-Trading (DAG orchestration, output contracts, grounding)

Modules:
  tool_registry:   Typed action registration with context injection
  loop_detector:   Action repetition and page stagnation detection
  output_gate:     Deliverable quality classification
  dag_orchestrator: Task dependency graph with topological layering
"""

from workflow_pattern_kit.tool_registry import ToolRegistry, register_core_actions
from workflow_pattern_kit.loop_detector import LoopDetector, PageFingerprint, compute_action_hash
from workflow_pattern_kit.output_gate import OutputGate
from workflow_pattern_kit.dag_orchestrator import DAG, DAGResult, simple_chain

__all__ = [
    "ToolRegistry",
    "register_core_actions",
    "LoopDetector",
    "PageFingerprint",
    "compute_action_hash",
    "OutputGate",
    "DAG",
    "DAGResult",
    "simple_chain",
]
