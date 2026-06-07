# Nous Portal Billing Disambiguation

**Observed:** `stepfun/step-3.7-flash:free` returns `"pricing":{"prompt":"0","completion":"0"}` via the Nous Portal models endpoint. The API does not bill for inference on free-tier models.

This document captures why a user on a free model may still see charges, and how to diagnose the source.

## The split: inference vs. infrastructure

Nous Portal bundles free inference with **managed services** that are tracked separately:

| Service | Toolset | Billing signal |
|---|---|---|
| Browser automation | browser | Browserbase session minutes |
| TTS | tts | OpenRouter / ElevenLabs / edge char counts |
| Image generation | image_gen | FAL backend generations |
| Web extraction (Firecrawl) | web | Firecrawl crawl / scrape units |
| Web search (Tavily, etc.) | web/search | Third-party search provider queries |
| Modal execution | execute_code | Modal runtime hours |

None of these show up in the model's pricing block. They are tracked by the respective backend provider.

## Quick charge-localization checklist

1. Check hermes status --all — which managed tools are marked active?
2. Check recent tool call volume: hermes insights --days 1 — high browser/web counts point there.
3. Check whether the Nous Portal UI exposes per-service breakdown (browser, TTS, image, Firecrawl).
4. env | grep -iE 'BROWSER|FAL|TAVILY|EDGE|ELEVEN' — an injected key means that service is wired up.

## Cost controls

- Disable tool authentication keys in ~/.hermes/.env to disable a managed service.
- hermes tools disable browser / hermes tools disable image_gen to remove tool access.
- Avoid text_to_speech, image_generate, and browser_* calls on free-tier plans unless confirmed unlimited.

## Why the confusion happens

The parent chat model is stepfun/step-3.7-flash:free with $0 pricing. Subagents, web hooks, and non-inference tools have independent billing paths. A single delegate_task call appears free; a single browser_navigate call may not.

The appearance of a charge for "non-inference" almost always means one of the managed services above — not the LLM API.
