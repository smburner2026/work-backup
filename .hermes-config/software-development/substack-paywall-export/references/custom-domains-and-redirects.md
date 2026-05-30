# Custom Domains and Auth Redirects

Substack publications can use custom domains (e.g. `www.bronzeagepervert.yoga`) instead of the standard `{pub}.substack.com` format. This introduces several gotchas for authenticated access.

## Discovery Pattern

When a publication uses a custom domain, the flow works via redirect:

```
{bare}.substack.com/api/v1/archive  → 301 redirect  →  www.{custom}.yoga/api/v1/archive  →  200 OK
{bare}.substack.com/p/{slug}         → 301 redirect  →  www.{custom}.yoga/p/{slug}         →  200 OK
```

The substack subdomain (`bronzeagepervert.substack.com`) acts as a gateway — it carries the auth, redirects to the custom domain, and the custom domain returns the content.

### Rule: always use the substack subdomain as the primary entry point

Hit `{pub}.substack.com` first, follow redirects. Never try the custom domain directly — the archive API returns 404 when hit directly on the custom domain:

```
www.bronzeagepervert.yoga/api/v1/archive  →  404 (direct hit without redirect chain)
bronzeagepervert.substack.com/api/v1/archive  →  301 → www.bronzeagepervert.yoga/api/v1/archive  →  200
```

## www vs non-www

Some custom domains require the `www.` prefix:
- `bronzeagepervert.yoga` → 301 redirect to `www.bronzeagepervert.yoga`
- `www.bronzeagepervert.yoga` → works (serves content)

Others may work without `www.`. The safe approach: try both variants when resolving a custom domain.

Algorithm:
```python
def get_domain_variants(pub):
    """Try www and non-www variants of custom domains."""
    variants = []
    if '.' in pub and 'substack.com' not in pub:
        variants.append(f"https://{pub}")
        if pub.startswith("www."):
            variants.append(f"https://{pub[4:]}")
        else:
            variants.append(f"https://www.{pub}")
    return variants
```

## Cookie Stripping on Cross-Domain Redirects

**This is the most common failure mode.** When an HTTP client follows a redirect from `substack.com` to a custom domain, some clients strip the auth cookie:

| Client | Behavior | 
|---|---|
| `urllib.request.urlopen()` | **Strips Cookie header** on cross-domain redirect — returns 404 on custom domain |
| `requests.Session.get()` | **Preserves Cookie** across redirects — works correctly |
| `curl -L` | **Preserves Cookie** (reads from cookie jar) — works correctly |

**Always use `requests.Session` or `curl -L` for authenticated Substack requests.** Never use bare `urllib.request.urlopen()` with cookies when the destination might be a custom domain.

✅ Correct pattern:
```python
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"
session.headers["Cookie"] = "connect.sid=s%3A..."
resp = session.get(f"https://{pub}.substack.com/p/{slug}", allow_redirects=True)
```

❌ Broken pattern (urllib strips cookie on redirect):
```python
req = urllib.request.Request(url, headers={"Cookie": cookie, ...})
resp = urllib.request.urlopen(req)  # 404 if redirected to custom domain
```

## Known Publications Using Custom Domains

| Domain | Type | Notes |
|---|---|---|
| `www.bronzeagepervert.yoga` | Custom domain, requires www | Bronze Age Pervert |
