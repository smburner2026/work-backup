#!/usr/bin/env python3
"""
Clean Chapter IX text of VSTB Vol 6.
Input: /home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-raw.txt
Output: /home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-clean.txt
"""
import re
import sys

def clean_text(text):
    # 1. Strip === PAGE N === markers (with optional newline)
    text = re.sub(r'={3} PAGE \d+ ={3}\n?', '', text)
    
    # 2. Strip running headers
    # Numeric page header lines
    text = re.sub(r'^\d{2,3} [A-ZA-Z\xcc-\u0358].*\n', '', text, flags=re.MULTILINE)
    
    # "VIET-NAM CACH-MANG CAN-SU 123" style running headers
    text = re.sub(r'^VIET-\w+ CACH-M[AU]NG CAN-SU \d{2,3}\n', '', text, flags=re.MULTILINE)
    
    # CUOC KHOI-NGHIA <NAME> page headers
    text = re.sub(r'^\d{2,3} CUOC KHOI[LN-]*NGHIA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUOC KHOI NGHIA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} TIEU-SU [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} ONG TU LE-THANH-PHUONG\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} ONG TU LE-THANH-PHU' + chr(0x01a0) + r'NG\n', '', text, flags=re.MULTILINE)
    
    # 3. Join hyphenated Vietnamese word breaks at line end
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    # 4. Fix OCR errors
    
    # Specific known errors
    text = text.replace('C6', 'Có')
    text = text.replace('khäng', 'kháng')
    text = text.replace('Khäng', 'Kháng')
    text = text.replace('chién', 'chiến')
    text = text.replace('Chién', 'Chiến')
    text = text.replace('thwång', 'thường')
    text = text.replace('Thwc', 'Thực')
    text = text.replace('ce', 'có')
    text = text.replace('dä', 'đã')
    text = text.replace('Dä', 'Đã')
    text = text.replace('dà', 'đà')
    text = text.replace('Dà', 'Đà')
    text = text.replace('Bäc', 'Bắc')
    text = text.replace('bäc', 'bắc')
    text = text.replace('Bắc-kÿ', 'Bắc-kỳ')
    text = text.replace('Trung-kÿ', 'Trung-kỳ')
    text = text.replace('Trung-Kÿ', 'Trung-Kỳ')
    text = text.replace('thät', 'thất')
    text = text.replace('Thät', 'Thất')
    text = text.replace('län', 'lần')
    text = text.replace('nöm', 'năm')
    text = text.replace('blnh', 'binh')
    text = text.replace('düng', 'dũng')
    text = text.replace('mäc', 'mắc')
    text = text.replace('ngïa', 'nghĩa')
    text = text.replace('nghïa', 'nghĩa')
    text = text.replace('nghï', 'nghĩ')
    text = text.replace('Nghïa', 'Nghĩa')
    text = text.replace('lòng', 'lòng')
    text = text.replace('thë', 'thế')
    text = text.replace('Thë', 'Thế')
    text = text.replace('thó', 'thỏ')
    text = text.replace('cüng', 'cũng')
    text = text.replace('Cüng', 'Cũng')
    text = text.replace('phäi', 'phải')
    text = text.replace('Phäi', 'Phải')
    text = text.replace('nåy', 'này')
    text = text.replace('Nåy', 'Này')
    text = text.replace('näy', 'này')
    text = text.replace('lån', 'lần')
    text = text.replace('chï', 'chỉ')
    text = text.replace('chû', 'chủ')
    text = text.replace('Chû', 'Chủ')
    text = text.replace('khi', 'khi')
    text = text.replace('thuòng', 'thường')
    text = text.replace('thuòng', 'thường')
    text = text.replace('song', 'song')  # keep, it's correct Vietnamese
    text = text.replace('kha', 'kha')  # keep
    text = text.replace('chö', 'cho')
    text = text.replace('chü', 'chư')
    text = text.replace('ü', 'ư')
    text = text.replace('Ü', 'Ư')
    text = text.replace('ô', 'ô')  # already correct
    text = text.replace('ö', 'ơ')
    text = text.replace('Ö', 'Ơ')
    text = text.replace('ä', 'ă')
    text = text.replace('Ä', 'Ă')
    text = text.replace('ë', 'ê')
    text = text.replace('Ë', 'Ê')
    
    # Fix diaeresis errors
    text = text.replace('đẩä', 'đã')
    text = text.replace('đẩẩ', 'đã')
    text = text.replace("nghiềm'", 'nghiêm')
    text = text.replace('sï', 'sĩ')
    text = text.replace('ÿ', 'kỳ')
    
    # 0 at start of word -> Ô
    text = re.sub(r'\b0', 'Ô', text)
    
    # Fix common Vietnamese OCRed words
    text = text.replace('chúng tôi đã nói trên đầy', 'chúng tôi đã nói trên đây')
    text = text.replace('đồng bào', 'đồng bào')
    text = text.replace('toàn-bô', 'toàn-bộ')
    text = text.replace('thöi', 'thời')
    text = text.replace('Thöi', 'Thời')
    text = text.replace('đệ', 'để')
    text = text.replace('quện', 'quyền')
    text = text.replace('tuyêt', 'tuyệt')
    text = text.replace('tỉnh-trạng', 'tình-trạng')
    text = text.replace('tỉnh-thân', 'tinh-thần')
    text = text.replace('tỉnh-thần', 'tinh-thần')
    text = text.replace('tỉnh', 'tinh')
    text = text.replace('người', 'người')
    text = text.replace('Việt-Nam', 'Việt-Nam')
    text = text.replace('nưdc', 'nước')
    text = text.replace('nưåe', 'nước')
    text = text.replace('quä', 'quả')
    text = text.replace('Quä', 'Quả')
    text = text.replace('Việtgian', 'Việt-gian')
    text = text.replace('thựcđân', 'thực-dân')
    text = text.replace('công', 'công')
    text = text.replace('thän', 'thân')
    text = text.replace('Thän', 'Thân')
    text = text.replace('ngüoi', 'người')
    
    # 5. Clean up spacing
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def main():
    with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-raw.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned = clean_text(text)
    
    with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-clean.txt', 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    lines_before = len(text.split('\n'))
    lines_after = len(cleaned.split('\n'))
    
    print(f"Lines before: {lines_before}")
    print(f"Lines after: {lines_after}")
    print("Done! Cleaned text written to ch9-clean.txt")

if __name__ == '__main__':
    main()
