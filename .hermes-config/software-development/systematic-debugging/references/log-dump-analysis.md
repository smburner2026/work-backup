# Log Dump Analysis — Systematic Methodology

## When to Use

The user provides a log dump (agent.log, errors.log, gateway.log from
`~/.hermes/logs/`) and asks what's wrong. Rarely do they provide a specific
search query — they want a **full diagnostic**.

## Steps

### Step 1: Categorize by Source

Hermes produces three log files:

| File | Level | What it captures |
|------|-------|-----------------|
| `agent.log` | INFO+ | Every API call, tool execution, session turn, latency, cache hit ratio, turn start/end |
| `errors.log` | WARNING+ | Errors, tool failures, loops, and anything the agent should know about |
| `gateway.log` | INFO+ | Gateway lifecycle, platform connections, shutdowns, restarts, cron ticks |

**Read agent.log first** — it has the most signal. Scan for:
- Tool failures (especially repeated ones)
- Memory capacity warnings
- Background review failures
- Slow or timed-out operations
- API call count trends

Then cross-reference with **errors.log** for the same session ID to see
what was severe enough to log as a warning.

Finally **gateway.log** for platform-level issues, shutdowns, restarts.

### Step 2: Classify Severity

Sort issues into three buckets:

| Severity | Signal | Examples |
|----------|--------|---------|
| 🔴 **Critical** | Breaks core function, wastes significant resources | Memory overflow loops, bg-review tool whitelist failures, disconnected platforms, broken search |
| 🟡 **Problematic** | Causes wasted effort, delays, or silent failure | Tool escaping bugs, timed-out builds, SIGTERM mid-session, patch mismatches |
| 🟢 **Minor** | Worth noting but not urgent | Skill name typos, memory growth trends, single-provider dependency |

### Step 3: Trace Repetition Patterns

**Same tool, same failure, repeated calls** is the signal for a loop.

```python
# In errors.log, look for:
same_tool_failure_warning; count=3; {tool_name} has failed 3 times this turn
```

When detected:
1. Identify the **context** (main agent vs background review)
2. Look at which specific arguments failed (e.g. `memory(action='replace', old_text='X')`)
3. Trace WHY those arguments were wrong (e.g. the text didn't match, the store was full)
4. Fix at root cause, not symptom

### Step 4: Correlate with Current State

Before proposing fixes, always check current state:

- **Memory**: `hermes memory status` or read legacy files at `~/.hermes/memories/`
- **Config**: `hermes config` or read `~/.hermes/config.yaml`
- **Platforms**: `send_message(action='list')` to check gateway targets
- **Services**: Run a simple `web_search` to verify search works
- **Filesystem**: `ls /root/work/...` to check project state

This prevents proposing a fix that's already been applied or suggesting
a change that's no longer relevant.

### Step 5: Fix at Root Cause

Common root cause patterns:

| Symptom (in log) | Likely Root Cause | Fix |
|-----------------|-------------------|-----|
| bg-review denies `patch`/`terminal`/`read_file` | Tool whitelist built from toolsets; if the tool isn't in a named toolset, it's denied | Add tool to the relevant toolset in `toolsets.py`, or update the whitelist in `agent/background_review.py` |
| `memory(action='replace', old_text='...')` fails with "No entry matched" | The old text doesn't match any current entry — either it was already removed or the text was slightly different | Switch to `mnemosyne_remember` which doesn't require matching old text |
| `execute_code` with `SyntaxError: unterminated string literal` on line 3 | The agent nested shell quoting inside Python string literals | Use `terminal()` directly from `hermes_tools` instead of nesting shell inside Python |
| `web_search` returns 400 Bad Request | Malformed query, API key issue, or Tavily endpoint issue | Check `TAVILY_API_KEY` in `.env`, simplify the query |
| Discord `ServerDisconnected` | Transient network issue (usually recovers on next session restart) | Check with `send_message(action='list')`, restart gateway if needed |
| WeasyPrint timeout on build | PDF generation OOM on low-memory VPS (2GB) | Use per-work PDFs + `pdfunite` merge strategy |
| SIGTERM mid-session | systemd restart or `stop/restart` command | Check `systemctl --user status hermes-gateway` |

### Step 6: Present as Structured Summary

Best format for a Telegram-friendly diagnosis:

```markdown
## 🔴 Critical

**1. Title** — description of what went wrong, why it matters
**2. Next issue** — with same reasoning

## 🟡 Problematic

**3.** ...

## 🟢 Minor / Worth Noting

**4.** ...
```

End with actionable next steps in priority order. Always offer to fix.

## Pitfalls

- **Don't propose fixes without checking current state** — the problem may
  already be self-healed (Tavily/Discord often recover on restart)
- **Don't trust a single error line** — correlate across all three log files
  to distinguish transient from persistent failures
- **Don't miss background review failures** — they don't interrupt the main
  conversation but silently waste API calls
- **Memory tools in bg-review**: the legacy `memory` tool fills up; bg-review
  agents should use `mnemosyne_remember` instead, but the tool must also be
  in the bg-review's tool whitelist (built from `toolsets.py` — the `memory`
  toolset must include mnemosyne tools)
