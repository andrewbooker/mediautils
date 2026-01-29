#!/usr/bin/env python3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import os
import sys
import math
from datetime import datetime
import qrcode


spec = {
    "orientation": "landscape",
    "cropLeft": 0,
    "sub": {
        "text": "Ambient music sound art installation",
    },
    "loc": {
        "details": [
            "Turbine Room",
            "The Engine House",
            "2 Forest Road London N17 9NH"
        ],
        "h": 0.63
    },
    "dates": {
        "from": "2026-02-28",
        "to": "2026-03-01"
    },
    "times": {
        "from": "09:30",
        "to": "15:30"
    },
    "admission": "Free entry",
    "headingColour": "LightBlue"
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
width = int(height / math.sqrt(2)) if cropLeft > 0 else origWidth
if cropLeft > 0:
    img = img.crop((cropLeft, 0, cropLeft + width, height))

print(img.size)

heading = "Randomatones"
headingColour = (255, 255, 255) # if "headingColour" not in spec else spec["headingColour"]
tx = 70
hy = 50
headingRatio = 1.75
subHeadingRatio = 2.15
if "orientation" in spec and spec["orientation"] == "landscape":
    headingRatio = 0.65
    subHeadingRatio = 0.8
    hy = int(0.08    * height)
headingSize = int(headingRatio * width / len(heading))

txt = Image.new("RGBA", img.size, (0,0,255,60))

img = Image.alpha_composite(img, txt)
img.save(os.path.join(workingDir, f"background.png"))

d = ImageDraw.Draw(img)
d.text([tx - 3, hy], heading, fill=headingColour, font=ImageFont.truetype("impact.ttf", headingSize))


title = spec["sub"]["text"]
ty = int(hy + headingSize + 30)
titleSize = int(subHeadingRatio * width / len(title))
d.text([tx + 3, ty], title, fill=headingColour, font=ImageFont.truetype("impact.ttf", titleSize))

locY = int(spec["loc"]["h"] * height)
dy = 0
detailSize = 90
details = spec["loc"]["details"][:]
details.extend([dates(), times(), spec["admission"], "randomatones.co.uk"])
for detail in details:
    detailSize -= 5
    d.text([tx + 3, locY + dy], detail, fill="white", font=ImageFont.truetype("impact.ttf", detailSize))
    dy += detailSize + 10

yt = Image.open("./logo-youtube.png")
ig = Image.open("./logo-instagram.png").resize(yt.size)
img.paste(yt, (tx, locY + dy), mask=yt)
img.paste(ig, (tx + 6 + yt.size[0], locY + dy), mask=ig)
d.text([tx + yt.size[0] + ig.size[0] + 12, locY + dy], "@randomatones", fill="white", font=ImageFont.truetype("impact.ttf", detailSize))

if "orientation" not in spec or spec["orientation"] != "landscape":
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2
    )
    qr.add_data("https://www.youtube.com/@Randomatones/videos")
    qr.make(fit=True)

    bottomLeft = 400
    img.paste(qr.make_image(fill_color="black", back_color="white"), (width - bottomLeft, height - bottomLeft))

img.save(os.path.join(workingDir, f"{outFn}.png"))
img.close()


print("heading size", headingSize)
print("title size", titleSize)

