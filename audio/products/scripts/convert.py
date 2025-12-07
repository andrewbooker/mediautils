#!/usr/bin/env python


import sys
import os
from datetime import datetime

#runs a command such as:
#ffmpeg -i in.mp3 -i test.png -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" out.mp3

inDir = sys.argv[1]
outDir = sys.argv[2]
artworkFn = sys.argv[3]
files = [f for f in filter(lambda f: ".wav" in f, os.listdir(os.path.join(inDir, "wav")))]
year = datetime.strftime(datetime.now(), "%Y")


def metadata(cmd, k, v):
    cmd.append("-metadata")
    cmd.append("%s=\"%s\"" % (k, v))

for i in range(len(files)):
    f = files[i]
    cmd = ["ffmpeg -i"]
    cmd.append(os.path.join(inDir, "wav", f))
    cmd.append("-i")
    cmd.append(artworkFn)
    cmd.append("-map 0:0 -map 1:0")
    cmd.append("-id3v2_version 3")
    metadata(cmd, "album", "Randomatones Volume Two")
    metadata(cmd, "title", " ".join(["%s%s" % (t[0].upper(), t[1:]) for t in f.split(".")[0].split("_")[1:]]))
    metadata(cmd, "track", "%d/%d" % (i + 1, len(files)))
    metadata(cmd, "artist", "Andrew Booker")
    metadata(cmd, "composer", "Andrew Booker")
    metadata(cmd, "year", year)
    metadata(cmd, "genre", "ambient")

    cmd.append("-b:a 192k")
    cmd.append("-y")
    cmd.append(os.path.join(outDir, "%s.mp3" % f.split(".")[0]))

    os.system(" ".join(cmd))
