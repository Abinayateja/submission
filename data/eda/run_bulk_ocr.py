import os
import json
import cv2
from paddleocr import PaddleOCR

RAW_DIR = "../raw"
OUT_DIR = "../ocr_outputs"

os.makedirs(OUT_DIR, exist_ok=True)

ocr = PaddleOCR(use_angle_cls=True, lang="en")

for img_name in os.listdir(RAW_DIR):
    img_path = os.path.join(RAW_DIR, img_name)
    out_path = os.path.join(OUT_DIR, img_name.replace(".jpg", ".json"))

    if os.path.exists(out_path):
        continue  # skip already processed

    image = cv2.imread(img_path)
    if image is None:
        continue

    try:
        result = ocr.ocr(image, cls=True)
    except Exception as e:
        print(f"❌ OCR failed for {img_name}: {e}")
        continue

    words = []
    if result and result[0]:
        for line in result[0]:
            bbox, (text, conf) = line
            words.append({
                "text": text,
                "bbox": bbox,
                "confidence": round(conf, 3)
            })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    print(f"OCR done: {img_name}")
