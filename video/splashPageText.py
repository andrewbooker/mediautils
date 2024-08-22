#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys


workingDir = sys.argv[1]
frameFn = sys.argv[2]
title = sys.argv[3]
episode_number = sys.argv[4] if len(sys.argv) > 4 else None
headingStart = int(sys.argv[5]) if len(sys.argv) > 5 else 730
headingSize = 90
titleSize = int(headingSize * 0.8)

episodeColour = "#5190ff" #"#ff2d00"
titleColour = "white"   #"#5190ff"

img = Image.open(os.path.join(workingDir, frameFn)).convert("RGB")

d = ImageDraw.Draw(img)
d.text([60, headingStart], "Randomatones.", fill=titleColour, font=ImageFont.truetype("impact.ttf", headingSize))

d.text([60 + (len("Randomatones") * 0.532 * headingSize), int(headingStart + (headingSize * 0.2))], episode_number, fill=titleColour, font=ImageFont.truetype("impact.ttf", int(headingSize * 0.8)))

d.text([60, headingStart + headingSize], title, fill=episodeColour, font=ImageFont.truetype("impact.ttf", titleSize))

outFn = os.path.join(workingDir, "splash_%s.jpg" % frameFn.split(".")[0])
print("saving as", outFn)
img.save(outFn)
img.close()

