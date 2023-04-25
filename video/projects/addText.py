
import os
import sys


charsPerSec = 20.0
textBaseX = 60
textBaseY = 800
titleSize = 130
scrollTextSize = 50
reqTime = 28


def addTextFilterCmdsTo(c, fontSize, x, y, fontFile):
    c.append("fontcolor=0xffffff")
    c.append("x=%s" % x)
    c.append("y=%s" % y)
    c.append("fontsize=%d" % fontSize)
    c.append("fontfile=%s" % fontFile)


def writeText(what, vf, startAt, dur, size, x, y):
    txt = []
    txt.append("drawtext=enable=between(t\,%f\,%f)" % (startAt, startAt + dur))
    txt.append("text='%s'" % what)
    addTextFilterCmdsTo(txt, size, x, y, "/usr/local/share/fonts/impact.ttf")

    vf.append(":".join(txt))

def writeScrollText(what, vf, startAt, readingTime, x, y):
    dt = 1.0 / charsPerSec
    for i in range(len(what)):
        t = what[:i + 1]
        s = startAt + (i * dt)
        d = dt if (i + 1) < len(what) else readingTime
        txt = []
        txt.append("drawtext=enable=between(t\,%f\,%f)" % (s, s + d))
        txt.append("text='%s'" % t)
        addTextFilterCmdsTo(txt, scrollTextSize, x, y, "/usr/share/fonts/X11/Type1/c0419bt_.pfb") #courier regular

        vf.append(":".join(txt))
    return readingTime + (len(what) * 1.0 / charsPerSec)



def applyTextTo(vf, number, title, totalRunningTime):
    readingTime = 4
    startTime = 3
    toScroll = [
        "floating ambient music generators",
        "recorded at locations with natural reverb"
    ]
    for i in range(len(toScroll)):
        s = toScroll[i]
        print(len(s), "chars", len(s) * 1.0 / charsPerSec, startTime)
        startTime += writeScrollText(s, vf, startTime, readingTime, textBaseX, textBaseY + titleSize)
    if len(toScroll) == 0:
        startTime += 10

    writeText("Randomatones", vf, 2, startTime - 2, titleSize, textBaseX, textBaseY)
    startTime = 26
    ed = writeScrollText("episode %d" % number, vf, startTime, readingTime + 3, textBaseX, textBaseY + 50)
    writeText(title, vf, startTime + 3, ed - 3, 100, textBaseX, textBaseY + scrollTextSize + 50)

    endingTextStart = totalRunningTime - 13
    madeByDur = writeScrollText("made by", vf, endingTextStart, 10, textBaseX, textBaseY)
    nameOffSet = 1
    writeText("Andrew Booker", vf, endingTextStart + nameOffSet, madeByDur - nameOffSet, 80, textBaseX, textBaseY + scrollTextSize)

def applyFadeTo(vf, totalRunningTime):
    vf.append("fade=type=in:duration=3,fade=type=out:duration=6:start_time=%d" % (totalRunningTime - 6))

