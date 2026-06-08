# Hermes Browser Engine Architecture (browser_tool.py)

Reference for understanding how Hermes resolves and uses browser engines.

## Engine Resolution

browser_tool.py maintains a cached engine setting via `_get_browser_engine()`:

```
config.yaml browser.engine → _get_browser_engine() → cached
```

Valid values: `auto`, `lightpanda`, `chrome`
- `_VALID_ENGINES = {"auto", "lightpanda", "chrome"}` (line 674)
- `auto` evaluates credentials (Browserbase API key → browserbase, Browser Use API key → browser_use, else → local Chrome/Lightpanda)
- `lightpanda` forces Lightpanda engine for local browser operations
- `chrome` forces Chrome engine (default agent-browser behavior)

## Lightpanda Integration Points

### Session Creation (line ~1958)
When `_inject_engine` is True and engine is Lightpanda, `--engine lightpanda` is appended to agent-browser CLI invocations:
```python
if engine == "lightpanda" and _should_inject_engine(engine):
    args.insert(1, "--engine")
    args.insert(2, "lightpanda")  # or args[1:1] = ["--engine", "lightpanda"]
```

### Chromium Requirement Bypass (line ~1917)
Lightpanda engine skips the Chromium installation check:
```python
if _is_local_mode() and not _chromium_installed() and _get_browser_engine() != "lightpanda":
    # Only error out if NOT lightpanda engine
```

### Automatic Chrome Fallback (line ~2177)
After every browser command, the engine checks if the result needs Chrome retry:
1. `_needs_lightpanda_fallback()` checks for: errors, empty/truncated snapshots, missing screenshot files, placeholder PNGs
2. If fallback needed, `_lightpanda_fallback()` creates a Chrome session, navigates to the Lightpanda session's URL, reruns the command, and returns the Chrome result with a `_lightpanda_fallback` annotation

### Vision/Screenshot Pre-routing (line ~3087)
`browser_vision` always routes vision/screenshots to Chrome when engine is Lightpanda:
```python
if engine == "lightpanda" and _should_inject_engine(engine):
    # Pre-route to Chrome — Lightpanda has no graphical renderer
    fb_result = _lightpanda_fallback(engine, "vision", result, task_id)
```
Lightpanda returns a placeholder PNG (panda logo) for screenshots — vision_analyze detects small files and triggers fallback.

### Engine Detection Helper (line ~698)
```python
def _using_lightpanda_engine() -> bool:
    return _get_browser_engine() == "lightpanda"
```
Used in local mode checks and in `execute_code` integration to determine environment setup.

## Fallback Annotation

When Chrome fallback is used, the result dict includes:
```python
{
    "_lightpanda_fallback": {
        "from": "lightpanda",
        "to": "chrome", 
        "reason": "Lightpanda returned an empty/too-short snapshot; retried with Chrome."
    }
}
```

## Config Surface

- `browser.engine` — `auto` (default), `lightpanda`, or `chrome`
- Read once at session init — mid-session changes require restart
- Takes effect for ALL `browser_*` tools that use the local agent-browser execution path

## Requirements

- agent-browser v0.25.3+ (our version: 0.26.0)
- Lightpanda binary at `/usr/local/bin/lightpanda`
- No API keys needed (local stack, unlike Browserbase/Browser Use cloud backends)
