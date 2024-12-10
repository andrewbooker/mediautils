#!/usr/bin/env python

import sounddevice as sd
import math
import sys
import time
import random

print(sd.query_devices())

device = int(sys.argv[1]) if len(sys.argv) > 1 else None
channels = int(sys.argv[2]) if len(sys.argv) > 2 else 1
level = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0


if device is None:
    exit()

use_pg = False
sound = []
sampleRate = 44100
durSecs = 3
fHz = 220


detune = []
for c in range(channels):
    detune.append(-0.005 + (0.01 * (random.random() * 0.5)))

totalDur = sampleRate * (durSecs + 2.0)
rampTime = sampleRate * durSecs * 0.25
rampUpFinish = sampleRate + rampTime
rampDownStart = totalDur - (sampleRate + rampTime)

for i in range(int(totalDur)):
    sample = []
    for c in range(channels):
        if i < sampleRate or i > (sampleRate * (durSecs + 1)):
            sample.append(0.0)
        else:
            v = 1.0 + (0.5 * (math.sin(i * fHz * 2 * math.pi * (1.0 + detune[c]) / (1.0 * sampleRate))))
            vol = level
            if i > sampleRate and i < rampUpFinish:
                vol *= ((i - sampleRate) / rampTime)
            elif i > rampDownStart and i < (totalDur - sampleRate):
                vol *= (1.0 - ((i - rampDownStart) / rampTime))
            sample.append(v * vol)
    sound.append(sample)

print("using device", device)

if not use_pg:
    sd.default.channels = channels
    sd.default.device = device

    sd.play(sound, sampleRate)
    print("playing")
    time.sleep(len(sound) / (1.0 * sampleRate))
    print("stopping")
else:
    import pygame as pg
    import numpy as np
    
    print("initialising pygame")
    pg.init()
    print("initialising mixer")
    pg.mixer.init(frequency=sampleRate, size=-16, channels=channels, buffer=1024, devicename="HDA NVidia: HDMI 0 (hw:1,7), ALSA (0 in, 8 out)")
    pg.mixer.set_num_channels(3) # simultaneous notes
    
    print("converting buffer to byte array")
    cs = []
    for c in range(channels):
        cs.append([s[c] for s in sound])
    print(len(cs))
    print(len(sound))
    ba = np.array(cs)
    print("creating pg sound")
    pgs = pg.mixer.Sound(array=ba)
    
    print("selecting a channel")
    channel = pg.mixer.find_channel()
    channel.set_volume(level)
    print("playing")
    channel.play(pgs)
    print("waiting to stop")    
    time.sleep(3)
    pg.quit()
            

