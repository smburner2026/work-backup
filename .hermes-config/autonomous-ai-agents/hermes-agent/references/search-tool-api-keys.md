# Search Tool API Key Setup

Hermes shows API keys like Tavily and Browserbase in `hermes config` output
(e.g. `Tavily         (not set)`), but these are backed by flat environment
variables, not config-yaml keys.

## The Pitfall

```bash
# THIS CRASHES:
hermes config set search.tavily_api_key <key>
```

Error:

```
ValueError: Invalid environment variable name: 'SEARCH.TAVILY_API_KEY'
```

`hermes config set` internally uppercases the dotted key and tries to
write it to `.env` as-is (dots and all), which gets rejected because env
var names cannot contain dots.

## The Fix

Add the plain env var to `~/.hermes/.env`:

```bash
echo 'TAVILY_API_KEY=tvly-xxxxx' >> ~/.hermes/.env
```

Or edit `.env` directly at the path given by `hermes config env-path`.

## Verification

```bash
hermes config | grep -i tavily    # should show masked value, not "(not set)"
hermes doctor                     # check dependencies and config
```

Then `/reset` or start a new session to activate the web/search tool.