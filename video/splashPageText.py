#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys


workingDir = sys.argv[1]
storyboardDir = os.path.join(workingDir, "storyboard")
frameFn = sys.argv[2]
title = sys.argv[3]
headingSize = 130
titleSize = int(headingSize * 0.8)
headingStart = 50

img = Image.open(os.path.join(storyboardDir, frameFn))
d = ImageDraw.Draw(img)
d.text([60, headingStart], "Randomatones.", fill="yellow", font=ImageFont.truetype("impact.ttf", headingSize))
d.text([60 + (len("Randomatones") * 0.535 * headingSize), int(headingStart * 1.54)], "26", fill="yellow", font=ImageFont.truetype("impact.ttf", int(headingSize * 0.8)))
d.text([60, headingStart + headingSize], title, fill="orange", font=ImageFont.truetype("impact.ttf", titleSize))

img.save(os.path.join(workingDir, "splash_%s.jpg" % frameFn.split(".")[0]))
img.close()

