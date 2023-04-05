#!/usr/bin/env python3

import os
import sys


charsPerSec = 20.0
textBaseY = 800
titleSize = 130
reqTime = 28
totalRunningTime = 45

def addTextFilterCmdsTo(c, fontSize, y, fontFile):
    c.append("fontcolor=0xffffff")
    c.append("x=60")
    c.append("y=%d" % y)
    c.append("fontsize=%d" % fontSize)
    c.append("fontfile=%s" % fontFile)


def writeText(what, vf, startAt, dur, size, y):
    txt = []
    txt.append("drawtext=enable=between(t\,%f\,%f)" % (startAt, startAt + dur))
    txt.append("text='%s'" % what)
    addTextFilterCmdsTo(txt, size, y, "/usr/local/share/fonts/impact.ttf")

    vf.append(":".join(txt))

def writeScrollText(what, vf, startAt, readingTime, y):
    dt = 1.0 / charsPerSec
    for i in range(len(what)):
        t = what[:i + 1]
        s = startAt + (i * dt)
        d = dt if (i + 1) < len(what) else readingTime
        txt = []
        txt.append("drawtext=enable=between(t\,%f\,%f)" % (s, s + d))
        txt.append("text='%s'" % t)
        addTextFilterCmdsTo(txt, 50, y, "/usr/share/fonts/X11/Type1/c0419bt_.pfb") #courier regular

        vf.append(":".join(txt))
    return readingTime + (len(what) * 1.0 / charsPerSec)


def applyTextTo(vf, number, title, location):
    toScroll = [
        "single-board computer ambient music generators",
        "recorded at outdoor locations with natural reverb",
        "this is episode %d" % number,
    ]

    readingTime = 4
    startTime = 4
    for i in range(len(toScroll)):
        s = toScroll[i]
        print(len(s), "chars", len(s) * 1.0 / charsPerSec, startTime)
        startTime += writeScrollText(s, vf, startTime, readingTime, textBaseY + titleSize)

    writeText("Randomatones", vf, 2, startTime - 2, titleSize, textBaseY)

    coordsDur = writeScrollText(location, vf, startTime + readingTime, reqTime - startTime, textBaseY + titleSize)
    writeText(title, vf, startTime, coordsDur + readingTime, 100, textBaseY)


    endingTextStart = totalRunningTime - 14
    madeByDur = writeScrollText("made by", vf, endingTextStart, 10, textBaseY)
    nameOffSet = 1
    writeText("Andrew Booker", vf, endingTextStart + nameOffSet, madeByDur - nameOffSet, 80, textBaseY + 50)

def applyFadeTo(vf):
    vf.append("fade=type=in:duration=3,fade=type=out:duration=4:start_time=%d" % (totalRunningTime - 4))


vf = []
applyTextTo(vf, 19, "Regents Canal Park Road", "latitude 51.5284447 longitude -0.1669526 03 Mar 2023 6.30pm")
applyFadeTo(vf)

applyToFn = sys.argv[1]
outDir = sys.argv[2]

cmd = []
cmd.append("ffmpeg")
cmd.append("-i")
cmd.append(applyToFn)
if len(vf):
    cmd.append("-vf")
    cmd.append("\"%s\"" % ",".join(vf))
cmd.append("-y")
cmd.append(os.path.join(outDir, "with_text.mp4"))

fc = " ".join(cmd)
os.system(fc)
