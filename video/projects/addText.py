
import os
import sys


charsPerSec = 20.0
textBaseX = 60
titleSize = 130
scrollTextSize = 50
reqTime = 28


FONT_IMPACT = "/usr/local/share/fonts/impact.ttf"
FONT_COURIER = "/usr/share/fonts/X11/Type1/c0419bt_.pfb"


def addTextFilterCmdsTo(c, fontSize, x, y, fontFile, colour):
    c.append("fontcolor=%s" % colour)
    c.append("x=%s" % x)
    c.append("y=%s" % y)
    c.append("fontsize=%d" % fontSize)
    c.append("fontfile=%s" % fontFile)


def writeText(what, vf, startAt, dur, size, x, y, colour):
    txt = []
    txt.append("drawtext=enable=between(t\,%f\,%f)" % (startAt, startAt + dur))
    txt.append("text='%s'" % what)
    addTextFilterCmdsTo(txt, size, x, y, FONT_IMPACT, colour)

    vf.append(":".join(txt))

def writeSmallText(what, vf, fontSize, x, y, startAt, dur, colour):
    txt = []
    txt.append("drawtext=enable=between(t\,%f\,%f)" % (startAt, startAt + dur))
    txt.append("text='%s'" % what)
    addTextFilterCmdsTo(txt, fontSize, x, y, FONT_IMPACT, colour)

    vf.append(":".join(txt))

def writeScrollText(what, vf, startAt, readingTime, x, y, colour):
    dt = 1.0 / charsPerSec
    for i in range(len(what)):
        t = what[:i + 1]
        s = startAt + (i * dt)
        d = dt if (i + 1) < len(what) else readingTime
        writeSmallText(t, vf, scrollTextSize, x, y, s, d, colour)

    return readingTime + (len(what) * 1.0 / charsPerSec)


def applyTextTo(vf, spec):
    number = spec["number"]
    title = spec["title"]
    totalRunningTime = spec["tt"]
    headingColour = spec["colour"] if "colour" in spec else "white"
    episodeColour = spec["colour"] if "colour" in spec else "white"
    textBaseY = spec["yPos"]
    textColour = episodeColour
    readingTime = 2.5
    startTime = spec["heading"]["start"] + 1
    toScroll = [
        "randomised ambient music generators",
        "running on battery-powered Raspberry Pi computers"
    ]
    
    for i in range(len(toScroll)):
        s = toScroll[i]
        print(len(s), "chars", len(s) * 1.0 / charsPerSec, startTime)
        startTime += writeScrollText(s, vf, startTime, readingTime, textBaseX, textBaseY + titleSize, textColour)
    if len(toScroll) == 0:
        startTime += 10

    writeText("Randomatones", vf, spec["heading"]["start"], spec["heading"]["dur"], titleSize, textBaseX, textBaseY, headingColour)

    startTime = spec["episode"]["start"]
    dur = spec["episode"]["dur"] if "dur" in spec["episode"] else 10
    if "yPos" in spec["episode"]:
        textBaseY = spec["episode"]["yPos"]
    ed = writeScrollText("episode %d" % number, vf, startTime, dur, textBaseX, textBaseY + 50, textColour)
    writeText(title, vf, startTime + 3, ed - 3, 100, textBaseX, textBaseY + scrollTextSize + 50, episodeColour)

    endingTextStart = totalRunningTime - 13
    madeByDur = writeScrollText("made by", vf, endingTextStart, 10, textBaseX, textBaseY, textColour)
    nameOffSet = 1
    writeText("Andrew Booker", vf, endingTextStart + nameOffSet, madeByDur - nameOffSet, 80, textBaseX, textBaseY + scrollTextSize, headingColour)

def applyFadeTo(vf, totalRunningTime):
    vf.append("fade=type=in:duration=3,fade=type=out:duration=6:start_time=%d" % (totalRunningTime - 6))

