# Substack Paywall Authentication

## Auth mechanism

Substack uses a session cookie called **`connect.sid`** to authenticate users. This is set when you log in at `substack.com` and is shared across all Substack subdomains (*.substack.com).

- **Cookie name**: `connect.sid` (NOT `substack.sid` — the Huryn note on substack.com says `connect.sid`)
- **Domain**: `.substack.com` (shared across all publications)
- **Lifetime**: Stays valid for months as long as you do not explicitly sign out. Even survives MFA sessions.
- **Rotation**: Sign out and sign back in to generate a new cookie. Old cookie is invalidated on sign-out.

## Cookie extraction

From Chrome DevTools:
1. Navigate to any Substack page while logged in
2. F12 → Application → Storage → Cookies → `substack.com`
3. Find row with Name = `connect.sid`
4. Copy the Value field (long alphanumeric string)

From Firefox DevTools:
1. F12 → Storage → Cookies → `substack.com`
2. Same process

## Cookie format for NHagar/substack_api library

The NHagar library expects cookies in a specific JSON file format:

```json
[
  {
    "domain": ".substack.com",
    "name": "connect.sid",
    "value": "YOUR_SESSION_VALUE",
    "path": "/",
    "httpOnly": true,
    "secure": true
  }
]
```

Save as a JSON file (e.g. `~/substack_cookies.json`, mode 600) and pass to:

```python
from substack_api import SubstackAuth
auth = SubstackAuth(cookies_path="~/substack_cookies.json")
```

## Secure usage patterns

**DO NOT:**
- Pass `connect.sid` in shell `curl -H "Cookie: connect.sid=..."` — saved to shell history
- Log the cookie value in output files, debug logs, or error messages
- Share cookies between machines over unencrypted channels

**DO:**
- Use `requests.Session.cookies.set("connect.sid", value)` in Python
- Store the cookie in environment variable `SUBSTACK_COOKIE` and read at runtime
- Save to a JSON file with `chmod 600` restricted permissions
- Only use your own cookies from your own authenticated session

## Known working endpoints (auth'd)

| Endpoint | Method | Purpose |
|---|---|---|
| `https://substack.com/api/v1/reader/profile` | GET | Auth'd user profile + subscriptions |
| `{pub}.substack.com/api/v1/archive?sort=new&offset=N` | GET | Publication archive (with auth, shows paywalled posts too) |
| `{pub}.substack.com/api/v1/posts` | GET | Recent posts from a publication |
| `{pub}.substack.com/p/{slug}` | GET | Individual article page (embed `window._preloads`) |

## References

- [Paweł Huryn's note on Substack's hidden API](https://substack.com/@huryn/note/c-181571328) — the `connect.sid` discovery
- [NHagar/substack_api](https://github.com/NHagar/substack_api) — full Python library with cookie support
- [Jakub Slys — reverse engineering Substack API](https://iam.slys.dev/p/no-official-api-no-problem-how-i) — methodology for discovering endpoints

## Limitations

- **Unofficial API**: No guarantee of stability. Endpoints may change without notice.
- **Rate limiting**: Conservative — max 1 req/sec. Be polite.
- **Cookie expiry**: Only guaranteed invalid on sign-out. May expire silently after months of inactivity.
- **No email/password auth**: The `connect.sid` cookie is the only supported auth mechanism for programmatic access. Some libraries offer email/password login but it's less reliable.
