# Prompt Compression Techniques for Hermes Souls

These four techniques were observed in highly optimized Hermes SOUL.md files to reduce token usage while preserving meaning and structure.

## 1. Structural Compression
- Convert verbose chain descriptions into named state-machine blocks.
- Example: Long repeated agent process descriptions → `[AGENT_LOOP]` and `[LEARN_LOOP]` blocks.
- Benefit: The model can reference the block by name instead of re-reading full logic.

## 2. Token Packing
- Use dense notation instead of verbose syntax.
- `a.b.c` → `{a,b,c}`
- Long phrases replaced with short canonical primitives (`CheckCtx`, `MapTools`, `ParseIntent`).
- Reduces token count per instruction.

## 3. Semantic Normalization
- Collapse repeated concepts into short labels.
- "self-improving persistent agent that compounds capability" → `SelfImprove`, `CompoundLearning`.
- Group related systems into modules (`MEMORY_SYS`, `SKILL_SYS`, `EXEC_ENV`).
- Eliminates redundant phrasing.

## 4. DSL Encoding
- Replace arrow-heavy chain notation with assignment-style syntax.
- Use `=` and `{}` forms instead of long `→` sequences.
- Significantly reduces delimiter tokens (arrows, dashes, parentheses).
- Turns the prompt into a more code-like, compact representation.

These techniques are especially valuable when maintaining large, persistent system prompts like SOUL.md that must stay under context limits.