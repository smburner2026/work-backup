---
name: codebase-inspection
description: "Inspect codebases: LOC metrics (pygount) AND rapid architecture analysis of open-source repos."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository, Architecture, Open Source]
    related_skills: [github-repo-management, writing-plans]
prerequisites:
  commands: [pygount]
---

# Codebase Inspection

Two complementary methodologies for inspecting codebases: quantitative (LOC metrics) and qualitative (architecture analysis).

---

## PART 1: LOC Analysis with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

### When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- User wants code-vs-comment ratios
- General "how big is this repo" questions

### Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

### 1. Basic Summary (Most Common)

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

### 2. Common Folder Exclusions

Adjust based on the project type:

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

### 3. Filter by Specific Language

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

### 4. Detailed File-by-File Output

```bash
# Default format shows per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Sort by code lines (pipe through sort)
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

### 5. Output Formats

```bash
# Summary table (default recommendation)
pygount --format=summary .

# JSON output for programmatic use
pygount --format=json .

# Pipe-friendly: Language, file count, code, docs, empty, string
pygount --format=summary . 2>/dev/null
```

### 6. Interpreting Results

The summary table columns:
- **Language** — detected programming language
- **Files** — number of files of that language
- **Code** — lines of actual code (executable/declarative)
- **Comment** — lines that are comments or documentation
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled, etc.)
- `__generated__` — auto-generated files (detected heuristically)
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized file types

### Pitfalls

1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.

---

## PART 2: Architecture Analysis (Rapid Open-Source Repo Assessment)

Rapidly analyze a GitHub repository's architecture to understand what it does, how it's built, whether it's well-engineered, and what patterns are worth adopting. This is NOT about LOC counts — it's about reading the code to understand design decisions.

### When to Use

- User asks "is this repo useful or hype?"
- User wants to understand how a project works architecturally
- User wants to extract reusable patterns from an open-source project
- User asks "should we adopt patterns from project X?"
- Evaluating whether to depend on a library or fork a project

### The 7-Step Methodology

#### Step 1: Triage

Before reading code, get the meta-picture:

```python
# Check the repo
curl -sL "https://api.github.com/repos/owner/repo" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f\"Stars: {d.get('stargazers_count','N/A')}\")
print(f\"Description: {d.get('description','N/A')}\")
print(f\"Language: {d.get('language','N/A')}\")
print(f\"Last push: {d.get('pushed_at','N/A')}\")
print(f\"License: {d.get('license',{}).get('spdx_id','N/A')}\")
"
```

What to look for:
- **Stars vs age**: 10k+ stars in <1 year = heavy marketing. 5k stars over 3 years = organic growth.
- **Author**: Research lab (Stanford, HKU, Berkeley) vs solo dev vs company. Lab repos tend to have better engineering.
- **Language**: Python repos are easiest to analyze. JS/TS next. Go/Rust tighter codebases.
- **License**: MIT/APACHE = permissive. AGPL = red flag for commercial use.

#### Step 2: README & Surface

Read the README to understand:
- **Project goals** — what problem does it solve?
- **Architecture diagram** — does it have one? If yes, it's well-documented.
- **Features** — listed features vs actual code coverage
- **Quick start** — does `pip install` actually work? Is there a demo?
- **Benchmarks** — numbers presented without methodology = marketing

```bash
curl -sL "https://raw.githubusercontent.com/owner/repo/main/README.md" | head -200
```

Look for red flags:
- "Enterprise-grade" with no tests
- Claims of "autonomous" anything without showing the loop
- "AI-powered" as the only feature description
- No architecture diagram or code structure explanation

#### Step 3: Dependency Analysis

Read the build file (pyproject.toml, package.json, Cargo.toml) to understand the tech stack and dependencies:

```bash
curl -sL "https://raw.githubusercontent.com/owner/repo/main/pyproject.toml" 2>/dev/null
```

What to look for:
- **Heavy dependencies** on a single library (e.g., `swarms`, `langchain`) = thin wrapper
- **Version numbers**: 0.1.x = very early stage. 1.x = mature.
- **Optional deps** (extras) tell you what the project considers non-core
- **Author's other projects** — if the same person maintains 20 repos, each is shallow
- **Peer deps** — does it depend on the author's other libraries? Circular portfolio.

#### Step 4: Directory Structure

Map the source tree to identify modules:

```python
# Get repo contents
curl -sL "https://api.github.com/repos/owner/repo/contents/src_or_browser_use" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if isinstance(d,list):
    for item in sorted(d, key=lambda x: x['type']=='dir', reverse=True):
        print(f\"{'📁' if item['type']=='dir' else '📄'} {item['name']}\")
"
```

Key modules to identify in AI agent repos:
- `agent/` — the main loop
- `browser/` or `controller/` — infrastructure layer
- `tools/` or `actions/` — action/tool registry
- `llm/` or `providers/` — LLM abstraction
- `dom/` or `view/` — page/content extraction
- `scripts/` or `bin/` — CLI entry points

In general repos, look for:
- Clear separation of concerns (data models, services, interfaces)
- Config files in YAML/JSON (declarative config is a good sign)
- Tests directory with actual tests

#### Step 5: Core Loop

Read the main execution loop — this is the heart of any agent project:

```python
# For agent repos, find the step() or run() method
# For other repos, find the main entry point
```

Questions to answer:
1. **How does it actually work?** Is it a simple chain or a proper loop?
2. **Error handling** — what happens when the LLM fails? Timeout? Rate limit?
3. **State management** — is state persisted? Can it resume?
4. **Event-driven or synchronous?** Event-driven scales better.
5. **How is context managed?** Message compaction, token tracking?

#### Step 6: Data Models & Config

Read the data models and configuration to understand the system's shape:

```bash
curl -sL "https://raw.githubusercontent.com/owner/repo/main/src/agent/views.py" 2>/dev/null | head -100
curl -sL "https://raw.githubusercontent.com/owner/repo/main/browser_use/agent/views.py" 2>/dev/null | head -100
```

What to look for:
- **Pydantic models** — well-typed = good engineering
- **State enums** — lifecycle states show maturity
- **Config surface** — how many knobs? Too few = inflexible. Too many = over-engineered.
- **Union types / generics** — proper typing = production-grade

#### Step 7: Evaluate & Extract

Synthesize findings into a verdict with three categories:

**Useful patterns** — things worth adopting:
- Tool registration with dependency injection
- Message compaction strategies
- Loop detection with escalating nudges
- Event-driven architecture patterns
- AX Tree → serialized DOM extraction

**Hype markers** — things that signal surface-level quality:
- "Enterprise-grade" with no tests
- Claims of autonomy without showing the loop
- Heavy marketing with thin code
- One-person portfolio of 20+ repos, all shallow
- Version 0.1.x with 10k+ stars (marketing > substance)

**Reality checks** — contextual evaluation:
- Would you run this with real money? Real data? Production traffic?
- What happens at failure? At scale? Under load?
- Is the README aspirational or accurate?

### Example Walkthrough (from a real session)

**Repo**: browser-use/browser-use (96k⭐)

1. **Triage**: 96k⭐, Python, MIT, active. High stars but mature project.
2. **README**: Real architecture content, benchmarks, demos, API docs.
3. **Deps**: aiohttp, pydantic, httpx, cdp-use — lean but capable. No single-framework lock-in.
4. **Structure**: agent/, browser/, tools/, dom/, llm/, mcp/ — proper separation.
5. **Core loop**: step() → _prepare_context → _get_next_action → _execute_actions → _post_process. Clean ReAct loop with error handling, compaction, loop detection.
6. **Data models**: Rich Pydantic models, state enums, typed action registry with dependency injection.
7. **Verdict**: Genuinely well-engineered. Patterns worth adopting: Tool Registry (typed actions + injected context), Message Compaction, Loop Detection, AX Tree → Serializable DOM, Domain-based Action Filtering.

### Reference Files

This skill ships with reference files documenting architecture patterns extracted from real repos:

- `references/browser-use-architecture.md` — architectural patterns from browser-use/browser-use

See the `references/` directory for detailed extracts from each analyzed project.

### Pitfalls

1. **Don't judge by stars alone** — 2.9k⭐ on a month-old repo is marketing, not quality. 96k⭐ on a 2-year-old repo with 20 contributors is real traction.
2. **Don't read the whole codebase** — focus on: README → deps → directory structure → core loop → data models. That's 80% of the architecture signal in 20% of the files.
3. **Don't skip the config** — pyproject.toml tells you more about a project than most source files. Dependencies, version, author, build system.
4. **Don't trust what the README says** — verify by reading the actual code. "Multi-agent swarm" might be a single for-loop calling the same LLM 4 times.
5. **Don't skip error handling code** — the error handler tells you the maturity level. If there's no retry logic, no timeout handling, no state recovery, it's not production-ready.
6. **Version numbers matter** — v0.1.x = proof of concept. v0.5+ = maturing. v1.0+ = production claims have some weight.
