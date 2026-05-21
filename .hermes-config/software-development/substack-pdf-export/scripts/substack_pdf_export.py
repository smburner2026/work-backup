#!/usr/bin/env python3
"""
Substack PDF Export Pipeline

Extracts articles from a Substack publication as clean markdown, then
generates text-only PDFs.

Usage:
  1. Set PUBLICATION and CHAPTERS below
  2. python3 substack_pdf_export.py

Output: workdir/nolte_md/*.md (intermediate) and workdir/nolte_pdf/*.pdf
"""

import os, re, sys, time, codecs, json, html as html_mod
import urllib.request
import trafilatura

# --------------- config ---------------
PUBLICATION = "theognisomegara"
WORKDIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS = []  # list of slugs to fetch

# --------------- fetch ---------------
def fetch_body_html(slug):
    url = f"https://{PUBLICATION}.substack.com/p/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")
    m = re.search(r'window\._preloads\s*=\s*JSON\.parse\(\"(.*?)\"\)', html)
    if not m:
        return None, None
    data = json.loads(codecs.decode(m.group(1), "unicode_escape"))
    post = data.get("post", {})
    return post.get("body_html", ""), post.get("title", slug.replace("-", " ").title())

# --------------- extraction ---------------
def body_html_to_markdown(body_html):
    text = trafilatura.extract(body_html,
        output_format="markdown",
        include_links=False,
        include_images=False,
        include_formatting=True,
        favor_precision=True,
    )
    if not text:
        return None
    text = re.sub(r'^This below is.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^FUNDRAISING.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Click here to navigate.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Subscribe now\s*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()

# --------------- PDF ---------------
def sanitize(text):
    for ch in "\u200b\u200c\u200d\u2060\ufeff\u200e\u200f":
        text = text.replace(ch, "")
    REPL = {"\u2013": "-", "\u2014": "--", "\u2018": "'", "\u2019": "'",
            "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00a0": " "}
    for old, new in REPL.items():
        text = text.replace(old, new)
    return text

def generate_pdf(markdown, slug, title, out_dir):
    from fpdf import FPDF
    os.makedirs(out_dir, exist_ok=True)
    fpath = os.path.join(out_dir, f"{slug}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    mw = pdf.w - pdf.l_margin - pdf.r_margin

    def wl(ln, sz=10, b=False):
        sty = "B" if b else ""
        pdf.set_font("DejaVu", sty, sz)
        ln_s = sanitize(ln)
        if not ln_s.strip():
            pdf.ln(3); return
        try:
            lw = pdf.get_string_width(ln_s)
        except:
            lw = mw + 1
        if lw <= mw:
            try:
                pdf.multi_cell(0, 5, ln_s)
            except:
                pdf.ln(3)
            return
        words = ln_s.split()
        buf = ""
        for w in words:
            test = (buf + " " + w).strip()
            try:
                tw = pdf.get_string_width(test)
            except:
                tw = mw + 1
            if tw > mw and buf:
                try:
                    pdf.multi_cell(0, 5, buf)
                except:
                    pdf.ln(3)
                buf = w
            else:
                buf = test
        if buf:
            try:
                pdf.multi_cell(0, 5, buf)
            except:
                pdf.ln(3)

    wl(html_mod.unescape(title).strip(), 14, True)
    pdf.ln(3)
    for line in markdown.split("\n"):
        if pdf.get_y() > 270:
            pdf.add_page()
        line = line.strip()
        if not line:
            pdf.ln(2)
        elif line.startswith("#"):
            wl(line.lstrip("#").strip(), 12, True)
        else:
            wl(line)
    pdf.output(fpath)
    return fpath

# --------------- main ---------------
def main():
    if not CHAPTERS:
        print("ERROR: CHAPTERS list is empty. Edit the script and add slugs.")
        sys.exit(1)

    md_dir = os.path.join(WORKDIR, "nolte_md")
    pdf_dir = os.path.join(WORKDIR, "nolte_pdf")
    os.makedirs(md_dir, exist_ok=True)

    total = len(CHAPTERS)
    for i, slug in enumerate(CHAPTERS, 1):
        print(f"[{i}/{total}] {slug}")
        body_html, title = fetch_body_html(slug)
        if not body_html:
            print(f"  FAILED — no body_html")
            continue

        md = body_html_to_markdown(body_html)
        if not md:
            print(f"  FAILED — trafilatura returned None")
            continue

        md_path = os.path.join(md_dir, f"{slug}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"  -> {md_path} ({len(md):,} chars)")

        pdf_path = generate_pdf(md, slug, title, pdf_dir)
        print(f"  -> {pdf_path}")

        time.sleep(0.4)

    print(f"\nDone: {total} chapters -> {md_dir}/ and {pdf_dir}/")


if __name__ == "__main__":
    main()