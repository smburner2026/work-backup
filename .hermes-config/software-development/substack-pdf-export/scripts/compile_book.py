#!/usr/bin/env python3
"""
Compile markdown chapter files into a single bound volume PDF.
Style: early 20th century history textbook.

Usage:
  1. Place all .md files in a directory
  2. Set MD_DIR, OUT_PATH, BOOK_ORDER, CHAPTER_LABELS, and section dicts
  3. Run: python3 compile_book.py

Features:
  - Liberation Serif (Times New Roman) — install fonts-liberation2
  - Justified text with per-word inline formatting (*italic*, **italic**, ***bold italic***)
  - Title page with decorative rule
  - Hierarchical Table of Contents (front matter, chapters with sections, back matter)
  - Title case for all headings (Chicago-style with proper noun awareness)
  - Chapter/section title pages with centered heading + decorative rule
  - Running headers, centered page numbers
  - Long-word overflow protection (auto-fallback to multi_cell)
  - Boilerplate stripping (preface notes, Chapter/Roman heading lines)
  - Subsection headings (## / ###) rendered as bold section titles
"""
import os, re

from fpdf import FPDF

# ===== CONFIGURE THESE =====
MD_DIR = "/home/vthen/work/nolte_md"
OUT_PATH = "/home/vthen/work/nolte_book.pdf"
# ===========================

FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

FONT_SIZE = 12
LEADING = 6.5
MARGIN = 25

# ---- Canonical book order (slug from filename, no .md) ----
BOOK_ORDER = [
    # Front matter
    "historians-disputea-balance-sheet",     # Preface
    "introduction-of-european-civil-war",    # Introduction
    # Chapter 1
    "final-point-and-prelude-1933-the",
    # Chapter 2: order as in the book
    "russias-collapse-and-the-drive-towards",        # 2.1
    "the-emergence-of-the-communist-party",           # 2.2
    "the-victory-of-the-bolsheviks-and",              # 2.3
    "early-anti-bolshevism-and-the-first",            # 2.4
    "world-revolution-or-national-government",        # 2.5
    "the-soviet-union-from-the-death-of",             # 2.6
    "the-period-of-stabilization-of-the",             # 2.7
    "state-relations-between-germany-and",            # 2.8
    "the-limited-civil-war-in-germany",               # 2.9
    "the-eve-of-the-national-socialist",              # 2.10
    # Chapter 3
    "national-socialist-germany-and-the",             # 3.1
    "the-rohm-putsch-and-the-assassination",          # 3.2
    "world-politics-19351936",                        # 3.3
    "germany-and-the-soviet-union-in-the",            # 3.4
    "the-great-purge-and-the-construction",           # 3.5
    "hitlers-triumphs-and-the-consensus",             # 3.6
    "the-failure-of-the-anti-communist",              # 3.7
    "the-hitler-stalin-pact-as-the-beginning",        # 3.8
    "the-fragile-alliance-triumphs-gains",            # 3.9
    # Chapter 4
    "the-state-parties-and-their-leaders",            # 4.1
    "the-state-security-organs-and-terror",           # 4.2
    "the-youth-associations",                         # 4.3
    "understanding-of-self-and-others",               # 4.4
    "the-politicized-culture",                        # 4.5
    "law-and-lawlessness",                            # 4.6
    "emigration-and-resistance",                      # 4.7
    "total-mobilization",                             # 4.8
    # Chapter 5
    "the-attack-against-the-soviet-union",            # 5.1
    "necessities-coincidences-and-alternatives",      # 5.2
    "world-war-of-ideologies",                        # 5.3
    "genocides-and-final-solution-to-the",            # 5.4
    "the-change-of-characteristics-and",              # 5.5
    # Back matter
    "conclusionary-reflection-from-the",
    "letter-from-francois-furet-to-ernst",
    "the-holocaust-the-latent-issue-in",
]

# ---- Labels for standalone entries (Preface, Chapter I, Conclusion, etc.) ----
CHAPTER_LABELS = {
    "historians-disputea-balance-sheet": "Preface",
    "introduction-of-european-civil-war": "Introduction",
    "final-point-and-prelude-1933-the": "Chapter I",
    "russias-collapse-and-the-drive-towards": "Chapter II",
    "national-socialist-germany-and-the": "Chapter III",
    "the-state-parties-and-their-leaders": "Chapter IV",
    "the-attack-against-the-soviet-union": "Chapter V",
    "conclusionary-reflection-from-the": "Conclusion",
    "letter-from-francois-furet-to-ernst": "Letter from François Furet",
    "the-holocaust-the-latent-issue-in": "Appendix",
}

# ---- Chapter display names for the TOC ----
CHAPTER_FULL_NAMES = {
    "Chapter I": "Chapter I — Final Point and Prelude 1933:\nThe Anti-Marxist Seizure of Power in Germany",
    "Chapter II": "Chapter II — Looking Back in the Years 1917–32:\nCommunists, National Socialists, Soviet Russia",
    "Chapter III": "Chapter III — The Hostile Ideological-States\nin Peace 1933–1941",
    "Chapter IV": "Chapter IV — Structures of Two One-Party States",
    "Chapter V": "Chapter V — The German-Soviet War 1941–1945",
}

# ---- Section numbers for multi-section chapters ----
CH2_SECTIONS = { "russias-collapse-and-the-drive-towards": 1, "the-emergence-of-the-communist-party": 2,
    "the-victory-of-the-bolsheviks-and": 3, "early-anti-bolshevism-and-the-first": 4,
    "world-revolution-or-national-government": 5, "the-soviet-union-from-the-death-of": 6,
    "the-period-of-stabilization-of-the": 7, "state-relations-between-germany-and": 8,
    "the-limited-civil-war-in-germany": 9, "the-eve-of-the-national-socialist": 10, }
CH3_SECTIONS = { "national-socialist-germany-and-the": 1, "the-rohm-putsch-and-the-assassination": 2,
    "world-politics-19351936": 3, "germany-and-the-soviet-union-in-the": 4,
    "the-great-purge-and-the-construction": 5, "hitlers-triumphs-and-the-consensus": 6,
    "the-failure-of-the-anti-communist": 7, "the-hitler-stalin-pact-as-the-beginning": 8,
    "the-fragile-alliance-triumphs-gains": 9, }
CH4_SECTIONS = { "the-state-parties-and-their-leaders": 1, "the-state-security-organs-and-terror": 2,
    "the-youth-associations": 3, "understanding-of-self-and-others": 4,
    "the-politicized-culture": 5, "law-and-lawlessness": 6,
    "emigration-and-resistance": 7, "total-mobilization": 8, }
CH5_SECTIONS = { "the-attack-against-the-soviet-union": 1, "necessities-coincidences-and-alternatives": 2,
    "world-war-of-ideologies": 3, "genocides-and-final-solution-to-the": 4,
    "the-change-of-characteristics-and": 5, }


def get_section_label(slug):
    if slug in CH2_SECTIONS:
        return f"Chapter II, Section {CH2_SECTIONS[slug]}"
    if slug in CH3_SECTIONS:
        return f"Chapter III, Section {CH3_SECTIONS[slug]}"
    if slug in CH4_SECTIONS:
        return f"Chapter IV, Section {CH4_SECTIONS[slug]}"
    if slug in CH5_SECTIONS:
        return f"Chapter V, Section {CH5_SECTIONS[slug]}"
    return CHAPTER_LABELS.get(slug, "")


class BookPDF(FPDF):
    def __init__(self, title, subtitle):
        super().__init__()
        self.book_title = title
        self.book_subtitle = subtitle
        self.add_font("Serif", "", FONT_REG)
        self.add_font("Serif", "B", FONT_BOLD)
        self.add_font("Serif", "I", FONT_ITALIC)
        self.add_font("Serif", "BI", FONT_BI)
        self.set_auto_page_break(True, MARGIN)
        self.set_margin(MARGIN)
        self.current_section = ""

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("Serif", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, self.current_section or self.book_title, align="C")
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
        self.ln(6)
        self.set_font("Serif", "I", 14)
        self.multi_cell(0, 8, self.book_subtitle, align="C")
        self.ln(8)
        x = self.l_margin
        w = self.w - 2 * MARGIN
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(8)
        self.set_font("Serif", "I", 10)
        self.multi_cell(0, 6, "Compiled from published translation", align="C")

    def add_chapter_title(self, title, section_label=""):
        self.add_page()
        self.ln(30)
        if section_label:
            self.set_font("Serif", "I", 11)
            self.set_text_color(80, 80, 80)
            self.multi_cell(0, 6, section_label, align="C")
            self.ln(8)
        self.set_font("Serif", "B", 16)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 9, title, align="C")
        self.ln(6)
        x = self.l_margin
        w = self.w - 2 * MARGIN
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(12)

    def write_body(self, md_text):
        lines = md_text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            if not line or re.match(r'^\s*$', line):
                self.ln(LEADING / 2)
                continue

            if re.match(r'^(FUNDRAISING|Click here to navigate|Subscribe now|This below is)', line):
                continue

            if re.match(r'^[-*_=]{3,}$', line):
                self.ln(4)
                continue

            if line.startswith("> "):
                quote_lines = []
                while i - 1 < len(lines) and lines[i - 1].strip().startswith("> "):
                    quote_lines.append(lines[i - 1].strip()[2:])
                    i += 1
                self.write_blockquote(" ".join(quote_lines))
                self.ln(3)
                continue

            # Skip standalone bold title lines (handled by chapter title pages)
            if re.match(r'^\*\*.*\*\*$', line) and len(line) < 120:
                continue

            # Subsection headings ## / ###
            if line.startswith("## ") or line.startswith("### "):
                sub_title = re.sub(r'^\#+\s+', '', line)
                sub_title = re.sub(r'\*\*', '', sub_title)
                self.ln(3)
                fs = FONT_SIZE + 2 if line.startswith("## ") else FONT_SIZE
                self.set_font("Serif", "B", fs)
                self.set_text_color(30, 30, 30)
                al = "C" if line.startswith("## ") else "L"
                self.multi_cell(self.w - 2 * MARGIN, LEADING + 1, sub_title, align=al)
                self.ln(3)
                self.set_text_color(0, 0, 0)
                continue

            self.write_paragraph(line)
            self.ln(LEADING / 2)

    def write_paragraph(self, text):
        """Justified paragraph with inline formatting: **bold**->italic, *italic*->italic, ***bold italic*-->bold italic."""
        text = self.sanitize(text)
        if not text.strip():
            return

        tokens = self.tokenize_inline(text)
        line_width = self.w - 2 * self.l_margin

        # Fast path: no inline formatting
        if all(s == "" for _, s in tokens):
            self._write_plain_paragraph(text, line_width)
            return

        self.set_text_color(0, 0, 0)
        words_buf = []  # [(text, style)]
        for segment, style in tokens:
            for w in segment.split():
                self.set_font("Serif", self._style_to_font(style), FONT_SIZE)
                w_w = self.get_string_width(w)
                if w_w > line_width:
                    self._flush_styled_line(words_buf, line_width)
                    self.set_font("Serif", self._style_to_font(style), FONT_SIZE)
                    self.multi_cell(line_width, LEADING, w)
                    words_buf = []
                    continue
                test_buf = words_buf + [(w, style)]
                test_w = self._get_styled_width(test_buf)
                if test_w > line_width and words_buf:
                    self._flush_styled_line(words_buf, line_width)
                words_buf.append((w, style))

        if words_buf:
            self._flush_styled_line(words_buf, line_width, last_line=True)

    def _style_to_font(self, style):
        return {"B": "I", "I": "I", "BI": "BI"}.get(style, "")

    def _get_styled_width(self, words_buf):
        total = 0
        for w, s in words_buf:
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            total += self.get_string_width(w) + self.get_string_width(" ")
        return total

    def _flush_styled_line(self, words_buf, max_width, last_line=False):
        if not words_buf:
            return
        if len(words_buf) == 1:
            w, s = words_buf[0]
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            self.cell(max_width, LEADING, w)
            self.ln()
            words_buf.clear()
            return
        word_info = []
        ww = []
        for w, s in words_buf:
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            wi = self.get_string_width(w)
            word_info.append((w, s, wi))
            ww.append(wi)
        total = sum(ww)
        sc = len(words_buf) - 1
        sp = max(0, (max_width - total) / sc) if not last_line else self.get_string_width(" ")
        x = self.l_margin
        for i, (w, s, wi) in enumerate(word_info):
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            self.set_xy(x, self.get_y())
            self.cell(wi, LEADING, w)
            x += wi + (sp if i < sc else 0)
        self.ln()
        words_buf.clear()

    def _write_plain_paragraph(self, text, line_width):
        if not text.strip():
            return
        self.set_font("Serif", "", FONT_SIZE)
        self.set_text_color(0, 0, 0)
        words = text.split()
        if not words:
            return
        buf = ""
        for word in words:
            ww = self.get_string_width(word)
            if ww > line_width:
                if buf:
                    self._simple_justify(buf, line_width)
                self.multi_cell(line_width, LEADING, word)
                buf = ""
                continue
            test = (buf + " " + word).strip() if buf else word
            if self.get_string_width(test) > line_width and buf:
                self._simple_justify(buf, line_width)
                buf = word
            else:
                buf = test
        if buf:
            self.cell(0, LEADING, buf)
            self.ln()

    def _simple_justify(self, text, max_width):
        words = text.split()
        if not words:
            return
        if len(words) == 1:
            self.set_font("Serif", "", FONT_SIZE)
            self.cell(max_width, LEADING, words[0])
            self.ln()
            return
        ww = [self.get_string_width(w) for w in words]
        sc = len(words) - 1
        sp = max(0, (max_width - sum(ww)) / sc)
        self.set_font("Serif", "", FONT_SIZE)
        x = self.l_margin
        for k, w in enumerate(words):
            self.set_xy(x, self.get_y())
            self.cell(ww[k], LEADING, w)
            x += ww[k] + (sp if k < sc else 0)
        self.ln()

    def write_blockquote(self, text):
        self.ln(2)
        text = self.sanitize(text)
        self.set_font("Serif", "I", FONT_SIZE - 1)
        self.set_text_color(60, 60, 60)
        self.set_x(MARGIN + 12)
        self.multi_cell(self.w - 2 * MARGIN - 12, LEADING, text)
        self.set_text_color(0, 0, 0)

    def tokenize_inline(self, text):
        tokens = []
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

    def sanitize(self, text):
        for ch in "\u200b\u200c\u200d\u2060\ufeff\u200e\u200f":
            text = text.replace(ch, "")
        return text


# ====== Markdown title extraction ======

def extract_title_from_md(md_text):
    """8-pattern priority chain for extracting chapter/section titles from inconsistent markdown."""
    # 1. Hash heading
    m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 2. Bold + section number: **1. Title**
    m = re.search(r'^\*\*(\d+\.\s+[^*]+?)\*\*', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 3. Plain numbered: 3. Title (no bold)
    m = re.search(r'^(\d+\.\s+[A-Z][^.\n]+?)(\.?\n\n|\.\s+\n)', md_text, re.MULTILINE)
    if m and len(m.group(1)) > 15:
        return clean_title(m.group(1))
    # 4. Bold, non-numbered, excluding Chapter/Roman/translator notes
    m = re.search(r'^\*\*(?!\[)(?!Chapter\s+[IVXLCDM])(?!\s*[IVXLCDM]+\s)(.+?)\*\*', md_text, re.MULTILINE)
    if m and not re.match(r'^[IVXLCDM]+\s', m.group(1)):
        return clean_title(m.group(1).strip())
    # 5. Chapter heading: Chapter III: ...
    m = re.search(r'^Chapter\s+[IVXLCDM]+\s*[.:]\s*(.*)$', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 6. Bold Roman-numeral chapter head: **IV Structures...**
    m = re.search(r'^\*\*([IVXLCDM]+\s+[A-Z][^*]+?)\*\*', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 7. Chapter.section: IV. 2. Title
    m = re.search(r'^[IVXLCDM]+\.\s+\d+\.\s+(.*)$', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 8. First substantive standalone line
    for line in md_text.split('\n'):
        s = line.strip()
        if (15 <= len(s) <= 150 and s[0].isupper()
                and not s.startswith('**') and not s.startswith('*')
                and not s.startswith('[') and not re.match(r'^[IVXLCDM]+\s', s)):
            return clean_title(s)
    return ""


def clean_title(title):
    """Remove leading numbers, Roman numerals, trailing period; apply title case."""
    title = re.sub(r'^[IVXLCDM]+\.?\s+', '', title)
    title = re.sub(r'^\d+\.\s+', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    title = re.sub(r'\.$', '', title).strip()
    return to_title_case(title)


def to_title_case(text):
    """Chicago-style English title case with proper noun awareness."""
    minor_words = {
        "a", "an", "the", "and", "but", "or", "for", "nor", "yet", "so",
        "in", "of", "to", "with", "by", "at", "from",
        "as", "into", "onto", "upon", "up", "out",
        "on", "off", "over", "under", "through", "between",
        "against", "within", "without", "along", "among",
        "about", "after", "before", "behind", "below", "beneath",
        "beside", "beyond", "down", "during", "except", "inside",
        "near", "past", "since", "throughout", "toward", "towards",
        "via", "vs",
    }
    always_cap = {
        "bolshevik", "bolsheviks", "bolshevism",
        "soviet", "soviets", "german", "germany", "germans",
        "hitler", "hitler's", "stalin", "stalin's", "lenin", "lenin's",
        "communist", "communists", "communism",
        "national", "nationals", "nationalism", "nationalist",
        "socialist", "socialists", "socialism",
        "nazi", "nazis", "nazism", "fascist", "fascists", "fascism",
        "marxist", "marxists", "marxism",
        "russian", "russians", "russia",
        "european", "europe",
        "weimar", "reich", "volksgemeinschaft",
        "röhm", "kirov", "furet", "nolte",
        "jewish", "jew", "jews", "holocaust", "auschwitz", "gulag",
        "red", "white",
        "anti-bolshevism", "anti-communist", "anti-fascist", "anti-marxist",
    }

    if not text or text.isupper():
        return text
    words = text.split()
    if len(words) <= 1:
        return text.capitalize()

    result = []
    for i, w in enumerate(words):
        stripped = w.strip(
            '""\'\'"".,:;!?\u2014\u2013-()[]{}'
        )
        lead = w[:len(w) - len(w.lstrip(
            '""\'\'"".,:;!?\u2014\u2013-()[]{}'
        ))]
        trail = w[len(w.rstrip(
            '""\'\'"".,:;!?\u2014\u2013-()[]{}'
        )):]
        if not stripped:
            result.append(w)
            continue

        lower = stripped.lower()
        if i == 0 or i == len(words) - 1:
            core = stripped[0].upper() + stripped[1:]
        elif lower in always_cap:
            core = stripped[0].upper() + stripped[1:]
        elif lower in minor_words:
            core = stripped.lower()
        elif re.match(r'^\d', stripped):
            core = stripped
        else:
            core = stripped[0].upper() + stripped[1:]

        result.append(lead + core + trail)
    return " ".join(result)


# ====== Main ======

def compile_book():
    # Determine book title from directory or use a default
    book_title = "The European Civil War\n1917\u20131945"
    book_subtitle = "National Socialism and Bolshevism\n\nby Ernst Nolte"

    pdf = BookPDF(book_title, book_subtitle)
    pdf.add_title_page()

    # === Table of Contents ===
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("Serif", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "CONTENTS", align="C")
    pdf.ln(14)

    chapter_groups = {}
    standalone = []
    for slug in BOOK_ORDER:
        fpath = os.path.join(MD_DIR, f"{slug}.md")
        if not os.path.exists(fpath):
            print(f"  SKIP: {slug}")
            continue
        with open(fpath, encoding="utf-8") as f:
            md = f.read()
        title = extract_title_from_md(md) or slug.replace("-", " ").title()
        label = get_section_label(slug)

        if label.startswith("Chapter") and "Section" not in label:
            chapter_groups[label] = {"label": label, "slug": slug, "title": title, "sections": []}
        elif "Section" in label:
            ch = label.split(",")[0]
            chapter_groups.setdefault(ch, {"label": ch, "slug": None, "title": "", "sections": []})
            chapter_groups[ch]["sections"].append((slug, label, title))
        else:
            standalone.append((slug, label, title))

    # Render: front matter
    for slug, label, title in standalone:
        if label in ("Appendix", "Letter from François Furet", "Conclusion"):
            continue
        pdf.set_font("Serif", "B", 10)
        pdf.cell(0, 5, f"{label}:")
        pdf.ln()
        pdf.set_font("Serif", "I", 9)
        pdf.set_x(MARGIN + 8)
        pdf.cell(0, 5, title)
        pdf.ln(7)

    # Render: chapters with sections
    for ch_label in ["Chapter I", "Chapter II", "Chapter III", "Chapter IV", "Chapter V"]:
        g = chapter_groups.get(ch_label)
        if not g:
            continue
        ch_display = CHAPTER_FULL_NAMES.get(ch_label, ch_label)
        pdf.set_font("Serif", "B", 10)
        pdf.ln(2)
        pdf.multi_cell(0, 5, ch_display)
        pdf.ln(3)

        if g["slug"] and not g["sections"]:
            pdf.set_font("Serif", "I", 9)
            pdf.set_x(MARGIN + 8)
            pdf.cell(0, 5, g["title"])
            pdf.ln(6)
        for slug, label, title in g["sections"]:
            sec_num = label.split("Section ")[1] if "Section " in label else ""
            pdf.set_font("Serif", "I", 9)
            pdf.set_x(MARGIN + 8)
            pdf.multi_cell(pdf.w - 2 * MARGIN - 8, 5, f"Section {sec_num}: {title}")
            pdf.ln(1)

    # Render: back matter
    for slug, label, title in standalone:
        if label not in ("Conclusion", "Letter from François Furet", "Appendix"):
            continue
        pdf.ln(2)
        pdf.set_font("Serif", "B", 10)
        pdf.cell(0, 5, f"{label}:")
        pdf.ln()
        pdf.set_font("Serif", "I", 9)
        pdf.set_x(MARGIN + 8)
        pdf.cell(0, 5, title)
        pdf.ln(7)

    # === Process each chapter ===
    total = len(BOOK_ORDER)
    for i, slug in enumerate(BOOK_ORDER, 1):
        fpath = os.path.join(MD_DIR, f"{slug}.md")
        if not os.path.exists(fpath):
            print(f"[{i}/{total}] SKIP {slug}")
            continue

        with open(fpath, encoding="utf-8") as f:
            md_text = f.read()

        label = get_section_label(slug)
        title = extract_title_from_md(md_text) or label or slug.replace("-", " ").title()
        pdf.current_section = title

        pdf.add_chapter_title(title, label)

        # Strip title line from body
        te = re.escape(title)
        for pat in [
            rf'^#\s+{te}\s*(\n|$)',
            rf'^\*\*{te}\*\*\s*(\n|$)',
            rf'^\d+\.\s+{te}\s*(\n|$)',
            rf'^Chapter\s+[IVXLCDM]+\s*[.:]\s+{te}\s*(\n|$)',
            rf'^[IVXLCDM]+\.?\s+\d*\.?\s*{te}\s*(\n|$)',
        ]:
            md_text = re.sub(pat, '', md_text, flags=re.MULTILINE)

        # Strip italic preface notes
        md_text = re.sub(r'^\*[^*]+\*(\n\n)*', '', md_text)
        # Strip standalone Chapter/Roman heading lines
        md_text = re.sub(r'^Chapter\s+[IVXLCDM]+\s*[.:].*$', '', md_text, flags=re.MULTILINE)
        md_text = re.sub(r'^\*\*[IVXLCDM]+\s+[A-Z][^*]*?\*\*\s*$', '', md_text, flags=re.MULTILINE)

        pdf.write_body(md_text)
        print(f"[{i}/{total}] {slug}  ({len(md_text):,} chars)")

    pdf.output(OUT_PATH)
    size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
    print(f"\nBook compiled: {OUT_PATH}")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    compile_book()
