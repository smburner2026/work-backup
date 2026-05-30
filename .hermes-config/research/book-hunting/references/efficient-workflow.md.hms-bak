# Efficient Book-Hunting Workflow

## Sequence (optimized from session 2026-05-27)

1. **Extract book info** — If the source is an X/Twitter post, use Lightpanda:
   ```bash
   lightpanda fetch <url> --dump markdown --wait-ms 8000
   ```
   Do NOT waste time with curl or the Hermes browser for X posts — Lightpanda handles them cleanly.

2. **Search libgen.li by ISBN** — Skip all other sources. Go straight to:
   ```
   https://libgen.li/index.php?req=<ISBN>&columns%5B%5D=t...&curtab=e
   ```
   Use the `curtab=e` (editions) tab to find the full book entry.

3. **Download via get.php** — From the edition page, extract the download URL:
   ```bash
   curl -sL "https://libgen.li/ads.php?md5=<MD5>" | grep -oP 'get\.php\?md5=[^"]+'
   curl -sL "https://libgen.li/<get_url>" -o <output.pdf>
   ```

## What NOT to do (wastes turns)

- Do NOT try IPFS gateways (cloudflare-ipfs, pinata.cloud) — unreliable/blocked
- Do NOT try Anna's Archive fast_download (requires JS session, curl gets HTML)
- Do NOT try Internet Archive direct PDF (returns 401 for in-copyright books)
- Do NOT try the Hermes browser for X posts — Lightpanda fetch is faster
- Do NOT load the Lightpanda skill and then not use it — the user will notice
