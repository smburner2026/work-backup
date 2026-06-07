# Hermes Resolver — Full Reference

Complete routing table for all Hermes skills.
Loaded via `skill_view(name='hermes-resolver', file_path='references/resolver.md')`.

## Quick Index by User Intent

| When user says... | Load skill/tool |
|---|---|
| drill / practice / MCQ / exam | `dabt-drill-mode` |
| explain / understand / why | `dabt-deep-dive` |
| look up / search / check reference | `dabt-reference` → mcp_gbrain_query |
| consolidate / compare topics | `dabt-synthesis-review` |
| post to X / Twitter | `xurl` |
| diagram / draw / architecture | `excalidraw` or `architecture-diagram` |
| light / hue / philips | `openhue` |
| invest / prediction / polymarket | `polymarket` |
| paper / arxiv / research | `arxiv` |
| flashcard / memento / memorize | `memento-flashcards` |
| translate / nolte / german | `document-translation` |
| spotify / music / song | `spotify` |
| youtube / transcript / video | `youtube-content` |
| GIF / reaction | `gif-search` |
| website / scrape / extract | `lightpanda-batch-scraping` or `web_extract` |
| compose / book / document | `book-pdf-compilation` or `document-pipelines` |
| substack / newsletter | `substack-paywall-export` or `substack-pdf-export` |
| chart / trading / pinescript | `pinescript-indicator-dev` |
| swing / BAMBAM / fatcat | `swingcatcher` |
| model / ML / training | `huggingface-hub` or `llama-cpp` or `dspy` |
| git / GitHub / PR | `github-*` skills |
| debug / test / TDD | `systematic-debugging` or `test-driven-development` |
| fix / bug / investigate | `systematic-debugging` |
| password / bitwarden / secret | `secrets-management` |
| Jupyter / notebook / Python | `jupyter-live-kernel` |
| image / gen / stable diffusion | `comfyui` |
| video / animation / manim | `manim-video` |
| ASCII / puns / text art | `ascii-art` or `ascii-video` |
| design / mockup / UI | `sketch` or `claude-design` |
| plan / outline / approach | `writing-plans` or `plan` |
| wallpaper / background | `autonomous-ai-agents` → delegate |
| kanban / board / task | `kanban-orchestrator` or `kanban-worker` |
| Euphy / daily / journal | `euphy-personal-journal` or `euphy-bullet-journal` |
| Mike / tutor / Socrates | DABT tutor mode |

## Skills Not Yet Categorized

The following skills exist but have no dedicated domain section yet.
They are fully functional — load with `skill_view(name='<name>')` when
their description matches the task.

- `ai-tutor`, `audiocraft-audio-generation`, `baoyu-*-*`, `batch-data-enrichment`
- `claude-code`, `claude-design`, `codebase-inspection`
- `codex`, `comfyui`, `dabt-*-*` (covered above in DABT section)
- `debugging-hermes-tui-commands`, `design-md`, `discord-bot-windows-setup`
- `document-translation-pipeline`, `dogfood`, `eikon`, `eikon-create`
- `engineering-discipline`, `git-memory-layer`, `git-secret-remediation`
- `github-auth`, `github-repo-management`, `godmode`, `google-workspace`
- `heartmula`, `hermes-agent-skill-authoring`, `hermes-environment-sync`
- `hermes-plugins`, `hermes-s6-container-supervision`, `hermes-soul-design`
- `humanizer`, `ideation`, `kanban-codex-lane`, `kanban-editorial-pipeline`
- `linear`, `maps`, `minecraft-modpack-server`, `nano-pdf`, `native-mcp`
- `node-inspect-debugger`, `obliteratus`, `ocr-and-documents`, `opencode`
- `orchestration-workflow`, `personal-workspace`, `pi`, `pokemon-player`
- `powerpoint`, `pretext`, `profile-compression`, `project-outcome-chaining`
- `python-debugpy`, `python-desktop-app-optimization`, `requesting-code-review`
- `research-paper-writing`, `segment-anything-model`, `serving-llms-vllm`
- `songsee`, `songwriting-and-ai-music`, `spike`, `subagent-driven-development`
- `teams-meeting-pipeline`, `terminal-io-debugging`, `tool-evaluation`
- `touchdesigner-mcp`, `user-content-handling`, `valledin-translation`
- `webhook-subscriptions`, `yuanbao`

## Disambiguation Rules

1. **Prefer the most specific match** — `dabt-drill-mode` over generic `dabt-database` for exam practice
2. **Content type routing** — If the user shares a URL → `web_extract` or browser tool; if a YouTube URL → `youtube-content`
3. **Consult always-hot memory first** — Key triggers (Euphy, Mike) and core references (G-Brain for DABT) are in MEMORY
4. **When in doubt, ask** — If 2+ skills could match equally, a 1-turn clarification prevents wrong execution
5. **Chain when phases say so** — Some skills explicitly chain (e.g. enrich → import → embed)
