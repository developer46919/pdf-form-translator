#!/usr/bin/env python3
"""
OCR a PNG image and translate extracted text to Japanese.

Usage:
  python translate_png_ocr_to_japanese.py input.png --print-ocr --print-translation
"""

import argparse
from pathlib import Path

from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator


def ocr_image(image_path: Path, ocr_lang: str = "eng") -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=ocr_lang)
    return text.strip()


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "ja") -> str:
    if not text.strip():
        return ""
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)


def main():
    parser = argparse.ArgumentParser(description="OCR PNG and translate text to Japanese")
    parser.add_argument("input_png", help="Path to PNG image")
    parser.add_argument("--ocr-lang", default="eng", help="Tesseract OCR language, e.g. eng")
    parser.add_argument("--source-lang", default="auto")
    parser.add_argument("--target-lang", default="ja")
    parser.add_argument("--save-ocr", default=None, help="Optional path to save OCR text")
    parser.add_argument("--save-translation", default=None, help="Optional path to save translated text")
    parser.add_argument("--print-ocr", action="store_true", help="Print OCR text")
    parser.add_argument("--print-translation", action="store_true", help="Print translated text")
    args = parser.parse_args()

    input_path = Path(args.input_png)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    ocr_text = ocr_image(input_path, ocr_lang=args.ocr_lang)
    translated = translate_text(ocr_text, source_lang=args.source_lang, target_lang=args.target_lang)

    if args.print_ocr:
        print("=== OCR TEXT ===")
        print(ocr_text)

    if args.print_translation:
        print("=== TRANSLATED (JA) ===")
        print(translated)

    if args.save_ocr:
        Path(args.save_ocr).write_text(ocr_text, encoding="utf-8")

    if args.save_translation:
        Path(args.save_translation).write_text(translated, encoding="utf-8")

    if not any([args.print_ocr, args.print_translation, args.save_ocr, args.save_translation]):
        print(translated)


if __name__ == "__main__":
    main()
