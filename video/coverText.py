#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import os
import sys

def rgb(a):
	return "rgb%s" % str(tuple(a))

workingDir = sys.argv[1]
frameFn = sys.argv[2]
title = sys.argv[3]
rows = int(sys.argv[4])
headingSize = 78
titleSize = 98


img = Image.open(os.path.join(workingDir, frameFn)).convert("RGBA").copy()
(width, height) = img.size
tx = (width / 3)
hy = (height / rows) - headingSize
ty = ((rows - 1) * height / rows) - 22

d = ImageDraw.Draw(img)
d.text([tx - 3, hy], "Randomatones", fill="white", font=ImageFont.truetype("impact.ttf", headingSize))
d.text([tx + 3, ty], title, fill="white", font=ImageFont.truetype("impact.ttf", titleSize))

img.save(os.path.join(workingDir, "artwork.png"))
img.close()

