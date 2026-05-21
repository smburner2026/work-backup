# Open WebUI Lean Install (No PyTorch / No ML Stack)

Open WebUI's `pip install` drags in ~2GB of ML dependencies (PyTorch, CUDA
toolkits, ChromaDB, sentence-transformers, faster-whisper, onnxruntime,
transformers, etc.) that are only needed for local RAG/embeddings/STT.

When using Open WebUI strictly as a chat frontend for Hermes Agent's API
server, none of that is needed. This reference documents a lean install that
skips the ML bloat.

## Architecture

```
Browser → Open WebUI (port 8080) → Hermes API Server (port 8642) → LLM
```

Open WebUI talks to Hermes via the OpenAI-compatible API endpoint. Hermes
handles all tool calls, memory, skills. Open WebUI is just the web UI.

## Step-by-Step Lean Install

### 1. Configure Hermes API Server

Add to `~/.hermes/.env`:

```
API_SERVER_ENABLED=true
API_SERVER_KEY=<generate a random key>
API_SERVER_HOST=127.0.0.1
API_SERVER_PORT=8642
API_SERVER_MODEL_NAME=Hermes Agent
```

### 2. Start Hermes Gateway

```bash
hermes gateway run   # background: terminal(background=true)
# Verify: curl http://127.0.0.1:8642/health
# Verify models: curl -H "Authorization: Bearer $KEY" http://127.0.0.1:8642/v1/models
```

### 3. Create Venv and Install Open WebUI (Without ML Deps)

```bash
python3.11 -m venv ~/.local/open-webui-venv
source ~/.local/open-webui-venv/bin/activate

# Install the package without automatic dependency resolution
pip install open-webui --no-deps

# Extract pinned deps from the wheel, then install only the ones needed
# for the web server (skipping ML/NLP/vision/audio packages)
python3 << 'PYEOF'
import zipfile, re
with zipfile.ZipFile(glob.glob('/tmp/openwebui-wheel/open_webui-*.whl')[0]) as z:  # or download
    with z.open('open_webui-0.9.5.dist-info/METADATA') as f:
        deps = [l.replace('Requires-Dist: ', '') for l in f.read().decode().splitlines()
                if l.startswith('Requires-Dist:') and 'extra ==' not in l]

# Packages known to pull in torch/CUDA — skip these
SKIP_PKGS = {
    'accelerate', 'chromadb', 'einops', 'faster-whisper',
    'langchain', 'langchain-classic', 'langchain-community',
    'langchain-text-splitters', 'sentence-transformers',
    'sentencepiece', 'transformers', 'onnxruntime',
    'rapidocr-onnxruntime', 'rank-bm25', 'opencv-python-headless',
    'pytube', 'pypandoc', 'soundfile', 'pydub', 'nltk', 'ctranslate2',
}
SKIP_PREFIXES = {'nvidia-', 'cuda-', 'triton'}

filtered = []
for dep in deps:
    pkg = dep.split('==')[0].split('>=')[0].split('[')[0].strip()
    if pkg in SKIP_PKGS or any(pkg.startswith(p) for p in SKIP_PREFIXES):
        continue
    filtered.append(dep)

with open('/tmp/openwebui_deps.txt', 'w') as f:
    f.write('\n'.join(filtered))
PYEOF

pip install -r /tmp/openwebui_deps.txt
```

### 4. Install the Remaining Deps That Open WebUI Imports Eagerly

Open WebUI imports most of its modules at startup, so even optional features
must be installed. After the filtered install above, the following additional
packages are needed for a clean import:

```bash
pip install chromadb==1.5.2 pydub==0.25.1 soundfile==0.13.1
pip install langchain-community==0.4.1 langchain==1.2.10 \
            langchain-classic==1.0.1 langchain-text-splitters==1.1.1 \
            onnxruntime==1.24.3
```

This is still far smaller than the full install (no torch, no CUDA, no
transformers, no sentence-transformers).

### 5. Create Data Directory

```bash
mkdir -p ~/.local/share/open-webui/data
```

### 6. Create Launcher Script

Save as `~/.local/bin/start-open-webui-hermes.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

export DATA_DIR="$HOME/.local/share/open-webui/data"
export WEBUI_NAME="Hermes Agent WebUI"
export ENABLE_SIGNUP=true
export ENABLE_PUBLIC_ACTIVE_USERS_COUNT=False
export ENABLE_VERSION_UPDATE_CHECK=False
export OPENAI_API_BASE_URL="http://127.0.0.1:8642/v1"
export OPENAI_API_KEY="$(python3 -c "from pathlib import Path; import re; \
    p=Path.home()/'.hermes'/'.env'; \
    print(re.search(r'API_SERVER_KEY=(.+)', p.read_text()).group(1))")"
export ENABLE_OPENAI_API=True
export ENABLE_OLLAMA_API=False
export OFFLINE_MODE=True
export BYPASS_EMBEDDING_AND_RETRIEVAL=True
export RAG_EMBEDDING_MODEL_AUTO_UPDATE=False
export RAG_RERANKING_MODEL_AUTO_UPDATE=False
export SCARF_NO_ANALYTICS=true
export DO_NOT_TRACK=true
export ANONYMIZED_TELEMETRY=false
export HOST="127.0.0.1"
export PORT="${OPEN_WEBUI_PORT:-8080}"

mkdir -p "$DATA_DIR"
source "$HOME/.local/open-webui-venv/bin/activate"
exec open-webui serve
```

### 7. Start It

```bash
# Background (survives until WSL restart):
bash ~/.local/bin/start-open-webui-hermes.sh

# Verify:
curl -so /dev/null -w "%{http_code}" http://127.0.0.1:8080
```

## First-Time Setup

Open `http://127.0.0.1:8080` in your browser. The first account you create
becomes admin. The Hermes Agent connection should auto-configure via the
environment variables in the launcher. If not:
- Admin Settings → Connections → Add Connection
- URL: `http://host.docker.internal:8642/v1` (if Open WebUI runs in Docker)
- URL: `http://127.0.0.1:8642/v1` (if running natively as above)
- API Key: the `API_SERVER_KEY` from `~/.hermes/.env`

## Pitfalls

### `DATA_DIR` does not exist
> peewee.OperationalError: unable to open database file

Open WebUI creates its SQLite database in `$DATA_DIR`. If this directory
doesn't exist, it errors. Create it before starting.

### ModuleNotFoundError cascade
Open WebUI eagerly imports all modules at startup. Several "optional"
packages (chromadb, langchain-community, pydub, onnxruntime) are imported
at module level — they are effectively required even if you don't use the
feature. The dep list above covers the full import chain.

### Version pinning
Open WebUI 0.9.5 uses exact version pins for all deps (`==1.13.0` not
`>=1.13.0`). Do not use relaxed versions unless you verify compatibility.

### Gateway dies on terminal close
The Hermes gateway background process does not survive WSL restart. Start
it fresh each time, or set up a systemd user service.

## Verification

```bash
# Hermes API health
curl http://127.0.0.1:8642/health
# → {"status": "ok", ...}

# Model discovery
curl -H "Authorization: Bearer $API_SERVER_KEY" http://127.0.0.1:8642/v1/models
# → {"object": "list", "data": [{"id": "Hermes Agent", ...}]}

# Open WebUI serving
curl -so /dev/null -w "%{http_code}" http://127.0.0.1:8080
# → 200
```

## Comparison

| Approach | Disk Usage | ML Features | Notes |
|----------|-----------|-------------|-------|
| Full `pip install` | ~3-4 GB | Full RAG/STT/local models | Includes PyTorch, CUDA toolkits |
| Lean (this doc) | ~800 MB | Chat frontend only | No torch, no CUDA, no transformers |
| Docker | ~1 GB image + volume | Full | Uses host.docker.internal |
