#!/usr/bin/env python

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

A6 = [111, 154]
DPI = 300
INCH_PER_MM = 1000 / 2.54

SIZE = tuple([int(DPI * INCH_PER_MM / m) for m in A6])
print(SIZE)


from reportlab.pdfgen.canvas import Canvas
canvas = Canvas("thing.pdf", pagesize=SIZE)
canvas.drawString(72, 72, "Randomatones")
canvas.save()
