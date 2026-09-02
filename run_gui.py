#!/usr/bin/env python3
"""
GUI runner to select a file/folder via Explorer/Finder dialogs,
then run OCR + Japanese translation.
"""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

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


def main():
    root = tk.Tk()
    root.title("PNG OCR -> Japanese Translator")
    root.geometry("420x200")

    frm = tk.Frame(root, padx=20, pady=20)
    frm.pack(fill="both", expand=True)

    tk.Label(frm, text="Choose how you want to run:", font=("Segoe UI", 11, "bold")).pack(pady=(0, 12))

    tk.Button(frm, text="Single PNG (pick file)", width=30, command=single_file_mode).pack(pady=6)
    tk.Button(frm, text="Batch PNGs (pick folders)", width=30, command=batch_mode).pack(pady=6)
    tk.Button(frm, text="Exit", width=30, command=root.destroy).pack(pady=6)

    root.mainloop()


if __name__ == "__main__":
    main()
