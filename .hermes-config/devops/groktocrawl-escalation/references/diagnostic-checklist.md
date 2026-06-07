# Diagnostic Checklist — GroktoCrawl Stack

Full health check when the user reports failures or asks for diagnostics. Run levels sequentially — stop at first failure.

## Level 0: Python Modules (zero Docker)

```bash
# 1. barrier_classifier
python3 -c "
import sys; sys.path.insert(0, '<skill_dir>/scripts')
from barrier_classifier import classify_barrier
r = classify_barrier(url='https://test.com', html='<html>Just a moment...</html>')
assert r.detected == True and r.confidence >= 0.7, f'FAIL: {r}'
print('barrier_classifier: OK')
"

# 2. quality_gates
python3 -c "
import sys; sys.path.insert(0, '<skill_dir>/scripts')
from quality_gates import assess_quality
r = assess_quality(markdown='Error 404. Page not found.')
assert r.score < 0.5, f'FAIL: {r.score}'
print('quality_gates: OK')
"

# 3. escalate (requires workflow_pattern_kit)
python3 -c "
from workflow_pattern_kit import DAG, LoopDetector, OutputGate, Dedup
import sys; sys.path.insert(0, '<skill_dir>/scripts')
from escalate import escalate
print('escalate: OK')
"
# If this fails with ModuleNotFoundError for workflow_pattern_kit:
#   cd /root/.hermes/skills/devops/workflow-pattern-kit
#   ln -sf python workflow_pattern_kit
#   SITE_PACKAGES=$(python3 -c 'import site; print(site.getsitepackages()[0])')
#   echo '/root/.hermes/skills/devops/workflow-pattern-kit' > $SITE_PACKAGES/workflow_pattern_kit.pth
```

## Level 0.5: Hermes Native Tools

```bash
# web_search — should return ≥1 result
# web_extract — should return content > 200 chars
# web_search_plus — should route to a provider (Tavily, etc.)
```
Verify by running each against a known-good URL (e.g., https://example.com).

## Level 1-2: Docker Stack

```bash
# Docker installed?
docker --version
# If not: curl -fsSL https://get.docker.com | sh && systemctl start docker && systemctl enable docker

# Docker daemon running?
systemctl is-active docker
# If not: systemctl start docker
# The groktocrawl wrapper auto-starts/stops Docker daemon on demand

# Stack directory exists?
ls ~/groktocrawl/docker-compose.yml
# If not: git clone --branch v0.6.0 --depth 1 https://github.com/groktopus/groktocrawl.git ~/groktocrawl

# Deploy minimal stack (valkey + searxng + scraper + agent, ~270MB):
cd ~/groktocrawl
cp .env.sample .env  # edit as needed
docker compose up -d valkey searxng scraper-svc agent-svc

# Health endpoint?
curl -fsS --max-time 5 http://localhost:8080/health

# Container status?
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Memory usage?
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}"
```

### On-demand lifecycle
- `groktocrawl start` — auto-starts Docker daemon + brings full stack up (~400MB)
- `groktocrawl minimal` — search + scrape only (~330MB)
- `groktocrawl stop` — tears down containers + stops Docker daemon (frees ~400MB)
- Stack should be stopped when not in use on small VPS (2GB)

### VPS RAM optimization (2GB plan)
If running out of RAM, check for unnecessary services:
- `multipathd` — device-mapper multipath, useless on VPS → `systemctl disable multipathd`
- `snapd` — only needed if using snap packages (e.g., Bitwarden) → `systemctl disable snapd` to stop daemon
- Docker daemon itself uses ~100MB — auto-stopped by `groktocrawl stop` when no containers running
- Journald: limit with `SystemMaxUse=50M` in `/etc/systemd/journald.conf.d/vacuum.conf`

## Module API Gotchas

- `classify_barrier(url, html="", content="", title="")` — first arg is `url`, not content. Passing text as first arg sets `url=text` and both `html`/`content` stay empty → always returns `detected=False`.
- `QualityReport` has `score`, `checks`, `detail` — no `passed` attribute. Use `report.score >= 0.5` for pass/fail.
- `GroktoCrawl` (not `GroktoCrawlClient`) — class name in `groktocrawl_client.py`.
