import json
import os
from ultralytics import YOLO
from final_verifier import verify_invoice

# ---------------- PATHS ----------------
MODEL_PATH = "runs/detect/train3/weights/best.pt"
IMAGE_DIR = "val/images"
OCR_DIR = "../../data/ocr_outputs"
OUTPUT_DIR = "../../outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- LOAD MODEL ----------------
model = YOLO(MODEL_PATH)

# ---------------- PROCESS IMAGES ----------------
for img_name in os.listdir(IMAGE_DIR):
    if not img_name.endswith(".png"):
        continue

    invoice_id = img_name.replace(".png", "")
    img_path = os.path.join(IMAGE_DIR, img_name)

    # 1️⃣ YOLO prediction
    results = model(img_path)[0]

    yolo_preds = []
    for box in results.boxes:
        cls = results.names[int(box.cls)]
        conf = float(box.conf)
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        yolo_preds.append({
            "class": cls,
            "conf": conf,
            "bbox": [x1, y1, x2, y2]
        })

    image_h = results.orig_shape[0]

    # 2️⃣ Consensus decision
    final_result = verify_invoice(
        yolo_preds=yolo_preds,
        ocr_dir=OCR_DIR,
        image_h=image_h
    )

    final_result["invoice_id"] = invoice_id

    # 3️⃣ Save final JSON
    out_path = os.path.join(
        OUTPUT_DIR,
        invoice_id + ".json"
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)

    print(f"✅ Processed {invoice_id}")
