def parse_yolo_results(results):
    preds = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            class_name = "signature" if cls_id == 0 else "stamp"

            x1, y1, x2, y2 = map(float, box.xyxy[0])

            preds.append({
                "class": class_name,
                "conf": conf,
                "bbox": [x1, y1, x2, y2]
            })

    return preds
