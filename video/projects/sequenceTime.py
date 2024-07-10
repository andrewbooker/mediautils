#!/usr/bin/env python3

import sys
import os
import json

seqFn = os.path.join(sys.argv[1], "sequence.json")

def load():
    with open(seqFn, "r") as seqF:
        return json.load(seqF)

j = load()
t = 0
print(len(j["sequence"]), "scenes")
for s in j["sequence"]:
    t += s[1][1]

print(f"{int(t / 60):02d}:{t % 60:02d}")
