#!/bin/bash
# Reapply background review patch after Hermes upgrade
#
# Run this after: pip install --upgrade hermes-agent
# Usage: bash /root/work/scripts/reapply-bg-review-fix.sh

set -e

HERMES_HOME="/usr/local/lib/hermes-agent"

echo "=== Reapplying bg-review memory fix ==="

# 1. Patch toolsets.py — add mnemosyne tools to 'memory' toolset
sed -i '/^    "memory": {/,/^    },/c\
    "memory": {\
        "description": "Persistent memory across sessions (personal notes + user profile) via Mnemosyne",\
        "tools": [\
            "memory",\
            "mnemosyne_remember", "mnemosyne_recall", "mnemosyne_get_stats",\
            "mnemosyne_sleep", "mnemosyne_scratchpad_read", "mnemosyne_scratchpad_write",\
            "mnemosyne_invalidate", "mnemosyne_update", "mnemosyne_forget",\
            "mnemosyne_export", "mnemosyne_import", "mnemosyne_diagnose",\
            "mnemosyne_triple_add", "mnemosyne_triple_query",\
            "mnemosyne_graph_query", "mnemosyne_graph_link",\
        ],\
        "includes": []\
    },' "$HERMES_HOME/toolsets.py"

echo "  [OK] toolsets.py patched"

# 2. Patch background_review.py prompts
python3 << 'PYEOF'
import re

path = "/usr/local/lib/hermes-agent/agent/background_review.py"
with open(path, 'r') as f:
    content = f.read()

# 2a. Memory review prompt
content = content.replace(
    'save it using the memory tool. ',
    'save it using mnemosyne_remember. Do NOT use the legacy memory tool \xe2\x80\x94 it is at capacity. '
)

# 2b. Combined review prompt
content = content.replace(
    'preferences with the memory tool.\\n\\n',
    'preferences using mnemosyne_remember. Do NOT use the legacy memory tool.\\n\\n'
)

# 2c. Tool restriction message
content = content.replace(
    'You can only call memory and skill management tools. Other tools will be denied at runtime \xe2\x80\x94 do not attempt them.',
    'You can only call mnemosyne_remember, mnemosyne_recall, and skill management tools. The legacy memory tool is at capacity and will fail. Only use the tools listed above. Other tools will be denied at runtime. Do not attempt them.'
)

with open(path, 'w') as f:
    f.write(content)

print("  [OK] background_review.py patched")
PYEOF

echo "=== Done. Both patches applied ==="
