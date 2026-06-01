#!/usr/bin/env python3
"""
Clean Chapter II of VSTB Volume 6.
Strips page markers, running headers, joins hyphenated line breaks,
fixes common OCR diacritic errors, and reflows paragraphs.
"""
import re
import sys

def clean_text(text: str) -> str:
    lines = text.split('\n')
    
    # Step 1: Remove === PAGE N === markers
    cleaned = []
    for line in lines:
        if re.match(r'^=== PAGE \d+ ===$', line.strip()):
            continue
        cleaned.append(line)
    
    text = '\n'.join(cleaned)
    
    # Step 2: Remove running headers/footers that appear after page breaks
    # These are lines like:
    # "VIỆT-NAM CÁCH-MẠNG CẬN-ŠỬ 39" (page header)
    # "40 TỪ HUẾ RA TẢN-SỞ" (page footer with number + running title)
    # "VIỆT-NAM CÂCH-MANG CẬN SỬ 4" (variant with missing diacritics)
    # "VIËT-NAM CÁCH-MẠNG CẬN-SỬ 4" (variant)
    # "TỪ HUẾ RA TẢN-SỈ" (running title standalone)
    # Later in the chapter: "VUA HÀM-NGHI QUA AI-LAO" etc.
    
    # More robust: remove lines matching the running header patterns
    # Pattern: starts with volume abbreviation + number
    # Pattern: starts with number + running title
    # These only appear as standalone lines after page markers
    
    lines = text.split('\n')
    cleaned = []
    
    skip_patterns = [
        # Volume title + number (page header)
        r'^VIỆT-NAM\s+C[ÁAÀ][CH]?[MH]?\s*-\s*M[ẠA][NG]+\s+C[ẬÂ][NẠ]\s*-\s*S[ỬƯ]\s*\d+\s*$',
        # Number + running title (page footer)
        r'^\d+\s+TỪ\s+HU[ẾÊ]\s+RA\s+T[ẢÂ][NNS]+[\-\s]*S[ỞỈƠ]\s*$',
        r'^\d+\s+VUA\s+HÀM\s*-\s*NGHI\s+QUA\s+AI\s*-\s*LAO\s*$',
        # Running title without number
        r'^TỪ\s+HU[ẾÊ]\s+RA\s+T[ẢÂ][NNS]+[\-\s]*S[ỞỈƠ]\s*$',
        r'^VUA\s+HÀM\s*-\s*NGHI\s+QUA\s+AI\s*-\s*LAO\s*$',
        # Variants with OCR errors
        r'^VIỆT-NAM\s+C[ÁA]CH-M[ẠA]NG\s+C[ẬÂ]N-S[ỬƯ]\s*\d+\s*$',
        r'^VIỆT-NAM\s+C[ÁA]CH\s*M[ẠA]NG\s+C[ẬÂ]N\s*S[ỬƯ]\s*\d+\s*$',
        r'^\d+\s+TỪ\s+HU[ẾÊ]\s+RA\s+T[ẢÂ]N\s*S[ỞỈƠ]\s*$',
        # The specific variants seen in raw text
        r'^VIỆT-NAM\s+CÁCH-MẠNG\s+CẬN-ŠỬ\s+\d+\s*$',
        r'^VIỆT-NAM\s+CÂCH-MANG\s+CẬN\s+SỬ\s+\d+\s*$',
        r'^VIËT-NAM\s+CÁCH-MẠNG\s+CẬN-SỬ\s+\d+\s*$',
        r'^VIỆT-NAM\s+CCÁH-MẠNG\s+CẬN-SỬ\s+\d+\s*$',
        r'^VIỆT-NAM\s+CÁCH-MẠNG\s+CẢN-SỬ\s+\d+\s*$',
        # Number + VUA HÀM-NGHI QUA AI-LAO
        r'^\d+\s+VUA\s+HÀM\s*-\s*NGHI\s+QUA\s+AI\s*-\s*LAO\s*$',
        # "VUA HÀM-NGHÀ QUA AI- LAO" - OCR variant
        r'^\d*\s*VUA\s+HÀM-NGH[IÀ]\s+QUA\s+AI\s*-\s*LAO\s*$',
        # "VUA HÀM-NGHI QUA AI-LAO" as header standalone
        r'^VUA\s+HÀM\s*-\s*NGHI\s+QUA\s+AI\s*-\s*LAO\s*$',
        r'^\d+\s+VUA\s+HÀM-NGHI\s+QUA\s+AI-LAO\s*$',
    ]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if this line is a running header
        is_header = False
        for pat in skip_patterns:
            if re.match(pat, stripped):
                is_header = True
                break
        
        # Also check for combined lines like "=== PAGE 36 ===\nVIỆT-NAM..."
        # but those were already split
        
        if is_header:
            i += 1
            continue
        
        cleaned.append(line)
        i += 1
    
    text = '\n'.join(cleaned)
    
    # Step 3: Join hyphenated line breaks
    # A word split across lines: "word-\nword" → "wordword"
    # But real hyphens (like "Tôn-thất-Thuyết") should be preserved
    
    # Join lines that end with a hyphen (word-break hyphenation)
    lines = text.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1 and line.endswith('-') and not line.endswith('---'):
            # Join with next line, removing the hyphen
            next_line = lines[i + 1]
            # Only join if the next line doesn't start with a number or special char
            if next_line and not next_line[0].isdigit() and not next_line.startswith('(') and not next_line.startswith('['):
                lines[i + 1] = line[:-1] + next_line
                continue
        result.append(line)
    
    text = '\n'.join(result)
    
    # Step 4: Reflow paragraphs
    # Currently lines are hard-wrapped. Join lines that don't start a new paragraph.
    # A new paragraph starts with a blank line before it, or with an indented/tabbed line.
    
    lines = text.split('\n')
    reflowed = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Empty line - preserve as paragraph break
        if not stripped:
            reflowed.append('')
            i += 1
            continue
        
        # Check if this starts a new paragraph
        # A line that starts a paragraph typically:
        # - Has a blank line before it (handled above)
        # - Is a chapter title, section header (all caps or starts with number+period)
        # - Is a block quote (starts with «)
        
        # Collect continuation lines
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line:
                break
            
            # Check if next line starts a new section/header
            if (re.match(r'^[A-ZÀ-Ý][A-ZÀ-Ý\s\-]{3,}', next_line) and 
                not re.match(r'^[A-ZÀ-Ý][a-zà-ý]', next_line) and
                len(next_line) < 80):
                # This is probably a header
                break
            
            # Check for footnote continuation
            if next_line.startswith('(') and re.match(r'^\(\d+\)', next_line):
                para_lines.append(next_line)
                i += 1
                continue
            
            # Regular continuation
            para_lines.append(next_line)
            i += 1
        
        # Join paragraph lines
        para = ' '.join(para_lines)
        reflowed.append(para)
    
    text = '\n'.join(reflowed)
    
    # Step 5: Fix common OCR diacritic errors
    replacements = {
        # Hàm Nghi name variants
        'Hàm-nghỉ': 'Hàm-Nghi',
        'Hàm-Nghỉ': 'Hàm-Nghi',
        'Hàm-Nghî': 'Hàm-Nghi',
        'Hàm-Nghì': 'Hàm-Nghi',
        'Hàm-nghi': 'Hàm-Nghi',
        'Häm-Nghi': 'Hàm-Nghi',
        'Häm-Nghỉ': 'Hàm-Nghi',
        'Hàm-nghî': 'Hàm-Nghi',
        'Hàm-Nghà': 'Hàm-Nghi',
        
        # Tôn Thất Thuyết name variants
        'Tôn-thät-Thuyét': 'Tôn-Thất-Thuyết',
        'Tôn-thất-Thuyết': 'Tôn-Thất-Thuyết',
        'Tôn-thät': 'Tôn-Thất',
        'Tôn-thấtThuyết': 'Tôn-Thất-Thuyết',
        'Tôn-thất-Liệt': 'Tôn-Thất-Liệt',
        'Thuyết': 'Thuyết',  # keep correct
        'Thuyét': 'Thuyết',
        
        # Nguyễn Văn Tường name variants
        'Nguyễn-văn-Tường': 'Nguyễn-Văn-Tường',
        'Nguyễn-vän-Tường': 'Nguyễn-Văn-Tường',
        'Nguyễn văn Tường': 'Nguyễn-Văn-Tường',
        'Nguyễn-vănTuông': 'Nguyễn-Văn-Tường',
        'Nguyễn-vănTưởng': 'Nguyễn-Văn-Tường',
        
        # Thái hậu variants
        'Thäi-hâu': 'Thái-hậu',
        'Thäihâu': 'Thái-hậu',
        'Thái-Hậu': 'Thái-hậu',
        'Thäi-Hâu': 'Thái-hậu',
        'Thái-hậu': 'Thái-hậu',  # already correct
        
        # Từ Dũ variants
        'Từ-Dñ': 'Từ-Dũ',
        'Từ-Dü': 'Từ-Dũ',
        'Tủ-Dữ': 'Từ-Dũ',
        'Từ-Dữ': 'Từ-Dũ',
        
        # OCR confusion with diacritics
        'Tânsởc': 'Tân-sở',
        'Tân-sổ': 'Tân-sở',
        'Tân-SỞ': 'Tân-sở',
        'tân-đô': 'Tân-sở',
        'Tân-sở': 'Tân-sở',  # keep
        
        # Quảng Trị variants
        'Quãng-Trị': 'Quảng-Trị',
        'Quäng-Trị': 'Quảng-Trị',
        'Quảng-trị': 'Quảng-Trị',
        'Quảng-Trị': 'Quảng-Trị',  # keep
        
        # Kinh thành variants
        'Kinh-thanh': 'Kinh-thành',
        'Kinh-thành': 'Kinh-thành',  # keep
        
        # General diacritic fixes
        'nữ': 'nữa' if False else 'nữa',  # handled case-by-case
        'đệ-nhị-niên': 'đệ-nhị-niên',  # keep
        'Ất-đậu': 'Ất-Dậu',
        'Ất-dậu': 'Ất-Dậu',
        
        # Tam cung
        'Tam-Cung': 'Tam-Cung',
        'Tamcung': 'Tam-Cung',
        
        # Various
        'Trän-xuân-Soan': 'Trần-Xuân-Soạn',
        'Nguyễn-đình-Chiều': 'Nguyễn-Đình-Chiểu',
        'Phạm-thận-Duật': 'Phạm-Thận-Duật',
        'Phạm-thậnDuật': 'Phạm-Thận-Duật',
        'Trương-quang-Đản': 'Trương-Quang-Đản',
        'Trương quang-Đản': 'Trương-Quang-Đản',
        'Trương-quang-Đẳn': 'Trương-Quang-Đản',
        'Trương-đăng-Đệ': 'Trương-Đăng-Đệ',
        'Trương đăng Đệ': 'Trương-Đăng-Đệ',
        'Hoàngtá-Viêm': 'Hoàng-Tá-Viêm',
        'Hoàng-tá-Viêm': 'Hoàng-Tá-Viêm',
        'Nguyễn-quang-Bích': 'Nguyễn-Quang-Bích',
        'Nguyễn-đình-Nhuận': 'Nguyễn-Đình-Nhuận',
        'Tôn-thất-Nam': 'Tôn-Thất-Nam',
        'Tôn-thất-Lệ': 'Tôn-Thất-Lệ',
        'Lã-xuân-Oai': 'Lã-Xuân-Oai',
        
        # Quotes and punctuation
        '«': '« ',
        '»': ' »',
        'Trâm': 'Trẫm',
        'Träm': 'Trẫm',
        
        # Other common OCR errors
        'không-khi': 'không-khí',
        'tuyêt-ddi': 'tuyệt-đối',
        'đï-nhiên': 'đĩ-nhiên',
        'dï-nhiên': 'đĩ-nhiên',
        'dĩnhiên': 'đĩ-nhiên',
        'bi-mât': 'bi-mật',
        'muc-dich': 'mục-đích',
        'đạináo': 'đại-náo',
        'täi-diên': 'tái-diễn',
        'thäo-luän': 'thảo-luận',
        'xü-lir': 'xử-trị',
        'sô-dï': 'sở-dĩ',
        'qui-hợp': 'Quy-Hợp',
        'Qui-hợp': 'Quy-Hợp',
        'Quí': 'Quý',
        'kỷ': 'ký',  # context dependent
        'ký': 'ký',  # keep
        'lý': 'lý',  # keep
        'lỷ-do': 'lý-do',
        
        # Pháp variants
        'thựcdân': 'thực-dân',
        'thực-dân': 'thực-dân',
        'thycdân': 'thực-dân',
        'thuc-dân': 'thực-dân',
        
        # Cần Vương
        'cầnvương': 'Cần-Vương',
        'Cần-vương': 'Cần-Vương',
        'cần-vương': 'Cần-Vương',
        'Cần Vương': 'Cần-Vương',
        
        # Kháng chiến
        'khäng-chién': 'kháng-chiến',
        'kháng-chiến': 'kháng-chiến',
        'khángchiến': 'kháng-chiến',
        'kháng-cbiến': 'kháng-chiến',
        'kháng-nhiến': 'kháng-chiến',
        'kháng-chiên': 'kháng-chiến',
        'khäng-chiến': 'kháng-chiến',
        'kháng-chiên': 'kháng-chiến',
        
        # Bắc Kỳ
        'Bắc-Kỳ': 'Bắc-kỳ',
        'Bắckỳ': 'Bắc-kỳ',
        'Bäc-kÿ': 'Bắc-kỳ',
        'Bäc-kỳ': 'Bắc-kỳ',
        
        # Trung Kỳ
        'Trung-kỳ': 'Trung-kỳ',
        'Trungkỳ': 'Trung-kỳ',
        
        # Việt Nam
        'Việt-Nam': 'Việt-Nam',
        'Viêt-Nam': 'Việt-Nam',
        'Việ-Nam': 'Việt-Nam',
        
        # Various
        'sảng': 'sáng',
        'bẩy': 'bảy',
        'bảy': 'bảy',
        'thẳngthốt': 'thảng-thốt',
        'thâu': 'tâu',
        'Thâu': 'Tâu',
        'bẩn': 'bản',
        'triêt-dè': 'triệt-để',
        'cáo-thị': 'cáo-thị',
        'cảo-thị': 'cáo-thị',
        'chỈthị': 'chỉ-thị',
        'chỉ-thị': 'chỉ-thị',
        'lươngthực': 'lương-thực',
        'lươngthực': 'lương-thực',
        'vậtliệu': 'vật-liệu',
        'vữkhíi': 'vũ-khí',
        'vữ-khí': 'vũ-khí',
        'vũ-khi': 'vũ-khí',
        'vü-khi': 'vũ-khí',
        'vũ-khí': 'vũ-khí',
        'tân-binh': 'tân-binh',
        'viện-binh': 'viện-binh',
        'viện binh': 'viện-binh',
        'Un-tée': 'ưu-tư',
        'ưu-tư': 'ưu-tư',
        'bão-vê': 'bảo-vệ',
        'hô-vê': 'hộ-vệ',
        'Kinh-kÿ': 'Kinh-kỳ',
        'Ngư-đạo': 'Ngự-đạo',
        'Ngự-đạo': 'Ngự-đạo',
        'Ngự-dạ': 'Ngự-đạo',
        'ngự-đạo': 'Ngự-đạo',
        'Ngự-đạo': 'Ngự-đạo',
        'duo-ngy': 'Ngự-đạo',
        'Bai-Nam': 'Đại-Nam',
        'Hạnh-thụ': 'Hành-thứ',
        'Hành-cung': 'Hành-cung',
        'Hänh-cung': 'Hành-cung',
        'Hành-cung': 'Hành-cung',
        'Khiêm-cung': 'Khiêm-cung',
        'Khiêm-cung': 'Khiêm-cung',
        'hâụ-dao': 'hậu-đạo',
        'Đạongg': 'Đạo-ngự',
        'thêthẩm': 'thê-thảm',
        'phän-khôi': 'phấn-khởi',
        'tinh-thän': 'tinh-thần',
        'mät': 'mất',
        'bõ': 'bỏ',
        'xã-tắc': 'xã-tắc',
        'tâu trình': 'tâu-trình',
        'giao-động': 'dao-động',
        'lính thän-co': 'lính thần-cơ',
        'phảo-binh': 'pháo-binh',
        'phäo-thuyën': 'pháo-thuyền',
        'Đại-Nội': 'Đại-Nội',
        'đại-nội': 'Đại-Nội',
        'hoàngthành': 'Hoàng-thành',
        'Hoàng-thành': 'Hoàng-thành',
        'hoàng-thành': 'Hoàng-thành',
        'hoàngthành': 'Hoàng-thành',
        'thän-thần': 'thân-thần',
        'quốc-gia đa-ngn': 'quốc-gia đa-đoan',
        'phẩmnã': 'phẩm-nhã',
        'HuyỀN-lỏng': 'Huyền-Vũ',
        'Quáchtử-Nghi': 'Quách-Tử-Nghi',
        'Lự-quang-Bậi': 'Lý-Quang-Bật',
        'Triệu-Thôi': 'Triệu-Thôi',
        'Hồ-Yền': 'Hồ-Diên',
        'thäi-dé': 'thái-độ',
        'täc-già': 'tác-giả',
        'tâc-gii': 'tác-giả',
        'bimh-luân': 'bình-luận',
        'Hòa-ước': 'Hòa-ước',
        'Hòa ước': 'Hòa-ước',
        'Hiệp-ước': 'Hiệp-ước',
        'Hiệpước': 'Hiệp-ước',
        'bãi-bô': 'bãi-bỏ',
        'bài-bỏ': 'bãi-bỏ',
        'khôi-phục': 'khôi-phục',
        'khôi-phuc': 'khôi-phục',
        'Ngự-đạo': 'Ngự-đạo',
        'Ngự-đạo': 'Ngự-đạo',
        'loạn thành trị': 'loạn thành trị',
        'ngưng': 'ngừng',
        'từ-giä': 'từ-giã',
        'gäi': 'gửi',
        'gởi': 'gửi',
        'đềnghị': 'đề-nghị',
        'dè-nghi': 'đề-nghị',
        'đềnghị': 'đề-nghị',
        'kết-quà': 'kết-quả',
        'kếtquả': 'kết-quả',
        'thä': 'thảo',
        'mi': 'mời',
        'tư-tưởng thoái-bại': 'tư-tưởng thoái-bại',
        'hưu-trí': 'hưu-trí',
        'huu-tri': 'hưu-trí',
        '1rương-đăng-Đệ': 'Trương-Đăng-Đệ',
        # The "ai theo đöi" -> "ai theo dõi"
        'đöi': 'dõi',
        'Ai-Lao': 'Ai-Lao',
        'Ai-lao': 'Ai-Lao',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Step 6: Fix specific patterns
    # Fix "nữa" vs "nửa" - context dependent, use "nữa" most often
    text = re.sub(r'\bgần nữ\b', 'gần như', text)
    
    # Fix "chue" -> "chứa" if needed
    
    # Remove page number + title footers that might have been missed
    # Pattern: number at start of line followed by all-caps
    text = re.sub(r'^\d+\s+[A-ZÀ-Ý][A-ZÀ-Ý\s\-]+$', '', text, flags=re.MULTILINE)
    
    # Step 7: Clean up excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Step 8: Fix footnote markers that got joined
    # (1) and (2) etc. with spaces
    text = re.sub(r'\((\d+)\)', r'(\1)', text)
    
    return text.strip()


def main():
    if len(sys.argv) != 3:
        print("Usage: clean_ch2.py <input_file> <output_file>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    with open(input_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    cleaned = clean_text(raw)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"Cleaned text written to {output_path}")
    print(f"Original: {len(raw)} chars, Cleaned: {len(cleaned)} chars")
    
    # Count remaining issues
    lines = cleaned.split('\n')
    print(f"Lines: {len(lines)}")


if __name__ == '__main__':
    main()
