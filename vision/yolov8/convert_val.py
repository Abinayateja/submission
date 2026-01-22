import os
from labelme_to_yolo import convert

RAW_DIR = "../../data/annotations"
VAL_IMG_DIR = "val/images"
VAL_LBL_DIR = "val/labels"

os.makedirs(VAL_LBL_DIR, exist_ok=True)

converted = 0

for img_name in os.listdir(VAL_IMG_DIR):
    if not img_name.endswith(".png"):
        continue

    img_path = os.path.join(VAL_IMG_DIR, img_name)
    json_name = img_name.replace(".png", ".json")
    json_path = os.path.join(RAW_DIR, json_name)

    if not os.path.exists(json_path):
        print(f"Missing annotation for {img_name}")
        continue

    out_txt = os.path.join(
        VAL_LBL_DIR,
        img_name.replace(".png", ".txt")
    )

    convert(json_path, img_path, out_txt)
    converted += 1

print(f"VAL Converted: {converted}")
