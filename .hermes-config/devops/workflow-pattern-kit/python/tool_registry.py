"""
tool_registry.py — Typed action registration with context injection.

Pattern borrowed from browser-use's Registry system. Lets you register
typed actions (Pydannel models) and auto-injects shared context so
handlers don't need to import infrastructure.

Usage:
    registry = ToolRegistry()
    
    @registry.action("Search the web", param_model=SearchParams)
    async def search_google(params: SearchParams, browser_session=None, file_system=None):
        # params.query, params.limit — typed
        # browser_session injected automatically
        ...
    
    # LLM sees:
    registry.get_prompt_description()
    # > search_google(query: str, limit: int) — Search the web
    
    # Execution:
    result = await registry.execute("search_google", {"query": "hello"})
"""

from __future__ import annotations

import inspect
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Generic, TypeVar

from pydantic import BaseModel, create_model

logger = logging.getLogger(__name__)

# ── Types ──────────────────────────────────────────────────────────

Context = TypeVar("Context")

# Known context parameters the registry can inject.
# Map param_name -> (type, description)
CONTEXT_PARAMS: dict[str, tuple[type | None, str]] = {
    "browser_session": (None, "Current browser session for DOM/page operations"),
    "file_system": (None, "Persistent file system for reading/writing files"),
    "page_url": (str, "Current page URL, for domain-filtering actions"),
    "cdp_client": (None, "Chrome DevTools Protocol client"),
    "has_sensitive_data": (bool, "Whether sensitive data placeholders are active"),
    "available_file_paths": (list, "Files available for download/upload"),
}

# ── Data models ────────────────────────────────────────────────────


@dataclass
class RegisteredAction:
    """A single registered action with its metadata."""

    name: str
    description: str
    fn: Callable[..., Coroutine[Any, Any, Any] | Any]
    param_model: type[BaseModel]
    is_async: bool
    domain_filter: str | None = None  # e.g. "github.com" — only show on this domain


@dataclass
class ActionRegistry:
    """Internal storage for registered actions."""

    actions: dict[str, RegisteredAction] = field(default_factory=dict)
    exclude_actions: set[str] = field(default_factory=set)


# ── Param model builder ────────────────────────────────────────────


def _build_param_model(
    fn: Callable,
    skip_params: set[str],
) -> type[BaseModel]:
    """Auto-build a Pydantic param model from a function's signature.

    Only includes params NOT in skip_params (context params).

    If the first non-skip param is already a BaseModel subclass, returns it
    directly (Type 1 pattern: function accepts a single Pydantic model).
    Otherwise builds a flat model from individual params (Type 2 pattern).
    """
    sig = inspect.signature(fn)

    # Collect non-skip, non-self params
    action_params: list[inspect.Parameter] = []
    for name, param in sig.parameters.items():
        if name in skip_params or name in ("self", "cls"):
            continue
        action_params.append(param)

    if not action_params:
        return create_model(f"{fn.__name__}_params", __base__=BaseModel)

    # Type 1 check: first param is a BaseModel subclass
    first_param = action_params[0]
    if len(action_params) == 1:
        annotation = first_param.annotation
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return annotation  # Use directly

    # Type 2: build from individual params
    fields: dict[str, tuple[type, Any]] = {}
    for param in action_params:
        annotation = param.annotation if param.annotation is not inspect.Parameter.empty else str
        default = param.default if param.default is not inspect.Parameter.empty else ...
        fields[param.name] = (annotation, default)

    return create_model(f"{fn.__name__}_params", **fields, __base__=BaseModel)  # type: ignore


# ── Tool Registry ──────────────────────────────────────────────────


class ToolRegistry(Generic[Context]):
    """Register typed actions, auto-inject context, produce prompt descriptions.

    Example:
        >>> registry = ToolRegistry()
        >>>
        >>> class SearchParams(BaseModel):
        ...     query: str
        ...     limit: int = 5
        >>>
        >>> @registry.action("Search Google", param_model=SearchParams)
        ... async def search(params: SearchParams, page_url: str = ""):
        ...     return f"Searching {page_url} for {params.query}"
        >>>
        >>> registry.get_prompt_description()
        'search(query: str, limit: int = 5) — Search Google'
    """

    def __init__(self, context: Context | None = None):
        self.registry = ActionRegistry()
        self.context = context

    # ── Registration ────────────────────────────────────────────────

    def action(
        self,
        description: str = "",
        param_model: type[BaseModel] | None = None,
        domain_filter: str | None = None,
    ):
        """Decorator: register a function as an executable action.

        Args:
            description: Human-readable description for the LLM prompt.
            param_model: Optional explicit Pydantic model. If None, built
                from the function signature (skipping context params).
            domain_filter: If set, only show this action when page_url
                matches this domain.
        """

        def decorator(fn: Callable) -> Callable:
            name = fn.__name__
            is_async = inspect.iscoroutinefunction(fn)

            # Determine which signature params are "context" (injected, not from LLM)
            sig = inspect.signature(fn)
            context_params = {n for n in sig.parameters if n in CONTEXT_PARAMS}

            # Build param model from signature if not provided
            model = param_model or _build_param_model(fn, context_params)

            self.registry.actions[name] = RegisteredAction(
                name=name,
                description=description or fn.__doc__ or "",
                fn=fn,
                param_model=model,
                is_async=is_async,
                domain_filter=domain_filter,
            )
            logger.debug("Registered action: %s (%s)", name, description[:50])
            return fn

        return decorator

    # ── Execution ───────────────────────────────────────────────────

    async def execute(
        self,
        action_name: str,
        params: dict[str, Any] | BaseModel,
        injected_context: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a registered action by name.

        Args:
            action_name: Name of the registered action.
            params: Parameters as dict or Pydantic model.
            injected_context: Override context values (browser_session, etc.)

        Returns:
            The action's return value.

        Raises:
            KeyError: If action is not registered.
        """
        if action_name not in self.registry.actions:
            available = list(self.registry.actions.keys())
            raise KeyError(f"Unknown action '{action_name}'. Available: {available}")

        action = self.registry.actions[action_name]

        # Parse params into the action's param model
        if isinstance(params, dict):
            parsed = action.param_model.model_validate(params)
        else:
            parsed = params

        # Build kwargs
        kwargs: dict[str, Any] = {}

        # Check if this is Type 1 (function accepts the param model directly)
        # or Type 2 (function accepts individual fields)
        sig = inspect.signature(action.fn)
        sig_params = list(sig.parameters.values())
        type1 = False
        for sp in sig_params:
            if sp.name in CONTEXT_PARAMS or sp.name in ("self", "cls"):
                continue
            ann = sp.annotation
            if isinstance(ann, type) and issubclass(ann, BaseModel) and ann is action.param_model:
                type1 = True
            break

        if type1:
            # Pass the parsed model as the first action arg
            for sp in sig_params:
                if sp.name in CONTEXT_PARAMS or sp.name in ("self", "cls"):
                    continue
                kwargs[sp.name] = parsed
                break
        else:
            # Unpack param model fields as kwargs
            for field_name in action.param_model.model_fields:
                kwargs[field_name] = getattr(parsed, field_name)

        # Inject context params that the function accepts
        sig = inspect.signature(action.fn)
        context_params = {n for n in sig.parameters if n in CONTEXT_PARAMS}
        ctx = injected_context or {}
        for param_name in context_params:
            if param_name in ctx:
                kwargs[param_name] = ctx[param_name]
            elif hasattr(self.context, param_name):
                kwargs[param_name] = getattr(self.context, param_name)
            # If not available, don't pass it — let the function handle default

        # Execute
        if action.is_async:
            return await action.fn(**kwargs)
        return action.fn(**kwargs)

    # ── Prompt descriptions ─────────────────────────────────────────

    def get_prompt_description(
        self,
        page_url: str | None = None,
        include_domain_filtered: bool = True,
    ) -> str:
        """Generate an LLM-friendly description of all available actions.

        Args:
            page_url: If provided, filters actions by domain.
            include_domain_filtered: If False, hides domain-filtered actions.

        Returns:
            Formatted string like:
                search(query: str, limit: int = 5) — Search Google
                click(index: int) — Click an element
        """
        lines: list[str] = []
        for name, action in sorted(self.registry.actions.items()):
            if action.name in self.registry.exclude_actions:
                continue

            # Domain filter: only show the action if the page URL matches
            if action.domain_filter:
                if page_url and action.domain_filter not in page_url:
                    continue  # Wrong domain — hide
                elif not page_url and not include_domain_filtered:
                    continue  # No URL context — hide unless explicitly included

            # Build param signature from the model
            sig_parts: list[str] = []
            for f_name, f_field in action.param_model.model_fields.items():
                type_hint = _type_display(f_field.annotation)
                if f_field.is_required():
                    sig_parts.append(f"{f_name}: {type_hint}")
                else:
                    default = f_field.default
                    sig_parts.append(f"{f_name}: {type_hint} = {default}")

            sig_str = ", ".join(sig_parts)
            lines.append(f"  {name}({sig_str}) — {action.description}")

        return "\n".join(lines)

    def get_actions_for_url(self, url: str) -> list[RegisteredAction]:
        """Return actions visible for a given URL (respects domain_filter)."""
        result = []
        for action in self.registry.actions.values():
            if action.name in self.registry.exclude_actions:
                continue
            if action.domain_filter and action.domain_filter not in url:
                continue
            result.append(action)
        return result


# ── Helpers ────────────────────────────────────────────────────────


def _type_display(annotation: type | None) -> str:
    """Pretty-print a type annotation for LLM consumption."""
    if annotation is None:
        return "any"
    origin = getattr(annotation, "__origin__", None)
    if origin is list:
        args = getattr(annotation, "__args__", ())
        if args:
            return f"list[{_type_display(args[0])}]"
        return "list"
    if origin is dict:
        args = getattr(annotation, "__args__", ())
        if len(args) >= 2:
            return f"dict[{_type_display(args[0])}, {_type_display(args[1])}]"
        return "dict"
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    return str(annotation)


# ── Built-in actions (optional) ────────────────────────────────────


def register_core_actions(registry: ToolRegistry) -> None:
    """Register built-in actions every agent should have."""

    class FinishParams(BaseModel):
        answer: str = ""
        success: bool = True

    @registry.action(
        "Finish the task and return the result",
        param_model=FinishParams,
    )
    async def finish(params: FinishParams) -> dict:
        """Signal task completion with the final answer."""
        return {"done": True, "answer": params.answer, "success": params.success}

    class ReportErrorParams(BaseModel):
        error: str
        recoverable: bool = False

    @registry.action(
        "Report an error and optionally mark it recoverable",
        param_model=ReportErrorParams,
    )
    async def report_error(params: ReportErrorParams) -> dict:
        """Report an error to the runtime."""
        return {"done": False, "error": params.error, "recoverable": params.recoverable}
