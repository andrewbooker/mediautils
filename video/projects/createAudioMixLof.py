#!/usr/bin/env python3
import json
import os
import sys

def load(f):
    with open(f, "r") as e:
        return json.load(e)

def str_to_secs(s):
    if ":" not in s:
        return float(s)
    spl = [s for s in reversed(s.split(":"))]
    total = 0.0
    for i in range(len(spl)):
        total += pow(60, i) * float(spl[i])
    return total

inDir = sys.argv[1]
outDir = sys.argv[2]
mixdownFn = sys.argv[3]

seq_json = load(os.path.join(inDir, "sequence.json"))
audio_sync = seq_json["audioSync"]
seq = seq_json["sequence"]
audio_base_sync = float(audio_sync["audioMixdown"])

cues = []
start = 0
for s in seq:
    dur = s[1][1]
    segment = {
        "file": "NP2_1.wav",
        "mixStart": start,
        "fileStart": 0,
        "duration": s[1][1]
    }
    src = s[0]
    file_secs = str_to_secs(str(s[1][0]))

    sync = audio_sync[s[0]] if s[0] in audio_sync else None
    if sync is None:
        segment["file"] = f"{src}.wav"
        segment["fileStart"] = file_secs
    else:
        segment["file"] = mixdownFn
        sync_audio_mix = (file_secs - sync) + audio_base_sync
        segment["fileStart"] = sync_audio_mix

    cues.append(segment)
    start += dur
    print(segment)

with open(os.path.join(outDir, "mixdown_cues.json"), "w") as outF:
    json.dump(cues, outF, indent=4)
