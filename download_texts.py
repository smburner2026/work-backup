#!/usr/bin/env python3
"""
Download Ian Johnston's translations of Nietzsche's works,
strip HTML tags, clean whitespace, and save as plain text.
"""
import urllib.request
import re
import os
import sys

def fetch_url(url):
    """Fetch a URL with a browser-like User-Agent."""
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    return html

def strip_html(html):
    """Strip HTML tags and clean up whitespace."""
    # Remove script and style elements
    html = re.sub(r'(?is)<script[^>]*>.*?</script>', '', html)
    html = re.sub(r'(?is)<style[^>]*>.*?</style>', '', html)
    # Remove HTML comments
    html = re.sub(r'(?is)<!--.*?-->', '', html)
    # Replace <br> and <p> with newlines
    html = re.sub(r'(?is)<br\s*/?>', '\n', html)
    html = re.sub(r'(?is)</p>', '\n\n', html)
    html = re.sub(r'(?is)<div[^>]*>', '\n', html)
    html = re.sub(r'(?is)</div>', '\n', html)
    html = re.sub(r'(?is)<tr[^>]*>', '\n', html)
    html = re.sub(r'(?is)<td[^>]*>', '\t', html)
    html = re.sub(r'(?is)</td>', '', html)
    html = re.sub(r'(?is)</tr>', '\n', html)
    html = re.sub(r'(?is)<li[^>]*>', '\n* ', html)
    # Remove all other tags
    html = re.sub(r'<[^>]+>', '', html)
    # Decode common HTML entities
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&quot;', '"')
    html = html.replace('&#39;', "'")
    html = html.replace('&mdash;', '—')
    html = html.replace('&ndash;', '–')
    html = html.replace('&rsquo;', "'")
    html = html.replace('&lsquo;', "'")
    html = html.replace('&rdquo;', '"')
    html = html.replace('&ldquo;', '"')
    # Normalize whitespace: collapse multiple newlines to max 2
    html = re.sub(r'\n{3,}', '\n\n', html)
    # Collapse multiple spaces/tabs within lines
    html = re.sub(r'[ \t]+', ' ', html)
    # Strip leading/trailing whitespace
    html = html.strip()
    return html

def main():
    outdir = '/root/work/nietzsche-anthology/sources'
    os.makedirs(outdir, exist_ok=True)

    # --- 1. The Birth of Tragedy ---
    print("Fetching The Birth of Tragedy...")
    bot_html = fetch_url('http://johnstoniatexts.x10host.com/nietzsche/tragedyhtml.html')
    print(f"  Got {len(bot_html)} bytes of HTML")
    bot_text = strip_html(bot_html)
    print(f"  Stripped to {len(bot_text)} chars")
    outfile1 = os.path.join(outdir, 'birth_of_tragedy_johnston.txt')
    with open(outfile1, 'w', encoding='utf-8') as f:
        f.write(bot_text)
    print(f"  Saved to {outfile1}")

    # --- 2. Use and Abuse of History ---
    print("Fetching Use and Abuse of History...")
    uah_html = fetch_url('http://johnstoniatexts.x10host.com/nietzsche/historyhtml.html')
    print(f"  Got {len(uah_html)} bytes of HTML")
    uah_text = strip_html(uah_html)
    print(f"  Stripped to {len(uah_text)} chars")
    outfile2 = os.path.join(outdir, 'use_abuse_history_johnston.txt')
    with open(outfile2, 'w', encoding='utf-8') as f:
        f.write(uah_text)
    print(f"  Saved to {outfile2}")

    print("\nDone! Files:")
    for f in [outfile1, outfile2]:
        size = os.path.getsize(f)
        lines = sum(1 for _ in open(f, 'r'))
        print(f"  {f} — {size:,} bytes, {lines:,} lines")

if __name__ == '__main__':
    main()
