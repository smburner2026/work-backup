#!/usr/bin/env python3
"""
Substack Paywall Export CLI (stash)

Usage:
  stash auth                          Validate cookie, show account info
  stash pubs                          List subscribed publications
  stash pubs --add <pub>              Add a publication by subdomain
  stash pubs --remove <pub>           Remove a publication
  stash fetch <pub>                   Fetch all articles from a publication
  stash fetch <pub> --since <date>    Fetch articles since a date (ISO format)
  stash fetch <pub> --limit N         Fetch last N articles
  stash fetch --all                   Fetch all known publications
  stash fetch <pub> --force           Re-fetch even if cached
  stash export <pub> [--format md|pdf|both]  Export articles
  stash export <pub> --slug <slug>    Export a single article
  stash list <pub>                    List cached articles for a publication
  stash status                        Show cache status
  stash clean                         Clean exported files (keep raw cache)

Examples:
  stash auth
  stash pubs
  stash fetch substack.com
  stash fetch theognisomegara
  stash export theognisomegara --format md
  stash export theognisomegara --slug some-article-slug --format pdf
"""

import os
import sys
import json
import time
import argparse
import re
from pathlib import Path

# Add scripts dir to path for imports
_SCRIPTS_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SCRIPTS_DIR))

from substack_client import (
    load_auth, save_auth, get_current_user,
    discover_subscriptions, resolve_pub_url,
    fetch_archive, fetch_article_content,
    body_html_to_markdown,
    load_cached_article, save_cached_article,
    load_cached_archive, save_cached_archive,
    CACHE_DIR, AUTH_PATH,
)

# Output dirs
OUTPUT_BASE = Path(os.path.expanduser("~/substack_exports"))


# ========== Command handlers ==========

def cmd_auth(args):
    """Validate auth cookie and show account info."""
    cookie = load_auth()
    if not cookie:
        print("No auth cookie found.")
        print(f"Set one up with: stash auth --cookie \"s%3A...\"")
        print("Get the cookie from browser DevTools → Application → Cookies → substack.com → connect.sid")
        return 1

    if args.cookie:
        save_auth(args.cookie)
        cookie = args.cookie
        print("Auth cookie saved.")

    print("Validating auth cookie...")
    user = get_current_user(cookie)
    if user:
        print(f"✓ Auth valid!")
        print(f"  Handle: @{user.get('handle', '?')}")
        print(f"  Name:   {user.get('name', '?')}")
        print(f"  Email:  {user.get('email', '?')}")
        ppids = user.get('paid_publication_ids', [])
        if ppids:
            print(f"  Paid publications: {ppids}")
        else:
            print(f"  Paid publications: (none found in profile)")
        print(f"  Cookie file: {AUTH_PATH}")
        print(f"  Cookie expires: when you sign out or change password")
    else:
        print("✗ Auth failed — could not fetch user profile.")
        print("  The cookie may be expired or invalid.")
        print("  Re-export it from browser DevTools.")
        return 1

    return 0


def cmd_pubs(args):
    """List subscribed/add/remove publications."""
    cookie = load_auth()
    if not cookie:
        print("No auth cookie. Run 'stash auth --cookie ...' first.")
        return 1

    pubs_file = _get_pubs_file()
    known_pubs = _load_pubs(pubs_file)

    if args.add:
        pub = args.add.strip().lower()
        # Normalize: remove .substack.com suffix if given
        pub = re.sub(r'\.substack\.com$', '', pub)
        pub = re.sub(r'^https?://', '', pub)
        if pub not in known_pubs:
            known_pubs.append(pub)
            _save_pubs(pubs_file, known_pubs)
            print(f"Added: {pub}.substack.com")
        else:
            print(f"Already in list: {pub}.substack.com")
        return 0

    if args.remove:
        pub = args.remove.strip().lower()
        pub = re.sub(r'\.substack\.com$', '', pub)
        if pub in known_pubs:
            known_pubs.remove(pub)
            _save_pubs(pubs_file, known_pubs)
            print(f"Removed: {pub}.substack.com")
        else:
            print(f"Not in list: {pub}")
        return 0

    # List known pubs + try API discovery
    print("=== Discovering Subscribed Publications ===")
    
    # Try API discovery
    print("Scanning API...")
    api_pubs = discover_subscriptions(cookie)
    if api_pubs:
        print(f"\nAPI found {len(api_pubs)} publications:")
        for p in api_pubs:
            subdomain = p.get("subdomain", "")
            name = p.get("name", "")
            print(f"  {subdomain}.substack.com — {name}")
    else:
        print("  API returned no subscriptions.")
        print("  (Substack's internal API may not expose all subscriptions)")
    
    # List known pubs
    print(f"\n=== Your Known Publications ({len(known_pubs)}) ===")
    if known_pubs:
        for pub in known_pubs:
            print(f"  {pub}.substack.com")
    else:
        print("  (none added yet)")
        print("  Add with: stash pubs --add <publication-name>")

    # Print profile-based hints
    user = get_current_user(cookie)
    if user and user.get("paid_publication_ids"):
        print(f"\n  Hint: Your profile shows paid publication IDs:")
        print(f"  {user['paid_publication_ids']}")
        print(f"  Try: stash pubs --resolve (coming soon)")

    return 0


def cmd_fetch(args):
    """Fetch articles from a publication."""
    cookie = load_auth()
    if not cookie:
        print("No auth cookie. Run 'stash auth --cookie ...' first.")
        return 1

    if args.all:
        pubs_file = _get_pubs_file()
        pubs = _load_pubs(pubs_file)
        if not pubs:
            print("No publications in list. Add with: stash pubs --add <pub>")
            return 1
        for pub in pubs:
            print(f"\n{'='*60}")
            print(f"Fetching: {pub}.substack.com")
            print(f"{'='*60}")
            _fetch_single(pub, cookie, args)
    else:
        pub = _normalize_pub(args.pub)
        _fetch_single(pub, cookie, args)

    return 0


def _fetch_single(pub, cookie, args):
    """Fetch articles for a single publication."""
    base_display = resolve_pub_url(pub).replace("https://", "")
    
    # Check cache
    archive = load_cached_archive(pub) if not args.force else None
    
    if archive and not args.force:
        print(f"  Using cached archive ({len(archive)} posts)")
    else:
        print(f"  Fetching archive list...")
        archive = fetch_archive(pub, cookie)
        if not archive:
            print(f"  ✗ No posts found for {base_display}")
            print(f"    Check: does this publication exist? Is it paywalled?")
            return
        print(f"  Found {len(archive)} posts total")
        save_cached_archive(pub, archive)

    # Filter by date
    if args.since:
        from datetime import datetime
        try:
            since_dt = datetime.fromisoformat(args.since)
            archive = [p for p in archive if p.get("post_date", "") >= args.since]
            print(f"  After filtering: {len(archive)} posts since {args.since}")
        except ValueError:
            print(f"  Invalid date format: {args.since} (use YYYY-MM-DD)")
            return

    # Limit
    if args.limit:
        archive = archive[:args.limit]

    # Fetch each article
    total = len(archive)
    success = 0
    cached = 0

    for i, post in enumerate(archive, 1):
        slug = post["slug"]
        title = post.get("title", slug)

        # Check cache
        cached_data = load_cached_article(pub, slug)
        if cached_data and not args.force:
            print(f"  [{i}/{total}] {slug} (cached)")
            cached += 1
            continue

        print(f"  [{i}/{total}] Fetching: {slug}...", end=" ", flush=True)
        
        content = fetch_article_content(pub, slug, cookie)
        if not content or not content.get("body_html"):
            print("✗ no content")
            continue

        body = content["body_html"]
        article_title = content.get("title", title)
        
        print(f"✓ {len(body)} chars" + 
              (" (paywalled)" if content.get("is_paywalled") else "") +
              (f" ({content.get('page_count',1)} pages)" if content.get('page_count',1) > 1 else ""))

        # Cache raw data
        save_cached_article(pub, slug, {
            "slug": slug,
            "title": article_title,
            "post_date": post.get("post_date", ""),
            "body_html_length": len(body),
            "is_paywalled": content.get("is_paywalled", False),
            "raw_body_html_saved": True,
        })

        success += 1
        time.sleep(0.4)

    print(f"\n  Done: {success} new, {cached} cached, {total} total")

    # Auto-export if any new content was fetched
    if success > 0:
        print(f"  Run 'stash export {pub} --format md' to generate markdown files")


def cmd_export(args):
    """Export fetched articles as markdown/PDF."""
    pub = _normalize_pub(args.pub)
    cookie = load_auth()

    # Get the list of what we've cached
    archive = load_cached_archive(pub)
    if not archive:
        print(f"No cached archive for {pub}.substack.com")
        print(f"Run 'stash fetch {pub}' first")
        return 1

    # Filter to specific slug if requested
    if args.slug:
        archive = [p for p in archive if p["slug"] == args.slug]
        if not archive:
            print(f"Slug '{args.slug}' not found in archive")
            return 1

    fmt = args.format or "both"

    # Create output directory
    out_dir = OUTPUT_BASE / pub
    md_dir = out_dir / "markdown"
    pdf_dir = out_dir / "pdf"

    if fmt in ("md", "both"):
        md_dir.mkdir(parents=True, exist_ok=True)
    if fmt in ("pdf", "both"):
        pdf_dir.mkdir(parents=True, exist_ok=True)
        try:
            from fpdf import FPDF
            has_fpdf = True
        except ImportError:
            print("Warning: fpdf2 not installed. PDF export unavailable.")
            print("Install: pip3 install --break-system-packages fpdf2")
            has_fpdf = False

    total = len(archive)
    exported = 0

    for i, post in enumerate(archive, 1):
        slug = post["slug"]
        title = post.get("title", slug)

        # Check if we have raw cached data
        cached = load_cached_article(pub, slug)
        if not cached:
            print(f"  [{i}/{total}] {slug} — not fetched yet, skipping")
            continue

        # Fetch or use cached body_html
        print(f"  [{i}/{total}] Converting: {slug}...", end=" ", flush=True)
        
        content = fetch_article_content(pub, slug, cookie)
        if not content or not content.get("body_html"):
            print("✗ no content")
            continue

        body_html = content["body_html"]
        article_title = content.get("title", title)

        # Convert to markdown
        md_text = body_html_to_markdown(body_html)
        if not md_text:
            print("✗ conversion failed")
            continue

        # Save markdown
        if fmt in ("md", "both"):
            md_path = md_dir / f"{slug}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"# {article_title}\n\n")
                f.write(f"> {post.get('post_date', '')}\n\n")
                f.write(md_text)
            print(f"md ({len(md_text)} chars)", end="")

        # Generate PDF
        if fmt in ("pdf", "both") and has_fpdf:
            try:
                _generate_pdf(md_text, article_title, slug, pdf_dir)
                print(" + pdf", end="")
            except Exception as e:
                print(f" + pdf FAILED: {e}", end="")

        print()
        exported += 1
        time.sleep(0.3)

    print(f"\n  Done: {exported}/{total} exported")
    print(f"  Output: {out_dir}")

    return 0


def _generate_pdf(markdown, title, slug, out_dir):
    """Generate a clean text-only PDF from markdown text.
    Handles proper paragraph spacing, justified text, headings."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, 20)
    
    # Try DejaVu, fall back to built-in
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    if os.path.exists(font_path):
        pdf.add_font("DejaVu", "", font_path)
        pdf.add_font("DejaVu", "B", font_bold_path)
        font_family = "DejaVu"
    else:
        font_family = "Courier"

    mw = pdf.w - pdf.l_margin - pdf.r_margin

    def sanitize(text):
        for ch in "\u200b\u200c\u200d\u2060\ufeff\u200e\u200f":
            text = text.replace(ch, "")
        text = text.replace("\u2013", "-").replace("\u2014", "--")
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        text = text.replace("\u2026", "...").replace("\u00a0", " ")
        return text

    def write_paragraph(text, sz=10, bold=False):
        """Write a paragraph as a justified block with word-wrap."""
        text = sanitize(text)
        if not text.strip():
            pdf.ln(4)
            return
        
        style = "B" if bold else ""
        pdf.set_font(font_family, style, sz)
        
        # Word-wrap and justify the paragraph
        words = text.split()
        if not words:
            pdf.ln(4)
            return
        
        buf = []
        line_width = 0
        space_w = pdf.get_string_width(" ")
        
        for word in words:
            w_w = pdf.get_string_width(word)
            if line_width + w_w + (space_w if buf else 0) > mw and buf:
                # Flush current line
                line = " ".join(buf)
                if len(buf) > 1 and sz <= 11:
                    # Justify
                    total_w = sum(pdf.get_string_width(w) for w in buf)
                    gap = (mw - total_w) / (len(buf) - 1)
                    x = pdf.l_margin
                    for w in buf:
                        pdf.set_xy(x, pdf.get_y())
                        pdf.cell(pdf.get_string_width(w), 5.5, w)
                        x += pdf.get_string_width(w) + gap
                    pdf.ln(5.5)
                else:
                    pdf.multi_cell(0, 5.5, line)
                buf = [word]
                line_width = w_w
            else:
                buf.append(word)
                line_width += w_w + space_w
        
        if buf:
            pdf.multi_cell(0, 5.5, " ".join(buf))
    
    # Title
    if title:
        pdf.set_font(font_family, "B", 14)
        pdf.multi_cell(0, 7, sanitize(title), align="C")
        pdf.ln(5)
    
    # Process markdown paragraph by paragraph
    paragraphs = markdown.split("\n\n")
    
    for para in paragraphs:
        if pdf.get_y() > 260:
            pdf.add_page()
        
        para = para.strip()
        if not para:
            continue
        
        lines = para.split("\n")
        first_line = lines[0].strip() if lines else ""
        
        # Skip boilerplate
        if any(first_line.startswith(x) for x in ["Subscribe", "FUNDRAISING", "Click here", "This below is"]):
            continue
        
        # Heading
        if first_line.startswith("#"):
            heading = para.lstrip("#").strip()
            pdf.set_font(font_family, "B", 12)
            pdf.multi_cell(0, 6, sanitize(heading))
            pdf.ln(2)
        else:
            # Regular paragraph — rejoin lines into one block
            text = " ".join(line.strip() for line in lines if line.strip())
            write_paragraph(text)
            pdf.ln(2)

    fpath = out_dir / f"{slug}.pdf"
    pdf.output(str(fpath))
    return fpath

    fpath = out_dir / f"{slug}.pdf"
    pdf.output(str(fpath))
    return fpath


def cmd_list(args):
    """List cached articles for a publication."""
    pub = _normalize_pub(args.pub)
    archive = load_cached_archive(pub)
    
    if not archive:
        print(f"No cached archive for {pub}.substack.com")
        print("Run 'stash fetch' first")
        return 1

    print(f"Cached articles for {pub}.substack.com:")
    print(f"{'Slug':<45} {'Date':<15} {'Cached':<8} {'Size':<8}")
    print("-" * 76)
    
    total_chars = 0
    for post in archive:
        slug = post["slug"]
        date = post.get("post_date", "")[:10]
        cached = load_cached_article(pub, slug)
        cached_str = "✓" if cached else "—"
        size = f"{cached.get('body_html_length', 0):,}" if cached else ""
        total_chars += cached.get("body_html_length", 0) if cached else 0
        print(f"{slug:<45} {date:<15} {cached_str:<8} {size:<8}")

    total = len(archive)
    fetched = sum(1 for p in archive if load_cached_article(pub, p["slug"]))
    print(f"\n{total} total, {fetched} fetched, ~{total_chars:,} chars")

    return 0


def cmd_status(args):
    """Show overall cache status."""
    cookie = load_auth()
    auth_ok = cookie is not None

    print("=== Substack Paywall Export Status ===")
    print(f"  Auth cookie: {'✓ present' if auth_ok else '✗ missing'}")
    if auth_ok:
        user = get_current_user(cookie)
        if user:
            print(f"  Account: @{user.get('handle', '?')} ({user.get('name', '?')})")
    
    # Cache stats
    if CACHE_DIR.exists():
        total_size = sum(
            f.stat().st_size for f in CACHE_DIR.rglob("*") if f.is_file()
        )
        total_files = sum(1 for f in CACHE_DIR.rglob("*") if f.is_file())
        pubs = set()
        for f in CACHE_DIR.iterdir():
            if f.is_dir():
                pubs.add(f.name)
            elif f.name.endswith("_archive.json"):
                pubs.add(f.name.replace("_archive.json", ""))

        print(f"  Cache dir: {CACHE_DIR}")
        print(f"  Cached publications: {len(pubs)}")
        print(f"  Cache files: {total_files}")
        print(f"  Cache size: {total_size / 1024:.1f} KB")
        
        for pub in sorted(pubs)[:10]:
            pub_dir = CACHE_DIR / pub
            n_articles = len(list(pub_dir.glob("*.json"))) if pub_dir.is_dir() else 0
            archive = load_cached_archive(pub)
            n_total = len(archive) if archive else 0
            print(f"    {pub}.substack.com: {n_articles} articles cached of {n_total} total")
    else:
        print(f"  Cache: empty")

    print(f"\n  Output dir: {OUTPUT_BASE}")
    exports = list(OUTPUT_BASE.iterdir()) if OUTPUT_BASE.exists() else []
    if exports:
        print(f"  Exports: {len(exports)} publications")
        for d in exports:
            if d.is_dir():
                md_files = len(list((d / "markdown").glob("*.md"))) if (d / "markdown").exists() else 0
                pdf_files = len(list((d / "pdf").glob("*.pdf"))) if (d / "pdf").exists() else 0
                print(f"    {d.name}: {md_files} md, {pdf_files} pdf")

    return 0


def cmd_clean(args):
    """Remove exported files, keep raw cache."""
    if not OUTPUT_BASE.exists():
        print("No exports to clean")
        return 0

    import shutil
    total = 0
    for d in OUTPUT_BASE.iterdir():
        if d.is_dir():
            for sub in d.iterdir():
                if sub.is_dir():
                    count = len(list(sub.rglob("*")))
                    shutil.rmtree(sub)
                    total += count
    print(f"Cleaned {total} exported files (raw cache preserved)")


def cmd_resolve(args):
    """Resolve paidPublicationIds to publication names."""
    cookie = load_auth()
    if not cookie:
        print("No auth cookie.")
        return 1

    user = get_current_user(cookie)
    if not user or not user.get("paid_publication_ids"):
        print("No paid publication IDs found in profile.")
        return 1

    print(f"Found {len(user['paid_publication_ids'])} publication IDs:")
    for pid in user["paid_publication_ids"]:
        # Try to resolve by fetching the publication's home page
        # We can try a few known subdomains or search
        print(f"  ID: {pid} — (unable to auto-resolve)")
        print(f"    Try browsing: https://substack.com/@untaprando to see your subscriptions")

    return 0


# ========== Helpers ==========

def _normalize_pub(pub):
    """Normalize a publication identifier to its subdomain name."""
    pub = pub.strip().lower()
    pub = re.sub(r'\.substack\.com$', '', pub)
    pub = re.sub(r'^https?://', '', pub)
    pub = re.sub(r'^www\.', '', pub)
    return pub


def _get_pubs_file():
    """Get path to the known publications list."""
    cfg = Path(os.path.expanduser("~/.hermes/config"))
    cfg.mkdir(parents=True, exist_ok=True)
    return cfg / "substack_pubs.json"


def _load_pubs(path):
    """Load known publications list."""
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            pass
    return []


def _save_pubs(path, pubs):
    """Save known publications list."""
    with open(path, "w") as f:
        json.dump(pubs, f, indent=2)


# ========== Main ==========

def main():
    parser = argparse.ArgumentParser(
        description="Substack Paywall Export CLI",
        usage="stash <command> [options]",
    )
    parser.add_argument("--cookie", help="Set Substack connect.sid cookie")

    sub = parser.add_subparsers(dest="command", help="Command")

    # auth
    p_auth = sub.add_parser("auth", help="Validate cookie and show account info")
    p_auth.add_argument("--cookie", help="Set Substack connect.sid cookie")

    # pubs
    p_pubs = sub.add_parser("pubs", help="List subscribed publications")
    p_pubs.add_argument("--add", help="Add a publication (subdomain name)")
    p_pubs.add_argument("--remove", help="Remove a publication")
    p_pubs.add_argument("--resolve", action="store_true", help="Resolve paid publication IDs")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Fetch articles from a publication")
    p_fetch.add_argument("pub", nargs="?", help="Publication subdomain name")
    p_fetch.add_argument("--since", help="Only articles since date (YYYY-MM-DD)")
    p_fetch.add_argument("--limit", type=int, help="Max number of articles")
    p_fetch.add_argument("--force", action="store_true", help="Re-fetch even if cached")
    p_fetch.add_argument("--all", action="store_true", help="Fetch all known publications")

    # export
    p_export = sub.add_parser("export", help="Export articles as markdown/PDF")
    p_export.add_argument("pub", help="Publication subdomain name")
    p_export.add_argument("--format", choices=["md", "pdf", "both"], help="Output format")
    p_export.add_argument("--slug", help="Export a single article by slug")

    # list
    p_list = sub.add_parser("list", help="List cached articles")
    p_list.add_argument("pub", nargs="?", help="Publication subdomain name")

    # status
    sub.add_parser("status", help="Show cache status")

    # clean
    sub.add_parser("clean", help="Remove exported files (keep raw cache)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "auth": cmd_auth,
        "pubs": cmd_pubs,
        "fetch": cmd_fetch,
        "export": cmd_export,
        "list": cmd_list,
        "status": cmd_status,
        "clean": cmd_clean,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
