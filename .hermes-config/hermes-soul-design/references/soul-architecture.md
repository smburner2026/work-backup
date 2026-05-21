# Hermes Agent Soul Architecture

File-level anatomy of the Hermes soul system — where SOUL.md files live, how they're generated, loaded, and scoped.

## File Locations

| Component | Path | Purpose |
|-----------|------|---------|
| Master soul | `$HERMES_HOME/SOUL.md` (default `~/.hermes/SOUL.md`) | Active persona definition for the current profile |
| Profile souls | `$HERMES_HOME/profiles/<name>/SOUL.md` | Per-profile persona override |
| Default template | `hermes_cli/default_soul.py` | `DEFAULT_SOUL_MD` constant seeded on `hermes setup` or first run |
| Docker template | `docker/SOUL.md` | Distribution template |
| Compressed examples | `~/.hermes/skills/prompt-engineering/soul-compression/references/` | Reference souls in compressed format (aristocrat, euphy, KB template) |

## Generation Mechanism

- `hermes_cli/config.py:_ensure_default_soul_md()` writes `DEFAULT_SOUL_MD` from `default_soul.py` to `$HERMES_HOME/SOUL.md` if the file doesn't exist.
- Called during `hermes setup` and during `load_cli_config()` / config initialization.
- Profile souls: `hermes_cli/profiles.py` creates `profiles/<name>/SOUL.md` with the same default when creating a new profile.
- The default soul is minimal: "You are Hermes Agent, an intelligent AI assistant created by Nous Research..."

## Loading Semantics

- SOUL.md is reloaded **fresh every message** — no restart required.
- The system reads the file contents and injects them as persona instructions into the agent's system prompt each turn.
- Deleting the file or clearing its contents reverts to the built-in default (no soul instruction).
- The soul is **not** referenced from `config.yaml` — it's a standalone file in `HERMES_HOME`, sibling to `config.yaml`, `.env`, `sessions/`, `logs/`, etc.

## Profile Binding

- Each Hermes profile (`~/.hermes/profiles/<name>/`) can have its own `SOUL.md`.
- When a profile is active, *that* profile's SOUL.md becomes the master soul.
- Switching profiles via `hermes profile switch <name>` swaps the active SOUL.md.
- The doctor CLI (`hermes doctor`) checks if the soul file exists and reports issues.

## Compressed Soul Format

Reference souls in `soul-compression` use a dense DSL format with these sections:

- **Identity line:** Name, tone, style compressed into a single line
- **PersonalityRubric:** Numeric OCEAN scores + custom facet scores (0-100)
- **ExecRules:** Behavioral directives in compact form (`Bias→Action. Verify>Assume.`)
- **AGENT_LOOP:** The execution loop as a chain: `Assess→Gather→Plan→Execute→Verify→Deliver`
- **LEARN_LOOP:** The learning loop: `Persist→SkillMgmt→Reflect`
- **KNOWLEDGE_BASE:** Memory and skill management constraints
- **COMPLEX_TASK:** Decomposition strategies (OMNICOMP, ChainConstructor, etc.)
- **GUARDRAILS:** Self-reminders and resource limits

This format is optional — most users write plain-prose SOUL.md files. The compressed format is used by advanced users and power profiles like Euphy.

## CLI Interactions

- `hermes doctor` — validates soul file existence and contents
- `hermes profile switch <name>` — switches active profile (and thus active soul)
- `hermes setup` — creates default soul if missing
- The web dashboard (`hermes serve`) exposes `/api/profiles/{name}/soul` (GET/PUT) for GUI editing
- SOUL.md is not a slash command — it's loaded automatically every turn

## Relationship to Skills

- The `hermes-soul-design` skill teaches how souls work
- The `soul-compression` skill teaches how to write compressed souls
- Soul content is *persona*; skills are *procedural knowledge* (how to do things)
- They complement each other: the soul sets *who* you are, skills set *what* you know how to do
