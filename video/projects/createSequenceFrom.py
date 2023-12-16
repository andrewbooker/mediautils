#!/usr/bin/env python3

import os
import sys
import re
import json
import cv2

inDir = sys.argv[1]
#files = filter(lambda f: not os.path.isdir(os.path.join(inDir, f)) and ".txt" not in f, os.listdir(inDir))
files = []
title = sys.argv[2]
number = int(sys.argv[3])


d = re.search(r"202[0-9]-[0-1][0-9]-[0-3][0-9]", sys.argv[1]).group()
if not os.path.exists(d):
    os.makedirs(d)

patterns = [
    (r"202[0-9]_[0-9]{4}_.*\.MOV", "apeman"),
    (r"FILE.*\.MOV", "apexcam"),
    (r"NORM.*\.MP4", "dragon"),
    (r"[0-9]{8}_[0-9]{6}\.mp4", "G5"),
    (r"VID_[0-9]{8}_[0-9]{9}\.mp4", "NP2")
]

out = {
    "projectName": title,
    "number": number,
    "aliases": {},
    "sequence": []
}

aliasCount = {}
toJoin = {}
edits = {}

for f in files:
    print("reading length of", f)
    v = cv2.VideoCapture(os.path.join(inDir, f))
    length = v.get(cv2.CAP_PROP_FRAME_COUNT) / v.get(cv2.CAP_PROP_FPS)
    for p in patterns:
        if len(re.findall(p[0], f)):
            if p[1] not in aliasCount:
                aliasCount[p[1]] = 0
            aliasCount[p[1]] += 1
            if p[1] in ["apexcam", "dragon"]:
                if p[1] not in toJoin:
                    toJoin[p[1]] = []
                toJoin[p[1]].append({ "file": f, "length": length })
            else:
                out["aliases"][f] = { "name": "%s_%d" % (p[1], aliasCount[p[1]]), "length": length }
        else:
            out["aliases"][f] = { "name": ".".join(f.split(".")[:-1]), "length": length }
        edits[f] = {"sync": 0, "edits": []}

for (a, fs) in toJoin.items():
    cf = os.path.join(inDir, "%s.txt" % a)
    tl = 0
    with open(cf, "w") as concat:
        for f in fs:
            tl += f["length"]
            concat.write("file '%s'\n" % f["file"])
            outfile = "%s.%s" % (a, f["file"].split(".")[1])
    os.system("ffmpeg -safe 0 -f concat -i %s -c copy -y %s" % (cf, os.path.join(inDir, outfile)))
    out["aliases"][outfile] = { "name": a, "length": tl }


with open(os.path.join(d, "sequence.json"), "w") as js:
    json.dump(out, js, indent=4)

with open(os.path.join(d, "edits.json"), "w") as ejs:
    json.dump(edits, ejs, indent=4)

buildDir = os.path.dirname(inDir)
buildFn = os.path.join(buildDir, "build.py")
resDir = os.path.dirname(os.getcwd())
buildSeqFn = os.path.join(resDir, "buildSequence.py")
seqFn = os.path.join(os.getcwd(), d, "sequence.json")

with open(buildFn, "w") as build:
    build.write("#!/bin/bash\n")
    build.write(f"{buildSeqFn} {inDir} {seqFn} . 1\n")
    build.write("./compile.sh")
    build.write("./merge.sh")
    build.write("#./extractAudio.sh")
    build.write("#~/Documents/wavmixer/mix.py ./Audio/ Audio/cues.json")
    build.write("#ffmpeg -i merged/merged.avi -i Audio/cues_L.wav -i Audio/cues_R.wav -filter_complex \"[1:a]amerge=inputs=2[a]\" -ac 2 -map 0:v -map \"[a]\" -y merged/test.mp4")

os.system(f"chmod +x {buildFn}")
