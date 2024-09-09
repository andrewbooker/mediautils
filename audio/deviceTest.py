#!/usr/bin/env python

import sounddevice as sd
import math
import sys
import time
import random

print(sd.query_devices())

device = int(sys.argv[1]) if len(sys.argv) > 1 else None
channels = int(sys.argv[2]) if len(sys.argv) > 1 else 1

if device is None:
    exit()

sound = []
sampleRate = 44100
durSecs = 2
fHz = 200
level = 0.5


detune = []
for c in range(channels):
    detune.append(-0.005 + (0.01 * (random.random() * 0.5)))

for i in range(sampleRate * durSecs):
    sample = []
    for c in range(channels):
        v = 1.0 + (0.5 * (math.sin(i * fHz * 2 * math.pi * (1.0 + detune[c]) / (1.0 * sampleRate))))
        sample.append(v * level)
    sound.append(sample)

sd.default.channels = channels
sd.default.device = device

sd.play(sound, sampleRate)
time.sleep(len(sound) / (1.0 * sampleRate))

print("using device", device)
