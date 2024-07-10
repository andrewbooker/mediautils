#!/usr/bin/env python3

import sys
import os
import json

seqFn = os.path.join(sys.argv[1], "edits.json")
srcPath = sys.argv[2]
baseOutDir = os.path.dirname(srcPath)

def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)

j = load()
inFiles = [(os.path.join(srcPath, e), j[e]["sync"], j[e]["length"]) for e in j]


toMergeDir = os.path.join(baseOutDir, "toMerge")
if not os.path.exists(toMergeDir):
    os.makedirs(toMergeDir)


mergedDir = os.path.join(baseOutDir, "merged")
if not os.path.exists(mergedDir):
    os.makedirs(mergedDir)

loQ = True
h = 1080
w = 1920
workingExt = "avi" if loQ else "mp4"
compression = "-crf 0" if not loQ else "-b:v 40M -c:v mpeg4 -vtag XVID"

dur = None
for f in inFiles:
    _, ss, d = f
    dd = int(d - ss)
    if dur is None or dd < dur:
        dur = dd

srcs = []
for f in inFiles:
    i, ss, _ = f
    cmd = ["ffmpeg"]
    if ss > 0:
        cmd.append(f"-ss {ss}")
    cmd.append(f"-t {dur}")
    cmd.append(f"-i \"{i}\"")
    cmd.append(f"-vf \"scale={int(w / 2)}x{int(h / 2)}\"")
    fn = os.path.join(toMergeDir, f"{len(srcs)}.{workingExt}")
    cmd.append(f"-y {fn}")

    print(" ".join(cmd))
    srcs.append(fn)


mCmd = ["ffmpeg"]
for i in range(len(srcs)):
    mCmd.append("-i")
    mCmd.append(srcs[i])
fc = []
fc.append("[0][1]hstack[top]")
fc.append("[2][3]hstack[bottom]")
fc.append("[top][bottom]vstack[out]")

mCmd.append("-filter_complex \"%s\"" % ";".join(fc))
mCmd.append("-map \"[out]\" -y")
mCmd.append("-an -r 30 -y")
mCmd.append(compression)
jfn = os.path.join(mergedDir, f"contact.{workingExt}")
mCmd.append(jfn)
os.system(" ".join(mCmd))

