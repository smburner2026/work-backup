#!/usr/bin/env python3
"""Fix over-corrections in cleaned Chapter I."""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch2-clean.txt"

with open(path, 'r') as f:
    text = f.read()

fixes = [
    ('kẻ từ', 'kể từ'),
    ('kẻ trên', 'kể trên'),
    ('còng', 'công'),
    ('Báo hoàng', 'Bảo hoàng'),
    ('báo-vệ', 'bảo-vệ'),
    ('Báo-hộ', 'Bảo-hộ'),
    ('đều đều chết', 'đều chết'),
    ('xác- đáng', 'xác-đáng'),
    ('kỷ', 'ký'),
    ('thổa hiệp', 'thỏa hiệp'),
    ('đồng-chỉ', 'đồng-chí'),
    ('vi ông', 'vì ông'),
    ('bịnh đội', 'binh đội'),
    ('lim', 'làm'),
    ('dé', 'đó'),
    ('dũng cẩm', 'dũng cảm'),
    ('Bắc-viêt', 'Bắc-Việt'),
    ('Bắc-kÿ', 'Bắc-kỳ'),
    ('Tam-Đáo', 'Tam-Đảo'),
    ('Tônthất-Thuyết', 'Tôn-Thất-Thuyết'),
    ('khángchiến', 'kháng-chiến'),
    ('chỉnh-trị', 'chính-trị'),
    ('đông đáo', 'đông đảo'),
    ('diệt Pháp', 'diệt Pháp'),
]

for old, new in fixes:
    text = text.replace(old, new)

with open(path, 'w') as f:
    f.write(text)

print("Fixed.")
