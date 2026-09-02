#!/usr/bin/env python3
"""
Shared helpers for natural language translation used across the CLI
scripts and the GUI.

This module centralizes:
- OCR (PNG -> text)
- Translation (any source language -> any target language) via
  deep-translator's GoogleTranslator backend
- A curated list of common target languages for use in UI pickers
- Script-detection helpers so text already written in the target
  language's script is not re-translated
"""

from pathlib import Path

from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator

# A curated set of common target languages (display name -> language code).
# Kept as a static fallback so the app still works if the underlying
# translation backend's dynamic language list is unavailable.
COMMON_LANGUAGES = {
    "Japanese": "ja",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Turkish": "tr",
    "Polish": "pl",
    "Greek": "el",
    "Hebrew": "iw",
    "Swedish": "sv",
    "Ukrainian": "uk",
}

DEFAULT_TARGET_LANGUAGE_NAME = "Japanese"
DEFAULT_TARGET_LANGUAGE_CODE = "ja"

# Unicode script ranges used to detect when text is already written in a
# given target language's script, so it does not need (and should not be)
# re-translated.
_SCRIPT_RANGES = {
    "ja": ((0x3040, 0x309F), (0x30A0, 0x30FF), (0x4E00, 0x9FFF), (0xFF66, 0xFF9D)),
    "zh-cn": ((0x4E00, 0x9FFF),),
    "zh-tw": ((0x4E00, 0x9FFF),),
    "zh": ((0x4E00, 0x9FFF),),
    "ko": ((0xAC00, 0xD7A3), (0x1100, 0x11FF)),
    "ru": ((0x0400, 0x04FF),),
    "uk": ((0x0400, 0x04FF),),
    "ar": ((0x0600, 0x06FF),),
    "iw": ((0x0590, 0x05FF),),
    "he": ((0x0590, 0x05FF),),
    "th": ((0x0E00, 0x0E7F),),
    "el": ((0x0370, 0x03FF),),
    "hi": ((0x0900, 0x097F),),
}


def get_supported_languages() -> dict:
    """Return a mapping of display name -> language code.

    Tries to use deep-translator's dynamic supported-language list (title
    cased for display) and falls back to the curated COMMON_LANGUAGES set
    if that lookup fails (e.g. no network access).
    """
    try:
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
        return {name.title(): code for name, code in sorted(langs.items())}
    except Exception:
        return dict(COMMON_LANGUAGES)


def is_already_target_script(text: str, target_lang: str) -> bool:
    """Return True if text appears to already be written in the script
    typically used by target_lang, meaning translation can be skipped.
    """
    ranges = _SCRIPT_RANGES.get((target_lang or "").lower())
    if not ranges:
        return False
    for ch in text:
        code = ord(ch)
        if any(lo <= code <= hi for lo, hi in ranges):
            return True
    return False


def ocr_image(image_path: Path, ocr_lang: str = "eng") -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=ocr_lang)
    return text.strip()


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "ja") -> str:
    """Translate text into target_lang, skipping text already in that
    language's script (when known) and blank input.
    """
    if not text or not text.strip():
        return ""
    if is_already_target_script(text, target_lang):
        return text
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)
