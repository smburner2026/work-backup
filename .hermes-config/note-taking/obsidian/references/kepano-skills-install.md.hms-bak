---
name: kepano-skills-install
description: Install matrix and behavior notes for kepano/obsidian-skills across LLM agent platforms. What the 5 skills cover, restart requirements, and the install pattern that prevents the "files on disk are dead weight" failure mode.
---

# Kepano Skills — Install Matrix

Steph Ango (kepano, formerly Obsidian's product lead, now at Anthropic) maintains a curated set of agent skills for working with Obsidian. They follow the [agentskills.io](https://agentskills.io/specification) open spec.

## The 5 skills

| Skill | What it teaches the agent |
|---|---|
| `obsidian-markdown` | Obsidian Flavored Markdown — wikilinks, callouts, properties, embeds |
| `obsidian-bases` | Obsidian Bases (`.base` files) — queryable database views inside vaults |
| `json-canvas` | JSON Canvas (`.canvas` files) — visual graphs |
| `obsidian-cli` | Driving the Obsidian app via its CLI |
| `defuddle` | Clean markdown extraction from web pages |

**Important:** these are *format reference* skills. They do not auto-link, do not perform semantic search, do not run a dream cycle. The agent that uses them writes correct Obsidian syntax; the *agent itself* is the linker.

## Install by platform

### OpenCode (recommended for this user's stack)

```bash
mkdir -p ~/.opencode/skills/
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

**Critical:** clone the full repo, not just the inner `skills/` folder. The expected layout is `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`. OpenCode auto-discovers on startup.

**Restart required.** Auto-discovery reads SKILL.md files on launch. If OpenCode is already running, restart it. Without a restart, the new skills will not be available even though they're on disk.

### Claude Code

Add the contents of the repo to a `/.claude` folder at the root of the Obsidian vault (or whichever folder you're using with Claude Code). See [Anthropic's Claude Skills docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

### Codex CLI

Copy the `skills/` directory into `~/.codex/skills/`.

### Plugin marketplace (Obsidian's plugin system, not LLM-side)

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

This installs the skills *into Obsidian itself* for the in-app AI features. Different audience than the LLM-side install.

## What changes after install

Once the agent can load `obsidian-markdown`:
- Wikilinks are written with proper case (`[[Note Name]]`, not `[[note name]]`)
- Callouts use the OFM syntax (`> [!info]`, `> [!warning]`, `> [!quote]`)
- YAML frontmatter uses Obsidian properties (`tags`, `aliases`, `cssclass`, `created`, etc.)
- Base files (`.base`) are written with valid filter/view/formula syntax
- Canvas files (`.canvas`) are valid JSON matching the jsoncanvas.org spec

## Failure mode: "I installed but nothing changed"

If after install the agent still writes generic markdown:
- Verify the install path: `ls ~/.opencode/skills/obsidian-skills/skills/` (should show 5 subdirs)
- Verify the SKILL.md files exist in each: `ls ~/.opencode/skills/obsidian-skills/skills/obsidian-markdown/SKILL.md`
- Restart OpenCode — this is the most common reason
- Check that auto-discovery is enabled (it is by default; only an explicit `opencode.json` override can disable it)

## When NOT to install

- The user has no vault — installing skills without a vault is wasted disk
- The user is going to write the notes themselves manually (rare; the user is typically a delegator, see "agent is the linker" in SKILL.md)
- The vault is on a synced drive and the user wants skills to travel with it — kepano skills install to the agent home, not the vault; if the user wants vault-local skill copies, this is a different install pattern (Claude Code's `/.claude/` works for this)
