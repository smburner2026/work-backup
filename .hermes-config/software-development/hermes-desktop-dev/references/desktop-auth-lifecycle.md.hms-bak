# Desktop App Auth Lifecycle

## Source locations
- Auth mode classification: `apps/desktop/electron/connection-config.cjs`
- Token handling + WS connect: `apps/desktop/electron/main.cjs` (lines ~3144–3800)
- Gateway token generation: `hermes_cli/web_server.py` (line 135)
- Gateway OAuth cookie flow: `hermes_cli/dashboard_auth/cookies.py`

## Token mode (legacy)

Gateway generates session token at startup:
```python
# hermes_cli/web_server.py:135
_SESSION_TOKEN=os.environ.get("HERMES_DASHBOARD_SESSION_TOKEN") or secrets.token_urlsafe(32)
```

Desktop injects it via env var when spawning the gateway process:
```javascript
// main.cjs:3797
HERMES_DASHBOARD_SESSION_TOKEN: token,
```

REST requests use header:
```
X-Hermes-Session-Token: <token>
```
Or legacy Bearer fallback:
```
Authorization: Bearer <token>
```
WS connections use query param:
```
ws://host/api/ws?token=<token>
```

**The token is NOT persisted by the gateway.** It exists only in the running process memory. Any gateway restart (update, crash, `hermes gateway restart`, SSH logout without linger) regenerates it.

## OAuth mode

When `GET /api/status` returns `auth_required: true`:
1. Desktop authenticates via browser OAuth flow → sets HttpOnly cookie
2. REST requests use the cookie automatically
3. WS upgrades require a single-use ticket:
   ```
   POST /api/auth/ws-ticket  (with session cookie)
   → returns { ticket: "..." }
   ws://host/api/ws?ticket=<ticket>
   ```
4. Ticket is single-use and short-lived

Cookie variants (checked in order):
- `__Host-hermes_session_at` (HTTPS direct)
- `__Secure-hermes_session_at` (behind path prefix)
- `hermes_session_at` (loopback HTTP)

## Common failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Desktop shows "connection refused" after update | Gateway restarted, token changed | Reconnect from desktop settings |
| 401 on all API calls | Token mismatch (desktop has old, gateway has new) | `hermes gateway restart` + re-enter URL in desktop |
| WS connects then immediately disconnects | OAuth ticket expired or already used | Desktop should auto-mint new ticket on reconnect |
| Desktop works locally but not over Tailscale | CORS blocking non-localhost origin | Gateway CORS is locked to localhost/127.0.0.1 — need to use localhost hostname or adjust CORS |
| Token works for REST but WS fails | WS uses `?token=` not header; URL encoding issue | Check token doesn't contain characters needing encode |

## Key invariants
- Token mode: token is ephemeral, process-scoped, not serialized to disk
- OAuth mode: cookie persists across restarts but ticket is per-WS-upgrade
- Desktop always probes `GET /api/status` first to determine mode
- Auth check uses `hmac.compare_digest` (constant-time) — no timing side-channel
