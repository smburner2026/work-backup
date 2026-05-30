# Teknium on gbrain MCP Performance (May 2026)

**Source:** [@Teknium tweet](https://x.com/Teknium/status/2059029993058115710), May 25, 2026 — reply to Aakash/Garry Tan/@gbrainio

**TL;DR:** Two issues when gbrain is wired through MCP:
1. Context bloat from MCP payloads hitting every turn
2. Fix is Tier A/B/C skill routing (progressive loading)

## Full Tweet (truncated by X's API)

> Hey Aakash — two issues stacked on top of each other:
> 
> 1. Slowness: if you're hitting gbrain through MCP on every turn, the agent is reasoning over big payloads each time. Garry has a scaling guide for this — Tier A/B/C skill routing (~25K → ~4K tokens/turn).

(The full tweet was longer; only ~300 chars were extractable from X's server-side HTML.)

## What This Means for gbrain MCP Setup

The key issue Teknium flags: when gbrain tools (mcp_gbrain_search, mcp_gbrain_think, etc.) are **always available** in the agent's tool list, the tool definitions themselves consume ~25K tokens per turn in the system prompt. The agent also spends reasoning cycles deciding whether to call them.

The fix — **Tier A/B/C skill routing** — means loading gbrain tools only when the user's intent matches a gbrain-relevant query. In Hermes, this would look like:

- **Tier A** (always loaded, ~4K tokens) — core tools: terminal, file ops, web search
- **Tier B** (loaded on intent match) — gbrain MCP tools, code review tools
- **Tier C** (loaded only when explicitly triggered) — heavy synthesis, dream cycle control

This isn't built into Hermes's MCP wiring — it requires the agent to be selective about when to load the gbrain skill vs. having mcp_gbrain_* tools always registered.

## Practical Takeaway

Don't wire gbrain MCP into Hermes config.yaml as an always-on MCP server for high-turnrate sessions. Instead:
- Load the `gbrain` skill only when the user asks a brain-relevant question
- Or set up a `/gbrain` slash command that triggers the skill load

This keeps per-turn overhead at ~4K tokens instead of ~25K.
