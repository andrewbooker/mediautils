#!/usr/bin/env python3

import os
import sys
from functools import reduce

workingDir = sys.argv[1]
files = []
for i in range(12):
    files.append("%02d.png" % (i + 1))

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

def cropScale(f):
    return singleFn("crop=1440:1080,scale=480:360", f, "cs%s" %f)


s = [cropScale(i) for i in range(len(files))]
h = [reduce(hstack, s[(i*3):((i+1)*3)]) for i in range(int(len(files) / 3))]

out = reduce(vstack, h)

cmd.append("-filter_complex")
cmd.append("\"%s\"" % ";".join(fc))
cmd.append("-map")
cmd.append("[%s]" % out)
cmd.append("-y")
cmd.append(os.path.join(workingDir, "out.bmp"))

os.system(" ".join(cmd))
