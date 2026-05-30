# Photo Embedding in Translated PDF Output

Concrete recipe from the Cao Dai Army session: extracting 44 images from a 108-page Vietnamese PDF and embedding 31 of them in the translated English output at correct positions.

## Source PDF Profile

- Title: *Quân Đội CAO ĐÀI* (The Cao Dai Army), compiled by Tỉnh Tâm, 2017
- 108 pages, 5.5×8.5 inch format, InDesign CS5.5 source
- ~50K chars of Vietnamese text, ~5 pages of photo gallery at end
- Embedded text (not scanned) — clean pdftotext extraction

## Image Inventory (from pdfimages -list)

```
Page  1: images 0-4  → cover/background (skip)
Page  3: images 5-6  → logo/emblem (skip)
Page 23: images 8-10 → General Trần Quang Vinh portraits → IN TEXT
Page 43: images 11-13 → General Nguyễn Thành Phương portraits → IN TEXT
Page 64: images 14-16 → Generals Lê Văn Tất + Nguyễn Văn Thành → IN TEXT
Page 78: images 17-19 → General Trình Minh Thế portraits → IN TEXT
Page 84: images 20-22 → General Văn Thành Cao portraits → IN TEXT
Pages 103-108: images 23-43 → Photo gallery section → AT END
Page 108: image 44 → end matter (skip)
```

Total to include: 11 portrait images + 21 gallery images = 31 images embedded.

## Workflow

### Step 1: Extract All Images

```bash
mkdir -p /tmp/caodai_images
pdfimages -j "/path/to/source.pdf" /tmp/caodai_images/img
# Produces img-NNN.jpg (JPEG) or img-NNN.ppm (PPM fallback)
```

### Step 2: Convert PPMs to JPEG via PIL

```python
from PIL import Image

for name in ['img-028', 'img-031', 'img-034']:
    ppm = f'/tmp/caodai_images/{name}.ppm'
    jpg = f'/tmp/caodai_images/{name}.jpg'
    img = Image.open(ppm)
    img.save(jpg, 'JPEG', quality=85)
```

PPM files are uncompressed (7MB for a single photo) and cannot be loaded by PDF renderers. JPEG conversion is mandatory.

### Step 3: Detect Image Insertion Points in Translated Text

The English text has paragraph boundaries. Map each general's portrait to their narrative section by matching the section header paragraph:

```
Para 39: "1. General Trần Quang Vinh (1897–1977)" → img-008, 009, 010
Para 50: "2. Nguyễn Thành Phương" → img-011, 012, 013
Para 61: "3. General Lê Văn Tất" → img-014
Para 64: "4. General Nguyễn Văn Thành (1915–1972)" → img-015, 016
Para 69: "5. General Văn Thành Cao" → img-020, 021
Para 76: "6. General Trình Minh Thế (1922–1955)" → img-017, 018, 019
```

**Trap**: "2. Nguyễn Thành Phương" lacks the "General" prefix while all others include it. Detection logic must handle both patterns.

### Step 4: Generate HTML with Embedded Images

Build the HTML programmatically in Python. For each general section header, inject a `<div class="in-text-img">` containing the image HTML immediately after the `<h2>`:

```python
def get_img_html(name, caption=''):
    """Return HTML for an image at path /tmp/caodai_images/{name}{.jpg or .ppm}"""
    for ext in ['.jpg', '.ppm']:
        path = f'/tmp/caodai_images/{name}{ext}'
        if os.path.exists(path):
            if ext == '.ppm':
                jpg_path = path.replace('.ppm', '.jpg')
                if not os.path.exists(jpg_path):
                    Image.open(path).save(jpg_path, 'JPEG', quality=85)
                path = jpg_path
            src = 'file://' + os.path.abspath(path)
            cap = f'<p class="img-caption">{caption}</p>' if caption else ''
            return f'<div class="in-text-img">{cap}<img src="{src}" alt="{caption}" /></div>\n'
    return ''
```

Photo gallery at end: iterate the gallery image list and insert each with a page break every 2 images.

### Step 5: CSS Configuration

```css
/* In-text portraits — centered, avoid page-break inside, capped at 80% width */
.in-text-img { text-align: center; margin: 1em 0; page-break-inside: avoid; }
.in-text-img img { max-width: 80%; height: auto; }
.img-caption { font-size: 9pt; color: #666; font-style: italic; text-align: center; margin-bottom: 0.3em; }

/* Photo gallery pages — full-bled, centered */
.photo-page { page-break-before: always; text-align: center; }
.photo-page img { max-width: 95%; height: auto; margin: 0.3em auto; display: block; }
```

### Step 6: Build PDF

```bash
weasyprint book.html book.pdf
```

Check stderr for any "Failed to load image" errors — these mean an image file is missing, unconverted, or the path is wrong.

### Step 7: Verify

- **Before adding images**: 53 pages
- **After adding portraits + gallery**: 61 pages (+8 pages from images)
- Photo section images should each take roughly one page
- Portrait images should appear adjacent to the corresponding general's biography

## Key Lessons

1. **Never drop all photos at the end** — the user will notice and correct you. Map each image to its original page position.
2. **PPM is a trap** — `pdfimages -j` gives JPEG for most images but PPM for some. Always check the extension and convert.
3. **Page numbers in `pdfimages -list` bound the positions** — use them to decide "gallery vs in-text" classification.
4. **Detection logic matters** — section headers in the translated text may vary (e.g. "2. Nguyễn Thành Phương" lacks "General"). Test against the actual paragraph text.
5. **Tell the user what moved** — "61 pages now (was 53) — the portraits added 8 pages where they belong" confirms the fix worked.
6. **Do NOT use the full-page screenshot approach** — rendering each original page as a screenshot image with English text overlaid produces output the user considers "weird." Even though it preserves every photo in its exact original position, the visual quality is poor and the reading experience is degraded. Always go straight to clean text with extracted images embedded at narrative positions + photo gallery at end.
7. **Photo placement acceptance order** — The user rejected these in sequence: (a) all photos dumped at end, (b) full-page screenshot overlays. Only approach (c) — clean text with embedded extracted images at narrative positions, gallery at end — was accepted as "fine." Get to (c) directly, don't try (a) or (b).
