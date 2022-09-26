#!/usr/bin/env python

import sounddevice as sd
import math
import sys
import time

print(sd.query_devices())

device = int(sys.argv[1]) if len(sys.argv) > 1 else None

if device is None:
    exit()

sound = []
sampleRate = 44100
durSecs = 2
fHz = 200

for i in range(sampleRate * durSecs):
    sound.append(1.0 + (0.5 * (math.sin(i * fHz * 2 * math.pi / (1.0 * sampleRate)))))

sd.default.channels = 1
sd.default.device = device

sd.play(sound, sampleRate)
time.sleep(len(sound) / (1.0 * sampleRate))

print("using device", device)
