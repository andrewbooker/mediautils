#!/usr/bin/env python3

import sys
import os
import json

def toSecs(s):
    if type(s) != str:
        return s
    spl = s.split(":")
    return (float(spl[0]) * 60) + float(spl[1])


def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)

rawDir = sys.argv[1]
seqFn = sys.argv[2]
baseOutDir = sys.argv[3]

res_options = [
    "1920x1080",
    "768x432",
    "3840x2160"
]

res = int(sys.argv[4]) if len(sys.argv) > 4 else 0
loRes = res == 1
resolution = res_options[res]
horiz = int(resolution.split("x")[0])
vert = int(resolution.split("x")[1])

textColourTestsDir = os.path.join(baseOutDir, "textColourTests")
if not os.path.exists(textColourTestsDir):
    os.makedirs(textColourTestsDir)


j = load()
text = j["text"]

srcs = []

headingStart = text["heading"]["start"]
print(headingStart)

class Sequence:
    def __init__(self):
        self.filesByStartTime = dict()

    def load_from(self, model):
        sequence = model["sequence"]
        files = {model["aliases"][a]["name"]: a for a in model["aliases"]}
        rt = 0
        for s in sequence:
            fr = s[0]
            start = toSecs(s[1][0])
            dur = s[1][1]
            self.filesByStartTime.setdefault(rt, (files[fr], start))
            rt += dur

    def file_at(self, rt):
        ks = [k for k in self.filesByStartTime]
        for i in range(len(ks)):
            c = ks[i]
            n = ks[i + 1]
            if rt >= c and rt < n:
                fn, start = self.filesByStartTime[c]
                pos = (rt - c) + start
                fnb = fn.split(".")[0]
                fqfn_in = os.path.join(rawDir, fn)
                fqfn_out = os.path.join(textColourTestsDir, f"{fnb}_{pos}.jpg")
                os.system(f"./extract_single_frame.sh {fqfn_in} {pos} {fqfn_out} 2>/dev/null")
                return (rt, fqfn_out, start, pos)

seq = Sequence()
seq.load_from(j)
print(seq.filesByStartTime)

print(seq.file_at(4))
print(seq.file_at(6))
print(seq.file_at(14))

