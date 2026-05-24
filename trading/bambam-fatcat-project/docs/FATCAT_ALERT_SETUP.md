# FATCAT Alert Setup (Invite-Only Indicator)

Since FATCAT is invite-only and you can't modify its source, use TV's
built-in chart condition alerts instead.

## One-Time Setup

### Step 1: Start the MCP server
```bash
cd /path/to/bambam-fatcat-project
python3 mcp_server.py http
```
This starts listening on port 8080.

### Step 2: Add FATCAT to your chart
- Open the Ferocious FATCAT indicator on a BTCUSDT 15m chart

### Step 3: Create the buy signal alert
1. Right-click the chart → **Add Alert**
2. **Condition:** Select "Ferocious FATCAT" → find the Bull/Buy signal
   (Usually listed as "Buy Signal" or "Bullish" in the indicator's plots)
3. **Expiration:** Select "Until cancelled" (for Bar Replay)
4. **Webhook URL:** `http://YOUR_LOCAL_IP:8080`
5. **Message:** Use this payload template:
```json
{"source":"fatcat","direction":"bull","symbol":"{{ticker}}","timeframe":"15m","timestamp":"{{timenow}}","price":{{close}}}
```
6. Click **Create**

### Step 4: Create the sell signal alert (if needed)
Same as Step 3 but select the Bear/Sell signal, direction set to "bear".

### Step 5: Test with Bar Replay
1. Right-click → **Bar Replay**
2. Set start date to 90 days ago
3. Set speed to maximum (fast-forward)
4. Watch the MCP server console — signals should appear
5. Check: `curl http://localhost:8080/stats`

## Troubleshooting

- **No alerts firing:** Open the indicator's visual plots, confirm the signal
  names match what's available in the condition dropdown
- **Webhook URL not reachable:** TV running on the same machine? Use
  `localhost`. Different machine? Use the LAN IP.
- **Bar Replay exits early:** TV has a bar limit per replay session.
  Use 30-day windows and run multiple passes if needed.
- **Wrong payload format:** Check the MCP server logs — it shows raw payloads.

## After Capture

Once you have signals in the DB:

```bash
# Export BAMBAM signals as JSON for the sweep
python3 -c "
from mcp_server import query_signals, store_signal
import json
data = query_signals(source='bambam')
json.dump(data, open('export_bambam.json','w'))
data = query_signals(source='fatcat')
json.dump(data, open('export_fatcat.json','w'))
print('Exported')
"

# Run the sweep
python3 sweep.py --pbb export_bambam.json --fatcat export_fatcat.json
```
