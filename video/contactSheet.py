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
fc.append("[0][1]hstack[v1a]")
fc.append("[v1a][2]hstack[v1]")
fc.append("[3][4]hstack[v2a]")
fc.append("[v2a][5]hstack[v2]")

fc.append("[v1][v2]vstack[out]")

cmd.append("-filter_complex")
cmd.append("\"%s\"" % ";".join(fc))
cmd.append("-map")
cmd.append("[out]")
cmd.append("-y")
cmd.append(os.path.join(workingDir, "out.jpg"))

os.system(" ".join(cmd))

