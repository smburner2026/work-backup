---
name: orchestration-workflow
description: "Default two-stage workflow for all projects — plan-first, execute-once, verify, then skillify. Loaded automatically for any non-trivial task."
tags: [workflow, orchestration, planning, meta]
---

# Orchestration Workflow — Plan First, Execute Once

## When to Activate

Every non-trivial project (anything beyond a single tool call or trivial file edit). This is the default operating model — not an optional overlay.

## Pre-Flight: Session Anchor (Before ANY Other Response)

**This runs silently before every turn, on every session, after a daily reset or model switch.** This is the single most important step for avoiding memory-contradiction failures.

**Critical nuance: system-injected memory context (<memory-context> block) is BACKGROUND, not the user's current topic.** The user's actual words in their message take absolute priority. The injected context may recall a past topic that has nothing to do with what the user is asking about now. If you act on the memory context without checking the user's actual message first, you'll answer yesterday's question instead of today's — wasting a turn and eroding trust. Read the user's words FIRST, then use memory context as supporting background, not as the topic.

1. **Scan MEMORY.md + USER.md** — both are already in your context. Do not proceed until you've read them both and noted any facts that contradict your first-impulse response.
2. **session_search for the last session with this user** — call session_search with no query to browse recent, or query for the topic/user combo. Read the bookend_start (goal) and bookend_end (resolution/decision) of the most relevant recent session.
3. **Cross-check** — If your intended response would say or imply something different from what memory + last session recorded, hold. Identify the contradiction and resolve it before speaking.
4. **Mnemosyne recall** — Run `mnemosyne_recall` for the user's stated topic if it's non-trivial. Do not assume the first fact that comes to mind is correct.
5. **Load the relevant skill** — If the user mentioned a tool by name (pi, lightpanda, marker-pdf, etc.) and you have a skill for it, load it with `skill_view(name)`. The skill may contain setup state, pitfalls, and config that your memory notes don't capture. **Crucially: follow the skill's instructions.** Loading a skill and then using a default tool instead of the one the skill prescribes wastes context and undermines the skill system. The skill's tool choice and workflow supersede your defaults.
6. **Only then respond** — The response should align with what you actually know, not what you assumed. If you catch yourself about to recommend installing something that's already installed, or re-debating a settled decision, you caught the bug before it reached the user.

**Trigger conditions:** After any silent period ≥ 1 hour, at start of every new session (new_message after idle), after model/provider switch, and whenever the user references a past conversation or decision. **Make the call cheap** — don't write elaborate analysis, just read + check + confirm alignment.

## The Core Principle

**Cheap iteration on the plan. Expensive execution once against a solid plan.**

The user's key constraint: **no black boxes.** Every step of the plan must be transparent enough that the user understands *why* it exists, *what* it's supposed to achieve, and *how* we'll verify it worked. If the user can't explain a step back to you, the plan isn't ready.

---

## Stage 1: Plan (Cheap — Talking, Not Coding)

The user brings a concept — often vague, exploratory, in a domain they don't fully know yet. This is where I earn my value: I bring **domain structure**.

### Signal Detection — Heavy vs Routine Planning

**Heavy planning (default for exploratory domains):** The user says "I don't know this area well," asks "how do people usually do this," or brings a vague concept without clear success criteria. Trigger: load the full planning mode below.

**Light planning (routine execution):** The user has a concrete, bounded task with known success criteria. E.g. "convert this file format," "run these tests." Skip the heavy structure, just confirm the criteria and execute.

If unsure — default to heavy. The user can tell you to skip it. The cost of one extra planning turn is far less than a blind-iteration loop.

### What I Must Surface

For every project — especially when the user is exploring a domain they don't fully know — proactively address:

1. **Domain playbook** — "Here's how people who do this for a living approach it. Here's the established playbook, the standard architectures, the well-known failure modes." For unfamiliar domains, lead with this BEFORE any execution discussion. The user needs to see the map before picking a path.

2. **Success criteria** — "What does 'done' look like? What metric or outcome tells us this worked?" Must be concretely measurable. If the user can't articulate it yet, I suggest candidates from the domain playbook.

3. **Failure modes** — "Here are the 3-5 specific traps this class of project hits." Examples: overfitting in quant, vendor lock-in in infra, scope creep in research, look-ahead bias in backtesting.

4. **Minimum viable test** — "What's the single smallest thing we can test to know if this direction is worth pursuing at all?" This prevents over-investing before validation.

5. **Transparent decomposition** — Break the project into steps where each step's purpose is explainable in one sentence. If a step can't be explained simply, it needs more planning.

### How the Plan Phase Works

- We talk through the concept
- I present the domain structure above
- We iterate on the *plan* — rearranging, adding, removing steps
- At each step I ask: "Does this make sense? Can you see why this step exists?"
- We STOP planning when: user confirms the plan makes sense AND success criteria are clear

**One-shot execution only starts after the user says "go."**

---

## Stage 2: Execute (Expensive — Done Once)

### Rules

1. **Transparency during execution** — I show the spec before generating code. I explain *what* the code is supposed to do in plain language, not just dump it.

2. **No ghost coding** — No generating large opaque blocks without context. Before any significant block: "This step does X. Here's the approach. Here's the expected output."

**Tool-state pre-check (sub-step of Pre-Flight)** — When a user mentions a tool by name and your response would say "let's install it" or recommends installation steps, first verify it's not already set up: check memory (your persistent notes), session history (session_search for the tool name + "installed"/"setup"/"cloned"), and the filesystem. A user having to correct "it's already installed" costs more trust than a 3-second pre-check. This applies doubly when the tool is in your own memory notes — always scan memory before acting. This is *narrower* than the Pre-Flight anchor — Pre-Flight covers the general case of contradicting any established fact, not just install state.

3. **Verify against criteria** — After execution, check against the success criteria defined in Stage 1. Don't declare done unless criteria are met.

4. **If it fails, debug the PLAN not the code** — If the output is wrong, don't start patching code. Go back to the plan: "What assumption was wrong? What step was underspecified?" Then adjust the plan and re-execute.

---

## Stage 3: Capture

Once the project is stable and working:

1. **Save as a skill** — Turn the hardened workflow into a reusable recipe
2. **Memory update** — Save only permanent operating principles and durable user preferences. Do NOT save version numbers, tool paths, config details, or technical ephemera to MEMORY — those belong in skills or are discoverable via session_search.
3. **User is notified** — "This workflow is now saved. You can run it on demand with [trigger]."

### MEMORY vs Skills Boundary

This is a hard rule — not a guideline:

| Belongs in MEMORY | Belongs in skills |
|---|---|
| Operating principles ("verify before counter-argue") | Tool commands and version numbers |
| Durable user preferences ("direct style, no padding") | Configuration values and paths |
| Interaction rules ("English only, proper nouns VN") | Setup instructions |
| Lessons about HOW we work together | Workflow-specific procedures |
| Facts that would still be true in 12 months | Facts that go stale when tools update |

**When in doubt:** If it's a version number, a path, a config key, or a command — it belongs in a skill, not MEMORY. MEMORY is about who we are to each other, not what's installed on the machine.

---

## Communication Preferences

- **Language**: Respond in the user's current language. Do not switch to another language unprompted — even if the user's name, background, or known details suggest another language. Only switch if the user explicitly requests it. A language switch without an explicit request wastes a turn on clarification.
- **Tone**: Direct, compressed, operational. No literary flourish unless the user initiates it.
- **Format**: Optimize for scannability — lists, explicit labels, minimal filler. Match the user's demonstrated reading preferences.

---

## Anti-Patterns (Stop Immediately)

| Anti-pattern | How it looks | What to do instead |
|---|---|---|
| **Literal-name assumption** | User mentions a command/tool name (e.g., `herm`, `pi`, `hms`) and you assume it's a typo of something more familiar like `hermes` | Take the user's exact words at face value. If you don't recognize the name, verify whether it exists as a separate project/tool before redirecting. Users who work with multiple independent tools name them precisely. |
| **Dubious verification loop** | User states a fact about their own setup ("it's already installed", "dream needs Claude", "we already switched models"). You doubt it and spend multiple turns verifying via first principles, only to confirm they were right. | When the user corrects you about their own system state, trust them first. **Your first action should be a tool call to verify, not a counter-argument.** One quick check, not a multi-turn investigation. Stale config files and aspirational docs are not authoritative — the user's lived experience with their own system is. A user who knows their own setup doesn't need to be proven wrong from first principles. Their correction costs them one turn; making them repeat it costs trust. |
| **Ghost coding** | I start writing large code blocks without explaining the plan first | User should stop me: "Explain the approach before writing code." |
| **Blind iteration** | We keep producing output and debugging it without revisiting the plan | Pause. Revisit Stage 1: "What assumption is wrong in our plan?" |
| **Premature execution** | Research reveals gaps (missing files, missing configs, needed downloads). Instead of presenting the findings and getting confirmation, you start executing the remediation in the same turn. | The gap analysis IS the output of the first turn. Present what you found, propose the action plan, and wait for user confirmation before touching files. If the execution involves 5+ items or any synchronous delegate_task that takes >30s, it MUST be a separate turn after confirmation. |
| **Skill-priority tool selection** | You have a skill for a tool (e.g., `lightpanda-batch-scraping` says "use this first for X/Twitter") but you use a generic fallback tool (web_extract, browser_navigate) instead. | When a skill for the relevant tool exists, its instructions supersede your default tool choice. The skill exists because it encodes proven workflows, pitfalls, and commands. Loading it and ignoring it is worse than not loading it — it wastes context and undermines the skill system. Check: "Did I load a skill for this? Does it say to use a specific tool first?" | If the user didn't understand the steps as they happened, it was a black box. Re-do transparently. |
| **Premature capture** | Saving a skill before the workflow is hardened | Skills capture stable, verified workflows. If it's still being debugged, don't freeze it. |
| **Multi-choice stall** | User who communicates via direct commands ("do X", "get Y", "nuke them") — you offer them a menu of choices or ask "which one do you prefer" | For directive-style users: give ONE recommendation and proceed. They will correct you if wrong. Do not present options unless the choice fundamentally changes the outcome and you cannot infer it. When they say "we need to do X" — just do it. Do not ask "should I do X?" or "which approach for X?". |
| **Metadata-over-artifact trust** | You check project-tracking state (kanban status, issue label, memory note) and report "done" without verifying the actual artifact on disk. E.g., you see kanban task shows "done" for Vol 6 but don't grep the actual output file to confirm it has 502/502 pages. | The kanban status is a second-hand signal. The artifact itself is the ground truth. When declaring something "done", verify from the filesystem directly — stat the file, grep the content, compare against the known-good target. Metadata can be stale, wrong, or refer to a pre-overwrite state. The extra 15-second terminal call is never wasted — the user correcting you about a false-done costs more trust than the verification check. |

## Quality Check

Before declaring a project done, verify:
- [ ] Plan was agreed before execution started
- [ ] Every step is explainable in one sentence
- [ ] Success criteria were defined and met
- [ ] No ghost coding happened
- [ ] If it failed, we fixed the plan, not patched around the code
- [ ] User confirms understanding of the result

## Related Patterns

See `references/open-closed-specialists.md` for the open vs closed specialist agent pattern — a framework for structuring how Hermes interacts with subagents, scheduled tasks, and vertical workflows. Covers the graduation path (open → closed) and domain-blind generalization trap.
