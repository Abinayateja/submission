import os, json, re
from collections import Counter

OCR_DIR = "../ocr_outputs"
hp_values = []

for f in os.listdir(OCR_DIR):
    with open(os.path.join(OCR_DIR, f), encoding="utf-8") as jf:
        words = json.load(jf)

    for w in words:
        match = re.search(r"(\d{2,3})\s*HP", w["text"].upper())
        if match:
            hp_values.append(int(match.group(1)))

with open("../pseudo_labels/horsepower.json", "w") as out:
    json.dump(hp_values, out, indent=2)

print("HP samples:", len(hp_values))
print("Most common HPs:", Counter(hp_values).most_common(5))
