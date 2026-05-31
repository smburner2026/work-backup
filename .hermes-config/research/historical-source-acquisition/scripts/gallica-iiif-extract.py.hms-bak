#!/usr/bin/env python3
"""
Gallica IIIF Book Extractor — download public-domain books from Gallica (BnF)
and compile into a PDF using the IIIF image API.

Usage:
  python3 gallica-iiif-extract.py <manifest_url> [--output-dir DIR] [--delay SEC] [--res-width PX]

Examples:
  # Full resolution (slow, high-quality)
  python3 gallica-iiif-extract.py \\
    "https://gallica.bnf.fr/iiif/ark:/12148/bpt6k374553s/manifest.json"

  # Lower resolution (faster, kinder to server, still readable)
  python3 gallica-iiif-extract.py \\
    "https://gallica.bnf.fr/iiif/ark:/12148/bpt6k374553s/manifest.json" \\
    --res-width 800 --delay 3.0

Notes:
  - Rate limiting: Gallica IIIF server 429s after ~55 requests at high frequency.
    Use delay >= 2s and res-width <= 1000 for reliability.
  - On 429: waits 180s, then retries up to 5 times with exponential backoff.
  - Resume: --resume skips already-downloaded pages (cached by filename).
"""

import json
import os
import sys
import time
import random
import argparse
import urllib.request
import urllib.error
import img2pdf

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
BACKOFF_BASE = 180  # seconds for first 429 retry
MAX_RETRIES = 5
MIN_SIZE_KEEP = 3000


def download_manifest(url, retries=MAX_RETRIES):
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = BACKOFF_BASE * attempt + random.uniform(0, 30)
                print(f"  Manifest 429, waiting {wait:.0f}s (attempt {attempt}/{retries})")
                time.sleep(wait)
            else:
                raise


def download_page(img_url, out_path, retries=MAX_RETRIES):
    """Download one page image with retry and exponential backoff on 429."""
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(img_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            assert data is not None and len(data) > 0
            with open(out_path, "wb") as f:
                f.write(data)
            return len(data)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = BACKOFF_BASE * attempt + random.uniform(0, 30)
                print(f"    429, waiting {wait:.0f}s (attempt {attempt}/{retries})")
                time.sleep(wait)
            else:
                raise
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Extract Gallica IIIF book to PDF"
    )
    parser.add_argument("manifest_url", help="IIIF manifest URL")
    parser.add_argument(
        "--output-dir", "-o", default=".",
        help="Output directory"
    )
    parser.add_argument(
        "--delay", "-d", type=float, default=2.0,
        help="Seconds between page requests (default: 2.0; increase if 429s)"
    )
    parser.add_argument(
        "--res-width", type=int, default=0,
        help="Width in px for IIIF resize (e.g. 600, 800). "
             "0 = full resolution. Lower = faster, fewer 429s."
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Skip already-downloaded pages"
    )
    args = parser.parse_args()

    delay = args.delay
    width = args.res_width
    out_dir = args.output_dir
    pages_dir = os.path.join(out_dir, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    print("[1/3] Downloading IIIF manifest...")
    manifest = download_manifest(args.manifest_url)
    canvases = manifest["sequences"][0]["canvases"]
    total = len(canvases)

    title = (manifest.get("description") or "").strip() or "gallica-book"
    safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in title)
    pdf_path = os.path.join(out_dir, f"{safe_title[:80]}.pdf")

    # Build resize parameter
    if width > 0:
        size_param = f"{width},"
        print(f"Using width={width}px resolution")
    else:
        size_param = "full"

    print(f"[2/3] Downloading {total} pages to {pages_dir}/ ...")

    images = []
    start = time.monotonic()
    for i, canvas in enumerate(canvases):
        label = canvas.get("label", f"page_{i+1}")
        img_service = canvas["images"][0]["resource"]["service"]["@id"]
        img_url = f"{img_service}/full/{size_param}/0/default.jpg"
        out_path = os.path.join(pages_dir, f"page_{i+1:04d}.jpg")

        if args.resume and os.path.exists(out_path) and \
                os.path.getsize(out_path) > MIN_SIZE_KEEP:
            images.append(out_path)
            print(f"  [{i+1}/{total}] {label} — cached")
            continue

        try:
            size = download_page(img_url, out_path)
            if size:
                images.append(out_path)
                elapsed = time.monotonic() - start
                rate = (i + 1) / (elapsed / 60) if elapsed > 0 else 0
                print(f"  [{i+1}/{total}] {label} — {size//1024}KB "
                      f"[{rate:.1f} pages/min]")
            if delay > 0:
                time.sleep(delay + random.uniform(0, delay * 0.3))
        except Exception as e:
            print(f"  [{i+1}/{total}] {label} — FAILED: {e}", file=sys.stderr)

    if not images:
        print("ERROR: No pages downloaded.", file=sys.stderr)
        sys.exit(1)

    print(f"\n[3/3] Compiling {len(images)}/{total} pages into PDF...")
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(images))

    size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    elapsed = time.monotonic() - start
    print(f"PDF: {pdf_path}")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Time: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print("Done.")


if __name__ == "__main__":
    main()
