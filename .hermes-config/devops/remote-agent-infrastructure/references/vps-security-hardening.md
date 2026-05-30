# VPS Security Hardening

Layered defense model for a Hermes agent VPS. Each layer builds on the one below — skipping layers creates hidden gaps.

## Threat Model

| Threat | Surface | Layer blocked |
|--------|---------|---------------|
| SSH brute force / scanner bots | Port 22 on public IP | Network |
| Exploited skill/plugin | Agent's code execution context | OS (non-root user) |
| Config file leak (API keys) | `~/.hermes/config.yaml` readability | Application (file perms + vault) |
| Supply chain (malicious npm/PyPI dep) | Package install in agent runtime | OS + Application |
| Platform token compromise | Telegram/Discord tokens in config | Application (vault + rotation) |
| Direct origin IP discovery (if public HTTP) | DNS resolution reveals VPS IP | Network (Cloudflare proxy) |

## Layer 1 — Network

### Discovery: what's listening

```bash
ss -tlnp                # TCP listening services
ss -ulnp                # UDP
```

### Firewall — UFW (recommended)

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow from 100.64.0.0/10 to any port 22 proto tcp   # SSH from Tailscale only
ufw enable
```

If public HTTP behind Cloudflare:
```bash
curl -s https://www.cloudflare.com/ips-v4 | xargs -I{} ufw allow from {} to any port 80,443 proto tcp
curl -s https://www.cloudflare.com/ips-v6 | xargs -I{} ufw allow from {} to any port 80,443 proto tcp
```

### Firewall — iptables (minimal)

```bash
iptables -P INPUT DROP
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -i tailscale0 -j ACCEPT
iptables -A INPUT -p udp --dport 41641 -j ACCEPT            # Tailscale DERP
iptables -A INPUT -s 100.64.0.0/10 -p tcp --dport 22 -j ACCEPT
```

### SSH hardening

```bash
# /etc/ssh/sshd_config — explicitly set:
ListenAddress <tailscale-ip>
PasswordAuthentication no
PermitRootLogin prohibit-password
PubkeyAuthentication yes
MaxAuthTries 3
```

Verify: `sshd -t && systemctl reload sshd`

### Service audit — disable what's not needed

```bash
systemctl disable --now cups.service cups-browsed.service avahi-daemon.service bluetooth.service postfix.service 2>/dev/null
```

### Auto-updates

```bash
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

## Layer 2 — OS / System

### Non-root Hermes user

Running as root means any exploited package or skill owns the machine.

```bash
adduser --disabled-password hermes
cp -r /root/.hermes /home/hermes/
chown -R hermes:hermes /home/hermes/.hermes
```

Migrate systemd services to `--user --machine=hermes@`.

### File permissions

```bash
chmod 600 ~/.hermes/config.yaml
chmod 700 ~/.hermes
chmod 600 ~/.ssh/authorized_keys
```

### Kernel hardening

```bash
sysctl -w vm.swappiness=10
sysctl -w net.ipv4.conf.all.rp_filter=1
sysctl -w net.ipv4.tcp_syncookies=1
```

Persist in `/etc/sysctl.conf`.

### Fail2ban

```bash
apt install fail2ban
```

## Layer 3 — Application (Hermes-specific)

### Zero port principle

Evaluate each service:
- **Gateway** — outbound-only by default (polling). Needs no open ports.
- **Web UI / Dashboard** — Tailscale IP + internal port only.
- **File server** — Tailscale-bound, not public.
- **Webhook receivers** — use Cloudflare Tunnel (outbound) instead of opening ports.

### Secrets

```bash
chmod 600 ~/.hermes/config.yaml
```

Beyond 600: use Bitwarden Secrets Manager (see `references/bitwarden-secrets-manager.md`).

### Skill audit

Every skill is arbitrary code. Review installed skills:
```bash
hermes skills list
grep -r "web_search\|terminal\|memory\|read_file" ~/.hermes/skills/*/SKILL.md
```

### Token hygiene

- Telegram bot token: rotate every 30-90 days
- Discord bot token: every 30-90 days
- LLM provider keys: every 90 days (cost-bearing)
- Hermes API server key: on breach suspicion

## Layer 4 — Supply Chain & Resilience

### Dependency audit

```bash
cd /usr/local/lib/hermes-agent
venv/bin/pip audit 2>/dev/null || true
```

### Minimal backup set

```
~/.hermes/config.yaml        # Core config (secrets redacted)
~/.hermes/mnemosyne/         # Memory DB
~/.hermes/skills/            # Custom skills
~/.hermes/cron/jobs.json     # Cron definitions
```

Do NOT back up: `.env`, `node_modules/`, `venv/`, `sessions.db`.

### Config versioning

Track in a private git repo with secrets redacted.

## Verification Checklist

- [ ] `ss -tlnp` — only expected services listening
- [ ] `ufw status verbose` — default deny, expected allows only
- [ ] `ssh root@<public-ip>` — connection refused (if SSH restricted to Tailscale)
- [ ] `ssh root@<tailscale-ip>` — connects successfully
- [ ] `sudo -u hermes hermes --version` — non-root agent runs
- [ ] `ls -la ~/.hermes/config.yaml` — mode 600
- [ ] `systemctl status unattended-upgrades` — active
- [ ] `df -h /` — ≥ 20% free, swap configured
- [ ] `fail2ban-client status sshd` — banned IPs count (if previously exposed)
