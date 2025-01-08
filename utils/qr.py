#!/usr/bin/env python
import qrcode

img = qrcode.make("http://randomatones.co.uk/portfolio.html")
img.save("qr.png")
