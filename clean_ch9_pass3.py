#!/usr/bin/env python3
"""
Comprehensive third-pass OCR cleanup for Chapter IX.
"""
import re

def deep_clean(text):
    # Fix Thiếu (misspelled as Thiéu, Thiëu, etc.)
    text = re.sub(r'Thi[eë]u', 'Thiếu', text)
    text = re.sub(r'Thi[eë]', 'Thiếu', text)
    
    # Fix Nghĩa variants
    text = re.sub(r'ng[aâ]?[ïi]a', 'nghĩa', text)
    text = re.sub(r'NGH[AÂ]?[ÏI]A', 'NGHĨA', text)
    text = re.sub(r'ng[iî]a', 'nghĩa', text)
    text = re.sub(r'ngh[iî]a', 'nghĩa', text)
    
    # ch? variants
    text = text.replace('chë', 'chế')
    text = text.replace('Chë', 'Chế')
    text = text.replace('chi', 'chỉ')
    text = text.replace('chi-huy', 'chỉ-huy')
    
    # ph? variants
    text = text.replace('phäi', 'phải')
    text = text.replace('phâi', 'phải')
    text = text.replace('phån', 'phần')
    text = text.replace('phän', 'phần')
    
    # qu? variants
    text = text.replace('quä', 'quả')
    text = text.replace('Quä', 'Quả')
    text = text.replace('quôc', 'quốc')
    text = text.replace('Quôc', 'Quốc')
    text = text.replace('quän', 'quân')
    text = text.replace('Quän', 'Quân')
    
    # Vowel fixes
    text = text.replace('cö', 'cơ')
    text = text.replace('Cö', 'Cơ')
    text = text.replace('cü', 'cư')
    text = text.replace('Cü', 'Cư')
    text = text.replace('möt', 'một')
    text = text.replace('nöi', 'nơi')
    text = text.replace('Nöi', 'Nơi')
    text = text.replace('sü', 'sư')
    text = text.replace('Sü', 'Sư')
    text = text.replace('tü', 'tư')
    text = text.replace('Tü', 'Tư')
    text = text.replace('vö', 'vơ')
    text = text.replace('Vö', 'Vơ')
    
    # xö => xơ
    text = text.replace('xö', 'xơ')
    text = text.replace('chö', 'cho')
    
    # Common Vietnamese words
    text = text.replace('nhüng', 'những')
    text = text.replace('Nhüng', 'Những')
    text = text.replace('chüng', 'chúng')
    text = text.replace('Chüng', 'Chúng')
    text = text.replace('vân', 'vẫn')
    text = text.replace('Vân', 'Vẫn')
    text = text.replace('nöi', 'nơi')
    text = text.replace('hô', 'hồ')
    text = text.replace('dä', 'đã')
    text = text.replace('Dư', 'Dư')  # keep as is (proper name?)
    text = text.replace('dư', 'dư')  # keep
    text = text.replace('nhièu', 'nhiều')
    text = text.replace('luổn', 'luôn')
    text = text.replace('thięn', 'thiên')
    text = text.replace('chüa', 'chưa')
    text = text.replace('nàm', 'năm')
    text = text.replace('Nàm', 'Năm')
    text = text.replace('năm', 'năm')  # keep
    text = text.replace('nắm', 'năm')  # years
    text = text.replace('trong thê', 'trong thế')
    text = text.replace('trong thời', 'trong thời')
    
    # Specific OCR fixes
    text = text.replace('bôi-phän', 'bội-phần')
    text = text.replace('tranh sống', 'tranh sống')
    text = text.replace('tàn lui', 'tàn lụi')
    text = text.replace('3 tấn', 'tấn')
    text = text.replace('lịchsử', 'lịch sử')
    text = text.replace('tinhthần', 'tinh thần')
    text = text.replace('thôn-tinh', 'thôn tính')
    text = text.replace('toan-bô', 'toàn bộ')
    text = text.replace('bai miền', 'hai miền')
    text = text.replace('đàng kề', 'đáng kể')
    text = text.replace('hièm trở', 'hiểm trở')
    text = text.replace('chiếnlược', 'chiến lược')
    text = text.replace('khoa-mục', 'khoa mục')
    text = text.replace('dia-dièm', 'địa điểm')
    text = text.replace('cồ-họng', 'cửa họng')
    text = text.replace('không-ché', 'không chế')
    text = text.replace('sän-xuât', 'sản xuất')
    text = text.replace('biền', 'biển')
    text = text.replace('thuyền mành', 'thuyền mành')
    text = text.replace('Hèng-Linh', 'Hùng-Linh')
    text = text.replace('hén', 'hèn')
    text = text.replace('tuyêt-vong', 'tuyệt vọng')
    text = text.replace('quật-khởi', 'quật khởi')
    text = text.replace('bièu-duong', 'biểu dương')
    text = text.replace('quật cường', 'quật cường')
    text = text.replace('dân ta', 'dân ta')  # keep
    text = text.replace('đông đảo', 'đông đảo')
    text = text.replace('hoảng sợ', 'hoảng sợ')
    text = text.replace('việc dạ tràng se cát', 'việc dã tràng se cát')
    text = text.replace('son sắt', 'son sắt')
    text = text.replace('thản chết không lo', 'thân chết không lo')
    text = text.replace('Tô-quôc', 'Tổ-quốc')
    text = text.replace('can-tràng', 'can tràng')
    text = text.replace('khẩm-phục', 'khâm-phục')
    text = text.replace('tôn-thử', 'tôn-thờ')
    text = text.replace('nầy', 'này')
    text = text.replace('cầm đầu', 'cầm đầu')
    text = text.replace('bắt sống', 'bắt sống')
    text = text.replace('bề thế', 'bề thế')
    text = text.replace('đỗ vỡ', 'đổ vỡ')
    text = text.replace('đỗ', 'đổ')
    text = text.replace('bỏ của', 'bỏ của')
    text = text.replace('rô-rêt', 'rõ rệt')
    text = text.replace('cō', 'cơ')
    text = text.replace('gēn', 'gần')
    text = text.replace('dư-đẳng', 'dư đảng')
    text = text.replace('chổng-cự', 'chống cự')
    text = text.replace('Bãi-Sậy', 'Bãi-Sậy')
    text = text.replace('khởi nghïa', 'khởi nghĩa')
    text = text.replace('khởinghĩa', 'khởi nghĩa')
    text = text.replace('khởl-nghĩa', 'khởi nghĩa')
    text = text.replace('khởi - nghĩa', 'khởi nghĩa')
    
    # Clean up spaces in hyphenated compounds
    text = re.sub(r'(\w) - (\w)', r'\1-\2', text)
    text = re.sub(r'(\w)- (\w)', r'\1-\2', text)
    text = re.sub(r'(\w) -(\w)', r'\1-\2', text)
    
    # Space after commas, periods
    text = re.sub(r',(\S)', r', \1', text)
    text = re.sub(r'\.(\w)', r'. \1', text)
    
    # Clean multiple spaces
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def main():
    path = '/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch9-clean.txt'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned = deep_clean(text)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    lines = len(cleaned.split('\n'))
    print(f"Third pass done. Lines: {lines}")

if __name__ == '__main__':
    main()
