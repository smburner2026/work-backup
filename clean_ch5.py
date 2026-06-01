#!/usr/bin/env python3
"""Clean Chapter V of VSTB Vol 6 — systematic Tesseract OCR fixes."""

import re
import sys

def clean(text):
    lines = text.split('\n')
    cleaned = []
    skip_header_footer = False
    
    for i, line in enumerate(lines):
        # Strip === PAGE N === markers and page header/footer lines
        if re.match(r'^=== PAGE \d+ ===$', line.strip()):
            continue
        # Strip running headers like "VIỆT-NAM CÁCH-MẠNG CẬN-SỬ N" or "N VUA HÀM-NGHI..."
        if re.match(r'^\d+ [A-ZÀ-Ỹ].*[A-ZÀ-Ỹ] [A-ZÀ-Ỹ]', line.strip()):
            # These are running page headers with page number
            # Pattern: "68 VUA HÀM-NGHI HOẠT ĐỘNG Ô HÀ-TĨNH"
            if re.match(r'^\d+ [A-ZÀ-Ỹ]', line.strip()):
                continue
        # Strip "VIỆT-NAM CÁCH-MẠNG CẬN-SỬ N" lines
        if re.match(r'^VIỆT-NAM CÁCH-MẠNG CẬN-SỬ\s*—?\s*\d*$', line.strip()):
            continue
        if re.match(r'^VIỆT-NAM CÁCH-MẠNG CẬN-SỬ \d+', line.strip()):
            continue
        # Strip page number at end of content (page footers like just a number)
        if re.match(r'^\d+$', line.strip()):
            # Check if it's a footnote marker (small number)
            if len(line.strip()) <= 2:
                continue
        
        cleaned.append(line)
    
    text = '\n'.join(cleaned)
    
    # Join hyphenated line breaks across lines (but not double-hyphens)
    # A hyphenated line break is a word at end of line with a hyphen -
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    # Remove spaces before hyphens within words
    text = re.sub(r'(\w) +- +(\w)', r'\1-\2', text)
    text = re.sub(r'(\w)- +(\w)', r'\1-\2', text)
    text = re.sub(r'(\w) +-(\w)', r'\1-\2', text)
    
    # Remove spaces before punctuation
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    
    # Normalize multiple spaces
    text = re.sub(r'  +', ' ', text)
    
    # Normalize line spacing (no more than 2 consecutive newlines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # ===== SYSTEMATIC OCR FIXES =====
    
    # 1. đẩä/đẩẩ → đã
    text = text.replace('đẩä', 'đã')
    text = text.replace('đẩẩ', 'đã')
    
    # 2. nghiềm'/nghiềm → nghiêm
    text = re.sub(r"nghiềm[']", 'nghiêm', text)
    text = text.replace('nghiềm', 'nghiêm')
    
    # 3. sï → sĩ
    text = text.replace('sï', 'sĩ')
    # Also sỉ → sĩ in some cases (sỉ-phu → sĩ-phu)
    text = text.replace('sỉ', 'sĩ')
    
    # 4. ÿ → kỳ (Trung-ÿ → Trung-kỳ, etc.)
    # But not if ÿ is part of a proper name or French
    text = re.sub(r'ÿ(?=[\s,;.:!?)\]]|$)', 'kỳ', text)
    text = re.sub(r'Trung-ÿ', 'Trung-kỳ', text)
    text = re.sub(r'Nam-ÿ', 'Nam-kỳ', text)
    text = re.sub(r'Bắc-ÿ', 'Bắc-kỳ', text)
    # standalone ÿ
    text = re.sub(r'\bÿ\b', 'kỳ', text)
    
    # 5. Individual character fixes in common words
    replacements = {
        'dai-diên': 'đại-diện',
        'dai-diện': 'đại-diện',
        'Trungkÿ': 'Trung-kỳ',
        'Viét-Nam': 'Việt-Nam',
        'Viétnam': 'Việt-Nam',
        'bỉnh-sĩ': 'binh-sĩ',
        'qui-vât': 'qui-vật',
        'thờitiết': 'thời-tiết',
        'liênmiên': 'liên-miên',
        'sậm-sụt': 'sầm-sụt',
        'phong-trän': 'phong-trần',
        'rầu rãi': 'dầu dãi',
        'nằm là': 'nằm ỳ',
        'vồng': 'võng',
        'bỉnh-sĩ': 'binh-sĩ',
        'lươngthực': 'lương-thực',
        'chẩy': 'chảy',
        'cẩm': 'cảm',
        'Chänh-phà': 'Chánh-phủ',
        'Vọng -các': 'Vọng-các',
        'täng-phäm': 'tặng-phẩm',
        'vươngtriều': 'vương-triều',
        'zin': 'xin',
        'côn lệ-thuộc': 'còn lệ-thuộc',
        'triền-đình': 'triều-đình',
        'Bai-üy': 'Bại-úy',
        'tiều-đoàn': 'tiểu-đoàn',
        'chi-luu': 'chi-lưu',
        'ngủ dèm': 'ngủ đêm',
        'ngũ tai': 'ngủ tại',
        'thứ chin': 'thứ chín',
        'nghi chân': 'nghỉ chân',
        'quäng': 'quãng',
        'cà đoàn': 'cả đoàn',
        'do đỏ': 'do đó',
        'vơi': 'voi',
        'khỏ đầu': 'khó đầu',
        'vi thế': 'vì thế',
        'cần thận': 'cẩn thận',
        'mệnh-một': 'mệnh-một',
        'bôn tầu': 'bôn tẩu',
        'vôi-vä': 'vội-vã',
        'bổ chạy': 'bỏ chạy',
        'khổi': 'khỏi',
        'không quả': 'không quá',
        'Quihợp': 'Quy-hợp',
        'Qui-hop': 'Quy-hợp',
        'Hàm-thảo': 'Hàm-thao',
        'toi đón': 'tới đón',
        'ngu-dao': 'ngự-đạo',
        'rước Vua': 'rước vua',
        'dà được bot': 'đã được bớt',
        'Mệ-Tríu': 'Mệ-Trìu',
        'Tù-Dũ': 'Từ-Dũ',
        'kề tội': 'kể tội',
        'Hà-Tinb': 'Hà-Tĩnh',
        'hiềm-yếu': 'hiểm-yếu',
        'Ân-sât': 'Án-sát',
        'Huÿnh-xuân-Phong': 'Huỳnh-xuân-Phong',
        'Triphủ': 'Tri-phủ',
        'Ngụy - khắc- Kiều': 'Ngụy-Khắc-Kiều',
        'Phan-khäc-Hôa': 'Phan-Khắc-Hòa',
        'Ản-sát': 'Án-sát',
        'nguyèn': 'nguyên',
        'Đô-ngg-sử': 'Đô-ngự-sử',
        'Tän-lÿ': 'Tán-lý',
        'Son-Phông': 'Sơn-Phòng',
        'thihành': 'thi-hành',
        'Cän-vrong': 'Cần-vương',
        'chiến Cän-vrong': 'chiếu Cần-vương',
        'l8': 'lời',
        'thèm': 'thêm',
        'dai-ÿ': 'đại-ý',
        'hiệpước': 'hiệp-ước',
        'Länh-sự': 'Lãnh-sự',
        'di-sẩn': 'di-sản',
        'dänh': 'đánh',
        'sủng lớn': 'súng lớn',
        'nhà-hiép': 'nhà-hiếp',
        'Triëu-dinh': 'Triều-đình',
        'quân đân': 'quân dân',
        'Hoàngthành': 'Hoàng-thành',
        'thihänh': 'thi-hành',
        'tai đế-đô': 'tại-đế-đô',
        'Nghệan': 'Nghệ-an',
        'tiêuđiệt': 'tiêu-diệt',
        'khôi-phuc': 'khôi-phục',
        'tät-nhièn': 'tất-nhiên',
        'dinh-chinh': 'đính-chính',
        'triêt-dè': 'triệt-để',
        'khai-thác': 'khai-thác',
        'Tü-Dü': 'Từ-Dũ',
        'Kinhlược phu-khuyét': 'Kinh-lược phó-sứ',
        'Nguyễn-trọng-Hợp.': 'Nguyễn-Trọng-Hợp',
        'Thải-hận': 'Thái-hậu',
        'phỉnh gat': 'phỉnh-gạt',
        'bién-cô': 'biến-cố',
        'bạo thiên nghịch dia': 'bạo thiên nghịch địa',
        'lưu đầy': 'lưu đày',
        'Hoäng-tôc': 'Hoàng-tộc',
        'väo': 'vào',
        'ngôi bán': 'ngôi báu',
        'dược tôn': 'được tôn',
        'vién': 'viên',
        'Phu-chänh': 'Phụ-chánh',
        'hư-Irugền': 'hư-truyền',
        'viéc nàg': 'việc nầy',
        'mua Kiến-Phúc': 'vua Kiến-Phúc',
        'cỏn': 'còn',
        'biển-cố': 'biến-cố',
        'xẩu ra': 'xảy ra',
        'hoànfoàn': 'hoàn-toàn',
        'Tôn-thät-Thayët': 'Tôn-thất-Thuyết',
        'Nguyễn-uän-Tường': 'Nguyễn-văn-Tường',
        'gâu nên': 'gây nên',
        'củng': 'cùng',
        'một lỏng một chi': 'một lòng một dạ',
        'sau.bọn': 'sau bọn',
        'khiển': 'khiến',
        'cửu Miếu': 'tôn miếu',
        'sợi tợ': 'sợi tơ',
        'Hoäng-thién': 'Hoàng-thiên',
        'häo-tâm': 'hảo-tâm',
        'sóng naụ đã tên': 'sóng dữ đã êm',
        '0.0': 'v.v.',
        'tuyênngôn': 'tuyên-ngôn',
        'phuhoa': 'phù-hoa',
        'Viét-gian': 'Việt-gian',
        'đồi bên': 'đôi bên',
        'hồi ảm': 'hồi âm',
        'mạt.sảt': 'mạt-sát',
        'Häm-nghi': 'Hàm-nghi',
        'phuhoa': 'phù-hoa',
        'quảng bả': 'quảng cáo',
        'uy -tín': 'uy-tín',
        'thäi-hâu': 'thái-hậu',
        'di-nhièn': 'đi-nhiên',
        'thề.': 'thể',
        'Häm-nghi': 'Hàm-nghi',
        'giátrị': 'giá-trị',
        'ải-quốc': 'ái-quốc',
        'cô-động': 'cổ-động',
        'häng-häi': 'hăng-hái',
        'Thực-dân': 'Thực-dân',
        'lửa dạy': 'lửa dậy',
        'phéngtrèo': 'phòng-trào',
        'Binh-thuân': 'Bình-thuận',
        'lương-giảo': 'lương-giáo',
        'bi-thẩm': 'bi-thảm',
        'côn-đồ': 'côn-đồ',
        'nỗi lên': 'nổi lên',
        'sỉ- phu': 'sĩ-phu',
        'tinh thế': 'tình thế',
        'rôi-ren': 'rối-ren',
        'lung-tung': 'lung-tung',
        'kề xiết': 'kể xiết',
        'Vän-Thân': 'Văn-Thân',
        'khoa-muc': 'khoa-mục',
        'triêt-ha': 'triệt-hạ',
        'Cônggiáo': 'Công-giáo',
        'đàn-áp': 'đàn-áp',
        'nhém': 'nhóm',
        'Trần-quang-Cần': 'Trần-Quang-Cần',
        'Trương-quang-Thủ': 'Trương-Quang-Thủ',
        'Nguyễn-huy-Điền': 'Nguyễn-Huy-Điền',
        'Nguyén-vắn-Tường': 'Nguyễn-văn-Tường',
        'Tổngthống': 'Tổng-thống',
        'khôïi-nghïa': 'khởi-nghĩa',
        'bất đầu': 'bắt đầu',
        'điệt-trừ': 'điệt-trừ',
        'dung-tüng': 'dung-túng',
        'Vän-Thân Nghệ Tĩnh': 'Văn-Thân Nghệ-Tĩnh',
        'ngắm-ngầm': 'ngấm-ngầm',
        'thải-độ': 'thái-độ',
        'rồ-rệt': 'rõ-rệt',
        'quần Pháp': 'quân Pháp',
        'lièn-lac': 'liên-lạc',
        'thấtthủ': 'thất-thủ',
        'nắm': 'năm',
        'quản Pháp': 'quân Pháp',
        'Có lễ': 'Có lẽ',
        'dồn': 'đồn',
        'vịtrí': 'vị-trí',
        'vô-ich': 'vô-ích',
        'nhàn-sĩ': 'nhân-sĩ',
        'Sơn-Phỏng': 'Sơn-phòng',
        'Nghĩa-hội': 'Nghĩa-hội',
        'bức nh-thành': 'bức tỉnh thành',
        'Tuän-Vü': 'Tuần-Vũ',
        'Nguyễn-Ngoạn': 'Nguyễn-Ngoạn',
        'Bố-chá£n': 'Bố-chánh',
        'Hä-thüc-Quän': 'Hà-Thúc-Quán',
        'dược': 'được',
        'Trüng-lôc': 'Trung-lộc',
        'tan rä': 'tan rã',
        'tnh-ly': 'tỉnh-lỵ',
        'Nguyễn-HH': 'Nguyễn-',
        'dày đẳng': 'đấy đẳng',
        'van-miéu': 'văn-miếu',
        'Thäng': 'Tháng',
        'nam': 'năm',
        'phü-du': 'phủ-dụ',
        'Tông-Pôc': 'Tổng-đốc',
        'Ân-sät': 'Án-sát',
        'Nguyễn-đinh-Văn': 'Nguyễn-Đình-Văn',
        'Võ-doän-Tuân': 'Võ-Doãn-Tuân',
        'An-sät': 'Án-sát',
        'cù-muc': 'cựu-mục',
        'hầu hét': 'hầu hết',
        'tịch-thu': 'tịch-thu',
        'Nguyễn-Thân': 'Nguyễn-Thân',
        'Quäng-Nam': 'Quảng-Nam',
        'chiêu-thão-sử': 'chiêu-thảo-sứ',
        'bai': 'hai',
        'kếtliễu': 'kết-liễu',
        'Tỉ-trựckỷ': 'Tả-trực kỳ',
        'Tuyênẩy': 'Tuyên-ủy',
        'đạithần': 'đại thần',
        'hièu-thi': 'hiểu-thị',
        'Bäc-kÿ': 'Bắc-kỳ',
        'thựcdân': 'thực-dân',
        'đẳng Cần-vương': 'đảng Cần-vương',
        'thúc đầy': 'thúc đẩy',
        'sĩdân': 'sĩ-dân',
        'Quảng - ngãi': 'Quảng-Ngãi',
        'thôa-hiép': 'thỏa-hiệp',
        'Nghĩa-Định chiêu-thảo-sứ': 'Nghĩa-Định chiêu-thảo-sứ',
        'Quäng-Ngäi': 'Quảng-Ngãi',
        'giết tróc': 'giết tróc',
        'Binh-thuận': 'Bình-thuận',
        'Khänh-hôa': 'Khánh-Hòa',
        'Phú-yên': 'Phú-Yên',
        'Trän-bä-Lôc': 'Trần-bá-Lộc',
        'Thiếu-tá De Lorme': 'Thiếu-tá De Lorme',
        'Trü-str': 'Trù-sự',
        'đánh dep': 'đánh dẹp',
        'chiën-': 'chiến-',
        'ich đài rộng': 'liên-đài rộng',
        'chät-chè': 'chặt-chẽ',
        'thủ-đoạn dã-man': 'thủ-đoạn dã-man',
        'kinh tổm': 'kinh tởm',
        'cải chước': 'cái chước',
        'lấp dé giết dé': 'lấp dế giết dế',
        'hiéu-nghiêm': 'hiệu-nghiêm',
        'Tbáng': 'Tháng',
        'Pinh-hợi': 'Đinh-Hợi',
        'Phỏdướng': 'Phó-tướng',
        'nghĩaquân': 'nghĩa-quân',
        'cử-mục': 'cựu-mục',
        'Phü-Yèn': 'Phú-Yên',
        'Ẩn.sát': 'Án-sát',
        'Huÿnh-Côn': 'Huỳnh-Côn',
        'Tä.lÿ': 'Tả-lý',
        'Luong-xuân-Huyèn': 'Lương-xuân-Huyền',
        'Cao-Đệ': 'Cao-Đệ',
        'Bố-chảnh': 'Bố-chánh',
        'An-sat': 'Án-sát',
        'Tôn<hät-Bâ': 'Tôn-thất-Bá',
        'än-sät': 'Án-sát',
        'Đinh-duy-Tân': 'Đinh-Duy-Tân',
        'câch-mang': 'cách-mạng',
        'Tống-duy-Tän': 'Tống-Duy-Tân',
        'Hươngkhê': 'Hương-Khê',
        'HùngLĩnh': 'Hùng-Lĩnh',
        'trường hoat-dông': 'trường hoạt-động',
        'khángdịch': 'kháng-địch',
        'kề rành - mạch': 'kể rành-mạch',
        'nồi tiếng': 'nổi tiếng',
        'anh-düng': 'anh-dũng',
        'thám-phục': 'thán-phục',
        'Trung - kỷ': 'Trung-kỳ',
        'lam tiết': 'làm tiếc',
        'Quốc--quận hồng của ngay-chyền': 'quốc-sử hồng của ngay-chuyền',
        'ghỉ chép': 'ghi chép',
        'Miễn Bắc': 'miền Bắc',
        'khôïnghia': 'khởi-nghĩa',
        'Nam-Ngãi': 'Nam-Ngãi',
        'dàiđược': 'dài được',
        'Trung-kÿ': 'Trung-kỳ',
        'trổ ra': 'trở ra',
        'địalỷ': 'địa-lý',
        'De- Courcy': 'De Courcy',
        'đuồi theo': 'đuổi theo',
        'Thäng': 'Tháng',
        'nằm ấy': 'năm ấy',
        'tỉnh-ly': 'tỉnh-ly',
        'chi': 'chỉ',
        'it kể': 'ít kẻ',
        'không đảm': 'không dám',
        'thuở đỏ': 'thuở đó',
        'vườn không nhà trống': 'vườn không nhà trống',
        'lai còn': 'lại còn',
        'nộituyến': 'nội-tuyến',
        'đốt phả': 'đốt phá',
        'Công-giäo': 'Công-giáo',
        'nguy-binh': 'nguy-binh',
        'chi-diém': 'chỉ-điểm',
        'Thiếutá': 'Thiếu-tá',
        'thịsát': 'thị-sát',
        'tải lập': 'tái lập',
        'Chợ -Säi': 'Chợ-Sãi',
        'sầm-uất': 'sầm-uất',
        'gi ổa': 'giữa',
        'Chủngviện': 'Chủng-viện',
        'giảo-dân': 'giáo-dân',
        'Bäi-Son': 'Bãi-Sơn',
        'giảo-dân': 'giáo-dân',
        'Công-giảo': 'Công-giáo',
        'năm ruôi': 'năm rưỡi',
        'giảo-đân': 'giáo-dân',
        'giảo-đường': 'giáo-đường',
        'Luong-giäo': 'Lương-giáo',
        'ải-quốc': 'ái-quốc',
        'nhan': 'mạnh',
        'dai-dôi': 'đại-đội',
        'Quäng-tri': 'Quảng-trị',
        'thắm': 'thăm',
        'Cam -lộ': 'Cam-lộ',
        'Tân-Sở': 'Tân-Sở',
        'Mai-lĩnh': 'Mai-lĩnh',
        'Do-lính': 'Do-lính',
        'viở đây': 'vì ở đây',
        'điện -tín': 'điện-tín',
        'giết': 'giết',
        'Giáosĩ': 'Giáo-sĩ',
        'Kháng -chiến': 'Kháng-chiến',
        'tàn-sảt': 'tàn-sát',
        'kết- quả': 'kết-quả',
        'khả - quan': 'khả-quan',
        'Thiếu-tưởng': 'Thiếu-tướng',
        'Prudhomne': 'Prudhomme',
        'phànnàn': 'phàn-nàn',
        'Bao-ngu': 'Bao-ngu',
        'ần núp': 'ẩn núp',
        'Bãi - Đức': 'Bãi-Đức',
        'Cửa Vé': 'Cửa Vẽ',
        'luu-vyc': 'lưu-vực',
        'chi-lwu': 'chi-lưu',
        'Rào-Nậy': 'Rào-Nậy',
        'Rào-Năn': 'Rào-Năn',
        'thäo-luân': 'thảo-luận',
        'phối:hợp': 'phối-hợp',
        'công-tâc': 'công-tác',
        'vô-ich': 'vô-ích',
        'œó': 'có',
        'rảirác': 'rải-rác',
        'khấp nơi': 'khắp nơi',
        'sổ': 'số',
        'vồilôi': 'với lôi',
        'it nhiền': 'ít nhiều',
        'Kháng:chiến': 'Kháng-chiến',
        'cồn': 'còn',
        'phäi': 'phải',
        'bâo-vé': 'bảo-vệ',
        'đả.đảo': 'đả-đảo',
        'chánh-sảchthì': 'chánh-sách thì',
        'cỏ thề': 'có thể',
        'cổ một': 'có một',
        'nồi da xáo thịt': 'nồi da xáo thịt',
        'thủ-túc tương': 'thủ-túc tương',
        'cỏ thê': 'có thể',
        'chiến.sĩ': 'chiến-sĩ',
        'đàng khác': 'đằng khác',
        'đầy': 'đẩy',
        'song': 'sang',
        'ï': '',
        'Đảng tiếc thay': 'Đáng tiếc thay',
        'NHÜNG': 'NHỮNG',
        'bổ': 'bỏ',
        '&': 'ở',
        'Tĩnh-Bình': 'Tĩnh-Bình',
        'täng cường': 'tăng cường',
        'triêu-dinh': 'triều-đình',
        'lo-ngai': 'lo-ngại',
        'trấn-ĩnh tinb-thän': 'trấn-ĩnh tinh-thần',
        'dé.nghị': 'đề-nghị',
        'bầy cuộc': 'bày cuộc',
        'danh-nghïa': 'danh-nghĩa',
        'linh Pháp': 'lính Pháp',
        'hộ-giá': 'hộ-giá',
        'Quâng-Binh': 'Quảng-Bình',
        'hiêu-quà': 'hiệu-quả',
        'phẩi': 'phải',
        'cổ gắng': 'cố gắng',
        'quỷ kế': 'quỷ kế',
        'Tôngtrấn': 'Tổng-trấn',
        'Hà-tỉnh': 'Hà-tĩnh',
        'hỏng loi-dung': 'hòng lợi-dụng',
        'khäng-chién': 'kháng-chiến',
        'êm địu': 'êm dịu',
        'Phô-mä': 'Phó-mã',
        'Hoàng-tả-Viêm': 'Hoàng-tá-Viêm',
        'Hữu-trực-kỳ': 'Hữu-trực-kỳ',
        'yên-phủ kinh-lược sứ': 'yên-phủ kinh-lược sứ',
        'đảng kề': 'đáng kể',
        'Thựcdân': 'Thực-dân',
        'Vi sao': 'Vì sao',
        'Hoàngtá-Viêm': 'Hoàng-tá-Viêm',
        'nởi tiếng': 'nổi tiếng',
        'chiến-sỉ': 'chiến-sĩ',
        'lĩnh-tụ': 'lĩnh-tụ',
        'trung -kiên': 'trung-kiên',
        'thành-tích': 'thành-tích',
        'cäm-tinh': 'cảm-tình',
        'si-dân': 'sĩ-dân',
        'con cỏ mỗi': 'con cờ mồi',
        'nghi-ngai': 'nghi-ngại',
        'Trương - văn-Ban': 'Trương-Văn-Ban',
        'Nguyễn - Chữ': 'Nguyễn-Chữ',
        'Lê - mộ - Giai': 'Lê-Mộ-Giai',
        'Nguyễn - nguyên-': 'Nguyễn-Nguyên-',
        'Phantrong-Muu': 'Phan-Trọng-Mưu',
        'Nguyễn-xuânÔn': 'Nguyễn-Xuân-Ôn',
        'Lé-doän-Nha': 'Lê-Doãn-Nha',
        'Ngô-xuân-Quýnh': 'Ngô-Xuân-Quýnh',
        'nguyênhàm': 'nguyên-hàm',
        'Trän-xuân-Soạn': 'Trần-xuân-Soạn',
        'Nguyén-pham-Tuân': 'Nguyễn-phạm-Tuân',
        'täi-dung': 'tái-dụng',
        'truy-tố': 'truy-tố',
        'chiêu-đụ': 'chiêu-dụ',
        'Cơ-Mật-viện': 'Cơ-Mật-viện',
        'khổi': 'khỏi',
        'cận-thần': 'cận-thần',
        'twong-lai': 'tương-lai',
        'Pham-vän-Mÿ': 'Phạm-văn-Mỹ',
        'Minh-cim': 'Minh-Cầm',
        'Đạiúy': 'Đại-úy',
        'Boulangier': 'Boulangier',
        'Trương quangNgọc': 'Trương-quang-Ngọc',
        'quốclộ': 'quốc-lộ',
        'cứ-điềm': 'cứ-điểm',
        'khé-khän': 'khó-khăn',
        'phuc-kich': 'phục-kích',
        'hộ-tống': 'hộ-tống',
        'quan-lai': 'quan-lại',
        'Phäp': 'Pháp',
        'đám': 'dám',
        'di-chuyèn': 'di-chuyển',
        'trụsở': 'trụ-sở',
        'lân-cận': 'lân-cận',
        'Quäng-Khè': 'Quảng-Khê',
        'Ha-Tĩnh': 'Hà-Tĩnh',
        'bay': 'hay',
        'đàn': 'dàn',
        'đượ-': 'được',
        'chỈhuy': 'chỉ-huy',
        'tiềnđồn': 'tiền-đồn',
        'xuất-phát binh.sĩ': 'xuất-phát binh-sĩ',
        'khäng-chiến': 'kháng-chiến',
        'CẢ bai bên': 'Cả hai bên',
        'gắng sức': 'gắng sức',
        'thúcthủ': 'thúc-thủ',
        'ló ra': 'ló ra',
        'Ké-viém': 'Kế-Viêm',
        'đồi ra': 'đổi ra',
        'Trần-kếXương': 'Trần-Kế-Xương',
        'Té-Xuong': 'Tế-Xương',
        'giäi-nguy': 'giải-nguy',
        'mở tối': 'mờ tối',
        'đảnh đẹp': 'đánh dẹp',
        'toàn điện': 'toàn diện',
        'dẻo dai': 'dẻo dai',
        'kịch-liệt': 'kịch-liệt',
        'Vi lý-do': 'Vì lý-do',
        'kề tới': 'kể tới',
        'Đồng-hởi': 'Đồng-Hới',
        'Võ cử': 'Võ-cử',
        'Nguyễn viết Tôn': 'Nguyễn-Viết-Tôn',
        'quả ở': 'ở',
        'chi-tiét': 'chi-tiết',
        'đưới đây': 'dưới đây',
        'tòng vong': 'tòng-vong',
        'lần lút': 'lẩn lút',
        'đuồi theo': 'đuổi theo',
        'cồn nhặt': 'còn nhặt',
        'cải võng': 'cái võng',
        'kề cả': 'kể cả',
        'oũng': 'cũng',
        'JA': 'là',
        'Đã thé': 'Đã thế',
        'Trần xuân Soạn': 'Trần-xuân-Soạn',
        'càng càng': 'càng',
        'lim ra': 'tìm ra',
        'Đêm 14 qua 45-8-4686': 'Đêm 14 qua 15-8-1886',
        'đảm': 'đám',
        'Tü-tài Phòng': 'Tú-tài Phòng',
        'đây lui': 'đẩy lui',
        'si quan': 'sĩ quan',
        'Tham-biện sử-qguán': 'Tham-biện sứ-quán',
        'Thiểu-tả': 'Thiếu-tá',
        'Kháng chiến.': 'Kháng-chiến',
        'ho gián': 'dán',
        'Tòa Khảm': 'Tòa Khâm',
        'thỏa mạ': 'thoá mạ',
        'cỏ kỀ': 'có kể',
        'Nguyễn-hữn Độ': 'Nguyễn-hữu-Độ',
        'Co mật-viện': 'Cơ-mật-viện',
        'Tön-thất-Thuyết': 'Tôn-thất-Thuyết',
        'sồ Tên Thất': 'sổ Tôn-Thất',
        'cải qua': 'cải sang',
        'sắc-dụ đưởi đời': 'sắc-dụ dưới đời',
        'Khẩi-Định': 'Khải-Định',
        'phương điện': 'phương diện',
        'linh tụ': 'lĩnh-tụ',
    }
    
    # Apply all replacements (longest first to avoid partial replacements)
    for old, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    
    # Fix specific character-level issues
    # 'd' -> 'đ' at word starts if it should be đ
    # But only for specific known words, not blanket replacement
    
    # Fix 0 at start of word -> Ô
    text = re.sub(r'\b0([a-z]*)', r'Ô\1', text)
    
    # Fix some a/ă/â confusions by context
    text = re.sub(r'\bHàm-nghỉ\b', 'Hàm-nghi', text)
    text = re.sub(r'\bHàm-Nghỉ\b', 'Hàm-Nghi', text)
    text = text.replace('Hàm-nghỉ', 'Hàm-nghi')
    
    # Fix date formats: remove spaces in dates
    text = re.sub(r'(\d) (\d)-(\d)-(\d{4})', r'\1\2-\3-\4', text)
    text = re.sub(r'(\d)-(\d) (\d{4})', r'\1-\2-\3', text)
    
    # Fix 17 10.1885 -> 17-10-1885
    text = re.sub(r'(\d+) ?[.] ?(\d+) ?[.] ?(\d{4})', r'\1-\2-\3', text)
    
    # Fix various date OCR errors
    text = re.sub(r'45-8-4686', '15-8-1886', text)
    text = re.sub(r'18-8-1886', '18-8-1885', text)  # Context: this is the 12th day from 5-6 Aug 1885
    
    # Fix Hàm-Nghỉ to Hàm-Nghi
    text = re.sub(r'Hàm[- ]?Nghỉ', 'Hàm-Nghi', text)
    text = re.sub(r'Hàm[- ]?nghỉ(?![\w])', 'Hàm-nghi', text)
    
    # Fix scattered punctuation
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\.{2,}', '.', text)
    
    # Remove leading/trailing whitespace on each line
    lines = text.split('\n')
    lines = [l.rstrip() for l in lines]
    text = '\n'.join(lines)
    
    # Normalize multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^\n+', '', text)
    text = re.sub(r'\n+$', '', text)
    
    return text


def main():
    with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch5-raw.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned = clean(text)
    
    with open('/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch5-clean.txt', 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"Cleaned text: {len(cleaned)} chars, {len(cleaned.split(chr(10)))} lines")
    print("Written to ch5-clean.txt")


if __name__ == '__main__':
    main()
