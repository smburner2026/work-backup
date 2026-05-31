#!/usr/bin/env python3
"""Download Hoang-Tham from Gallica IIIF - ultra conservative.
Waits for rate limit to expire, then downloads one page every 15 seconds."""

import json, os, sys, time, urllib.request, urllib.error, img2pdf, random

MANIFEST_URL = "https://gallica.bnf.fr/iiif/ark:/12148/bpt6k374553s/manifest.json"
OUT_DIR = "/root/work/post-colonial-vietnam/sources/chack/hoang-tham-pages"
OUT_PDF = "/root/work/post-colonial-vietnam/sources/chack/Hoang-Tham_pirate_Paul_Chack_1933.pdf"
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
os.makedirs(OUT_DIR, exist_ok=True)

mf = os.path.join(OUT_DIR, "manifest.json")
if not os.path.exists(mf):
    req = urllib.request.Request(MANIFEST_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        with open(mf, "wb") as f:
            f.write(r.read())
with open(mf) as f:
    manifest = json.load(f)

canvases = manifest["sequences"][0]["canvases"]
total = len(canvases)
print(f"Total pages: {total}")

# Use smaller images to reduce server load
RES = "800,"  # moderate resolution
DELAY = 12     # 12 seconds between pages
BACKOFF = 300  # 5 min backoff on 429
INITIAL_WAIT = 120  # wait 2 minutes at start for rate limit to reset

print(f"Waiting {INITIAL_WAIT}s for rate limit to reset...")
time.sleep(INITIAL_WAIT)

images = []
for i, canvas in enumerate(canvases):
    label = canvas.get("label", f"p{i+1}")
    svc = canvas["images"][0]["resource"]["service"]["@id"]
    img_url = f"{svc}/full/{RES}/0/default.jpg"
    out = os.path.join(OUT_DIR, f"p{i+1:04d}.jpg")

    if os.path.exists(out) and os.path.getsize(out) > 3000:
        images.append(out)
        print(f"  [{i+1}/{total}] {label} — cached")
        continue

    success = False
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(img_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            assert data is not None and len(data) > 1000
            with open(out, "wb") as f:
                f.write(data)
            images.append(out)
            kb = len(data) / 1024
            print(f"  [{i+1}/{total}] {label} — {kb:.0f}KB")
            success = True
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = BACKOFF * attempt + random.uniform(0, 60)
                print(f"  [{i+1}/{total}] 429 — waiting {wait:.0f}s (attempt {attempt})")
                time.sleep(wait)
            else:
                print(f"  [{i+1}/{total}] FAILED: {e}")
                break
        except Exception as e:
            print(f"  [{i+1}/{total}] FAILED: {e}")
            break

    if not success:
        print(f"  [{i+1}/{total}] Giving up after 3 attempts")
    time.sleep(DELAY + random.uniform(0, 3))

if images:
    os.chdir(OUT_DIR)
    page_files = [f"p{i+1:04d}.jpg" for i in range(total) if f"p{i+1:04d}.jpg" in os.listdir('.')]
    print(f"\nCompiling {len(page_files)} pages into PDF...")
    with open(OUT_PDF, "wb") as f:
        f.write(img2pdf.convert([os.path.join(OUT_DIR, p) for p in sorted(page_files)]))
    sz = os.path.getsize(OUT_PDF) / 1048576
    print(f"PDF: {OUT_PDF} ({sz:.1f} MB)")
    print(f"Got {len(images)}/{total} pages")
else:
    print("No images downloaded!")
