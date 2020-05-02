#!/usr/bin/env python

from midiFileWriter import *

def expect(v, e):
    value = int.from_bytes(v, "big")
    expected = e
    if (value == expected):
        print("Pass", expected)
    else:
        print("FAIL: expected", expected, "got", value)


m = MidiFileWriter("./ignore.mid")

#test cases from http://www.giordanobenicchi.it/midi-tech/midifile.htm

expect(m._noteLength(0), 0x0)
expect(m._noteLength(0x40), 0x40)
expect(m._noteLength(0x7f), 0x7f)
expect(m._noteLength(0x80), 0x8100)
expect(m._noteLength(0x2000), 0xC000)
expect(m._noteLength(0x3FFF), 0xFF7F)
expect(m._noteLength(0x4000), 0x818000)
expect(m._noteLength(0x100000), 0xC08000)
expect(m._noteLength(0x1FFFFF), 0xFFFF7F)
expect(m._noteLength(0x200000), 0x81808000)
expect(m._noteLength(0x08000000), 0xC0808000)
expect(m._noteLength(0x0FFFFFFF), 0xFFFFFF7F)


del m

