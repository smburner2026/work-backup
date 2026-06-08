# Gateway Service Audit

Use this when checking which gateway instance is running, failing, or restarting on a host with multiple Hermes profiles.

## Quick topology
- Default profile gateway: `hermes-gateway.service`
- Named profile gateway: `hermes-gateway-<profile>.service`
- Both run under `systemd --user`
- Multiple gateways are normal because each profile is isolated
- Do not merge config/platform wiring across profiles

## Commands
```bash
systemctl --user list-units 'hermes-gateway*' --all
journalctl --user -u hermes-gateway*.service -n 80 --no-pager
hermes gateway status
```

## Token / auth failure pattern
- Symptoms: `InvalidToken`, `Unauthorized`, `LoginFailure`
- Common root cause: expired, revoked, or manually rotated platform token
- Platform can crash the gateway by treating bad token as startup failure, not fallthrough
- Don’t keep a broken platform in `~/.hermes/config.yaml` or profile config — either fix the token or remove the platform block
- Detect with grep for the token error string across all services and configs

## Decision tree
1. Identify failing service from `list-units`
2. Check platform token in the profile `.env` and config platform block
3. Choose:
   - Fix: replace token, restart both relevant services
   - Remove: delete platform key from `~/.hermes/config.yaml` and each affected profile config, remove `telegram:`, `discord:`, etc. blocks where the platform is not wanted
4. Verify by restarting affected services and `hermes gateway status`
