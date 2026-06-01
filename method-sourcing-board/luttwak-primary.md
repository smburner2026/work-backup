# Luttwak — Primary Source Acquisition Log
**Status:** `unverified-draft`
**Date:** 2026-06-01

## Verified: what was checked and what it actually returned

| Source | URL / API | Result |
|--------|-----------|--------|
| luttwak.com | Top-level fetch | 45 bytes — site appears down/empty |
| Hoover Institution profile | https://www.hoover.org/profiles/edward-luttwak | HTML shell only; no biography text retrieved |
| AEI scholar page | https://www.aei.org/scholar/edward-luttwak | 500 bytes — stub/redirect |
| CSIS Strategy and Statecraft | https://www.csis.org/programs/strategy-and-statecraft | 33 KB program page; no Luttwak-specific publication list |
| C-SPAN | https://www.c-span.org/video/?300852-1 | 356–372 bytes — stub |
| C-SPAN author list | https://www.c-span.org/person/edward.luttwak/ | 335 bytes — stub |
| Foreign Affairs (full paywall) | /reviews/capsule-history/strategic-dimension-history | Paywall + 404 via Jina |
| JSTOR search | /action/doSearch?AllField=Edward+Luttwak+strategy | 39 KB search shell; no article text |
| Wilson Center | /people/edward-luttwak | 61 KB HTML shell |
| CFR expert page | /expert/edward-luttwak | Next.js 404 |
| Hudson Institute | /experts/edward-luttwak | 404 |
| Wayback 2025 snapshot | https://web.archive.org/web/20250712145326/https://www.luttwak.com | Archive.org interstitial; no original content |
| YouTube transcripts | bq03uz-TwU4, GYCHXQ4zFcA, W5XlACFoe88, xLJyEe_Ynxk, okatgIu_NzE | Cloud VPS IP blocked; oEmbed gives title/channel only |
| Semantic Scholar author API | authorId 89362233 | 143 papers listed; link fields present but 0 open-access PDFs for Luttwak-relevant titles |

## Confirmed sources (real content, but not Luttwak’s own words about method)

- YouTube videos confirmed to exist (oEmbed):
  - *Conversations with History: Edward Luttwak* (UCTV)
  - *2012 – Master Class: Thinking Strategically* (PresidentialConf, Israeli Presidential Conference)
  - *Grand Strategy of the Byzantine Empire* by Edward Luttwak (historyscientist)
  - *Postkahanism Podcast Episode 7 – Dr. Edward Luttwak* (Boris Kogan)
  - *The Balance of Power, Tariffs, & Future of the American Dream* (Geopolitics & Empire)

## Abstraction surface for Luttwak

- 0 direct quotes / passages bound to source
- 0 short-form primary texts acquired
- 0 paywalls bypassed
- 5 nonfiction videos confirmed to exist but no transcript accessible from this IP
- Existing skill (`luttwak-strategic-analysis`) remains `unverified-draft`

## What would actually work (blockers requiring user intervention)

1. **YouTube transcripts** — need cookies.txt from a personal YouTube session in this VPS; `yt-dlp --cookies` is the documented fallback in `youtube-content` skill
2. **Foreign Affairs / C-SPAN** — need account credentials; transcript endpoints require login
3. **Semantic Scholar** — author index works, but Luttwak has zero open-access PDFs in this corpus; full-text still needs institutional access
4. **Academia.edu / JSTOR / Oxford** — all restricted from this IP

## Next action

Defer to Kanban task `tsk-bhxjon9pwf`. Do not further characterize Luttwak’s method from training knowledge until a primary source is actually in hand.
