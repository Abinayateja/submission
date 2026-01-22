import os, json

OCR_DIR = "../ocr_outputs"
dealer_lines = []

for f in os.listdir(OCR_DIR):
    with open(os.path.join(OCR_DIR, f), encoding="utf-8") as jf:
        words = json.load(jf)

    lines = {}
    for w in words:
        y = int(w["bbox"][0][1] // 40)
        lines.setdefault(y, []).append(w["text"])

    for y, texts in lines.items():
        line = " ".join(texts)
        if any(k in line.lower() for k in ["dealer", "m/s", "authorized", "tractor"]):
            dealer_lines.append(line)

with open("../pseudo_labels/dealer_candidates.json", "w") as out:
    json.dump(dealer_lines[:200], out, indent=2)

print("Dealer-like lines collected:", len(dealer_lines))
