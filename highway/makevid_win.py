#!/usr/bin/env python3
"""Make a video from images in a folder (Windows version)."""

import subprocess
import sys
import os
import glob

if len(sys.argv) < 2:
    print("usage: python makevid_win.py <folder>")
    sys.exit(1)

folder = sys.argv[1]
output = f"{folder}.mp4"
listfile = "filelist.txt"

# generate file list for ffmpeg
images = sorted(glob.glob(os.path.join(folder, "*.jpg")))
with open(listfile, "w") as f:
    for img in images:
        f.write(f"file '{img}'\n")
        f.write("duration 0.0333\n")  # ~30fps

subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", listfile,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    output
])

os.remove(listfile)
print(f"saved {output}")
