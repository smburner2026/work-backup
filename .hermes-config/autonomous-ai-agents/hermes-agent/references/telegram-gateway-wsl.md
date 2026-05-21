# Telegram Gateway on WSL — Working Setup Sequence (2026-05-15)

This sequence was verified to produce a working, persistent Telegram bot connected to a local Hermes instance on WSL.

## Prerequisites
- systemd enabled in WSL (`/etc/wsl.conf` with `[boot] systemd=true`)
- User has already run `hermes gateway setup` at least once

## Step-by-Step (Tested Order)

1. **Create bot**
   - Message @BotFather → `/newbot`
   - Copy the resulting token (format: `123456789:AA...`)

2. **Run setup wizard**
   ```bash
   hermes gateway setup
   ```
   - Select Telegram
   - Paste the full bot token
   - When prompted for allowed user ID, enter your Telegram numeric ID (e.g. 1149647881)

3. **Install as persistent service**
   ```bash
   hermes gateway install
   hermes gateway start
   ```

4. **Verify**
   ```bash
   hermes gateway status          # Should show "active (running)"
   tail -30 ~/.hermes/logs/gateway.log
   ```

## Common Failure Modes & Fixes

- **"/mybots shows no current bots"**  
  Token was never persisted. Re-run `hermes gateway setup` and paste the token again.

- **Bot receives messages but gives no reply**  
  Check logs for "No user allowlists configured". Re-run setup and explicitly enter the allowed user ID.

- **Service dies after closing terminal**  
  Linger is required. The `hermes gateway install` step enables it automatically.

## Verification Commands
```bash
hermes gateway status
journalctl --user -u hermes-gateway -n 20 --no-pager
tail -30 ~/.hermes/logs/gateway.log
```

After successful setup, the same Hermes instance (skills, memory, model) is reachable via both terminal and Telegram. Closing the terminal does not stop the bot.