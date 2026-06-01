#!/usr/bin/env python3
"""Second-pass cleaning for ch5-clean.txt - fix remaining artifacts."""

with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch5-clean.txt', 'r') as f:
    text = f.read()

# Fix the messy running header merging
text = text.replace(
    "VUA HÀM-NGHI HOẠT Như ta đã thấy, bị chận ở Quảng->\nĐỘNG Ở HÀ-TĨNH Bình, ông Thuyết phải dùng đường\nAi-lào đưa vua ra Bắc-kỳ tính\nlập thêm cơ-sở chiến-đấu Ngự đạo theo phía Tây dãy\nTrườngsơn mà di rồi tới Cửu-châu thuộc thị-trấn Savannakhet\ncủa Ai-lào.",
    "VUA HÀM-NGHI HOẠT-ĐỘNG Ở HÀ-TĨNH\n\nNhư ta đã thấy, bị chận ở Quảng-Bình, ông Thuyết phải dùng đường\nAi-lao đưa vua ra Bắc-kỳ tính\nlập thêm cơ-sở chiến-đấu. Ngự-đạo theo phía Tây dãy\nTrường-sơn mà đi rồi tới Cửu-châu thuộc thị-trấn Savannakhet\ncủa Ai-lao."
)

# Fix "Ai-lào" -> "Ai-lao"
text = text.replace('Ai-lào', 'Ai-lao')

# More fixes
fixes = {
    'quả mệt mỗi': 'quá mệt mỏi',
    'ông lu đã': 'ông liền đã',
    'khó đầu trả giá rất cao': 'khó khăn, trả giá rất cao',
    'mệnh-một\n\nmột đáng thương': 'mệnh-một đáng thương',
    'đổ lương-thực': 'đồ lương-thực',
    'không quá 40 kẻ': 'không quá 40',
    'tháng 7 (tức là cuối tháng 8 Dương-lịch': 'tháng 7 (tức là cuối tháng 8 Dương-lịch)',
    'tháng 8 Dương-lịch)': 'tháng 8 Dương-lịch)',
}

for old, new in sorted(fixes.items(), key=lambda x: -len(x[0])):
    text = text.replace(old, new)

with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch5-clean.txt', 'w') as f:
    f.write(text)

print(f'Done. {len(text)} chars, {len(text.split(chr(10)))} lines')
