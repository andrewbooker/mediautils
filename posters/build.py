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
    fmt = "%a %d %b"
    y = spec["dates"]["to"][:4]
    return f"{datetime.strftime(df, fmt)} to {datetime.strftime(dt, fmt)} {y}"

def times():
    f = spec["times"]["from"]
    t = spec["times"]["to"]
    return f"{f} to {t} each day"

workingDir = sys.argv[1]
frameFn = sys.argv[2]
outFn = sys.argv[3]
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
detailSize = 75
details = spec["loc"]["details"][:]
details.extend([dates(), times(), spec["admission"], "randomatones.co.uk"])
for detail in details:
    detailSize -= 5
    d.text([tx + 3, locY + dy], detail, fill="white", font=ImageFont.truetype("impact.ttf", detailSize))
    dy += detailSize + 10

d.text([tx + 3, locY + dy], "youtube.com/@Randomatones", fill="white", font=ImageFont.truetype("impact.ttf", detailSize))
#yt = Image.open("./logo-youtube.svg").convert("RGBA").copy()


img.save(os.path.join(workingDir, f"{outFn}.png"))
img.close()


print("heading size", headingSize)
print("title size", titleSize)

