# VPS + Hermes First Deployment (Hetzner CX23)

## Trigger
User is deploying Hermes on a fresh VPS (Hetzner CX23 recommended). Covers SSH key setup, first login, install, and initial rsync.

## Recommended Flow
1. Generate key locally (WSL):
   ```bash
   ssh-keygen -t ed25519 -C "hetzner-vps" -f ~/.ssh/id_ed25519 -N ""
   cat ~/.ssh/id_ed25519.pub
   ```
2. During Hetzner server creation, paste the public key.
3. After server shows "Running":
   ```bash
   ssh root@IP
   ```
4. Immediate post-login commands:
   ```bash
   apt update && apt upgrade -y
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   hermes doctor
   ```
5. Fix common first-boot issues:
   - Host key changed: `ssh-keygen -f ~/.ssh/known_hosts -R 'IP'`
   - Missing local key: regenerate and add via dashboard "Reset root password" → manual key add inside server.

## Pitfalls
- Hetzner can take 5-10 min to reach "Running" even after "created".
- If key login fails on first try, always reset root password from dashboard rather than fighting key issues.
- Never run Hermes install before `apt upgrade`.

## Next Steps After Install
- `hermes gateway setup` (Telegram token)
- rsync local `~/.hermes/` to VPS
- `hermes gateway install && hermes gateway start`