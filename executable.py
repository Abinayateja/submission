import sys, json, time, cv2
from pdf2image import convert_from_path
import numpy as np
from ultralytics import YOLO
from utils.consensus_detector import consensus_decision
from extraction.dealer_name import extract_dealer
from extraction.model_name import extract_model
from extraction.horsepower import extract_hp
from extraction.asset_cost import extract_cost
from ocr.paddle_ocr import run_ocr

YOLO_MODEL_PATH = "yolov8n.pt"
yolo_model = YOLO(YOLO_MODEL_PATH)



MASTER_DEALERS = []  # load from CSV later
MODEL_MASTER = []    # load from CSV later

start = time.time()

pdf_path = sys.argv[1]
images = convert_from_path(
    pdf_path,
    poppler_path=r"C:\poppler-25.12.0\Library\bin"
)


image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
h, w, _ = image.shape

# ---------- OCR ----------
words = run_ocr(image)
ocr_text = " ".join(w["text"] for w in words)

# ---------- YOLO ----------
results = yolo_model(image)[0]

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

# ---------- CONSENSUS (THIS MUST COME AFTER yolo_preds) ----------
decision = consensus_decision(
    yolo_preds=yolo_preds,
    ocr_text=ocr_text,
    image_h=h
)

dealer, d_conf = extract_dealer(words, MASTER_DEALERS, h)
model, m_conf = extract_model(words, MODEL_MASTER)
hp, hp_conf = extract_hp(words)
cost, c_conf = extract_cost(words)

confidence = round((d_conf + m_conf + hp_conf + c_conf) / 4, 2)

output = {
    "doc_id": pdf_path,
    "fields": {
        "dealer_name": dealer,
        "model_name": model,
        "horse_power": hp,
        "asset_cost": cost,
        "signature": decision["signature"],
        "stamp": decision["stamp"]
    },
    "confidence": confidence,
    "processing_time_sec": round(time.time() - start, 2),
    "cost_estimate_usd": round((time.time() - start) * 0.0005, 4)
}


print(json.dumps(output, indent=2))
