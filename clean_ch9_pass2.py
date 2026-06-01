#!/usr/bin/env python3
"""
Second pass cleaning for Chapter IX.
Fixes more OCR issues and remaining running headers.
"""
import re

def clean_pass2(text):
    # Remove remaining running headers
    text = re.sub(r'^VIỆT-NAM CÁCH-MẠNG CẬN-SỬ \d{2,3}\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỞI-NGHĨA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỞI NGHĨA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỔI-NGHĨA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} TIỀU-SỬ [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} ÔNG TÚ [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỞILNGHĨA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHÔI-NGHÏA [A-Z].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỞI NGHĨA HUƠNG-KHẺ\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỞI NGHĨA [A-ZÀ-Ỹ].*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d{2,3} CUỘC KHỞ[^ ]*NGHĨA [A-Z].*\n', '', text, flags=re.MULTILINE)
    
    # More aggressive: any line that is just a number followed by a Vietnamese uppercase word
    # that appears to be a page header
    text = re.sub(r'^\d{2,3} [A-ZÀ-Ỹ][A-ZÀ-Ỹ \-]{5,}$\n', '', text, flags=re.MULTILINE)
    
    # Fix hyphenation more carefully - don't join across sentences
    # Join hyphenated words broken across lines
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    # Fix common OCR errors - Thiếu
    text = text.replace('Thiéu', 'Thiếu')
    text = text.replace('Thié', 'Thiếu')
    text = text.replace('chi-huy', 'chỉ-huy')
    text = text.replace('Chihuy', 'Chỉ-huy')
    text = text.replace('Chỉhuy', 'Chỉ-huy')
    text = text.replace('mäc', 'mắc')
    text = text.replace('phân', 'phần')
    text = text.replace('thän', 'thân')
    text = text.replace('thät', 'thất')
    text = text.replace('dat', 'đặt')
    text = text.replace('Dat', 'Đặt')
    text = text.replace('nay', 'nay')  # keep
    text = text.replace('nay là', 'nay là')
    text = text.replace('nay đã', 'nay đã')
    text = text.replace('đệ', 'để')
    text = text.replace('khäng-chién', 'kháng-chiến')
    text = text.replace('thåy', 'thấy')
    text = text.replace('thäy', 'thấy')
    text = text.replace('thay', 'thay')  # keep
    text = text.replace('Thay', 'Thay')
    text = text.replace('löi', 'lối')
    text = text.replace('thời', 'thời')  # keep
    text = text.replace('thöi', 'thời')
    text = text.replace('bäy', 'bấy')
    text = text.replace('Bäy', 'Bấy')
    text = text.replace('bây', 'bây')  # keep
    text = text.replace('gior', 'giờ')
    text = text.replace('giö', 'giờ')
    
    # Numbers cleanup
    text = text.replace('đại-bác', 'đại-bác')
    text = text.replace('Thiëu', 'Thiếu')
    text = text.replace('luc', 'lục')
    text = text.replace('lục-quân', 'lục-quân')
    
    # Space fixes
    text = re.sub(r' :', ':', text)
    text = re.sub(r' ;', ';', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\s+,', ',', text)
    
    # Line joining - if a line doesn't end with sentence-ending punctuation, 
    # join it with the next line (Vietnamese paragraphs)
    # But this is complex and can break things. Let's just clean up spaces.
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def main():
    path = '/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-clean.txt'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned = clean_pass2(text)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    lines = len(cleaned.split('\n'))
    print(f"Second pass done. Lines: {lines}")
    print("File written to ch9-clean.txt")

if __name__ == '__main__':
    main()
