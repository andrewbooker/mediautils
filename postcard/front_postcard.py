#!/usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
import os
from PIL import Image
import requests
import io


bleed = 0.3 * cm
size = (tuple([t + (bleed * 2) for t in landscape(A6)]))
canvas = Canvas("postcard_front.pdf", pagesize=size)

w_imgs = [
    ("/home/abooker/Downloads/IMG_20251004_131115316.jpg", 0.4, "Barclay Park"),
    ("54959381627_79bb48599d", 0.0, "Coventry"),
    ("54303583019_8b91477cc0", 0.3, "Turbine Room"),
    ("54842102195_72a90b1762", 0.0, "Woodbridge")
]

x_2 = size[0] / 2
y_2 = size[1] / 2
ratio = size[0] / size[1]

for i in range(4):
    isLocal = w_imgs[i][0][0] == "/"
    if not isLocal:
        get_resp = requests.get(f"https://live.staticflickr.com/65535/{w_imgs[i][0]}_b.jpg")
        if get_resp.status_code != 200:
            break

        pil_img = Image.open(io.BytesIO(get_resp.content))
    else:
        pil_img = Image.open(w_imgs[i][0])
    required_width = int(pil_img.height * ratio)
    surplus_width = pil_img.width - required_width

    top = 0
    bottom = pil_img.height
    left = surplus_width * w_imgs[i][1]
    right = left + required_width

    img = ImageReader(pil_img.crop((left, top, right, bottom)))
    canvas.drawImage(img, (i % 2) * x_2, (int(0.5 * i) % 2) * y_2, width=x_2, height=y_2, mask="auto")

canvas.save()
