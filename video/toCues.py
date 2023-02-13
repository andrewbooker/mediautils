#!/usr/bin/env python3
import sys
import os
import json
import datetime

seq = []
with open(sys.argv[1], "r") as sf:
    j = json.load(sf)
    seq = j["sequence"]

t = 0
for s in seq:
    p = []
    p.append(s[0])
    p.append(str(s[1][0]))
    p.append(str(s[1][1]))
    p.append("%d (%s)" % (t, str(datetime.timedelta(seconds=t))[-4:]))

    print(", ".join(p))
    t += s[1][1]

