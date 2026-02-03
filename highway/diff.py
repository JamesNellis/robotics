#!/usr/bin/env python3
"""Compare consecutive images and output pixels that changed enough."""

from PIL import Image
import numpy as np
import os

INPUT_DIR = "input"
OUTPUT_DIR = "output"
THRESHOLD = 30

images = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
os.makedirs(OUTPUT_DIR, exist_ok=True)

for i in range(len(images) - 1):
    img1 = np.array(Image.open(os.path.join(INPUT_DIR, images[i])).convert("RGB"))
    img2 = np.array(Image.open(os.path.join(INPUT_DIR, images[i + 1])).convert("RGB"))

    diff = np.sum(np.abs(img1.astype(int) - img2.astype(int)), axis=2)
    out = np.where(diff >= THRESHOLD, 255, 0).astype(np.uint8)

    out_name = f"dif{i+1:06d}.jpg"
    Image.fromarray(out).save(os.path.join(OUTPUT_DIR, out_name))
    print(f"saved {out_name}")

print("done")
