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
headingSize = 170
titleSize = headingSize + 10
headingStart = 40

img = Image.open(os.path.join(workingDir, frameFn))
d = ImageDraw.Draw(img)
d.text([60, headingStart], "Randomatones", fill="yellow", font=ImageFont.truetype("impact.ttf", headingSize))
d.text([60, headingStart + headingSize], title, fill="orange", font=ImageFont.truetype("impact.ttf", titleSize))

img.save(os.path.join(workingDir, "splash_%s.png" % frameFn.split(".")[0]))
img.close()

