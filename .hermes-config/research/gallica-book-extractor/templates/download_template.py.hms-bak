#!/usr/bin/env python3
"""Download a book from Gallica IIIF. Template — edit CONFIG section."""
import json, os, sys, time, urllib.request, urllib.error, img2pdf, random

# === CONFIG (edit these) ===
ARK = "bpt6kXXXXXXX"
AUTHOR_SLUG = "author_name"
BOOK_SLUG = "book_title"
YEAR = "1933"
MANIFEST_URL = f"https://gallica.bnf.fr/iiif/ark:/12148/{ARK}/manifest.json"
OUT_DIR = f"/root/work/post-colonial-vietnam/sources/{AUTHOR_SLUG}"
OUT_PDF = os.path.join(OUT_DIR, f"{BOOK_SLUG}_{AUTHOR_SLUG}_{YEAR}.pdf")
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
RES = "800,"
DELAY = 12
BACKOFF = 300
INITIAL_WAIT = 120
# === END CONFIG ===

os.makedirs(OUT_DIR, exist_ok=True)
mf = os.path.join(OUT_DIR, "manifest.json")

if not os.path.exists(mf):
    print("Downloading IIIF manifest...")
    req = urllib.request.Request(MANIFEST_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        with open(mf, "wb") as f: f.write(r.read())

with open(mf) as f: manifest = json.load(f)
canvases = manifest["sequences"][0]["canvases"]
total = len(canvases)
print(f"Total pages: {total}")
print(f"Waiting {INITIAL_WAIT}s for rate limit cooldown..."); sys.stdout.flush()
time.sleep(INITIAL_WAIT)

images = []
for i, canvas in enumerate(canvases):
    label = canvas.get("label", f"p{i+1}")
    svc = canvas["images"][0]["resource"]["service"]["@id"]
    img_url = f"{svc}/full/{RES}/0/default.jpg"
    out = os.path.join(OUT_DIR, f"p{i+1:04d}.jpg")
    if os.path.exists(out) and os.path.getsize(out) > 3000:
        images.append(out); print(f"  [{i+1}/{total}] {label} — cached"); continue
    success = False
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(img_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            assert data is not None and len(data) > 1000
            with open(out, "wb") as f: f.write(data)
            images.append(out); print(f"  [{i+1}/{total}] {label} — {len(data)//1024}KB")
            success = True; break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = BACKOFF * attempt + random.uniform(0, 60)
                print(f"  [{i+1}/{total}] 429 — waiting {wait:.0f}s"); sys.stdout.flush(); time.sleep(wait)
            else: print(f"  [{i+1}/{total}] FAILED: {e}"); break
        except Exception as e: print(f"  [{i+1}/{total}] FAILED: {e}"); break
    time.sleep(DELAY + random.uniform(0, 3))

if images:
    os.chdir(OUT_DIR)
    files = sorted([f for f in os.listdir('.') if f.endswith('.jpg') and os.path.getsize(f) > 1000])
    print(f"\nCompiling {len(files)} pages into PDF..."); sys.stdout.flush()
    with open(OUT_PDF, "wb") as f: f.write(img2pdf.convert([os.path.join(OUT_DIR, p) for p in files]))
    sz = os.path.getsize(OUT_PDF) / 1048576
    print(f"PDF: {OUT_PDF} ({sz:.1f} MB)")
