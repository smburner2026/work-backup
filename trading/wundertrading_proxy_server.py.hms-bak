#!/usr/bin/env python3
"""
Wundertrading TP-Only Proxy MCP Server

This server sits between Hermes Agent and the Wundertrading MCP API.
It PHYSICALLY ONLY exposes:
  - get_live_strategies  (read positions)
  - get_strategy         (read single strategy details)
  - edit_take_profit     (update take profit levels ONLY)

Constitutional constraint: this binary does NOT contain code paths for
close, sell, stop-loss, cancel, trailing stop, or any other execution.
The sell button does not exist in this process.
"""

import os
import sys
import json
import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP

# ── Configuration ──────────────────────────────────────────────────────────
WUNDER_MCP_URL = "https://wundertrading.com:2083/mcp"
API_KEY = os.environ.get("WUNDER_API_KEY", "")
SECRET_KEY = os.environ.get("WUNDER_SECRET_KEY", "")

HEADERS = {
    "X-API-Key": API_KEY,
    "X-Secret-Key": SECRET_KEY,
    "Content-Type": "application/json",
}

# ── MCP Server Setup ──────────────────────────────────────────────────────
mcp = FastMCP("wundertrading-tp-proxy")


def _ensure_configured() -> None:
    """Hard check: if credentials are missing, refuse to start."""
    if not API_KEY or not SECRET_KEY:
        raise RuntimeError(
            "Wundertrading proxy not configured. "
            "Set WUNDER_API_KEY and WUNDER_SECRET_KEY environment variables."
        )


async def _call_wunder_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """
    Call a tool on the Wundertrading MCP server via HTTP transport.
    
    CONSTITUTIONAL RULE: This function is the ONLY bridge to the
    Wundertrading API. New tools added here must be manually reviewed.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(WUNDER_MCP_URL, json=payload, headers=HEADERS)
        resp.raise_for_status()
        result = resp.json()
    
    if "error" in result:
        return {"status": "error", "message": result["error"].get("message", str(result["error"]))}
    
    # Extract content from MCP response
    content = result.get("result", {}).get("content", [])
    text_parts = [item.get("text", "") for item in content if item.get("type") == "text"]
    combined = "\n".join(text_parts)
    
    # Try to parse as JSON if possible
    try:
        return json.loads(combined)
    except (json.JSONDecodeError, TypeError):
        return {"result": combined}


# ── Tool: Get Live Strategies ──────────────────────────────────────────────
@mcp.tool()
async def get_live_strategies() -> dict[str, Any]:
    """
    Get all currently active/live trading strategies (open positions).
    Use this to see what positions are open and their current status.
    Read-only — no trading side effects.
    """
    _ensure_configured()
    return await _call_wunder_tool("get_live_strategies", {})


# ── Tool: Get Single Strategy ─────────────────────────────────────────────
@mcp.tool()
async def get_strategy(strategy_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific strategy, including entry price,
    current price, take profits, and stop loss settings.
    
    Args:
        strategy_id: The strategy ID or clientId from Wundertrading.
    """
    _ensure_configured()
    return await _call_wunder_tool("get_strategy", {"id": strategy_id})


# ── Tool: Edit Take Profit (TP-ONLY) ──────────────────────────────────────
@mcp.tool()
async def edit_take_profit(
    strategy_id: str,
    take_profits: list[dict[str, Any]],
    base_on: str = "entry_order",
) -> dict[str, Any]:
    """
    Update the take profit levels on an existing position.
    
    CONSTITUTIONAL CONSTRAINT: This is the ONLY modification tool available.
    It can ONLY set take profit targets. It CANNOT:
    - Close positions
    - Stop loss
    - Trail stops
    - Cancel strategies
    - Place new trades
    
    Args:
        strategy_id: The strategy ID or clientId of the position to update.
        take_profits: List of take profit targets. Each target has:
            - price (number): Trigger price. For LONG: above entry price.
              For SHORT: below entry price.
            - portfolio (number): Portion of position (0-1], e.g. 0.5 = 50%.
              Sum of all portfolios must equal 1.0.
        base_on: Price basis for TP — "entry_order" or "average_price".
    
    Returns:
        Status of the update operation.
    """
    _ensure_configured()
    
    # Validate portfolio sums to 1.0
    total_portfolio = sum(
        float(tp.get("portfolio", 0)) for tp in take_profits
    )
    if abs(total_portfolio - 1.0) > 0.01:
        return {
            "status": "error",
            "message": f"Take profit portfolios sum to {total_portfolio:.2f}, must equal 1.0"
        }
    
    arguments = {
        "id": strategy_id,
        "takeProfits": [
            {
                "price": float(tp["price"]),
                "portfolio": str(tp["portfolio"]),
            }
            for tp in take_profits
        ],
        "takeProfitBaseOn": base_on,
    }
    
    return await _call_wunder_tool("edit_trade_strategy", arguments)


# ── Health Check ───────────────────────────────────────────────────────────
@mcp.tool()
async def proxy_health() -> dict[str, Any]:
    """
    Check if the proxy is properly configured and can reach Wundertrading.
    Returns connection status and API key presence (not the key itself).
    """
    return {
        "configured": bool(API_KEY and SECRET_KEY),
        "has_api_key": bool(API_KEY),
        "has_secret_key": bool(SECRET_KEY),
        "wunder_mcp_url": WUNDER_MCP_URL,
    }


# ── Main Entrypoint ────────────────────────────────────────────────────────
def main():
    """Run the proxy server over stdio (for Hermes MCP integration)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
