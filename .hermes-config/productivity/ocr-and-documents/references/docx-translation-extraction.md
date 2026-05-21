# Extracting Existing Translations from Python-docx

When a project has partial translations in .docx files that need to be merged with new translations in plain text format:

## Technique

```python
from docx import Document

doc = Document('path/to/translation.docx')
full = '\n'.join(p.text for p in doc.paragraphs)

# Find sections by content markers
pos_activity = full.find('ACTIVITY\n')
pos_intensity = full.find('INTENSITY\n')

content = full[pos_activity:pos_intensity].strip()
with open('output.en.txt', 'w') as f:
    f.write('HEADER\n\n' + content)
```

## Pitfalls
- DOCX paragraphs may have different line-ending patterns than the raw join produces.
- Section headings may use different English translations than expected (e.g., "IMMEDIACY: ACTION" vs "IMMEDIACY: ACTING"). Search for partial strings, not exact.
- Use glob + recursive scan to find .docx files when paths contain special characters (apostrophes, unicode).
- Extract in ascending position order to avoid off-by-one at section boundaries.
