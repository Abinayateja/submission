import os
from labelme_to_yolo import convert

RAW_DIR = "../../data/annotations"
TRAIN_IMG_DIR = "train/images"
TRAIN_LBL_DIR = "train/labels"

os.makedirs(TRAIN_LBL_DIR, exist_ok=True)

converted = 0
skipped = 0

print("Using RAW_DIR:", os.path.abspath(RAW_DIR))

for img_name in os.listdir(TRAIN_IMG_DIR):
    if not img_name.endswith(".png"):
        continue

    img_path = os.path.join(TRAIN_IMG_DIR, img_name)
    json_path = os.path.join(RAW_DIR, img_name + ".json")

    print("Looking for:", json_path)

    if not os.path.exists(json_path):
        print("Skipping:", img_name)
        skipped += 1
        continue

    out_txt = os.path.join(
        TRAIN_LBL_DIR,
        img_name.replace(".png", ".txt")
    )

    convert(json_path, img_path, out_txt)
    converted += 1

print(f"Done. Converted: {converted}, Skipped: {skipped}")
