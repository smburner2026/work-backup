---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.

   ⚠️ **Cloud VPS caveat:** If running from a cloud server (AWS, GCP, Azure, Hetzner, etc.), `youtube-transcript-api` and `yt-dlp` will likely fail with "IP blocked" errors. YouTube blocks most cloud provider IP ranges. If the script fails, skip directly to the **Cloud VPS / IP-Blocked Environments** section below — do not retry, do not suggest the user enable captions.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

## Error Handling

- **IP blocked / "Sign in to confirm you're not a bot"**: happens from cloud VPS IPs. Do NOT retry the script. Jump to the **Cloud VPS / IP-Blocked Environments** section and follow the fallback chain (oEmbed → web_search → browser subagent). This is the most common failure mode from Hermes' infrastructure.
- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.

## Cloud VPS / IP-Blocked Environments

YouTube blocks most cloud provider IP ranges. The `youtube-transcript-api` and `yt-dlp` (without browser cookies) will fail from cloud VPS (AWS, GCP, Azure, Hetzner, etc.) with "Sign in to confirm you're not a bot" or "IP blocked" errors.

### Fallback Chain (in order)

1. **oEmbed API** — always works, even from blocked IPs. Gives you title, author, channel URL, thumbnail:
   ```
   https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json
   ```
   Use as a Python `requests.get()` or `web_extract`. Parse the JSON for `title`, `author_name`, `author_url`.

2. **web_search** on the video title + channel — can surface blog posts, Reddit discussions, or articles covering the video. Use when you need context beyond the title.

3. **web_search** on the channel name — the channel's description and focus area provide framing even without the specific video transcript.

4. **yt-dlp with cookies** — if a cookie file from a logged-in YouTube session is available:
   ```bash
   yt-dlp --cookies /path/to/cookies.txt --skip-download --write-auto-subs --sub-langs en -o "/tmp/yt_video" 'VIDEO_URL'
   ```
   Cookie export guide: see `references/ip-block-workarounds.md`.

5. **Browser subagent** — spawn a delegate_task with `browser` toolset to render the YouTube page with full JavaScript. Gets description, channel stats, timestamps, and any JS-rendered metadata. Won't bypass the transcript sign-in wall but gives richer extraction than oEmbed. Expensive (3-5 min, 30+ calls). See `references/ip-block-workarounds.md` for exact call pattern.

6. **Infer from public sources** — when all extraction fails, work from what you have: title, channel, channel focus, and domain knowledge. State clearly what you confirmed vs. inferred. A structured summary with explicit "confirmed" and "inferred" sections is honest and useful.

📁 See `references/ip-block-workarounds.md` for details on each method, including cookie setup and alternative YouTube frontend API instances.
