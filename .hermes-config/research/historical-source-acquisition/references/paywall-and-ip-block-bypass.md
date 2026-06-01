# Paywall and IP Block Bypass Reference
**Status:** Partial working knowledge — no generic bypass exists. Only credential-bearing and service-specific paths work.

## Boring Reality Check (May 2026)
There is no universal "get past bot blocks" tool. What works depends on the target site, the block type, and whether the user has credentials/access. This file captures what actually works, what doesn't, and what requires user-supplied credentials.

## What DOES NOT Work (tested this session)
- Lightpanda fetch — bypasses basic bot detection for JS rendering, but NOT paywalls or IP blocks
- Jina AI reader (`r.jina.ai`) — extracts rendered text, but does NOT bypass auth/paywall gates
- Generic curl with different user-agents — blocked by Cloudflare, IP blocks, login walls
- Wayback Machine snapshots of paywalled sites — usually returns the interstitial, not the original content
- Invidious / Piped YouTube frontends — returns 403/502/526 from cloud IPs
- Semantic Scholar open-access filter — useful for discovery, but Luttwak had 0 open-access PDFs in corpus; Wickham had 1

## What WORKS (requires user-supplied credentials)

### YouTube Transcripts (cloud VPS blocked without cookies)
**Tool:** `youtube-content` skill + `yt-dlp`
**Required:** `cookies.txt` exported from user's logged-in YouTube browser session
**Command:**
```bash
yt-dlp --cookies /path/to/cookies.txt \
  --skip-download \
  --write-auto-subs \
  --sub-langs en \
  --convert-subs srt \
  -o "/tmp/yt_video" \
  'https://www.youtube.com/watch?v=VIDEO_ID'
```
**Risk:** YouTube may permanently ban the account used for cookie auth. Use a throwaway account.
**Fallback chain (documented in `youtube-content` skill):**
1. oEmbed API (title/channel only — no transcript)
2. `yt-dlp --cookies` (full transcript if cookies work)
3. web_search on video title + channel (often surfaces summaries/transcripts others posted)
4. Browser subagent with `browser` toolset (expensive: 3-5 min, 30+ tool calls; still can't bypass sign-in wall)

### Foreign Affairs / Paywalled Journalism
**No working bypass from cloud VPS without credentials.**
Options:
1. User provides login credentials (cookie-based auth)
2. User provides institutional access (university VPN/library proxy)
3. Search for the article title + author — often surfaces reposts, PDFs on author's site, or summaries

### JSTOR / Academic Journals
**No working bypass from cloud VPS without credentials.**
Options:
1. User's institutional access via VPN
2. Semantic Scholar discovery (find papers, check `openAccessPdf` field)
3. DOI lookup → check Unpaywall API: `https://api.unpaywall.org/v2/10.xxxx/xxxx?email=user@example.com`
4. Author's personal site / ResearchGate / Academia.edu (often has preprints)

### C-SPAN Transcripts
**Cloud VPS IP blocked for transcript endpoints.**
Options:
1. User provides C-SPAN account (free registration sometimes works)
2. Web search for "C-SPAN [speaker] [date] transcript" — third-party sites often repost
3. Contact C-SPAN directly for educational use

### Personal/Academic Sites (luttwak.com, hoover.org)
**luttwak.com:** Returns 45 bytes — site is effectively down
**hoover.org:** Profile pages return 404 for some researchers
**Options:**
1. Wayback Machine (often returns interstitial, not content)
2. Web search for "[name] site:[domain]" — cached copies, PDFs hosted elsewhere
3. Search for author name + "CV" or "publications" — academic CVs are often publicly posted

## What ACTUALLY Works (no credentials needed)

### Semantic Scholar (Open Access Discovery)
**Endpoint:** `https://api.semanticscholar.org/graph/v1/`
**No key required.** Returns author search, paper lists, abstracts, and `openAccessPdf` URLs.
**Limitations:**
- Coverage varies by field/historical period
- Many older/historical works have no open-access PDF
- Rate-limited (bursty, but works for manual queries)

### OpenLibrary / Wikipedia APIs
**Endpoint:** `https://openlibrary.org/search.json?q=...`
**No key required.** Bibliographic metadata only, not full text.
**Use case:** Verify edition details, find ISBNs, discover alternate titles

### AbeBooks / Used Book Market
**Endpoint:** `https://www.abebooks.fr/servlet/SearchResults?tn=<TITLE>&an=<AUTHOR>`
**No key required.** Parseable via curl. Shows used physical copies.
**Use case:** Last resort for out-of-print/copyrighted books

### YouTube oEmbed (Metadata Only)
**Endpoint:** `https://www.youtube.com/oembed?url=<VIDEO_URL>&format=json`
**No key required.** Returns title, author_name, author_url only. No transcript, no description.
**Use case:** Confirm video exists, get canonical title for web search

## Decision Tree for Blocked Sources

```
Need [target]?
├── YouTube transcript?
│   ├── User has cookies.txt → yt-dlp --cookies
│   ├── No cookies → web_search title + channel
│   └── Still nothing → oEmbed (title only) + mark source as unverified
├── Paywalled article (FA, C-SPAN, JSTOR)?
│   ├── User has institutional access → use their VPN/proxy
│   ├── No access → web_search for title + "pdf" or "full text"
│   └── Author has personal site → search [author name] publications
├── Dead personal site (luttwak.com, etc.)?
│   ├── Wayback → usually returns interstitial
│   ├── Web search [site:domain] → cached copies
│   └── Search for "[author] CV" or "[author] publications list"
├── Academic paper?
│   ├── Semantic Scholar → check openAccessPdf
│   ├── DOI → Unpaywall API
│   └── Author's ResearchGate/Academia.edu (often has preprints)
└── Book already on disk?
    └── Read it directly — no fetch needed
```

## Session-Specific Findings (2026-06-01)

### Luttwak
- **luttwak.com:** 45 bytes, effectively down
- **Hoover Institution:** Profile 404
- **AEI:** 500-byte stub
- **CSIS Strategy and Statecraft:** 33 KB program page, no Luttwak-specific publication list
- **C-SPAN:** IP-blocked stubs (335–372 bytes)
- **Foreign Affairs:** Paywalled, 404 via Jina
- **JSTOR:** 39 KB search shell, no article text
- **CFR:** Next.js 404
- **Hudson Institute:** 404
- **Wayback 2025:** Archive.org interstitial, no original content
- **YouTube:** Cloud VPS IP blocked; 5 videos confirmed via oEmbed; no transcript accessible
- **Semantic Scholar:** 143 papers listed; 0 open-access PDFs for Luttwak-relevant titles

### Wickham
- **Oxford faculty page:** **Genuine self-description retrieved** (12 KB Lightpanda, 18 KB Jina)
  - Key quote: "I am using archaeology, legal documents and letters, to try to get at how regional exchange fits together with long-distance exchange. Here my aim is to figure out, not only how the Mediterranean economy worked in this period, but also how the logic(s) of pre-capitalist economic systems operated on the ground."
  - Status: `partial-verified` — one real source, but not enough to verify the full skill
- **Academia.edu:** 532-byte stub
- **Warwick:** 404
- **Oxford podcasts:** Lecture series listing, no Wickham-specific content
- **Semantic Scholar:** 153 papers; 1 open-access PDF found (*The Power of Property: Land Tenure in Fāṭimid Egypt*, 2019)

## Lessons Learned

1. **No generic paywall bypass exists.** Every "bypass" requires credentials the user must provide. Don't theatrical-fetch dead endpoints.
2. **Wayback Machine is not a bypass tool.** It returns the archive interstitial, not the original content, for most paywalled sites.
3. **Semantic Scholar is the best no-credential discovery tool** for academic papers — use it before burning cycles on dead personal sites.
4. **YouTube from cloud VPS is functionally unusable without cookies.** The `youtube-content` skill documents this; follow its fallback chain.
5. **"Find ways around it" ≠ infinite retries on dead endpoints.** The correct response is: try the Tier 0.5 APIs, try credential-bearing paths, THEN tell the user what access they need to supply.
6. **Oxford/Cambridge faculty pages are often gold mines** — self-written bios with explicit methodological statements, freely accessible.
