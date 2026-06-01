# Gateway Conflicts in Multi-Instance Setups

## Symptom

Repeated warnings in `gateway.log`:

```
WARNING gateway.platforms.telegram: [Telegram] Telegram polling conflict (1/5)
  — previous session still held open on Telegram's servers.
  Waiting 20s for it to expire.
  Error: Conflict: terminated by other getUpdates request;
  make sure that only one bot instance is running
```

The log file fills rapidly — can hit 200+ conflicts in a few hours.

## Root Cause

Telegram's Bot API only allows ONE `getUpdates` polling session per bot token
at a time. When two Hermes gateway instances poll with the same bot token,
they fight for the lock — whichever polls second gets kicked, waits 20s,
retries, while the other grabs it in the meantime.

Common scenario: **dual-instance setup** (VPS hub + local WSL) where the
gateway started on both machines because the install process default-enabled it.

## Diagnosis

```bash
grep -c "polling conflict" ~/.hermes/logs/gateway.log
```

If the count is 100+ and the gateway has been running less than a day, you
have a conflict. Also check which processes are polling — look for duplicate
`python -m hermes_cli.main gateway run` processes:

```bash
ps aux | grep gateway | grep -v grep
```

If only one shows on this machine, the other instance is on a different host
(reachable via Tailscale, LAN, or the public internet).

## Resolution

**Option A — Run Telegram only on the primary hub (recommended)**

Stop and disable the gateway on the secondary instance:

```bash
# On the secondary instance (e.g., WSL):
systemctl --user stop hermes-gateway
systemctl --user disable hermes-gateway
```

Then restart the primary gateway to reclaim the Telegram lock:

```bash
# On the primary instance (e.g., VPS hub):
systemctl --user restart hermes-gateway
```

It may take up to 60s for Telegram to release the old session after the
secondary gateway stops. The primary will show "polling resumed after
conflict retry" once it claims the lock cleanly.

**Option B — Different bot tokens per instance**

Create a second bot via [@BotFather](https://t.me/BotFather) and configure
each instance with its own `TELEGRAM_BOT_TOKEN` in `.env`. This lets both
instances run gateways independently — but they'll respond to different bots.

## Prevention

- **Designate one instance as the gateway owner** before setting up
  multi-instance infrastructure. The always-on VPS/hub is the natural choice.
- **Do NOT start the gateway on WSL or other local machines** if the VPS
  already owns it.
- **When setting up a new instance**, skip gateway setup or explicitly
  disable it after install:
  ```bash
  systemctl --user disable hermes-gateway
  ```
- **HMS sync does NOT duplicate gateway state** — the `gateway/` directory
  under `~/.hermes/` is instance-local. But the `.env` file with the bot
  token will be the same if cloned from the hub, so the secondary instance
  can still start its own gateway if enabled.
