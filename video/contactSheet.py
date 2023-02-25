#!/usr/bin/env python3

import os
import sys

workingDir = sys.argv[1]
files = []
for i in range(6):
    files.append("%02d.png" % (i + 1))

cmd = ["ffmpeg"]
for f in files:
    cmd.append("-i")
    cmd.append(os.path.join(workingDir, f))


fc = []

def hstack(l, r, c):
    return "[%s][%s]hstack[%s]" % (l, r, c)

def vstack(t, b, c):
    return "[%s][%s]vstack[%s]" % (t, b, c)


fc.append(hstack(0, 1, "h01"))
fc.append(hstack("h01", 2, "h012"))
fc.append(hstack(3, 4, "h34"))
fc.append(hstack("h34", 5, "h345"))

fc.append(vstack("h012", "h345", "out"))

cmd.append("-filter_complex")
cmd.append("\"%s\"" % ";".join(fc))
cmd.append("-map")
cmd.append("[out]")
cmd.append("-y")
cmd.append(os.path.join(workingDir, "out.jpg"))

os.system(" ".join(cmd))

