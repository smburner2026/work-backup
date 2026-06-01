# VPS Work Directory Audit

When cleaning up the VPS work directory (`/root/work/`), use this methodology to identify what's reclaimable and what's actively needed.

## Trigger

- User says "clean up the work directory" or "what's using space in my workspace"
- VPS disk is running low (check `df -h /`)
- Routine maintenance — comparing VPS vs WSL to find duplicate data

## Quick Audit Commands

```bash
# Step 1 — Get the lay of the land
du -sh /root/work/*/ | sort -rh
du -sh /root/work/
df -h /

# Step 2 — Deep dive into biggest dirs
for dir in /root/work/*/; do
  name=$(basename "$dir")
  size=$(du -sh "$dir" | cut -f1)
  echo "=== $name ($size) ==="
  du -sh "$dir"/*/ 2>/dev/null | sort -rh | head -10
done

# Step 3 — Cross-reference with WSL (if dual-instance)
ssh local-machine "du -sh /home/vthen/work/*/ | sort -rh"
```

## What to Look For

### Heavy items on VPS (>50M)

| Type | Typical size | Reclaimable? |
|------|-------------|-------------|
| PDF source files (VSTB volumes) | 30-55 MB each | Yes — if WSL also has them and OCR runs on WSL |
| Textbook PDFs (DABT) | 10-50 MB each | Usually keep — actively referenced |
| Market data CSVs (trading) | 10-100 MB | Low value — regeneratable |
| Extracted references (DABT) | 40-50 MB | Keep — actively used |
| Research PDFs (Chack, etc.) | 45-90 MB | Depends — ask user |
| Temp/intermediate files | Variable | Yes — remove after session |

### Common cleanup candidates

| Item | Typical savings | Risk |
|------|---------------|------|
| VSTB source PDFs (if on WSL too) | ~290 MB | None — OCR runs on WSL |
| Trading market data | ~100 MB | Low — regeneratable |
| Old rotated logs (agent.log.1/2/3) | ~13 MB | None |
| Stale kanban workspaces | ~1 MB | None |

### Quick triple-check before deleting PDFs from VPS

```bash
# 1. Confirm WSL has them
ssh local-machine "ls -lh /home/vthen/work/<project>/sources/*.pdf" 2>/dev/null

# 2. Confirm OCR output also exists on WSL (not just VPS)
ssh local-machine "ls -lh /home/vthen/work/<project>/sources/*.txt" 2>/dev/null

# 3. Check if VPS even needs them (is OCR configured to run on WSL?)
grep -l "local-machine\|WSL" /root/work/vstb-ocr-workflow/SKILL.md 2>/dev/null || \
  grep -r "local" /root/work/*/sources/vstb/ 2>/dev/null | head -3
```

## VPS → WSL Remote Hermes Wrapper

If you need to dispatch Hermes commands from the VPS to the WSL machine:

```bash
# Create a local wrapper
cat > /usr/local/bin/hermes-local << 'WRAPPER'
#!/bin/bash
ssh local-machine "/home/vthen/.local/bin/hermes $*"
WRAPPER
chmod +x /usr/local/bin/hermes-local

# Uses the SSH host alias from ~/.ssh/config:
Host local-machine
    HostName 100.110.237.89
    User vthen
    IdentityFile ~/.ssh/id_ed25519_vps2local
    StrictHostKeyChecking accept-new
```

Then run Heres on WSL as if it were local:

```bash
hermes-local --version
hermes-local chat -q "process these OCR files"
hermes-local skills list
```

## Pitfalls

- **Don't delete PDFs from VPS if they're the only copy** — always check WSL first
- **Don't delete DABT reference PDFs** — actively used for exam prep
- **Check timestamps** — if VPS file is newer than WSL, it may not have been synced back yet. Push first.
- **Temp files in `/tmp/`** — separate from `/root/work/`; check independently
- **Kanban workspaces** can be cleaned via `hms cleanup` or `hermes kanban gc` — don't `rm -rf` manually
