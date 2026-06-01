"""
dag_orchestrator.py — Task dependency graph with topological layering.

Pattern borrowed from Vibe-Trading's SwarmRuntime. Lets you define tasks
with dependencies, then executes them in topological order — parallel
within each layer, serial between layers.

Usage:
    dag = DAG()
    
    @dag.task(depends_on=[])
    async def fetch_macro():
        return {"gdp": "2.1%", "cpi": "3.2%"}
    
    @dag.task(depends_on=["fetch_macro"])
    async def analyze_sector(macro):
        return {"sector": "tech", "macro_gdp": macro["gdp"]}
    
    @dag.task(depends_on=["analyze_sector"])
    async def generate_report(sector):
        return {"report": f"Sector: {sector['sector']}"}
    
    results = await dag.run()
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

# Sentinel for skipped tasks (distinct from None which is a valid result)
_SKIPPED = object()


# ── Models ─────────────────────────────────────────────────────────


@dataclass
class TaskNode:
    """A single task in the DAG."""

    id: str
    fn: Callable[..., Coroutine[Any, Any, Any] | Any]
    depends_on: list[str]
    result: Any = None
    error: str | None = None
    status: str = "pending"
    input_from: dict[str, str] = field(default_factory=dict)


@dataclass
class DAGResult:
    """Result of a full DAG execution."""

    task_results: dict[str, Any]
    task_errors: dict[str, str | None]
    task_statuses: dict[str, str]
    execution_order: list[list[str]]

    def success(self, task_id: str) -> bool:
        return self.task_statuses.get(task_id) == "completed"

    def output(self, task_id: str) -> Any:
        return self.task_results.get(task_id)

    def failed_tasks(self) -> list[str]:
        return [tid for tid, st in self.task_statuses.items() if st == "failed"]

    @property
    def all_succeeded(self) -> bool:
        return all(st == "completed" for st in self.task_statuses.values())


# ── DAG Engine ─────────────────────────────────────────────────────


class DAG:
    """Directed Acyclic Graph task orchestrator."""

    def __init__(self, max_concurrency: int = 4):
        self._tasks: dict[str, TaskNode] = {}
        self.max_concurrency = max_concurrency

    # ── Registration ────────────────────────────────────────────────

    def task(
        self,
        task_id: str | None = None,
        depends_on: list[str] | None = None,
        input_from: dict[str, str] | None = None,
    ):
        """Decorator: register an async function as a DAG task."""

        def decorator(fn: Callable) -> Callable:
            tid = task_id or fn.__name__
            self._tasks[tid] = TaskNode(
                id=tid,
                fn=fn,
                depends_on=depends_on or [],
                input_from=input_from or {},
            )
            return fn

        return decorator

    # ── Validation ──────────────────────────────────────────────────

    def validate(self) -> list[str]:
        """Validate the DAG. Returns list of error messages (empty = valid)."""
        errors: list[str] = []
        all_ids = set(self._tasks.keys())

        for tid, node in self._tasks.items():
            for dep in node.depends_on:
                if dep not in all_ids:
                    errors.append(f"Task '{tid}' depends on unknown task '{dep}'")

        # Cycle detection via DFS
        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {tid: WHITE for tid in all_ids}
        path: list[str] = []

        def dfs(node_id: str) -> bool:
            color[node_id] = GRAY
            path.append(node_id)
            node = self._tasks.get(node_id)
            if node:
                for dep in node.depends_on:
                    if dep in color:
                        if color[dep] == GRAY:
                            cycle_path = " -> ".join(path[path.index(dep) :] + [dep])
                            errors.append(f"Cycle detected: {cycle_path}")
                            path.pop()
                            return True
                        elif color[dep] == WHITE:
                            if dfs(dep):
                                path.pop()
                                return True
            path.pop()
            color[node_id] = BLACK
            return False

        for tid in all_ids:
            if color[tid] == WHITE:
                dfs(tid)

        return errors

    # ── Topological layering ────────────────────────────────────────

    def topological_layers(self) -> list[list[str]]:
        """Return task IDs grouped by topological layer."""
        in_degree: dict[str, int] = {}
        for tid in self._tasks:
            in_degree[tid] = len(self._tasks[tid].depends_on)

        queue = deque(tid for tid, deg in in_degree.items() if deg == 0)
        layers: list[list[str]] = []

        while queue:
            layer = []
            for _ in range(len(queue)):
                tid = queue.popleft()
                layer.append(tid)

            for tid in layer:
                for other_id, other in self._tasks.items():
                    if tid in other.depends_on:
                        in_degree[other_id] -= 1
                        if in_degree[other_id] == 0:
                            queue.append(other_id)

            if layer:
                layers.append(layer)

        return layers

    # ── Execution ───────────────────────────────────────────────────

    async def run(self, shared_context: dict[str, Any] | None = None) -> DAGResult:
        """Execute all tasks in topological order."""
        errors = self.validate()
        if errors:
            raise ValueError("DAG validation failed:\n" + "\n".join(errors))

        layers = self.topological_layers()
        task_results: dict[str, Any] = {}
        task_errors: dict[str, str | None] = {}
        task_statuses: dict[str, str] = {}

        ctx = shared_context or {}

        for layer_idx, layer_tasks in enumerate(layers):
            async def run_task(tid: str) -> tuple[str, Any, str | None]:
                node = self._tasks[tid]

                # Skip if any upstream dependency failed
                upstream_failed = [
                    dep for dep in node.depends_on
                    if task_statuses.get(dep) == "failed"
                ]
                if upstream_failed:
                    return tid, _SKIPPED, None

                # Build kwargs from input_from + convenience
                kwargs: dict[str, Any] = {}
                already_mapped = set(node.input_from.values())
                for param_name, upstream_id in node.input_from.items():
                    if upstream_id in task_results:
                        kwargs[param_name] = task_results[upstream_id]

                for dep_id in node.depends_on:
                    if dep_id in already_mapped:
                        continue
                    if dep_id in task_results:
                        kwargs[dep_id] = task_results[dep_id]

                # Shared context — inject individual keys if the function accepts them
                sig = inspect.signature(node.fn)
                fn_params = {p.name for p in sig.parameters.values()}
                for ctx_key, ctx_val in ctx.items():
                    if ctx_key in fn_params and ctx_key not in kwargs:
                        kwargs[ctx_key] = ctx_val
                # Also pass entire ctx if function accepts it
                if "ctx" in fn_params:
                    kwargs["ctx"] = ctx

                try:
                    result = await node.fn(**kwargs)
                    return tid, result, None
                except Exception as e:
                    return tid, None, str(e)

            sem = asyncio.Semaphore(self.max_concurrency)

            async def bounded(tid: str):
                async with sem:
                    return await run_task(tid)

            tasks = [bounded(tid) for tid in layer_tasks]
            completed = await asyncio.gather(*tasks)

            for tid, result, error in completed:
                task_results[tid] = result if result is not _SKIPPED else None
                task_errors[tid] = error
                if error:
                    task_statuses[tid] = "failed"
                    self._cascade_skip(tid, task_statuses)
                elif result is _SKIPPED:
                    task_statuses[tid] = "skipped"
                else:
                    task_statuses[tid] = "completed"

        return DAGResult(
            task_results=task_results,
            task_errors=task_errors,
            task_statuses=task_statuses,
            execution_order=layers,
        )

    def _cascade_skip(self, failed_id: str, statuses: dict[str, str]) -> None:
        """Cascade 'skipped' status downstream from a failed task."""
        for tid, node in self._tasks.items():
            if tid == failed_id:
                continue
            if failed_id in node.depends_on and statuses.get(tid) not in (
                "completed", "failed", "skipped"
            ):
                statuses[tid] = "skipped"
                self._cascade_skip(tid, statuses)


# ── Convenience ────────────────────────────────────────────────────


def simple_chain(*fns: Callable) -> DAG:
    """Build a linear chain DAG from ordered functions."""
    dag = DAG()
    previous_id = None
    for i, fn in enumerate(fns):
        tid = fn.__name__ or f"task_{i}"
        deps = [previous_id] if previous_id else []
        input_from = {"prev": previous_id} if previous_id else {}
        dag.task(task_id=tid, depends_on=deps, input_from=input_from)(fn)
        previous_id = tid
    return dag
