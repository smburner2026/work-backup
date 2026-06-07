## Slash Commands (In-Session)

Type these during an interactive chat session. New commands land fairly
often; if something below looks stale, run `/help` in-session for the
authoritative list or see the [live slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands).
The registry of record is `hermes_cli/commands.py` — every consumer
(autocomplete, Telegram menu, Slack mapping, `/help`) derives from it.

### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/snapshot [sub]      Create or restore state snapshots of Hermes config/state (CLI)
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/steer <prompt>      Inject a message after the next tool call without interrupting
/agents (/tasks)     Show active agents and running tasks
/resume [name]       Resume a named session
/goal [text|sub]     Set a standing goal Hermes works on across turns until achieved
                     (subcommands: status, pause, resume, clear)
/redraw              Force a full UI repaint (CLI)
```

### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/busy [sub]          Control what Enter does while Hermes is working (CLI)
                     (subcommands: queue, steer, interrupt, status)
/indicator [style]   Pick the TUI busy-indicator style (CLI)
                     (styles: kaomoji, emoji, unicode, ascii)
/footer [on|off]     Toggle gateway runtime-metadata footer on final replies
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/reload-skills       Re-scan ~/.hermes/skills/ for added/removed skills
/reload              Reload .env variables into the running session (CLI)
/reload-mcp          Reload MCP servers
/cron                Manage cron jobs (CLI)
/curator [sub]       Background skill maintenance (status, run, pin, archive, …)
/kanban [sub]        Multi-profile collaboration board (tasks, links, comments)
/plugins             List plugins (CLI)
```

### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update Hermes to latest (gateway)
/topic [sub]         Enable or inspect Telegram DM topic sessions (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/copy [N]            Copy the last assistant response to clipboard (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/gquota              Show Google Gemini Code Assist quota usage (CLI)
/status              Session info (gateway)
/profile             Active profile info
/debug               Upload debug report (system info + logs) and get shareable links
```

### Exit
```
/quit (/exit, /q)    Exit CLI
```

---

### Key Paths & Config

```yaml
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets
$HERMES_HOME/skills/        Installed skills
~/.hermes/sessions/         Session transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

### VPS Deployment Reference
See `references/vps-hetzner-setup.md` for the condensed first-time Hetzner CX23 + SSH key + Hermes install workflow and common first-boot pitfalls.

Profiles use `~/.hermes/profiles/<name>/` with the same layout.

### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value`.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `voice` | `record_key` (ctrl+b), `auto_tts`, `beep_enabled`, `silence_threshold`, `max_recording_seconds` |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` (built-in, mnemosyne, honcho, etc.) |
| `mnemosyne` | `auto_sleep`, `sleep_threshold`, `vector_type`, `ignore_patterns`, `profile_isolation` — only read when `memory.provider: mnemosyne`. See `references/mnemosyne-memory-provider.md` for details and pitfalls. |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

Full config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

### API Keys for Web & Search Tools

Hermes's web/search tools (`web` and `search` toolsets) use Tavily under the hood. These API keys are stored in `~/.hermes/.env`, not in `config.yaml`. You can see their status with `hermes config` (they show up as `(not set)` or masked), but attempting to set them via `hermes config set search.tavily_api_key <key>` **will crash** with `ValueError: Invalid environment variable name` — the dotted key path is rejected because the value maps to a flat env var.

**Correct setup (choose one):**

```bash
# Directly append to .env
echo 'TAVILY_API_KEY=tvly-xxxxx' >> ~/.hermes/.env

# Or edit .env manually
hermes config env-path        # prints ~/.hermes/.env path
```

**Keys visible via `hermes config`:**

| Label | Env var | Toolset |
|-------|---------|---------|
| Tavily | `TAVILY_API_KEY` | `web`, `search` |
| Browserbase | `BROWSERBASE_API_KEY` | `browser` |

After setting a key, run `hermes doctor` to verify it's picked up, then `/reset` (or start a new session) to activate the tool.

Full reference on search/web tools: `references/search-tool-api-keys.md`

### Bitwarden Secrets Manager

Pull API keys from Bitwarden Secrets Manager at process startup instead of storing them in plaintext inside `~/.hermes/.env`. One bootstrap secret (a machine-account access token) replaces N per-provider keys.

**Setup (when `hermes secrets` subcommand is available):**
```bash
hermes secrets bitwarden setup     # interactive wizard
hermes secrets bitwarden status    # check config
hermes secrets bitwarden sync      # dry-run pull
hermes secrets bitwarden sync --apply  # pull + apply
hermes secrets bitwarden disable   # flip off
```

**Manual setup (when `hermes secrets` is not available — v0.14.x and earlier):**
1. Ensure `BWS_ACCESS_TOKEN` is set in `~/.hermes/.env`
2. Install `bws` binary: `hermes config set secrets.bitwarden.auto_install true` (Hermes downloads v2.0.0 to `~/.hermes/bin/bws` on next startup)
3. Set project ID: `hermes config set secrets.bitwarden.project_id <uuid>`
4. Enable: `hermes config set secrets.bitwarden.enabled true`

**CRITICAL: Secret creation method matters.** The `bws` CLI returns inline values for secrets created via CLI:
```bash
bws secret create KEY_NAME "value" <project_id> --output json
```
Secrets created via the **Bitwarden web UI** store values as "file" type, which `bws` returns as `@/tmp/bws_xxx` file references — Hermes cannot resolve these. Always create secrets via CLI if they will be consumed by Hermes. To migrate existing web-UI secrets: delete them and recreate via CLI.

**Binary resolution order** (in `agent/secret_sources/bitwarden.py::find_bws()`):
1. `~/.hermes/bin/bws` (Hermes-managed copy — v2.0.0, preferred)
2. System PATH (`bws` on `$PATH`)
3. Auto-download to managed path (when `install_if_missing=True`)

If a newer `bws` (e.g. v2.1.0 from `apt`/`snap`) is on PATH before the managed copy is installed, Hermes picks the system one. To force the managed copy, remove the system `bws` from PATH and let Hermes auto-install v2.0.0.

**Using `bws run` for script-based secret injection:**
```bash
bws run --project-id <uuid> -- /path/to/script.sh
```
Note: `bws run` with inline shell commands (`sh -c 'echo ...'`) fails because `-c` clashes with `--color`. Always use a script file. The child process receives secrets as real env vars, but `env` output masks them as `***`.

**Config structure** (in `~/.hermes/config.yaml`):
```yaml
secrets:
  bitwarden:
    enabled: false           # master switch
    access_token_env: BWS_ACCESS_TOKEN
    project_id: ""           # UUID of the project
    cache_ttl_seconds: 300   # in-process fetch cache
    override_existing: true  # BSM values overwrite .env
    auto_install: true       # download bws if missing
```

**Docs:** https://hermes-agent.nousresearch.com/docs/user-guide/secrets/bitwarden

### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| AI Gateway (Vercel) | API key | `AI_GATEWAY_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| GitHub Copilot ACP | External | `COPILOT_CLI_PATH` or Copilot CLI |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|-----------------|
| `web` | Web search and content extraction |
| `search` | Web search only (subset of `web`) |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `video` | Video analysis and generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `todo` | In-session task planning and tracking |
| `kanban` | Multi-agent work-queue tools (gated to workers) |
| `debugging` | Extra introspection/debug tools (off by default) |
| `safe` | Minimal, low-risk toolset for locked-down sessions |
| `spotify` | Spotify playback and playlist control |
| `homeassistant` | Smart home control (off by default) |
| `discord` | Discord integration tools |
| `discord_admin` | Discord admin/moderation tools |
| `feishu_doc` | Feishu (Lark) document tools |
| `feishu_drive` | Feishu (Lark) drive tools |
| `yuanbao` | Yuanbao integration tools |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |

Full enumeration lives in `toolsets.py` as the `TOOLSETS` dict; `_HERMES_CORE_TOOLS` is the default bundle most platforms inherit from.

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

---
