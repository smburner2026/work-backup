---
title: MEMORY.md Compression Worked Example
version: 1.0
date: 2026-05-18
description: Before/after of compressing Hermes's MEMORY.md into soul-compression DSL flat blocks. Achieved 42% reduction (2,140→1,246 chars).
---

# MEMORY.md Compression: Worked Example

## Source material

The original MEMORY.md contained 10 §-delimited prose paragraphs of operational/environmental facts — IP addresses, project paths, repo names, Discord channel IDs, tool preferences, persona triggers, timezone info, and a user correction about skill-suggestion etiquette.

## Compression techniques applied

| Technique | Application |
|---|---|
| **Structural** | 11 domain-labeled blocks (WORKDIR, DABT, TRIGGERS, VALLENTIN, OCR, DISCORD, NIETZSCHE, TZ, GIT, RULE — VPS merged into WORKDIR). Flat layout. |
| **Semantic** | All-caps single-word labels. Consistent punctuation: colon after label, comma between properties, period at block end. |
| **Token packing** | `35ch` for "35 chapters", `9.9M` for "9.9 MB", `→` for arrows/went-to, `|` for OR-list, `/` for compound alternatives, `()` for inline qualifiers like IP suffix, `+` for accumulative lists. |
| **DSL** | `Label: val1, val2, val3→result.` format throughout. No prose transitions, no copula avoidance, no "there is / there are." |

## Before (2,140 chars, 10 blocks)

```
Global work directory: /root/work for all file operations, database creation, scripts,
and output files on the VPS.
§
DABT reference library extracted: 35 C&D chapters (9.9 MB) + 39 Hayes chapters (11 MB)
+ 29 regulations (4.2 MB) in reference/extracted/. Each source has index.json.
Skills: dabt-reference (3-pass search), dabt-drill-mode, dabt-deep-dive, dabt-database.
Launch: hermes -w /home/vthen/work/dabt-tutor -s dabt-drill-mode (or dabt-deep-dive).
dabt-database and dabt-reference load automatically as dependencies.
§
TempMoon: "Euphy" → Euphy persona (soft feminine subordinate). "Mike" → Mike DABT tutor
(Socratic data-first, from dabt-deep-dive). Triggers: euphy-trigger, mike-trigger skills.
§
Vallentin Napoleon translation at /root/work/vallentin-clean4/ — 182K words, 36 chapters.
Committed to GitHub work-backup repo. Style guide exists in project zip. Use session_search
for editorial details.
§
VPS IP: 178.156.199.37. Windows/WSL, home /home/vthen/. rsync pull for transfers.
OCR fpdf2: use pdf.write() not multi_cell for >50K chars (avoids x-drift, state
corruption, chunk artifacts).
§
Discord: #general (home), #secretary-agent (bullet journal), #researcher-agent, #outputs.
Euphy: input=1505617142991556710, output=1505617307639218197. Cron uses opencode-go.
User likes high-density SOULs.
§
Nietzsche discussion: remain neutral on controversial views (misogyny, aristocracy, etc.).
No apologies, no moral signalling, no approval/disapproval. Comment on structure and
rhetoric only. Trust user's relationship with text.
§
TempMoon is in US Central Time (currently CDT, UTC-5). Cron job times should be expressed
in CT.
§
GitHub: smburner2026, free plan. Classic PAT in git-credential store. Repo: work-backup
(backup of /root/work/). gh v2.92 installed, not authed (missing read:org).
credential-store unreliable — embed token in remote URL.
§
Before suggesting skill installations or making recommendations, always check
`hermes skills list` first to see what's already installed. Cross-reference before
offering. Randoooos found it irritating when I suggested skills that were already
installed.
```

## After (1,246 chars, 11 labeled blocks)

```
WORKDIR: /root/work(VPS). WSL=/home/vthen/. rsync pull.
VPS: 178.156.199.37

DABT: C&D(35ch,9.9M)+Hayes(39ch,11M)+Regs(29,4.2M)→reference/extracted/. Skills: dabt-reference|drill|deep-dive|database. Launch: hermes -w /home/vthen/work/dabt-tutor -s dabt-drill-mode/deep-dive. db+ref auto-deps.

TRIGGERS: "Euphy"→euphy-secretary(girly). "Mike"→mike-dabt-tutor(Socratic data-first). Skills: euphy-trigger|mike-trigger.

VALLENTIN: /root/work/vallentin-clean4/—182Kwd,36ch. GitHub work-backup. Style guide in zip. session_search for editorial.

OCR(fpdf2): pdf.write() not multi_cell for >50K chars(vs x-drift/chunk-error).

DISCORD: #general(home), #secretary-agent(bullet-j), #researcher-agent, #outputs. Euphy: in=1505617142991556710, out=1505617307639218197. Cron→opencode-go. User likes dense SOULs.

NIETZSCHE: Neutral on controversy. No apology/approval/moral-signal. Structure+rhetoric only. Trust user's text-relationship.

TZ: TempMoon US Central(CDT, UTC-5). Cron→CT.

GIT: smburner2026(free). PAT in credential-store. Repo: work-backup(/root/work/). gh v2.92 unauthed(no read:org). credential-store unreliable→embed token in URL.

RULE: Check `hermes skills list` first before suggesting installs. Randoooos hates repeats.
```

## What each compression decision achieved

| Original phrase | Compressed | Technique | Chars saved |
|---|---|---|---|
| `for all file operations, database creation, scripts, and output files on the VPS` | `(VPS)` | Redundancy drop — label implies scope | ~90 |
| `35 C&D chapters (9.9 MB) + 39 Hayes chapters (11 MB) + 29 regulations (4.2 MB) in reference/extracted/` | `C&D(35ch,9.9M)+Hayes(39ch,11M)+Regs(29,4.2M)→reference/extracted/` | Token packing + DSL arrow | ~60 |
| `soft feminine subordinate` | `girly` | Token packing | ~20 |
| `Socratic data-first, from dabt-deep-dive` | `Socratic data-first` | Redundancy drop — source is implicit | ~20 |
| `Committed to GitHub work-backup repo. Style guide exists in project zip.` | `GitHub work-backup. Style guide in zip.` | Copula removal | ~15 |
| `avoids x-drift, state corruption, chunk artifacts` | `vs x-drift/chunk-error` | Token packing + `/` | ~35 |
| `bullet journal` | `bullet-j` | Token packing | ~10 |
| `Cron uses opencode-go` | `Cron→opencode-go` | DSL arrow | ~5 |
| `User likes high-density SOULs` | `User likes dense SOULs` | Semantic normalization | ~5 |
| `remain neutral on controversial views (misogyny, aristocracy, etc.)` | `Neutral on controversy` | Token packing | ~30 |
| `TempMoon is in US Central Time (currently CDT, UTC-5). Cron job times should be expressed in CT.` | `TZ: TempMoon US Central(CDT, UTC-5). Cron→CT.` | Label + token packing | ~30 |
| `credential-store unreliable — embed token in remote URL.` | `credential-store unreliable→embed token in URL.` | DSL arrow + redundancy drop | ~15 |
| `Before suggesting skill installations or making recommendations, always check... Cross-reference before offering. Randoooos found it irritating when I suggested skills that were already installed.` | `Check \`hermes skills list\` first before suggesting installs. Randoooos hates repeats.` | Drop to imperative + token pack | ~60 |

## Total savings: ~894 chars (42%)

## When to use this pattern

Apply MEMORY.md compression when:
- The file exceeds 60% of its 2,200-char budget
- A new fact needs adding and there's no room
- Individual entries have drifted into prose paragraphs with redundant transitions
- The file has accumulated § signs that no longer serve a structural purpose (labels replace them)

Do NOT compress when the user explicitly prefers readable prose over density, or when the MEMORY.md is still under 50% capacity and stable.
