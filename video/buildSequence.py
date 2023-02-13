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

seq = j["sequence"]
files = []
cmds = []
tt = 0
for s in seq:
    cmd = ["ffmpeg"]
    cmd.append("-i")
    cmd.append("\"%s\"" % os.path.join(rawDir, aliases[s[0]]))
    startDur = "_".join([str(i) for i in s[1]])
    if len(s[1]) > 1:
        cmd.append("-ss")
        cmd.append(str(s[1][0]))
        cmd.append("-t")
        cmd.append(str(s[1][1]))
        tt += s[1][1]
    else:
        cmd.append("-t")
        cmd.append(str(s[1][0]))
        tt += s[1][0]
    cmd.append("-an -b:v 40M -c:v mpeg4 -vtag XVID -r 30 -y")
    cmd.append("-vf")
    vf = []
    if s[0] in toRotate:
        vf.append("vflip")
        vf.append("hflip")
    vf.append("scale=%s" % resolution)
    cmd.append("\"%s\"" % ",".join(vf))

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
#look for soundtrack in merged dir, if present add as -i followed by -b:a 192k
mp4Cmd.append("-t")
mp4Cmd.append(str(tt))
mp4Cmd.append("-vf")
mp4Cmd.append("\"fade=type=in:duration=4,fade=type=out:duration=4:start_time=%d\"" % (tt - 4)) # add text commands to this
mp4Cmd.append("-y")
mp4Cmd.append(os.path.join(mergedDir, "%s.mp4" % projectName.lower().replace(" ", "_")))

with open("./toMp4.sh", "w") as cf:
    cf.write("\n%s\n" % " ".join(mp4Cmd))

os.chmod("./compile.sh", 0o777)
os.chmod("./merge.sh", 0o777)
os.chmod("./toMp4.sh", 0o777)

