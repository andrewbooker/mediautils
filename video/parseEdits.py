#!/usr/bin/env python3

import json
import os
import sys

def load(f):
    with open(f, "r") as e:
        return json.load(e)

edits = load(sys.argv[1])
j = load(sys.argv[2])

aliases = {}
names = {}
lengths = {}
for a in j["aliases"]:
    n = j["aliases"][a] if "name" not in j["aliases"][a] else j["aliases"][a]["name"]
    if "length" in j["aliases"][a]:
        lengths[n] = j["aliases"][a]["length"]
    aliases[n] = a
    names[a] = n

sync = j["sync"]

print(names)
print(lengths)

def anyOtherFrom(others, pos, s, currentAlias):
    for o in others:
        if o not in this and o in sync:
            start = pos + sync[o] - sync[currentAlias]
            dur = s - pos
            return (o, start, dur)


pos = 0
for e in edits:
    this = names[e]
    others = []
    for a in aliases:
        if e not in a:
            others.append(a)

    if "edits" in edits[e]:
        for k in edits[e]["edits"]:
            s = k["start"]
            if pos == 0:
                pos = s
            d = k["end"] - s

            if pos != s:
                print("[\"%s\", [%d, %d]]" % anyOtherFrom(others, pos, s, this))
                pos = s
            print("[\"%s\", [%d, %d], { \"splitScreenWith\": [\"apeman\", \"dragon_2\", \"apexman_1\"] }]," % (this, s, d))
            pos += d

