# Vietnamese Book Translation — Session Reference

## Books Translated This Session

### 1. *Bảy Viễn — Thủ Lĩnh Bình Xuyên* (Bay Vien: The Binh Xuyen Leader)
- **Author**: Nguyên Hùng (Nguyen Hung)
- **Format**: PDF, 185 pages, embedded text
- **Content**: Documentary novel about Lê Văn Viễn (Bảy Viễn), Bình Xuyên leader in 1940s-50s Saigon
- **Size**: ~395K Vietnamese chars, 80 chapters
- **Output**: 466-page English PDF, colloquial storytelling voice
- **Key characters**: Bảy Viễn, Mười Trí, Ba Dương, Khăm Chay, Thomas Phước, Ngô Đình Diệm, Bảo Đại

### 2. *Quân Đội CAO ĐÀI* (The Cao Dai Army)
- **Compiler**: Tỉnh Tâm
- **Format**: PDF, 108 pages, InDesign, embedded text + 44 images
- **Content**: Documentary history of the Cao Dai religious sect's military
- **Size**: ~50K Vietnamese chars, 4 sections + appendix (6 documents)
- **Output**: 53-page English PDF with 21 embedded photos
- **Key figures**: Hộ Pháp Phạm Công Tắc, Trần Quang Vinh, Nguyễn Thành Phương, Trình Minh Thế
- **Connection**: Bảy Viễn signs 1955 United National Front alongside Hộ Pháp

## Glossary Patterns

### Narrative Vietnamese books:
- Bảy Viễn → keep as Bảy Viễn (never "Seven Vien")
- Bình Xuyên → keep as Bình Xuyên
- giang hồ → gangster / underworld (context)
- nối khố → sworn brother ("sharing a loincloth")
- ăn thua đủ → "go all the way / play for keeps"
- Chi đội → battalion/regiment
- Phòng Nhì → Deuxième Bureau

### Cao Dai religious/historical texts:
- Đức Hộ Pháp → His Holiness the Pope (gloss once, keep Vietnamese)
- Bần Đạo → "This humble priest"
- Tòa Thánh → Holy See (Tây Ninh)
- Thánh Thất → Holy Temple
- Đức Chí Tôn → The Supreme Being
- Nội Ứng Nghĩa Binh → Internal Response Righteous Army
- Thiếu Tướng → Major General / Trung Tướng → Lieutenant General

## Voice Decision Tree

| Tone of source | Translate as | Example |
|---|---|---|
| Novel with dialogue/action | Colloquial storytelling | Bảy Viễn |
| Documentary/historical compilation | Clear expository, formal for letters | Cao Đài Army |
| Official correspondence | Formal register, period terms | Hộ Pháp letters |
| Poem/verse | Rhymed English, emotional weight preserved | Trình Minh Thế's poem |

## Image Pipeline
```bash
pdfimages -j input.pdf /tmp/images/img
python3 -c "from PIL import Image; Image.open('img.ppm').save('img.jpg', 'JPEG', quality=85)"
```

## Delivery
- Compile to 6×9 PDF via weasyprint (Georgia 11pt)
- Send to Discord home channel: send_message with MEDIA: path
