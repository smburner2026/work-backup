# browser-use/browser-use — Architecture Patterns (96k⭐)

Repository: https://github.com/browser-use/browser-use
Author: Gregor Zunic
License: MIT
Language: Python (3.11+)
Deps: aiohttp, pydantic, httpx, cdp-use, bubus, openai, anthropic
Version: 0.12.9

---

## Architecture — 6-Layer System

```
Layer       Module              Role
────────────────────────────────────────────────────────
1. Agent    agent/service.py    Step loop: context → LLM → execute → compact
2. Tools    tools/registry/     Typed action registration with injected deps
3. Browser  browser/session.py  CDP-based browser control (event-driven)
4. DOM      dom/service.py      AX tree → enhanced snapshot → serialized elements
5. Memory   agent/message_manager/  State + conversation with compaction
6. Prompts  agent/system_prompts/   Markdown prompt files, modifiable
```

## Core Step Loop

```
step()
  ├── _prepare_context()        # Grab DOM + screenshot, build messages, compact
  │   ├── _check_and_update_downloads()
  │   ├── _check_stop_or_pause()
  │   ├── _update_action_models_for_page()
  │   └── _maybe_compact_messages()
  ├── _get_next_action()         # Call LLM with structured AgentOutput schema
  │   └── (retry logic, timeout)
  ├── _execute_actions()         # multi_act (up to 5 actions via tool registry)
  │   └── multi_act()
  └── _post_process()            # Detect loops, track downloads, update plan
```

## Pattern 1: Tool Registry with Injected Context

**What**: Actions are typed Python functions with Pydantic param models. The registry auto-injects special context parameters so handlers don't import infrastructure.

**Key code**: `browser_use/tools/registry/service.py`

```python
# Registration:
@ctrl.action('Search Google', param_model=SearchParams)
async def search_google(params: SearchParams, browser_session: BrowserSession, page_url: str):
    ...

# Internally, the Registry class:
class Registry(Generic[Context]):
    def __init__(self, exclude_actions: list[str] | None = None):
        self.registry = ActionRegistry()
        self.exclude_actions = list(exclude_actions) if exclude_actions else []

    # Special params auto-injected by name:
    _special_params = {
        'context': None,           # Generic TypeVar
        'browser_session': BrowserSession,
        'page_url': str,
        'cdp_client': None,
        'page_extraction_llm': BaseChatModel,
        'available_file_paths': list,
        'has_sensitive_data': bool,
        'file_system': FileSystem,
        'extraction_schema': None,
    }
```

**Why it's good**: Action handlers don't need to import browser, LLM, or file system modules. The registry wires them up by matching parameter names. Clean separation of concerns — each action is a pure function of (params + injected context).

**To adopt**: Create a `@tool` or `@action` decorator that registers a function and its param model. Use `inspect.signature` to extract special params from function signature. On execution, look up special params from a context object and pass them + the user-provided params.

---

## Pattern 2: Domain-based Action Filtering

**What**: Only show relevant tools for the current page URL. If you're on github.com, don't show Gmail-specific tools.

**Key code**: `browser_use/tools/registry/service.py`

```python
# Each action can declare domain filtering:
page_filtered_actions = self.tools.registry.get_prompt_description(browser_state_summary.url)

# Internal: Registry tracks URL patterns per action
# When building the prompt, only actions matching the current URL domain are included
```

**Why it's good**: Reduces LLM confusion by not presenting irrelevant tools. Keeps prompts compact.

---

## Pattern 3: Message Compaction with Token Budget

**What**: Configurable compaction that triggers at N steps or N token threshold. Uses a separate LLM to summarize older history into a compact memory block, keeping the last N raw items.

**Key config**: `browser_use/agent/views.py:MessageCompactionSettings`

```python
class MessageCompactionSettings(BaseModel):
    enabled: bool = True
    compact_every_n_steps: int = 25
    trigger_char_count: int | None = None   # ~40k chars default (~10k tokens)
    keep_last_items: int = 6               # Keep this many most-recent items raw
    summary_max_chars: int = 6000          # Cap on the compacted summary
    compaction_llm: BaseChatModel | None = None  # Separate LLM for compaction
```

**Why it's good**: Long agent runs don't blow context. The compaction LLM is typically cheaper/faster (e.g., GPT-4o-mini for a GPT-4o agent). Keeps the agent's "short-term memory" (last 6 steps) accurate while summarizing the rest.

**To adopt**: Monitor total message size (char or token count). When it exceeds threshold, call a cheap LLM to summarize all messages except the most recent N. Inject the summary as a system message and drop the old messages from context.

---

## Pattern 4: Action Loop Detection with Escalating Nudges

**What**: SHA-256 hashes each action (normalized by type) and tracks repetition in a rolling window. Doesn't block — emits escalating awareness nudges at 5/8/12 repeats so the LLM can self-correct.

**Key code**: `browser_use/agent/views.py:ActionLoopDetector`

```python
class ActionLoopDetector(BaseModel):
    window_size: int = 20
    recent_action_hashes: list[str] = []
    recent_page_fingerprints: list[PageFingerprint] = []
    max_repetition_count: int = 0
    consecutive_stagnant_pages: int = 0

    def get_nudge_message(self) -> str | None:
        # Escalating: 5 → 8 → 12 repeats
        if self.max_repetition_count >= 12:
            return f'Heads up: repeated {self.max_repetition_count}x... If not making progress, try different approach.'
        elif self.max_repetition_count >= 8:
            return f'Repeated {self.max_repetition_count}x. Are you still making progress?'
        elif self.max_repetition_count >= 5:
            return f'Repeated {self.max_repetition_count}x. If intentional, carry on.'
        # Also check page stagnation
        if self.consecutive_stagnant_pages >= 5:
            return 'Page has not changed in 5+ actions. Try a different element.'
        return None

# Action hashing normalizes by type:
def _normalize_action_for_hash(action_name: str, params: dict) -> str:
    if action_name == 'click':
        return f'click|{params.get(\"index\")}'
    if action_name == 'search':
        tokens = sorted(set(query.lower().split()))
        return f'search|{engine}|{tokens}'
    if action_name == 'navigate':
        return f'navigate|{url}'  # full URL
    # etc.

# Page fingerprinting:
class PageFingerprint(BaseModel):
    url: str
    element_count: int
    text_hash: str  # first 16 chars of SHA-256 of DOM text
```

**Why it's good**: Hard loop limits kill productive repetition (e.g., scrolling through a list). Soft nudges let the LLM decide. The escalation gives the model increasing "pressure" to change strategy without blocking.

**To adopt**: After each action step, hash the action and check the rolling window. If count exceeds threshold, append a system-style nudge message to the next agent prompt. Reset the counter when the page fingerprint changes.

---

## Pattern 5: AX Tree → Enhanced DOM Snapshot

**What**: Uses Chrome's Accessibility Tree (not HTML parsing) to build a serialized element map. Paint-order filtering, viewport-based hidden element detection, iframe depth limits.

**Key flow**: `dom/enhanced_snapshot.py` + `dom/serializer/`

```
CDP getFullAXTree() → build_snapshot_lookup() → ClickableElementDetector → DOMTreeSerializer
```

What gets serialized for each clickable element:
- tag_name, text, attributes
- CSS selector (via CDP)
- bounding rect (x, y, w, h)
- computed styles (display, visibility, opacity)
- paint order index
- iframe depth

**Why it's good**: AX tree is more reliable than HTML regex for finding interactive elements. It provides accessibility metadata that HTML parsing misses (aria labels, roles, keyboard handlers). Paint-order filtering means the agent sees elements in visual order, not source order.

**To adopt**: Requires CDP access (Chrome DevTools Protocol). The `cdp-use` library wraps this well. The key insight is: don't parse HTML — request the accessibility tree and filter for interactive nodes.

---

## Pattern 6: Sensitive Data Redaction

**What**: A redaction layer that intercepts action parameters containing credentials, API keys, passwords — replaces them with placeholders before writing to history/persistent storage.

**Key code**: `browser_use/agent/views.py:AgentHistory._filter_sensitive_data_from_string()`

```python
# Agent receives sensitive_data as dict:
sensitive_data = {"password": "my_pass", "email": "user@example.com"}

# History serialization filters these out:
def _filter_sensitive_data_from_dict(self, data, sensitive_data):
    # Recursively replace sensitive values with [REDACTED]
    ...
```

**Why it's good**: Prevents credential leakage in saved conversation files, logs, and telemetry. Important for any agent that handles auth/passwords.

---

## Key Dependencies

| Package | Purpose |
|---------|---------|
| cdp-use | Chrome DevTools Protocol client — replaces Playwright |
| bubus | Event bus for decoupled component communication |
| pydantic | Data models, config validation, action param schemas |
| httpx/aiohttp | HTTP for cloud browser API, downloads |
| posthog | Telemetry |

## Note on "Flash Mode"

A variant of the agent loop that strips `thinking`, `evaluation_previous_goal`, and `next_goal` from the output schema. Only requires `memory` and `action`. Used when the provider is their cloud service (ChatBrowserUse) for reduced token overhead. When `flash_mode=True`, planning is automatically disabled.
