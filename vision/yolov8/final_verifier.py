from ocr_text_parser import extract_text_from_ocr_folder
from consensus_detector import consensus_decision

def verify_invoice(yolo_preds, ocr_dir, image_h):
    ocr_text = extract_text_from_ocr_folder(ocr_dir)
    decision = consensus_decision(yolo_preds, ocr_text, image_h)

    def confidence(evidence_count):
        if evidence_count >= 3:
            return "HIGH"
        elif evidence_count == 2:
            return "MEDIUM"
        else:
            return "LOW"

    sig_evidence = []
    stamp_evidence = []

    if decision["signature"]["present"]:
        sig_evidence = ["vision", "ocr", "position"]

    if decision["stamp"]["present"]:
        stamp_evidence = ["vision", "position"]

    final_verdict = "INVALID_DOCUMENT"
    if decision["signature"]["present"] and decision["stamp"]["present"]:
        final_verdict = "VALID_DOCUMENT"
    elif decision["signature"]["present"] or decision["stamp"]["present"]:
        final_verdict = "PARTIALLY_VALID"

    return {
        "signature": {
            "present": decision["signature"]["present"],
            "confidence": confidence(len(sig_evidence)),
            "evidence": sig_evidence
        },
        "stamp": {
            "present": decision["stamp"]["present"],
            "confidence": confidence(len(stamp_evidence)),
            "evidence": stamp_evidence
        },
        "final_verdict": final_verdict
    }
