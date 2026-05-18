#!/usr/bin/env python3
"""
Compile all Nolte chapters into a single bound volume PDF.
Style: early 20th century history textbook.
"""
import os, re

from fpdf import FPDF

MD_DIR = "/root/work/scripts/nolte_md"
OUT_PATH = "/root/work/nolte_book.pdf"

FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FONT_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

FONT_SIZE = 12
LEADING = 6.5
MARGIN = 25

# Canonical book order from Table of Contents
BOOK_ORDER = [
    # Front matter
    "historians-disputea-balance-sheet",     # Preface
    "introduction-of-european-civil-war",    # Introduction
    # Chapter 1
    "final-point-and-prelude-1933-the",
    # Chapter 2: Looking Back 1917-32
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
    # Chapter 3: Hostile Ideological-States in Peace 1933-1941
    "national-socialist-germany-and-the",             # 3.1
    "the-rohm-putsch-and-the-assassination",          # 3.2
    "world-politics-19351936",                        # 3.3
    "germany-and-the-soviet-union-in-the",            # 3.4
    "the-great-purge-and-the-construction",           # 3.5
    "hitlers-triumphs-and-the-consensus",             # 3.6
    "the-failure-of-the-anti-communist",              # 3.7
    "the-hitler-stalin-pact-as-the-beginning",        # 3.8
    "the-fragile-alliance-triumphs-gains",            # 3.9
    # Chapter 4: Structures of Two One-Party States
    "the-state-parties-and-their-leaders",            # 4.1
    "the-state-security-organs-and-terror",           # 4.2
    "the-youth-associations",                         # 4.3
    "understanding-of-self-and-others",               # 4.4
    "the-politicized-culture",                        # 4.5
    "law-and-lawlessness",                            # 4.6
    "emigration-and-resistance",                      # 4.7
    "total-mobilization",                             # 4.8
    # Chapter 5: The German-Soviet War 1941-1945
    "the-attack-against-the-soviet-union",            # 5.1
    "necessities-coincidences-and-alternatives",      # 5.2
    "world-war-of-ideologies",                        # 5.3
    "genocides-and-final-solution-to-the",            # 5.4
    "the-change-of-characteristics-and",              # 5.5
    # Back matter
    "conclusionary-reflection-from-the",
    "letter-from-francois-furet-to-ernst",
    # Appendix
    "the-holocaust-the-latent-issue-in",
]

# Chapter labels
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

# Section numbers for Chapter II
CH2_SECTIONS = {
    "russias-collapse-and-the-drive-towards": 1,
    "the-emergence-of-the-communist-party": 2,
    "the-victory-of-the-bolsheviks-and": 3,
    "early-anti-bolshevism-and-the-first": 4,
    "world-revolution-or-national-government": 5,
    "the-soviet-union-from-the-death-of": 6,
    "the-period-of-stabilization-of-the": 7,
    "state-relations-between-germany-and": 8,
    "the-limited-civil-war-in-germany": 9,
    "the-eve-of-the-national-socialist": 10,
}

# Section numbers for Chapter III
CH3_SECTIONS = {
    "national-socialist-germany-and-the": 1,
    "the-rohm-putsch-and-the-assassination": 2,
    "world-politics-19351936": 3,
    "germany-and-the-soviet-union-in-the": 4,
    "the-great-purge-and-the-construction": 5,
    "hitlers-triumphs-and-the-consensus": 6,
    "the-failure-of-the-anti-communist": 7,
    "the-hitler-stalin-pact-as-the-beginning": 8,
    "the-fragile-alliance-triumphs-gains": 9,
}

# Section numbers for Chapter IV
CH4_SECTIONS = {
    "the-state-parties-and-their-leaders": 1,
    "the-state-security-organs-and-terror": 2,
    "the-youth-associations": 3,
    "understanding-of-self-and-others": 4,
    "the-politicized-culture": 5,
    "law-and-lawlessness": 6,
    "emigration-and-resistance": 7,
    "total-mobilization": 8,
}

# Section numbers for Chapter V
CH5_SECTIONS = {
    "the-attack-against-the-soviet-union": 1,
    "necessities-coincidences-and-alternatives": 2,
    "world-war-of-ideologies": 3,
    "genocides-and-final-solution-to-the": 4,
    "the-change-of-characteristics-and": 5,
}


def get_section_label(slug):
    """Get section label like 'Chapter II, Section 3' or 'Chapter I'."""
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
        header_text = self.current_section or self.book_title
        self.cell(0, 5, header_text, align="C")
        self.ln(6)

    def footer(self):
        self.set_y(-MARGIN + 5)
        self.set_font("Serif", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, str(self.page_no()), align="C")

    def add_title_page(self):
        """Main title page."""
        self.add_page()
        self.ln(50)
        self.set_font("Serif", "B", 22)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 12, self.book_title, align="C")
        self.ln(6)
        self.set_font("Serif", "I", 14)
        self.multi_cell(0, 8, self.book_subtitle, align="C")
        self.ln(8)
        # Decorative rule
        x = MARGIN
        w = self.w - 2 * MARGIN
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(8)
        self.set_font("Serif", "I", 10)
        self.multi_cell(0, 6, "Translated and presented by\nTheognis of Megara\n\nThe Indo-European Friendship Club", align="C")

    def add_chapter_title(self, title, section_label=""):
        """Chapter/section title page."""
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
        # Decorative rule
        x = MARGIN
        w = self.w - 2 * MARGIN
        self.set_draw_color(80, 80, 80)
        self.set_line_width(0.3)
        self.line(x, self.get_y(), x + w, self.get_y())
        self.ln(12)

    def write_body(self, md_text):
        """Parse markdown and render as body text."""
        lines = md_text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            if not line or re.match(r'^\s*$', line):
                self.ln(LEADING / 2)
                continue

            # Skip boilerplate lines
            if re.match(r'^(FUNDRAISING|Click here to navigate|Subscribe now|This below is)', line):
                continue

            # Skip horizontal rules
            if re.match(r'^[-*_=]{3,}$', line):
                self.ln(4)
                continue

            # Blockquote
            if line.startswith("> "):
                quote_lines = []
                while i - 1 < len(lines) and lines[i - 1].strip().startswith("> "):
                    quote_lines.append(lines[i - 1].strip()[2:])
                    i += 1
                self.write_blockquote(" ".join(quote_lines))
                self.ln(3)
                continue

            # Skip standalone bold lines that are just title repeats
            if re.match(r'^\*\*.*\*\*$', line) and len(line) < 120:
                # Could be a chapter title already rendered
                continue

            # Subsection headings ## and ### — render as bold section titles
            if line.startswith("## ") or line.startswith("### "):
                sub_title = re.sub(r'^#+\s+', '', line)
                sub_title = re.sub(r'\*\*', '', sub_title)  # strip any bold markers
                self.ln(3)
                self.set_font("Serif", "B", FONT_SIZE + 2 if line.startswith("## ") else FONT_SIZE)
                self.set_text_color(30, 30, 30)
                self.multi_cell(self.w - 2 * MARGIN, LEADING + 1, sub_title, align="C" if line.startswith("## ") else "L")
                self.ln(3)
                self.set_text_color(0, 0, 0)
                continue

            # Regular paragraph
            self.write_paragraph(line)
            self.ln(LEADING / 2)

    def write_paragraph(self, text):
        """Write a justified paragraph with inline formatting.
        **bold** → italic (academic emphasis/foreign terms),
        *italic* → italic,
        ***bold italic*** → bold italic."""
        text = self.sanitize(text)
        if not text.strip():
            return

        tokens = self.tokenize_inline(text)

        line_width = self.w - 2 * self.l_margin

        # If no formatting tokens, use the simple path
        if all(s == "" for _, s in tokens):
            self._write_plain_paragraph(text, line_width)
            return

        # Render with inline formatting
        self.set_text_color(0, 0, 0)
        # Group tokens by lines
        words_buf = []  # (text, style)
        for segment, style in tokens:
            seg_words = segment.split()
            for w in seg_words:
                # Check for overflow single word
                self.set_font("Serif", self._style_to_font(style), FONT_SIZE)
                w_w = self.get_string_width(w)
                if w_w > line_width:
                    # Flush buffer, then use multi_cell for this long word
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
        """Map token style to font style. **bold** renders as italic."""
        mapping = {"B": "I", "I": "I", "BI": "BI"}
        return mapping.get(style, "")

    def _get_styled_width(self, words_buf):
        """Total width of a buffer of (text, style) tokens."""
        total = 0
        for w, s in words_buf:
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            total += self.get_string_width(w) + self.get_string_width(" ")
        return total

    def _flush_styled_line(self, words_buf, max_width, last_line=False):
        """Render a buffered line with per-word styling."""
        if not words_buf:
            return
        if len(words_buf) == 1:
            w, s = words_buf[0]
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            self.cell(max_width, LEADING, w)
            self.ln()
            words_buf.clear()
            return

        # Calculate word widths and total
        word_info = []
        word_widths = []
        for w, s in words_buf:
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            wi = self.get_string_width(w)
            word_info.append((w, s, wi))
            word_widths.append(wi)

        total_words = sum(word_widths)
        space_count = len(words_buf) - 1
        space_width = max(0, (max_width - total_words) / space_count) if not last_line else self.get_string_width(" ")

        x = self.l_margin
        for i, (w, s, ww) in enumerate(word_info):
            self.set_font("Serif", self._style_to_font(s), FONT_SIZE)
            self.set_xy(x, self.get_y())
            self.cell(ww, LEADING, w)
            x += ww + (space_width if i < space_count else 0)
        self.ln()
        words_buf.clear()

    def _write_plain_paragraph(self, text, line_width):
        """Write a justified paragraph without inline formatting."""
        if not text.strip():
            return
        self.set_font("Serif", "", FONT_SIZE)
        self.set_text_color(0, 0, 0)
        words = text.split()
        if not words:
            return

        line_buf = ""
        for word in words:
            word_w = self.get_string_width(word)
            if word_w > line_width:
                if line_buf:
                    self._simple_justify(line_buf, line_width)
                self.multi_cell(line_width, LEADING, word)
                line_buf = ""
                continue
            test = (line_buf + " " + word).strip() if line_buf else word
            test_w = self.get_string_width(test)
            if test_w > line_width and line_buf:
                self._simple_justify(line_buf, line_width)
                line_buf = word
            else:
                line_buf = test

        if line_buf:
            self.cell(0, LEADING, line_buf)
            self.ln()

    def _simple_justify(self, text, max_width):
        """Justify a single line."""
        words = text.split()
        if len(words) == 1:
            self.set_font("Serif", "", FONT_SIZE)
            self.cell(max_width, LEADING, words[0])
            self.ln()
            return
        word_widths = [self.get_string_width(w) for w in words]
        total = sum(word_widths)
        space_count = len(words) - 1
        space = max(0, (max_width - total) / space_count)
        self.set_font("Serif", "", FONT_SIZE)
        x = self.l_margin
        for k, w in enumerate(words):
            self.set_xy(x, self.get_y())
            self.cell(word_widths[k], LEADING, w)
            x += word_widths[k] + (space if k < space_count else 0)
        self.ln()

    def write_blockquote(self, text):
        """Indented italic blockquote."""
        self.ln(2)
        text = self.sanitize(text)
        self.set_font("Serif", "I", FONT_SIZE - 1)
        self.set_text_color(60, 60, 60)
        self.set_x(MARGIN + 12)
        w = self.w - 2 * MARGIN - 12
        self.multi_cell(w, LEADING, text)
        self.set_text_color(0, 0, 0)

    def tokenize_inline(self, text):
        """Split into (text, style) tokens."""
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


def extract_title_from_md(md_text):
    """Extract the chapter/section title from markdown.
    Tries multiple patterns in order of priority."""
    # 1. # Hash heading (any line)
    m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 2. **Bold text** that starts with a section number like "**1. Title**" or "**6. Title**"
    m = re.search(r'^\*\*(\d+\.\s+[^*]+?)\*\*', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 3. Plain numbered section like "3. Title" or "7. Title" at the start of a paragraph
    m = re.search(r'^(\d+\.\s+[A-Z][^.\n]+?)(\.?\n\n|\.\s+\n)', md_text, re.MULTILINE)
    if m:
        t = m.group(1).strip()
        if len(t) > 15:
            return clean_title(t)
    # 4. **Bold text** without section numbers (e.g. "**World Politics 1935/1936**")
    #    Exclude lines that start with Chapter, [(translator notes), or Roman numerals (chapter headings)
    m = re.search(r'^\*\*(?!\[)(?!Chapter\s+[IVXLCDM])(?!\s*[IVXLCDM]+\s)(.+?)\*\*', md_text, re.MULTILINE)
    if m:
        t = m.group(1).strip()
        if not re.match(r'^[IVXLCDM]+\s', t):  # exclude bold Roman-numeral chapter heads
            return clean_title(t)
    # 5. Chapter heading like "Chapter III: ..." or "Chapter V. ..."
    m = re.search(r'^Chapter\s+[IVXLCDM]+\s*[.:]\s*(.*)$', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 6. Bold Roman-numeral chapter heads like "**IV Structures of two one-party states**"
    m = re.search(r'^\*\*([IVXLCDM]+\s+[A-Z][^*]+?)\*\*', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 7. Chapter.section like "IV. 2. Title"
    m = re.search(r'^[IVXLCDM]+\.\s+\d+\.\s+(.*)$', md_text, re.MULTILINE)
    if m:
        return clean_title(m.group(1).strip())
    # 8. First substantive standalone line (plain text title on its own line followed by blank line)
    lines = md_text.split('\n')
    for line in lines:
        s = line.strip()
        # Look for a line that looks like a title: 15-150 chars, capital start, no terminal punctuation
        if (15 <= len(s) <= 150 and s[0].isupper() and not s.startswith('**')
                and not s.startswith('*') and not s.startswith('[')
                and not re.match(r'^[IVXLCDM]+\s', s)):
            # Check it's on its own line (followed by blank or different content)
            return clean_title(s)
    return ""


def clean_title(title):
    """Clean up a title by removing leading numbers and extra punctuation."""
    # Remove leading chapter indicators like "IV ", "IV.", "IV. "
    title = re.sub(r'^[IVXLCDM]+\.?\s+', '', title)
    # Remove leading section numbers like "2. ", "10. "
    title = re.sub(r'^\d+\.\s+', '', title)
    # Remove double spaces
    title = re.sub(r'\s+', ' ', title).strip()
    # Remove trailing period if the title ends with one
    title = re.sub(r'\.$', '', title)
    title = title.strip()
    # Apply title case
    title = to_title_case(title)
    return title


def to_title_case(text):
    """Convert a string to standard English title case.
    Capitalizes first/last word and major words; lowercases articles,
    prepositions, and coordinating conjunctions. Preserves ALL-CAPS
    acronyms and proper nouns with internal caps."""
    # Minor words to keep lowercase (unless first or last word)
    minor_words = {
        "a", "an", "the",
        "and", "but", "or", "for", "nor", "yet", "so",
        "in", "of", "to", "with", "by", "at", "from",
        "as", "into", "onto", "upon", "up", "out",
        "on", "off", "over", "under", "through", "between",
        "against", "within", "without", "along", "among",
        "about", "after", "before", "behind", "below", "beneath",
        "beside", "beyond", "down", "during", "except", "inside",
        "near", "past", "since", "throughout", "toward", "towards",
        "via", "vs",
    }
    # Words that should always be capitalized (proper nouns, key terms)
    always_cap = {
        "bolshevik", "bolsheviks", "bolshevism",
        "soviet", "soviets",
        "german", "germany", "germans",
        "hitler", "hitler's",
        "stalin", "stalin's",
        "lenin", "lenin's",
        "communist", "communists", "communism",
        "national", "nationals", "nationalism", "nationalist",
        "socialist", "socialists", "socialism",
        "nazi", "nazis", "nazism",
        "fascist", "fascists", "fascism",
        "marxist", "marxists", "marxism",
        "russian", "russians", "russia",
        "european", "europe",
        "weimar",
        "reich",
        "volksgemeinschaft",
        "röhm",
        "kirov",
        "furet",
        "nolte",
        "jewish", "jew", "jews", "judaism",
        "holocaust",
        "auschwitz",
        "gulag",
        "red",
        "white",
        "world war",
        "chinese",
        "anti-bolshevism",
        "anti-communist",
        "anti-fascist",
        "anti-marxist",
    }

    # If already a short word, just capitalize it
    if len(text.split()) <= 1:
        return text.capitalize()

    # If fully uppercase (acronym or emphasis), preserve as-is
    if text.isupper():
        return text

    words = text.split()
    words = text.split()
    result = []
    for i, w in enumerate(words):
        is_first = (i == 0)
        is_last = (i == len(words) - 1)
        prev_word = words[i - 1] if i > 0 else ""

        # Strip leading/trailing punctuation for word check
        stripped = w.strip('""''"".,:;!?—–-()[]{}«»‹›')
        lead_punct = w[:len(w) - len(w.lstrip('""''"".,:;!?—–-()[]{}«»‹›"'))]
        trail_punct = w[len(w.rstrip('""''"".,:;!?—–-()[]{}«»‹›"')):]

        if not stripped:
            result.append(w)
            continue

        lower = stripped.lower()

        # Always capitalize first word, last word, and word after colon/question/dash
        is_after_punct = bool(re.search(r'[:?—!;]$', prev_word))

        if is_first or is_last or is_after_punct:
            core = stripped[0].upper() + stripped[1:]
        elif lower in always_cap:
            core = stripped[0].upper() + stripped[1:]
        elif lower in minor_words:
            core = stripped.lower()
        elif re.match(r'^\d', stripped):
            core = stripped
        else:
            core = stripped[0].upper() + stripped[1:]

        result.append(lead_punct + core + trail_punct)

    return " ".join(result)


CHAPTER_FULL_NAMES = {
    "Chapter I": "Chapter I — Final Point and Prelude 1933:\nThe Anti-Marxist Seizure of Power in Germany",
    "Chapter II": "Chapter II — Looking Back in the Years 1917–32:\nCommunists, National Socialists, Soviet Russia",
    "Chapter III": "Chapter III — The Hostile Ideological-States\nin Peace 1933–1941",
    "Chapter IV": "Chapter IV — Structures of Two One-Party States",
    "Chapter V": "Chapter V — The German-Soviet War 1941–1945",
}


def compile_book():
    pdf = BookPDF(
        "The European Civil War\n1917–1945",
        "National Socialism and Bolshevism\n\nby Ernst Nolte"
    )

    # Title page
    pdf.add_title_page()

    # Build table of contents page
    pdf.add_page()
    pdf.ln(20)
    pdf.set_font("Serif", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "CONTENTS", align="C")
    pdf.ln(14)

    # Build per-chapter groupings
    chapter_groups = {}  # chapter_label -> list of (slug, label, title)
    standalone = []
    for slug in BOOK_ORDER:
        fpath = os.path.join(MD_DIR, f"{slug}.md")
        if not os.path.exists(fpath):
            print(f"  SKIP (missing file): {slug}")
            continue
        with open(fpath, encoding="utf-8") as f:
            md = f.read()
        title = extract_title_from_md(md) or slug.replace("-", " ").title()
        label = get_section_label(slug)

        if label.startswith("Chapter") and "Section" not in label:
            # Chapter I, Chapter II etc. — map to chapter group
            chapter_groups[label] = {"label": label, "slug": slug, "title": title, "sections": []}
        elif "Section" in label:
            ch = label.split(",")[0]  # e.g. "Chapter II"
            if ch not in chapter_groups:
                chapter_groups[ch] = {"label": ch, "slug": None, "title": "", "sections": []}
            chapter_groups[ch]["sections"].append((slug, label, title))
        else:
            standalone.append((slug, label, title))

    # Render TOC: front matter first, then chapters with sections, then back matter
    MARGIN_TOC = MARGIN

    # Standalone front matter
    for slug, label, title in standalone:
        if label in ("Appendix", "Letter from François Furet", "Conclusion"):
            continue  # render at the end
        pdf.set_font("Serif", "B", 10)
        pdf.cell(0, 5, f"{label}:")
        pdf.ln()
        pdf.set_font("Serif", "I", 9)
        pdf.set_x(MARGIN_TOC + 8)
        pdf.cell(0, 5, title)
        pdf.ln(7)

    # Chapters with sections
    for ch_label in ["Chapter I", "Chapter II", "Chapter III", "Chapter IV", "Chapter V"]:
        if ch_label not in chapter_groups:
            continue
        g = chapter_groups[ch_label]
        # Chapter heading
        ch_display = CHAPTER_FULL_NAMES.get(ch_label, ch_label)
        pdf.set_font("Serif", "B", 10)
        pdf.ln(2)
        pdf.multi_cell(0, 5, ch_display)
        pdf.ln(3)

        # Sections indented under it
        if g["slug"] and not g["sections"]:
            # Single-chapter chapter (Chapter I)
            pdf.set_font("Serif", "I", 9)
            pdf.set_x(MARGIN_TOC + 8)
            pdf.cell(0, 5, g["title"])
            pdf.ln(6)
        for slug, label, title in g["sections"]:
            sec_num = label.split("Section ")[1] if "Section " in label else ""
            pdf.set_font("Serif", "I", 9)
            pdf.set_x(MARGIN_TOC + 8)
            pdf.multi_cell(pdf.w - 2 * MARGIN_TOC - 8, 5, f"Section {sec_num}: {title}")
            pdf.ln(1)

    # Back matter standalone
    for slug, label, title in standalone:
        if label not in ("Conclusion", "Letter from François Furet", "Appendix"):
            continue
        pdf.ln(2)
        pdf.set_font("Serif", "B", 10)
        pdf.cell(0, 5, f"{label}:")
        pdf.ln()
        pdf.set_font("Serif", "I", 9)
        pdf.set_x(MARGIN_TOC + 8)
        pdf.cell(0, 5, title)
        pdf.ln(7)

    # Process each chapter
    total = len(BOOK_ORDER)
    for i, slug in enumerate(BOOK_ORDER, 1):
        fpath = os.path.join(MD_DIR, f"{slug}.md")
        if not os.path.exists(fpath):
            print(f"[{i}/{total}] SKIP {slug} (not found)")
            continue

        with open(fpath, encoding="utf-8") as f:
            md_text = f.read()

        label = get_section_label(slug)
        title = extract_title_from_md(md_text) or label or slug.replace("-", " ").title()
        pdf.current_section = title

        # Chapter title page
        pdf.add_chapter_title(title, label)

        # Remove the extracted title from the body to avoid duplication,
        # but only the exact first occurrence of the bold/hash title line
        title_escaped = re.escape(title)
        md_text = re.sub(r'^#\s+' + title_escaped + r'\s*(\n|$)', '', md_text, flags=re.MULTILINE)
        md_text = re.sub(r'^\*\*' + title_escaped + r'\*\*\s*(\n|$)', '', md_text, flags=re.MULTILINE)
        # Also strip numbered title lines that match the extracted title (after stripping the number)
        # like "3. The Victory of the Bolsheviks..." when title is "The Victory of the Bolsheviks..."
        md_text = re.sub(r'^\d+\.\s+' + title_escaped + r'\s*(\n|$)', '', md_text, flags=re.MULTILINE)
        # Strip "Chapter III: " or "Chapter III. " lines
        md_text = re.sub(r'^Chapter\s+[IVXLCDM]+\s*[.:]\s+' + title_escaped + r'\s*(\n|$)', '', md_text, flags=re.MULTILINE)
        # Strip "IV Structures of..." or "IV. 2. Title" lines
        md_text = re.sub(r'^[IVXLCDM]+\.?\s+\d*\.?\s*' + title_escaped + r'\s*(\n|$)', '', md_text, flags=re.MULTILINE)

        # Remove italic preface/disclaimer notes at the start of chapters
        md_text = re.sub(r'^\*[^*]+\*(\n\n)*', '', md_text)

        # Strip standalone Chapter/Roman-numeral headings that remain in the body
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
