#!/usr/bin/env python3

import os
import sys
import re
import json

files = os.listdir(sys.argv[1])
title = sys.argv[2]
number = int(sys.argv[3])

patterns = [
    (r"202[3-9]_[0-9]{4}_.*\.MOV", "apeman"),
    (r"FILE.*\.MOV", "apexman"),
    (r"NORM.*\.MP4", "dragon"),
    (r"[0-9]{8}_[0-9]{6}\.mp4", "G5")
]


out = {
    "projectName": title,
    "number": number,
    "aliases": {},
    "sequence": []
}

aliasCount = {}

for f in files:
    for p in patterns:
        if len(re.findall(p[0], f)):
            if p[1] not in aliasCount:
                aliasCount[p[1]] = 0
            aliasCount[p[1]] += 1
            out["aliases"][f] = "%s_%d" % (p[1], aliasCount[p[1]])

print(json.dumps(out, indent=4))
