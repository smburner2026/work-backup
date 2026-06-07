# Session DB Behavior Mining

When the user asks "is feature X actually being used?" or "what's eating my context?", don't answer from benchmarks or general claims — **mine the actual session DBs**. The user has explicit "empirically verify" preferences; recommendations that aren't grounded in their real data are weak.

This is the read-only companion to `references/session-db-cleanup.md`. Pruning removes; mining analyzes.

## When to use

- User asks "is X really happening in my workflow?" (skill X, command X, MCP server X, behavior X)
- User asks "where is my context going?" before any optimization recommendation
- User asks about adoption of a feature, frequency of a pattern, or cost of a behavior
- Before recommending an install/uninstall based on benchmarks — verify the use case applies

## Schema discovery first

The session DB at `/root/.hermes/sessions/sessions.db` is a stub on most installs — actual session data is in **JSONL files** under `/root/.hermes/sessions/`. Before writing analysis code, look at one file to learn the actual schema:

```bash
# Look at the latest session to see real field structure
tail -1 /root/.hermes/sessions/$(ls -t /root/.hermes/sessions/*.jsonl | head -1) | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(json.dumps({k: (str(v)[:120] + '...' if len(str(v))>120 else v) for k,v in d.items()}, indent=2))"
```

The actual fields you'll see:

| Field | Where | What it has |
|---|---|---|
| `obj['role']` | every message | `session_meta`, `user`, `assistant`, `tool` |
| `obj['tools']` | session_meta only | Tool definitions (large) |
| `obj['tool_calls'][i]['function']['name']` | assistant msg | Tool name (e.g. `terminal`, `skill_view`) |
| `obj['tool_calls'][i]['function']['arguments']` | assistant msg | JSON-string of args (cmd, path, query) |
| `obj['tool_name']` / `obj['name']` | tool result | The tool that produced this result |
| `obj['content']` | tool result | Result payload (often a JSON-stringified dict) |

**Pitfall:** tool result `content` is usually a JSON-string (not parsed object) — you must `json.loads()` to extract fields like `name` (for skill_view), `path` (for read_file), `query` (for session_search).

**Pitfall:** the assistant message has the *call* (with args), the tool result has the *response* (with size). To map calls to results you have to walk the conversation linearly. Result sizes tell you the context cost; call counts tell you the behavior frequency.

## Reusable analysis template

The user has explicit "comprehensive diagnostics, not piecemeal" preferences — run this kind of analysis in **one pass** and report structured findings, not piecemeal answers.

```python
import json, glob, os
from collections import Counter, defaultdict

# Adjust path if session storage changes
SESSION_GLOB = '/root/.hermes/sessions/*.jsonl'

files = sorted(glob.glob(SESSION_GLOB))
print(f"Analyzed {len(files)} sessions")

# Counters
tool_call_count = Counter()         # how often each tool is CALLED
tool_result_bytes = Counter()       # total bytes each tool RETURNS to context
shell_command_first_word = Counter() # what shell commands are actually run
file_read_paths = Counter()          # what files are read

for f in files:
    for line in open(f, 'r', errors='ignore'):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        # Tool CALL (in assistant message)
        for tc in obj.get('tool_calls') or []:
            fn = tc.get('function', {}) or {}
            name = fn.get('name', '')
            tool_call_count[name] += 1
            if name in ('terminal', 'execute_code', 'process'):
                # Extract the actual command for first-word analysis
                try:
                    args = json.loads(fn.get('arguments', ''))
                    if isinstance(args, dict):
                        cmd = (args.get('command') or args.get('cmd') or args.get('code') or '').strip()
                        if cmd:
                            shell_command_first_word[cmd.split()[0]] += 1
                except Exception:
                    pass
            elif name in ('read_file', 'file_read'):
                try:
                    args = json.loads(fn.get('arguments', ''))
                    if isinstance(args, dict):
                        path = args.get('path') or args.get('file_path')
                        if path:
                            file_read_paths[path] += 1
                except Exception:
                    pass
        # Tool RESULT (in role:tool message)
        if obj.get('role') == 'tool':
            name = obj.get('tool_name') or obj.get('name') or ''
            content = obj.get('content') or ''
            if isinstance(content, list):
                content = json.dumps(content)
            tool_result_bytes[name] += len(content) if isinstance(content, str) else 0

# Report
print("\n=== Tool calls (frequency) ===")
for n, c in tool_call_count.most_common(20):
    print(f"  {c:>5}  {n}")
print(f"\n=== Tool results (context cost) ===")
total = sum(tool_result_bytes.values()) or 1
for n, b in tool_result_bytes.most_common(15):
    print(f"  {b/1024:>8.1f} KB  {n}  ({b/total*100:.1f}%)")
print(f"\n=== Top shell commands (first word) ===")
for c, n in shell_command_first_word.most_common(15):
    print(f"  {n:>4}  {c}")
print(f"\n=== Most-read files ===")
for p, n in file_read_paths.most_common(10):
    print(f"  {n:>3}  {p}")
```

## Reading the output

- **Tool call counts** tell you *behavior frequency* (e.g., "you call `terminal` 947 times in 82 sessions — heavy shell user?")
- **Tool result bytes** tell you *context cost* (e.g., "skill_view returns 1.8MB total — the largest single category")
- **Re-read detection**: for each path/file/tool, count calls and divide by unique count. > 2.0 means redundancy the upstream `dedup` should have caught but didn't.
- **Size distributions**: don't trust averages. Bucket calls by size (`<1KB`, `1-10KB`, `10-100KB`, `>100KB`). The 90th-percentile size matters more than the mean.

## Sample findings the user validated

- **RTK wasn't worth it for them.** Benchmarks showed 89% shell output compression; the data showed 1,013 shell calls averaging 1.7 KB each with zero calls >100KB. The benchmark didn't apply because they don't run `cargo test` or other noisy commands.
- **`hermes-agent` skill was loaded 19x in 82 sessions**, contributing 937KB (52% of all skill_view context). Confirmed by per-session, per-platform, per-model breakdown — Grok-4.3 loaded it 33% of the time vs DeepSeek 19% (model behavior, not system load).
- **read_file had 53% re-read rate** (97 of 183 calls were repeats). The upstream `dedup` PR should catch this but didn't, suggesting a configuration or version mismatch.

## Pitfalls

- **Don't use a small sample to generalize.** 82 sessions over 5 days isn't a long-term trend. If a question is high-stakes, sample larger or note the recency bias.
- **`.hms-bak` files are not sessions** — they're Hermes's own backup files. Exclude from analysis (`*.jsonl` only).
- **Empty `sessions.db` file is normal** — Hermes writes session data to JSONL, not SQLite, on most installs. The `.db` file is a 0-byte stub.
- **Profile-specific sessions live in `~/.hermes/profiles/<name>/sessions/`** — exclude from the main analysis OR analyze separately per profile if the question is profile-specific.
- **Assistant's `tool_calls[].function.arguments` is a JSON string, not an object** — must `json.loads()` before field access.
- **Tool result `content` is often a JSON-stringified dict** — must `json.loads()` to extract `name` (for skill_view), `path` (for read_file), `query` (for session_search), etc.
- **Don't conflate "tool call" and "tool result"** — they're separate messages. Call counts come from assistant messages; result sizes come from tool messages. To map them, walk linearly. To compare them, compute both.
- **Recommendations grounded in the data beat recommendations grounded in benchmarks.** When the data contradicts a general claim, the data wins. The user has strong "trust but verify" preferences and will catch recommendations not grounded in their actual workflow.
