[BILL] Avoid billable Nous(browser/img-gen/TTS/Firecrawl/GroktoCrawl); use OpenRouter.
[DABT] `mike` profile for all DABT work. Workflow audits/reviews→kanban cards w/ concrete system examples.
[QUALITY] Stability over new features when degraded. (2026-06-07 abandonment risk noted)
[EXEC] Execute immediately on request—no analysis/pre-flight menus. Return outcomes.
[ARTIFACT] Session JSON>cutoff→gzip ~/backups/archive/old-sessions/; keep sessions.json/db protected. Config backups→latest 1 only. Weekly cron cleanup preferred.
[DIRS] Extreme clean-dir preference: no temp files, orphan dirs, merged folders. Delete .hms-bak aggressively.
[ISOLATION] Strict 5-profile isolation. Default=orchestrator. Controlled 1-way skill push to jacob/mike/euphy only. orchestrator-profile-skill-pusher skill governs this.
[STYLE] Direct, non-repetitive output. No repetitive sign-offs. No incomplete/cut-off responses.
[SOURCE] Text analysis→primary source first, direct quotes. No framework-only without grounding.
[MEMORY] Session history is recoverable memory—high-value, do not delete casually. Backup repo `/root/work`. Archived sessions→~/.hermes/backups/archive/old-sessions/ as .jsonl.
§
Session recovery via backup archive is actual but incomplete. Recovery of old sessions does NOT auto-merge into live session_search DB. WSL history in /root/.hermes/sessions/sessions-wsl.json (851 lines, May 21+). Live session_search only returns post-hygiene cluster (May 30+). Aggressive compression/hygiene settings: threshold 0.75, target_ratio 0.2, hygiene_hard_message_limit 600, protect_first_n=3, protect_last_n=20. Output truncation issue observed in delivered messages. Disk pressure: root 55% used (20G/38G), sessions dir 303M. Active session count ~32k messages.
§
Skill library disciplined update required during tool review pass. Execute skill_manage updates only within memory/skill tools scope.