#!/usr/bin/env python3

import os
import sys
import re
import json
import cv2

inDir = sys.argv[1]
files = filter(lambda f: not os.path.isdir(os.path.join(inDir, f)) and ".txt" not in f, os.listdir(inDir))
title = sys.argv[2]
number = int(sys.argv[3])


d = re.search(r"202[3-9]-[0-1][0-9]-[0-3][0-9]", sys.argv[1]).group()
if not os.path.exists(d):
    os.makedirs(d)

patterns = [
    (r"202[3-9]_[0-9]{4}_.*\.MOV", "apeman"),
    (r"FILE.*\.MOV", "apexcam"),
    (r"NORM.*\.MP4", "dragon"),
    (r"[0-9]{8}_[0-9]{6}\.mp4", "G5")
]

out = {
    "projectName": title,
    "number": number,
    "aliases": {},
    "sequence": []
}

aliasCount = {}
toJoin = {}

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

