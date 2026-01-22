from ultralytics import YOLO
from consensus import consensus_decision


model = YOLO("runs/detect/signature_v2/weights/best.pt")

model.predict(
    source="train/images",
    conf=0.05,
    imgsz=640,
    save=True
)
img_h, img_w = image.shape[:2]

signature_result = consensus_decision(
    yolo_boxes=yolo_preds,
    ocr_words=ocr_words,
    img_w=img_w,
    img_h=img_h,
    target="signature"
)

stamp_result = consensus_decision(
    yolo_boxes=yolo_preds,
    ocr_words=ocr_words,
    img_w=img_w,
    img_h=img_h,
    target="stamp"
)

print("FINAL DECISION")
print("Signature:", signature_result)
print("Stamp:", stamp_result)
