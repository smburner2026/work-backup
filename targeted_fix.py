#!/usr/bin/env python3
"""
Targeted fixes for ch2-clean-v2.txt — only fixes known remaining issues
without cascading replacements that create artifacts.
"""
import re
import sys

def targeted_fixes(text: str) -> str:
    # Only fix clearly broken OCR artifacts, one pattern at a time
    
    fixes = [
        # Title fix
        ('TỪ HUẾ RA TÂNSỞC', 'TỪ HUẾ RA TÂN-SỞ'),
        
        # "gần nữa" → "gần như" (context-based)
        ('gần nữa không', 'gần như không'),
        
        # Hyphenated joins that were missed
        ('thấtbại', 'thất-bại'),
        ('bímật', 'bí-mật'),
        ('độtngột', 'đột-ngột'),
        ('tưởngtượng', 'tưởng-tượng'),
        ('tìnhthần', 'tinh-thần'),
        ('lựclượng', 'lực-lượng'),
        ('quânđội', 'quân-đội'),
        ('dântộc', 'dân-tộc'),
        ('địađiềm', 'địa-điểm'),
        ('chiếnlược', 'chiến-lược'),
        ('vậtlực', 'vật-lực'),
        ('tiếtlộ', 'tiết-lộ'),
        
        # Hàm Nghi name normalization
        ('Hàm-Nghỉ', 'Hàm-Nghi'),
        ('Hàm-Nghî', 'Hàm-Nghi'),
        ('Hàm-nghỉ', 'Hàm-Nghi'),
        ('Hàm-nghi', 'Hàm-Nghi'),
        ('Häm-Nghi', 'Hàm-Nghi'),
        ('Hàm-Nghà', 'Hàm-Nghi'),
        ('Hăm-Nghi', 'Hàm-Nghi'),
        
        # Tôn Thất Thuyết
        ('Tôn-thất-Thuyết', 'Tôn-Thất-Thuyết'),
        ('Tôn-Thất-Thuyết', 'Tôn-Thất-Thuyết'),
        ('Tôn-thấtThuyết', 'Tôn-Thất-Thuyết'),
        ('Tôn-thấtPhan', 'Tôn-Thất-Phan'),
        ('Tôn-thấtNinh', 'Tôn-Thất-Ninh'),
        ('Tôn-thấtNam', 'Tôn-Thất-Nam'),
        ('Tôn-thấtLệ', 'Tôn-Thất-Lệ'),
        ('Tôn-thấtLiệt', 'Tôn-Thất-Liệt'),
        ('Thuyết tâu', 'Thuyết tâu'),
        ('Thuyết không đáp', 'Thuyết không đáp'),
        
        # Nguyễn Văn Tường
        ('Nguyễn-văn-Tường', 'Nguyễn-Văn-Tường'),
        ('Nguyễn-Văn-Tường', 'Nguyễn-Văn-Tường'),
        
        # Thái hậu
        ('Thái-hâu', 'Thái-hậu'),
        ('Thäi-hâu', 'Thái-hậu'),
        ('Thäi-Hâu', 'Thái-hậu'),
        
        # Từ Dũ
        ('Từ-Dñ', 'Từ-Dũ'),
        ('Từ-Dü', 'Từ-Dũ'),
        ('Tủ-Dữ', 'Từ-Dũ'),
        
        # Tam cung
        ('Tamcung', 'Tam-Cung'),
        ('Tam-Cung', 'Tam-Cung'),
        ('TamCung', 'Tam-Cung'),
        
        # Kinh thành
        ('Kinh-thanh', 'Kinh-thành'),
        ('Kinhthanh', 'Kinh-thành'),
        
        # Quảng Trị
        ('Quảng-trị', 'Quảng-Trị'),
        ('Quäng-Trị', 'Quảng-Trị'),
        ('QuängTri', 'Quảng-Trị'),
        ('Quảng-Trị', 'Quảng-Trị'),
        
        # Tân sở
        ('Tân-sổ', 'Tân-sở'),
        ('Tân-SỞ', 'Tân-sở'),
        ('Tân-sở', 'Tân-sở'),
        ('TânSở', 'Tân-sở'),
        ('TânSổ', 'Tân-sở'),
        ('Tân-sở', 'Tân-sở'),
        
        # Thuyết
        ('Thuyét', 'Thuyết'),
        
        # Phạm Thận Duật
        ('Phạm-thận-Duật', 'Phạm-Thận-Duật'),
        ('Phạm-Thận-Duật', 'Phạm-Thận-Duật'),
        
        # Trương Quang Đản
        ('Trương-quang-Đản', 'Trương-Quang-Đản'),
        ('Trương-Quang-Đản', 'Trương-Quang-Đản'),
        ('Trương-quang-Đẳn', 'Trương-Quang-Đản'),
        
        # Trương Đăng Đệ
        ('Trương-đăng-Đệ', 'Trương-Đăng-Đệ'),
        ('Trương-Đăng-Đệ', 'Trương-Đăng-Đệ'),
        
        # Page header artifacts that slipped through
        ('40 TỪ HUẾ RA TẢN-SỞ\n', ''),
        ('42 TỪ HUẾ RA TẢN-SỞ\n', ''),
        ('44 TỪ HUẾ RA TẢN-SỞ\n', ''),
        ('46 TỪ HUẾ RA TẢN-SỞ\n', ''),
        ('48 TỪ HUẾ RA TẢN-SỞ\n', ''),
        ('50 TỪ HUẾ RA TẢN-SỞ\n', ''),
        
        # Running header remnants
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 39\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 4\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 41\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 43\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 45\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 47\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 49\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 51\n', ''),
        ('VIỆT-NAM CÁCH-MẠNG CẬN-SỬ 53\n', ''),
        
        # Common OCR character errors (specific, not general)
        ('xagiá', 'xa-giá'),
        ('cùa', 'của'),
        ('cùa', 'của'),
        ('của a', 'của'),
        ('của ông', 'của ông'),
        ('của vua', 'của vua'),
        ('của Pháp', 'của Pháp'),
        ('của ta', 'của ta'),
        ('của mình', 'của mình'),
        ('các cửa', 'các cửa'),
        ('không có', 'không có'),
        ('đó là', 'đó là'),
        ('sự thật', 'sự thật'),
        ('sau đó', 'sau đó'),
        ('cho đến', 'cho đến'),
        ('trong khi', 'trong khi'),
        ('trong đó', 'trong đó'),
        ('trong lúc', 'trong lúc'),
        ('trong nước', 'trong nước'),
        ('bởi vì', 'bởi vì'),
        ('điều đó', 'điều đó'),
        ('ngay sau', 'ngay sau'),
        ('ngày hôm', 'ngày hôm'),
        ('đây là', 'đây là'),
        ('đó là', 'đó là'),
        ('những ai', 'những ai'),
        ('những điều', 'những điều'),
        ('những người', 'những người'),
        ('những kẻ', 'những kẻ'),
        ('vào lúc', 'vào lúc'),
        ('vào buổi', 'vào buổi'),
        ('vào khoảng', 'vào khoảng'),
        ('vào giữa', 'vào giữa'),
        ('ra ngoài', 'ra ngoài'),
        ('ra đi', 'ra đi'),
        ('đã đến', 'đã đến'),
        ('đã làm', 'đã làm'),
        ('đã được', 'đã được'),
        ('đã có', 'đã có'),
        ('đã ra', 'đã ra'),
        ('đã đi', 'đã đi'),
        ('đã bị', 'đã bị'),
        ('đã phải', 'đã phải'),
        ('có thể', 'có thể'),
        ('một số', 'một số'),
        ('một người', 'một người'),
        ('một cuộc', 'một cuộc'),
        ('với nhau', 'với nhau'),
        ('với Pháp', 'với Pháp'),
        ('với vua', 'với vua'),
        ('cho nên', 'cho nên'),
        ('cho đến', 'cho đến'),
        ('cho rằng', 'cho rằng'),
        ('cho thấy', 'cho thấy'),
        ('cho phép', 'cho phép'),
        
        # Specific phrases
        ('cờ tam tài', 'cờ tam tài'),
        ('Quẳng-Đức', 'Quảng-Đức'),
        ('bẩy giờ', 'bảy giờ'),
        ('rưởi', 'rưỡi'),
        ('ngả chùa', 'ngã chùa'),
        ('áo-não', 'ảo-não'),
        ('loan-giá', 'Long-giá'),  # imperial palanquin
        ('khóc tòng', 'khóc ròng'),
        ('Trường-Thi', 'Trường-Thi'),
        ('bỏng - bảy', 'bóng-bảy'),
        ('tàn binh', 'tàn binh'),
        ('bầy tám trăm', 'bảy tám trăm'),
        ('đãi ngộ', 'đãi ngộ'),
        ('hưu trí', 'hưu trí'),
        
        # Numbers
        ('một7-7', '13-7'),  # quick partial fix
    ]
    
    for old, new in fixes:
        text = text.replace(old, new)
    
    # Fix any remaining "=== PAGE" markers
    text = re.sub(r'=== PAGE \d+ ===\n?', '', text)
    
    # Fix multiple consecutive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r'\n{2,}([A-ZÀ-Ý][A-ZÀ-Ý\s\-]{2,})', r'\n\n\1', text)
    
    return text.strip()


def main():
    if len(sys.argv) != 3:
        print("Usage: targeted_fix.py <input_file> <output_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()
    
    result = targeted_fixes(text)
    
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Targeted fixes applied to {sys.argv[2]}")
    print(f"Input: {len(text)} chars, Output: {len(result)} chars")


if __name__ == '__main__':
    main()
