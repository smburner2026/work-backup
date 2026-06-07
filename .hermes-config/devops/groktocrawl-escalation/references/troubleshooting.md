# Troubleshooting — GroktoCrawl Escalation

## Common failures

### `sources` parameter must be a list, not a string

The `/v2/search` endpoint expects `sources` as a list:
```python
# WRONG — returns 422 Unprocessable Content
gc.search("query", sources="web")

# CORRECT
gc.search("query", sources=["web"])
# or just omit it — defaults to ["web"]
gc.search("query")
```

The `groktocrawl_client.py` `search()` method defaults to `sources=["web"]` (fixed in v0.6.0-patch). If you see `HTTPError: 422` with `"Input should be a valid list"`, update the client or pass a list explicitly.

### `Connection refused` on every call

The Docker stack isn't running. Start it:

```bash
groktocrawl start
# or
groktocrawl minimal   # smaller footprint
```

Verify with `groktocrawl status` — if containers are listed but health fails, wait 10s and retry (image warmup).

**Note:** On 2GB VPS, the `groktocrawl` wrapper auto-starts Docker daemon with `start` and auto-stops it with `stop` when no containers are running. This saves ~100MB RAM when idle. If you need Docker for other things, start it manually: `systemctl start docker`.

### Stack starts but health never returns 200

Usually means one of the service dependencies is unhealthy. Check:

```bash
docker compose -f ~/groktocrawl/docker-compose.yml ps
docker compose -f ~/groktocrawl/docker-compose.yml logs agent-svc
docker compose -f ~/groktocrawl/docker-compose.yml logs scraper-svc
```

Common causes:
- **Valkey unhealthy** → `docker compose restart valkey`
- **SearXNG config error** → check `searxng/settings.yml` for YAML syntax
- **LLM provider key missing** → re-edit `~/groktocrawl/.env`, then `docker compose up -d --force-recreate agent-svc`

### `Out of memory` errors

The full stack needs ~750MB. If you don't have that headroom:

```bash
groktocrawl stop
free -h
# If free < 1GB, use the minimal profile:
groktocrawl minimal
```

You can also disable individual services via `docker compose up -d` with explicit service names:

```bash
# Bare minimum: just search + scrape, no browser, no parse
cd ~/groktocrawl && docker compose up -d valkey searxng scraper-svc agent-svc
```

### `.env` changes not picked up after `docker compose restart`

**Problem:** Editing `~/groktocrawl/.env` and running `docker compose restart` does NOT apply the changes. Docker compose caches environment variables at container creation time.

**Fix:** Use `--force-recreate` instead of `restart`:

```bash
cd ~/groktocrawl
docker compose up -d --force-recreate agent-svc
```

Verify the new env inside the container:
```bash
docker compose exec agent-svc env | grep LLM_
```

**Common scenario:** Changing `LLM_MODEL` or `LLM_API_KEY` in `.env` to switch LLM providers. The container keeps using the old values until recreated.

### LLM configuration for `/v2/answer`

The `/v2/answer` endpoint requires a real LLM (not `fixture-model`). Configure in `~/groktocrawl/.env`:

```bash
# OpenRouter free models (no API cost)
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
LLM_API_KEY=sk-or-v1-...  # from ~/.hermes/.env OPENROUTER_API_KEY
```

Other working free models on OpenRouter: `poolside/laguna-xs.2:free`, `poolside/laguna-m.1:free`.

After changing, recreate: `docker compose up -d --force-recreate agent-svc`.

**Note:** `meta-llama/llama-4-maverick:free` returns 404 on OpenRouter (model not available). Use `nvidia/nemotron-3-ultra-550b-a55b:free` or check `curl https://openrouter.ai/api/v1/models | jq '.data[] | select(.id | endswith(":free"))' | jq .id` for current free models.

### "Barrier detected" on every request

Either the target site genuinely has Cloudflare/CAPTCHA, or the scraper is misclassifying. Check the `barrier.detail` field for which signals matched.

If misclassification (e.g. a benign page that mentions "rate limit" in a sentence):

- Edit `scraper-svc/scraper/fetch.py` to add the site to the allowlist
- Or pass the URL through Tier 3 directly: `gc.scrape_with_browser(url)`

### Loop detector triggers after 2-3 escalations

The model is escalating without progress. This is **the correct behavior** — the loop detector surfaces the failure chain to the user instead of silently retrying.

Read `result.full_failure_chain` and either:
- Try a different query (different angle, different archive)
- Accept the information isn't reachable and report back
- Manually investigate the barrier with a browser

### Escalation reaches Level 4 with no answer

Level 4 (autonomous agent) is the last resort. The agent runs its own internal search/scrape loop and may still fail. When this happens:

1. The full failure chain is in `result.escalation_trace` — show it to the user
2. The agent's own `attempted_chain` is in the response data — useful for debugging
3. The query may genuinely not have an online source. Accept the dead end.

## Performance

### Cold start: 5-10s

First `groktocrawl start` after `docker compose down` is slow (image cache miss). Subsequent starts within an hour are ~2s.

If you find yourself starting/stopping frequently, consider leaving the **minimal** profile running continuously (~315MB).

### Browser tier: 300MB RAM, 1-3s per page

Playwright is heavy. Only used when Level 2 detects a barrier or you explicitly call `gc.scrape_with_browser()`.

To skip it entirely (saves 300MB):
```bash
groktocrawl minimal
```

### SearXNG first request: 3-5s

SearXNG initializes the meta-search backend on first query. Subsequent queries are ~500ms.

## Maintenance

### Update GroktoCrawl

```bash
cd ~/groktocrawl

# If shallow clone (check with: cat .git/shallow):
git fetch --unshallow origin
git fetch origin main
git reset --hard FETCH_HEAD

# If full clone:
git pull origin main

# Rebuild and restart (env var changes require --force-recreate)
docker compose build --no-cache
docker compose up -d --force-recreate agent-svc
```

**Important:** `docker compose restart` does NOT pick up `.env` changes. Always use `--force-recreate` after editing `.env`.

### View all logs

```bash
cd ~/groktocrawl
docker compose logs --tail=100
```

### Reset Valkey cache

```bash
docker compose exec valkey valkey-cli FLUSHALL
```

### Wipe everything and start over

```bash
cd ~/groktocrawl
docker compose down -v   # -v removes volumes
docker compose up -d
```

## When to give up

The escalation tree is bounded at 4 levels. Beyond that, no amount of automation will help. Surface to the user:

- "Tried 4 escalation levels (search → scrape → browser → agent). All returned no useful content. The information may not be publicly available online, or the source site may be currently blocking automated access."
- List the failure trace
- Suggest: "Try a different query angle, or check the source manually in a browser."
