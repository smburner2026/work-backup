#!/usr/bin/env python3
"""
Compile Nolte chapter markdown files into PDFs.
Style: early 20th century history textbook — Liberation Serif, justified, dignified.
"""
import os, re

from fpdf import FPDF

MD_DIR = "/home/vthen/work/nolte_md"
PDF_DIR = "/home/vthen/work/nolte_pdf"

# Liberation Serif = metrically identical to Times New Roman
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

FONT_SIZE = 11       # body text
LEADING = 5.5         # line height
MARGIN = 25           # mm — generous textbook margins


class TextbookPDF(FPDF):
    def __init__(self, title):
        super().__init__()
        self.chapter_title = title
        self.add_font("Serif", "", FONT_REG)
        self.add_font("Serif", "B", FONT_BOLD)
        self.add_font("Serif", "I", FONT_ITALIC)
        self.add_font("Serif", "BI", FONT_BI)
        self.set_auto_page_break(True, MARGIN)
        self.set_margin(MARGIN)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Serif", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, self.chapter_title, align="C")
            self.ln(6)

    def footer(self):
        self.set_y(-MARGIN + 5)
        self.set_font("Serif", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, str(self.page_no()), align="C")

    def add_title_page(self, title):
        """Centered chapter title — classic style."""
        self.add_page()
        self.ln(40)
        self.set_font("Serif", "B", 18)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 10, title, align="C")
        self.ln(8)
        # Decorative rule
        x = self.get_x()
        w = self.w - 2 * MARGIN
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(MARGIN, self.get_y(), MARGIN + w, self.get_y())
        self.ln(12)

    def write_body(self, md_text):
        """Parse markdown and render as textbook body."""
        lines = md_text.split("\n")
        i = 0

        # Peek at first content line for title detection
        first = ""
        for l in lines:
            ls = l.strip()
            if ls and not ls.startswith(">"):
                first = ls
                break

        while i < len(lines):
            line = lines[i].strip()
            i += 1

            # Ensure we have a page before writing
            if self.page == 0:
                self.add_page()

            if not line:
                self.ln(2)
                continue

            # Chapter title (# ...)
            if line.startswith("# ") and not line.startswith("## "):
                title = line[2:].strip()
                self.add_title_page(title)
                continue

            # Bold title without # (some chapters use **Title** on first line)
            if line == first and re.match(r'^\*\*.+\*\*$', line) and self.page == 1:
                title = line.strip("*")
                self.add_title_page(title)
                continue

            # Section heading (### ...)
            if line.startswith("### "):
                heading = line[4:].strip()
                self.ln(4)
                self.set_font("Serif", "B", 12)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 7, heading)
                self.ln(2)
                continue

            # Sub-heading (### followed by text — sometimes appears as plain bold)
            if line.startswith("## "):
                heading = line[3:].strip()
                self.ln(3)
                self.set_font("Serif", "B", 13)
                self.multi_cell(0, 7, heading)
                self.ln(2)
                continue

            # Horizontal rules or separator lines — skip
            if re.match(r'^[-*_=]{3,}$', line):
                self.ln(2)
                continue

            # Blockquote — indent and italicize
            if line.startswith("> "):
                self._write_blockquote(lines, i - 1)
                while i < len(lines) and lines[i].strip().startswith("> "):
                    i += 1
                self.ln(3)
                continue

            # Numbered list item
            if re.match(r'^\d+\.\s', line):
                self._write_paragraph(line, indent=8)
                continue

            # Regular paragraph
            self._write_paragraph(line)

    def _write_paragraph(self, text, indent=0):
        """Write a paragraph with bold/italic inline formatting, justified."""
        self.set_font("Serif", "", FONT_SIZE)
        self.set_text_color(0, 0, 0)
        self.set_x(MARGIN + indent)

        # Parse inline markdown: **bold**, *italic*, **_bold-italic_**
        tokens = self._tokenize_inline(text)
        line_buf = ""
        line_width = self.w - 2 * MARGIN - indent

        first = True
        for token_text, token_style in tokens:
            self.set_font("Serif", token_style, FONT_SIZE)
            words = token_text.split(" ")
            for j, word in enumerate(words):
                test = (line_buf + " " + word).strip() if line_buf else word
                test_w = self.get_string_width(test)
                if test_w > line_width and line_buf:
                    # Justify the line (except last line of paragraph)
                    self._write_justified_line(line_buf, line_width, first)
                    first = False
                    line_buf = word
                else:
                    line_buf = test

        if line_buf:
            # Last line of paragraph — left-aligned, no justification
            self.set_x(MARGIN + indent)
            self.set_font("Serif", "", FONT_SIZE)
            self.cell(0, LEADING, line_buf)
            self.ln()

        self.ln(1)

    def _write_justified_line(self, text, max_width, is_first):
        """Write a single justified line with precise word spacing."""
        self.set_x(MARGIN)
        if is_first:
            indent = 0  # First line already handled
        else:
            indent = 0
            self.set_x(MARGIN)

        words = text.split()
        if len(words) == 1:
            self.set_font("Serif", "", FONT_SIZE)
            self.cell(max_width, LEADING, words[0])
            self.ln()
            return

        # Measure total word width
        word_widths = [self.get_string_width(w) for w in words]
        total_words = sum(word_widths)
        space_needed = max_width - total_words
        space_count = len(words) - 1
        space_width = max(0, space_needed / space_count)

        self.set_font("Serif", "", FONT_SIZE)
        x = MARGIN
        for k, word in enumerate(words):
            self.set_xy(x, self.get_y())
            self.cell(word_widths[k], LEADING, word)
            x += word_widths[k]
            if k < space_count:
                x += space_width
        self.ln()

    def _tokenize_inline(self, text):
        """Split text into (string, style) tokens. Styles: '' 'B' 'I' 'BI'"""
        tokens = []
        # Pattern: **_text_** (bold-italic), **text** (bold), *text* (italic)
        pattern = r'(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*)'
        last = 0
        for m in re.finditer(pattern, text):
            if m.start() > last:
                tokens.append((text[last:m.start()], ""))
            if m.group(1).startswith("***"):
                tokens.append((m.group(2), "BI"))
            elif m.group(1).startswith("**"):
                tokens.append((m.group(3), "B"))
            else:
                tokens.append((m.group(4), "I"))
            last = m.end()
        if last < len(text):
            tokens.append((text[last:], ""))
        return tokens

    def _write_blockquote(self, lines, start_idx):
        """Write a blockquote section — indented, smaller, italic."""
        self.ln(2)
        quote_lines = []
        while start_idx < len(lines) and lines[start_idx].strip().startswith("> "):
            quote_lines.append(lines[start_idx].strip()[2:])
            start_idx += 1
        quote_text = " ".join(quote_lines)

        # Indented italic block
        self.set_font("Serif", "I", FONT_SIZE - 1)
        self.set_text_color(60, 60, 60)
        self.set_x(MARGIN + 12)
        w = self.w - 2 * MARGIN - 12
        self.multi_cell(w, LEADING, quote_text)
        self.set_text_color(0, 0, 0)


def sanitize(text):
    """Replace characters that Liberation Serif can't render."""
    for ch in "\u200b\u200c\u200d\u2060\ufeff\u200e\u200f":
        text = text.replace(ch, "")
    return text


def compile_all():
    os.makedirs(PDF_DIR, exist_ok=True)
    md_files = sorted(f for f in os.listdir(MD_DIR) if f.endswith(".md"))
    total = len(md_files)

    for i, fname in enumerate(md_files, 1):
        slug = fname[:-3]
        fpath = os.path.join(MD_DIR, fname)
        with open(fpath, encoding="utf-8") as f:
            md_text = sanitize(f.read())

        # Extract title from first # heading
        title = slug.replace("-", " ").title()
        m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
        if m:
            title = m.group(1).strip()

        print(f"[{i}/{total}] {slug}")

        pdf = TextbookPDF(title)
        pdf.write_body(md_text)

        out_path = os.path.join(PDF_DIR, f"{slug}.pdf")
        pdf.output(out_path)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  -> {out_path} ({len(md_text):,} chars -> {size_kb:.0f} KB)")

    print(f"\nDone: {total} PDFs -> {PDF_DIR}/")


if __name__ == "__main__":
    compile_all()