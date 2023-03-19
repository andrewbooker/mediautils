#!/usr/bin/env python3

import json
import os
import sys
from timeline import Timeline

inDir = sys.argv[1]

def load(f):
    with open(f, "r") as e:
        return json.load(e)

edits = load(os.path.join(inDir, "edits.json"))
sources = load(os.path.join(inDir, "sequence.json"))["aliases"]

timeline = Timeline(sources, edits)

[print(t) for t in timeline.create()]
