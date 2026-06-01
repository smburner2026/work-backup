---
name: lightpanda-batch-scraping
description: "Web scraping and browser automation with Lightpanda — Hermes native browser engine integration for fast headless browsing, plus manual CLI extraction and parallel batch scraping via agent-browser + delegate_task."
version: 2.0.0
author: Hermes Agent
tags: [scraping, lightpanda, agent-browser, web, batch, x-twitter, browser-engine]
---

# Lightpanda Batch Scraping

## Hermes Native Integration (PREFERRED)

Lightpanda is built into Hermes as a **native browser engine**. Set `browser.engine: lightpanda` in config.yaml and all standard Hermes browser tools (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_scroll`, `browser_press`, `browser_back`) use Lightpanda automatically — no manual CLI commands needed.

**Config:** `browser.engine: lightpanda`  
**Effect:** All `browser_*` tools route through `agent-browser --engine lightpanda`  
**Fallback:** Automatic Chrome fallback for vision/screenshots (Lightpanda has no graphical renderer)  
**Speed:** 1.3–5.8× faster than Chrome, 9× less memory  
**Requirements:** `agent-browser` installed (v0.25.3+), Lightpanda binary at `/usr/local/bin/lightpanda`

### What works natively

| Hermes Tool | With engine=lightpanda |
|---|---|
| `browser_navigate` | Lightpanda — fast, no Chromium needed |
| `browser_snapshot` | Lightpanda — accessibility tree snapshot |
| `browser_click` / `browser_type` / `browser_scroll` / `browser_press` / `browser_back` | Lightpanda |
| `browser_vision` | **Always Chrome** — Lightpanda has no graphical renderer. Transparent auto-fallback. |
| `browser_get_images` | **Always Chrome** — same graphical limitation |
| `browser_console` | Chrome fallback when Lightpanda engine fails |
| Empty/truncated snapshots | Auto-retry with Chrome |

### How to enable

```bash
hermes config set browser.engine lightpanda
```

Takes effect on **next session** — `browser.engine` is read once at session init.

### Verification

```bash
# After next session start, run a browser command
# Hermes logs will show: engine=lightpanda
# If it fails, agent-browser automatically retries with Chrome
```

### Pitfalls (native integration)

- **Engine is session-locked** — agent-browser sessions are pinned to one engine. The Hermes fallback creates a parallel Chrome session when Lightpanda can't handle something, navigates to the current URL, and runs the command there. This adds latency but is transparent.
- **No graphical renderer** — `browser_vision` and `browser_get_images` always route through Chrome. Slower for vision tasks but handled automatically.
- **Limited JS support** — Lightpanda's minimal V8 engine may choke on complex SPAs. The automatic Chrome fallback catches most cases.
- **Config is per-session** — changing `browser.engine` mid-session requires a restart.
- **agent-browser must be installed** — `npm install -g agent-browser`. The Hermes bundled version at `/usr/local/lib/hermes-agent/node_modules/.bin/agent-browser` is used automatically.

---

## Manual CLI Usage (fallback / advanced)

Use these approaches when you need direct control outside the Hermes browser tool stack, or when you're running in a subagent with `toolsets: ["terminal", "file"]`.

### Toolchain

| Tool | Purpose | Command |
|------|---------|---------|
| **Lightpanda** | Fast headless extraction | `lightpanda fetch <url> --dump markdown` |
| **agent-browser** | Interactive scraping + snapshots | `agent-browser --engine lightpanda open/snapshot/click` |
| **Hermes delegate_task** | Parallel batch scraping | Spawn concurrent subagents, each processing a URL subset |

### Setup

Installed at:
- `agent-browser` → `/usr/local/lib/hermes-agent/node_modules/.bin/agent-browser` (Hermes bundled) or `npm install -g agent-browser`
- `lightpanda` → `/usr/local/bin/lightpanda` (nightly binary, Linux x86_64)

Update:
```bash
npm update -g agent-browser
wget -q -O /usr/local/bin/lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux
```

---

### Mode 1: Fast extraction with Lightpanda fetch

Best for: **one-off URLs, markdown extraction, static content, X/Twitter posts.**

Lightpanda renders JS and dumps clean markdown — no X API or API keys needed. Even works on login-walled pages (X/Twitter, etc.) since it renders the public view.

```bash
lightpanda fetch <url> --dump markdown

# Wait for network idle (SPA sites)
lightpanda fetch <url> --dump markdown --wait-until networkidle --wait-ms 10000

# Get JSON with embedded markdown
lightpanda fetch <url> --dump markdown --json

# Strip JS, CSS, images
lightpanda fetch <url> --dump markdown --strip-mode full

# Scrape with custom user-agent
lightpanda fetch <url> --dump markdown --user-agent-suffix "Hermes/1.0"
```

#### X/Twitter posts (no API needed)

```bash
lightpanda fetch https://x.com/user/status/POST_ID --dump markdown --wait-ms 8000
```

Returns post text, author, engagement stats, and media links as markdown. Works for any public X post.

**Fallback:** If Lightpanda fails, use `fxtwitter.com` proxy:
```bash
curl -s https://api.fxtwitter.com/status/POST_ID | jq '.tweet.text'
```

---

### Mode 2: Interactive scraping with agent-browser

Best for: **form filling, login flows, multi-page navigation, JS-heavy SPAs, pagination.**

```bash
# Start session with Lightpanda engine
agent-browser --engine lightpanda open https://example.com
agent-browser snapshot -i           # see interactive elements with @eN refs
agent-browser click @e3             # interact via refs
agent-browser fill @e2 "query"      # fill inputs
agent-browser screenshot page.png   # visual verification
agent-browser close
```

#### Key commands

```bash
agent-browser open <url>         # Navigate
agent-browser snapshot -i        # Interactive elements only (preferred)
agent-browser snapshot -i -u     # Include href URLs
agent-browser snapshot -i -c     # Compact mode (no empty structural nodes)
agent-browser click @eN          # Click element by ref
agent-browser fill @eN "text"    # Clear + type into input
agent-browser type @eN "text"    # Type without clearing
agent-browser get text @eN       # Get visible text
agent-browser get html @eN       # Get inner HTML
agent-browser get attr @eN href  # Get attribute
agent-browser get title          # Page title
agent-browser get url            # Current URL
agent-browser scroll down 500    # Scroll page
agent-browser wait --load networkidle  # Wait for page load
agent-browser screenshot <path>  # Visual check
agent-browser close              # End session
```

#### Semantic locators (no snapshot needed)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

---

### Mode 3: Parallel batch scraping via Hermes delegation

Best for: **large-scale scraping across many URLs (50+ pages).**

Use `delegate_task` to spawn parallel subagents, each processing a subset:

```python
# Pseudocode — in practice, chunk URLs and delegate
from hermes_tools import delegate_task

urls = ["https://site.com/page/1", "https://site.com/page/2", ...]
chunks = [urls[i:i+10] for i in range(0, len(urls), 10)]

tasks = []
for i, chunk in enumerate(chunks):
    tasks.append({
        "goal": f"Extract all content from these {len(chunk)} URLs using lightpanda fetch or agent-browser. Return structured markdown for each URL.",
        "context": f"URLs to scrape:\n" + "\n".join(chunk),
        "toolsets": ["terminal", "file"]
    })

results = delegate_task(tasks=tasks)  # up to 3 concurrent subagents
```

---

## Pitfalls (all modes)

### Tool-selection discipline (user-enforced rule)
- **Rule: loading this skill means you WILL use Lightpanda for the task at hand.** If you read this skill and then fall back to curl or the Hermes browser for something Lightpanda can handle (X/Twitter posts, JS-rendered pages, markdown extraction), the user will flag this as tool-avoidance. When this skill matches the class of task, execute it — don't just read it.
- **When to use Lightpanda:** JS-heavy pages (X/Twitter, SPAs, login-walled public content), markdown extraction from rendered pages, any URL where curl returns HTML but not the rendered text content.
- **When NOT to use Lightpanda:** Shadow-library searches (libgen, Anna's Archive), direct download URLs (PDFs, files), REST API endpoints that return JSON, or any URL where curl works cleanly. Lightpanda is heavier than curl for simple fetches.
- **Data volume warning:** `--dump markdown` on large dynamic pages (libgen search results with 25+ entries) can produce 20–90 KB of HTML noise. Pair with `--strip-mode full` and/or post-process with a regex/tag-strip before parsing. If you need structured fields, search for `get.php`, `edition.php?id=`, or `md5=` in the rendered output.

### Technical pitfalls

- **WSL / sudo-less install** — `npm install -g agent-browser` puts it under `~/.hermes/node/bin/`, which may not be in PATH. Add `$HOME/.hermes/node/bin` to `~/.profile`. For lightpanda, download the binary to `~/.local/bin/` instead of `/usr/local/bin/` since WSL typically lacks passwordless sudo.
- **Lightpanda has limited JS support** — V8 engine is minimal. Complex SPAs (React-heavy, WebGL, canvas) may not render fully. The native Hermes integration auto-falls back to Chrome; manual CLI usage needs explicit `--engine chrome`.
- **X/Twitter rate limits** — Lightpanda fetch works without auth but X may rate-limit rapid repeated requests. Add `--wait-ms 2000` between fetches.
- **agent-browser refs are ephemeral** — `@eN` refs go stale after any page change. Always re-snapshot after clicking/navigating.
- **Memory** — Lightpanda is 9x lighter than Chrome, but each Lightpanda process still uses some memory. For very large batches, limit parallelism.
- **No cookies by default** — Lightpanda fetch doesn't persist sessions. Use `--cookie-jar` for stateful scraping.
- **agent-browser Chrome engine** — `agent-browser install` downloads Chromium for the default engine. Lightpanda engine skips this — no Chromium install needed.
- **Mid-session engine switch is expensive** — When the native integration falls back to Chrome, it creates a new session, navigates to the current URL (JavaScript-heavy fallback path), runs the command, and tears it down. This works but adds seconds of latency.

## Verification

```bash
# Test Lightpanda binary
lightpanda fetch https://example.com --dump markdown

# Test agent-browser + Lightpanda
agent-browser --engine lightpanda open https://example.com
agent-browser snapshot -i
agent-browser close --all

# Test X/Twitter extraction
lightpanda fetch https://x.com/username/status/POST_ID --dump markdown --wait-ms 8000

# After enabling engine=lightpanda:
# Hermes browser_* tools use Lightpanda transparently
