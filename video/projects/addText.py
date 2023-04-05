
import os
import sys


charsPerSec = 20.0
textBaseY = 800
titleSize = 130
reqTime = 28


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


def applyTextTo(vf, number, title, location, totalRunningTime):
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

def applyFadeTo(vf, totalRunningTime):
    vf.append("fade=type=in:duration=3,fade=type=out:duration=4:start_time=%d" % (totalRunningTime - 4))

