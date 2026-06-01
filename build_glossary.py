#!/usr/bin/env python3
"""Build glossary of proper names from Chapter I VSTB Vol 6."""
import re

CLEANED = "/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/ch2-clean.txt"
GLOSSARY = "/home/vthen/work/post-colonial-vietnam/sources/vstb/translations/glossary-ch2.md"

with open(CLEANED, 'r') as f:
    text = f.read()

# Extract all capitalized Vietnamese compound names
# Vietnamese proper names use hyphens: Tôn-Thất-Thuyết, Nguyễn-văn-Tường
vn_name_pattern = r'[A-ZĐÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+(?:[-][A-ZĐÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+)*'

# French names
fr_pattern = r'[A-Z][a-zéèêëàâäùûüôöîïçÉÈÊËÀÂÄÙÛÜÔÖÎÏÇ]+(?:[-][A-Z][a-zéèêëàâäùûüôöîïç]+)*'

# Find all matches
vn_names = set(re.findall(vn_name_pattern, text))
fr_names = set(re.findall(fr_pattern, text))

# Filter to proper names (not common words at start of sentences)
# Vietnamese compound names typically have 2+ capitalized parts separated by hyphens
# Or are single words that are clearly names

# Known proper names from context
proper_names = {
    # People - Vietnamese
    'Tôn-Thất-Thuyết': 'Tôn Thất Thuyết — Regent, leader of the anti-French resistance at the Huế court',
    'Nguyễn-văn-Tường': 'Nguyễn Văn Tường — Co-Regent, colleague of Tôn Thất Thuyết',
    'Tôn-Thất-Lễ': 'Tôn Thất Lễ — Vietnamese commander during the attack on the French Legation',
    'Tôn-thất-Đạm': 'Tôn Thất Đạm — Son of Tôn Thất Thuyết',
    'Trần-xuân-Soạn': 'Trần Xuân Soạn — Đề-đốc (Admiral/Governor) who commanded the attack on Trấn-Bình-Đài',
    'Phạm-Thận-Duật': 'Phạm Thận Duật — Court official who attended de Courcy\'s banquet',
    'Hàm-Nghi': 'Hàm Nghi — Emperor of Vietnam (r. 1884–1885), fled after the fall of the Citadel',
    'Kiến-Phúc': 'Kiến Phúc — Emperor of Vietnam (r. 1883–1884), predecessor of Hàm Nghi',
    'Từ-Dũ': 'Từ Dũ — Dowager Empress, mother of Emperor Tự Đức',
    'Lưu-Vĩnh-Phúc': 'Lưu Vĩnh Phúc — Chinese commander of the Black Flag Army',
    'Guerrier': 'Guerrier — French official involved in Hàm Nghi\'s enthronement',
    'Lemaire': 'Lemaire — French Resident (Khâm-sứ) in Huế before de Courcy',
    'Champeaux': 'de Champeaux — French Resident (Khâm-sứ) in Huế during de Courcy\'s arrival',
    'Rheinart': 'Rheinart — Previous French Resident in Huế',
    'Courbet': 'Courbet — French Admiral who died just before de Courcy arrived',
    'Brière de l\'Isle': 'Brière de l\'Isle — French General commanding in Tonkin',
    'Pernot': 'Pernot — French Lieutenant-Colonel (Trung-tá) commanding at Mang Cá',
    'Metzinger': 'Metzinger — French Chef de Bataillon (Thiếu-tá)',
    'Gosselin': 'Gosselin — French Captain (Đại-Úy), author of "L\'Empire d\'Annam"',
    'Bouché': 'Bouché — French Second Lieutenant (Trung-úy) on duty the night of the attack',
    'Bruneau': 'Bruneau — French Captain (Đại-Úy) killed in the battle',
    'Drouin': 'Drouin — French Captain (Đại-Úy) wounded in the battle',
    'Constant': 'Constant — French Second Lieutenant (Trung-úy) wounded in the battle',
    'La Croix': 'La Croix — French Second Lieutenant wounded in the battle',
    'Heitschel': 'Heitschel — French Second Lieutenant killed in the battle',
    'Caspar': 'Caspar — French missionary (Giám-mục) who spied for the French',
    'Mangin': 'Mangin — French military doctor sent to check on Tôn Thất Thuyết',
    'Garnier': 'Francis Garnier — French officer who seized the Huế citadel in 1873',
    'Rivière': 'Henri Rivière — French officer killed at the Battle of Paper Bridge, 1883',
    'Brisson': 'Brisson — French Prime Minister who replaced Jules Ferry',
    'Ferry': 'Jules Ferry — French Prime Minister, architect of colonial expansion',
    'Millot': 'Millot — French General commanding in Tonkin before Brière de l\'Isle',
    'Campbell': 'J. Duncan Campbell — Chinese Customs official who mediated the Sino-French ceasefire',
    'Billot': 'Billot — French Foreign Ministry inspector who signed the ceasefire',
    'Delvaux': 'A. Delvaux — French author of "Guerre du Tonkin"',
    'Thomson': 'Thomson — French Governor of Cochinchina (Nam Kỳ)',
    'Diệp-văn-Kỳ': 'Diệp Văn Kỳ — Southern Vietnamese intellectual',
    'Gosselin': 'Charles Gosselin — French officer and author',
    'Bửu Kế': 'Bửu Kế — Author of article in Bách Khoa magazine',
    'Marchant de Trigon': 'Marchant de Trigon — French author on Hàm Nghi\'s enthronement',
    'Cosserat': 'Cosserat — French author on Hàm Nghi\'s enthronement',
    'Marcel Gauthier': 'Marcel Gauthier — French author of "Le roi proscrit"',
    'Max de Pirey': 'Max de Pirey — French missionary',
    
    # Places
    'Huế': 'Huế — Imperial capital of the Nguyễn dynasty',
    'Kinh-thành': 'Kinh-thành (Imperial Citadel) — The walled capital in Huế',
    'Hoàng-thành': 'Hoàng-thành (Imperial Enclosure) — Inner citadel containing the palaces',
    'Đại Nội': 'Đại Nội (Imperial Palace/Forbidden City) — The innermost palaces',
    'Mang Cá': 'Mang Cá — French military camp near the Huế citadel',
    'Tòa Khâm': 'Tòa Khâm (Office of the Khâm-sứ/French Resident) — French Legation in Huế',
    'Sứ-quán': 'Sứ-quán (French Legation) — The French diplomatic mission',
    'Cửa Thuận': 'Thuận An — Coastal port and entry point to Huế',
    'Thuận-Hóa': 'Thuận Hóa — Historical name for the Huế region',
    'Trấn-Bình-Đài': 'Trấn-Bình-Đài (Mang Cá fort) — The French fort at Mang Cá',
    'Cầu Thanh-Long': 'Cầu Thanh Long (Green Dragon Bridge) — Bridge in Huế, later called Pont de l\'attentat',
    'Cửa Đông Ba': 'Đông Ba Gate — Eastern gate of the Huế citadel',
    'Cửa An-Hòa': 'An Hòa Gate — Gate of the Huế citadel',
    'Cửa Hiền Nhơn': 'Hiền Nhơn Gate — Gate of the Huế citadel',
    'Cửa Hậu': 'Rear Gate — Gate of the Huế citadel',
    'Vịnh Hạ-long': 'Hạ Long Bay — Bay in northern Vietnam where de Courcy arrived',
    'Bắc-kỳ': 'Bắc Kỳ (Tonkin) — Northern region of Vietnam',
    'Nam-kỳ': 'Nam Kỳ (Cochinchina) — Southern region of Vietnam',
    'Trung-du': 'Trung du (Midlands) — Transitional region between delta and highlands',
    'Trung-châu': 'Trung châu (Delta) — The Red River Delta',
    'sông Hồng': 'Red River — Major river in northern Vietnam',
    'Tam-Đảo': 'Tam Đảo — Mountain range north of Hanoi',
    'Vĩnh-Yên': 'Vĩnh Yên — Town in northern Vietnam',
    'Thái-Nguyên': 'Thái Nguyên — Province in northern Vietnam',
    'Tuyên-quang': 'Tuyên Quang — Province in northern Vietnam',
    'Hưng-Hóa': 'Hưng Hóa — Province in northern Vietnam',
    'Hà-nội': 'Hanoi — Capital of Tonkin',
    'Hải-phòng': 'Hải Phòng — Major port city in northern Vietnam',
    'Thuận-An': 'Thuận An — Coastal entry point to Huế',
    'Trường-giang': 'Trường Giang (Yangtze River) — River in China, referent of naval blockade',
    'Bắc-kinh': 'Bắc Kinh (Beijing) — Capital of the Qing dynasty',
    'Thanh-đình': 'Thanh đình (Qing court) — The Chinese imperial government',
    'Viễn-đông': 'Viễn Đông (Far East)',
    'Cao Miên': 'Cao Miên (Cambodia)',
    'Ai Lao': 'Ai Lao (Laos)',
    'Quảng-Trị': 'Quảng Trị — Province in central Vietnam',
    'Thanh-Hóa': 'Thanh Hóa — Province in central Vietnam',
    'Sơn-phòng': 'Sơn phòng (Mountain防御 post)',
    'Cam Lộ': 'Cam Lộ — District in Quảng Trị',
    'Mai Linh': 'Mai Linh — Place of exile',
    
    # Treaties and historical terms
    'Hòa-ước Patenôtre': 'Patenôtre Treaty (1884) — Treaty establishing the French protectorate over Vietnam',
    'Hòa-ước Quý-Mùi': 'Quý Mùi Treaty (Harmand Treaty, 1883) — First protectorate treaty',
    'Hòa-ước Giáp-thân': 'Giáp Thân Treaty (Patenôtre Treaty, 1884) — Second protectorate treaty',
    'Hội-đồng Phụ-chính': 'Hội đồng Phụ chính (Regency Council) — Council of regents ruling in the emperor\'s name',
    'Cơ-mật-viện': 'Cơ mật viện (Secret Council/Privy Council) — Highest advisory body to the emperor',
    'Bộ Binh': 'Bộ Binh (Ministry of War)',
    'bộ Lại': 'Bộ Lại (Ministry of Personnel/Civil Service)',
    'Tôn Nhân Phủ': 'Tôn Nhân Phủ (Imperial Clan Court)',
    
    # People - French
    'De Courcy': 'De Courcy — French General and Governor-General of Indochina, sent to pacify Vietnam in 1885',
    'Courbet': 'Courbet — French Admiral who commanded the naval blockade',
    'Brière de l\'Isle': 'Brière de l\'Isle — French General commanding in Tonkin',
    'Garnier': 'Francis Garnier — French naval officer who seized the Huế citadel in 1873',
    'Rivière': 'Henri Rivière — French naval officer killed in 1883',
    'Patenôtre': 'Jules Patenôtre — French diplomat who negotiated the 1884 treaty',
    'Champeaux': 'de Champeaux — French Resident in Huế',
}

# Build glossary markdown
glossary_lines = [
    '# Glossary — Chapter I: De Courcy Provokes the Southern Court\'s Resistance',
    '# The Fall of the Imperial Citadel (Ất-Dậu-1885)',
    '',
    '## Usage Note',
    'Vietnamese proper names are preserved in the translation. Titles are translated on first appearance with the Vietnamese original in parentheses, then rendered in English thereafter. Both lunar and Western calendar dates are retained.',
    '',
    '## People',
    '',
]

# Sort by category
people_vn = []
people_fr = []
places = []
treaties = []

for name, desc in sorted(proper_names.items()):
    # Categorize
    is_fr = any(fr in name for fr in ['De Courcy', 'Brière', 'Courbet', 'Garnier', 'Rivière', 
                'Patenôtre', 'Champeaux', 'Lemaire', 'Rheinart', 'Pernot', 'Metzinger',
                'Gosselin', 'Bouché', 'Bruneau', 'Drouin', 'Constant', 'La Croix', 
                'Heitschel', 'Caspar', 'Mangin', 'Ferry', 'Brisson', 'Millot',
                'Campbell', 'Billot', 'Delvaux', 'Thomson', 'Gosselin', 'Marchant',
                'Cosserat', 'Gauthier', 'Max de Pirey', 'Trigón', 'Guerrier'])
    
    is_treaty = any(t in name for t in ['Hòa-ước', 'Treaty'])
    is_place = any(p in name for p in ['Huế', 'Kinh-thành', 'Hoàng-thành', 'Đại Nội', 
                 'Mang Cá', 'Tòa Khâm', 'Sứ-quán', 'Cửa Thuận', 'Thuận-Hóa', 
                 'Trấn-Bình', 'Cầu Thanh', 'Cửa Đông', 'Cửa An', 'Cửa Hiền',
                 'Vịnh', 'Bắc-kỳ', 'Nam-kỳ', 'Trung-du', 'Trung-châu', 'sông Hồng',
                 'Tam-Đảo', 'Vĩnh-Yên', 'Thái-Nguyên', 'Tuyên-quang', 'Hưng-Hóa',
                 'Hà-nội', 'Hải-phòng', 'Thuận-An', 'Trường-giang', 'Bắc-kinh',
                 'Thanh-đình', 'Viễn-đông', 'Cao Miên', 'Ai Lao', 'Quảng-Trị',
                 'Thanh-Hóa', 'Sơn-phòng', 'Cam Lộ', 'Mai Linh'])
    
    if is_place:
        places.append(f'- **{name}** — {desc}')
    elif is_treaty or any(t in name for t in ['Hội-đồng', 'Cơ-mật', 'Bộ Binh', 'bộ Lại', 'Tôn Nhân']):
        treaties.append(f'- **{name}** — {desc}')
    elif is_fr:
        people_fr.append(f'- **{name}** — {desc}')
    else:
        people_vn.append(f'- **{name}** — {desc}')

glossary_lines.append('### Vietnamese')
glossary_lines.append('')
glossary_lines.extend(people_vn)
glossary_lines.append('')
glossary_lines.append('### French')
glossary_lines.append('')
glossary_lines.extend(people_fr)
glossary_lines.append('')
glossary_lines.append('## Places')
glossary_lines.append('')
glossary_lines.extend(places)
glossary_lines.append('')
glossary_lines.append('## Treaties & Institutions')
glossary_lines.append('')
glossary_lines.extend(treaties)
glossary_lines.append('')

with open(GLOSSARY, 'w') as f:
    f.write('\n'.join(glossary_lines))

print(f"Glossary written: {GLOSSARY}")
print(f"Entries: {len(people_vn)} VN people, {len(people_fr)} French people, {len(places)} places, {len(treaties)} treaties/institutions")
