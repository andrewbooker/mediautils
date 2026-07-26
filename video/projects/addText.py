
import os
import sys


charsPerSec = 20.0
textBaseX = 60
titleSize = 130
scrollTextSize = 50
reqTime = 28


FONT_IMPACT = "/usr/local/share/fonts/impact.ttf"
FONT_COURIER = "/usr/share/fonts/X11/Type1/c0419bt_.pfb"

def startFrom(s):
    if type(s) != str:
        return s
    spl = s.split(":")
    return (int(spl[0]) * 60) + int(spl[1])


def addTextFilterCmdsTo(c, fontSize, x, y, fontFile, colour, bordercolor=None):
    c.append("fontcolor=%s" % colour)
    c.append("x=%s" % x)
    c.append("y=%s" % y)
    c.append("fontsize=%d" % fontSize)
    c.append("fontfile=%s" % fontFile)
    if bordercolor is not None:
        c.append(f"bordercolor={bordercolor}")
        c.append("borderw=1")

def writeText(what, vf, startAt, dur, size, x, y, colour, bordercolor=None):
    txt = []
    txt.append("drawtext=enable=between(t\,%f\,%f)" % (startAt, startAt + dur))
    txt.append("text='%s'" % what)
    addTextFilterCmdsTo(txt, size, x, y, FONT_IMPACT, colour, bordercolor)

    vf.append(":".join(txt))


def writeSmallText(what, vf, fontSize, x, y, startAt, dur, colour, bordercolor=None):
    txt = []
    txt.append("drawtext=enable=between(t\,%f\,%f)" % (startAt, startAt + dur))
    txt.append("text='%s'" % what)
    addTextFilterCmdsTo(txt, fontSize, x, y, FONT_IMPACT, colour, bordercolor)

    vf.append(":".join(txt))


def writeScrollText(what, vf, startAt, readingTime, x, y, colour, bordercolor=None):
    dt = 1.0 / charsPerSec
    for i in range(len(what)):
        t = what[:i + 1]
        s = startAt + (i * dt)
        d = dt if (i + 1) < len(what) else readingTime
        writeSmallText(t, vf, scrollTextSize, x, y, s, d, colour, bordercolor)

    return readingTime + (len(what) * 1.0 / charsPerSec)


def applyTextTo(vf, spec):
    masterColour = spec["colour"] if "colour" in spec else "white"
    masterBorderColour = spec["borderColour"] if "borderColour" in spec else None
    madeByColour = spec["madeBy"]["colour"] if "madeBy" in spec and "colour" in spec["madeBy"] else masterColour
    textBaseY = spec["yPos"] if "yPos" in spec else 60 
    totalRunningTime = spec["tt"]
    readingTime = 9

    if "heading" in spec:
        headingColour = spec["heading"]["colour"] if "colour" in spec["heading"] else masterColour
        headingBorderColour = spec["heading"]["borderColour"] if "borderColour" in spec["heading"] else masterBorderColour
        startTime = spec["heading"]["start"] + 1
        toScroll = [
            "Randomised ambient music generators"
        ]

        for i in range(len(toScroll)):
            s = toScroll[i]
            print(len(s), "chars", len(s) * 1.0 / charsPerSec, startTime)
            startTime += writeScrollText(s, vf, startTime, readingTime, textBaseX, textBaseY + titleSize, headingColour, headingBorderColour)
        if len(toScroll) == 0:
            startTime += 10

        writeText("Randomatones", vf, spec["heading"]["start"], spec["heading"]["dur"], titleSize, textBaseX, textBaseY, headingColour, headingBorderColour)

    if "episode" in spec:
        number = spec["number"]
        title = spec["title"]
        episodeColour = spec["episode"]["colour"] if "colour" in spec["episode"] else masterColour
        episodeBorderColour = spec["episode"]["borderColour"] if "borderColour" in spec["episode"] else masterBorderColour
        startTime = spec["episode"]["start"]
        dur = spec["episode"]["dur"] if "dur" in spec["episode"] else 10
        if "yPos" in spec["episode"]:
            textBaseY = spec["episode"]["yPos"]
        ed = writeScrollText("episode %d" % number, vf, startTime, dur, textBaseX, textBaseY + 50, episodeColour, episodeBorderColour)
        writeText(title, vf, startTime + 3, ed - 3, 100, textBaseX, textBaseY + scrollTextSize + 50, episodeColour, episodeBorderColour)

    if "commentary" in spec:
        for commentary in spec["commentary"]:
            baseY = commentary["yPos"] if "yPos" in commentary else textBaseY
            commentaryColour = commentary["colour"] if "colour" in commentary else masterColour
            commentaryBorderColour = commentary["borderColour"] if "borderColour" in commentary else masterBorderColour
            writeScrollText(commentary["text"], vf, startFrom(commentary["start"]), int(commentary["dur"]), textBaseX, baseY + 50, commentaryColour, commentaryBorderColour)

    #endingTextStart = totalRunningTime - (int(spec["endingTextStart"]) if "endingTextStart" in spec else 13)
    #madeByDur = writeScrollText("@randomatones", vf, endingTextStart, 10, textBaseX, textBaseY, madeByColour)


def applyFadeTo(vf, totalRunningTime):
    fade_in = 1
    fade_out = 3
    vf.append(f"fade=type=in:duration={fade_in},fade=type=out:duration={fade_out}:start_time={totalRunningTime - fade_out}")

