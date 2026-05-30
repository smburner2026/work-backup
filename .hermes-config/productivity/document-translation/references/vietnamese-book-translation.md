# Vietnamese Translation — Session Reference & Voice Decision Tree

## Voice Decision Tree

| Tone of source | Translate as | Example book |
|---|---|---|
| Novel with dialogue/action | Colloquial storytelling ("a guy telling a story over a beer") | Bảy Viễn (Binh Xuyen leader) |
| Documentary/historical compilation | Clear expository, formal for letters | Cao Đài Army |
| Official correspondence | Formal register, period terms | Hộ Pháp letters |
| Poem/verse | Rhymed English, emotional weight preserved | Trình Minh Thế's poem |

## Books Translated

### 1. *Bảy Viễn — Thủ Lĩnh Bình Xuyên* (Bay Vien: The Binh Xuyen Leader)
- **Author**: Nguyên Hùng (Nguyen Hung)
- **Format**: PDF, 185 pages, embedded text
- **Content**: Documentary novel about Lê Văn Viễn (Bảy Viễn), Bình Xuyên leader
- **Size**: ~395K Vietnamese chars, 80 chapters
- **Output**: 466-page English PDF, colloquial storytelling voice

### 2. *Quân Đội CAO ĐÀI* (The Cao Dai Army)
- **Compiler**: Tỉnh Tâm
- **Format**: PDF, 108 pages, InDesign, embedded text + 44 images
- **Content**: Documentary history of the Cao Dai religious sect's military
- **Size**: ~50K Vietnamese chars, 4 sections + appendix (6 documents)
- **Output**: 53-page English PDF with 21 embedded photos
- **Key figures**: Hộ Pháp Phạm Công Tắc, Trần Quang Vinh, Nguyễn Thành Phương, Trình Minh Thế

## Image Pipeline (Caodaist book)
```bash
pdfimages -j input.pdf /tmp/images/img
python3 -c "from PIL import Image; Image.open('img.ppm').save('img.jpg', 'JPEG', quality=85)"
```

## Delivery Format
- Compile to 6×9 PDF via weasyprint (Georgia 11pt)
- Send to platform via send_message with MEDIA: path
