# WunderTrading Webhook Integration

## Alert Lifecycle (TradingView)

**Removing an indicator does NOT remove the alerts** — but the alerts become nonfunctional:

- Alerts survive in the alert manager (bell icon → Manage alerts) after indicator removal
- They will throw runtime errors if their condition referenced the removed indicator's plots or calculations
- Price-based conditions (simple price levels, time conditions) survive unaffected
- Re-adding an identical copy of the indicator does NOT reliably restore orphaned alerts — TV's internal ID for the indicator changes
- **Manual cleanup required** — always check the alert manager after indicator changes

## WunderTrading Webhook Modes

WunderTrading accepts signals in **two modes**. The mode depends on how the bot is configured.

### Mode 1: Strategy Comment Mode (default)

For TradingView **Strategy** scripts (not indicators). The strategy's `strategy.entry()` / `strategy.exit()` calls include a `comment` parameter. The TradingView alert message is set to:

```
{{strategy.order.comment}}
```

WunderTrading receives the comment string, matches it against the bot's configured comment codes, and executes the appropriate action.

**Setup:**
1. Configure the bot in WunderTrading with specific comment codes for Enter-Long, Enter-Short, Exit-All, etc.
2. In your Pine Script strategy, pass matching strings to `strategy.entry(comment="Enter-Long")`
3. Create ONE alert on the strategy with message `{{strategy.order.comment}}`

**Pros:** Single alert handles all actions (entry, exit, close). WunderTrading automatically knows whether it's an entry or exit.
**Cons:** Only works with Strategy scripts, not Indicators. No way to override sizing per signal.

### Mode 2: JSON Mode (indicator-friendly)

For TradingView **Indicators** or when you need per-signal control over sizing, TP/SL. The alert message is a JSON payload:

```json
{
  "code": "Enter-Long",
  "orderType": "market",
  "amountPerTradeType": "quote",
  "amountPerTrade": 150,
  "takeProfits": [
    { "priceDeviation": 0.01, "portfolio": 0.25 },
    { "priceDeviation": 0.02, "portfolio": 0.25 },
    { "priceDeviation": 0.03, "portfolio": 0.25 },
    { "priceDeviation": 0.06, "portfolio": 0.25 }
  ],
  "stopLoss": { "priceDeviation": 0.015 },
  "reduceOnly": false,
  "placeConditionalOrdersOnExchange": false
}
```

**Setup:**
1. Configure the bot in WunderTrading with **Bot settings format = JSON**
2. WunderTrading generates a Webhook URL and template code/comment expectations
3. In your TradingView alert, use the JSON above as the Message body

### JSON Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `code` | string | **Yes** | Action: `Enter-Long`, `Enter-Short`, `Exit-Long`, `Exit-Short`, `Exit-All`. Must match the bot's comment EXACTLY (case-sensitive). If you edit the bot's Name, Exchange, Timeframe, or Pair, the comment codes change — update the alert. |
| `orderType` | string | No | `market` (default) or `limit`. |
| `amountPerTradeType` | string | No | `quote` (USDT), `base` (BTC), `percents` (% of balance), or `contracts` (futures). |
| `amountPerTrade` | number | No | Quantity in the unit specified by `amountPerTradeType`. |
| `price` | number | No | Limit order price (only for `orderType: "limit"`). |
| `stopLoss` | object | No | `{ "priceDeviation": 0.01 }` (1%) or `{ "price": 75000 }`. Single-pair only. |
| `stopLossBasedOn` | string | No | `"average_price"` or `"entry_order"`. Determines which cost basis SL is calculated from for DCA positions. |
| `takeProfits` | array | No | Array of `{ "priceDeviation": 0.02, "portfolio": 0.25 }`. `portfolio` values must sum to exactly 1.0. |
| `takeProfitsBasedOn` | string | No | `"average_price"` or `"entry_order"`. |
| `priceDeviation` | number | — | Must be in **decimals** (0.02 = 2%), never percent strings like "2%". Multi-pair bots MUST use `priceDeviation`, not `price`. |
| `reduceOnly` | bool | No | `true` for exits that should only reduce position (futures only, no effect on spot). |
| `placeConditionalOrdersOnExchange` | bool | No | `false` by default. |

### Important Constraints

- **`code` field is case-sensitive** — `"Enter-Long"` ≠ `"enter-long"`
- **Multi-pair bots must use `priceDeviation`** (decimal fractions), not absolute `price`
- **`takeProfits[i].portfolio` must sum to exactly 1.0** (100%). Fractions are fine (0.25 = 25%).
- **Port 80 only** for TradingView webhook URLs — TV rejects custom ports (e.g., 8080 is blocked). If running a webhook receiver server, bind it to port 80.
- **Swing Trade (ON)** must be enabled for auto-flip positions (futures only). In this mode, you only need `Enter-Long` / `Enter-Short` — the bot automatically closes the opposite position.
- **Swing Trade (OFF)** requires explicit exit signals: `Exit-Long`, `Exit-Short`, or `Exit-All`.

## Ensuring Compatibility When Swapping Indicators

When replacing an indicator (e.g., switching from FATCAT to a custom replica), the **critical invariant is the alert message format, NOT the indicator itself**:

1. **Preserve the Message field** — the JSON body in the TradingView alert's Message field is what WunderTrading parses. As long as the new indicator fires an alert with the same JSON structure, WunderTrading is unaffected.
2. **The `code` field must match** whatever the bot expects (`Enter-Long`, `Enter-Short`, etc.) — this is configured in the WunderTrading bot settings, not in the indicator.
3. **Delete old orphaned alerts** — after removing the old indicator, open the alert manager (bell icon) and delete any alerts that referenced it. They won't fire correctly anymore even if the condition is repointed.
4. **Test the pipeline** — after creating the new alert, use a manual POST to the webhook URL with the same JSON body to confirm WunderTrading accepts it before waiting for a live signal.

## Webhook URL

The webhook URL is generated by WunderTrading's Signal Bot settings. It's unique per bot configuration. If you edit the bot's Name, Exchange, Timeframe, or Pair, the webhook URL changes and you must update the TradingView alert accordingly.

**Do NOT guess or construct the URL manually** — always copy it from the WunderTrading bot's Alerts tab.

## Pine Script Alert Message Construction (v6)

For JSON mode from a Pine Script indicator:

```pinescript
//@version=6
indicator("My Signal", overlay=true)

// Build the JSON payload dynamically
makePayload() =>
    '{"code":"Enter-Long","orderType":"market","amountPerTradeType":"quote","amountPerTrade":150}'

// Fire alert on signal
if bullCondition
    alert(makePayload(), alert.freq_once_per_bar_close)
```

Key constraints:
- `alert()` (not `alertcondition()`) accepts series strings with dynamic values
- v6 supports `+` string concat but only on a single physical line
- `str.tostring(bool)` is unreliable — use ternary `b ? "true" : "false"`
- `alert()` is a side effect — remove `timeframe=""` from `indicator()` declaration
