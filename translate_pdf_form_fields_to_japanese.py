#!/usr/bin/env python3
"""
Translate ONLY filled text form fields in a PDF into Japanese.

Usage:
  python translate_pdf_form_fields_to_japanese.py input.pdf output_ja.pdf
"""

import argparse
import sys
from typing import Dict, Any

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject, BooleanObject
from deep_translator import GoogleTranslator


def normalize_field_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def is_probably_japanese(text: str) -> bool:
    for ch in text:
        code = ord(ch)
        if (
            0x3040 <= code <= 0x309F
            or 0x30A0 <= code <= 0x30FF
            or 0x4E00 <= code <= 0x9FFF
            or 0xFF66 <= code <= 0xFF9D
        ):
            return True
    return False


def translate_text_to_japanese(text: str, translator: GoogleTranslator) -> str:
    text = text.strip()
    if not text:
        return text
    if is_probably_japanese(text):
        return text
    return translator.translate(text)


def get_all_form_fields(reader: PdfReader) -> Dict[str, Any]:
    fields = reader.get_fields()
    return fields or {}


def main():
    parser = argparse.ArgumentParser(
        description="Translate filled PDF form text fields to Japanese."
    )
    parser.add_argument("input_pdf", help="Path to input PDF")
    parser.add_argument("output_pdf", help="Path to output translated PDF")
    parser.add_argument("--source-lang", default="auto")
    parser.add_argument("--target-lang", default="ja")
    parser.add_argument("--log-file", default="translation_log.txt")
    args = parser.parse_args()

    try:
        reader = PdfReader(args.input_pdf)
    except Exception as e:
        print(f"[ERROR] Failed to read input PDF: {e}")
        sys.exit(1)

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    if "/AcroForm" in reader.trailer["/Root"]:
        writer._root_object.update(
            {NameObject("/AcroForm"): reader.trailer["/Root"]["/AcroForm"]}
        )
        try:
            writer._root_object["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)}
            )
        except Exception:
            pass

    fields = get_all_form_fields(reader)
    if not fields:
        print("[INFO] No AcroForm fields found. Output will be identical to input.")
        with open(args.output_pdf, "wb") as f_out:
            writer.write(f_out)
        sys.exit(0)

    translator = GoogleTranslator(source=args.source_lang, target=args.target_lang)

    updates = {}
    log_lines = []

    for field_name, field_obj in fields.items():
        field_type = field_obj.get("/FT")
        raw_value = field_obj.get("/V")
        value = normalize_field_value(raw_value)

        if field_type != "/Tx":
            continue
        if not value:
            continue

        try:
            translated = translate_text_to_japanese(value, translator)
        except Exception as e:
            print(f"[WARN] Translation failed for field '{field_name}': {e}")
            translated = value

        updates[field_name] = TextStringObject(translated)
        log_lines.append(f"FIELD: {field_name}\nORIG : {value}\nTRANS: {translated}\n")

    for page in writer.pages:
        writer.update_page_form_field_values(page, updates)

    with open(args.output_pdf, "wb") as f_out:
        writer.write(f_out)

    with open(args.log_file, "w", encoding="utf-8") as logf:
        logf.write("\n".join(log_lines) if log_lines else "No translated fields.\n")

    print("[DONE]")
    print(f"Input PDF   : {args.input_pdf}")
    print(f"Output PDF  : {args.output_pdf}")
    print(f"Log file    : {args.log_file}")


if __name__ == "__main__":
    main()
