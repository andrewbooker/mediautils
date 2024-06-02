#!/usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6, landscape


canvas = Canvas("thing.pdf", pagesize=landscape(A6))
canvas.drawString(72, 144, "Randomatones")
canvas.save()
