# Community Extension OpSec

When installing third-party extensions to Hermes Agent — plugins, MCP servers, or skills — the risk profile differs significantly by type. Here's the framework.

## Three Surfaces

### Plugins (`hermes plugins install owner/repo`) — HIGHEST RISK

**Why:** Runs **in-process** with Hermes. Full access to the Python runtime, the filesystem, and — critically — all environment variables in `~/.hermes/.env` (OpenRouter, Anthropic, GitHub tokens, etc). There is no sandbox between a plugin and your secrets.

**Audit checklist:**
- Read the source before installing. Look at `src/`, especially `registry.register()` calls.
- Check what tools it exposes (each `register()` call adds a tool the agent can invoke).
- Scan for `os.environ` reads, network calls (`requests`, `urllib`, `aiohttp`), file reads outside the plugin's stated scope.
- Prefer authors with a visible track record (Nous Research, frequent committers, known organisations).
- `hermes plugins disable <name>` when not actively using — the plugin won't load on next session restart.
- Consider running a plugin-heavy Hermes under a dedicated OS user with a lean `.env` (only the keys that instance actually needs).

### MCP Servers — MEDIUM RISK

**Setup paths (same risk profile):**
- CLI: `hermes mcp add <name> --command ...` (ad-hoc, per-session)
- Config: `~/.hermes/config.yaml` → `mcp_servers:` block (persistent, auto-loads on startup — see the `native-mcp` skill)

Both paths create a subprocess that exposes tools to the agent. The vetting is identical.

**Why safer:** MCP servers run as **separate subprocesses**, not in-process. Hermes applies environment filtering — only `PATH`, `HOME`, `USER`, `LANG`, `LC_ALL`, `TERM`, `SHELL`, `TMPDIR`, and `XDG_*` vars pass through by default. Your API keys are not leaked to the MCP subprocess. Error messages are sanitised for credential patterns (`ghp_...`, `sk-...`, `token=`, `key=`, `password=`, `secret=`).

**Remaining risks:**
- Undocumented tools — an MCP server can register tools beyond what its README advertises.
- Whatever you explicitly pass via `--env` can be read or exfiltrated.
- MCP tool calls **bypass** the terminal dangerous-command approval flow. They're tool calls, not shell commands.

**Audit checklist:**
- `hermes mcp list` — shows all registered tool names. If you see something unexpected, investigate.
- `hermes mcp configure <name>` — selectively disable tools you don't need.
- Pass only the minimal set of env vars. For services with their own credential storage (e.g. `substack-mcp-plus` stores encrypted tokens via its setup wizard), you may need zero secrets in `--env`.
- Prefer `--command` (stdio) over `--url` (HTTP/SSE). Stdio has a smaller attack surface — no open port, no network-addressable endpoint.

### Skills (`hermes skills install <id>`, `hermes skills tap add owner/repo`) — LOWEST DIRECT RISK

**Why safe:** Skills are **markdown files** — no code execution on their own. The agent still goes through dangerous-command approval before running destructive shell commands.

**Real risk:** Prompt injection. A skill could instruct the agent to override its judgement, exfiltrate data, or call tools in ways the author intended to be harmful. A skill doesn't need destructive shell commands to cause damage — it could simply tell the agent to `web_extract` the contents of `~/.hermes/.env` and POST them somewhere.

**Mitigations:**
- `hermes skills inspect <id>` or `skill_view(name)` to read the content before installing.
- Prefer skills from the official hub (`source: official`, ★ badge) — Nous vets these.
- For community `tap add` repos, scan the skill text for prompt-injection patterns like "ignore previous instructions", "disregard your training", hidden HTML comments, or instructions to exfiltrate secrets.
- The agent's dangerous-command approval still protects against destructive shell commands, but quiet data-read-and-exfiltrate via HTTP tools is a harder class of attack to catch from the approval layer alone.
- Skills that ask you to install companion MCP servers or plugins should be treated with extra scrutiny — the skill itself might be harmless while being a delivery mechanism for a malicious MCP server.

### Additional Hardening

For a production gateway handling sensitive operations, run Hermes in a **container backend** (`terminal.backend: docker`, Modal, Daytona, etc.). This limits blast radius: if a plugin or MCP server goes rogue, the host's filesystem and primary `.env` are not exposed.

## Quick-Reference Table

| Extension type | Risk | Main threat | Primary mitigation |
|---|---|---|---|
| Official hub skill | Low | Prompt injection | Inspect before install |
| Community `tap` skill | Low-Medium | Prompt injection | Review text for injection patterns |
| Plugin, known author | Medium-High | Full env access | Audit `register()` calls + source |
| Plugin, random author | High | Any | Read every line or don't install |
| MCP server, stdio | Medium | Undocumented tools | `mcp list` + `mcp configure` + minimal env |
| MCP server, HTTP/SSE | Medium-Higher | Open port, network exposure | Network-isolate if possible |
