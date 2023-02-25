#!/usr/bin/env python3

import os
import sys
from functools import reduce

workingDir = sys.argv[1]
files = []
for i in range(6):
    files.append("%02d.png" % (i + 1))

cmd = ["ffmpeg"]
for f in files:
    cmd.append("-i")
    cmd.append(os.path.join(workingDir, f))


fc = []

def redFn(name, f1, f2):
    r = "%s_%s" % (f1, f2)
    fc.append("[%s][%s]%s[%s]" % (f1, f2, name, r))
    return r

def hstack(f1, f2):
    return redFn("hstack", f1, f2)

def vstack(f1, f2):
    return redFn("vstack", f1, f2)

out = vstack(reduce(hstack, [0, 1, 2]), reduce(hstack, [3, 4, 5]))

cmd.append("-filter_complex")
cmd.append("\"%s\"" % ";".join(fc))
cmd.append("-map")
cmd.append("[%s]" % out)
cmd.append("-y")
cmd.append(os.path.join(workingDir, "out.jpg"))


os.system(" ".join(cmd))

