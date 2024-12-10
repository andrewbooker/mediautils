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

use_pg = True
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

print("using device", device)

if not use_pg:
    sd.default.channels = channels
    sd.default.device = device

    sd.play(sound, sampleRate)
    time.sleep(len(sound) / (1.0 * sampleRate))
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
            

