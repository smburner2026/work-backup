# Pi + OpenCode Go

Concrete configuration for using Pi with an OpenCode Go subscription. OpenCode Go provides open-weight models (DeepSeek, GLM-5, Kimi K2.5, MiniMax M2.5) at a flat $10/month subscription via an OpenAI-compatible endpoint.

## models.json

Location: `~/.pi/agent/models.json`

```json
{
  "providers": {
    "opencode-go": {
      "baseUrl": "https://opencode.ai/zen/go/v1",
      "api": "openai-completions",
      "apiKey": "OPENCODE_GO_API_KEY",
      "authHeader": true,
      "models": [
        {
          "id": "deepseek-v4-flash",
          "name": "DeepSeek V4 Flash (OpenCode Go)",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 128000,
          "maxTokens": 16384
        }
      ]
    }
  }
}
```

## Selecting the Model

```bash
pi -p "Write a Pine Script v6 RSI indicator" --model opencode-go/deepseek-v4-flash
```

## API Key Resolution

If `OPENCODE_GO_API_KEY` is set in `~/.hermes/.env` but NOT exported (common with Hermes setups where the var is read internally but not exported to the shell), use the shell-command format instead of the env-var-name format:

```json
"apiKey": "!grep '^OPENCODE_GO_API_KEY=*** /path/to/.env | head -1 | cut -d= -f2"
```

The `!grep ...` command runs at request time, so a re-sourced `.env` is picked up immediately without restarting Pi. Key details:

- The grep pattern `'^OPENCODE_GO_API_KEY=*** is anchored to line start with `^` — this skips comment lines like `# OPENCODE_GO_API_KEY=*** `head -1` ensures only the first matching line is used
- `cut -d= -f2` extracts everything after the first `=`
- **Do NOT include the key value in the grep pattern** — just `'^OPENCODE_GO_API_KEY=*** with nothing after the `=`. Including the value causes failures when the file is transferred between machines (the value gets redacted during scp/terminal output, baking literal `***` into the pattern).

### Cross-Machine Config Copy

When copying `~/.pi/agent/models.json` between machines (e.g. VPS → local WSL):

1. **Fix the `.env` path** — VPS uses `/root/.hermes/.env`, local WSL uses `/home/<user>/.hermes/.env`
2. **Verify the `apiKey` line** — if the transfer redacted the key value into `***` in the pattern, the grep won't match. The correct pattern has nothing after `=`:
   ```
   "apiKey": "!grep '^OPENCODE_GO_API_KEY=*** /correct/path/.env | head -1 | cut -d= -f2"
   ```
- **Do NOT include the literal characters `***` in the grep pattern** — those are Hermes' terminal redaction, not the actual file content. The correct grep is just `^OPENCODE_GO_API_KEY=` with nothing after the `=`.

## Smoke Test

```bash
pi -p "Respond with exactly: PI_OPENCODE_OK" --model opencode-go/deepseek-v4-flash
# Expected: PI_OPENCODE_OK
```

## Known Models (OpenCode Go)

- `deepseek-v4-flash` -- default, fast coding
- Check `https://opencode.ai/zen/go/v1/models` for full list
