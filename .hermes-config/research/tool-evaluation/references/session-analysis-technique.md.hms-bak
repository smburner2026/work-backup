# Session Analysis Technique — Verifying Tool Applicability via Actual Usage

**Purpose:** When recommending a tool that targets a specific use case, query the user's actual session history to verify the use case exists. A tool's benchmark describes capability; session analysis describes applicability. Both must align for a GO verdict.

**When to use:**
- The tool has a benchmark-driven pitch ("saves 80% on X" where X is a specific workload)
- The recommendation hinges on the user doing a particular kind of work
- The user says "I don't know if I actually do that" (treat as a green light to verify, not a hand-wave)
- Before installing any tool that targets a specific use case (CLI compression, file processor, image tool, etc.)

**When to skip:**
- The tool targets a generic capability (file sync, password manager, note-taking)
- The use case is universal (a Python formatter, a JSON validator)
- The user has explicitly described their workflow in detail and the analysis is redundant

## Where the data lives

Sessions are stored as JSONL at `~/.hermes/sessions/*.jsonl`. Each line is a message in a session (user, assistant, tool, system). Tool call invocations and tool results are the two most informative message types.

**Schema reminders (from real data):**

```json
// Assistant message with tool calls
{
  "role": "assistant",
  "tool_calls": [
    {
      "function": {
        "name": "terminal",
        "arguments": "{\"command\": \"ls -la /root\"}"
      }
    }
  ]
}

// Tool result
{
  "role": "tool",
  "tool_name": "terminal",
  "content": "{\"output\": \"...\"}"
}
```

**Gotchas:**
- `tool_name` may also appear as just `name` — check both
- `content` may be a string OR a list (sometimes JSON-encoded) — normalize
- Some sessions are huge (150+ KB) — stream line-by-line, don't load the file
- Empty `tool_calls` arrays are common — skip them
- Malformed JSON happens — wrap in `try/except`

## The query patterns

### Pattern 1: Tool call frequency (what the user invokes)

```python
import json, glob
from collections import Counter

files = sorted(glob.glob('/root/.hermes/sessions/*.jsonl'))
tool_call_count = Counter()

for f in files:
    for line in open(f, 'r', errors='ignore'):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        for tc in obj.get('tool_calls') or []:
            name = tc.get('function', {}).get('name', '')
            tool_call_count[name] += 1

# Top tools by call count
for name, n in tool_call_count.most_common(30):
    print(f"  {name:<35} {n:>5}")
```

### Pattern 2: Tool result sizes (what dominates context)

```python
tool_result_total_bytes = Counter()

for f in files:
    for line in open(f, 'r', errors='ignore'):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get('role') != 'tool':
            continue
        name = obj.get('tool_name') or obj.get('name') or ''
        content = obj.get('content') or ''
        if isinstance(content, list):
            content = json.dumps(content)
        size = len(content) if isinstance(content, str) else 0
        tool_result_total_bytes[name] += size

# Top tools by total result bytes
for name, b in tool_result_total_bytes.most_common(20):
    print(f"  {name:<35} {b/1024:>8.1f} KB")
```

### Pattern 3: Shell command first-words (the actual programs)

```python
shell_command_first_word = Counter()

for f in files:
    for line in open(f, 'r', errors='ignore'):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        for tc in obj.get('tool_calls') or []:
            name = tc.get('function', {}).get('name', '')
            if name in ('terminal', 'execute_code', 'process'):
                args_raw = tc.get('function', {}).get('arguments', '')
                try:
                    args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                    cmd = args.get('command') or args.get('cmd') or args.get('code') or ''
                    first = cmd.strip().split()[0] if cmd.strip() else '(empty)'
                    shell_command_first_word[first] += 1
                except Exception:
                    pass

# Top shell programs
for cmd, n in shell_command_first_word.most_common(25):
    print(f"  {cmd:<25} {n:>5}")
```

### Pattern 4: Result size distribution per tool

```python
size_buckets = Counter()
for size in shell_sizes:
    if size < 1024: size_buckets['<1KB'] += 1
    elif size < 5120: size_buckets['1-5KB'] += 1
    elif size < 20480: size_buckets['5-20KB'] += 1
    elif size < 102400: size_buckets['20-100KB'] += 1
    else: size_buckets['>100KB'] += 1
```

The long tail (>20 KB) is where optimization tools actually have something to compress. If a tool's target is the 1-5 KB range, it's optimizing the wrong tail.

### Pattern 5: Top result-size outliers (the dominant calls)

```python
skill_view_examples.sort(reverse=True)  # by size
for size, name, sample in skill_view_examples[:20]:
    print(f"  {size/1024:>6.1f} KB  {name}")
```

Often a single repeated call (same skill, same search query) dominates a category. Fixing the call site fixes the bloat.

## How to use the findings

**Decision matrix:**

| Question | If yes | If no |
|---|---|---|
| Does the user call the tool's target category at all? | Continue | NO-GO: tool targets nonexistent use case |
| Do those calls produce the size range the tool targets? | Continue | NO-GO: tool optimizes the wrong tail |
| Does the user have a top-1 outlier that dominates the category? | Investigate outlier (might be a single bad call) | Continue |
| Is the user already doing something similar in their existing stack? | Check preconditions / overlap | Continue |
| Is the install cost (disk, deps, time) > the expected savings? | NO-GO: cost > benefit | **GO with caveats** (escape hatch, smoke test) |

**Output format (when the analysis changes the verdict):**

```markdown
## Empirical Verification: [tool-name]

**Method:** Queried `~/.hermes/sessions/*.jsonl` ([N] sessions, [size] total, [calls] tool calls).

**Findings:**
- [Tool] result bytes: [X] KB across [Y] calls, avg [Z] KB
- Top commands/programs: [list]
- Size distribution: [buckets]

**The mismatch (or match):** [Tool] targets [use case]. User's actual [X] is [different/same]. [Verdict reasoning.]

**When this would flip:** [Workload shift that would change the verdict.]
```

Save the analysis under `references/session-analysis-<toolname>.md` so future sessions can re-validate without re-querying.

## Cost of the analysis

- ~50 lines of Python, runs in <1 second
- One web/file read of the session corpus
- The output (a few hundred characters) is a permanent reference

**This is the cheapest verification step in the framework.** If the analysis would change the verdict, the cost-benefit is overwhelmingly positive. If it wouldn't change the verdict (the tool is generic, the use case is universal), the cost is one minute of dead time — still worth it.

## Limitations

- **Session corpus is point-in-time.** A user with a Rust project in active development might shift to a shell-heavy profile in two weeks. Re-run the analysis when recommending to a new project, or when the user says "I'm starting X."
- **Sessions may be partial.** Hermes uses LCM compaction for long sessions. Recent sessions are full; older ones may be summarized. The first ~80 sessions in this user's history were full JSONL; later ones may be different. Verify by sampling.
- **Platform matters.** A user with most activity on Telegram mobile may have very different patterns than one driving via CLI. The platform is in the session meta — check it before generalizing.
- **Skill-call data may not reflect skill content loaded.** `skill_view` calls show the skill was loaded, but they don't show what was loaded automatically as part of system prompt. The always-loaded cost (USER.md, MEMORY.md, skills registered in the system prompt) is separate from on-demand skill_view. For comprehensive context accounting, audit `~/.hermes/SOUL.md` and skill manifests too.

## Related patterns

- **Phase 5b in SKILL.md — Forum-Debate Stress Test:** Combine with session analysis. The forum debate surfaces *evidence weaknesses*; session analysis surfaces *use-case mismatches*. Both are cheap. Run both before a final recommendation.
- **Phase 4b in SKILL.md — Listicle Review:** Session analysis is particularly useful for listicle recommendations, where you have 5+ tools to evaluate and can't deep-dive all of them. Triage by Phase 4b first, then session-analysis the credible ones.
- **Phase 5d in SKILL.md — Solve With Existing Capabilities:** The "edit existing before adding new" rule. Session analysis often reveals that the existing tools have parameters (limit, offset, window) that the user isn't using. Configuration changes are free.
