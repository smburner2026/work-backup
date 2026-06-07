# Nous Portal OAuth Flow — Verified Reference

Use this when the user wants to switch the desktop app from basic auth (username/password) to OAuth (Nous Portal) — typically because they said "my login is via github" or asked to remove the username/password step.

## Mental model

The desktop app never talks to GitHub directly. The flow is:

```
Desktop App  →  Nous Portal  →  GitHub OAuth  →  Portal  →  Desktop App
              (identity hub)   (one of several Portal-supported IdPs)
```

The Portal supports GitHub, Google, and email-based accounts. GitHub is one of several sign-in options on the Portal sign-in page itself, not a separate identity provider for the dashboard.

## What the user sees vs what's actually happening

| User says | Actual meaning |
|---|---|
| "My login is via github" | Their Nous Portal account was created via GitHub OAuth |
| "Sign in with Nous Research" | The desktop app is calling the Portal's OAuth endpoint |
| "Sign in with GitHub" (inside the browser popup) | The Portal is calling GitHub as one of its supported IdPs |
| "I want OAuth" | They want the Portal-mediated flow, not username/password |

**Do not** interpret "my login is via github" as "wire GitHub directly as the OIDC provider." GitHub is not a standard OIDC provider and the dashboard's `auth_providers` list does not include a "github" entry — only "basic" and "oauth" (Portal).

## Step 1: `hermes setup --portal`

This is the login. It is **interactive** and **needs a TTY** (it opens a browser for OAuth). Cannot be scripted headlessly from a non-interactive shell.

### Pitfall: PTY mode does not satisfy the TTY check

Even with `pty=true` in the agent's terminal tool, `hermes setup --portal` detects "no TTY" and bails with:

```
⚕ Hermes Setup — Non-interactive mode
  Running in a non-interactive environment (no TTY detected).
  ...
```

Run this from the **user's own terminal** (SSH session, local shell on the desktop, or any interactive bash). Not from the agent's session.

### What the user does

1. Run `hermes setup --portal` in their terminal
2. CLI prints a URL and a short code (e.g. `https://portal.nousresearch.com/device?code=ABCD-1234`)
3. Open the URL in any browser (laptop, phone)
4. Click "Sign in with GitHub" (or whatever IdP the Portal account uses)
5. Enter the code when prompted
6. Browser says "success" → CLI says "logged in" → token saved to `~/.hermes/`

This takes <60s once the user starts the browser step.

### Verification

```bash
hermes auth status nous
# Expected: custom:nous: logged in (with the account email/handle)
```

**Caveat:** `auth status` may still show "logged out" even when a token was saved — the check uses a different state than what `dashboard register` validates. The reliable verification is `dashboard register` itself.

## Step 2: `hermes dashboard register`

```bash
hermes dashboard register --name "Hermes VPS"
# Optional flags:
#   --redirect-uri <url>   Public HTTPS OAuth redirect (omit for Tailscale-only)
#   --portal-url <url>     Override Portal base URL (testing/staging)
```

This writes `HERMES_DASHBOARD_OAUTH_CLIENT_ID` into `~/.hermes/.env` and creates the OAuth client on the Portal side.

### The two distinct errors

| Error | Cause | Fix |
|---|---|---|
| `You're not logged into Nous Portal. Run `hermes setup` (or `hermes auth login nous`) first, then retry.` | No Portal token, or token not loaded. **Note:** the error message references `hermes auth login nous` which is **not** a real subcommand. Use `hermes setup --portal`. | Run `hermes setup --portal` from an interactive terminal. |
| `Registration failed: Self-hosted dashboard registration is not available for this account.` | Portal account lacks the self-hosted dashboard feature. Login succeeded, feature is gated. | Check https://portal.nousresearch.com account settings for a "Self-hosted dashboards" / "Local dashboards" toggle or enrollment. If absent, basic auth is the only path — this is a Nous-side decision. |

**Critical:** error B is not a setup problem. It will not fix itself by re-running login. It is an account-tier / waitlist gate on the Portal side.

## Step 3: Restart and verify

```bash
systemctl --user restart hermes-dashboard

curl -s http://<tailscale-ip>:9119/api/status | python3 -m json.tool | grep -A 5 auth
# Expected:
#   "auth_required": true,
#   "auth_providers": ["basic", "oauth"]
```

Both providers coexist. To drop basic auth (cleaner for public-internet deployments), remove the three `HERMES_DASHBOARD_BASIC_AUTH_*` env vars from `~/.hermes/.env` and restart.

## Step 4: Desktop app reconnect

In the desktop app: **Settings → Gateway → Remote gateway → Save and reconnect**.

The sign-in popup will switch from the username/password form to:

> **Sign in with Nous Research**

Click → browser opens Portal → click "Sign in with GitHub" (or the user's IdP) → consent (first time only) → redirect back to the app authenticated.

Sessions persist across desktop app restarts via the OAuth refresh token. No popup on subsequent boots unless the session expires (months of inactivity or manual sign-out).

## Popup diagnostic — basic vs OAuth at a glance

| Popup heading | Footer text | Provider |
|---|---|---|
| `SIGN IN — Hermes Agent` / `SIGN IN WITH USERNAME & PASSWORD` | `PUBLIC BIND · AUTH REQUIRED` | **basic** (username/password) |
| `Sign in with Nous Research` (button text) | n/a — opens browser | **oauth** (Portal) |

If the user expected OAuth but the popup shows the username/password form, the `oauth` provider is missing from `auth_providers` in `/api/status`. Most common cause: `dashboard register` didn't run, didn't write `HERMES_DASHBOARD_OAUTH_CLIENT_ID`, or the dashboard hasn't been restarted since the env var was added.

## Session-token leftover from `--insecure` days

`HERMES_DASHBOARD_SESSION_TOKEN=***` in `~/.hermes/.env` is from the old `--insecure` setup. With basic auth or OAuth active, this token is unused. Safe to delete the line:

```bash
sed -i '/^HERMES_DASHBOARD_SESSION_TOKEN=/d' ~/.hermes/.env
```

The `~/.hermes/dashboard-session-token` file (binary, ~65 bytes) is the runtime cache of the same token. Also safe to remove; the dashboard will recreate or ignore it depending on whether basic auth is still configured.

## Verified migration transcript (June 2026)

Starting state: dashboard running with `--insecure --host 0.0.0.0`. No auth. Port exposed to public internet.

1. Added `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` / `_PASSWORD` / `_SECRET` to `~/.hermes/.env` (mode 0600).
2. Rewrote `/root/.config/systemd/user/hermes-dashboard.service` to remove `--insecure`, bind to `--host 100.113.2.25` (Tailscale IP), add `EnvironmentFile=%h/.hermes/.env`.
3. `systemctl --user daemon-reload && systemctl --user restart hermes-dashboard`.
4. Verified `/api/status` returns `auth_required: true, auth_providers: ["basic"]`.
5. User opened Hermes Desktop on Windows (with Tailscale running), entered `http://100.113.2.25:9119` as Remote URL, clicked Sign in → username/password popup appeared.
6. User wanted OAuth instead: ran `hermes setup --portal` from their VPS terminal (TTY required), signed in with GitHub via Portal.
7. `hermes dashboard register --name "Hermes VPS"` returned: `Registration failed: Self-hosted dashboard registration is not available for this account.`
8. Decision: keep basic auth (works, fully secure, Tailscale-only). Cleanup: removed `HERMES_DASHBOARD_SESSION_TOKEN` line from `.env`.

Net result: dashboard bound to Tailscale IP only, basic auth required, sessions persist across restarts, no `--insecure`, port no longer exposed to public internet. The OAuth path is documented and ready to switch to if/when the Portal account gets the feature.
