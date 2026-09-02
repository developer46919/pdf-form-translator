# PDF Form + PNG OCR + DOCX Translator (Any Language)

This repository provides Python scripts to:

1. Translate **filled PDF form text fields only** (not full PDF page content) to any target language.
2. OCR text from PNG images and translate that text to any target language.
3. Batch-process multiple PNG files.
4. Translate DOCX text content (paragraphs + tables) to any target language.
5. Use a GUI (Explorer/Finder file pickers + a target-language dropdown) for no-command-line runs.

All scripts default to Japanese (`ja`) for backward compatibility, but every script accepts a
`--target-lang` argument (e.g. `es`, `fr`, `de`, `zh-CN`, `ko`, ...) to translate into any language
supported by the underlying translation backend.

## Requirements

- Python 3.10+
- Tesseract OCR installed on your OS (required for PNG OCR)

### Install Python dependencies

```bash
pip install -r requirements.txt
```

## Setup Tesseract

### Windows
1. Install Tesseract (e.g., UB Mannheim build).
2. Add Tesseract install path to PATH, e.g.:
   `C:\Program Files\Tesseract-OCR`

### macOS
```bash
brew install tesseract
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

## Scripts

### 1) PDF form fields -> any language

```bash
python translate_pdf_form_fields_to_japanese.py input.pdf output_ja.pdf --target-lang ja
```

### 2) Single PNG OCR + translate

```bash
python translate_png_ocr_to_japanese.py input.png --target-lang es --print-ocr --print-translation
```

### 3) Batch PNG OCR + translate

```bash
python batch_translate_pngs.py ./input_images ./output --glob "*.png" --target-lang fr
```

Outputs per image:
- `<name>.ocr.txt`
- `<name>.<target-lang>.txt`

### 4) DOCX translate -> any language

```bash
python translate_docx_to_japanese.py input.docx output_ja.docx --target-lang de
```

### 5) GUI mode (file explorer dialogs)

```bash
python run_gui.py
```

Pick a **Translate to:** target language from the dropdown, then choose:
- **Single PNG (pick file)**
- **Batch PNGs (pick folders)**
- **Translate DOCX (pick file)**
- **Translate PDF form fields (pick file)**

### 6) Windows double-click launcher

Double-click:

- `run_gui.bat`

## Notes

- Translation uses `deep-translator` (Google Translate backend). This is the free, unofficial
  Google Translate web endpoint — it requires **no API key**. It is not the official paid Google
  Cloud Translation API.
- PDF script only updates AcroForm text field values.
- For scanned PDFs (image-only), use OCR flow instead.
- Text already written in the selected target language's script (e.g. Japanese, Chinese, Korean,
  Russian, Arabic) is left unchanged rather than re-translated.
