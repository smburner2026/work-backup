#!/usr/bin/env bash
# hms — Hermes Multi-Sync v2.0
# Safe bidirectional sync between local (WSL/desktop) and VPS.
# Local is the primary workhorse for RAM-heavy tasks.
# VPS is the always-on gateway (Telegram, cron, persistent services).
#
# Usage:
#   hms pull       VPS -> Local (catch up before local work)
#   hms push       Local -> VPS (after finishing local work)
#   hms watch      Continuous bidirectional sync daemon
#   hms stop       Stop the watch daemon
#   hms status     Show sync status
#   hms setup      Initial setup: copy script, configure, test
#   hms merge-db   Smart LCM DB merge (not just timestamp swap)
#
# Architecture:
#   - VPS is the canonical hub for gateway sessions (Telegram/Discord)
#   - Local is the heavy-lifting machine (inference, training, big queries)
#   - Sync is bidirectional with --update (never overwrite newer)
#   - Watch mode polls both sides every 30s for near-real-time sync
#   - Session DB uses VACUUM INTO snapshots to avoid corruption
#   - Config/.env/auth are per-machine -- NEVER synced

set -euo pipefail

###############################################################################
# CONFIG
###############################################################################
VPS_HOST="${HMS_VPS_HOST:-root@100.113.2.25}"
VPS_HERMES="${HMS_VPS_HERMES:-/root/.hermes}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
HMS_DIR="${HERMES_HOME}/hms"
PIDFILE="${HMS_DIR}/watch.pid"
WATCH_LOG="${HMS_DIR}/watch.log"
TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)

RSYNC_SAFE="-avz --no-o --no-g --no-t --update --backup --suffix=.hms-bak --exclude=*.hms-bak*"
EXCLUDE_COMMON="--exclude=.git/ --exclude=node_modules/ --exclude=venv/ --exclude=.venv/ --exclude=__pycache__/ --exclude=*.pyc --exclude=.DS_Store --exclude=*.log --exclude=.cache/"
EXCLUDE_SECRETS="--exclude=.env --exclude=auth.json --exclude=*.lock --exclude=config.yaml --exclude=credentials.*"

mkdir -p "$HOME/work" "$HMS_DIR" 2>/dev/null || true

###############################################################################
# Helpers
###############################################################################
say()  { echo "  [$(date +%H:%M:%S)] $*"; }
info() { echo "  [$(date +%H:%M:%S)] $*"; }
warn() { echo "  !! $*" >&2; }
die()  { echo "  ERROR: $*" >&2; exit 1; }

check_ssh() {
  ssh -q -o ConnectTimeout=5 "$VPS_HOST" exit 2>/dev/null || die "Cannot reach $VPS_HOST"
}

snapshot_db() {
  local src="$1" dst="$2"
  [ -f "$src" ] || { say "[db] $src not found, skipping"; return 0; }
  sqlite3 "$src" "VACUUM INTO '$dst';" || die "Failed to snapshot $src"
}

sync_to_vps() {
  local src="$1" dst="$2" label="$3"; shift 3
  local extra="$*"
  ssh "$VPS_HOST" "mkdir -p '$dst'" 2>/dev/null || true
  eval rsync $RSYNC_SAFE $extra "'$src/'" "'$VPS_HOST:$dst/'" 2>&1 | tail -1 || true
  say "[$label] pushed"
}

sync_from_vps() {
  local src="$1" dst="$2" label="$3"; shift 3
  local extra="$*"
  mkdir -p "$dst"
  eval rsync $RSYNC_SAFE $extra "'$VPS_HOST:$src/'" "'$dst/'" 2>&1 | tail -1 || true
  say "[$label] pulled"
}

###############################################################################
# Gateway management
###############################################################################
vps_gateway_stop() {
  say "[gateway] stopping VPS gateway..."
  ssh "$VPS_HOST" "XDG_RUNTIME_DIR=/run/user/\$(id -u) systemctl --user stop hermes-gateway.service 2>/dev/null" || true
  sleep 1
}
vps_gateway_start() {
  say "[gateway] starting VPS gateway..."
  ssh "$VPS_HOST" "XDG_RUNTIME_DIR=/run/user/\$(id -u) systemctl --user start hermes-gateway.service 2>/dev/null" || true
  sleep 2
  local s=$(ssh "$VPS_HOST" "XDG_RUNTIME_DIR=/run/user/\$(id -u) systemctl --user is-active hermes-gateway.service 2>/dev/null" || echo "unknown")
  say "[gateway] status: $s"
}

###############################################################################
# Timestamp-gated DB sync
###############################################################################
newer_side() {
  local lp="$1" rp="$2"
  local lm=$(stat -c%Y "$lp" 2>/dev/null || echo 0)
  local rm=$(ssh "$VPS_HOST" "stat -c%Y $rp 2>/dev/null || echo 0" 2>/dev/null || echo 0)
  [ "$lm" -gt "$rm" ] && return 0
  [ "$rm" -gt "$lm" ] && return 1
  return 2
}

sync_db_push() {
  local db="$1" label="$2"
  local ld="$HERMES_HOME/$db" vd="$VPS_HERMES/$db"
  [ ! -f "$ld" ] && { say "[$label] no local DB"; return 0; }
  newer_side "$ld" "$vd" && local_n=true || local_n=false
  $local_n || { say "[$label] VPS same/newer"; return 0; }
  local snap="/tmp/hms-${db//\//-}-snapshot.db"
  echo "$db" | grep -q lcm && vps_gateway_stop
  snapshot_db "$ld" "$snap"
  rsync -avz "$snap" "$VPS_HOST:$vd" | tail -1
  ssh "$VPS_HOST" "rm -f ${vd}-wal ${vd}-shm" || true
  rm -f "$snap"; say "[$label] pushed"
  echo "$db" | grep -q lcm && vps_gateway_start
}

sync_db_pull() {
  local db="$1" label="$2"
  local ld="$HERMES_HOME/$db" vd="$VPS_HERMES/$db"
  ssh "$VPS_HOST" "[ -f $vd ]" 2>/dev/null || { say "[$label] no VPS DB"; return 0; }
  newer_side "$ld" "$vd" && local_n=true || local_n=false
  $local_n && { say "[$label] local same/newer"; return 0; }
  local snap="/tmp/hms-${db//\//-}-snapshot.db"
  ssh "$VPS_HOST" "sqlite3 $vd \"VACUUM INTO '$snap';\"" || die "VPS snapshot failed"
  rsync -avz "$VPS_HOST:$snap" "$ld" | tail -1
  ssh "$VPS_HOST" "rm -f $snap" || true
  rm -f "${ld}-wal" "${ld}-shm" || true
  say "[$label] pulled"
}

###############################################################################
# Commands
###############################################################################
cmd_pull() {
  echo "=== HMS PULL -- VPS > Local ==="; echo "  VPS: $VPS_HOST"; echo ""
  check_ssh
  say "[skills] pulling..."
  sync_from_vps "$VPS_HERMES/skills" "$HERMES_HOME/skills" "skills"
  say "[plugins] pulling..."
  sync_from_vps "$VPS_HERMES/plugins" "$HERMES_HOME/plugins" "plugins" "$EXCLUDE_SECRETS"
  say "[scripts] pulling..."
  sync_from_vps "$VPS_HERMES/scripts" "$HERMES_HOME/scripts" "scripts"
  say "[bin] pulling..."
  sync_from_vps "$VPS_HERMES/bin" "$HERMES_HOME/bin" "bin"
  say "[cron] pulling..."
  sync_from_vps "$VPS_HERMES/cron" "$HERMES_HOME/cron" "cron"
  say "[profiles] pulling..."
  sync_from_vps "$VPS_HERMES/profiles" "$HERMES_HOME/profiles" "profiles" "$EXCLUDE_SECRETS"
  echo ""; say "[lcm] pulling session DB..."; sync_db_pull "lcm.db" "lcm"
  say "[mnemosyne] pulling..."
  sync_from_vps "$VPS_HERMES/mnemosyne" "$HERMES_HOME/mnemosyne" "mnemosyne" "--exclude=models/ --exclude=cache/"
  ssh "$VPS_HOST" "[ -d $VPS_HERMES/memories ]" 2>/dev/null && sync_from_vps "$VPS_HERMES/memories" "$HERMES_HOME/memories" "memories" || true
  echo ""; say "[work] pulling..."
  sync_from_vps "~/work" "$HOME/work" "work" "$EXCLUDE_COMMON"
  say "[hms] self-sync..."
  rsync -avz "$VPS_HOST:$VPS_HERMES/bin/hms" "$HERMES_HOME/bin/hms" 2>&1 | tail -1 || true
  chmod +x "$HERMES_HOME/bin/hms" 2>/dev/null || true
  echo ""; say "[config] SKIPPED -- per-machine"; echo "=== HMS PULL complete ==="
}

cmd_push() {
  echo "=== HMS PUSH -- Local > VPS ==="; echo "  VPS: $VPS_HOST"; echo ""
  check_ssh
  say "[skills] pushing..."; sync_to_vps "$HERMES_HOME/skills" "$VPS_HERMES/skills" "skills"
  say "[plugins] pushing..."; sync_to_vps "$HERMES_HOME/plugins" "$VPS_HERMES/plugins" "plugins" "$EXCLUDE_SECRETS"
  say "[scripts] pushing..."; sync_to_vps "$HERMES_HOME/scripts" "$VPS_HERMES/scripts" "scripts"
  say "[bin] pushing..."; sync_to_vps "$HERMES_HOME/bin" "$VPS_HERMES/bin" "bin"
  say "[cron] pushing..."; sync_to_vps "$HERMES_HOME/cron" "$VPS_HERMES/cron" "cron"
  say "[profiles] pushing..."; sync_to_vps "$HERMES_HOME/profiles" "$VPS_HERMES/profiles" "profiles" "$EXCLUDE_SECRETS"
  echo ""; say "[lcm] pushing session DB..."; sync_db_push "lcm.db" "lcm"
  say "[mnemosyne] pushing..."; sync_to_vps "$HERMES_HOME/mnemosyne" "$VPS_HERMES/mnemosyne" "mnemosyne" "--exclude=models/ --exclude=cache/"
  [ -d "$HERMES_HOME/memories" ] && sync_to_vps "$HERMES_HOME/memories" "$VPS_HERMES/memories" "memories" || true
  echo ""; say "[work] pushing..."; sync_to_vps "$HOME/work" "~/work" "work" "$EXCLUDE_COMMON"
  echo ""; say "[config] SKIPPED -- per-machine"; echo "=== HMS PUSH complete ==="
}

cmd_watch() {
  [ -f "$PIDFILE" ] && { local p=$(cat "$PIDFILE" 2>/dev/null || echo ""); [ -n "$p" ] && kill -0 "$p" 2>/dev/null && { say "Already running (PID $p)"; return 0; }; rm -f "$PIDFILE"; }
  echo "$$" > "$PIDFILE"; echo "=== HMS WATCH (PID $$) ==="; echo "  Log: $WATCH_LOG"; echo ""
  exec >> "$WATCH_LOG" 2>&1; check_ssh; say "[watch] started"
  cmd_pull; cmd_push; say "[watch] initial sync done"
  while true; do sleep 30
    local ch=0
    find "$HERMES_HOME/skills" "$HERMES_HOME/scripts" "$HERMES_HOME/bin" "$HOME/work" -type f -mmin -1 2>/dev/null | head -1 | grep -q . && ch=1
    ssh "$VPS_HOST" "find $VPS_HERMES/skills $VPS_HERMES/scripts $HOME/work -type f -mmin -1 2>/dev/null" 2>/dev/null | head -1 | grep -q . && ch=1
    [ "$ch" = "1" ] && { say "[watch] changes -- syncing..."; cmd_pull 2>&1 | tail -3; cmd_push 2>&1 | tail -3; }
  done
}

cmd_stop() {
  [ -f "$PIDFILE" ] && { local p=$(cat "$PIDFILE" 2>/dev/null || echo ""); [ -n "$p" ] && kill -0 "$p" 2>/dev/null && kill "$p" 2>/dev/null && say "Stopped (PID $p)"; rm -f "$PIDFILE"; } || say "Not running"
}

cmd_setup() {
  echo "=== HMS SETUP ==="; echo "  VPS: $VPS_HOST"; echo "  Target: $HERMES_HOME"; echo ""
  check_ssh; ssh "$VPS_HOST" "ls -d $VPS_HERMES" 2>/dev/null || die "VPS Hermes not found"
  cmd_pull
  echo ""; echo "--- Local setup ---"
  echo "Add to ~/.bashrc:"; echo "  export PATH=\"\$PATH:\$HOME/.hermes/bin\""
  echo ""; echo "Cron for auto-sync:"; echo "  */30 * * * * \$HOME/.hermes/bin/hms pull && \$HOME/.hermes/bin/hms push >> \$HOME/.hermes/logs/hms-cron.log 2>&1"
  echo ""; echo "Boot-up auto-pull (add to ~/.bashrc):"; echo "  \$HOME/.hermes/bin/hms pull 2>/dev/null"
  local vc=$(ssh "$VPS_HOST" "find $VPS_HERMES/skills -type f -name '*.md' 2>/dev/null | wc -l" || echo "?")
  local lc=$(find "$HERMES_HOME/skills" -type f -name '*.md' 2>/dev/null | wc -l || echo "?")
  echo "  Skills: VPS=$vc  Local=$lc"; echo "=== HMS SETUP complete ==="
}

cmd_status() {
  echo "=== HMS STATUS -- $TIMESTAMP ==="; check_ssh
  local vc=$(ssh "$VPS_HOST" "find $VPS_HERMES/skills -type f -name '*.md' 2>/dev/null | wc -l" || echo "?")
  local lc=$(find "$HERMES_HOME/skills" -type f -name '*.md' 2>/dev/null | wc -l || echo "?")
  echo "  Skills: VPS=$vc | Local=$lc"
  local vp=$(ssh "$VPS_HOST" "ls -d $VPS_HERMES/profiles/*/skills 2>/dev/null | wc -l" || echo "?")
  local lp=$(ls -d "$HERMES_HOME/profiles/"*/skills 2>/dev/null | wc -l || echo "?")
  echo "  Profiles: VPS=$vp | Local=$lp"
  local vdb=$(ssh "$VPS_HOST" "stat -c%s $VPS_HERMES/lcm.db 2>/dev/null || echo 0")
  local ldb=$(stat -c%s "$HERMES_HOME/lcm.db" 2>/dev/null || echo 0)
  local vm=$(ssh "$VPS_HOST" "stat -c%Y $VPS_HERMES/lcm.db 2>/dev/null || echo 0")
  local lm=$(stat -c%Y "$HERMES_HOME/lcm.db" 2>/dev/null || echo 0)
  echo "  LCM: VPS=${vdb}b (mtime:$vm) | Local=${ldb}b (mtime:$lm)"
  [ -f "$PIDFILE" ] && kill -0 $(cat "$PIDFILE" 2>/dev/null) 2>/dev/null && echo "  Watch: running (PID $(cat $PIDFILE))" || echo "  Watch: not running"
  echo "  Gateway: $(ssh "$VPS_HOST" \"systemctl --user is-active hermes-gateway.service 2>/dev/null\" || echo 'unknown')"
  echo "=== HMS STATUS done ==="
}

cmd_merge_db() {
  echo "=== HMS MERGE-DB ==="; check_ssh
  newer_side "$HERMES_HOME/lcm.db" "$VPS_HERMES/lcm.db" && n="local" || n="vps"
  if [ "$n" = "local" ]; then say "Local newer -- pushing"; sync_db_pull "lcm.db" "lcm-backup"; sync_db_push "lcm.db" "lcm"
  else say "VPS newer -- pulling"; sync_db_pull "lcm.db" "lcm"; fi
  echo "=== HMS MERGE-DB complete ==="
}

cmd_cleanup() {
  echo "=== HMS CLEANUP ==="
  local h=$(hostname 2>/dev/null || echo "")
  if [ "$h" = "ghjgh" ]; then
    local bc=$(find "$HERMES_HOME" -name '*.hms-bak*' -type f 2>/dev/null | wc -l)
    [ "$bc" -gt 0 ] && { find "$HERMES_HOME" -name '*.hms-bak*' -type f -delete 2>/dev/null; echo "  removed $bc .hms-bak files"; }
    echo "  Disk: $(df -h "$HERMES_HOME" | tail -1)"; du -sh /root/*/ 2>/dev/null | sort -rh | head -8
  else
    check_ssh
    local bc=$(ssh "$VPS_HOST" "find $VPS_HERMES -name '*.hms-bak*' -type f 2>/dev/null | wc -l" 2>/dev/null || echo 0)
    [ "$bc" -gt 0 ] && ssh "$VPS_HOST" "find $VPS_HERMES -name '*.hms-bak*' -type f -delete 2>/dev/null" && echo "  removed $bc .hms-bak files"
    echo "  VPS: $(ssh "$VPS_HOST" "df -h $VPS_HERMES | tail -1" 2>/dev/null || true)"
  fi
  echo "=== HMS CLEANUP done ==="
}

case "${1:-help}" in
  pull|down)    check_ssh; cmd_pull ;;
  push|up)      check_ssh; cmd_push ;;
  watch|daemon) cmd_watch ;;
  stop|kill)    cmd_stop ;;
  setup|init)   cmd_setup ;;
  status|st)    check_ssh; cmd_status ;;
  merge-db|merge) cmd_merge_db ;;
  cleanup)      cmd_cleanup ;;
  *)
    echo "hms -- Hermes Multi-Sync v2.0"; echo ""
    echo "Commands: pull  VPS->Local | push  Local->VPS | watch  Continuous sync"
    echo "          setup Initialize local from VPS | stop  Stop watch daemon"
    echo "          status  Show sync state | merge-db  Merge divergent session DBs"
    echo "          cleanup  Remove .hms-bak debris"
    echo "Config: HMS_VPS_HOST (default: root@100.113.2.25), HMS_VPS_HERMES (default: /root/.hermes)"
    ;;
esac