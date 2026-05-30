# Post-Hard-Sync Recovery Audit

This reference documents the systematic cross-machine audit performed after
a raw/hard rsync between local (WSL) and VPS that may have overwritten config
and environment files without `--update` timestamp guards.

## Situation

After a hard sync (not using `hms push`/`pull`), config files, `.env` files,
and databases may have been overwritten in the wrong direction. The goal is
to verify state integrity and identify what needs fixing.

## Quick checklist (14 steps)

Run these comparisons in order. Stop and investigate if any step flags a problem.

### 1. config.yaml integrity

```bash
# Both sides should have the SAME hash
md5sum ~/.hermes/config.yaml
ssh root@<vps> 'md5sum .hermes/config.yaml'

# If different: diff them
diff ~/.hermes/config.yaml <(ssh root@<vps> 'cat .hermes/config.yaml')
```

**Pass:** Same hash ✓
**Fail:** Configs diverged — someone edited one side. Accept the canonical version.

### 2. .env — active vars check

```bash
# Compare only the non-commented, non-empty variables
diff <(grep -v '^#' ~/.hermes/.env | grep -v '^\s*$' | grep '=' | sort) \
     <(ssh root@<vps> 'grep -v "^#" .hermes/.env | grep -v "^\\s*$" | grep "=" | sort')
```

**Pass:** Machine-specific vars differ as expected (gateway has TELEGRAM/DISCORD,
local has SUDO_PASSWORD/TERMINAL_ENV). Only flag if a machine is MISSING a var
it needs to operate. ✓
**Fail:** Critical secrets missing on the machine that needs them.

### 3. Profile configs

```bash
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  echo "$name: local=$(md5sum "$p/config.yaml" | cut -d' ' -f1)"
  echo "$name: vps=$(ssh root@<vps> "md5sum .hermes/profiles/$name/config.yaml | cut -d' ' -f1")"
done
```

**Pass:** All hashes match ✓
**Fail:** Profile config edited on one side only.

### 4. Profile .env files

```bash
# Check existence
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  echo "$name: local env=$(test -f "$p/.env" && echo 'exists' || echo 'missing')"
  echo "$name: vps env=$(ssh root@<vps> "test -f .hermes/profiles/$name/.env && echo 'exists' || echo 'missing'")"
done
```

**Pass:** Template-only files are fine. Missing .env on a profile that needs
actual secrets should be flagged. ✓

### 5. LCM DB — most critical

```bash
# Compare filesize, mtime, AND message count
echo "LOCAL: $(ls -la ~/.hermes/lcm.db)"
sqlite3 ~/.hermes/lcm.db 'SELECT COUNT(*) || " messages" FROM messages'

echo "VPS: $(ssh root@<vps> 'ls -la .hermes/lcm.db')"
ssh root@<vps> "sqlite3 .hermes/lcm.db 'SELECT COUNT(*) || \" messages\" FROM messages'"
```

**Pass:** VPS has 50-200 more messages (gateway accumulates Discord/Telegram
sessions that local CLI never sees). Same approximate size. ✓
**Fail:** Local has MORE messages than VPS — local sessions may have been
overwritten when the VPS DB replaced the local one. If VPS >> local (e.g. 1000+
difference), check if VPS was ever synced properly.

### 6. Mnemosyne DB

```bash
md5sum ~/.hermes/mnemosyne/data/mnemosyne.db
ssh root@<vps> 'md5sum .hermes/mnemosyne/data/mnemosyne.db'
```

**Pass:** Same hash ✓
**Fail:** Memory state diverged. The more recent mtime's version is probably correct.

### 7. Skills catalog

```bash
echo "LOCAL: $(ls ~/.hermes/skills/*/ 2>/dev/null | wc -l) skills"
echo "VPS: $(ssh root@<vps> 'ls .hermes/skills/*/ 2>/dev/null | wc -l') skills"

# Check which directories differ
diff <(ls ~/.hermes/skills/) <(ssh root@<vps> 'ls .hermes/skills/')
```

**Pass:** Same count + no dir-level diffs ✓
**Fail:** Skills added on one side and not synced.

### 8. Cron jobs

```bash
# Compare job names
python3 -c "import json; j=json.load(open('$HOME/.hermes/cron/jobs.json')); [print(x['name']) for x in j['jobs']]"
ssh root@<vps> "python3 -c 'import json; j=json.load(open(\".hermes/cron/jobs.json\")); [print(x[\"name\"]) for x in j[\"jobs\"]]'"
```

**Pass:** Same job names (run counts may differ). ✓
**Fail:** A job exists on one side that doesn't on the other. VPS is canonical runner.

### 9. Community manifest

```bash
test -f ~/.hermes/community-manifest.json && echo "LOCAL: exists" || echo "LOCAL: missing"
ssh root@<vps> 'test -f .hermes/community-manifest.json && echo "VPS: exists" || echo "VPS: missing"'
```

**Pass:** Exists on both (or neither) ✓
**Fail:** Exists on one side but not the other — copy it over.

### 10. Backup debris

```bash
echo "LOCAL: $(find ~/.hermes ~/work -name '*.hms-bak*' -type f 2>/dev/null | wc -l) .hms-bak files"
ssh root@<vps> "find .hermes work -name '*.hms-bak*' -type f 2>/dev/null | wc -l"
```

**Pass:** Low count (<5) or zero ✓
**Warn:** Many files means aggressive overwrites happened. Check if config backups
match current configs.

### 11. Config backup verification

```bash
# Check if any config.yaml was overwritten with different content
for bak in $(find ~/.hermes -name 'config.yaml.hms-bak' -type f 2>/dev/null); do
  current="${bak%.hms-bak}"
  if diff -q "$bak" "$current" >/dev/null 2>&1; then
    echo "$(basename $(dirname $bak))/config.yaml: backup == current (safe)"
  else
    echo "$(basename $(dirname $bak))/config.yaml: BACKUP != CURRENT (data loss risk)"
    diff "$bak" "$current"
  fi
done
```

**Pass:** All backups match current configs ✓
**Fail:** A backup differs from current — the sync replaced a config with a different version.

### 12. Work directories

```bash
diff <(ls ~/work/ 2>/dev/null) <(ssh root@<vps> 'ls work/ 2>/dev/null')
```

**Pass:** Local may have extra dev-only dirs (redshift-build, etc.) ✓
**Fail:** Missing shared project directories on one side.

### 13. SSH + gateway health

```bash
ssh -o ConnectTimeout=5 root@<vps> 'echo "SSH OK"'
ssh root@<vps> 'systemctl --user is-active hermes-gateway.service'
```

**Pass:** SSH OK, gateway active ✓
**Fail:** Can't SSH (check Tailscale) or gateway down (restart with `systemctl --user start hermes-gateway.service`)

### 14. VPS disk space

```bash
ssh root@<vps> 'df -h / | tail -1'
```

**Pass:** >500MB free ✓
**Warn:** <500MB — next sync may hang. Run `hms cleanup`.
**Fail:** <100MB — sync will be blocked.

## Expected divergence reference

| Item | Expected diff | Direction |
|---|---|---|
| `.env` | Gateway has TELEGRAM/DISCORD/API_SERVER tokens; local has SUDO_PASSWORD | Either |
| `auth.json` | Different tokens per machine | Either |
| LCM messages | VPS 50-200 ahead | VPS > local |
| `cron/jobs.json` | VPS has more recent run timestamps | VPS |
| Work dirs | Local extra dev-only dirs | Local |
| Profile `.env` | Template on VPS, none on local (no secrets either way) | Either |

## Recovery commands

```bash
# Restore config from backup if overwritten
cp ~/.hermes/config.yaml.hms-bak ~/.hermes/config.yaml

# Copy community manifest from VPS
scp root@100.113.2.25:.hermes/community-manifest.json ~/.hermes/

# Sync cron state from VPS
scp root@100.113.2.25:.hermes/cron/jobs.json ~/.hermes/cron/jobs.json

# Re-copy canonical HMS script from VPS
scp root@100.113.2.25:.hermes/bin/hms ~/.hermes/bin/hms

# Clean up backup debris
hms cleanup
# or: find ~/.hermes ~/work -name '*.hms-bak*' -type f -delete

# Run a proper HMS sync to converge
hms pull    # VPS → local (start of session)
# work ...
hms push    # local → VPS (end of session)
```

## If LCM DB was synced in wrong direction

If the hard sync pushed the VPS DB over the local one (or vice versa) and you've
lost sessions:

1. Check if the `.hms-bak` backup of lcm.db exists:
   ```bash
   find ~/.hermes -name 'lcm.db.hms-bak*' -type f 2>/dev/null
   ```
2. If it does, compare message counts:
   ```bash
   sqlite3 lcm.db.hms-bak 'SELECT COUNT(*) FROM messages'
   sqlite3 lcm.db 'SELECT COUNT(*) FROM messages'
   ```
3. If the backup has MORE messages, restore it:
   ```bash
   cp lcm.db.hms-bak lcm.db
   ```
4. Run a clean `hms pull` to converge both sides.
