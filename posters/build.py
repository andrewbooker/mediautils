#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import os
import sys
import math
from datetime import datetime


spec = {
    "cropLeft": 1040,
    "sub": {
        "text": "Ambient music sound art installation",
    },
    "loc": {
        "details": [
            "The Engine House",
            "Walthamstow Wetlands",
            "2 Forest Road",
            "London N17 9NH"
        ],
        "h": 0.7
    },
    "dates": {
        "from": "2026-02-28",
        "to": "2026-03-01"
    },
    "times": {
        "from": "09:30",
        "to": "15:30"
    },
    "admission": "Free entry"
}


def rgb(a):
	return "rgb%s" % str(tuple(a))

def dates():
    inFmt = "%Y-%m-%d"
    df = datetime.strptime(spec["dates"]["from"], inFmt)
    dt = datetime.strptime(spec["dates"]["to"], inFmt)
    fmt = "%d %b"
    y = spec["dates"]["to"][:4]
    return f"{datetime.strftime(df, fmt)} to {datetime.strftime(dt, fmt)} {y}"

def times():
    f = spec["times"]["from"]
    t = spec["times"]["to"]
    return f"{f} to {t} each day"

workingDir = sys.argv[1]
frameFn = sys.argv[2]
cropLeft = spec["cropLeft"]

img = Image.open(os.path.join(workingDir, frameFn)).convert("RGBA").copy()
(origWidth, height) = img.size
width = int(height / math.sqrt(2))
img = img.crop((cropLeft, 0, cropLeft + width, height))
d = ImageDraw.Draw(img)
print(img.size)

heading = "Randomatones"

tx = 70
hy = 50
headingSize = int(1.75 * width / len(heading))
d.text([tx - 3, hy], heading, fill="white", font=ImageFont.truetype("impact.ttf", headingSize))



title = spec["sub"]["text"]
ty = int(hy + headingSize + 30)
titleSize = int(2.15 * width / len(title))
d.text([tx + 3, ty], title, fill="white", font=ImageFont.truetype("impact.ttf", titleSize))

locY = int(spec["loc"]["h"] * height)
dy = 0
locSize = 70
for dt in spec["loc"]["details"]:
    d.text([tx + 3, locY + dy], dt, fill="white", font=ImageFont.truetype("impact.ttf", locSize))
    dy += locSize + 10


whenSize = 60
d.text([tx + 3, locY + dy], dates(), fill="white", font=ImageFont.truetype("impact.ttf", whenSize))
dy += whenSize + 10
d.text([tx + 3, locY + dy], times(), fill="white", font=ImageFont.truetype("impact.ttf", whenSize))
dy += whenSize + 10
d.text([tx + 3, locY + dy], spec["admission"], fill="white", font=ImageFont.truetype("impact.ttf", whenSize - 10))



img.save(os.path.join(workingDir, "artwork1.png"))
img.close()


print("heading size", headingSize)
print("title size", titleSize)

