def consensus_decision(yolo_preds, ocr_text, image_h):
    result = {
        "signature": {"present": False, "bbox": None},
        "stamp": {"present": False, "bbox": None}
    }

    ocr_text = ocr_text.lower()

    # ================= SIGNATURE =================
    sig_votes = 0
    sig_bbox = None

    for p in yolo_preds:
        if p["class"] == "signature" and p["conf"] >= 0.15:
            sig_votes += 1
            sig_bbox = p["bbox"]

    # OCR keyword signal
    if any(k in ocr_text for k in ["signature", "authorized sign", "signatory"]):
        sig_votes += 1

    # Layout signal (bottom half)
    if sig_bbox and sig_bbox[1] > 0.6 * image_h:
        sig_votes += 1

    # FINAL DECISION
    if sig_votes >= 2 or ("signature" in ocr_text):
        result["signature"]["present"] = True
        result["signature"]["bbox"] = sig_bbox

    # ================= STAMP =================
    stamp_votes = 0
    stamp_bbox = None

    for p in yolo_preds:
        if p["class"] == "stamp" and p["conf"] >= 0.15:
            stamp_votes += 1
            stamp_bbox = p["bbox"]

    # OCR keyword signal
    if any(k in ocr_text for k in ["stamp", "seal", "authorized"]):
        stamp_votes += 1

    # Layout signal (lower half)
    if stamp_bbox and stamp_bbox[1] > 0.55 * image_h:
        stamp_votes += 1

    # FINAL DECISION
    if stamp_votes >= 2 or any(k in ocr_text for k in ["stamp", "seal"]):
        result["stamp"]["present"] = True
        result["stamp"]["bbox"] = stamp_bbox

    return result
