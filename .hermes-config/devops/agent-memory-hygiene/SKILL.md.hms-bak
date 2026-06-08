---
name: agent-memory-hygiene
description: Rules for treating user-provided memory context, session corrections, and explicit "we already have that" signals as binding before proposing actions. Prevents repetition of completed work or already-rejected approaches.
---

# Agent Memory Hygiene

## Core Rule
When the user supplies explicit memory context, session history, or states "we already have that" / "you are forgetting," treat the supplied information as authoritative. Do not re-propose the same action or solution.

## Trigger Conditions
- User pastes memory blocks or says "review the conversation"
- User says phrases like "we already have that", "you're repeating yourself", "fix your reasoning"
- User corrects a repeated suggestion or forgotten fact

## Required Behavior
1. Immediately acknowledge the supplied context as binding.
2. Stop the current proposal and ask for the delta or next constraint instead of re-explaining the same thing.
3. Do not default to generic solutions when operational facts have already been established in the current session or recent memory.
4. When the user asserts an operational fact (e.g., "we created this before", "I already did this", "this is complete"), run `session_search` BEFORE any counterclaim. Treat the user's assertion as the working hypothesis.
5. If your shell/filesystem view contradicts the user's claim, treat it as a state-drift or naming issue, not as evidence the user is wrong. Reconcile the discrepancy silently and present the reconciled state.

## Session Deletion Protocol (High Risk)
When the user asks to delete sessions, close chats, or clear history: treat this is a destructive operation requiring explicit memory-discipline steps BEFORE any deletion begins.

### Pre-flight Requirements
1. **Name the stakes.** Say what will be deleted (session transcripts, chat history) and what will NOT be deleted (Mnemosyne DB, `MEMORY.md`, `USER.md`, skills, artifacts). Do this BEFORE the first delete.
2. **Confirm current scope.** Show the user the exact list/set of sessions that match their request so they can validate the filter.
3. **Batch in one shot, not loops.** Avoid per-item confirmation loops. Build the target list first, present once, delete in one operation.
4. **Stop on ambiguity.** If the user’s request mixes “sessions” with “memory” or “kanban tasks,” clarify which category they mean; do not guess.
5. **Treat user panic as truth, not noise.** If the user later asks “what happened to our memory” or says “that’s months of memories gone,” immediately produce a clear memory-state report and offer recovery options rather than restating what was already done.

### Pitfalls to Avoid
- Treating recent session memory as "soft" or optional.
- Re-proposing a mechanism (plugin, cron, workflow) the user has already confirmed exists.
- Generating new suggestions before confirming the supplied memory context has been integrated.
- Executing bulk deletion without first distinguishing durable memory (Mnemosyne/MEMORY.md) from transient session transcripts, especially when the user is sensitive to data loss.

## Verification Step
Before any recommendation on a recurring operational topic (disk, plugins, Kanban, Mnemosyne, etc.), explicitly state the known state from the provided memory context first.

This skill overrides normal suggestion behavior when the above triggers fire.