# DOGA Plugin Evaluation — Full Audit

**Evaluated:** 2026-05-24
**Source:** https://github.com/0z1-ghb/doga-hermes
**Version:** v1.1.0 (25 commits, 1 release)
**Verdict:** GO — installed and enabled

## What It Is

DOGA (Doğa = "nature" in Turkish) is a Hermes plugin that injects a probabilistic, goal-aware reasoning layer before every LLM call. It adds scenario simulation (Monte Carlo), structured multi-perspective reasoning (De Bono Six Thinking Hats), and recursive self-critique to the agent's responses.

## Code Quality

### Green Flags

- **AST-whitelisted condition evaluation** — The Monte Carlo engine uses `ast.parse()` + an allowlist of safe node types (`ast.BoolOp`, `ast.Compare`, `ast.Name`, `ast.Constant`, etc.) instead of raw `eval()`. Any node type not in the whitelist causes a safe False return. + Restricted globals (`{"__builtins__": {}}`).
- **Thread-safe design** — Per-turn state uses `threading.local()` to prevent cross-session contamination in concurrent conversations. Monte Carlo engine creates a fresh `random.Random` instance per call (no shared RNG state).
- **Bounded caching** — Condition compilation cache capped at 1024 entries; clears when full. No memory leak risk.
- **Recursion limits** — `reason_deeper` tool has a configurable `max_recursion` (default 3) with a hard break after 3 ignored stop signals. Can't infinite-loop.
- **Type-annotated** — Full type hints across all files.
- **Clean decomposition** — 6 files, each with a single responsibility (simulation engine, De Bono hats, depth selection, output formatting, thinking prompts, plugin init).
- **Pure plugin** — No modifications to core Hermes files. Uses only the official plugin hooks API (`pre_llm_call`, `transform_llm_output`, `post_tool_call`).

### Minor Concerns

- **`estimate_from_description()` is a stub** — Static method in MonteCarloEngine always returns a single `{"name": "base_case", "variables": {"likelihood": 0.5}}`. Would be more useful if it parsed the query to extract variables automatically.
- **Goal detection is regex, not LLM** — The `transform_llm_output` hook pattern-matches for "Information|Understanding|Action" in the response. Simple but fragile — a mixed query (e.g., "show me the data then tell me what to do") gets one label only.
- **Hardcoded entropy thresholds** — High uncertainty = entropy > 1.5, medium > 0.5, low = else. Reasonable defaults but not configurable.
- **No tests shipped** — The repo has a `tests/` directory but no visible test content in the version evaluated.

## Security Audit

| Risk | Status |
|------|--------|
| `eval()` / `exec()` / `compile()` | None found |
| Raw `subprocess` / `os.system()` | None found |
| Network calls to hardcoded endpoints | None found |
| File writes outside plugin paths | None found (no file write capability at all) |
| Dangerous imports | None found (stdlib only + optional mnemosyne) |
| Unsanitized user input in critical paths | Conditions use AST whitelist |
| Supply chain risk | Zero runtime dependencies |

## Compatibility

- **Hermes plugin API** — Uses `ctx.register_hook()`, `ctx.register_tool()`, `ctx.register_command()` — matches the current plugin system (`hermes_cli/plugins.py`).
- **Hooks used:** `pre_llm_call`, `transform_llm_output`, `post_tool_call` — all are valid hooks in the Hermes plugin system.
- **Tools registered:** `simulate` (toolset: `doga`), `reason_deeper` (toolset: `doga`)
- **Command registered:** `/doga` with subcommands
- **Python version:** >= 3.10 — matches our runtime.
- **Mnemosyne:** Optional. Handled via try/except import guard, degrades gracefully.

## Installation Procedure

```bash
# Clone
git clone https://github.com/0z1-ghb/doga-hermes.git /tmp/doga-hermes

# Copy to user plugins
mkdir -p ~/.hermes/plugins/doga
cp /tmp/doga-hermes/doga/*.py ~/.hermes/plugins/doga/
cp /tmp/doga-hermes/plugin.yaml ~/.hermes/plugins/doga/

# Enable
hermes plugins enable doga

# Verify
hermes plugins list | grep doga   # → "doga │ enabled │ 1.1.0"

# Activate (new session)
/reset
```

## How It Works (Architecture Summary)

### Prompt Injection (pre_llm_call)
1. Resets recursion state for the turn
2. Assesses complexity (auto) or uses configured depth (manual)
3. Selects active De Bono hats for the depth level
4. Recalls past goal patterns from Mnemosyne (optional)
5. Builds a `<world_model_guide>` block with goal detection + scenario enumeration + hat guidance
6. Returns as `{"context": guide}` — appended to user message

### Output Transformation (transform_llm_output)
1. Strips the `<world_model_guide>` blocks from the LLM output
2. Detects goal type from the cleaned response via regex
3. Saves goal to Mnemosyne with importance=0.7
4. Formats simulation panel display (show/hide)

### Post-Tool-Call Tracking
1. Logs `simulate` tool usage
2. Tracks `reason_deeper` recursion depth + stack

### Monte Carlo Engine
- AST-whitelisted boolean expression evaluation with bounded cache
- Nested scenario support (children)
- Shannon entropy classification
- Default: 10K iterations, max 50K
- Fresh `random.Random(seed=42)` per call in convenience mode

## Available Configuration

| Setting | Default | Range |
|---------|---------|-------|
| `enabled` | True | on/off |
| `auto_depth` | True | auto/manual |
| `depth` | 3 | 1-5 |
| `show_simulation` | True | show/hide |
| `max_scenarios` | 5 | 1-N |
| `de_bono_enabled` | True | on/off |
| `max_recursion` | 3 | 1-5 |
| `memory_enabled` | True | on/off (needs Mnemosyne) |

## De Bono Hat Mapping by Depth

| Depth | Hats | Coverage |
|-------|------|----------|
| 1 | White | Facts, data, constraints |
| 2 | White, Black | Facts + risks |
| 3 | White, Black, Yellow | Facts + risks + benefits |
| 4 | White, Black, Yellow, Green | + creative alternatives |
| 5 | White, Black, Yellow, Green, Red | + intuition/gut feeling |

## Recursion Hat Rotation

Each `reason_deeper` call applies a different lens:
- Level 1: White + Black + Yellow (facts, risks, benefits)
- Level 2: Black + Green (critique + alternatives)
- Level 3: Red + Green (intuition + creative pivot)
- Level 4: Black + Yellow (deep trade-off analysis)
- Level 5: White + Red (revisit facts with intuition)
