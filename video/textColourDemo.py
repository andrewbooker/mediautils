#!/usr/bin/env python3

import sys
import os
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def toSecs(s):
    if type(s) != str:
        return s
    spl = s.split(":")
    return (float(spl[0]) * 60) + float(spl[1])


def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)


def writeTextOnto(fqfn, instructions):
    for i in instructions:
        text, size, yPos, colour = i
        print(size, yPos, colour, text)
        img = Image.open(fqfn).convert("RGB")
        d = ImageDraw.Draw(img)
        d.text([60, yPos], text, fill=colour, font=ImageFont.truetype("impact.ttf", size))
        img.save(fqfn)
        img.close()


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
                return (fqfn_out, start, pos, rt)

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
if not "text" in j:
    print("sequence has no text")
    exit

spec = j["text"]
srcs = []


seq = Sequence()
seq.load_from(j)

yPos = spec["yPos"] if "yPos" in spec else 60
masterColour = spec["colour"] if "colour" in spec else "white"
madeByColour = spec["madeBy"]["colour"] if "madeBy" in spec and "colour" in spec["madeBy"] else masterColour

def heading():
    start = spec["heading"]["start"]
    fhs = seq.file_at(start)
    writeTextOnto(fhs[0], [("Randomatones", 130, yPos, masterColour)])

def episode():
    number = j["number"]
    title = j["projectName"]
    episodeColour = spec["episode"]["colour"] if "colour" in spec["episode"] else masterColour
    start = spec["episode"]["start"]
    fhs = seq.file_at(start)
    episodeYPos = spec["episode"]["yPos"] if "yPos" in spec["episode"] else yPos
    writeTextOnto(fhs[0], [
        (f"Episode {number}", 50, episodeYPos, episodeColour),
        (title, 50, episodeYPos + 50, episodeColour)
    ])


heading()
episode()

