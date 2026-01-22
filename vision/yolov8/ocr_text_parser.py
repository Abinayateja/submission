import json
import os

def extract_text_from_ocr_folder(ocr_dir):
    """
    Reads all OCR JSON files and returns combined text
    """
    full_text = ""

    for file in os.listdir(ocr_dir):
        if not file.endswith(".json"):
            continue

        path = os.path.join(ocr_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for block in data:
                if "text" in block:
                    full_text += " " + block["text"]

    return full_text.lower()
