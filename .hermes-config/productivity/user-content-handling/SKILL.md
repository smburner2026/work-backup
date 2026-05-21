---
name: user-content-handling
description: "Govern how the agent processes user-provided content — distinguishing reference/discussion material from active profiling/ingestion tasks. Covers the restraint protocol (don't act on shared content unless asked) and the profiling workflow (extract traits from chat histories into durable memory)."
category: productivity
tags: [content, protocol, profiling, memory, chat-history, reference, ingestion]
trigger: |
  User pastes a document, sends a file attachment, shares a link, or provides chat history exports.
  Any time the agent receives content from the user without an explicit action frame.
---

# User Content Handling

## When to Use

- User pastes a document, file, link, or reference block in conversation
- User provides chat history exports, share links, or conversation logs from other models
- User shares material without specifying whether it's for reference or action
- Building or updating long-term user profile across sessions

## Core Principle

When the user shares content, first classify it:

| If the content is... | Response |
|---|---|
| A reference document, link, or text pasted for discussion | **Mode A: Reference Protocol** — read and discuss, don't act |
| A chat export or conversation log for profiling | **Mode B: Active Profiling** — extract traits and save to memory |

When uncertain, default to **Mode A** and ask.

---

## Mode A: Reference Material Protocol

User pastes a document/file/link/reference block with no specific action request.

### Protocol

1. **Read fully** before responding — don't scan-and-react.
2. **Engage cognitively** — analyze, question, connect to known context, offer observations.
3. **Do NOT modify state** based on reference content alone. This includes:
   - Memory writes (profile or notes)
   - File system changes
   - Config/settings modifications
   - Tool or skill updates
4. **Do NOT take actions** unless the user explicitly asks. If uncertain, default to discussion.

### Delivery Preferences (this user)

- When the user says "paste the document" or "send the file" explicitly: send the **original file format** (.docx, .pptx, .pdf as-is), not a text extraction or commentary.
- When sending a file after inline discussion/analysis: send the version incorporating that discussion, not the raw original.
- Use `.txt` extension for file delivery (`.md` files may not open natively on mobile).
- **Code/command delivery:** When providing small sets of commands or code for the user to copy-paste, present them as bare code blocks with minimal surrounding explanation. If explanation is needed, place it after the code block — not before. The user will read the code first, then context. Trigger phrase: "just the raw text please" = strip all surrounding explanation, deliver only the code blocks.

### Pitfalls (Mode A)

- **"Here's a document" ≠ "Here's something to implement."** Context is reading material until the user says otherwise.
- **Don't conflate reference with prompt.** If they wanted action, they'd say so.
- **When in doubt, discuss.** The safest default is to say something about it, not do something to it.
- **Don't save corrections solely to memory and consider it done.** Style/format/workflow preferences belong in SKILL.md, not just memory entries.
- **Memory label trap:** Before repeating a label from memory about the user ("they use Monte Carlo"), verify it against what they actually say in the current conversation. If there's a mismatch between memory and their current statement, flag the discrepancy — don't assume memory is correct. Stale labels can propagate for sessions without correction because the user assumes you know what you're saying.

---

## Mode B: Active Profiling (Chat History → Memory)

User provides chat exports, share links, or long conversation logs for the purpose of building a user model.

### Workflow

1. **Receive** the chat history (via paste, file, or link).
2. **Extract high-signal facts**: preferences, recurring topics, communication style, domain interests, expectations.
3. **Save** using `memory` tool (add/replace durable entries — keep concise, under limit).
4. **Process in chunks** for long histories.
5. **Prioritize quality** — focus on patterns that affect future behavior, not raw data.

### Next Step: Soul Compression

After extracting traits from chat histories, consider loading the **soul-compression** skill to build a Type B (User Master Persona) soul:

1. User-profiling extracts raw traits and patterns from chat logs
2. Soul-compression packs those traits into a dense, structured soul (SOUL+Rubric+Loops+Guardrails)
3. The resulting soul can be further compressed to fit USER.md memory (≤1,375 chars)

This two-skill workflow produces a richer, more portable representation than memory entries alone.

### Handling Grok/X Data Exports

Grok full data exports are fragmented (hundreds of small binary/JSON files). They rarely contain clean chat history.
- **Preferred**: Ask user to provide share links or manually copied conversations.
- **If only full export available**: Extract and inspect a few content files to confirm they're mostly media/PDFs.
- **Fallback**: Manual copy-paste or share links are more effective for memory ingestion than processing the export directly.

See `references/grok-export-processing.md` for details.

### References

- `references/grok-export-processing.md` — handling fragmented X/Grok data exports
- `prompt-engineering/soul-compression/SKILL.md` — for building a User Master Persona soul
