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
for a in j["aliases"]:
    n = j["aliases"][a] if "name" not in j["aliases"][a] else j["aliases"][a]["name"]
    if "length" in j["aliases"][a]:
        lengths[n] = j["aliases"][a]["length"]
    aliases[n] = a
    if "rotate180" in j["aliases"][a] and j["aliases"][a]["rotate180"]:
        toRotate.append(n)

workingExt = "mov" if not loRes else "avi"
compression = "-c:v qtrle -pix_fmt rgb24" if not loRes else "-b:v 40M -c:v mpeg4 -vtag XVID"

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

seq = j["sequence"]
sync = j["sync"]
tt = 0
storyboard = []
for s in seq:
    start = 0
    dur = 0
    if len(s[1]) > 1:
        start = s[1][0]
        dur = s[1][1]
    else:
        dur = s[1][0]

    startDur = "_".join([str(i) for i in s[1]])
    fn = "%s_%s.%s" % (s[0], startDur, workingExt)
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
        if "splitScreenWith" in s[2]:
            item["splitScreenWith"] = s[2]["splitScreenWith"]
            item["clipFn"] = "split_%s" % fn

    item["clipFqFn"] = os.path.join(toMergeDir, item["clipFn"])
    storyboard.append(item)
    tt += dur

print("total time", tt)

filesFqFn = os.path.join(toMergeDir, "files.txt")
with open(filesFqFn, "w") as ff:
    for item in storyboard:
        ff.write("file '%s'\n" % item["clipFn"])

mergedDir = os.path.join(baseOutDir, "merged")
if not os.path.exists(mergedDir):
    os.makedirs(mergedDir)

mergeCmd = ["ffmpeg -f concat -safe 0 -i"]
mergeCmd.append(filesFqFn)
mergeCmd.append("-c copy -y")
mergedFn = os.path.join(mergedDir, "merged.%s" % workingExt)
mergeCmd.append(mergedFn)

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


cmds = []
for item in storyboard:
    if not os.path.exists(item["clipFqFn"]):
        if "splitScreenWith" not in item:
            cmd = ["ffmpeg"]
            cmd.append("-i")
            cmd.append("\"%s\"" % os.path.join(rawDir, item["file"]))
            if item["fileStart"]:
                cmd.append("-ss")
                cmd.append(str(item["fileStart"]))
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

            if len(vf):
                cmd.append("-vf")
                cmd.append("\"%s\"" % ",".join(vf))
            cmd.append(item["clipFqFn"])

            cmds.append(" ".join(cmd))

        if "splitScreenWith" in item:
            srcs = [item["file"]]
            primarySync = sync[item["alias"]]
            ss = [item["fileStart"]]
            for s in item["splitScreenWith"]:
                syncKey = s.split("_")[0]
                lengthIteration = int(s.split("_")[1]) - 1 if len(s.split("_")) > 1 else 0
                passedLength = 0
                for i in range(lengthIteration):
                    passedLength += lengths["%s_%d" % (syncKey, i + 1)]
                ss.append(item["fileStart"] + sync[syncKey] - passedLength - primarySync)
                srcs.append(aliases[s])

            for i in range(len(srcs)):
                s = srcs[i]
                sCmd = ["ffmpeg -i"]
                sCmd.append("\"%s\"" % os.path.join(rawDir, s))
                sCmd.append("-ss %d" % ss[i])
                sCmd.append("-t %d" % item["duration"])
                sCmd.append("-vf \"scale=%dx%d\"" % (horiz / 2, vert / 2))
                sCmd.append("-an -r 30 -y")
                sCmd.append(compression)
                sCmd.append(os.path.join(toMergeDir, "split_%d.%s" % (i, workingExt)))

                cmds.append(" ".join(sCmd))

            mCmd = ["ffmpeg"]
            for i in range(len(srcs)):
                mCmd.append("-i")
                mCmd.append(os.path.join(toMergeDir, "split_%d.%s" % (i, workingExt)))
            fc = []
            fc.append("[0][1]hstack[top]")
            fc.append("[2][3]hstack[bottom]")
            fc.append("[top][bottom]vstack[out]")

            mCmd.append("-filter_complex \"%s\"" % ";".join(fc))
            mCmd.append("-map \"[out]\" -y")
            mCmd.append("-an -r 30 -y")
            mCmd.append(compression)
            mCmd.append(item["clipFqFn"])
            cmds.append(" ".join(mCmd))



with open("./compile.sh", "w") as cf:
    for c in cmds:
        cf.write("%s\n" % c)

with open("./merge.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mergeCmd))

#text
def rgbToHex(rgb):
	return "0x%s" % "".join(["%02x" % i for i in rgb])

number = j["number"]
txtConf = {
    "nameStart": 4,
    "nameDur": 10,
    "titleStart": 15,
    "titleDur": 10,
    "madeByStart": -16,
    "madeByDur": 12
}
fonts = {
	"impact": "/usr/local/share/fonts/impact.ttf",
	"arial": "/usr/local/share/fonts/arial.ttf"
}
nameCol = txtConf["nameCol"] if "nameCol" in txtConf else [255, 255, 255]
titleCol = txtConf["titleCol"] if "titleCol" in txtConf else [255, 255, 255]
titleSize = int(txtConf["titleSize"]) if "titleSize" in txtConf else 100
madeByCol = txtConf["madeByCol"] if "madeByCol" in txtConf else [255, 255, 255]
madeByAbCol = txtConf["madeByAbCol"] if "madeByAbCol" in txtConf else [255, 255, 255]
madeByXy = txtConf["madeByXy"] if "madeByXy" in txtConf else [60, 730]
madeByAbXy = txtConf["madeByXy"] if "madeByXy" in txtConf else [60, 810]
madeByStart = int(txtConf["madeByStart"]) if "madeByStart" in txtConf else -16
if madeByStart < 0:
	madeByStart += int(tt)

instr = [
	{"text": "Randomatones #%s" % number, "start": int(txtConf["nameStart"]), "dur": int(txtConf["nameDur"]), "rgb": nameCol, "x": 60, "y": 880, "size": 120},
	{"text": projectName, "start": int(txtConf["titleStart"]), "dur": int(txtConf["titleDur"]), "rgb": titleCol, "x": 60, "y": 880, "size": titleSize},
	{"text": "made by", "start": madeByStart, "dur": int(txtConf["madeByDur"]), "rgb": madeByCol, "x": madeByXy[0], "y": madeByXy[1], "size": 80, "font": "arial"},
	{"text": "Andrew Booker", "start": madeByStart, "dur": int(txtConf["madeByDur"]), "rgb": madeByAbCol, "x": madeByAbXy[0], "y": madeByAbXy[1], "size": 100}
] if not loRes else []

vf = []
for i in instr:
	font = i["font"] if "font" in i else "impact"
	colour = rgbToHex(i["rgb"])
	vf.append("drawtext=enable=between(t\\,%d\\,%d):text='%s':fontcolor=%s:x=%d:y=%d:fontsize=%d:fontfile=%s" % (i["start"], i["start"] + i["dur"], i["text"], colour, i["x"], i["y"], i["size"], fonts[font]))

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
    mp4Cmd.append("\"fade=type=in:duration=6,fade=type=out:duration=4:start_time=%d,%s\"" % (tt - 4, ",".join(vf)))
mp4Cmd.append("-y c:v libx264 -qp 0 -f mp4")
mp4Cmd.append(os.path.join(mergedDir, "%s.mp4" % baseOutFn))

with open("./toMp4.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mp4Cmd))

os.chmod("./compile.sh", 0o777)
os.chmod("./extractAudio.sh", 0o777)
os.chmod("./merge.sh", 0o777)
os.chmod("./toMp4.sh", 0o777)

import datetime
with open("./toStoryboard.sh", "w") as cf:
    for s in storyboard:
        startAsTime = str(datetime.timedelta(seconds=int(s["seqStart"])))[-4:].replace(":", "-")
        fn = "%d_%s_%s_%d_%d.bmp" % (s["seqStart"], startAsTime, s["alias"], s["fileStart"], s["duration"])
        cf.write("ffmpeg -i %s -vf \"select=eq(n\,0)\" -vframes 1 %s\n" % (s["clipFqFn"], os.path.join(storyboardDir, fn)))
os.chmod("./toStoryboard.sh", 0o777)
