import os
import cv2
import numpy as np
from collections import Counter

IMG_DIR = "../raw"

resolutions = []
aspect_ratios = []
grayscale_count = 0

for img_name in os.listdir(IMG_DIR):
    path = os.path.join(IMG_DIR, img_name)
    img = cv2.imread(path)

    if img is None:
        continue

    h, w, c = img.shape
    resolutions.append((h, w))
    aspect_ratios.append(round(w / h, 2))

    if np.mean(img[:,:,0] - img[:,:,1]) < 1:
        grayscale_count += 1

print("📄 Total documents:", len(resolutions))
print("📐 Avg height:", sum(h for h, _ in resolutions)//len(resolutions))
print("📐 Avg width :", sum(w for _, w in resolutions)//len(resolutions))
print("🖼️ Grayscale scans:", grayscale_count)

ratio_dist = Counter(aspect_ratios).most_common(5)
print("📊 Common aspect ratios:", ratio_dist)
