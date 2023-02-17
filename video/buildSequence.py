#!/usr/bin/env python3

import sys
import os
import json

rawDir = sys.argv[1]
seqFn = sys.argv[2]
baseOutDir = sys.argv[3]
resolution = sys.argv[4] if len(sys.argv) > 4 else "768x432"

toMergeDir = os.path.join(baseOutDir, "toMerge")
if not os.path.exists(toMergeDir):
    os.makedirs(toMergeDir)

audioDir = os.path.join(baseOutDir, "Audio")
if not os.path.exists(audioDir):
    os.makedirs(audioDir)

def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)

j = load()
projectName = j["projectName"]
aliases = {}
toRotate = []
for a in j["aliases"]:
    n = j["aliases"][a] if "name" not in j["aliases"][a] else j["aliases"][a]["name"]
    aliases[n] = a
    if "rotate180" in j["aliases"][a] and j["aliases"][a]["rotate180"]:
        toRotate.append(n)


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

audioCues = []
seq = j["sequence"]
files = []
cmds = []
tt = 0
for s in seq:
    cmd = ["ffmpeg"]
    cmd.append("-i")
    cmd.append("\"%s\"" % os.path.join(rawDir, aliases[s[0]]))

    start = 0
    dur = 0
    if len(s[1]) > 1:
        cmd.append("-ss")
        cmd.append(str(s[1][0]))
        cmd.append("-t")
        cmd.append(str(s[1][1]))
        start = s[1][0]
        dur = s[1][1]
    else:
        cmd.append("-t")
        cmd.append(str(s[1][0]))
        dur = s[1][0]

    audioCue = {}
    audioCue["file"] = audioFiles[s[0]]
    audioCue["mixStart"] = tt
    audioCue["fileStart"] = start
    audioCue["duration"] = dur
    audioCues.append(audioCue)

    tt += dur
    cmd.append("-an -b:v 40M -c:v mpeg4 -vtag XVID -r 30 -y")
    cmd.append("-vf")
    vf = []
    if s[0] in toRotate:
        vf.append("vflip")
        vf.append("hflip")
    vf.append("scale=%s" % resolution)
    cmd.append("\"%s\"" % ",".join(vf))

    startDur = "_".join([str(i) for i in s[1]])
    fn = "%s_%s.avi" % (s[0], startDur)
    fqFn = os.path.join(toMergeDir, fn)
    cmd.append(fqFn)

    files.append("file '%s'" % fn)
    if not os.path.exists(fqFn):
        cmds.append(" ".join(cmd))


filesFqFn = os.path.join(toMergeDir, "files.txt")
with open(filesFqFn, "w") as ff:
    for f in files:
        ff.write("%s\n" % f)

print("total time", tt)

with open(os.path.join(audioDir, "cues.json"), "w") as ac:
    json.dump(audioCues, ac, indent=4)


mergedDir = os.path.join(baseOutDir, "merged")
if not os.path.exists(mergedDir):
    os.makedirs(mergedDir)

mergeCmd = ["ffmpeg -f concat -safe 0 -i"]
mergeCmd.append(filesFqFn)

mergeCmd.append("-c copy -y")
mergedFn = os.path.join(mergedDir, "merged.avi")
mergeCmd.append(mergedFn)

with open("./compile.sh", "w") as cf:
    for c in cmds:
        cf.write("%s\n" % c)

with open("./merge.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mergeCmd))

mp4Cmd = ["ffmpeg -i"]
mp4Cmd.append(mergedFn)
soundtrackFqFn = os.path.join(mergedDir, "soundtrack.wav")
if os.path.exists(soundtrackFqFn):
    mp4Cmd.append("-i")
    mp4Cmd.append(soundtrackFqFn)
    mp4Cmd.append("-b:a 192k")
mp4Cmd.append("-t")
mp4Cmd.append(str(tt))
mp4Cmd.append("-vf")
mp4Cmd.append("\"fade=type=in:duration=4,fade=type=out:duration=4:start_time=%d\"" % (tt - 4)) # add text commands to this
mp4Cmd.append("-y")
mp4Cmd.append(os.path.join(mergedDir, "%s.mp4" % projectName.lower().replace(" ", "_")))

with open("./toMp4.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mp4Cmd))

os.chmod("./compile.sh", 0o777)
os.chmod("./extractAudio.sh", 0o777)
os.chmod("./merge.sh", 0o777)
os.chmod("./toMp4.sh", 0o777)

