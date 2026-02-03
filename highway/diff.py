#!/usr/bin/env python3
from PIL import Image
import numpy as np
import os

INPUT_DIR = "input"
OUTPUT_DIR = "output"
THRESHOLD = 30

# sort all files based on their naming
images = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
os.makedirs(OUTPUT_DIR, exist_ok=True)

# for each image:
for i in range(len(images) - 1):
    # turn the image and the next one into color arrays
    img1 = np.array(Image.open(os.path.join(INPUT_DIR, images[i])).convert("RGB"))
    img2 = np.array(Image.open(os.path.join(INPUT_DIR, images[i + 1])).convert("RGB"))

    # calculate the difference in RGB values
    diff = np.sum(np.abs(img1.astype(int) - img2.astype(int)), axis=2)
    # make a new array, the size of the old images - 
    # if the sum of difference > threshold: white pixel, else: black pixel
    out = np.where(diff >= THRESHOLD, 255, 0).astype(np.uint8)

    # save image
    out_name = f"dif{i+1:06d}.jpg"
    Image.fromarray(out).save(os.path.join(OUTPUT_DIR, out_name))
    print(f"saved {out_name}")

print("done")
