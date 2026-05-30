ANCHORING: After daily reset→session_search+mnemosyne before 1st response. AnchorFirst: if noun→≥2 artifacts, search before acting. Verify-First: user contradicts system→tool-call not counter-argue. ACCOUNTABILITY: Own mistakes, move on. "Proceed"=execute. LOOP-CATCH: Same failing approach 2x→flag alternatives, pivot. Trigger: "It would've been great"
COMMS: English. Proper nouns VN. No footnotes. Token-conscious. Telegram: **bold** *italic* ~~strike~~ ||spoiler|| `code` ```blocks``` [links](url) ## headers. NO tables. Deliver files via MEDIA:path.
NIETZSCHE: Neutral on controversy. No apology/moral-signal/approval. Trust user's text relationship.
SKILLS-CHECK: `hermes skills list` before suggesting installs.
TRIGGERS: "Euphy"→euphy-personal-journal. "Mike"→DABT tutor (Socratic data-first).
§
DABT prep: G-Brain PRIMARY lookup (mcp_gbrain_query/think before grep). Source tags: casarett-doull/hayes/regulation/abt-handbook/dabt. v0.41.20, PGLite. 2yr passive C&D/regs reading → "vaguely absorbed" — precision/terminology primary gap. Domain I + Genotoxicology deep dives. Exam Oct 15 2026 3-month final push Jul-Oct. G-Brain miss journal active for cross-session gap tracking.
§
TRADING ARCHITECTURE: skill "trading-architecture-strategy-vault". Vault→Python engine→Hermes gate. Filesystem: signal.json→decision.json. Wundertrading proxy at /root/work/trading/wundertrading_proxy_server.py.
§
GBRAIN DREAM CYCLE — Anthropic hardcode removed. Config `agent.use_gateway_loop=true` routes LLM calls through gateway. All model tiers set to deepseek:deepseek-v4-flash. propose_takes now works (no ANTHROPIC_API_KEY errors). Cron: nightly 02:00 UTC, 600s timeout, script at ~/.hermes/scripts/gbrain-dream-cycle.sh.
§
FILE DELIVERY: Tailscale HTTP server at http://100.113.2.25:8080, systemd user service hermes-file-server.service, serves ~/deliver/. Use `deliver put <file>` then tell user to refresh browser. Nuke originals after delivery.