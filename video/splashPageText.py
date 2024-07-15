#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import sys


workingDir = sys.argv[1]
frameFn = sys.argv[2]
title = sys.argv[3]
headingSize = 90
titleSize = int(headingSize * 0.8)
headingStart = 730


titleColour = "#5190ff"
episodeColour = "#ff2d00"

img = Image.open(os.path.join(workingDir, frameFn))
d = ImageDraw.Draw(img)
d.text([60, headingStart], "Randomatones.", fill=titleColour, font=ImageFont.truetype("impact.ttf", headingSize))

d.text([60 + (len("Randomatones") * 0.532 * headingSize), int(headingStart + (headingSize * 0.2))], "30", fill=titleColour, font=ImageFont.truetype("impact.ttf", int(headingSize * 0.8)))

d.text([60, headingStart + headingSize], title, fill=episodeColour, font=ImageFont.truetype("impact.ttf", titleSize))

outFn = os.path.join(workingDir, "splash_%s.png" % frameFn.split(".")[0])
print("saving as", outFn)
img.save(outFn)
img.close()

