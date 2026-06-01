---
name: doga-thinking-layer
description: "DOGA — probabilistic, goal-aware thinking layer for Hermes Agent. Six Thinking Hats guidance, Monte Carlo simulation, recursive reasoning, Mnemosyne goal memory integration. Active as Hermes plugin hooks on every turn."
version: 1.0.0
author: Hermes + 0z1-ghb
tags: [doga, thinking, probabilistic, monte-carlo, six-hats, mnemosyne, memory]
---

# DOGA — Probabilistic Thinking Layer

## Overview

DOGA is a Hermes plugin (`/root/.hermes/plugins/doga/`, v1.1.0) that runs as hooks on every LLM call. It injects structured thinking guidance before the call, formats output after, and tracks tool usage. Provides the `simulate` (Monte Carlo) and `reason_deeper` (recursive reasoning) tools.

## Active Hooks

| Hook | What it does |
|------|-------------|
| `pre_llm_call` | Injects `world_model_guide` thinking prompt with Six Thinking Hats. Queries Mnemosyne for past goal patterns. |
| `transform_llm_output` | Strips guide blocks, saves detected goal type to Mnemosyne, formats output with simulation summary if available. |
| `post_tool_call` | Tracks `simulate` and `reason_deeper` tool usage, manages recursion depth. |

## Mnemosyne Integration

Active by default (`memory_enabled: True`). Requires `mnemosyne-memory` pip package (installed as `doga-hermes[memory]` optional dependency).

**Pre-LLM (recall):** On every user message, DOGA calls `recall(user_message, top_k=3)` to find past goal patterns. Results are injected as `past_patterns` context in the thinking prompt so the LLM sees the distribution of previous goal types encountered.

**Post-LLM (remember):** After each response, DOGA picks the dominant `world_model` goal type (Information / Understanding / Action) via regex and saves: `remember(content=message, importance=0.7, source="doga_goal", metadata={goal_type, depth})`.

## Configuration via `/doga` Slash Command

| Subcommand | Effect |
|-----------|--------|
| `on` / `off` | Enable/disable DOGA entirely |
| `status` | Show current settings, memory status |
| `auto` | Automatic depth selection (default — assesses complexity per query) |
| `manual low\|medium\|high` | Force a specific thinking level |
| `depth <1-5>` | Set depth manually, switches to manual mode |
| `hats on\|off` | Enable/disable Six Thinking Hats |
| `max_recursion <1-5>` | Max recursion depth for reason_deeper (default: 3) |
| `show\|hide` | Show/hide simulation panel in responses |
| `memory on\|off` | Enable/disable Mnemosyne goal memory |
| `help` | Full command reference |

## Tools Provided

### `simulate` — Monte Carlo probability engine

Runs N iterations (default 10K, max 50K) over probabilistic scenarios with independent binary variables and optional logical conditions. Returns probability distribution with per-scenario breakdown. Use when quantitative weighing of uncertain factors is needed.

### `reason_deeper` — Recursive self-critique

Triggers next recursion level with focus-specific De Bono hat pair. Tracked via `_reasoning_stack` (thread-local). Hard stop after 3 consecutive stop signals. Each level uses a different hat pair for diverse lens coverage.

## Six Thinking Hats

Active by default at the configured depth (1-5). Each depth activates a different set of parallel thinking lenses:

| Depth | Hats Active |
|-------|------------|
| 1 | White (facts) |
| 2 | White, Black (risks) |
| 3 | White, Black, Yellow (benefits) |
| 4 | White, Black, Yellow, Green (alternatives) |
| 5 | White, Black, Yellow, Green, Red (intuition) |

Recursion levels use their own hat pairs, rotating through different lenses per depth.

## Known Limitations (from creator)

- Depth selection is manual by default; auto-depth still experimental
- Not extensively tested with reasoning models (Claude, GPT-4)
- Goal type detection via simple regex (`Information|Understanding|Action`) — may miss edge cases
- Mnemosyne integration is Phase 1 — recall uses flat top-k, no temporal decay or recency bias

## Pitfalls

- **DOGA writes to Mnemosyne on every turn** — if HMS sync is active simultaneously, the WAL desync risk is elevated. Coordinate sync windows with the sync guard the user has set up.
- **`simulate` runs inside the Hermes process** — expensive calls (50K iterations, many scenarios) can delay response. Default 10K iterations is fine for most cases.
- **The `world_model_guide` block is DOGA's injection** — not native Hermes behavior. If the output feels overly structured or the thinking frame is wrong, toggle with `/doga hats off` or `/doga off`.
- **Goal type is coarse** — only Information/Understanding/Action are classified. If you see `world_model` blocks that seem miscategorized, it's the regex, not deeper reasoning.
