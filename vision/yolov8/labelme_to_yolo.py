import json
import os
from PIL import Image

LABEL_MAP = {
    "signature": 0,
    "stamp": 1
}

def convert(json_path, image_path, output_txt):
    with open(json_path, "r") as f:
        data = json.load(f)

    img = Image.open(image_path)
    img_w, img_h = img.size

    yolo_lines = []

    for shape in data["shapes"]:
        label = shape["label"]
        if label not in LABEL_MAP:
            continue

        points = shape["points"]
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]

        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)

        x_center = ((x_min + x_max) / 2) / img_w
        y_center = ((y_min + y_max) / 2) / img_h
        w = (x_max - x_min) / img_w
        h = (y_max - y_min) / img_h

        yolo_lines.append(
            f"{LABEL_MAP[label]} {x_center} {y_center} {w} {h}"
        )

    with open(output_txt, "w") as f:
        f.write("\n".join(yolo_lines))
