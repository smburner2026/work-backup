# hermes-lcm Evaluation

**Date:** 2026-05-21
**Repo:** github.com/stephenschoettler/hermes-lcm (v0.11.1)
**Verdict:** GO — installed as context engine plugin

## What it is
Lossless Context Management plugin for Hermes Agent — replaces built-in ContextCompressor with a DAG-based context engine. Every message persisted verbatim in SQLite. Old context compacted into a hierarchical summary DAG (depth-0 leaf nodes → depth-1 condensations). 7 agent tools for retrieval: lcm_grep, lcm_load_session, lcm_describe, lcm_expand, lcm_status, lcm_doctor, lcm_expand_query.

## Code quality
- **Green flags:** 20+ well-separated modules, 11 test files, CI across Python 3.11-3.14 under low fd limit, 9 releases (v0.9.2→v0.11.1), multiple contributors
- **Yellow flags:** engine.py is 168KB monolithic, docs/ and scripts/ dirs empty, CI stubs Hermes ABC rather than end-to-end integration tests

## Compatible with our setup?
**Yes.** Hermes v0.14.0 has full pluggable context engine support:
- agent/context_engine.py — ContextEngine ABC
- agent/agent_init.py — loads engine via config context.engine
- plugins/context_engine/__init__.py — handles both register(ctx) plugin pattern and direct subclass discovery
- hermes_cli/plugins.py — PluginContext.register_context_engine()

## Installation
1. Clone to context engine dir: `git clone https://github.com/stephenschoettler/hermes-lcm.git /usr/local/lib/hermes-agent/plugins/context_engine/lcm/`
2. Set config: `context.engine: lcm`
3. Restart gateway

Trade-off: +lossless retention, +hierarchical DAG for token efficiency, +dedicated retrieval tools, -auxiliary model cost per compaction, -SQLite storage growth.

For the user's setup with compression at threshold 0.75 / protect_last_n: 20, LCM's default fresh_tail_count: 64 is more generous — more context preserved before compaction.
