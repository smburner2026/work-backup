# Hermes Context Architecture: What Goes Where

Hermes has four persistence layers. Choosing the right one prevents stale data and context pollution.

## The Four Layers

### 1. AGENTS.md / CLAUDE.md / .cursorrules — Project-Scoped State
**Lives in:** the project directory (`/home/vthen/work/<project>/AGENTS.md`)  
**Loaded when:** session runs from that directory (or via cron `workdir`)  
**Purpose:** Project-specific facts that are true while the project exists and irrelevant outside it.

- Exam dates, syllabus, scoring rubrics
- Project conventions, file paths, naming schemes
- Active PR numbers, current sprint goals (ephemeral but project-scoped)
- Topic mastery tables, session histories within a study program
- Reference library paths, database schemas

**Anti-pattern:** Putting project-specific state in user profile memory. The DABT exam date doesn't define who the user is — it's a temporary project goal. When the project ends, the AGENTS.md gets archived with it; user profile memory would need manual pruning.

### 2. User Profile Memory — Enduring Personal Traits
**Lives in:** `memory` tool with `target='user'`  
**Loaded when:** every turn, injected into system prompt  
**Purpose:** Facts about the person that hold across projects and time.

- Name, background, domain expertise
- Communication preferences, intellectual register
- Work style (brainstorm-first, methodical, etc.)
- Pet peeves, anti-patterns to avoid
- Typing quirks, accessibility needs

**Anti-pattern:** Project artifacts (PR numbers, commit SHAs, exam scores, session counts). These rot in days. Also avoid: instructions to yourself ("Always run tests with -n 4") — those belong in skills.

### 3. Skill Memory — Reusable Procedural Knowledge
**Lives in:** `~/.hermes/skills/` (skill_manage tool)  
**Loaded when:** requested via skill_view or --skills flag  
**Purpose:** How to do a class of task — steps, commands, pitfalls, verification.

- Workflows that succeeded after 5+ tool calls
- Error-fix recipes for recurring problems
- Tool-specific commands and flags
- Provider quirks, API oddities

**Skill vs Memory:** Skills encode *how* — the procedure. Memory encodes *who* and *what state*. If a fact will be stale in a week, it does not belong in memory. If it's a procedure you'll reuse, make it a skill.

### 4. Conversation Transcripts — Searchable Past
**Lives in:** `~/.hermes/sessions/` (session_search tool)  
**Purpose:** Record of what happened. Queryable but not injected.

- Task progress and completed-work logs
- Debugging transcripts
- Decisions made and their rationale

## Decision Heuristic

| The fact... | Belongs in... |
|-------------|---------------|
| Will still matter in 6 months, defines the person | User profile memory |
| Matters only within this project, expires when project ends | AGENTS.md |
| Is a procedure I'd repeat on a similar task | Skill |
| Records what happened in a past session | Conversation transcript (searchable) |
| Will be stale in < 1 week | Do NOT save — let it be re-discovered |

## Migration Pattern (from this session)

**Before:** DABT exam date, topic mastery, session scores, reference library paths all in user profile memory — polluting the global namespace with project-specific state.

**After:** All DABT state moved to `/home/vthen/work/dabt-tutor/AGENTS.md`. User profile reduced to: bioscience background, CLI-only, Nietzsche/philosophy, communication register, work methodology, typo handling. Result: 42% memory utilization (was 91%), clean separation.

**Trigger:** When user profile memory exceeds ~80% and contains project-specific entries, propose this migration. Don't wait for the user to suggest it.
