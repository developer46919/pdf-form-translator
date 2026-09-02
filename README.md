# PDF Form + PNG OCR + DOCX Translator (Japanese)

This repository provides Python scripts to:

1. Translate **filled PDF form text fields only** (not full PDF page content) to Japanese.
2. OCR text from PNG images and translate that text to Japanese.
3. Batch-process multiple PNG files.
4. Translate DOCX text content (paragraphs + tables) to Japanese.
5. Use a GUI file picker (Explorer/Finder) for no-command-line runs.

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

### 1) PDF form fields -> Japanese

```bash
python translate_pdf_form_fields_to_japanese.py input.pdf output_ja.pdf
```

### 2) Single PNG OCR + translate

```bash
python translate_png_ocr_to_japanese.py input.png --print-ocr --print-translation
```

### 3) Batch PNG OCR + translate

```bash
python batch_translate_pngs.py ./input_images ./output --glob "*.png"
```

Outputs per image:
- `<name>.ocr.txt`
- `<name>.ja.txt`

### 4) DOCX translate -> Japanese

```bash
python translate_docx_to_japanese.py input.docx output_ja.docx
```

### 5) GUI mode (file explorer dialogs)

```bash
python run_gui.py
```

Then choose:
- **Single PNG (pick file)**
- **Batch PNGs (pick folders)**
- **Translate DOCX (pick file)**

### 6) Windows double-click launcher

Double-click:

- `run_gui.bat`

## Notes

- Translation uses `deep-translator` (Google Translate backend).
- PDF script only updates AcroForm text field values.
- For scanned PDFs (image-only), use OCR flow instead.
