#!/usr/bin/env python3
"""
GUI runner to select files/folders via Explorer/Finder dialogs,
then run OCR/translation tasks.
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from docx import Document


def ocr_image(image_path: Path, ocr_lang: str = "eng") -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=ocr_lang)
    return text.strip()


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


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "ja") -> str:
    if not text.strip():
        return ""
    if is_probably_japanese(text):
        return text
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)


def single_file_mode():
    file_path = filedialog.askopenfilename(
        title="Select a PNG image",
        filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")],
    )
    if not file_path:
        return

    img = Path(file_path)
    out_dir = img.parent / "translated_output"
    out_dir.mkdir(exist_ok=True)

    try:
        ocr_text = ocr_image(img)
        ja_text = translate_text(ocr_text)

        ocr_out = out_dir / f"{img.stem}.ocr.txt"
        ja_out = out_dir / f"{img.stem}.ja.txt"
        ocr_out.write_text(ocr_text, encoding="utf-8")
        ja_out.write_text(ja_text, encoding="utf-8")

        messagebox.showinfo(
            "Done",
            f"Processed: {img.name}\n\nSaved:\n{ocr_out}\n{ja_out}",
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))


def batch_mode():
    in_dir = filedialog.askdirectory(title="Select INPUT folder (PNG files)")
    if not in_dir:
        return

    out_dir = filedialog.askdirectory(title="Select OUTPUT folder")
    if not out_dir:
        return

    in_path = Path(in_dir)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    files = sorted(in_path.glob("*.png"))
    if not files:
        messagebox.showwarning("No files", "No PNG files found in selected input folder.")
        return

    translator = GoogleTranslator(source="auto", target="ja")
    ok = 0
    fail = 0

    for img in files:
        try:
            ocr_text = ocr_image(img)
            ja_text = translator.translate(ocr_text) if ocr_text else ""

            (out_path / f"{img.stem}.ocr.txt").write_text(ocr_text, encoding="utf-8")
            (out_path / f"{img.stem}.ja.txt").write_text(ja_text, encoding="utf-8")
            ok += 1
        except Exception:
            fail += 1

    messagebox.showinfo("Batch complete", f"Success: {ok}\nFailed: {fail}\nOutput: {out_path}")


def docx_mode():
    file_path = filedialog.askopenfilename(
        title="Select a DOCX file",
        filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
    )
    if not file_path:
        return

    src = Path(file_path)
    out = src.with_name(f"{src.stem}.ja.docx")

    try:
        doc = Document(str(src))
        translator = GoogleTranslator(source="auto", target="ja")

        for para in doc.paragraphs:
            txt = para.text
            if txt and txt.strip() and not is_probably_japanese(txt):
                para.text = translator.translate(txt)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    txt = cell.text
                    if txt and txt.strip() and not is_probably_japanese(txt):
                        cell.text = translator.translate(txt)

        doc.save(str(out))
        messagebox.showinfo("Done", f"Translated DOCX saved:\n{out}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    root.title("Translator Utility")
    root.geometry("460x270")

    frm = tk.Frame(root, padx=20, pady=20)
    frm.pack(fill="both", expand=True)

    tk.Label(frm, text="Choose how you want to run:", font=("Segoe UI", 11, "bold")).pack(pady=(0, 12))

    tk.Button(frm, text="Single PNG (pick file)", width=34, command=single_file_mode).pack(pady=6)
    tk.Button(frm, text="Batch PNGs (pick folders)", width=34, command=batch_mode).pack(pady=6)
    tk.Button(frm, text="Translate DOCX (pick file)", width=34, command=docx_mode).pack(pady=6)
    tk.Button(frm, text="Exit", width=34, command=root.destroy).pack(pady=6)

    root.mainloop()


if __name__ == "__main__":
    main()
