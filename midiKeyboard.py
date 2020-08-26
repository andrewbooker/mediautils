#!/usr/bin/env python

from mididevices import UsbMidiDevices, MidiOut
import sys


midiDevices = UsbMidiDevices()
midiOut = MidiOut(midiDevices)
channel = 0
note = 0

done = False
for line in sys.stdin:
    if note > 0:
        midiOut.io.note_off(note, velocity=0, channel=channel)

    l = line.strip()
    if "q" == l:
        break

    if l.isdigit():
        n = int(l)
        if n != note:
            note = n
            midiOut.io.note_on(note, velocity=100, channel=channel)
    else:
        note = 0

del midiOut
del midiDevices
