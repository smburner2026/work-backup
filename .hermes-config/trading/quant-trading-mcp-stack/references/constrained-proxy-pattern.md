# Constrained MCP Proxy Pattern

## Why This Exists

Some APIs expose tools that are too powerful for an AI agent to have unfettered access to — sell buttons, delete operations, money-moving endpoints. Config-level whitelisting (`tools: { include: [...] }`) is fragile: it can be overridden by editing config.yaml, prompt injection, or tool registry manipulation.

A **code-level proxy** is stronger because the dangerous functions literally don't exist in the process's code.

## Architecture

```
AI Agent → (stdio) → Proxy MCP server → (HTTP/stdio) → Upstream API
                        ↑
                CONSTITUTIONAL ENFORCEMENT
                - No sell/close/cancel functions
                - Parameter sanitization
                - Portfolio sum validation
                - Read-only tools are true read-only
```

## When to Use

- The upstream API exposes destructive tools (close, delete, transfer)
- The agent only needs a subset of the API's capabilities
- The constraint needs to survive prompt injection attempts
- You want the constraint enforced at the process boundary, not config

## Implementation Template (FastMCP)

```python
#!/usr/bin/env python3
"""
Proxy MCP server that constrains an upstream API.
Only safe tools are exposed. Dangerous tools do not exist in this process.
"""
import os
from typing import Any
from mcp.server.fastmcp import FastMCP

# ── Setup ─────────────────────────────────────────────────────────────────
UPSTREAM_URL = os.environ.get("UPSTREAM_URL")
API_KEY = os.environ.get("API_KEY", "")
API_SECRET = os.environ.get("API_SECRET", "")

mcp = FastMCP("constrained-proxy")

def _check_configured() -> None:
    """Refuse to serve if credentials are missing."""
    if not API_KEY:
        raise RuntimeError("API_KEY not configured. Add to environment variables.")

async def _call_upstream(tool: str, args: dict) -> dict:
    """Bridge call to upstream MCP over HTTP. Only this function touches the upstream."""
    import httpx
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": tool, "arguments": args}}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(UPSTREAM_URL, json=payload, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        })
        resp.raise_for_status()
        result = resp.json()
    # Parse MCP response content
    text_parts = [c.get("text","") for c in result.get("result",{}).get("content",[])
                  if c.get("type") == "text"]
    try:
        import json
        return json.loads("\n".join(text_parts))
    except (json.JSONDecodeError, TypeError):
        return {"result": "\n".join(text_parts)}

# ── SAFE TOOLS ONLY ───────────────────────────────────────────────────────
# CONSTITUTIONAL: No close/sell/delete/transfer functions exist in this file.
# Adding a new tool requires manual code review.

@mcp.tool()
async def read_positions() -> dict[str, Any]:
    """
    Get all open positions. Read-only — no trading side effects.
    """
    _check_configured()
    return await _call_upstream("get_positions", {})

@mcp.tool()
async def update_take_profit(
    position_id: str,
    price: float,
    portfolio: float = 1.0,
) -> dict[str, Any]:
    """
    Update the take profit level on an existing position.
    
    CONSTITUTIONAL CONSTRAINT: This is the ONLY modification tool.
    It can ONLY update take profit levels. It cannot close, sell, stop, or cancel.
    
    Args:
        position_id: The position ID to modify.
        price: Take profit trigger price.
        portfolio: Portion of position (0-1], default 1.0 for full position.
    """
    _check_configured()
    # Validate: portfolio must be reasonable
    if not 0 < portfolio <= 1:
        return {"status": "error", "message": f"Portfolio must be between 0 and 1, got {portfolio}"}
    
    # SANITIZED: Only pass TP parameters. Stop-loss, trailing, and close params are STRIPPED.
    safe_args = {
        "id": position_id,
        "takeProfits": [{"price": float(price), "portfolio": str(portfolio)}],
        "takeProfitBaseOn": "entry_order",
    }
    return await _call_upstream("edit_strategy", safe_args)

@mcp.tool()
async def proxy_health() -> dict[str, Any]:
    """Check if the proxy is configured and reachable."""
    return {
        "configured": bool(API_KEY),
        "upstream": UPSTREAM_URL,
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Key Design Rules

1. **The sell button doesn't exist.** No function in the proxy calls the upstream's close/sell/cancel tool. Adding one requires a code change, not a config change.

2. **Parameter sanitization.** Even for safe tools, strip or block parameters that could cause harm. In the example above, `stopLossPrice` is never forwarded.

3. **Input validation.** Validate bounds before forwarding (e.g., portfolio sum must equal 1.0). Catch errors before they reach the upstream.

4. **Read-only tools are true read-only.** `get_positions`, `get_strategy`, etc. have zero side effects. Document this explicitly in the tool description so the LLM knows it's safe to call.

5. **Process isolation.** The proxy runs as a separate process. Hermes communicates with it via stdio. It has its own environment variables, its own credentials, and its own codebase.

## Comparison: Config- vs Code-Level Enforcement

| Dimension | Config whitelist (`tools: { include }`) | Proxy server (this pattern) |
|---|---|---|
| Strength | Config-level, editable | Code-level, architectural |
| Override risk | Prompt injection, config edit | Requires git commit + deploy |
| Parameter control | None (upstream decides) | Full (proxy sanitizes) |
| Audit trail | Hermes logs | Proxy has its own logs |
| Setup time | 5 minutes | 1 hour |
| Best for | Quick constraints, trusted APIs | Money-moving, irreversible operations |

## Real Implementation

See the Wundertrading TP-only proxy at `/root/work/trading/wundertrading_proxy_server.py` for a complete production example:
- Wipes `stopLossPrice`, `stopLossMovePrice`, `trailingStop*` parameters before forwarding
- Validates portfolio sum = 1.0
- Does not expose `close_strategy_market`, `cancel_strategy`, `place_strategy_trade`
- 4 tools total: 2 read-only, 1 TP modification, 1 health check
