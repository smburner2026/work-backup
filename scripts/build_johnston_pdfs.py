#!/usr/bin/env python3
"""
Build individual clean PDFs for Ian Johnston's Nietzsche translations.
Style: same FPDF pipeline as the Nolte book.
"""
import os, re, sys

from fpdf import FPDF

SRC = "/root/work/nietzsche-anthology/sources"
OUTDIR = "/root/work"

FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

FONT_SIZE = 12
LEADING = 6.5
MARGIN = 25


def read_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


# ─── BOILERPLATE PATTERNS ───────────────────────────────────────

BOILERPLATE_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r'^To download a Rich Text Format',
        r'^For a Rich Text Version',
        r'^Rich Text Format',
        r'^please use the following link',
        r'^For a PDF file',
        r'^For information on copyright',
        r'^Students, teachers, artists',
        r'^general public may download',
        r'^without permission and without charge',
        r'^freely edit the text',
        r'^All commercial use',
        r'^commercial use of this translation',
        r'^forbidden without the permission',
        r'^for any questions or comments',
        r'^Ian Johnston\b',
        r'^Vancouver Island University',
        r'^Nanaimo, British Columbia',
        r'^Note that in the following text.*square brackets',
        r'^words within square brackets',
        r'^added by the translator',
        r'^numbers in curved brackets',
        r'^explanatory endnotes',
        r'^Nietzsche.*\[RTF\]',
        r'^Prologue\. \[RTF\]',
        r'^Genealogy, Table of Contents',
        r'^\[Revised Edition',
        r'^\[RTF\]',
        r'^\[Table of Contents',
        r'^Canada.$',
        r'\[RTF\]',  # Any line mentioning RTF
    ]
]

BOILERPLATE_LINES = {
    "Friedrich Nietzsche", "BEYOND GOOD AND EVIL", "BEYOND GOOD AND EVIL ",
    "Translated by Ian Johnston,", "Translated by Ian Johnston",
    "Vancouver Island University,", "Vancouver Island University",
    "Nanaimo, British Columbia, Canada.", "Nanaimo, British Columbia, Canada",
    "Students, teachers, artists, and members of the",
    "general public may download and distribute this text without permission and",
    "without charge. They may also freely edit the text for their own purposes. All",
    "commercial use of this translation, however, is forbidden without the permission",
    "of the translator. For comments and questions, please contact",
    "Ian Johnston.",
    "Ian Johnston.",
    "¬†", "Translated by Ian Johnston, Vancouver Island University,",
    "Nanaimo, British Columbia, Canada",
    "Canada.",
    "Nietzsche,",
    "History [RTF]",
    "use the following link:",
    "Please use the following link:",
    "For a Rich Text Format (Word) of this text,",
    "please use the following link:",
    "[Students, teachers, artists, and members of the",
    "general public may download and distribute this text free of charge and without",
    "permission. They may also freely edit the text to suit their purposes. However,",
    "no commercial publication of this text or any part of it is permitted without",
    "permission of the translator. For any questions or comments please contact",
    "Note that in the following text, the words within",
    "square brackets have been added by the translator. The numbers in curved",
    "brackets indicate links to explanatory endnotes provided by the translator.]",
}


def is_boilerplate_line(stripped):
    if not stripped:
        return False
    # Strip non-breaking spaces too
    cleaned = stripped.replace('\xa0', '')
    for pat in BOILERPLATE_PATTERNS:
        if pat.search(cleaned):
            return True
    if cleaned in BOILERPLATE_LINES:
        return True
    # Also check if stripped (without \xa0) starts with any common heading
    if cleaned.startswith('PART ') or cleaned.startswith('ON THE PREJUDICES'):
        return False  # These are actual part headings, keep them
    # Catch any line mentioning [RTF], [Table, of Contents, or copyright year
    if '[RTF]' in cleaned or '[Table' in cleaned or 'of Contents' in cleaned:
        return True
    # Catch copyright year lines and download boilerplate
    if cleaned in ('2014',) or cleaned.startswith('If you '):
        return True
    # Catch "Nietzsche, Genealogy" boilerplate headers
    if cleaned.startswith('Nietzsche, Genealogy'):
        return True
    return False


def strip_boilerplate_block(text):
    """Remove boilerplate paragraphs from text."""
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if is_boilerplate_line(stripped):
            continue
        if re.match(r'^={10,}$', stripped):
            continue
        result.append(line)
    return '\n'.join(result)


def strip_footnote_markers(text):
    text = re.sub(r'\{[0-9]+\}', '', text)
    text = re.sub(r'\([0-9]+\)', '', text)
    text = re.sub(r'\[Back\s+to\s+Text\]', '', text)
    return text


def strip_endnotes_sections(text):
    """Remove NOTES sections from text (between content and next divider)."""
    # Remove NOTES followed by endnotes until next ===== or end of text
    text = re.sub(r'\n\s*NOTES\s*\n.*?(\n={5,}\n|\Z)', r'\1', text, flags=re.DOTALL)
    return text


def clean_generic(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Remove non-breaking spaces on otherwise-empty lines (they break \n\n detection)
    text = re.sub(r'\n\xa0\n', '\n\n', text)
    # Collapse 4+ newlines to 3 (keeps \n\n paragraph breaks intact)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


# ─── WORK CLEANERS ──────────────────────────────────────────────

def clean_birth(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = strip_boilerplate_block(text)
    idx = text.find("THE BIRTH OF TRAGEDY")
    if idx >= 0:
        text = text[idx:]
    else:
        print("  WARNING: 'THE BIRTH OF TRAGEDY' marker not found!")
    idx = text.find("ENDNOTES")
    if idx >= 0:
        text = text[:idx]
    text = strip_footnote_markers(text)
    return clean_generic(text)


def clean_bge(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Find PROLOGUE in the RAW text (before any stripping)
    idx = text.find("PROLOGUE")
    if idx >= 0:
        text = text[idx:]
    
    # Split by ===== section dividers FIRST (before stripping them)
    sections = re.split(r'\n={5,}\n', text)
    
    # Process each section
    cleaned_sections = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        
        lines = sec.split('\n')
        first = lines[0].strip() if lines else ""
        
        if len(sec) < 200 and first:
            # Short section = Part heading
            cleaned_sections.append(("heading", first))
        else:
            # Long section: strip boilerplate, NOTES, markers
            sec = strip_boilerplate_block(sec)
            sec = strip_endnotes_sections(sec)
            sec = re.sub(r'\n\s*BEYOND GOOD AND EVIL\s*\n', '\n', sec)
            sec = re.sub(r'^Friedrich Nietzsche\s*\n?', '', sec, flags=re.MULTILINE)
            sec = strip_footnote_markers(sec)
            sec = clean_generic(sec)
            if sec:
                cleaned_sections.append(("content", sec))
    
    return cleaned_sections


def clean_genealogy(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Find the real "Prologue" heading (last occurrence or standalone)
    matches = list(re.finditer(r'^Prologue\s*$', text, re.MULTILINE))
    if matches:
        pos = matches[-1].start()
        text = text[pos:]
    else:
        idx = text.find("Prologue")
        if idx >= 0:
            text = text[idx:]
    
    # Strip ALL endnotes sections (embedded between essays and trailing)
    # Remove from each ENDNOTES line to the next essay heading or end of text
    text = re.sub(
        r'\n\s*ENDNOTES\s*\n.*?(?=\nFirst\s+Essay|\nSecond\s+Essay|\nThird\s+Essay|\Z)',
        '\n',
        text,
        flags=re.DOTALL
    )
    
    # Now strip boilerplate blocks (copyright, download links, etc.)
    text = strip_boilerplate_block(text)
    text = strip_footnote_markers(text)
    text = re.sub(r'^Friedrich Nietzsche\s*\n?', '', text, flags=re.MULTILINE)
    return clean_generic(text)


def clean_use_abuse(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Find "PREFACE" in RAW text (before stripping - it's the real content start)
    idx = text.find("PREFACE")
    if idx >= 0:
        text = text[idx:]
    
    text = strip_boilerplate_block(text)
    
    text = strip_footnote_markers(text)
    text = re.sub(r'^Friedrich Nietzsche\s*\n?', '', text, flags=re.MULTILINE)
    return clean_generic(text)


# ─── FPDF ───────────────────────────────────────────────────────

class JohnstonPDF(FPDF):
    def __init__(self, work_title, work_subtitle, author, translator):
        super().__init__(format=(152.4, 228.6))  # 6" × 9" in mm
        self.book_title = work_title
        self.book_subtitle = work_subtitle
        self.book_author = author
        self.book_translator = translator
        self.add_font("Serif", "", FONT_REG)
        self.add_font("Serif", "B", FONT_BOLD)
        self.add_font("Serif", "I", FONT_ITALIC)
        self.add_font("Serif", "BI", FONT_BI)
        self.set_auto_page_break(True, MARGIN)
        self.set_margin(MARGIN)
        self.current_heading = work_title

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("Serif", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, self.current_heading, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-MARGIN + 5)
        self.set_font("Serif", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, str(self.page_no()), align="C")

    def add_title_page(self):
        self.add_page()
        self.ln(50)
        self.set_font("Serif", "B", 22)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 12, self.book_title, align="C")
        self.ln(4)
        if self.book_subtitle:
            self.set_font("Serif", "I", 14)
            self.multi_cell(0, 8, self.book_subtitle, align="C")
            self.ln(6)
        self.ln(4)
        x = self.l_margin
        w = self.w - 2 * self.l_margin
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(10)
        self.set_font("Serif", "", 11)
        self.multi_cell(0, 6, self.book_author, align="C")
        self.ln(4)
        self.set_font("Serif", "I", 10)
        self.multi_cell(0, 6, self.book_translator, align="C")

    def add_part_heading(self, heading):
        self.add_page()
        self.ln(20)
        self.set_font("Serif", "B", 14)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 9, heading, align="C")
        self.ln(4)
        x = self.l_margin
        w = self.w - 2 * self.l_margin
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(12)

    def write_body(self, text):
        """Write body text with paragraph handling."""
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                self.ln(LEADING / 2)
                continue

            lines = para.split('\n')
            first = lines[0].strip()

            # Skip horizontal rules
            if re.match(r'^[=\-*_]{10,}$', first):
                self.ln(2)
                x = self.l_margin
                w = self.w - 2 * self.l_margin
                y = self.get_y()
                self.set_draw_color(150, 150, 150)
                self.set_line_width(0.2)
                self.line(x, y, x + w, y)
                self.set_draw_color(80, 80, 80)
                self.ln(4)
                continue

            # Section number (standalone digit)
            if re.match(r'^\d+$', first) and len(first) <= 4:
                self.ln(2)
                self.set_font("Serif", "B", 12)
                self.set_text_color(0, 0, 0)
                self.cell(0, LEADING + 1, first)
                self.ln(LEADING + 2)
                continue

            # All-caps heading
            if (first.isupper() and len(first) > 4 and len(first) < 100 
                and '[' not in first):
                self.ln(4)
                self.set_font("Serif", "B", 13)
                self.set_text_color(0, 0, 0)
                self.multi_cell(0, 7, first, align="C")
                self.ln(3)
                # Render remaining lines as body text (don't continue — lines[1:] has the content)
                if len(lines) > 1:
                    rest = ' '.join(l.strip() for l in lines[1:] if l.strip())
                    if rest:
                        self.write_paragraph(rest)
                        self.ln(LEADING / 2)
                continue

            # Regular paragraph
            self.write_paragraph(' '.join(line.strip() for line in lines))
            self.ln(LEADING / 2)

    def write_paragraph(self, text):
        """Justified paragraph with inline italic."""
        text = self.sanitize(text)
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            return

        segments = []
        last_end = 0
        for m in re.finditer(r'\*([^*]+)\*', text):
            segments.append(('normal', text[last_end:m.start()]))
            segments.append(('italic', m.group(1)))
            last_end = m.end()
        segments.append(('normal', text[last_end:]))

        if len(segments) == 1:
            self._render_justified(text)
        else:
            self._render_mixed(segments)

    def _render_justified(self, text):
        line_width = self.w - 2 * self.l_margin
        words = text.split()
        if not words:
            return
        self.set_font("Serif", "", FONT_SIZE)
        line_buf = ""
        for word in words:
            test = (line_buf + " " + word).strip() if line_buf else word
            if self.get_string_width(test) > line_width and line_buf:
                self._justify_line(line_buf, line_width)
                line_buf = word
            else:
                line_buf = test
        if line_buf:
            self.cell(0, LEADING, line_buf)
            self.ln()

    def _justify_line(self, text, max_width):
        words = text.split()
        if len(words) == 1:
            self.cell(max_width, LEADING, words[0])
            self.ln()
            return
        word_widths = [self.get_string_width(w) for w in words]
        space_count = len(words) - 1
        space_width = max(0, (max_width - sum(word_widths)) / space_count)
        self.set_font("Serif", "", FONT_SIZE)
        x = self.l_margin
        for k, word in enumerate(words):
            self.set_xy(x, self.get_y())
            self.cell(word_widths[k], LEADING, word)
            x += word_widths[k] + (space_width if k < space_count else 0)
        self.ln()

    def _render_mixed(self, segments):
        line_width = self.w - 2 * self.l_margin
        x0 = self.l_margin
        styled_tokens = []
        for style, text in segments:
            if not text.strip():
                continue
            self.set_font("Serif", "I" if style == "italic" else "", FONT_SIZE)
            for word in text.split():
                w = self.get_string_width(word)
                styled_tokens.append((word, "I" if style == "italic" else "", w))
        lines = []
        current_line = []
        current_width = 0
        for word, style, w in styled_tokens:
            space_w = self.get_string_width(" ")
            if current_line and current_width + space_w + w > line_width:
                lines.append(current_line)
                current_line = [(word, style, w)]
                current_width = w
            else:
                if current_line:
                    current_width += space_w
                current_line.append((word, style, w))
                current_width += w
        if current_line:
            lines.append(current_line)
        for line_tokens in lines[:-1]:
            total_word_w = sum(t[2] for t in line_tokens)
            space_count = len(line_tokens) - 1
            space_width = max(0, (line_width - total_word_w) / space_count) if space_count > 0 else 0
            x = x0
            for word, style, w in line_tokens:
                self.set_font("Serif", style, FONT_SIZE)
                self.set_xy(x, self.get_y())
                self.cell(w, LEADING, word)
                x += w + space_width
            self.ln()
        if lines:
            x = x0
            for word, style, w in lines[-1]:
                self.set_font("Serif", style, FONT_SIZE)
                self.set_xy(x, self.get_y())
                self.cell(w, LEADING, word)
                x += w + self.get_string_width(" ")
            self.ln()

    def sanitize(self, text):
        for ch in "\u200b\u200c\u200d\u2060\ufeff\u200e\u200f":
            text = text.replace(ch, "")
        text = text.replace('\u2018', "'").replace('\u2019', "'")
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        text = text.replace('\u2013', '-').replace('\u2014', '--')
        return text


# ─── BUILD ──────────────────────────────────────────────────────

def build_pdf(work_key):
    configs = {
        "birth_of_tragedy": ("The Birth of Tragedy", "Out of the Spirit of Music", "birth_of_tragedy_johnston.txt", clean_birth),
        "bge": ("Beyond Good and Evil", "Prelude to a Philosophy of the Future", "bge_johnston_full.txt", clean_bge),
        "genealogy": ("On the Genealogy of Morals", "A Polemical Tract", "genealogy_johnston_full.txt", clean_genealogy),
        "use_abuse_history": ("On the Use and Abuse of History for Life", "", "use_abuse_history_johnston.txt", clean_use_abuse),
    }

    if work_key not in configs:
        print(f"Unknown work: {work_key}")
        return

    title, subtitle, filename, cleaner = configs[work_key]
    author = "Friedrich Nietzsche"
    translator = "Translated by Ian Johnston"

    filepath = os.path.join(SRC, filename)
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found!")
        return

    print(f"\n{'='*60}")
    print(f"Building: {title}")
    print(f"{'='*60}")

    raw = read_file(filepath)
    
    pdf = JohnstonPDF(title, subtitle, author, translator)
    pdf.current_heading = title
    pdf.add_title_page()

    if work_key == "bge":
        sections = cleaner(raw)
        for sec_type, content in sections:
            if sec_type == "heading":
                pdf.add_part_heading(content)
                pdf.current_heading = content
            else:
                pdf.write_body(content)
    else:
        cleaned = cleaner(raw)
        # Save cleaned text for review
        with open(f'/root/work/{work_key}_clean.txt', 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"  Clean text: {len(cleaned):,} chars")
        pdf.write_body(cleaned)

    out_path = os.path.join(OUTDIR, f"{work_key}.pdf")
    pdf.output(out_path)
    mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"  -> {out_path}")
    print(f"  Size: {mb:.1f} MB, Pages: {pdf.page_no()}")


def main():
    for key in ["birth_of_tragedy", "bge", "genealogy", "use_abuse_history"]:
        build_pdf(key)

if __name__ == "__main__":
    main()
