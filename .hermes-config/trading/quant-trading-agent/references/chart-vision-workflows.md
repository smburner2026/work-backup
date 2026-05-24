# Chart Screenshot Analysis — Vision & Fallback Workflows

## Primary Path: Vision Model

### DeepSeek Limitation

DeepSeek models (v4-flash, v4-pro, v3, r1) do **not** support image input via `vision_analyze`. The error is:

```
unknown variant 'image_url', expected 'text'
```

This is a provider-level limitation, not a format issue. No amount of resizing, format conversion, or compression will fix it.

### Fix: Route Vision to a Different Provider

Option 1 — Switch main model temporarily:
```
/model anthropic/claude-sonnet-4
```
Then send the screenshot, analyze, `/model deepseek-v4-pro` to switch back.

Option 2 — Configure auxiliary vision routing (recommended for frequent use):
```bash
hermes config set auxiliary.vision.provider opencode-go
hermes config set auxiliary.vision.model anthropic/claude-sonnet-4
hermes config set auxiliary.vision.timeout 120
```
Then `/reset`. Vision tasks automatically route to Claude while chat stays on DeepSeek.

OpenCode Go vision-capable models:
| Model | Chart Analysis Quality |
|---|---|
| `anthropic/claude-sonnet-4` | Best — reads timestamps, prices, arrow positions |
| `anthropic/claude-3.5-sonnet` | Excellent, slightly cheaper |
| `openai/gpt-4o` | Good, sometimes less precise on small text |
| `google/gemini-1.5-pro` | Works, weaker on TradingView UI details |

## Fallback: When Vision Isn't Available

### OCR (tesseract)

Only works if chart contains large, high-contrast text. TradingView charts typically fail OCR because:
- Timestamps are small and low-contrast
- Indicator names blend with chart background
- Candle patterns confuse the OCR engine

Installed on this system: `tesseract` + `pytesseract`. Usage:
```python
import pytesseract
from PIL import Image, ImageEnhance
img = Image.open('chart.jpg')
gray = img.convert('L')
enhanced = ImageEnhance.Contrast(gray).enhance(3.0)
text = pytesseract.image_to_string(enhanced, config='--psm 6')
```

### Color-Based Arrow Detection

For detecting buy/sell signals on a chart when you know the arrow colors:

```python
import numpy as np
from PIL import Image

img = Image.open('chart.jpg')
hsv = np.array(img.convert('HSV'), dtype=np.float32)
h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

# Green arrows (bull) — H around 85 (±30), saturated, not dark
green_mask = (h > 55) & (h < 115) & (s > 70) & (v > 80)

# Red arrows (bear) — H near 0-15 or 240-255
red_mask = ((h < 15) | (h > 240)) & (s > 70) & (v > 80)

# White arrows (original BAMBAM bull)
white_mask = (s < 30) & (v > 200)

# Black arrows (original BAMBAM bear)
black_mask = (v < 40) & (s < 50)
```

This can count arrows and estimate their chart positions, but cannot read timestamps or prices. Useful for counting, not for precise comparison data.

### Best Fallback: User Describes the Chart

Ask the user for:
- Instrument + timeframe
- Number of signals from each indicator
- Which specific bars disagree
- Any visible indicator name in the top-left

This is faster and more reliable than OCR or color detection on most charts.