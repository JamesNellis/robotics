#!/usr/bin/env python3

import cv2
import numpy as np
import os

INPUT_DIR = "input"
OUTPUT_DIR = "detect"


# how different a pixel must be (0-255) to count as "changed"
# lower = more sensitive, but picks up noise. higher = misses subtle motion
THRESHOLD = 25

# minimum blob size in pixels to draw a box around
# filters out tiny specks that pass the threshold but aren't real objects
MIN_AREA = 500

# gaussian blur kernel size (must be odd). smooths frame before comparison
# aims to get rid of single-pixel sensor noise, compression artifacts, etc.
BLUR_SIZE = 5

# how many times to dilate (expand) white regions in the motion mask
# fills gaps in detected objects, merges nearby blobs into one
# a car might show as hood + roof + trunk separately - dilation connects them
# too high and different objects merge into one
DILATE_ITER = 3


images = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
os.makedirs(OUTPUT_DIR, exist_ok=True)

prev_gray = None

for i, filename in enumerate(images):
    frame = cv2.imread(os.path.join(INPUT_DIR, filename))

    # convert to grayscale - simpler comparison, don't care about color shifts
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (BLUR_SIZE, BLUR_SIZE), 0)

    # need two frames to compare
    if prev_gray is None:
        prev_gray = gray
        continue

    # absolute difference between frames - bright = changed, dark = same
    diff = cv2.absdiff(prev_gray, gray)

    # binary threshold - pixel is either "moved" (white) or "didn't" (black)
    _, thresh = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)

    # dilate expands white regions, connecting nearby blobs
    # erode shrinks them back, but now they're connected
    # net effect: fills holes, bridges gaps, smooths edges
    thresh = cv2.dilate(thresh, None, iterations=DILATE_ITER)
    thresh = cv2.erode(thresh, None, iterations=1)

    # find outlines of white regions
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # draw boxes around anything big enough
    for contour in contours:
        if cv2.contourArea(contour) < MIN_AREA:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    prev_gray = gray

    out_name = f"det{i:06d}.jpg"
    cv2.imwrite(os.path.join(OUTPUT_DIR, out_name), frame)
    print(f"saved {out_name}")

print("done")
