# Session Title Generation

Hermes can auto-generate session titles from the first user/assistant exchange,
but this feature is **only wired into some entry paths**, not all. This
matters because untitled sessions are harder to discover via `session_search`
— they show only a `session_id` in browse mode and lack the FTS5 surface
a title would provide.

## Title Generator (`agent/title_generator.py`)

- `maybe_auto_title()` — fire-and-forget entry point. Spawns a daemon thread,
  checks if the session already has a title, then calls `auto_title_session()`.
- `auto_title_session()` — calls `generate_title()`, then
  `session_db.set_session_title()`.
- `generate_title()` — calls an auxiliary LLM with a simple prompt ("Generate
  a short, descriptive title (3-7 words)…"). Uses `call_llm()` from
  `agent/auxiliary_client.py`, which routes through the cheapest available
  model. Falls back silently on failure, emitting a warning log + optional
  failure callback.
- Guard: only fires on the first 1–2 user messages (counts user messages in
  `conversation_history`).
- Guard: skips if the session already has a title (user-set via `/title` or
  previously auto-generated).

## Wired Entry Points

These call paths invoke `maybe_auto_title` after the first response:

| Path | File | Approx line |
|------|------|-------------|
| **Gateway** (Telegram, Discord, etc.) | `gateway/run.py` | 16113 |
| **ACP / IDE** (VS Code, Zed, JetBrains) | `acp_adapter/server.py` | 1505 |

## NOT Wired (The Gap)

The core **CLI path** (`hermes` from terminal, `hermes chat -q`, all
`run_agent.py`-based sessions) does **not** call `maybe_auto_title`.

- `run_agent.py` — zero references to title generation.
- `cli.py` — has `_pending_title` for user-set `/title` commands, but no
  auto-generation wiring.
- `conversation_compression.py` — calls `set_session_title` to auto-number
  compressed continuations ("Fix auth bug (2)"), but this is compression
  naming, not initial titling.

**Impact:** every `hermes` terminal session launches with `title = NULL` and
stays that way unless the user remembers `/title`. For users who run Hermes
primarily from the CLI (or mix CLI with gateway), the session store fills
with untitled entries, degrading `session_search` browse mode and FTS5 match
quality.

## File Locations

```
agent/title_generator.py      — maybe_auto_title, auto_title_session, generate_title
agent/auxiliary_client.py     — call_llm (auxiliary model routing)
gateway/run.py ~16113         — wired call to maybe_auto_title
acp_adapter/server.py ~1505   — wired call to maybe_auto_title
run_agent.py                  — NOT wired (gap site)
cli.py                        — _pending_title for /title only (NOT wired)
```

## Fix Approach

Wire `maybe_auto_title` into the CLI path after the first successful
assistant response. The gateway pattern in `gateway/run.py` (around line
16110–16130) is the canonical reference:

```python
if final_response and self._session_db:
    try:
        from agent.title_generator import maybe_auto_title
        all_msgs = result_holder[0].get("messages", []) if result_holder[0] else []
        maybe_auto_title(
            session_db=self._session_db,
            session_id=effective_session_id,
            user_message=...,       # first user message
            assistant_response=..., # first assistant response
            conversation_history=...,
            failure_callback=getattr(agent, "_emit_auxiliary_failure", None),
            main_runtime={...},
        )
    except Exception:
        pass
```

The exact insertion point in the CLI is either:
1. In `run_agent.py` — inside `run_conversation()` after a text response is
   returned (non-tool-call branch), before returning.
2. In `cli.py` — after `_flush_history_to_db()` is called following the first
   assistant turn, matching how `/title` interacts with `_pending_title`.

A `config.yaml` flag (`auto_title.enabled: true`) could let users opt out
without modifying code.
