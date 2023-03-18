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

class SourceSeqs():
    def __init__(self):
        self.start = {}
        self.end = {}
        for alias in lengths:
            spl = alias.split("_")
            syncKey = spl[0]

            if syncKey in sync:
                if len(spl) > 1 and int(spl[1]) > 1:
                    prevKey = "%s_%d" % (syncKey, int(spl[1]) - 1)
                    self.start[alias] = self.end[prevKey]
                else:
                    self.start[alias] = sync[syncKey]
                self.end[alias] = self.start[alias] + lengths[alias]
                print(alias, self.start[alias], self.end[alias])

    def availableLengthAt(self, t, alias, currentAlias):
        if alias in self.start and t >= self.start[alias] and t < self.end[alias]:
            available = self.end[alias] - t
            if available > 0:
                return available
        return 0

sourceSeqs = SourceSeqs()

def listOptionsFrom(others, pos, currentAlias):
    r = []
    for o in others:
        t = pos - sync[currentAlias]
        available = sourceSeqs.availableLengthAt(t, o, currentAlias)
        if available and o not in currentAlias  :
            r.append((o, available))
    return r

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
                print("between split screen at", pos - sync[this], ":", listOptionsFrom(others, pos, this))
                print("[\"%s\", [%d, %d]]" % anyOtherFrom(others, pos, s, this))
                pos = s

            splitOptions = listOptionsFrom(others, pos, this)
            availableDur = d
            for o in splitOptions:
                if o[1] < availableDur:
                    availableDur = o[1]
            ssw = { "splitScreenWith": [o[0] for o in splitOptions] }

            print("[\"%s\", [%d, %0.2f], %s]," % (this, pos, availableDur, json.dumps(ssw)))
            pos += availableDur
            if availableDur != d:
                print("[\"%s\", [%0.2f, %0.2f], %s]," % (this, pos, d - availableDur, json.dumps({ "splitScreenWith": [o[0] for o in listOptionsFrom(others, pos, this)] })))
            pos += (d - availableDur)

