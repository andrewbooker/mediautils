#!/usr/bin/env python3

import os
import sys
from functools import reduce

workingDir = sys.argv[1]
layout = [2, 3, 2]
layerCount = [0, 2, 5]
print(layerCount)
numberOfComponents = reduce(lambda a, b: a + b, layout)
print(numberOfComponents, "components")

files = []
for i in range(numberOfComponents):
    files.append("%02d.png" % i)

cmd = ["ffmpeg"]
for f in files:
    cmd.append("-i")
    cmd.append(os.path.join(workingDir, f))


fc = []

def singleFn(name, f, o):
    fc.append("[%s]%s[%s]" % (f, name, o))
    return o

def binaryFn(name, f1, f2):
    r = "%s_%s" % (f1, f2)
    fc.append("[%s][%s]%s[%s]" % (f1, f2, name, r))
    return r

def hstack(f1, f2):
    return binaryFn("hstack", f1, f2)

def vstack(f1, f2):
    return binaryFn("vstack", f1, f2)


class Cropper:
    inRatio = (16, 9)
    finalSquareSide = 1440
    h = 1080

    def __init__(self, spl):
        squareUnits = Cropper.inRatio[1] * len(spl)
        self.crop = []
        self.scale = []
        self.h = Cropper.finalSquareSide / len(spl)

        for s in spl:
            wu = int(squareUnits / s) + (s % len(spl))
            cw = int(Cropper.h * wu / Cropper.inRatio[1])
            tw = 0
            tcu = 0
            for ss in range(s - 1):
                w = Cropper.finalSquareSide / s
                tw += w
                tcu += wu
                self.scale.append(w)
                self.crop.append(cw)
            self.scale.append(Cropper.finalSquareSide - tw)
            self.crop.append(int(Cropper.h * (squareUnits - tcu) / Cropper.inRatio[1]))

    def at(self, i):
        cr = f"{int(self.crop[i])}:1080"
        sc = f"{int(self.scale[i])}:{int(self.h)}"
        return singleFn(f"crop={cr},scale={sc}", i, f"cs{i}")


cropper = Cropper(layout)
s = [cropper.at(i) for i in range(len(files))]

h = [reduce(hstack, s[layerCount[i]:layerCount[i] + layout[i]]) for i in range(len(layout))]
out = reduce(vstack, h)

cmd.append("-filter_complex")
cmd.append("\"%s\"" % ";".join(fc))
cmd.append("-map")
cmd.append("[%s]" % out)
cmd.append("-y")
cmd.append(os.path.join(workingDir, "contact.bmp"))

print(" ".join(cmd))
if len(sys.argv) > 2 and int(sys.argv[2]) == 1:
    os.system(" ".join(cmd))
