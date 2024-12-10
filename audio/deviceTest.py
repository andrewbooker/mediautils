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

use_pg = device < 2
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
    vol = level
    if i > sampleRate and i < rampUpFinish:
        vol *= ((i - sampleRate) / rampTime)
    elif i > rampDownStart and i < (totalDur - sampleRate):
        vol *= (1.0 - ((i - rampDownStart) / rampTime))

    for c in range(channels):
        if i < sampleRate or i > (sampleRate * (durSecs + 1)):
            sample.append(0.0)
        else:
            v = 1.0 + (0.5 * (math.sin(i * fHz * 2 * math.pi * (1.0 + detune[c]) / (1.0 * sampleRate))))
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
    import numpy
    
    devices = ["PCM2902 Audio Codec Analog Stereo", "High Definition Audio Controller Digital Stereo (HDMI 2)"]
    
    print("initialising pygame")
    print("initialising mixer")
    pg.mixer.pre_init(devicename=devices[device], frequency=sampleRate, size=-16, channels=8, buffer=1024)
    pg.init()
    pg.mixer.init()
    pg.mixer.set_num_channels(1) # simultaneous notes
    
    print(len(sound))
    print("converting buffer to byte array")
    buf = numpy.zeros(len(sound), dtype = numpy.int16)
    max_sample = 2**(16 - 1) - 1
    print(max_sample)
    for s in range(len(sound)):
        for c in range(channels):
            buf[s] = int(max_sample * sound[s][c])
    
    print(len(buf))
    print("creating pg sound")
    pgs = pg.mixer.Sound(array=buf)    
    print("selecting a channel")
    channel = pg.mixer.find_channel()
    channel.set_volume(level)
    print("playing")
    channel.play(pgs)
    print("waiting to stop")    
    time.sleep(durSecs + 3)
    pg.quit()
            

