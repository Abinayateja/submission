import os, json
from collections import Counter

OCR_DIR = "../ocr_outputs"
costs = []

for f in os.listdir(OCR_DIR):
    with open(os.path.join(OCR_DIR, f), encoding="utf-8") as jf:
        words = json.load(jf)

    nums = [int(w["text"]) for w in words if w["text"].isdigit() and len(w["text"]) >= 5]
    if nums:
        costs.append(max(nums))

with open("../pseudo_labels/asset_cost.json", "w") as out:
    json.dump(costs, out, indent=2)

print("Pseudo asset costs collected:", len(costs))
print("Most common values:", Counter(costs).most_common(5))
