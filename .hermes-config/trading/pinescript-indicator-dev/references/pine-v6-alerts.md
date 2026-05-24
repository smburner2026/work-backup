# Pine Script v6: alertcondition() vs alert() — Message Parameter Types

From official TradingView docs: https://www.tradingview.com/pine-script-docs/faq/alerts

## alertcondition()
- `message` parameter: **const string** (fixed at compile time)
- CANNOT contain dynamic values, `str.tostring()`, variables, or function call results
- CAN contain `{{placeholders}}` like `{{close}}`, `{{time}}`, etc.
- Each `alertcondition()` call = separate condition in the "Create Alert" dropdown
- Each condition counts toward the plan alert limit
- Passing a dynamic (series) string produces **CE10123**: `Cannot call "operator +" with argument "expr0"=...` — the error is misleading; the `+` concat is fine, but `alertcondition()` rejects the non-const result

## alert()
- `message` parameter: **series string** (dynamic, can change bar-to-bar)
- Accepts `str.tostring()`, variables, concatenation, function results — everything
- All `alert()` calls in a script = ONE condition: "Any alert() function call"
- User creates ONE alert, ONE webhook URL
- Counts as ONE alert toward the plan limit regardless of how many `alert()` calls
- `freq` parameter controls frequency: `alert.freq_once_per_bar`, `alert.freq_once_per_bar_close`, `alert.freq_all`

## CE10080: Side effects + timeframe conflict
`alert()` creates side effects (drawings/alerts that fire externally). Scripts with side effects cannot have a `timeframe` argument on `indicator()`:
```
indicator("Name", overlay=true)              // ✅ OK
indicator("Name", overlay=true, timeframe="") // ❌ CE10080
```

## String handling in v6
- `+` concatenation IS supported for strings
- Multi-line "line wrapping" (splitting a single-line string across code lines with `+`) is deprecated
- Use single-line arrow expressions or `str.format()` for complex templates
- `str.tostring(bool)` is unreliable — use `bool ? "true" : "false"` ternary instead

## CE10144: Local scope restrictions
v6 rejects bare `if`/`for` without explicit local code blocks at the top level of an indicator. Use ternaries instead:
- ❌ `if deltaMode == "AND"\n    bearRaw := ...`  — CE10144
- ✅ `bearRaw = deltaMode == "AND" ? bear_AND : bear_OR`

## TV webhook port restriction
**TradingView only allows port 80 for HTTP webhooks.** Port 8080 and other custom ports are rejected. Always bind the receiver to port 80. Plain HTTP on port 80 works — no HTTPS required.
