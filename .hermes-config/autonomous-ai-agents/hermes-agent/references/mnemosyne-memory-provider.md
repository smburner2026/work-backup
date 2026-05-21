# Mnemosyne Memory Provider

[GitHub: AxDSan/mnemosyne](https://github.com/AxDSan/mnemosyne) ·
Package: `mnemosyne-memory` · License: MIT

A local-first memory provider for Hermes Agent with zero cloud dependencies.
Replaces the built-in memory system with a 3-tier BEAM architecture (Working
Memory → Episodic Memory → Scratchpad) using hybrid retrieval: sqlite-vec for
semantic search + FTS5 for keyword search, all in-process via SQLite.

## Architecture (BEAM)

- **Working memory:** hot context auto-injected via `pre_llm` hook, TTL-evicted.
- **Episodic memory:** long-term store with hybrid scoring (50% vector + 30%
  FTS5 + 20% importance) and temporal decay.
- **Scratchpad:** temporary reasoning workspace for the agent.
- **Triple store:** temporal knowledge graph with `valid_from`/`valid_until`
  and automatic invalidation.

## Key Differentiators vs. Cloud Providers (Honcho, Zep, Mem0)

| Feature | Mnemosyne | Cloud |
|---------|-----------|-------|
| Cost | Free forever | Paid tiers |
| Hosting | Local (your machine) | Cloud only |
| Latency (search) | ~1.2 ms | ~52–78 ms |
| Offline | Yes | No |
| Setup | `pip install mnemosyne-memory` | Docker + API keys |
| Vector store | sqlite-vec (built-in) | pgvector / external |
| Data ownership | You own the SQLite file | Vendor-hosted |
| Auto-consolidation | Sleep cycles built-in | Manual |
| Import | 7 providers (Mem0, Letta, Zep...) | N/A |

## Installation

### Using the Hermes venv (recommended on Linux VPS)

```bash
# Install into the active Hermes runtime venv
HERMES_VENV="/usr/local/lib/hermes-agent/venv"
$HERMES_VENV/bin/python -m pip install mnemosyne-memory

# With dense retrieval + local LLM (fastembed, ctransformers):
$HERMES_VENV/bin/python -m pip install 'mnemosyne-memory[all]'

# Register the Hermes plugin and set config
$HERMES_VENV/bin/python -m mnemosyne.install
# This symlinks ~/.hermes/plugins/mnemosyne/ → site-packages/hermes_memory_provider
# and sets memory.provider = mnemosyne in config.yaml

# Verify
hermes memory status
```

### Using the deploy script (no pip needed)

```bash
curl -sSL https://raw.githubusercontent.com/AxDSan/mnemosyne/main/deploy_hermes_provider.sh | bash
```

### Post-install: install optional dependencies

Mnemosyne needs `sqlite-vec` and `fastembed` for vector search and embeddings.
Without them, semantic/hybrid retrieval won't work:

```bash
pip install sqlite-vec mnemosyne-memory[embeddings] huggingface_hub
```

Verify with:

```bash
mnemosyne diagnose --dry-run
# Target: 7/25+ checks passed. Dependencies should show healthy.
```

### Test from Python

```python
from mnemosyne import Mnemosyne
m = Mnemosyne()
m.remember("User prefers dark mode.", scope="global")
results = m.recall("what theme does the user like?")
```

## Activation

### Setting the provider

Mnemosyne must be set as the active memory provider in config.yaml:

```yaml
memory:
  provider: mnemosyne       # switch from "built-in" (default)
```

### ⚠️ Pitfall: Duplicate YAML keys silently break activation

The install script or manual edit can create a duplicate `provider` key in the
`memory:` section. YAML silently uses the **last** value when keys are
duplicated:

```yaml
memory:
  provider: mnemosyne      # <-- set by install script
  memory_enabled: true
  user_profile_enabled: true
  provider: ''             # <-- duplicate overrides to empty string!
```

Result: every session runs the built-in memory, not Mnemosyne. The config
appears correct at a glance.

**Fix:** Remove the empty duplicate:
```bash
# Open config and ensure only ONE provider: line exists in the memory: block
hermes config edit
```

Or check programmatically:
```bash
grep -c "provider:" ~/.hermes/config.yaml
# Should be 1 in the memory: block. If 2+, there's a duplicate.
```

### Provider is loaded under an alias namespace

Hermes loads user-installed memory plugins under the namespace
`_hermes_user_memory.<name>` (see `plugins/memory/__init__.py` line 196).
This prevents the plugin's directory name from shadowing the pip-installed
`mnemosyne` package in `sys.modules`. It just works — no user action needed.

### How to verify it's active

```bash
# 1. Check the config key is there and correct
grep -A5 "provider: mnemosyne" ~/.hermes/config.yaml

# 2. Run a Python probe through Hermes's loader
python3 -c "
import sys; sys.path.insert(0, '/usr/local/lib/hermes-agent')
from plugins.memory import load_memory_provider
p = load_memory_provider('mnemosyne')
print('Loaded:', p)
print('Available:', p and p.is_available())
"

# 3. Check mnemosyne stats
mnemosyne stats
# Total memories should grow as sessions run
```

### Config changes

Config changes take effect on next session start (`/reset` in chat, or
start a new `hermes` process). The gateway needs a `/restart`.

### Configurable settings

These go under `memory.mnemosyne.<key>` in config.yaml:

| Key | Default | Description |
|-----|---------|-------------|
| `auto_sleep` | `false` | Auto-consolidate working→episodic when threshold exceeded |
| `sleep_threshold` | `50` | Working memory count before auto-sleep triggers |
| `vector_type` | `int8` | Vector precision: `float32`, `int8`, or `bit` |
| `ignore_patterns` | `[]` | Regex patterns to filter from memory storage |
| `profile_isolation` | `false` | Separate DB per Hermes profile via Mnemosyne banks |

Note: `hermes config show` does NOT display memory provider settings — you
must inspect config.yaml directly or use `grep`.

## Graceful Degradation (What breaks if it breaks)

Mnemosyne is loaded inside a try/except in `agent/agent_init.py` (lines
975-1033). Every failure path sets `agent._memory_manager = None` — it never
prevents Hermes from starting:

| Scenario | Behaviour |
|----------|-----------|
| Plugin fails to import | Exception caught → memory manager set to None → session continues |
| Plugin imported but `is_available()` returns False | Provider not added → memory manager has no providers → tools omitted |
| Plugin raises at runtime (e.g. DB corruption) | Caught per-call — logged, never crashes the agent loop |
| Provider name is empty string | `if _mem_provider_name and _mem_provider_name.strip():` → False → skipped entirely |

The **built-in `memory` tool** is part of the core agent framework, not the
external memory provider. It continues to work regardless of which provider
is configured or whether the provider is healthy. You never lose the ability
to store and retrieve persistent facts.

### Reverting (fallback safety)

```bash
hermes config set memory.provider built-in
```

Then restart (`/restart` in gateway, new session in CLI). The original session
DB (`~/.hermes/state.db`) is untouched by Mnemosyne — it operates on its own
SQLite store at `~/.hermes/mnemosyne/data/mnemosyne.db`. Session search
remains functional regardless of which provider is active.

To uninstall completely:

```bash
hermes config set memory.provider built-in
rm -rf ~/.hermes/plugins/mnemosyne
pip uninstall mnemosyne-memory
```

## Invariants

- **Not a session search replacement.** Mnemosyne is a memory *abstraction*
  layer over conversations. The session DB (`state.db`) still records raw
  transcripts; the `session_search` tool still queries those via FTS5.
  Mnemosyne adds semantic retrieval and structured fact extraction on top.
- **Auto-consolidation:** Mnemosyne's `sleep()` cycle compresses working
  memory into episodic memory. May happen on a timer or after session end.
- **LLM-dependent extraction:** entity extraction uses regex/Levenshtein
  (no spaCy), but fact extraction needs an LLM. Routes through Hermes's
  host provider, a remote API, or local ctransformers with graceful failure.
- **Import tool:** can migrate from Honcho, Mem0, Letta (MemGPT), Zep,
  Hindsight, Memobase, and MemPalace.
- **Plugin vs pip package relationship:** the plugin at
  `~/.hermes/plugins/mnemosyne/` is a symlink to
  `hermes_memory_provider/` inside the installed `mnemosyne-memory` pip
  package. It provides the Hermes MemoryProvider interface (pre/post-turn
  hooks, tool schema injection). The pip package provides the core Mnemosyne
  engine (BEAM, embeddings, vector store). Both must be present.
