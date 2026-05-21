# Fraktur German OCR Post-Processing Patterns

Common artifact cleanup for German texts scanned from Fraktur type (pre-1945), especially Google Books PDFs and UCAL page-level OCR.

## Extraction

```python
import fitz
doc = fitz.open('book.pdf')
text = doc[i].get_text()  # page i
```

## Cleaning Pipeline (4 passes)

### Pass 1: Hyphenation at line breaks
```python
text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # "neu-\nzeitlichen" → "neuzeitlichen"
text = re.sub(r'-\n', '', text)                 # leftover bare hyphens
```

### Pass 2: Missing spaces between words
Fraktur OCR commonly drops spaces, especially:
- After lowercase before uppercase: `dieGeschichte` → `die Geschichte`
- After period before uppercase: `Napoleons.Die` → `Napoleons. Die`

```python
text = re.sub(r'([a-zß])\.([A-ZÄÖÜ])', r'\1. \2', text)
text = re.sub(r'([a-zß])([A-ZÄÖÜ])', r'\1 \2', text)
```

Also fix: ` ,` → `,`, ` ;` → `;`, ` :` → `:`, normalize `>>` / `<<` to `»` / `«`.

### Pass 3: Common word-fragment dictionary (~100 entries)
Words split across lines without hyphens produce fragments like `Ge sichte` → `Geschichte`. The full dictionary is at the end of this file. Apply with `text.replace(wrong, right)` in a loop.

### Pass 4: Capitalized split-word detection
Single uppercase letter floating before a lowercase word: `N poleons` → `Napoleons` (covers uncommon or short-prefix cases missed by Pass 3).

```python
text = re.sub(r'\b([A-ZÄÖÜ])\s+([a-zäöü]{3,})\b', lambda m: m.group(1) + m.group(2), text)
```

## Full Common-Fix Dictionary (Pass 3)

```python
FIXES = {
    'Ge sichte': 'Geschichte', 'Ge schichte': 'Geschichte',
    'Ge sichtspunkte': 'Gesichtspunkte', 'Ge schichts': 'Geschichts',
    'Ge schichtlichen': 'Geschichtlichen', 'We sens': 'Wesens',
    'We sensdarstellung': 'Wesensdarstellung', 'Na poleons': 'Napoleons',
    'Be deutung': 'Bedeutung', 'Be ziehung': 'Beziehung',
    'Be ziehungen': 'Beziehungen', 'Er kenntnis': 'Erkenntnis',
    'Er kenntnisse': 'Erkenntnisse', 'Er scheinung': 'Erscheinung',
    'Er eignis': 'Ereignis', 'An deutung': 'Andeutung',
    'An schauung': 'Anschauung', 'Aus druck': 'Ausdruck',
    'Aus serung': 'Äusserung', 'Auf nahme': 'Aufnahme',
    'Auf fassung': 'Auffassung', 'Auf zeichnung': 'Aufzeichnung',
    'Dar stellung': 'Darstellung', 'Ent wicklung': 'Entwicklung',
    'Ge gebenheit': 'Gegebenheit', 'Ge genstand': 'Gegenstand',
    'Ge genwart': 'Gegenwart', 'Ge gensatz': 'Gegensatz',
    'Ge halt': 'Gehalt', 'Ge istigkeit': 'Geistigkeit',
    'In neres': 'Inneres', 'In nerste': 'Innerste',
    'Le benslauf': 'Lebenslauf', 'Le bensstoff': 'Lebensstoff',
    'Per son': 'Person', 'Um stände': 'Umstände',
    'Un tersuchung': 'Untersuchung', 'Un terricht': 'Unterricht',
    'Ver hältnis': 'Verhältnis', 'Vor stellung': 'Vorstellung',
    'Vor aussetzung': 'Voraussetzung', 'Zu stand': 'Zustand',
    'Zu sammenhang': 'Zusammenhang', 'tatsäch lichem': 'tatsächlichem',
    'sinn fällige': 'sinnfällige', 'Jahrhun derte': 'Jahrhunderte',
    'Andeu tung': 'Andeutung', 'Ge biete': 'Gebiete',
    'Bes tätigung': 'Betätigung', 'Be griff': 'Begriff',
    'Über einstimmung': 'Übereinstimmung', 'Über lieferung': 'Überlieferung',
    'umgestaltungen': 'Umgestaltungen', 'Agɣetvños': 'ἀρχέτυπος',
}
```

Test by counting `[a-zß][A-ZÄÖÜ]` in cleaned output — should approach zero.
