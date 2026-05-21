# VPS Provider Selection Notes (May 2026 session)

Observed user behavior:
- Strongly price-sensitive. Rejects $24/mo plans immediately ("way too much").
- Prefers ~$4–10/mo range for initial Hermes gateway + cron setup.
- Will switch providers mid-session (Hetzner CX23 → Vultr regular → back to Hetzner) when price exceeds comfort.

Recommended starting plan (budget path):
- Hetzner CX23 (2 vCPU/4 GB) ≈ €3.5–4.5/mo
- Vultr regular Cloud Compute 2 vCPU/4 GB ≈ $8–10/mo

Avoid leading with High Performance / High Frequency tiers unless user asks for speed.

Migration sequence remains identical across providers:
1. SSH key login
2. curl install script
3. rsync ~/.hermes/ and ~/work
4. hermes gateway setup (Telegram)
5. hermes cron + profiles

Reference: current conversation transcript for exact price reactions.