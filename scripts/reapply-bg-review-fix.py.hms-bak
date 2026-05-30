#!/usr/bin/env python3
"""Reapply bg-review memory fix after Hermes upgrade.
Run this after: pip install --upgrade hermes-agent
Usage: python3 /root/work/scripts/reapply-bg-review-fix.py
"""
import sys

HERMES_HOME = "/usr/local/lib/hermes-agent"

# ── 1. Patch toolsets.py ─────────────────────────────────────────────
path = f"{HERMES_HOME}/toolsets.py"
with open(path) as f:
    content = f.read()

old_toolset = '''    "memory": {
        "description": "Persistent memory across sessions (personal notes + user profile)",
        "tools": ["memory"],
        "includes": []
    },'''

new_toolset = '''    "memory": {
        "description": "Persistent memory across sessions (personal notes + user profile) via Mnemosyne",
        "tools": [
            "memory",
            "mnemosyne_remember", "mnemosyne_recall", "mnemosyne_get_stats",
            "mnemosyne_sleep", "mnemosyne_scratchpad_read", "mnemosyne_scratchpad_write",
            "mnemosyne_invalidate", "mnemosyne_update", "mnemosyne_forget",
            "mnemosyne_export", "mnemosyne_import", "mnemosyne_diagnose",
            "mnemosyne_triple_add", "mnemosyne_triple_query",
            "mnemosyne_graph_query", "mnemosyne_graph_link",
        ],
        "includes": []
    },'''

if old_toolset in content:
    content = content.replace(old_toolset, new_toolset)
    with open(path, 'w') as f:
        f.write(content)
    print("[OK] toolsets.py — memory toolset expanded with Mnemosyne tools")
else:
    # Check if already patched
    if "mnemosyne_remember" in content:
        print("[SKIP] toolsets.py — already patched (mnemosyne_remember found)")
    else:
        print("[FAIL] toolsets.py — could not find original memory toolset definition")
        sys.exit(1)

# ── 2. Patch background_review.py ────────────────────────────────────
path = f"{HERMES_HOME}/agent/background_review.py"
with open(path) as f:
    content = f.read()

changes = 0

# 2a. Memory review prompt
old = 'save it using the memory tool. '
new = 'save it using mnemosyne_remember. Do NOT use the legacy memory tool \u2014 it is at capacity. '
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("[OK] background_review.py — memory review prompt fixed")
else:
    if 'mnemosyne_remember' in content and 'save it using mnemosyne_remember' in content:
        print("[SKIP] background_review.py — memory review already patched")
    else:
        print("[WARN] background_review.py — memory review prompt not found in expected form")

# 2b. Combined review prompt
old = 'preferences with the memory tool.\\n\\n'
new = 'preferences using mnemosyne_remember. Do NOT use the legacy memory tool.\\n\\n'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("[OK] background_review.py — combined review prompt fixed")
else:
    if 'preferences using mnemosyne_remember' in content:
        print("[SKIP] background_review.py — combined review already patched")
    else:
        print("[WARN] background_review.py — combined review prompt not found in expected form")

# 2c. Tool restriction message
old = 'You can only call memory and skill management tools. Other tools will be denied at runtime \u2014 do not attempt them.'
new = 'You can only call mnemosyne_remember, mnemosyne_recall, and skill management tools. The legacy memory tool is at capacity and will fail. Only use the tools listed above. Other tools will be denied at runtime. Do not attempt them.'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("[OK] background_review.py — tool restriction message fixed")
else:
    if 'You can only call mnemosyne_remember' in content:
        print("[SKIP] background_review.py — tool restriction already patched")
    else:
        print("[WARN] background_review.py — tool restriction not found in expected form")

if changes > 0:
    with open(path, 'w') as f:
        f.write(content)

# ── Summary ──────────────────────────────────────────────────────────
total = 3  # three patches in background_review.py
print(f"\nDone. {changes}/{total} background_review.py patches applied.")
if changes < total:
    print("Some patches were skipped (already applied or format differs).")
