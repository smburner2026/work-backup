# Autonomous System Administration for Hermes

This reference documents patterns for enabling Hermes agents to perform autonomous system administration tasks by scanning documentation, cross-referencing against current setup, and executing maintenance actions.

## Overview

Autonomous system administration reduces operator cognitive load by having the agent:
1. Scan documentation sources for updates/changes
2. Cross-reference findings against the current instance configuration
3. Propose specific maintenance actions for user approval
4. Execute approved actions safely

This pattern aligns with the hermes-maintenance skill's goal of "long-term care of a Hermes Agent instance."

## Implementation Workflow

### Phase 1: Documentation Scan
- Check official Hermes documentation for recent updates
- Review skill repository changes (local, builtin, hub)
- Monitor release notes or version manifests
- Scan for configuration schema changes or new features

### Phase 2: Setup Cross-Reference
- Compare documented changes against current:
  - Installed skills and versions
  - Memory provider configuration (mnemosyne/honcho/etc.)
  - Honcho settings (dialectic depth, observation config)
  - Tool gateway configuration
  - Model/provider settings
  - Skill pinning/status

### Phase 3: Action Identification
Based on discrepancies, identify actions such as:
- **Config upgrades**: Apply new honcho dialectic depth controls
- **Memory hygiene**: Purge stale profile entries or forgotten configurations
- **Skill management**: Pin critical skills to prevent auto-archival
- **Tool updates**: Enable newly available toolsets or update API keys
- **Model updates**: Switch to newer/recommended models when appropriate

### Phase 4: Safe Execution
- Present proposed actions with clear rationale
- Require explicit user approval before execution
- Create checkpoints/backups before destructive operations
- Log actions taken for future reference
- Verify results post-execution

## Example Actions from Community Patterns

Based on real-world usage patterns:

### Honcho Memory Configuration
When documentation shows new dialectic depth controls:
```
# Check current honcho config
hermes config show honcho

# If missing/outdated, propose upgrade:
hermes config set honcho.dialectic_depth 3
hermes config set honcho.observation_config '{...}'
```

### Memory Stack Cleanup
When stale profile entries accumulate:
```
# Identify stale profiles in memory stack
# Propose purging forgotten entries:
# (Would be implemented via memory tool operations)
```

### Critical Skill Pinning
To prevent important skills from being archived:
```bash
# The curator CLI only accepts ONE skill per invocation:
hermes curator pin <skill-name>

# To pin multiple skills, use a loop:
cd ~/.hermes/skills && for skill in skill-a skill-b skill-c; do
  hermes curator pin "$skill"
done

# Verify pinned status:
hermes curator status
```

**Pin strategy — three tiers:**
1. **Infrastructure** (pin first): hermes-maintenance, background-agents, profile-guard-*, secrets-management, hermes-session-recovery, disk-full-mnemosyne-recovery
2. **High-use domain**: dabt-*, book-pdf-compilation, engineering-discipline, document-pipelines
3. **New/fragile** (pin immediately): Any skill created today/yesterday with 0 uses — the curator runs weekly and flags 30-day-unused skills as stale; brand-new skills need pinning before first real use

## Safety Guidelines

1. **Read-first approach**: Always scan and cross-reference before proposing actions
2. **Approval gate**: Require explicit user confirmation for any state changes
3. **Backup before change**: Ensure checkpoints exist for config/memory modifications
4. **Atomic actions**: Group related changes where possible to reduce intermediate states
5. **Verification step**: Confirm actions had intended effect after execution

## Curator Scope Limitation (Important)

The `hermes curator` commands (pin, archive, status, etc.) only operate on skills where `created_by: "agent"` in `~/.hermes/skills/.usage.json`. Skills with `created_by: null` (local/builtin/hub-installed) are **not** under curator control and will be rejected with "skill not found".

**Before attempting to archive/pin a skill, verify it's agent-created:**
```bash
grep '"skill-name"' ~/.hermes/skills/.usage.json
```
Look for `"created_by": "agent"` adjacent to the skill name. If it's `null`, the curator cannot manage it — those skills won't be auto-archived either, so they're safe but untracked.

**Typical curator-manageable skills include:**
- background-agents, hermes-maintenance, hermes-soul-design
- profile-guard-mike, profile-guard-jacob, profile-isolation
- agent-memory-hygiene, cronjob-management
- Most skills in `~/.hermes/skills/devops/` created by the agent

**Typical non-manageable skills:**
- All skills in subdirectories with `source: builtin` or `source: local` installed manually
- Skills cloned from git repos where `created_by` was never set to `"agent"`

## Integration with hermes-maintenance

This autonomous workflow complements the existing hermes-maintenance practices:
- Weekly backup ritual → Pre-action checkpoint creation
- Self-audits for update availability → Documentation scan phase
- Tracking community additions → Skill and tool monitoring
- Discovering what's been bolted onto base Hermes → Setup cross-reference

By adding autonomous scanning capabilities, hermes-maintenance evolves from periodic manual checks to continuous, lightweight oversight with actionable insights.