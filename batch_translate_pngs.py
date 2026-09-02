#!/usr/bin/env python3
"""
Batch OCR + translation for PNG files, to any target language.

Usage:
  python batch_translate_pngs.py ./input_images ./output --glob "*.png"
"""

import argparse
from pathlib import Path

from deep_translator import GoogleTranslator

from translator_core import ocr_image, is_already_target_script


def main():
    parser = argparse.ArgumentParser(description="Batch OCR PNG files and translate to any language")
    parser.add_argument("input_dir", help="Directory containing PNG files")
    parser.add_argument("output_dir", help="Directory for output text files")
    parser.add_argument("--glob", default="*.png", help="Glob pattern (default: *.png)")
    parser.add_argument("--ocr-lang", default="eng", help="Tesseract OCR language")
    parser.add_argument("--source-lang", default="auto")
    parser.add_argument("--target-lang", default="ja", help="Target language code, e.g. ja, es, fr, de")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Invalid input directory: {input_dir}")

    files = sorted(input_dir.glob(args.glob))
    if not files:
        print("No files found.")
        return

    translator = GoogleTranslator(source=args.source_lang, target=args.target_lang)

    for img_path in files:
        try:
            ocr_text = ocr_image(img_path, ocr_lang=args.ocr_lang)
            if ocr_text and not is_already_target_script(ocr_text, args.target_lang):
                translated = translator.translate(ocr_text)
            else:
                translated = ocr_text

            ocr_out = output_dir / f"{img_path.stem}.ocr.txt"
            translated_out = output_dir / f"{img_path.stem}.{args.target_lang}.txt"

            ocr_out.write_text(ocr_text, encoding="utf-8")
            translated_out.write_text(translated, encoding="utf-8")

            print(f"[OK] {img_path.name} -> {ocr_out.name}, {translated_out.name}")
        except Exception as e:
            print(f"[ERR] {img_path.name}: {e}")


if __name__ == "__main__":
    main()
