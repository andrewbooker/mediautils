#!/usr/bin/env python3

import sys
import os
import json

rawDir = sys.argv[1]
seqFn = sys.argv[2]
outDir = sys.argv[3]

def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)

j = load()
aliases = {}
for a in j["aliases"]:
    n = j["aliases"][a] if "name" not in j["aliases"][a] else j["aliases"][a]["name"]
    aliases[n] = a

seq = j["sequence"]


files = []
cmds = []
seqNum = 0
tt = 0
for s in seq:
    cmd = ["ffmpeg"]
    cmd.append("-i")
    cmd.append(os.path.join(rawDir, aliases[s[0]]))
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
    cmd.append("\"scale=768:432\"")

    fn = os.path.join(outDir, "%s_%03d.avi" % (s[0], seqNum))
    cmd.append(fn)
    seqNum += 1

    files.append("file '%s'" % fn)
    cmds.append(" ".join(cmd))

cmdFqFn = os.path.join(outDir, "compile.sh")
with open(cmdFqFn, "w") as cf:
    for c in cmds:
        cf.write("%s\n" % c)
os.chmod(cmdFqFn, 0o777)

filesFqFn = os.path.join(outDir, "files.txt")
with open(filesFqFn, "w") as ff:
    for f in files:
        ff.write("%s\n" % f)

print("total time", tt)

mergeCmd = ["ffmpeg -f concat -safe 0 -i"]
mergeCmd.append(filesFqFn)
#mergeCmd.append("-t")
#mergeCmd.append(str(tt))

#this has to go in the mp4 stage, as it cannot be used in conjunction with -c copy
#mergeCmd.append("-vf")
#mergeCmd.append("\"fade=type=in:duration=1,fade=type=out:duration=4:start_time=%d\"" % (tt - 4))

mergeCmd.append("-c copy -y")
mergeCmd.append(os.path.join(outDir, "merged.avi"))
print(" ".join(mergeCmd))

