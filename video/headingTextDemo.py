#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys


storyboardDir = os.path.join(sys.argv[1], "storyboard")
colourHex = sys.argv[2]
sceneIdx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
files = [f for f in sorted(os.listdir(storyboardDir), key=lambda fn: int(fn.split("_")[0]))]
img = Image.open(os.path.join(storyboardDir, files[sceneIdx]))
d = ImageDraw.Draw(img)
headingSize = 120
headingYPos = 800
d.text([60, headingYPos], "Randomatones", fill=f"#{colourHex}", font=ImageFont.truetype("impact.ttf", headingSize))

img.save(os.path.join(sys.argv[1], f"scene{sceneIdx}_{colourHex}.jpg"))
img.close()

