#!/usr/bin/env python3

import sys
import os
import json

rawDir = sys.argv[1]
seqFn = sys.argv[2]
baseOutDir = sys.argv[3]
loRes = bool(sys.argv[4]) if len(sys.argv) > 4 else False
resolution = "768x432" if loRes else "1920x1080"
horiz = int(resolution.split("x")[0])
vert = int(resolution.split("x")[1])

toMergeDir = os.path.join(baseOutDir, "toMerge")
if not os.path.exists(toMergeDir):
    os.makedirs(toMergeDir)

audioDir = os.path.join(baseOutDir, "Audio")
if not os.path.exists(audioDir):
    os.makedirs(audioDir)

storyboardDir = os.path.join(baseOutDir, "storyboard")
if not os.path.exists(storyboardDir):
    os.makedirs(storyboardDir)

def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)

j = load()
projectName = j["projectName"]
aliases = {}
lengths = {}
toRotate = []
longest = (0, "")
for a in j["aliases"]:
    n = j["aliases"][a] if "name" not in j["aliases"][a] else j["aliases"][a]["name"]
    if "length" in j["aliases"][a]:
        lengths[n] = j["aliases"][a]["length"]
        if lengths[n] > longest[0]:
            longest = (lengths[n], j["aliases"][a]["name"])
    aliases[n] = a
    if "rotate180" in j["aliases"][a] and j["aliases"][a]["rotate180"]:
        toRotate.append(n)

print(longest)
workingExt = "mov" if not loRes else "avi"
compression = "-c:v qtrle -pix_fmt rgb24" if not loRes else "-b:v 40M -c:v mpeg4 -vtag XVID"

#extract audio from sources
audioCmds = []
audioFiles = {}
for a in aliases:
    audioFiles[a] = "%s.wav" % a
    outFn = os.path.join(audioDir, audioFiles[a])
    srcFn = os.path.join(rawDir, aliases[a])
    if not os.path.exists(outFn):
        audioCmds.append("ffmpeg -i \"%s\" -ac 2 -ar 44100 -y %s" % (srcFn, outFn))

if len(audioCmds) > 0:
    with open("./extractAudio.sh", "w") as af:
        for c in audioCmds:
            af.write("%s\n" % c)
    os.chmod("./extractAudio.sh", 0o777)

seq = j["sequence"]
sync = j["sync"] if "sync" in j else None
tt = 0

def startFrom(s):
    if type(s) != str:
        return s
    spl = s.split(":")
    return (int(spl[0]) * 60) + int(spl[1])


storyboard = []
for s in seq:
    start = 0
    dur = 0
    if len(s[1]) > 1:
        start = startFrom(s[1][0])
        dur = s[1][1]
    else:
        dur = s[1][0]

    fn = "%s_%s.%s" % (s[0], "_".join([str(n) for n in [start, dur]]), workingExt)
    item = {
        "alias": s[0],
        "file": aliases[s[0]],
        "fileStart": start,
        "seqStart": tt,
        "duration": dur,
        "clipFn": fn
    }
    if len(s) > 2 and not type(s[2]) is str:
        if "multiplySpeed" in s[2]:
            item["multiplySpeed"] = float(s[2]["multiplySpeed"])
        if "reverse" in s[2]:
            item["reverse"] = True
        if "splitScreenWith" in s[2]:
            item["splitScreenWith"] = s[2]["splitScreenWith"]
            item["clipFn"] = "split_%s" % fn
        if "splitVerticalWith" in s[2]:
            item["splitVerticalWith"] = s[2]["splitVerticalWith"]
            item["clipFn"] = "split_%s" % fn

    item["clipFqFn"] = os.path.join(toMergeDir, item["clipFn"])
    storyboard.append(item)
    tt += dur

print("total time", tt)

#files.txt
filesFqFn = os.path.join(toMergeDir, "files.txt")
with open(filesFqFn, "w") as ff:
    for item in storyboard:
        ff.write("file '%s'\n" % item["clipFn"])

# merge
mergedDir = os.path.join(baseOutDir, "merged")
if not os.path.exists(mergedDir):
    os.makedirs(mergedDir)

mergeCmd = ["ffmpeg -f concat -safe 0 -i"]
mergeCmd.append(filesFqFn)
mergeCmd.append("-c copy -y")
mergedFn = os.path.join(mergedDir, "merged.%s" % workingExt)
mergeCmd.append(mergedFn)
with open("./merge.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mergeCmd))
os.chmod("./merge.sh", 0o777)

#audio cues
audioCues = []
for item in storyboard:
    audioCue = {}
    audioCue["file"] = audioFiles[item["alias"]]
    audioCue["mixStart"] = item["seqStart"]
    audioCue["fileStart"] = item["fileStart"]
    audioCue["duration"] = item["duration"]
    audioCues.append(audioCue)

with open(os.path.join(audioDir, "cues.json"), "w") as ac:
    json.dump(audioCues, ac, indent=4)

#direct mix audio cues synced with longest item
directMix = []
lastEntryTime = 0
directMixStoryboard = [item for item in filter(lambda i: i["alias"] == longest[1], storyboard)]
for i in range(len(directMixStoryboard)):
    item = directMixStoryboard[i]
    audioCue = {}
    audioCue["file"] = "direct_mix.wav"
    audioCue["mixStart"] = item["seqStart"]
    audioCue["fileStart"] = item["fileStart"]
    if (i + 1) < len(directMixStoryboard):
        audioCue["duration"] = directMixStoryboard[i + 1]["seqStart"] - item["seqStart"]
    else:
        audioCue["duration"] = item["duration"]
    directMix.append(audioCue)

with open(os.path.join(audioDir, "direct_mix.json"), "w") as ac:
    json.dump(directMix, ac, indent=4)


#compile
from projects.addText import writeSmallText
import math

def asTime(t):
    return "%02d\:%02d" % (math.floor(t / 60), t % 60)

cmds = []
for item in storyboard:
    if not os.path.exists(item["clipFqFn"]):
        if "splitScreenWith" not in item and "splitVerticalWith" not in item:
            cmd = ["ffmpeg"]
            if item["fileStart"]:
                cmd.append("-ss")
                cmd.append(str(item["fileStart"]))
            cmd.append("-i")
            cmd.append("\"%s\"" % os.path.join(rawDir, item["file"]))
            cmd.append("-t")
            cmd.append(str(item["duration"]))
            cmd.append("-an -r 30 -y")
            cmd.append(compression)

            vf = []
            if item["alias"] in toRotate:
                vf.append("vflip")
                vf.append("hflip")
            vf.append("scale=%s" % resolution)
            if "multiplySpeed" in item:
                vf.append("setpts=%.2f*PTS" % (1.0 / item["multiplySpeed"]))

            if loRes:
                startMins = item["fileStart"] % 60
                sceneDesc = "%s %s (%s) %s %s" % (asTime(item["seqStart"]), item["alias"], asTime(item["fileStart"]), item["fileStart"], item["duration"])
                writeSmallText(sceneDesc, vf, 20, 20, 20, 0, item["duration"], "0x90EE90")

            if len(vf):
                cmd.append("-vf")
                cmd.append("\"%s\"" % ",".join(vf))

            if "reverse" in item:
                revFqFn = os.path.join(toMergeDir, "rev_%s" % item["clipFn"])
                cmd.append(revFqFn)
                cmds.append(" ".join(cmd))
                cmds.append("ffmpeg -i %s %s -vf \"reverse\" -y %s" % (revFqFn, compression, item["clipFqFn"]))
                cmds.append("rm %s" % revFqFn)
            else:
                cmd.append(item["clipFqFn"])
                cmds.append(" ".join(cmd))

        else:
            srcs = [item["file"]]
            primarySync = sync[item["alias"]]
            ss = [item["fileStart"]]
            splits = item["splitScreenWith"] if "splitScreenWith" in item else item["splitVerticalWith"]
            for s in splits:
                syncKey = s.split("_")[0]
                ss.append(item["fileStart"] + sync[syncKey] - primarySync)
                srcs.append(aliases[s])

            splitSrcs = []
            for i in range(len(srcs)):
                s = srcs[i]

                sCmd = ["ffmpeg"]
                sCmd.append("-ss %d" % ss[i])
                sCmd.append("-i")
                sCmd.append("\"%s\"" % os.path.join(rawDir, s))
                sCmd.append("-t %d" % item["duration"])

                if "splitVerticalWith" in item and i == 0:
                    sCmd.append("-vf \"scale=%s,crop=%d:%d:0:0\"" % (resolution, horiz / 2, vert))
                else:
                    sCmd.append("-vf \"scale=%dx%d\"" % (horiz / 2, vert / 2))

                sCmd.append("-an -r 30 -y")
                sCmd.append(compression)
                sfqfn = os.path.join(toMergeDir, "split_%d.%s" % (i, workingExt))
                splitSrcs.append(sfqfn)
                sCmd.append(sfqfn)

                cmds.append(" ".join(sCmd))

            mCmd = ["ffmpeg"]
            for i in range(len(srcs)):
                mCmd.append("-i")
                mCmd.append(os.path.join(toMergeDir, "split_%d.%s" % (i, workingExt)))
            fc = []
            if "splitVerticalWith" in item:
                fc.append("[1][2]vstack[right]")
                fc.append("[0][right]hstack[out]")
            else:
                fc.append("[0][1]hstack[top]")
                fc.append("[2][3]hstack[bottom]")
                fc.append("[top][bottom]vstack[out]")

            mCmd.append("-filter_complex \"%s\"" % ";".join(fc))
            mCmd.append("-map \"[out]\" -y")
            mCmd.append("-an -r 30 -y")
            mCmd.append(compression)
            mCmd.append(item["clipFqFn"])
            cmds.append(" ".join(mCmd))

            for s in splitSrcs:
                cmds.append("rm %s" % s)


with open("./compile.sh", "w") as cf:
    for c in cmds:
        cf.write("%s\n" % c)
os.chmod("./compile.sh", 0o777)


#text
def rgbToHex(rgb):
	return "0x%s" % "".join(["%02x" % i for i in rgb])

number = j["number"]

vf = []
from projects.addText import applyTextTo, applyFadeTo
applyFadeTo(vf, tt)
if not loRes and "text" in j:
    spec = j["text"]
    spec["title"] = projectName
    spec["tt"] = tt
    spec["number"] = number
    applyTextTo(vf, spec)

baseOutFn = projectName.lower().replace(" ", "_")
mp4Cmd = ["ffmpeg -i"]
mp4Cmd.append(mergedFn)
soundtrackFqFn = os.path.join(mergedDir, "soundtrack.wav")
if os.path.exists(soundtrackFqFn):
    mp4Cmd.append("-i")
    mp4Cmd.append(soundtrackFqFn)
    mp4Cmd.append("-b:a 192k")
mp4Cmd.append("-t")
mp4Cmd.append(str(tt))
if len(vf):
    mp4Cmd.append("-vf")
    mp4Cmd.append("\"%s\"" % ",".join(vf))

mp4Cmd.append("-y")
mp4Cmd.append(os.path.join(mergedDir, "%s.mp4" % baseOutFn))

with open("./toMp4.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mp4Cmd))
os.chmod("./toMp4.sh", 0o777)


import datetime
with open("./toStoryboard.sh", "w") as cf:
    for s in storyboard:
        startAsTime = str(datetime.timedelta(seconds=int(s["seqStart"])))[-4:].replace(":", "-")
        fn = "%d_%s_%s_%d_%d.bmp" % (s["seqStart"], startAsTime, s["alias"], s["fileStart"], s["duration"])
        cf.write("ffmpeg -i %s -vf \"select=eq(n\,0)\" -vframes 1 %s\n" % (s["clipFqFn"], os.path.join(storyboardDir, fn)))
os.chmod("./toStoryboard.sh", 0o777)
